#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression test: BUG-2250 — die drei ``calcMMP``-Methods in
``gui/modules/inventory_gui.py`` packten ``shop_logic.calc_mmp()`` (1 Float,
Marktmacht) in fünf Variablen:

    mmp, at, misslepen, armqupen, armmanmod = calc_mmp(self.character)

→ ``TypeError: cannot unpack non-sequence float`` beim ersten Aufruf von
``InventoryWin``/``shopWin``/``editinventory``.

Nach dem Fix holen die drei Methods die fünf Werte direkt aus
``rpgtoolbox.rpgtools.equipmentPenalities(character)``:

    MMP          <- ep.weightpenalty
    AT           <- ep.AT
    misslepen    <- ep.misatpen
    armquickpen  <- ep.armqupen
    armmanmod    <- ep.maxmanmod

Testet die drei geänderten Methods über einen unbound-Call mit einem
Fake-``IntVar``-Substitut (keine ``tk.Tk()``-Root).

Run:  xvfb-run -a python3 gui/test_inventory_mmp.py
Exits 0 after fix (GREEN); 1 while the bug is present (RED).
"""
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "gui"))

from rpgtoolbox import rpgtools as rpg          # noqa: E402
import modules.inventory_gui as inv             # noqa: E402  (aus gui/ ein)


# unbound Method-Handles (calcMMP ist nicht `__`-name-mangled, plain-Attr OK)
unbound_inventory = inv.InventoryWin.calcMMP      # L468
unbound_shop      = inv.shopWin.calcMMP           # L1631
unbound_edit      = inv.editinventory.calcMMP     # L4410


class FakeVar:
    """Substituiert ``tkinter.IntVar()`` ohne Root-Fenster. Wirft
    ``RuntimeError`` im alten Bug-Fall (TypeError beim Unpack) auf; im
    Fixed-Fall werden nur ``.set()``/``.get()`` aufgerufen."""

    def __init__(self, initial=0):
        self.value = initial
        self.set_calls = 0

    def set(self, v):
        self.value = v
        self.set_calls += 1
        return v

    def get(self):
        return self.value


class StubWin:
    """Minimaler ``self``-Stub für den unbound-Call. Liest nur
    ``character`` + ``wcont`` — das machen auch die drei realen Methods."""
    def __init__(self, character):
        self.character = character
        self.wcont = {"MMP": FakeVar(0)}


def _ref(character):
    ep = rpg.equipmentPenalities(character)
    return {
        "MMP":         ep.weightpenalty,
        "AT":          ep.AT,
        "misslepen":   ep.misatpen,
        "armquickpen": ep.armqupen,
        "armmanmod":   ep.maxmanmod,
    }


def _run(name, unbound, character):
    s = StubWin(character)
    unbound(s)
    ref     = _ref(character)
    got_w   = s.wcont["MMP"].get()
    sets    = s.wcont["MMP"].set_calls
    g_char  = {k: character.get(k) for k in
               ("MMP", "AT", "misslepen", "armquickpen", "armmanmod")}
    print(f"  {name:<28} wcont={got_w!r}(sets={sets})  "
          f"char={g_char}")

    problems = []
    # Wichtiger invariant core: MMP in wcont MUSS == ep.weightpenalty
    if got_w != ref["MMP"]:
        problems.append(f"wcont MMP={got_w!r} != ep.weightpenalty={ref['MMP']}")
    # MMP auf character soll in shopWin + editinventory (die schreiben dorthin)
    if name != "InventoryWin.calcMMP":
        if g_char["MMP"] != ref["MMP"]:
            problems.append(
                f'character["MMP"]={g_char["MMP"]} != ref={ref["MMP"]}')
        for k in ("AT", "misslepen", "armquickpen", "armmanmod"):
            if g_char[k] != ref[k]:
                problems.append(
                    f'character["{k}"]={g_char[k]} != ep={ref[k]}')
    if problems:
        raise AssertionError("; ".join(problems))


def main():
    start    = time.time()
    fpattern = os.path.join(ROOT, "data", "Marcus", "Finrion.json")
    with open(fpattern, "r", encoding="utf-8") as fh:
        char = json.load(fh)

    ref = _ref(char)
    print(f"Finrion reference (ep): {ref}")
    print(f"Finrion character BEVOR: MMP={char.get('MMP')} AT={char.get('AT')} "
          f"misslepen={char.get('misslepen')} "
          f"armquickpen={char.get('armquickpen')} "
          f"armmanmod={char.get('armmanmod')}")

    failures = 0
    plan = [
        ("InventoryWin.calcMMP", unbound_inventory, char),
        ("shopWin.calcMMP",      unbound_shop,      char),
        ("editinventory.calcMMP",unbound_edit,      char),
    ]
    for name, unbound, c in plan:
        print(f"\n=== {name}")
        try:
            _run(name, unbound, dict(c))  # deepcopy via dict(c) — shallow;
            print("  PASS")               # char bleibt original, nur MMP/AT/… mutieren
        except Exception as e:
            failures += 1
            print(f"  FAIL — {type(e).__name__}: {e}")

    elapsed = time.time() - start
    print(f"\n{'-' * 58}")
    if failures:
        print(f"  {failures}/3 FAIL  ({elapsed:.2f}s)")
        print("  RESULT: RED  (BUG-2250 noch vorhanden)")
        sys.exit(1)
    print(f"  3/3 PASS  ({elapsed:.2f}s)")
    print("  RESULT: GREEN  (BUG-2250 fixiert, MMP+Penalties von equipmentPenalities)")
    sys.exit(0)


if __name__ == "__main__":
    main()
