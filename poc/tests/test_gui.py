"""GUI-Tests (offscreen, 05: K8/K9).

Decken ab:
  * charform: stats_order, stat_display, stat_values, build_stats_form
  * inventory: inventory_rows, InventoryModel (QAbstractTableModel)
  * window: stats_display_rows, stat_summary, inventory_display_rows,
            pending_display_rows, pending_labels, RpgMainWindow
  * wizard: full offscreen flow -- 8 Schritte durchklicken ->
            character_created Event -> append -> 2. Client sieht es
"""
from __future__ import annotations

import os
import sys
from typing import Any, Dict

import pytest

# Ensure offscreen BEFORE any Qt import.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

# Ensure poc/ is on the path (conftest also does this).
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from PyQt6.QtWidgets import QApplication  # noqa: E402
import rpgpoc

from rpgpoc.client import Client  # noqa: E402
from rpgpoc.gui.charform import (  # noqa: E402
    build_stats_form,
    stat_display,
    stat_values,
    stats_order,
)
from rpgpoc.gui.inventory import InventoryModel, inventory_rows  # noqa: E402
from rpgpoc.gui.window import (  # noqa: E402
    RpgMainWindow,
    inventory_display_rows,
    pending_display_rows,
    pending_labels,
    stat_summary,
    stats_display_rows,
)
from rpgpoc.gui.wizard import CharGenWizardDialog  # noqa: E402
from rpgpoc.gui.wizardlogic import CharGenWizard  # noqa: E402
from rpgpoc.loader import load_template  # noqa: E402
from rpgpoc.store import LocalJsonStore  # noqa: E402


@pytest.fixture(scope="session")
def qapp() -> QApplication:
    """Single QApplication per session (offscreen)."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def spec() -> Dict[str, Any]:
    """Loaded Rm role master template spec."""
    return load_template(os.path.join(ROOT, "templates", "rolemaster"))


@pytest.fixture
def state_10() -> Dict[str, Any]:
    """Fake chargen state (all 10 stats at temp=50, base=50)."""
    return {
        abbr: {"base": 50, "race": 0, "temp": 50, "bonus": 0, "cost": 0}
        for abbr in ("St", "Ag", "Re", "Co", "Pr", "Me", "In", "Qu", "Em", "SD")
    }


@pytest.fixture
def rm_abbrevs(spec) -> list:
    return [s["abbr"] for s in (spec.get("char_def") or {}).get("stats") or []] \
        or [s["abbr"] for s in (spec.get("stats") or [])]


# ---------------------------------------------------------------------------
# charform
# ---------------------------------------------------------------------------

def test_stats_order_reads_definition(spec, rm_abbrevs):
    order = stats_order(spec)
    assert order == rm_abbrevs
    assert len(order) == 10
    assert order[0] == rm_abbrevs[0]


def test_stat_display_none_on_missing():
    assert stat_display({}, "St") is None


def test_stat_display_formats_state(state_10):
    state_10["St"]["temp"] = 100
    state_10["St"]["bonus"] = 10
    line = stat_display(state_10, "St")
    assert line is not None
    assert "100" in line
    assert "10" in line


def test_stat_values_returns_ints(state_10):
    v = stat_values(state_10, "St")
    assert v["base"] == 50
    assert v["race"] == 0
    assert v["temp"] == 50
    assert v["bonus"] == 0
    assert v["cost"] == 0


def test_stat_values_empty_for_missing():
    assert stat_values({}, "St") == {}


def test_build_stats_form_builds_rows(qapp, spec, rm_abbrevs, state_10):
    form = build_stats_form(None, spec, state=None)
    assert form.rowCount() == len(rm_abbrevs)
    # Filled from state:
    form2 = build_stats_form(None, spec, state=state_10)
    assert form2.rowCount() == len(rm_abbrevs)


# ---------------------------------------------------------------------------
# inventory
# ---------------------------------------------------------------------------

def test_inventory_rows_from_state():
    state = {
        "inventory": [
            {"seq": 1, "id": "x1", "name": "Axt", "actor": "gm"},
            {"seq": 2, "id": "x2", "name": "Schild", "actor": "player"},
        ]
    }
    rows = inventory_rows(state)
    assert len(rows) == 2
    assert rows[0]["name"] == "Axt"
    assert rows[1]["actor"] == "player"


def test_inventory_rows_empty_on_missing():
    assert inventory_rows({}) == []


def test_inventory_model_rowcount(qapp):
    m = InventoryModel()
    assert m.rowCount() == 0
    m.reset_rows([
        {"seq": 1, "id": "1", "name": "Axt", "actor": "gm"},
        {"seq": 2, "id": "2", "name": "Bogen", "actor": "gm"},
    ])
    assert m.rowCount() == 2
    assert m.columnCount() == 4
    assert m.data(m.index(0, 2)) == "Axt"
    assert m.data(m.index(1, 0)) == 2


def test_inventory_model_refresh_from_state(qapp):
    m = InventoryModel()
    state = {"inventory": [
        {"seq": 1, "id": "1", "name": "Fackel", "actor": "gm"}]}
    m.refresh(state)
    assert m.rowCount() == 1
    assert m.data(m.index(0, 2)) == "Fackel"


# ---------------------------------------------------------------------------
# window
# ---------------------------------------------------------------------------

def test_stats_display_rows_from_character_created_payload():
    state = {
        "character_created": {
            "payload": {
                "stats": {
                    "St": {"base": 50, "race": 0, "temp": 100,
                           "bonus": 10, "cost": 100},
                    "Ag": {"base": 40, "race": -2, "temp": 38,
                           "bonus": -2, "cost": 0},
                }
            }
        }
    }
    rows = stats_display_rows(state)
    assert len(rows) == 2  # nur Stats, die im Payload existieren
    st_row = next(r for r in rows if r["abbr"] == "St")
    assert st_row["temp"] == 100
    assert st_row["bonus"] == 10


def test_stats_display_rows_empty_no_payload():
    assert stats_display_rows({}) == []


def test_stat_summary_returns_string():
    s = stat_summary({"abbr": "St", "base": 50, "race": 0,
                      "temp": 100, "bonus": 10, "cost": 10})
    assert "100" in s
    assert "10" in s


def test_inventory_display_rows():
    state = {"inventory": [
        {"seq": 1, "id": "a", "name": "Schild", "actor": "gm"},
    ]}
    rows = inventory_display_rows(state)
    assert len(rows) == 1
    assert rows[0][2] == "Schild"


def test_pending_display_rows_and_labels():
    state = {"pending_stats": {
        "St": {"value": 100, "actor": "gm", "seq": 5, "status": "pending"},
        "Ag": {"value": 40, "actor": "gm", "seq": 4, "status": "rejected"},
        "In": {"value": 60, "actor": "gm", "seq": 6, "status": "approved"},
    }}
    # approved rows must be filtered out
    rows = pending_display_rows(state)
    assert len(rows) == 2
    assert {r["stat"] for r in rows} == {"St", "Ag"}
    labels = pending_labels(rows)
    assert any("offen" in lbl for lbl in labels)
    assert any("abgelehnt" in lbl for lbl in labels)


def test_pending_labels_handles_empty():
    assert pending_labels([]) == []


def test_rpg_main_window_refreshes_on_append(qapp, spec, tmp_path):
    store = LocalJsonStore(tmp_path)
    c = Client(store, "finrion")
    # Simulate a created event.
    from rpgpoc import events as ev
    c.append(ev.Event(seq=0, char="finrion", type=ev.CHARACTER_CREATED,
                      actor="gm", payload={"stats": {
                          "St": {"base": 50, "race": 0, "temp": 100,
                                 "bonus": 10, "cost": 100},
                      }
                      }))
    c.item_add("Schild")

    win = RpgMainWindow(spec, c)
    assert win.stats_table.rowCount() <= 10
    assert win.inv_table.rowCount() == 1
    # Refresh from a second client on the same store.
    c2 = Client(store, "finrion")
    win.refresh(c2)
    assert win.inv_table.rowCount() == 1
    assert win.stats_table.rowCount() >= 1


# ---------------------------------------------------------------------------
# wizard (offscreen end-to-end): 8 Schritte -> Event -> 2. Client sieht es
# ---------------------------------------------------------------------------

def test_wizard_dialog_full_flow(qapp, spec, tmp_path):
    """Wizard: 8 Schritte durchklicken -> character_created -> append.

    Second Client on the same LocalJsonStore sees the appended event
    (Akz. 3: Zweit-Client sieht die Änderung).
    """
    store = LocalJsonStore(tmp_path)
    c1 = Client(store, "Finrion")

    dlg = CharGenWizardDialog(spec)
    pages = dlg.pages

    def fill(key, val):
        page = pages[key]
        page.set_value(val)
        dlg.on_next()
        assert dlg.wiz.error() is None, \
            f"step {key} error: {dlg.wiz.error()}"
        assert dlg.wiz.current_step() != key or key not in \
            ("race", "folk", "occupation", "stats", "categories",
             "equipment", "bgos", "finalize"), \
            f"did not advance past {key}"

    # Step 1: Rasse
    fill("race", "Wood Elves")
    # Step 2: Volk
    fill("folk", "Silvanii")
    # Step 3: Beruf
    fill("occupation", "Magician")
    # Step 4: Stats
    fill("stats", 300)
    # Step 5: Kategorien
    fill("categories", ["Combat Maneuvers"])
    # Step 6: Inventar + Beutel
    fill("equipment", "Schild\nLangschwert\nTasche: 12")
    # Step 7: BGOs
    fill("bgos", "vorteil: Nahsicht|1\nnachteil: Geiz")
    # Step 8: Name
    fill("finalize", "Finrion")

    assert dlg.wiz.current_step() == "done"
    dlg.finish_wizard()
    ev = dlg.result
    assert ev is not None
    assert ev.type == "character_created"
    assert ev.payload["name"] == "Finrion"
    assert "stats" in ev.payload

    # Append to store and check second client sees it.
    c1.append(ev)
    c2 = Client(store, "Finrion")
    state = c2.sheet()
    assert state["character_created"] is not None
    assert state["character_created"]["payload"]["name"] == "Finrion"


def test_wizard_logic_run_all(qapp, spec):
    """CharGenWizard (pure logic): run_all in einem Rutsch."""
    wiz = CharGenWizard(spec, spec.get("char_def") or {}, seed=42)
    spec_map = {
        "race": "Wood Elves",
        "folk": "Silvanii",
        "occupation": "Magician",
        "pool": 300,
        "stats_base": None,
        "categories": ["Combat Maneuvers"],
        "items": [{"name": "Schild"}, {"name": "Langschwert"}],
        "purse": 12,
        "bgos": [{"kind": "vorteil", "name": "Nahsicht"},
                 {"kind": "nachteil", "name": "Geiz"}],
        "name": "Finrion",
    }
    ev = wiz.run_all(spec_map)
    assert ev is not None
    assert ev.type == "character_created"
    assert ev.payload["name"] == "Finrion"
