"""GUI-Kern: 8-Schritt-CharGen-Wizard-Logik (05 Kriterium 8).

GUI/Logik-Entkopplung: ``CharGenWizard`` ist reine Logik (kein Qt) --
sie treibt ``rpgpoc.chargen.CharGen`` im festen 8-Schritt-Flow und
haelt den Wizard-Zustand (Cursor, Pro-Schritt Eingaben, Fehlermeldung).
Die Qt-Schicht (``rpgpoc.gui.wizard``) ist nur die Anzeige dafuer:
QWizard-Pages pro Schritt, Weiter/Back treiben ``advance()``/``back()``.
So ist der komplette Wizard-Flow offscreen- (und selbst ohne-Qt)
testbar: definition/char_def rein, ``run_all(spec)`` -> EIN
character_created-Event raus.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..chargen import CharGen, ChargenError, ChargenStepError

# Schritt-Reihenfolge = Chargen._STEPS (finale Name+finalize als 8.)
STEP_KEYS = ("race", "folk", "occupation", "stats",
             "categories", "equipment", "bgos", "finalize")

STEP_TITLES = {
    "race": "Rasse",
    "folk": "Volk",
    "occupation": "Beruf",
    "stats": "Attribute",
    "categories": "Grundkategorien",
    "equipment": "Ausruestung",
    "bgos": "BGOs",
    "finalize": "Name & Freigabe",
}


class CharGenWizardError(ValueError):
    """Wizard-Fehler (Cursor-Drift, zweites advance nach Fertig)."""


class CharGenWizard:
    """Treibt CharGen durch die 8 Schritte (reine Logik, kein Qt).

    Verwende (interaktiv):
      1. ``set(step, value)`` fuer den aktuellen Schritt
      2. ``advance()``       -> fuellt den Schritt, Cursor nach vorne
      3. ``result()``        -> character_created-Event (finalize)

    ``run_all(spec)`` -> kompletter Lauf in einem (Tests/CLI).
    """

    def __init__(self, definition: Dict[str, Any],
                 char_def: Optional[Dict[str, Any]] = None,
                 seed: Optional[int] = None) -> None:
        if not isinstance(definition, dict) or "stats" not in definition:
            raise CharGenWizardError("definition braucht 'stats'")
        self.definition = definition
        self.char_def = char_def or {}
        self._seed = seed
        self.chargen = CharGen(definition=definition,
                               char_def=self.char_def, seed=seed)
        self._cursor = 0
        self._input: Dict[str, Any] = {}
        self._error: Optional[str] = None
        self.finished_event = None

    # -- Status (fur die UI) --------------------------------------------------

    def current_step(self) -> str:
        return "done" if self._cursor >= len(STEP_KEYS) else STEP_KEYS[self._cursor]

    def steps(self) -> List[Dict[str, Any]]:
        out = []
        for i, key in enumerate(STEP_KEYS):
            status = ("done" if i < self._cursor else
                      "current" if i == self._cursor else "todo")
            out.append({"index": i, "key": key,
                        "title": STEP_TITLES[key], "status": status})
        return out

    def options(self) -> List[str]:
        """Optionen des aktuellen Schritts (Rassen / Kategorien)."""
        key = self.current_step()
        if key == "race":
            return self.chargen.race_options()
        if key == "categories":
            return [c["name"] for c in (self.definition.get("categories") or [])
                    if c.get("name")]
        return []

    def error(self) -> Optional[str]:
        return self._error

    # -- Eingabe ---------------------------------------------------------------

    def set(self, step: str, value: Any) -> None:
        """Pro-Schritt-Input hinterlegen (vor ``advance()``).

        value je Schritt:
          race/occupation/folk : str
          stats                : int (DP-Pool, Default 600)
          categories           : list[str] (mind. 1)
          equipment            : (items:list[dict], purse:int)
          bgos                 : list[dict]  ({kind,name,cost?})
          finalize             : str (Charakter-Name)
        """
        if step not in STEP_KEYS:
            raise CharGenWizardError(f"unbekannter Schritt {step!r}")
        self._input[step] = value
        self._error = None

    # -- Flow ------------------------------------------------------------------

    def advance(self) -> str:
        """Fuellen den aktuellen Schritt; liefert den erledigten key.

        Chargen-Fehler (unbekannte Rasse, Budget etc.): ``error()``
        gesetzt, Cursor bleibt stehen, Exception weitergeworfen (GUI
        kann abfassen; logik-testbar beide Wege).
        """
        key = self.current_step()
        if key == "done":
            raise CharGenWizardError("Wizard ist bereits fertig")
        v = self._input.get(key)
        try:
            if key == "race":
                self.chargen.step_race(str(v or ""))
            elif key == "folk":
                self.chargen.step_folk(str(v or ""))
            elif key == "occupation":
                self.chargen.step_occupation(str(v or ""))
            elif key == "stats":
                self.chargen.step_stats(pool=int(v if v is not None else 600))
            elif key == "categories":
                self.chargen.step_categories(list(v or []))
            elif key == "equipment":
                items, purse = (v if isinstance(v, (list, tuple))
                                and len(v) == 2 else ([], 0))
                self.chargen.step_equipment(items=list(items), purse=int(purse))
            elif key == "bgos":
                self.chargen.step_bgos(entries=list(v or []))
            elif key == "finalize":
                name = str(v or "").strip()
                self.finished_event = self.chargen.finalize(
                    name=name or None)
        except (ChargenError, ChargenStepError) as exc:
            self._error = str(exc)
            raise
        self._error = None
        self._cursor += 1
        return key

    def back(self) -> str:
        """Zurueck einen Schritt (Cursor zurueck; CharGen-Kursor bleibt,
        da Chargen nicht rewind-faehig ist -- UI-UX: ``restart()``
        ist der saubere Weg)."""
        if self._cursor <= 0:
            raise CharGenWizardError("bereits am Anfang")
        self._cursor -= 1
        return self.current_step()

    def restart(self) -> None:
        """Wizard komplett zuruecksetzen (neuer CharGen, Cursor 0)."""
        type(self).__init__(self, self.definition, self.char_def,
                            getattr(self, "_seed", None))  # type: ignore[call-arg]

    # -- Lauf im Ganzen (Tests/CLI) ---------------------------------------------

    def run_all(self, spec: Dict[str, Any]) -> Any:
        """Kompletter Lauf in einem -> character_created-Event.

        spec = Chargen.run-Spec (race, folk, occupation, pool,
        stats_base, categories, items, purse, bgos, name).
        """
        self.finished_event = self.chargen.run(dict(spec))
        self._cursor = len(STEP_KEYS)
        return self.finished_event

    def result(self) -> Any:
        return self.finished_event
