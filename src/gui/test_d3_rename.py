"""D3 regression harness: __renameSkill must NOT bake the session DP
reservation into character['DP'] (neither on success nor on failure).

Run:  xvfb-run -a python3 gui/test_d3_rename.py
"""
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/
TESTDATA = tempfile.mkdtemp(prefix="d3test_")

src = os.path.join(ROOT, "data", "Marcus", "Finrion.json")
dst_dir = os.path.join(TESTDATA, "Marcus")
os.makedirs(dst_dir)
shutil.copy(src, dst_dir + os.sep + "Finrion.json")
os.chdir(TESTDATA)
os.makedirs("data", exist_ok=True)
shutil.move(dst_dir, os.path.join("data", "Marcus"))
# default game data (ProfBonus etc.) — __finalize's choseProfession reads it
if not os.path.islink(os.path.join("data", "default")):
    os.symlink(os.path.join(ROOT, "data", "default"), os.path.join("data", "default"))
# picpath is CWD-relative ("./gui/pic/") — __finalize's charInfo->inputWin
# loads assassin.gif from it, so link the real pic dir into the test CWD
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

from gui.epwins import skillcatWin

char = json.load(open("data/Marcus/Finrion.json"))
DP0 = int(char["DP"])

win = skillcatWin(lang="en", char=char)
used = win._skillcatWin__usedDP
rename = win._skillcatWin__renameSkill
tree = win._skillcatWin__tree
M = "_skillcatWin__"

# ---- setup: one real rank increase (reservation in ledger) ----
all_items = list(tree.get_children(""))
cats = [i for i in all_items if "category" in tree.item(i)["tags"]]
skills = []
for c in cats:
    skills += [i for i in tree.get_children(c) if "category" not in tree.item(i)["tags"]]
cat_id = cats[2]
# NOTE: __selectTreeItem re-populates the spinboxes, so the new rank
# value must be entered AFTER the selection, not before.
tree.focus(cat_id)
win._skillcatWin__selectTreeItem(None)
win._catspin.delete(0, "end")
win._catspin.insert(0, str(int(tree.item(cat_id)["values"][3]) + 1))
win._skillcatWin__takeValsCat()
RES = win._skillcatWin__usedDP
assert RES > 0, "setup: rank increase should reserve DP"
assert int(char["DP"]) == DP0, "setup: reservation must stay in the ledger"
print(f"setup: reserved={RES}  charDP={char['DP']} (orig {DP0})")

# ---- failure path: rebuild raises -> full rollback required ----
sk_id = skills[1]
parent = tree.parent(sk_id)
oldname = tree.item(sk_id)["text"]
cat_name = tree.item(parent)["text"]
cat_dict = char["cat"][cat_name]
newname = oldname + "_testrename"
# NOTE: __selectTreeItem overwrites _skillentry with the old skill name
# (skill-branch, epwins.py L2815), so it must be run FIRST and the
# new name entered afterwards — mirrors real GUI use (select, then type).
tree.focus(sk_id)
win._skillcatWin__selectTreeItem(None)
win._skillentry.delete(0, "end")
win._skillentry.insert(0, newname)

orig_calc = getattr(win, M + "calcTotals")
setattr(win, M + "calcTotals", lambda: (_ for _ in ()).throw(RuntimeError("boom-d3")))
failed = False
try:
    rename()
except RuntimeError:
    failed = True
setattr(win, M + "calcTotals", orig_calc)

ok_fail = (
    failed
    and int(char["DP"]) == DP0
    and win._skillcatWin__usedDP == RES
    and newname not in cat_dict["Skill"]
    and oldname in cat_dict["Skill"]
)
print("FAIL-PATH:", "OK" if ok_fail else
      "BROKEN  (failed=%s charDP=%s used=%s newIn=%s oldIn=%s)" % (
          failed, char["DP"], win._skillcatWin__usedDP,
          newname in cat_dict["Skill"], oldname in cat_dict["Skill"]))

# ---- success path: reserve must stay in ledger (finalize-only commit) ----
# select first, then set the new name (see NOTE in FAIL-PATH section)
tree.focus(sk_id)
win._skillcatWin__selectTreeItem(None)
win._skillentry.delete(0, "end")
win._skillentry.insert(0, newname)
rename()
ok_ok = (
    int(char["DP"]) == DP0
    and win._skillcatWin__usedDP == RES
    and newname in cat_dict["Skill"]
)
# NOTE: __calcTotals re-assigns self._character (new dict object) —
# re-resolve references before judging the OK-path.
char_ref = win._character
char = char_ref
cat_dict = char["cat"][cat_name]
print("OK-PATH: ", "OK" if ok_ok else
      "BROKEN  (charDP=%s used=%s newIn=%s oldIn=%s)" % (
          char["DP"], win._skillcatWin__usedDP,
          newname in cat_dict["Skill"], oldname in cat_dict["Skill"]))

# ---- finalize path: only now do the reserved DP leave available pool ----
used_before_fin = win._skillcatWin__usedDP
win._skillcatWin__finalize()
ok_fin = (
    int(char["DP"]) == DP0 - RES
    and win._skillcatWin__usedDP == 0
)
print("FINALIZE:", "OK" if ok_fin else
      "BROKEN  (charDP=%s used=%s  expected=%s 0)" % (
          char["DP"], win._skillcatWin__usedDP, DP0 - RES))

if ok_fail and ok_ok and ok_fin:
    print("\nD3 ALL GREEN")
else:
    print("\nD3 FAILURES PRESENT")
    sys.exit(1)
