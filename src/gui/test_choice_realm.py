"""Regression test: BUG-021 — __setPPD crashes with KeyError 'Dwarves'
when realm='choice' (realm not yet chosen, e.g. new Dwarf).

Root cause: realms[0]='choice' → ppds[0]='' (empty str) → the original
lookup progressionType['' + 'Dwarves'] = progressionType['Dwarves'] raises
KeyError because only prefixed combos ('InDwarves', 'PrDwarves', …) exist.

Expected after fix: no exception; progression is written as the 'null'
entry (safe no-op while the user still picks a realm).

Run:  xvfb-run -a python3 gui/test_choice_realm.py
Exits 0 when fixed (GREEN); 1 when the bug is present (RED).
"""
import os
import sys
from types import SimpleNamespace

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "gui"))

from rpgtoolbox import rolemaster as rm
import epwins

_setPPD = epwins.priorizeWeaponsWin._priorizeWeaponsWin__setPPD


def _mk_char(realm: str) -> dict:
    """Build a minimal character dict that __setPPD needs."""
    ppd_cat_name = rm.speccat["en"][1]          # "Power Point Development"
    return {
        "name": "TestDwarf",
        "prof": "Common Men",
        "race": "Dwarves",
        "realm": realm,
        "cat": {
            ppd_cat_name: {
                "Progression": None,
                "Stats": None,
                "Skill": {
                    ppd_cat_name: {"Progression": None},
                },
            },
        },
    }


def run_case(realm: str):
    ch = _mk_char(realm)
    pseudo_self = SimpleNamespace(character=ch)
    _setPPD(pseudo_self)
    got = ch["cat"][rm.speccat["en"][1]]["Skill"][rm.speccat["en"][1]]["Progression"]
    print(f"  realm={realm!r:>20}  -> progression={got!r}")
    return got


# ---- case 1: realm='choice' — the BUG-021 trigger ----
print("Case 1 (BUG-021 trigger) realm='choice':")
try:
    v = run_case("choice")
except KeyError as e:
    print(f"  RED: KeyError {e} — BUG-021 still present")
    sys.exit(1)
expected_null = rm.progressionType["null"]
if v != expected_null:
    print(f"  FAIL: expected progressionType['null']={expected_null!r}, got {v!r}")
    sys.exit(1)
print("  GREEN: no KeyError, progressionType['null'] written")

# ---- case 2: normal realm (Channeling -> 'PPD Chan '), regression check ----
print("Case 2 (regression check) realm='Channeling':")
in_exp = rm.progressionType["PPD Chan Dwarves"]
ch = _mk_char("Channeling")
_setPPD(SimpleNamespace(character=ch))
got2 = ch["cat"][rm.speccat["en"][1]]["Skill"][rm.speccat["en"][1]]["Progression"]
print(f"  realm='Channeling' -> progression={got2!r}  (expected {in_exp!r})")
assert got2 == in_exp, "Channeling regression broken"

# ---- case 3: dual realm (Channeling+Mentalism -> ['PPD Chan ','PPD Ment ']) ----
print("Case 3 (regression check) realm=['Channeling','Mentalism']:")
dual_realm = ['Channeling', 'Mentalism']
ppd_list = ['PPD Chan ', 'PPD Ment ']
expected3 = max(
    rm.progressionType[p + "Dwarves"] for p in ppd_list
)
ch = _mk_char(dual_realm)
_setPPD(SimpleNamespace(character=ch))
got3 = ch["cat"][rm.speccat["en"][1]]["Skill"][rm.speccat["en"][1]]["Progression"]
print(f"  realm={dual_realm!r} (ppd={ppd_list}) -> progression={got3!r}  (expected {expected3!r})")
assert got3 == expected3, "dual-realm regression broken"

print("\nALL TESTS PASSED (BUG-021 fixed)")
sys.exit(0)
