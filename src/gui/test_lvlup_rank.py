#!/usr/bin/env python3
"""Regression test: 'Levelup after finalize — false ranks / over-max level-ups'.

Root cause identified in __takeValsSkill (gui/epwins.py): the guard
    lvlups <= len(dpCosts)
allows rank to be set to newrank even when no level-up slot is available
(lvlups already equals len(dpCosts)).  The `lvlups += diff` at the
corresponding `<` guard then adds 0, producing the documented symptom:
  'lvlups is correct but the new rank is wrong.'

Fix (to be applied):  change the six `<=` guards to `<` and move the rank
assignment inside the `<` block.

Harness mirrors test_final_save.py — no real tk.Tk() root, spin/tree
stubs, stub self with all attributes __takeValsSkill depends on.
"""
import os, sys, logging

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
os.environ.setdefault('DISPLAY', '')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

logging.basicConfig(level=logging.CRITICAL)

import epwins as epw
from epwins import skillcatWin

# ── monkeypatch module-level deps ──────────────────────────────────────
epw.calcTotals = lambda c: c
epw.getLvl     = lambda e: 1
# epwins_no_dp is defined in rpgtoolbox/lang.py already — leave screenmesg intact.
epw.rmlabels = {'en': {'costs': 'Costs'}}
epw.END = 'end'
# __info: no-op
skillcatWin._skillcatWin__info = lambda self, text='': None

# ── minimal tree and spin stubs ─────────────────────────────────────────
class TreeStub:
    def __init__(self, nodes):
        self.nodes = nodes
        self._focus = list(nodes)[0] if nodes else None
    def item(self, iid):            return self.nodes[iid]
    def parent(self, iid):          return self.nodes[iid]['parent']
    def focus(self):                return self._focus
    def set_focus(self, iid):       self._focus = iid
    def heading(self, *a, **kw):    pass
    def column(self, *a, **kw):     pass
    def tag_configure(self, *a, **kw): pass
    def bind(self, *a, **kw):       pass
    def insert(self, *a, **kw):     pass
    def get_children(self):
        return [k for k in self.nodes if self.nodes[k]['parent'] == '']
    def delete(self, *i):
        for x in i: self.nodes.pop(x, None)


class SpinStub:
    def __init__(self, v): self._v = int(v)
    def get(self):          return self._v
    def set(self, v):       self._v = int(v)
    def config(self, **kw): pass


def _calcRanks(progression, rank):
    """Copy of skillcatWin.__calcRanks for assertion purposes."""
    p = [int(x) for x in progression]
    if rank == 0:   return p[0]
    if 0 < rank < 11:    return int(p[1] * rank)
    if 10 <= rank < 21:  return int(p[1]*10 + p[2]*(rank % 10))
    return int((p[1]+p[2])*10 + p[3]*(rank % 10))

# ── stub self ───────────────────────────────────────────────────────────
def make_stub(char, spin_rank, cat, skill,
              cat_rank, skill_rank,
              cat_costs, skill_costs,
              cat_prog, skill_prog):
    """Build the minimal self object __takeValsSkill consumes.
    __takeValsSkill is called unbound:  METHOD(stub)."""
    s = type('S', (), {})()
    # Non-mangled attributes (single leading underscore)
    s.__dict__['_skillspin']   = SpinStub(spin_rank)
    s.__dict__['_character']   = char
    s.__dict__['lang']         = 'en'
    # Mangled attributes (double leading underscore → _skillcatWin__prefix)
    # __info: no-op (referenced on the bare stub via self.__info)
    s.__dict__['_skillcatWin__info'] = lambda self, text='': None

    s.__dict__['_skillcatWin__changed']  = {'cat': {}, 'name': 'T', 'player': 'P'}
    s.__dict__['_skillcatWin__usedDP']   = 0
    s.__dict__['_skillcatWin__rmlabels'] = epw.rmlabels

    nodes = {
        'cat':   {'values': (cat, cat_prog,  cat_costs,   cat_rank,   0),
                  'text': cat, 'tags': ['category'], 'parent': ''},
        'skill': {'values': (skill, skill_prog, skill_costs, skill_rank, 0),
                  'text': skill, 'tags': [cat], 'parent': 'cat'},
    }
    s.__dict__['_skillcatWin__tree']    = TreeStub(nodes)
    s.__dict__['_skillcatWin__curItem'] = 'skill'
    s.__dict__['_skillcatWin__chgtree'] = TreeStub({})

    # DP label (StringVar-ish) — set/get called at line 3239
    class _Var:
        def __init__(self, v=''): self._v = str(v)
        def set(self, v): self._v = str(v)
        def get(self): return self._v
    s.DPtext = _Var('0')

    # __buildChangedTree (line 3241) — no-op for this harness.
    # Assigned plain into __dict__, so it is invoked WITHOUT self.
    s.__dict__['_skillcatWin__buildChangedTree'] = lambda *a, **k: None

    # __calcRanks must be a callable that takes (progression, rank).
    def _cr(progression, rank):
        if isinstance(progression, str):
            p = [float(x) for x in progression.split()]
        else:
            p = progression
        return _calcRanks(p, rank)
    s.__dict__['_skillcatWin__calcRanks'] = _cr
    return s


def make_cat(cat='Athletics', rank=0, lvlups=0, DP=100,
              skill='Dagger',
              skill_rank=None, skill_lvlups=None,
              cat_costs='3 4 5', skill_costs='3 4 5',
              cat_prog='-2 2 1 0 0', skill_prog='-2 2 1 0 0'):
    """Return a minimal _character dict (single category + one skill)."""
    if skill_rank   is None: skill_rank   = rank
    if skill_lvlups is None: skill_lvlups = lvlups
    return {
        'DP': DP, 'lvl': 1, 'lvlup': 1, 'statgain': 10,
        'old_exp': 100, 'exp': 200, 'Hobby Ranks': 0,
        'Ag': {'temp': 10}, 'Co': {'temp': 10}, 'Me': {'temp': 10},
        'Re': {'temp': 10}, 'SD': {'temp': 10},
        'cat': {
            cat: {
                'Costs': cat_costs, 'Progression': cat_prog,
                'rank': rank, 'lvlups': lvlups, 'total bonus': 0,
                'rank bonus': 0, 'stat bonus': 0,
                'spec bonus': 0, 'item bonus': 0, 'prof bonus': 0,
                'Stats': ['Ag'],
                'Skill': {
                    skill: {
                        'Costs': skill_costs, 'Progression': skill_prog,
                        'rank': skill_rank, 'lvlups': skill_lvlups,
                        'total bonus': 0,
                        'rank bonus': 0, 'stat bonus': 0,
                        'spec bonus': 0, 'item bonus': 0, 'prof bonus': 0,
                    }
                }
            }
        }
    }


def run(scenario_name, char, spin_rank, cat, skill,
        cat_rank, skill_rank,
        cat_costs, skill_costs, cat_prog, skill_prog):
    """Invoke __takeValsSkill on a fresh stub and return the changed skill
    dict (or None if cat not in changed)."""
    s = make_stub(char, spin_rank, cat, skill,
                  cat_rank, skill_rank, cat_costs, skill_costs,
                  cat_prog, skill_prog)
    skillcatWin._skillcatWin__takeValsSkill(s)
    chg = s.__dict__['_skillcatWin__changed']['cat'].get(cat, {})
    return chg

# ── tests ───────────────────────────────────────────────────────────────

def test_fresh_single_level_up():
    """0 → 1.  One level-up, costs[0]=3, rank should go 0→1, lvlups→1."""
    char  = make_cat(rank=0, lvlups=0, skill_rank=0, skill_lvlups=0)
    chg   = run('fresh-0→1', char, spin_rank=1,
                cat='Athletics', skill='Dagger',
                cat_rank=0, skill_rank=0,
                cat_costs='3 4 5', skill_costs='3 4 5',
                cat_prog='-2 2 1 0 0', skill_prog='-2 2 1 0 0')
    if chg is None:
        raise AssertionError("cat not added to __changed — __takeValsSkill aborted")
    sk = chg['Skill']['Dagger']
    print(f"  fresh-0→1: rank={sk.get('rank')}  lvlups={sk.get('lvlups')}  (expect rank=1 lvlups=1)")
    assert sk['rank']  == 1, f"rank should be 1, got {sk['rank']}"
    assert sk['lvlups'] == 1, f"lvlups should be 1, got {sk['lvlups']}"


def test_fresh_up_to_max():
    """0 → 3 (max = len(costs)=3).  rank should go 0→3, lvlups→3."""
    char  = make_cat(rank=0, lvlups=0, skill_rank=0, skill_lvlups=0, DP=200)
    chg   = run('fresh-0→3', char, spin_rank=3,
                cat='Athletics', skill='Dagger',
                cat_rank=0, skill_rank=0,
                cat_costs='3 4 5', skill_costs='3 4 5',
                cat_prog='-2 2 1 0 0', skill_prog='-2 2 1 0 0')
    if chg is None:
        raise AssertionError("cat not added to __changed")
    sk = chg['Skill']['Dagger']
    print(f"  fresh-0→3: rank={sk.get('rank')}  lvlups={sk.get('lvlups')}  (expect rank=3 lvlups=3)")
    assert sk['rank']  == 3, f"rank should be 3, got {sk['rank']}"
    assert sk['lvlups'] == 3, f"lvlups should be 3, got {sk['lvlups']}"


def test_reedit_beyond_max_blocked():
    """Character fully leveled (rank 3, lvlups 3).  User sets spin to 4.
    rank MUST NOT be set to 4 (no level-up slot available)."""
    char  = make_cat(rank=3, lvlups=3, skill_rank=3, skill_lvlups=3, DP=50)
    chg   = run('reedit-3→4-blocked', char, spin_rank=4,
                cat='Athletics', skill='Dagger',
                cat_rank=3, skill_rank=3,
                cat_costs='3 4 5', skill_costs='3 4 5',
                cat_prog='-2 2 1 0 0', skill_prog='-2 2 1 0 0')
    if chg is None:
        raise AssertionError("cat not added to __changed — but it must be (no exception)")
    sk = chg['Skill']['Dagger']
    print(f"  reedit-3→4-blocked: rank={sk.get('rank')}  lvlups={sk.get('lvlups')}  (expect rank=3 lvlups=3)")
    assert sk['rank']  == 3, f"rank over-max: got {sk['rank']}, expected 3 (blocked)"
    assert sk['lvlups'] <= 3, f"lvlups over-max: got {sk['lvlups']}, expected <=3"


def main():
    import time
    start  = time.time()
    tests  = [
        ('Fresh single level-up (0→1)',       test_fresh_single_level_up),
        ('Fresh to max (0→3)',                test_fresh_up_to_max),
        ('Re-edit beyond max blocked (3→4)',  test_reedit_beyond_max_blocked),
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
        print('  RESULT: RED (expected before fix)');  sys.exit(1)
    print('  RESULT: GREEN');                           sys.exit(0)

if __name__ == '__main__':
    main()