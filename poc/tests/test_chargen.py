"""Tests für CharGen (Task 9) + char_def-Loader-Validation (Task 4).

Lauf: python3 -m pytest poc/tests/test_chargen.py -v
Deterministisch: fester seed bzw. base-Würfe, nie ungesteuert zufällig.
Anker-Werte der Stat-Mathematik sind aus dem Legacy (rpgtoolbox/rolemaster.py
statbonus/pointsneeded) übernommen und dort 1:1 verifiziert (alle v in 1..100).
"""
import copy
import dataclasses

import pytest

from rpgpoc import (
    CharGen,
    ChargenError,
    ChargenStepError,
    LocalJsonStore,
    TemplateLoadError,
    apply_event,
    empty_state,
    fold,
    load_template,
    points_needed,
    stat_bonus,
)
from rpgpoc.events import Event, UnknownEventType

TPL = "/home/mongol/git/rpg-tools/poc/templates/rolemaster"
CAT = "Spells - Own Realm Open Lists"

SEQ = ["step_race", "step_folk", "step_occupation", "step_stats",
       "step_categories", "step_equipment", "step_bgos"]


@pytest.fixture(scope="module")
def spec():
    return load_template(TPL)


def make_cg(spec, seed=7):
    public = {k: v for k, v in spec.items() if not k.startswith("_")}
    return CharGen(definition=public, char_def=spec.get("char_def"),
                   seed=seed)


def defaults(upto):
    """Feste Testwerte für die Schritte race..upto (inkl.)."""
    return {
        "step_race": {"name": "Wood Elves"},
        "step_folk": {"name": "Silvanii"},
        "step_occupation": {"name": "Magician"},
        "step_stats": {"pool": 300},
        "step_categories": {"names": [CAT]},
        "step_equipment": {"items": [{"name": "staff"}], "purse": 12},
        "step_bgos": {"entries": [
            {"kind": "nachteil", "name": "Bereits verflucht"},
            {"kind": "vorteil", "name": "Nahsicht", "cost": 1},
        ]},
    }


def run_prefix(cg, upto, **overrides):
    """Schritte race..*upto* abarbeiten (feste Werte, overrides erlaubt)."""
    vals = defaults(upto)
    vals.update(overrides)
    i = SEQ.index(upto)
    for j, step in enumerate(SEQ[:i + 1]):
        getattr(cg, step)(**vals[step])


# ---------------------------------------------------------------- stat-math --

def test_stat_bonus_matches_legacy_anchors():
    # Anker aus dem Legacy rolemaster.statbonus (1:1 verifiziert v in 1..100)
    assert stat_bonus(1) == -10
    assert stat_bonus(10) == -6      # (10-21)/2 = -5.5 -> banker's -6
    assert stat_bonus(11) == -4
    assert stat_bonus(30) == -1      # 10 < t < 31 -> (30-33)/5 = -0.6
    assert stat_bonus(31) == 0
    assert stat_bonus(50) == 0
    assert stat_bonus(69) == 0       # 30 < t < 70 -> 0 (Legacy-Bruch)
    assert stat_bonus(70) == 1
    assert stat_bonus(89) == 4
    assert stat_bonus(90) == 4       # (90-81)/2 = 4.5 -> banker's 4
    assert stat_bonus(91) == 5
    assert stat_bonus(100) == 10
    assert all(isinstance(stat_bonus(v), int) for v in range(1, 101))


def test_points_needed_matches_legacy():
    assert points_needed(15) == 20   # clamp auf 20 (Legacy: Ergebnis 20)
    assert points_needed(20) == 20
    assert points_needed(50) == 50
    assert points_needed(90) == 90
    assert points_needed(91) == 91
    assert points_needed(95) == 115  # 90 + 25
    assert points_needed(100) == 190
    assert isinstance(points_needed(99), int)


# ------------------------------------------------------------- loader/chardef

def test_loader_exposes_char_def_races(spec):
    races = spec["char_def"]["races"]
    names = [r["name"] for r in races]
    assert "Wood Elves" in names and "Common Men" in names
    we = next(r for r in races if r["name"] == "Wood Elves")
    assert we["stats"]["Ag"] == 4 and we["stats"]["Pr"] == 2
    assert we["bgo"] == 4 and isinstance(we["bgo"], int)


def test_loader_rejects_unknown_stat_in_race(tmp_path):
    d = open(f"{TPL}/definition.yaml", encoding="utf-8").read()
    root = tmp_path / "badtpl"
    root.mkdir()
    (root / "definition.yaml").write_text(d, encoding="utf-8")
    cd = root / "char_def"
    cd.mkdir()
    (cd / "races.yaml").write_text(
        "races:\n  - name: Bad\n    stats:\n      NoStat: 2\n",
        encoding="utf-8")
    with pytest.raises(TemplateLoadError,
                       match="nicht in definition.stats"):
        load_template(str(root))


def test_loader_rejects_non_int_bgo_budget(tmp_path):
    d = open(f"{TPL}/definition.yaml", encoding="utf-8").read()
    root = tmp_path / "badtpl2"
    root.mkdir()
    (root / "definition.yaml").write_text(d, encoding="utf-8")
    cd = root / "char_def"
    cd.mkdir()
    (cd / "races.yaml").write_text(
        "races:\n  - name: Bad\n    bgo: lots\n", encoding="utf-8")
    with pytest.raises(TemplateLoadError, match="bgo-Budget muss int"):
        load_template(str(root))


# ------------------------------------------------------------------ Schritte -

def test_step_order_enforced(spec):
    cg = make_cg(spec)
    with pytest.raises(ChargenStepError, match="erwarteter Schritt 'folk'"):
        cg.step_folk("Silvanii")


def test_step_cannot_repeat(spec):
    cg = make_cg(spec)
    cg.step_race("Wood Elves")
    with pytest.raises(ChargenStepError,
                       match="erwarteter Schritt 'race'"):
        cg.step_race("Dwarves")


def test_unknown_race_rejected(spec):
    cg = make_cg(spec)
    with pytest.raises(ChargenError, match="unbekannte Rasse"):
        cg.step_race("Klingon")


def _stats_rows(out):
    return {k: v for k, v in out.items() if k != "pool_remaining"}


def test_stats_pool_distribution(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_stats",
               **{"step_stats": {"pool": 300}})
    out = cg._payload["stats"]  # Ergebnis des letzten _advance
    rows = _stats_rows(out)
    assert len(rows) == 10
    for v in rows.values():
        assert all(isinstance(v[k], int) for k in
                   ("base", "race", "temp", "bonus", "cost"))
        assert 1 <= v["temp"] <= 100
        assert v["bonus"] == stat_bonus(v["temp"])
        assert v["cost"] == points_needed(v["temp"])
    # DP-Spend: Summe der Stufen-Kosten ueber die Startallokation.
    spend = sum(
        points_needed(v["temp"]) - points_needed(max(1, min(
            100, v["base"] + v["race"])))
        for v in rows.values())
    assert spend <= 300
    assert out["pool_remaining"] == 300 - spend


def test_stats_base_override_deterministic(spec):
    cg = make_cg(spec, seed=1)
    base = {i: 50 for i in range(10)}
    vals = defaults("step_stats")
    vals["step_stats"] = {"pool": 100, "base": base}
    vals.update({"step_race": {"name": "Common Men"}})
    for step in SEQ[:4]:
        getattr(cg, step)(**vals.get(step, {}))
    out = cg._payload["stats"]
    rows = _stats_rows(out)
    for a, v in rows.items():
        assert v["base"] == 50
        # DP kann nur addieren (oder die 100-Clamp halten):
        assert v["temp"] >= min(100, 50 + v["race"])


def test_stats_bad_base_mapping_rejected(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_occupation")
    with pytest.raises(ChargenError, match="Keys 0..9"):
        cg.step_stats(pool=100, base={1: 50, 2: 50})


def test_categories_validated(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_stats")
    with pytest.raises(ChargenError, match="unbekannte Kategorie"):
        cg.step_categories(["Nope"])


def test_categories_empty_rejected(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_stats")
    with pytest.raises(ChargenError, match="mind. eine Kategorie"):
        cg.step_categories([])


def test_equipment_requires_name(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_categories")
    with pytest.raises(ChargenError, match="name"):
        cg.step_equipment(items=[{"anzahl": 1}])
    with pytest.raises(ChargenError, match="negativ"):
        cg.step_equipment(items=[{"name": "s"}], purse=-1)


def test_bgos_budget_per_race(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_equipment")  # Wood Elves: bgo-Budget 4
    with pytest.raises(ChargenError, match="BGO-Budget"):
        cg.step_bgos(entries=[
            {"kind": "vorteil", "name": "Big", "cost": 3},
            {"kind": "vorteil", "name": "Bigger", "cost": 3},
        ])


def test_bgos_cost_from_candidates(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_equipment",
               **{"step_race": {"name": "Common Men"}})  # Budget 6
    out = cg.step_bgos(
        entries=[{"kind": "vorteil", "name": "Nearsight"}],
        candidates=[{"name": "Nearsight", "cost": 5}])
    assert out["spent"] == 5
    assert out["entries"][0]["cost"] == 5
    assert out["budget"] == 6


def test_bgos_disadvantage_costs_zero(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_equipment")
    out = cg.step_bgos(entries=[{"kind": "nachteil", "name": "Cursed"}])
    assert out["spent"] == 0
    assert out["entries"][0]["kind"] == "nachteil"
    assert out["entries"][0]["cost"] == 0


def test_bgos_invalid_cost_tier_rejected(spec):
    cg = make_cg(spec)
    run_prefix(cg, "step_equipment")
    with pytest.raises(ChargenError, match="cost_tiers"):
        cg.step_bgos(entries=[{"kind": "vorteil", "name": "X", "cost": 7}])


def test_finalize_requires_all_steps(spec):
    cg = make_cg(spec)
    cg.step_race("Common Men")
    with pytest.raises(ChargenStepError):
        cg.finalize(name="X")


# -------------------------------------------------------------------- run ----

VALID = {
    "race": "Wood Elves", "folk": "Silvanii", "occupation": "Magician",
    "pool": 300, "categories": [CAT],
    "items": [{"name": "staff"}], "purse": 15,
    "bgos": [
        {"kind": "nachteil", "name": "Bereits verflucht"},
        {"kind": "vorteil", "name": "Nahsicht", "cost": 1},
    ],
    "name": "Finrion",
}


def test_run_emits_character_created(spec):
    ev = make_cg(spec, seed=11).run(copy.deepcopy(VALID))
    assert isinstance(ev, Event)
    assert ev.type == "character_created"
    p = ev.payload
    assert p["name"] == "Finrion"
    assert p["race"] == "Wood Elves"
    assert p["bgos"]["spent"] == 1
    assert p["bgos"]["budget"] == 4
    assert p["equipment"]["purse"] == 15
    rows = _stats_rows(p["stats"])
    assert len(rows) == 10
    assert all(isinstance(v["temp"], int) for v in rows.values())
    spend = sum(points_needed(v["temp"]) - points_needed(max(1, min(
        100, v["base"] + v["race"]))) for v in rows.values())
    assert p["stats"]["pool_remaining"] == 300 - spend


def test_run_deterministic_with_seed(spec):
    p1 = make_cg(spec, seed=3).run(copy.deepcopy(VALID)).payload
    p2 = make_cg(spec, seed=3).run(copy.deepcopy(VALID)).payload
    assert p1 == p2
    p3 = make_cg(spec, seed=4).run(copy.deepcopy(VALID)).payload
    assert p3 != p1


def test_run_reducer_store_roundtrip(spec, tmp_path):
    ev = make_cg(spec, seed=99).run(copy.deepcopy(VALID))
    st = LocalJsonStore(str(tmp_path / "db"))
    st.append("Finrion", ev)
    log = st.read_log("Finrion")
    assert log[0].to_dict() == ev.to_dict()
    state = fold("Finrion", log)
    cc = state["character_created"]["payload"]
    assert cc["name"] == "Finrion" and cc["race"] == "Wood Elves"
    assert state["character_created"]["actor"] == "player"


def test_apply_event_rejects_unknown_type(spec):
    ev = make_cg(spec, seed=1).run(copy.deepcopy(VALID))
    bad = dataclasses.replace(ev, type="totally_bogus")
    st = empty_state("Finrion")
    with pytest.raises(UnknownEventType):
        apply_event(st, bad)
