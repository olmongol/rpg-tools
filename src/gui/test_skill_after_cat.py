"""Reproduction harness: cat level-up FIRST, then a SKILL of the SAME category.

This is the real GUI flow the user is hitting: pick a skill below a category,
raise the category button (takeValsCat), then raise a skill inside that same
already-changed category (takeValsSkill -> "cat in __changed" branch, skill
in changed). Prints __usedDP before/after; expects either UnboundLocalError
('lowval') or a silently skipped deduction.

Usage: xvfb-run -a python3 gui/test_skill_after_cat.py
"""
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/
TESTDATA = tempfile.mkdtemp(prefix="catfirst_")

src = os.path.join(ROOT, "data", "Marcus", "Finrion.json")
dst_dir = os.path.join(TESTDATA, "Marcus")
os.makedirs(dst_dir)
shutil.copy(src, dst_dir + os.sep + "Finrion.json")
os.chdir(TESTDATA)
os.makedirs("data", exist_ok=True)
shutil.move(dst_dir, os.path.join("data", "Marcus"))

sys.path.insert(0, ROOT)

import tkinter
tkinter.Misc.mainloop = lambda self, *a, **k: None
from gui import window as _gw
_gw.messageWindow.showinfo = lambda self, *a, **k: print("  [showinfo called]")
_gw.messageWindow.showwarning = lambda self, *a, **k: print("  [showwarning called]")
_gw.messageWindow.showerror = lambda self, *a, **k: print("  [showerror called]", *a)
_gw.messageWindow.show = lambda self, *a, **k: print("  [show called]", *a)

from gui.epwins import skillcatWin

char = json.load(open("data/Marcus/Finrion.json"))
print(f"character: {char['name']}  DP={char.get('DP')}  lvlup={char.get('lvlup')}")

win = skillcatWin(lang="en", char=char)
tree = win._skillcatWin__tree
sel = lambda i: (tree.focus(i), win._skillcatWin__selectTreeItem(None)) and i

def state(tag):
    used = win._skillcatWin__usedDP
    dpt = win.DPtext.get()
    print(f"  [{tag}] __usedDP={used}  DPtext='{dpt}'  (char DP={char['DP']})")
    return used, dpt

cats = [i for i in tree.get_children("") if "category" in tree.item(i)["tags"]]

# pick the FIRST cat and a skill INSIDE it (same category!)
cat_id = cats[0]
cat_name = tree.item(cat_id)["text"]
cat_rank = tree.item(cat_id)["values"][3]
cat_costs = tree.item(cat_id)["values"][2]
sk_id = [i for i in tree.get_children(cat_id) if "category" not in tree.item(i)["tags"]][0]
sk_name = tree.item(sk_id)["text"]
sk_rank = tree.item(sk_id)["values"][3]
sk_costs = tree.item(sk_id)["values"][2]
print(f"\n=== CAT FIRST: '{cat_name}'  rank={cat_rank}  costs={cat_costs}")
sel(cat_id)
state("before")
win._catspin.delete(0, "end")
win._catspin.insert(0, str(int(cat_rank) + 1))
try:
    win._skillcatWin__takeValsCat()
except Exception as e:
    print("  EXCEPTION in takeValsCat:", type(e).__name__, e)
state("after  cat rank+1")

print(f"\n=== SAME-CAT SKILL AFTER: '{cat_name}' / '{sk_name}'  rank={sk_rank}  costs={sk_costs}")
sel(sk_id)
state("before")
win._skillspin.delete(0, "end")
win._skillspin.insert(0, str(int(sk_rank) + 1))
try:
    win._skillcatWin__takeValsSkill()
except Exception as e:
    print("  EXCEPTION in takeValsSkill (SAME-CAT):", type(e).__name__, e)
state("after  skill rank+1 (SAME CAT as cat-abzug)")

print("\n=== chgtree rows:", win._skillcatWin__chgtree.get_children(""))
print("\nDONE")
