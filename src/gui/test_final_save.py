"""Regression test: BUG-2248 — 'sometimes it does not store the character
sheet successfully' (skillcatWin.__finalize / __save).

Root causes:
  A) __finalize indexes self.__changed['cat'][cat]['rank'] /
     'total bonus' and [...]['Skill'] without guards — a changed entry
     created by an older code path (or a renamed skill/catk) raises
     KeyError AFTER the DP reservation was committed → the sheet is
     never written, DP is lost.
  B) __save writes into spath/<player>/<name>.json but never ensures the
     player subdirectory exists; writeJSON() swallows every IO error
     (globaltools.writeJSON: except Exception: logger.error) → silent
     data loss for a new player (no data/<player>/ dir yet).

Expected after fix:
  A) finalize completes; rank/total copied only when present; missing
     Skill entries skipped without aborting the save.
  B) __save creates the target directory, writes the file, and FAILS
     LOUDLY (raises) when the write itself did not land — silent no-op
     saves are no longer possible.

Run:  xvfb-run -a python3 gui/test_final_save.py   (or env-unset DISPLAY)
Exits 0 when fixed (GREEN); 1 when the bug is present (RED).
"""
import os
import json
import shutil
import sys
import tempfile
from types import SimpleNamespace

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "gui"))

from rpgtoolbox import rolemaster as rm
import epwins

_finalize = epwins.skillcatWin._skillcatWin__finalize
_save = epwins.skillcatWin._skillcatWin__save

PASS = 0
FAIL = 0


def ok(name):
    global PASS
    PASS += 1
    print(f"  PASS  {name}")


def bad(name, err):
    global FAIL
    FAIL += 1
    print(f"  FAIL  {name}: {err!r}")


def _patch_deps(tmpdir):
    """Neutralize GUI/DB dependencies of __finalize for a headless test."""
    calls = {"writes": []}
    def _fake_wj(fname, content=None):
        calls["writes"].append(fname)
        with open(fname, "w", encoding="utf-8") as fp:
            json.dump(content, fp)
    epwins.writeJSON = _fake_wj
    epwins.calcTotals = lambda char: char
    epwins.handlemagic.updateSL = lambda character=None, datadir=None: None
    rm.choseProfession = lambda lang='en': {
        "Dwarf": {"Profession Bonusses": {}}}
    rm.refreshStatBonus = lambda char=None: char
    class _StubWin:
        def __init__(self, *a, **k):
            pass
        def destroy(self):
            pass
    epwins.MainWindow = _StubWin
    epwins.charInfo = _StubWin
    return calls


def _stub_self(char, changed, usedDP=0, spath=None):
    s = SimpleNamespace()
    s.lang = "en"
    s.spath = spath or os.getcwd() + "/data"
    s._character = char
    s._skillcatWin__changed = changed
    s._skillcatWin__usedDP = usedDP
    # __finalize calls self.__save('.json') — bind the REAL method
    # (name-mangled) onto the stub so the save path is exercised end-to-end
    s._skillcatWin__save = lambda ending='.snap': _save(s, ending)
    s.window = SimpleNamespace(destroy=lambda: None)
    return s


def _char(cat_entries):
    return {
        "name": "Finrion",
        "player": "Marcus",
        "prof": "Dwarf",
        "race": "Dwarves",
        "DP": 12,
        "lvlup": 1,
        "exp": 500,
        "old_exp": 400,
        "cat": cat_entries,
    }


def _cat():
    return {
        "rank": 1,
        "total bonus": 2,
        "Skill": {
            "Axe": {"rank": 2, "total bonus": 3, "Progression": ["+1"]},
            "Progression": [],
            "Stats": 0,
        },
    }


# ---------------------------------------------------------------- Case A
def case_a_changed_missing_rank_keys():
    """__changed entry without 'rank'/'total bonus' (legacy shape) and a
    renamed skill that no longer exists in the character must not abort
    __finalize before the sheet is saved (BUG-2248 root cause A)."""
    old_wj = epwins.writeJSON
    try:
        tmpdir = tempfile.mkdtemp(prefix="bug2248a")
        calls = _patch_deps(tmpdir)
        base_cat = _cat()
        base_cat["Skill"]["Axe"] = dict(base_cat["Skill"]["Axe"])  # deep copy
        char = _char({**{("Axes"): base_cat}})
        # legacy changed entry: NO 'rank', NO 'total bonus', no 'Skill';
        # plus a skill that was renamed away from the character
        changed = {
            "name": "Finrion",
            "player": "Marcus",
            "cat": {
                "Axes": {"Progression": ["+1"]},
                "Throwing": {"rank": 3, "total bonus": 4,
                            "Skill": {"OldName": {"rank": 1, "total bonus": 1}}},
            },
        }
        stub = _stub_self(char, changed, usedDP=4, spath=tmpdir)
        _finalize(stub)
        # the sheet + changes file must have been written
        joined = " ".join(calls["writes"])
        if "Finrion.json" not in joined:
            raise AssertionError(f"sheet not in save list: {calls['writes']}")
        if "Finrion_changes.json" not in joined:
            raise AssertionError(f"changes not in save list: {calls['writes']}")
        ok("A: finalize survives legacy __changed shape, sheet saved")
    except Exception as e:  # noqa: BLE001
        bad("A", e)
    finally:
        epwins.writeJSON = old_wj
        shutil.rmtree(tmpdir, ignore_errors=True)


# ------------------------------------------------------------- Case B
def case_b_save_missing_player_dir():
    """__save must create the missing <player>/ subdirectory (BUG-2248
    root cause B) — currently writeJSON swallows the FileNotFoundError
    and the sheet silently vanishes."""
    tmpdir = tempfile.mkdtemp(prefix="bug2248b")
    try:
        # real writeJSON (from globaltools) — the actual IO path
        from rpgtoolbox.globaltools import writeJSON
        char = _char({("Axes"): _cat()})
        stub = _stub_self(char, {"cat": {}}, spath=tmpdir)  # no data dir!
        _save(stub, ".json")
        target = os.path.join(tmpdir, "Marcus", "Finrion.json")
        if not os.path.isfile(target):
            raise AssertionError(f"sheet missing after save: {target} "
                                 "(silent data loss)")
        import json as _j
        data = _j.load(open(target, encoding="utf-8"))
        if data.get("name") != "Finrion":
            raise AssertionError(f"wrong sheet content: {data.get('name')}")
        ok("B: __save creates missing player dir, sheet persisted")
    except Exception as e:  # noqa: BLE001
        bad("B", e)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ------------------------------------------------------------- Case C
def case_c_save_failure_is_loud():
    """A write that does not land must raise (loud failure), not be
    swallowed (BUG-2248: silent no-op save)."""
    real_wj = epwins.writeJSON
    try:
        tmpdir = tempfile.mkdtemp(prefix="bug2248c")
        epwins.writeJSON = lambda fname, content=None: None  # simulates IO loss
        char = _char({("Axes"): _cat()})
        stub = _stub_self(char, {"cat": {}}, spath=tmpdir)
        _save(stub, ".json")
        bad("C", AssertionError("silent save with no file on disk"))
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        ok("C: failed save raised instead of silent no-op")
    finally:
        epwins.writeJSON = real_wj
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    case_a_changed_missing_rank_keys()
    case_b_save_missing_player_dir()
    case_c_save_failure_is_loud()
    print(f"\nRESULT: {PASS} passed, {FAIL} failed")
    sys.exit(1 if FAIL else 0)
