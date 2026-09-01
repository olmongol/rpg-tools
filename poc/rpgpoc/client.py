"""Client-Schicht über LocalJsonStore (05 Akz. 2/3/4: Multi-Client, GM).

Zwei Clients (Spieler + Zweit-Client) teilen sich EINE Store-Root und
einen Char-Namen. Jeder ``Client`` ist eine dünne Ansage auf
``LocalJsonStore`` über eine Char-Datei:

* ``append(event)``: genau EIN Event anhängen. seq = last_seq+1.
  Append-only: es werden keine alten Events überschrieben.
* ``pending()``: Events mit seq > seen_seq -- die Differenz, die diese(r)
  Client noch nicht kennt (GM-Seite schickt sie an den Spieler).
* ``mark_seen(seq)``: Wasserstand erhöhen (Client ackt die Events).
* ``sheet()``: Reduzierter State (fold über das komplette Log) --
  State = fold(Events); beide Clients sehen dasselbe Log, also denselben
  State (das ist der Multi-Client-Beweis).

``client_sheet(root, char)``: Rekonstruktion ohne Client-Instanz (z.B.
CLI-Snippet ``rpgpoc clientsheet <root> <char>``).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .events import Event
from .reducer import empty_state, fold
from .store import LocalJsonStore


class ClientError(Exception):
    """Kundenfehler (Typfehler, seq-Regress, unbekanntes Char)."""


class Client:
    """Ein RPG-Engine-Client auf einem LocalJsonStore für EINEN Char.

    PoC-Multi-Client-Scope: beide Clients (Spieler + Zweit-Client)
    erzeugen einen Client auf derselben LocalJsonStore mit demselben
    ``char``. State = fold(Events) -- beide sehen also exakt denselben
    Stand, unabhängig davon, wer wann was gelesen hat.
    """

    def __init__(self, store: LocalJsonStore, char: str,
                 seen_seq: int = 0) -> None:
        if not char or char in (".", ".."):
            raise ClientError(f"Char-Name fehlt oder ungültig: {char!r}")
        self._store = store
        self.char = char
        self.seen_seq = int(seen_seq)

    # -- Log-Zugriff (read-only) ------------------------------------------

    def log(self) -> List[Event]:
        """Komplettes Char-Log (Chronologie, ungefiltert)."""
        return list(self._store.read_log(self.char))

    def last_seq(self) -> int:
        max_seq = 0
        for e in self._store.read_log(self.char):
            if e.seq > max_seq:
                max_seq = e.seq
        return max_seq

    # -- Append (Single-Writer) --------------------------------------------

    def append(self, event: Event) -> Event:
        """EIN Event anhängen (seq = last_seq+1) und als gesehen markieren.

        Single-Writer-Modell: ein Client schreibt auf einen Char. Die
        LocalJsonStore hält eine pro-char Lock für Prozess-localen
        Parallelzugriff (Tests/Threads).
        """
        if not isinstance(event, Event):
            raise ClientError(f"Event erwartet, habe {type(event)!r}")
        if event.char != self.char:
            raise ClientError(
                f"Event.char {event.char!r} != Client.char {self.char!r}")
        seq = self.last_seq() + 1
        # Event is frozen: replace seq to the store-assigned one.
        import dataclasses
        ev = dataclasses.replace(event, seq=seq)
        self._store.append(self.char, ev)
        # sanity: die Log-Zeile ist tatsächlich da
        got = self._store.read_log(self.char)
        if not got or got[-1].seq != seq:
            raise ClientError(
                f"Append nicht sichtbar (last_seq {self.last_seq()})")
        self.seen_seq = max(self.seen_seq, seq)
        return ev

    # -- Pending / Ack -----------------------------------------------------

    def pending(self) -> List[Event]:
        """Events mit seq > seen_seq (die diesen Client betreffen).

        GM-Seite: sendt genau diese Differenz an den Spieler.
        """
        max_seq = self.last_seq()
        if self.seen_seq > max_seq:
            raise ClientError(
                f"seen_seq {self.seen_seq} neuer als Log-Ende {max_seq}")
        return [e for e in self._store.read_log(self.char)
                if e.seq > self.seen_seq]

    def mark_seen(self, seq: Optional[int] = None) -> None:
        """Wasserstand erhöhen (Client ackt die angebotenen Events).

        ``seq=None``: bis Log-Ende (alle derzeitigen Events bestätigen).
        """
        max_seq = self.last_seq()
        seq = max_seq if seq is None else int(seq)
        if seq < 0:
            raise ClientError("seq muss >= 0 sein")
        if seq > max_seq:
            raise ClientError(
                f"seen_seq {seq} neuer als Log-Ende {max_seq}")
        self.seen_seq = seq

    # -- State (Replay) ------------------------------------------------------

    def sheet(self) -> Dict[str, Any]:
        """Reduzierter State (fold) über das komplette Char-Log.

        Kern: State = fold(Events) -- beide Clients lesen dasselbe Log,
        also denselben Stand (Akz. 3: Zweit-Client sieht die Änderung).
        """
        log = self._store.read_log(self.char)
        if not log:
            return empty_state(char=self.char)
        return fold(self.char, log)

    # -- Convenience --------------------------------------------------------

    def item_add(self, name: str, actor: str = "player",
                 item_id: Optional[int] = None) -> Event:
        """Item-Event (Akz. 2: ``item add`` erzeugt Event)."""
        import uuid
        iid = item_id if item_id is not None else uuid.uuid4().int % (10 ** 8)
        return self.append(Event(
            seq=0, char=self.char, type="item_added", actor=actor,
            payload={"id": iid, "name": name}))

    def stat_propose(self, stat: str, value: int,
                     actor: str = "player") -> Event:
        """Stat-Vorschlag (Akz. 4: GM pending-Maschinerie)."""
        return self.append(Event(
            seq=0, char=self.char, type="stat_proposed", actor=actor,
            payload={"stat": stat, "value": int(value)}))

    def stat_approve(self, stat: str, value: Optional[int] = None,
                     actor: str = "gm") -> Event:
        """Stat-Zustimmung (GM-Seite)."""
        payload: Dict[str, Any] = {"stat": stat}
        if value is not None:
            payload["value"] = int(value)
        return self.append(Event(
            seq=0, char=self.char, type="stat_approved", actor=actor,
            payload=payload))


def client_sheet(root, char: str) -> Tuple[Dict[str, Any], int]:
    """(sheet, last_seq) eines Chars auf einer Store-Root.

    Komfort für CLI-Abfragen (z.B. ``python3 -m rpgpoc sheet <root> <char>``).
    """
    c = Client(LocalJsonStore(root), char)
    return c.sheet(), c.last_seq()
