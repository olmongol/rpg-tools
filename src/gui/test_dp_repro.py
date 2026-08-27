"""Reproduction harness for DP deduction in skillcatWin (skill + cat paths).

Instantiates the real window class under Xvfb with a character copy,
selects items in the real treeview, raises the real spinboxes, and
invokes the real button commands. Prints __usedDP / DPtext before/after.

Usage: xvfb-run -a python3 gui/test_dp_repro.py
"""
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/
TESTDATA = tempfile.mkdtemp(prefix="dptest_")

src = os.path.join(ROOT, "data", "Marcus", "Finrion.json")
dst_dir = os.path.join(TESTDATA, "Marcus")
os.makedirs(dst_dir)
shutil.copy(src, dst_dir + os.sep + "Finrion.json")

os.chdir(TESTDATA)   # spath default = cwd/data  -> TESTDATA/data ? no: cwd/data
# skillcatWin default spath: os.getcwd() + "/data"
os.makedirs("data", exist_ok=True)
shutil.move(dst_dir, os.path.join("data", "Marcus"))

sys.path.insert(0, ROOT)

import tkinter
# prevent mainloop from blocking
tkinter.Misc.mainloop = lambda self, *a, **k: None
# suppress message windows (no_dp etc.) from popping blocking toplevels
from gui import window as _gw
_gw.messageWindow.showinfo = lambda self, *a, **k: None
_gw.messageWindow.showwarning = lambda self, *a, **k: None
_gw.messageWindow.showerror = lambda self, *a, **k: None

from gui.epwins import skillcatWin

char = json.load(open("data/Marcus/Finrion.json"))
print(f"character: {char['name']}  DP={char.get('DP')}  lvlup={char.get('lvlup')}")

win = skillcatWin(lang="en", char=char)

tree = win._skillcatWin__tree
takeValsSkill = win._skillcatWin__takeValsSkill
takeValsCat = win._skillcatWin__takeValsCat
sel = lambda i: (tree.focus(i), win._skillcatWin__selectTreeItem(None)) and i

def state(tag):
    used = win._skillcatWin__usedDP
    dpt = win.DPtext.get()
    print(f"  [{tag}] __usedDP={used}  DPtext='{dpt}'  (char DP={char['DP']})")
    return used, dpt

all_items = list(tree.get_children(""))
cats = [i for i in all_items if "category" in tree.item(i)["tags"]]
skills = []
for c in cats:
    skills += [i for i in tree.get_children(c) if "category" not in tree.item(i)["tags"]]

# ---- pick one cat and one skill ----
cat_id = cats[2]
cat_name = tree.item(cat_id)["text"]
cat_rank = tree.item(cat_id)["values"][3]
cat_costs = tree.item(cat_id)["values"][2]
print(f"\n=== CAT TEST: '{cat_name}'  rank={cat_rank}  costs={cat_costs}")
sel(cat_id)
state("before")
win._catspin.delete(0, "end")
win._catspin.insert(0, str(int(cat_rank) + 1))   # raise 1 level
try:
    takeValsCat()
except Exception as e:
    print("  EXCEPTION in takeValsCat:", type(e).__name__, e)
state("after  cat rank+1")

skill_id = skills[1]
parent = tree.parent(skill_id)
sk_name = tree.item(skill_id)["text"]
sk_rank = tree.item(skill_id)["values"][3]
sk_costs = tree.item(skill_id)["values"][2]
print(f"\n=== SKILL TEST: '{tree.item(parent)['text']}' / '{sk_name}'  rank={sk_rank}  costs={sk_costs}")
sel(skill_id)
state("before")
win._skillspin.delete(0, "end")
win._skillspin.insert(0, str(int(sk_rank) + 1))  # raise 1 level
try:
    takeValsSkill()
except Exception as e:
    print("  EXCEPTION in takeValsSkill:", type(e).__name__, e)
state("after skill rank+1")

chgtree = win._skillcatWin__chgtree
print("\n=== chgtree rows:", chgtree.get_children(""))
for r in chgtree.get_children(""):
    print("   ", tree.item(r)["text"], tree.item(r)["values"])
print("\nDONE")
