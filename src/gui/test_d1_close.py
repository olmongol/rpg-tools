#!/usr/bin/env python3
"""D1 regression harness: closewin (ohne Finalize) muss die reservierten
DP in den Charakter commit-en (DP -= reserved, lvlup -= 1, usedDP -> 0).

Run:  xvfb-run -a python3 gui/test_d1_close.py
"""
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/
TESTDATA = tempfile.mkdtemp(prefix="d1test_")

src = os.path.join(ROOT, "data", "Marcus", "Finrion.json")
dst_dir = os.path.join(TESTDATA, "Marcus")
os.makedirs(dst_dir)
shutil.copy(src, dst_dir + os.sep + "Finrion.json")
os.chdir(TESTDATA)
os.makedirs("data", exist_ok=True)
shutil.move(dst_dir, os.path.join("data", "Marcus"))
if not os.path.islink(os.path.join("data", "default")):
    os.symlink(os.path.join(ROOT, "data", "default"), os.path.join("data", "default"))
if not os.path.islink("gui"):
    os.makedirs("gui", exist_ok=True)
if not os.path.islink(os.path.join("gui", "pic")):
    os.symlink(os.path.join(ROOT, "gui", "pic"), os.path.join("gui", "pic"))

sys.path.insert(0, ROOT)

import tkinter
tkinter.Misc.mainloop = lambda self, *a, **k: None
from gui import window as _gw
_gw.messageWindow.showinfo = lambda self, *a, **k: None
_gw.messageWindow.showwarning = lambda self, *a, **k: None
_gw.messageWindow.showerror = lambda self, *a, **k: None

from gui import epwins as _ep
# closewin öffnet am Ende einen neuen MainWindow -> stubben (kein Hang,
# wir prüfen den DP-Commit vor dem Window-Austausch)


class _FakeMain:
    def __init__(self, *a, **kw):
        pass


_ep.MainWindow = _FakeMain

from gui.epwins import skillcatWin

char = json.load(open("data/Marcus/Finrion.json"))
DP0 = int(char["DP"])
LVL0 = int(char["lvlup"])

win = skillcatWin(lang="en", char=char)
tree = win._skillcatWin__tree
M = "_skillcatWin__"

# ---- setup: realer Rank-Zuwachs (Kategorie), Reservierung im Ledger ----
all_items = list(tree.get_children(""))
cats = [i for i in all_items if "category" in tree.item(i)["tags"]]
cat_id = cats[2]
tree.focus(cat_id)
win._skillcatWin__selectTreeItem(None)
win._catspin.delete(0, "end")
win._catspin.insert(0, str(int(tree.item(cat_id)["values"][3]) + 1))
win._skillcatWin__takeValsCat()
RES = win._skillcatWin__usedDP
assert RES > 0, "setup: rank increase should reserve DP"
assert int(char["DP"]) == DP0, "setup: reservation must stay in the ledger"
print(f"setup: reserved={RES}  charDP={char['DP']} (orig {DP0}) lvlup={char['lvlup']} (orig {LVL0})")

prev_win = win.window
lvl_before_close = int(char["lvlup"])
dp_before_close = int(char["DP"])

win._skillcatWin__closewin()

char_ref = win._character  # closewin hat win.window neuinstanziert
used_after = getattr(win, M + "usedDP")
ok = (
    used_after == 0
    and int(char_ref["DP"]) == dp_before_close - RES
    and int(char_ref["lvlup"]) == max(lvl_before_close - 1, 0)
)
print(
    f"nach closewin: DP={char_ref['DP']} (vor={dp_before_close}, expected {dp_before_close - RES}) "
    f"lvlup={char_ref['lvlup']} (vor={lvl_before_close}) usedDP={used_after} (expected 0)"
)
print("D1-CLOSEWIN:", "OK (Reservation commitet, Ledger geleert)" if ok else "FAIL")
sys.exit(0 if ok else 1)
