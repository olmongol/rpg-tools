#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression test: Armor-Penalties — fehlende Tabellenwerte AT 9/13/17 explizit 0.

Hintergrund
───────────
``equipmentPenalities.calcArmorPen()`` (rpgtools.py) trug je nach AT-Stufe
nur einen Teil der vier Penalty-Felder.  Fehlt ein Feld, blieb der
Initialwert ``0`` aus ``__init__`` (implizit) — korrekt im Ergebnis,
aber unsichtbar im Code.

User-Entscheidung (2026-09-01):  alle fehlenden Werte *explizit* auf
``0`` setzen, damit jede Zeile der Penalty-Tabelle vier Felder hat.

Änderung (AT 9, AT 13, AT 17 in ``calcArmorPen``):
    AT 9 :  + ``self.misatpen = 0``   + ``self.armqupen = 0``
    AT 13:  + ``self.misatpen = 0``
    AT 17:  + ``self.misatpen = 0``
Die bestehenden Blöcke (AT 6, 8, 16, 20–32) bleiben unverändert.

Test-Harness: kein tk.Tk(), kein Netzwerk — nur ``equipmentPenalities``
mit Stubb-Character-JSONs (eine Rüstung pro AT-Stufe, Bonus-0).
Stubb-Feldnamen:
    ``character["background"]["weight"]``  →  **String** (Regex, z.B. ``"200 kg"``)
    ``character["inventory"]["armor"][*]["location"]``  →  ``"equipped"``
    ``character["inventory"]["armor"][*]["AT"]``  →  ``int``
    ``character["carried"]``  →  ``int`` (0 = leer, kein Gewichtsabzug)

Laufzeit: < 1 s.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rpgtools import equipmentPenalities


def make_character(AT_):
    """Minimal-Character-JSON: eine Rüstung mit der gewünschten AT,
    Bonus-0, damit ``maxmanmod`` = Basissatz aus ``calcArmorPen`` wird.

    Felder exakt so, wie der reale Code sie erwartet:
      - weight:  String (``re.compile("^(...)(kg|lbs)")``) in ``calcWeightPen``
      - AT:      int   (``type(armor["AT"]) == type(2)``) in ``getAT``
      - location:"equipped" (``armor["location"] == "equipped"``) in ``getAT``
      - carried: int  0 (no weight-penalty loop)
    """
    return {
        "background": {"weight": "200 kg"},
        "carried": 0,
        "inventory": {
            "armor": [
                {
                    "name":     "test",
                    "location": "equipped",
                    "AT":       AT_,
                    "total bonus": 0,
                    "weight":   5,
                }
            ],
        },
        "cat": {
            "Armor - Light":  {
                "Skill": {
                    "Soft Leather":  {"total bonus": 0},
                    "Rigid Leather": {"total bonus": 0},
                }
            },
            "Armor - Medium": {
                "Skill": {"Chain": {"total bonus": 0}}
            },
            "Armor - Heavy":  {
                "Skill": {"Plate": {"total bonus": 0}}
            },
        },
    }


def calc(AT_):
    ep = equipmentPenalities(make_character(AT_))
    return (ep.misatpen, ep.armqupen, ep.minmanmod, ep.maxmanmod)


# ── tests ───────────────────────────────────────────────────────────────

def test_at9_explicit_zero():
    """AT 9  (vorher: misatpen/armqupen fehlten)
    Erwartet: misatpen=0, armqupen=0, minmanmod=-5, maxmanmod=-50 (explizit)."""
    misatpen, armqupen, minmanmod, maxmanmod = calc(9)
    print(f"  AT 9 : misatpen={misatpen}  armqupen={armqupen}  "
          f"minmanmod={minmanmod}  maxmanmod={maxmanmod}")
    assert armqupen  == 0,   f"AT 9 armqupen erwartet 0, ist {armqupen!r}"
    assert misatpen  == 0,   f"AT 9 misatpen erwartet 0, ist {misatpen!r}"
    assert minmanmod == -5,  f"AT 9 minmanmod erwartet -5, ist {minmanmod!r}"
    assert maxmanmod == -50, f"AT 9 maxmanmod erwartet -50, ist {maxmanmod!r}"


def test_at13_explicit_zero():
    """AT 13 (vorher: misatpen fehlte)
    Erwartet: misatpen=0 (explizit), armqupen=-5, minmanmod=-10, maxmanmod=-70."""
    misatpen, armqupen, minmanmod, maxmanmod = calc(13)
    print(f"  AT 13: misatpen={misatpen}  armqupen={armqupen}  "
          f"minmanmod={minmanmod}  maxmanmod={maxmanmod}")
    assert misatpen  == 0,   f"AT 13 misatpen erwartet 0, ist {misatpen!r}"
    assert armqupen  == -5,  f"AT 13 armqupen erwartet -5, ist {armqupen!r}"
    assert minmanmod == -10, f"AT 13 minmanmod erwartet -10, ist {minmanmod!r}"
    assert maxmanmod == -70, f"AT 13 maxmanmod erwartet -70, ist {maxmanmod!r}"


def test_at17_explicit_zero():
    """AT 17 (vorher: misatpen fehlte)
    Erwartet: misatpen=0 (explizit), armqupen=-10, minmanmod=-15, maxmanmod=-90."""
    misatpen, armqupen, minmanmod, maxmanmod = calc(17)
    print(f"  AT 17: misatpen={misatpen}  armqupen={armqupen}  "
          f"minmanmod={minmanmod}  maxmanmod={maxmanmod}")
    assert misatpen  == 0,   f"AT 17 misatpen erwartet 0, ist {misatpen!r}"
    assert armqupen  == -10, f"AT 17 armqupen erwartet -10, ist {armqupen!r}"
    assert minmanmod == -15, f"AT 17 minmanmod erwartet -15, ist {minmanmod!r}"
    assert maxmanmod == -90, f"AT 17 maxmanmod erwartet -90, ist {maxmanmod!r}"


def test_existing_rows_unchanged():
    """Bestehende + AT 6 (nun auch mit expliziten 0).
    AT 6  : misatpen=-5,   armqupen=0,   minmanmod=0,  maxmanmod=-20
    AT 16 : misatpen=-20,  armqupen=-20, minmanmod=-25,maxmanmod=-130
    Hinweis: maxmanmod=-130 ist *geringer* als minmanmod=-25, daher greift
    der Clamp ``if maxmanmod > minmanmod`` (Zeile 428) hier NICHT.
    """
    misatpen, armqupen, minmanmod, maxmanmod = calc(6)
    print(f"  AT 6 : misatpen={misatpen}  armqupen={armqupen}  "
          f"minmanmod={minmanmod}  maxmanmod={maxmanmod}")
    assert misatpen  == -5,  f"AT 6 misatpen erwartet -5, ist {misatpen!r}"
    assert armqupen  == 0,   f"AT 6 armqupen erwartet 0 (explizit), ist {armqupen!r}"
    assert minmanmod == 0,   f"AT 6 minmanmod erwartet 0 (explizit), ist {minmanmod!r}"
    assert maxmanmod == -20, f"AT 6 maxmanmod erwartet -20, ist {maxmanmod!r}"

    misatpen, armqupen, minmanmod, maxmanmod = calc(16)
    print(f"  AT 16: misatpen={misatpen}  armqupen={armqupen}  "
          f"minmanmod={minmanmod}  maxmanmod={maxmanmod}")
    assert misatpen  == -20, f"AT 16 misatpen erwartet -20, ist {misatpen!r}"
    assert armqupen  == -20, f"AT 16 armqupen erwartet -20, ist {armqupen!r}"
    assert minmanmod == -25, f"AT 16 minmanmod erwartet -25, ist {minmanmod!r}"
    assert maxmanmod == -130, f"AT 16 maxmanmod erwartet -130, ist {maxmanmod!r}"


# ── runner ──────────────────────────────────────────────────────────────

def main():
    start  = time.time()
    tests  = [
        ('AT 9  — explizite 0 (neu)',           test_at9_explicit_zero),
        ('AT 13 — explizite 0 (neu)',           test_at13_explicit_zero),
        ('AT 17 — explizite 0 (neu)',           test_at17_explicit_zero),
        ('Bestehende Zeilen AT 6/16 unverändert', test_existing_rows_unchanged),
    ]
    failures = 0
    for name, fn in tests:
        print(f"\n=== {name}")
        try:
            fn()
            print('  PASS')
        except Exception as e:
            failures += 1
            print(f'  FAIL — {type(e).__name__}: {e}')
    elapsed = time.time() - start
    passed  = len(tests) - failures
    print(f"\n{'━'*58}")
    print(f"  {passed}/{len(tests)} passed, {failures} failed  ({elapsed:.2f}s)")
    if failures:
        print('  RESULT: RED');  sys.exit(1)
    print('  RESULT: GREEN');    sys.exit(0)


if __name__ == '__main__':
    main()
