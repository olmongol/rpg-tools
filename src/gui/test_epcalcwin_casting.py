#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression test: epcalcwin GUI „Zauber wirken"-Fenster (__winCasting).

Befunde (vor Fix):
- BUG-2254: _learned_blocks filterte nach ``total bonus > 0`` (Int-Check).
  Listen mit ``rank > 0`` und Bonus 0 (frisch erlernt, noch kein Bonus)
  fehlten; Listen mit Bonus > 0 aber rank 0 (Item-/Ausruestungsquelle)
  wurden fälschlich als erlernte Spruchliste aufgelistet.
- BUG-2255: _set_options() füllte das Menü mit
  ``command=lambda x: var.set(x)`` neu — der beim OptionMenu-Setup gesetzte
  command-Callback (Rebuild der tieferen Ebene) wurde bei jeder Refill
  überschrieben; Auswahl danach rief _rebuild_spells/_show_spell_info nie mehr auf.
- BUG-2256: Die Spruchlisten-/Zauber-Dropdowns (colspan=3) lagerten auf den
  Zeilen der Eingabefelder (row 1-3) → Grid-Kollisionen; Labels ohne
  explizite fg auf dem dunklen Hintergrund #333333 (schwarzer Text auf
  dunklem Grund).
- BUG-2257: char_var wurde ohne Initialwert erzeugt → Fenster öffnete mit
  leerer Auswahlanzeige und ungefüllten Listen.

Testet das FENSTER gegen einen deterministischen Inline-Fixture (kein
__init__, keine Netzwerk-/Datei-Abhängigkeit; Daten inline).

Lauf:  xvfb-run -a python3 gui/test_epcalcwin_casting.py
Beendet sich mit 0 nach Fix (GREEN); 1 bei vorhandenem Bug (RED).
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "gui"))

import tkinter as tk  # noqa: E402

import gui.modules.epcalcwin_gui as mod  # noqa: E402

# --------------------------------------------------------------------------- fixture
# 'Testling':
#   - Inner Walls    rank 3, bonus 5 → erlernt; Frost Lvl1 (ok), Fire Lvl5 (> rank, raus)
#   - Moving Ways    rank 2, bonus 0 → erlernt (BUG-2254-Fall A: Bonus 0)
#   - Path Mastery   rank 0, bonus 9 → NICHT erlernt (BUG-2254-Fall B: Item-Quelle)
#   - Leerling:      keine Spells → 0 Listen
CHARS = [
    {
        "player": "Testling",
        "name": "t1",
        "realm": "Essence",
        "cat": {
            "Spells - Own Realm Own Base Lists": {
                "total bonus": 0,
                "Skill": {
                    "Inner Walls": {
                        "rank": 3,
                        "total bonus": 5,
                        "Spells": [
                            {"Spell": "Frost", "Lvl": 1, "Duration": "1 Rnd",
                             "Range": "Self", "Area of Effect": "self",
                             "Type": "Warding", "Description": "kalt"},
                            {"Spell": "Fire", "Lvl": 5, "Duration": "1 Rnd",
                             "Range": "Near", "Area of Effect": "1 Ziel",
                             "Type": "Attack", "Description": "heiss"},
                        ],
                    },
                    "Moving Ways": {
                        "rank": 2,
                        "total bonus": 0,
                        "Spells": [
                            {"Spell": "Run", "Lvl": 1, "Duration": "1 Min",
                             "Range": "Self", "Area of Effect": "self",
                             "Type": "Move", "Description": "schnell"},
                        ],
                    },
                    "Path Mastery": {
                        "rank": 0,
                        "total bonus": 9,
                        "Spells": [
                            {"Spell": "Fly", "Lvl": 2, "Duration": "1 H",
                             "Range": "Self", "Area of Effect": "self",
                             "Type": "Move", "Description": "fliegen"},
                        ],
                    },
                },
            }
        },
    },
    {
        "player": "Leerling",
        "name": "t2",
        "realm": "Essence",
        "cat": {"Spells - Own Realm Own Base Lists": {"total bonus": 0, "Skill": {}}},
    },
]

# ------------------------------------------------------------------- helpers
FAIL = []


def check(label, cond, detail=""):
    tag = "ok  " if cond else "FAIL"
    print("  [%s] %s %s" % (tag, label, ("— " + detail) if detail and not cond else ""))
    if not cond:
        FAIL.append(label)


def menu_labels(menu_widget):
    """Alle Einträge eines tk-Öffnungmenüs (index('end') = LETZTER Index)."""
    m = menu_widget["menu"]
    i = m.index("end")
    if i is None:
        return []
    return [m.entrycget(idx, "label") for idx in range(i + 1)]


def pick_menu(menu_widget, label):
    """Wählt einen Menüeintrag per Label aus (lädt die tk-konforme invoke())."""
    labels = menu_labels(menu_widget)
    menu_widget["menu"].invoke(labels.index(label))


def grid_cells(widget):
    """Set von (row, col)-Zellen, die das Widget (inkl. rowspan/colspan) belegt."""
    cells = set()
    try:
        gi = widget.grid_info()
    except Exception:
        return cells
    if "row" not in gi:
        return cells
    r, c = int(gi["row"]), int(gi["column"])
    rs = int(gi.get("rowspan", 1))
    cs = int(gi.get("colspan", 1))
    for ri in range(r, r + rs):
        for ci in range(c, c + cs):
            cells.add((ri, ci))
    return cells


def build_window():
    ep = mod.EPCalcWin.__new__(mod.EPCalcWin)
    ep.lang = "de"
    ep.charlist = [dict(c) for c in CHARS]
    ep.window = tk.Tk()
    ep.window.withdraw()
    ep.menu = tk.Menu(ep.window)
    ep.window.configure(menu=ep.menu)
    ep._EPCalcWin__winCasting()
    return ep, ep.win_casting


# --------------------------------------------------------------------- tests
def test_default_char_selection(ep, top):
    """BUG-2257: Fenster öffnet mit gültiger Auswahl, Listen gefüllt."""
    menus = [w for w in top.winfo_children() if isinstance(w, tk.OptionMenu)]
    char_menu = menus[0]
    # Menubutton-Text spiegelt die zugehörige StringVar
    shown = str(char_menu.cget("text"))
    check("char-Auswahl initial != leer", shown != "" and shown is not None,
          "gezeigt %r" % shown)
    list_menu = menus[1]
    check("Spruchlisten-Menü initial nicht leer", len(menu_labels(list_menu)) > 0,
          "Menü leer")


def test_bug_2254_learned_lists(ep, top):
    """BUG-2254: genau die erlernten Listen (rank>0), nicht nur Bonus>0."""
    menus = [w for w in top.winfo_children() if isinstance(w, tk.OptionMenu)]
    char_menu, list_menu = menus[0], menus[1]
    # 'Testling' anwählen (standard-OptionMenu-Callback)
    pick_menu(char_menu, "Testling")
    ep.window.update()
    got = menu_labels(list_menu)
    check("exakt Inner Walls + Moving Ways",
          got == ["Inner Walls", "Moving Ways"], "got %r" % got)
    check("Moving Ways (rank>0, Bonus 0) vorhanden", "Moving Ways" in got)
    check("Path Mastery (Bonus>0, rank 0) NICHT vorhanden",
          "Path Mastery" not in got)


def test_bug_2255_callbacks(ep, top):
    """BUG-2255: Refill behält Callback — Listenwechsel + Zauberwahl wirken."""
    menus = [w for w in top.winfo_children() if isinstance(w, tk.OptionMenu)]
    list_menu, spell_menu = menus[1], menus[2]
    pick_menu(list_menu, "Inner Walls")
    ep.window.update_idletasks()
    sp = menu_labels(spell_menu)
    check("Inner Walls → nur Frost (Fire Lvl5 > rank3)", sp == ["Frost"],
          "got %r" % sp)
    pick_menu(list_menu, "Moving Ways")
    ep.window.update_idletasks()
    sp2 = menu_labels(spell_menu)
    check("Moving Ways → Run (Menü wurde aktualisiert)", sp2 == ["Run"],
          "got %r" % sp2)
    # Info-Text bei Zauberwahl aktualisiert
    sms = spell_menu["menu"]
    sp_labels = menu_labels(spell_menu)
    if "Run" in sp_labels:
        sms.invoke(sp_labels.index("Run"))
        ep.window.update_idletasks()
        inf = [w for w in top.winfo_children() if isinstance(w, tk.Text)][0]
        txt = inf.get("1.0", "end")
        check("Info-Text zeigt gewählten Zauber", "Run" in txt, repr(txt[:80]))


def test_bug_2256_layout(ep, top):
    """BUG-2256: keine Grid-Kollisionen + Labels lesbar (fg != #333333)."""
    occupancy = {}
    collisions = []
    for w in top.winfo_children():
        for cell in grid_cells(w):
            owner = occupancy.get(cell)
            if owner is not None and owner is not w:
                collisions.append(cell)
            occupancy[cell] = w
    check("keine Grid-Zellen doppelt belegt", not collisions,
          "Kollisionen: %r" % sorted(set(collisions)))
    bad = []
    for w in top.winfo_children():
        if not isinstance(w, tk.Label):
            continue
        try:
            fg, bg = w.cget("fg"), w.cget("bg")
        except Exception:
            continue
        if fg == "#333333" or (fg == bg and fg not in ("systemForeground", "")):
            bad.append(str(w.cget("text")))
    check("alle Labels lesbar auf Standard-Hintergrund", not bad, "unreadable: %r" % bad)


def main():
    ep, top = build_window()
    print("== epcalcWin Zaubern-Window Tests ==")
    test_default_char_selection(ep, top)
    test_bug_2254_learned_lists(ep, top)
    test_bug_2255_callbacks(ep, top)
    test_bug_2256_layout(ep, top)
    print()
    if FAIL:
        print("ERGEBNIS: %d FAIL —" % len(FAIL))
        for f in FAIL:
            print("  -", f)
        sys.exit(1)
    print("ERGEBNIS: alle Tests ok (BUG-2254, 2255, 2256, 2257 grün)")
    sys.exit(0)


if __name__ == "__main__":
    main()
