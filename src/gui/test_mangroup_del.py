#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests — gui/mangroup.py groupWin.__remChar (BUG-2258).

Befund vor Fix: __remChar parste das Listbox-Label mit
re.match(r"^([a-zA-Z ]+): ([a-zA-Z 0-9]+) \\(.+\\)$") und loeschte aus
charlist NUR bei Treffer. Namen mit Umlauten (z.B. "Gruenblatt")
passierten nicht [a-zA-Z ]+ -> das Listbox-Item verschwand, der
Charakter blieb in charlist und wurde beim Speichern zurueckgeschrieben.
Zweitdefekt im selben Block: die del-Loops lagen IN der
Selektions-For-Schleife -> bei Mehrfachauswahl wurden die Indizes
doppelt/versetzt verwendet.

Fix: Loeschung per Listenposition (Listbox-Eintrag i <-> charlist[i]),
absteigend, Listenbox und charlist synchron.

Lauf:   python3 gui/test_mangroup_del.py        (kein Display noetig)
Beendet mit 0 wenn alle Gruen, 1 sonst.
"""
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from gui.mangroup import groupWin  # noqa: E402

FAIL = []


def check(label, cond, detail=""):
    tag = "ok  " if cond else "FAIL"
    print("  [%s] %s %s" % (tag, label, ("— " + detail) if detail and not cond else ""))
    if not cond:
        FAIL.append(label)


class FakeBox(object):
    """Mini-Fake fuer Listbox: Index-Semantik von delete wie tk."""

    def __init__(self, entries):
        self.items = list(entries)
        self.selected = set()

    def curselection(self):
        return tuple(sorted(self.selected))

    def delete(self, i):
        del self.items[i]


def make_group(names):
    """Deterministische Gruppen-Daten (inkl. Umlaut- + Leerzeichen-Faelle)."""
    grp = []
    for player, name in names:
        grp.append({
            "player": player,
            "name": name,
            "prof": "Ranger",
            "lvl": 3,
            "culture": "Woodmen",
            "race": "Men",
        })
    return grp


def build(names):
    """groupWin ohne GUI; __remChar bekommt ein Fake-Listbox + charlist."""
    gw = groupWin.__new__(groupWin)
    grp = make_group(names)
    gw.charlist = grp
    labels = ["%s: %s (Ranger-3/Woodmen/Men)" % (p, n) for p, n in names]
    gw.charbox = FakeBox(labels)
    return gw, grp


def names(cast):
    return [c["name"] for c in cast]


def test_single_umlaut_name():
    """Umlaut-Name: Listbox + charlist + Speichern — alle drei ohne Eintrag."""
    print("== BUG-2258 a: Single Delete mit Umlaut ==")
    data = [("Katrin", "Alchemilla Grünblatt"),
            ("Marcus", "Finrion"),
            ("Aiko", "Carastan")]
    gw, grp = build(data)
    gw.charbox.selected.add(0)
    gw._groupWin__remChar()
    check("Listbox-Eintrag weg", len(gw.charbox.items) == 2,
          str(gw.charbox.items))
    check("charlist um 1 geschrumpft", len(grp) == 2, str([c["name"] for c in grp]))
    check("Umlaut-Name NICHT in charlist", "Alchemilla Grünblatt" not in names(grp))
    blob = json.dumps(grp, ensure_ascii=False)
    check("Umlaut-Name NICHT im JSON-Dump", "Grünblatt" not in blob)
    check("uebrige beiden Charaktere intakt",
          names(grp) == ["Finrion", "Carastan"], str(names(grp)))


def test_single_plain_name():
    print("== BUG-2258 b: Single Delete normaler Name ==")
    gw, grp = build([("Katrin", "Alchemilla Grünblatt"),
                     ("Marcus", "Finrion"),
                     ("Aiko", "Carastan")])
    gw.charbox.selected.add(2)
    gw._groupWin__remChar()
    check("charlist 2 Eintraege", len(grp) == 2, str(names(grp)))
    check("Carastan weg, andere bleiben",
          names(grp) == ["Alchemilla Grünblatt", "Finrion"], str(names(grp)))


def test_multi_select():
    print("== BUG-2258 c: Mehrfachauswahl (Index-Sicherheit) ==")
    gw, grp = build([("Katrin", "Alchemilla Grünblatt"),
                     ("Dunja", "Almiel"),
                     ("Marcus", "Finrion"),
                     ("Niels", "Isdan"),
                     ("Aiko", "Carastan"),
                     ("Meike", "Jeanny")])
    # Katrin(0, Umlaut) + Niels(3) zusammen loeschen
    gw.charbox.selected.update({0, 3})
    gw._groupWin__remChar()
    check("6 - 2 = 4 Eintraege", len(grp) == 4, str(names(grp)))
    check("Katrin und Niels weg, Reihenfolge der Restlichen intakt",
          names(grp) == ["Almiel", "Finrion", "Carastan", "Jeanny"],
          str(names(grp)))
    check("Listbox == charlist Groesstengleich", len(gw.charbox.items) == len(grp))


def test_empty_selection_noop():
    print("== BUG-2258 d: Leere Auswahl aendert nichts ==")
    gw, grp = build([("Katrin", "Alchemilla Grünblatt"),
                     ("Marcus", "Finrion")])
    gw._groupWin__remChar()
    check("charlist unveraendert", len(grp) == 2, str(names(grp)))
    check("Listbox unveraendert", len(gw.charbox.items) == 2)


def main():
    print("== mangroup __remChar Tests (BUG-2258) ==")
    test_single_umlaut_name()
    test_single_plain_name()
    test_multi_select()
    test_empty_selection_noop()
    print()
    if FAIL:
        print("ERGEBNIS: %d FAIL —" % len(FAIL))
        for f in FAIL:
            print("  -", f)
        sys.exit(1)
    print("ERGEBNIS: alle Tests ok (BUG-2258 gruen)")
    sys.exit(0)


if __name__ == "__main__":
    main()
