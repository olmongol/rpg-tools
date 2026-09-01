#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression test: defensive ``getAT()`` gegen fehlende Felder in armor-Einträgen.

``equipmentPenalities.getAT`` liest aus ``character["inventory"]["armor"][*]``.
Vor dem Fix crash-te die Funktion auf:

    * ``armor["name"]`` fehlt          -> ``KeyError``
    * ``armor["AT"]`` ist String       -> ``TypeError`` beim Vergleich
    * ``armor`` ist kein dict (z.B. String) -> ``TypeError`` beim Index-Zugriff
    * ``inventory`` / ``armor`` fehlen insgesamt

Nach dem Fix: ``None``/falscher Typ -> Stufe bleibt bei 1 (Initial), kein Crash.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rpgtools import equipmentPenalities


def ep_with_armor(armor_list):
    """Baut einen minimalen Character mit der gegebenen armor-Liste."""
    return equipmentPenalities({
        "background": {"weight": "200 kg"},
        "carried": 0,
        "inventory": {"armor": armor_list},
        "cat": {
            "Armor - Light":  {"Skill": {"Soft Leather":  {"total bonus": 0},
                                         "Rigid Leather": {"total bonus": 0}}},
            "Armor - Medium": {"Skill": {"Chain": {"total bonus": 0}}},
            "Armor - Heavy":  {"Skill": {"Plate": {"total bonus": 0}}},
        },
    })


# ── tests ───────────────────────────────────────────────────────────────

def test_regular_equipped_int_at():
    """Normfall: ein equipped-Rüstung mit int-AT 9 -> ``self.AT`` wird 9."""
    ep = ep_with_armor([
        {"name": "test", "location": "equipped", "AT": 9,
         "total bonus": 0, "weight": 5},
    ])
    print(f"  regular equipped int-AT 9 -> self.AT = {ep.AT!r}")
    # 9 + int(0.0 greaves) = 9
    assert ep.AT == 9, f"erwartet 9, ist {ep.AT!r}"


def test_string_at_ignored():
    """String-AT wird ignoriert (kein ValueError, kein TypeError)."""
    ep = ep_with_armor([
        {"name": "test", "location": "equipped", "AT": "9",
         "total bonus": 0, "weight": 5},
    ])
    print(f"  string-AT '9'         -> self.AT = {ep.AT!r} (bleibt 1)")
    # AT ist kein int -> wird ignoriert, also 1 + 0.0 greaves
    assert ep.AT == 1, f"erwartet 1, ist {ep.AT!r}"


def test_missing_name_no_crash():
    """Fehlendes 'name' -> kein KeyError, Stufe bleibt int-AT."""
    ep = ep_with_armor([
        {"location": "equipped", "AT": 9, "total bonus": 0, "weight": 5},
    ])
    print(f"  missing-name armor     -> self.AT = {ep.AT!r}")
    assert ep.AT == 9, f"erwartet 9, ist {ep.AT!r}"


def test_non_equipped_ignored():
    """Nicht-equipped Rüstung wird ignoriert."""
    ep = ep_with_armor([
        {"name": "test", "location": "head", "AT": 9,
         "total bonus": 0, "weight": 5},
    ])
    print(f"  non-equipped armor     -> self.AT = {ep.AT!r} (bleibt 1)")
    assert ep.AT == 1, f"erwartet 1, ist {ep.AT!r}"


def test_empty_armor_list():
    """Leere armor-Liste -> kein Crash, AT = Initial 1."""
    ep = ep_with_armor([])
    print(f"  empty armor list       -> self.AT = {ep.AT!r}")
    assert ep.AT == 1, f"erwartet 1, ist {ep.AT!r}"


def test_greaves_name_recognized():
    """'Greaves' im Namen -> +0.5 (geclippt auf int() = 0, also +0).
    Zwei Greaves = 1.0 -> +1 (int(greaves)=1).
    """
    ep = ep_with_armor([
        {"name": "Greaves", "location": "equipped", "AT": 9,
         "total bonus": 0, "weight": 5},
        {"name": "Shin Guard", "location": "equipped", "AT": 9,
         "total bonus": 0, "weight": 5},
        {"name": "Second Greaves", "location": "equipped", "AT": 9,
         "total bonus": 0, "weight": 5},
    ])
    print(f"  2x Greaves            -> self.AT = {ep.AT!r} (9 + 1 = 10)")
    assert ep.AT == 10, f"erwartet 10, ist {ep.AT!r}"


# ── runner ──────────────────────────────────────────────────────────────

def main():
    start  = time.time()
    tests  = [
        ('Regular equipped int-AT',       test_regular_equipped_int_at),
        ('String-AT ignored',             test_string_at_ignored),
        ('Missing "name" no crash',       test_missing_name_no_crash),
        ('Non-equipped ignored',          test_non_equipped_ignored),
        ('Empty armor list',              test_empty_armor_list),
        ('Greaves name recognized',       test_greaves_name_recognized),
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
