"""Client-Schicht: Akz. 2 (item add), 3 (Zweit-Client), 4 (GM pending).

Kern-Beweis: beide Clients teilen EINE LocalJsonStore + Char-Name;
State = fold(Events) -> derselbe Store-Log -> dieselbe Sicht.
"""
from __future__ import annotations

import pytest

from rpgpoc import events as ev
from rpgpoc.client import Client, ClientError, client_sheet
from rpgpoc.store import LocalJsonStore


@pytest.fixture
def store(tmp_path) -> LocalJsonStore:
    return LocalJsonStore(tmp_path)


def _created(char="alice", level=1) -> ev.Event:
    return ev.Event(seq=0, char=char, type=ev.CHARACTER_CREATED,
                    actor="gm", payload={"level": level, "hp": 20})


# -- Akz. 2: item add erzeugt Event, State neu berechnet --------------------

def test_item_add_appends_event_and_updates_state(store) -> None:
    c = Client(store, "alice")
    c.append(_created())
    c.item_add("Fackel")

    log = c.log()
    assert [e.type for e in log] == [ev.CHARACTER_CREATED, ev.ITEM_ADDED]
    assert [e.seq for e in log] == [1, 2]          # seq = last+1, lückenlos

    state = c.sheet()
    assert state["character_created"]["payload"]["level"] == 1
    assert [i["name"] for i in state["inventory"]] == ["Fackel"]
    assert state["inventory"][0]["id"] is not None


# -- Akz. 3: Zweit-Client liest denselben Store -> sieht die Änderung -----

def test_second_client_sees_the_change(store) -> None:
    c1 = Client(store, "finrion")
    c1.append(_created("finrion", level=3))
    c1.item_add("Kürbis")
    c1.item_add("Schwert")

    # Neuer Client (z.B. frisch gestartet) auf derselben Root:
    c2 = Client(store, "finrion")
    state = c2.sheet()
    assert [i["name"] for i in state["inventory"]] == ["Kürbis", "Schwert"]
    assert state["character_created"]["payload"]["hp"] == 20

    # ... und er sieht auch seq/log identisch:
    assert [e.seq for e in c2.log()] == [1, 2, 3]


# -- Akz. 4: GM propose -> pending -> approve ------------------------------

def test_stat_propose_pending_then_approve(store) -> None:
    player = Client(store, "bob")
    player.append(_created("bob"))
    player.stat_propose("St", 7)

    # Spieler sieht: pending
    assert player.sheet()["pending_stats"]["St"]["status"] == "pending"

    # GM-Client (anderes Client-Objekt, gleicher Store) sieht dieselbe Pending
    gm = Client(store, "bob")
    entry = gm.sheet()["pending_stats"]["St"]
    assert entry["status"] == "pending" and entry["value"] == 7

    gm.stat_approve("St", 7)
    assert gm.sheet()["pending_stats"]["St"]["status"] == "approved"

    # Spieler-Client (Replay nach Approval):
    player.mark_seen()
    assert player.sheet()["pending_stats"]["St"]["status"] == "approved"


# -- pending()/mark_seen(): Differenz-Ansatz --------------------------------

def test_pending_returns_only_new_events(store) -> None:
    c1 = Client(store, "carol")
    c1.append(_created("carol"))
    c1.item_add("Torch")

    c2 = Client(store, "carol", seen_seq=1)   # hat nur Event #1 gesehen
    pend = c2.pending()
    assert [e.type for e in pend] == [ev.ITEM_ADDED]
    assert pend[0].seq == 2

    c2.mark_seen()                            # alles acken
    assert c2.pending() == []
    assert c2.seen_seq == 2


def test_mark_seen_to_newer_than_log_is_rejected(store) -> None:
    c = Client(store, "dave")
    c.append(_created("dave"))
    with pytest.raises(ClientError, match="neuer als"):
        c.mark_seen(97)


def test_append_rejects_char_mismatch(store) -> None:
    c = Client(store, "erin")
    with pytest.raises(ClientError):
        c.append(_created("other"))           # anderes Char wird abgelehnt


def test_append_rejects_non_event(store) -> None:
    c = Client(store, "frank")
    with pytest.raises(ClientError, match="Event"):
        c.append({"seq": 1})                  # type: ignore[arg-type]


# -- client_sheet(): CLI-Komfort --------------------------------------------

def test_client_sheet_helper(tmp_path) -> None:
    st = LocalJsonStore(tmp_path)
    c = Client(st, "grace")
    c.append(_created("grace"))
    c.item_add("Krug")

    sheet, last = client_sheet(tmp_path, "grace")
    assert last == 2
    assert [i["name"] for i in sheet["inventory"]] == ["Krug"]
