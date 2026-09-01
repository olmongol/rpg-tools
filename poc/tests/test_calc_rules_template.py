"""Tests for the calc pillar, the RR probes, and the RM rules (Task 6/7).

Verifies, against the ACTUAL on-disk code and the ACTUAL RoleMaster template:
  * calc.expr mini-language: + - * / literals, dotted refs, clamp, null policy
  * calc block evaluate_block: rounding (floor/round/ceil) + clamp, int out
  * the RM template loads (loader validates all four files)
  * RM calc blocks: stat_total / cat_total / skill_total produce correct ints
    (stat_total grounded on legacy Finrion St = std 10 + race 2 + spec 8 = 20)
  * rules: rr_check fires rr_resisted/rr_failed; pause_bleed_on_heal fires
    ONLY on healed_while_bleeding; disease_cured/poison_cured are inert for
    unrelated event types.
"""
from __future__ import annotations
import pytest

from rpgpoc import calc, rules, probes as probes_mod, loader
from rpgpoc.events import Event

ROOT = "templates/rolemaster"


# ---------------------------------------------------------------------------
# calc.expr mini-language
# ---------------------------------------------------------------------------
def test_eval_expr_additive() -> None:
    assert calc.eval_expr("1 + 2 * 3", {}) == 7


def test_eval_expr_division() -> None:
    assert calc.eval_expr("10 / 4", {}) == 2.5


def test_eval_expr_dotted_ref() -> None:
    assert calc.eval_expr("stat.std + stat.race", {"stat": {"std": 10, "race": 2}}) == 12


def test_eval_expr_missing_ref_is_zero() -> None:
    assert calc.eval_expr("missing.path + 5", {}) == 5


def test_eval_expr_clamp_three_arg() -> None:
    assert calc.eval_expr("clamp(0, -5, 100)", {}) == 0
    assert calc.eval_expr("clamp(0, 50, 100)", {}) == 50
    assert calc.eval_expr("clamp(0, 200, 100)", {}) == 100


def test_eval_expr_unary_neg() -> None:
    assert calc.eval_expr("-3 + 5", {}) == 2


def test_eval_expr_rejects_unknown_call() -> None:
    with pytest.raises((calc.CalcSyntaxError, calc.CalcError)):
        calc.eval_expr("len(x)", {"x": [1, 2]})


def test_eval_expr_rejects_string_concat() -> None:
    # The AST whitelist has no string operators; "a" + "b" should fail.
    with pytest.raises((calc.CalcSyntaxError, calc.CalcError)):
        calc.eval_expr('"a" + "b"', {})


# ---------------------------------------------------------------------------
# calc block (rounding/clamp/int out)
# ---------------------------------------------------------------------------
def test_block_floor_rounding() -> None:
    block = {"pipeline": [{"expr": "10 / 3"}], "rounding": "floor"}
    assert calc.evaluate_block({}, block) == 3  # 3.33 -> 3


def test_block_ceil_rounding() -> None:
    block = {"pipeline": [{"expr": "10 / 3"}], "rounding": "ceil"}
    assert calc.evaluate_block({}, block) == 4


def test_block_round_half_away_from_zero() -> None:
    block = {"pipeline": [{"expr": "1.5"}], "rounding": "round"}
    assert calc.evaluate_block({}, block) == 2
    block_neg = {"pipeline": [{"expr": "-1.5"}], "rounding": "round"}
    assert calc.evaluate_block({}, block_neg) == -2  # NOT banker's


def test_block_clamp() -> None:
    block = {"pipeline": [{"expr": "200"}], "rounding": "floor", "clamp": [0, 100]}
    assert calc.evaluate_block({}, block) == 100


def test_block_requires_pipeline() -> None:
    with pytest.raises((calc.CalcError, ValueError)):
        calc.evaluate_block({}, {})


# ---------------------------------------------------------------------------
# RoleMaster template (loader + calc grounded on legacy)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def tmpl() -> dict:
    return loader.load_template(ROOT)


def test_template_declares_three_calc_blocks(tmpl: dict) -> None:
    assert set(tmpl["calc"].keys()) == {"stat_total", "cat_total", "skill_total"}


def test_template_stat_total_grounded_on_finrion_st(tmpl: dict) -> None:
    # Legacy src/data/Marcus/Finrion.json: St = {std:10, race:2, spec:8, total:20}
    ctx = {"stat": {"std": 10, "race": 2, "spec": 8}}
    assert calc.evaluate_block(ctx, tmpl["calc"]["stat_total"]) == 20


def test_template_cat_total(tmpl: dict) -> None:
    ctx = {"cat": {"stat_bonus": 3, "rank_bonus": 5, "spec": 1, "item": 2}}
    assert calc.evaluate_block(ctx, tmpl["calc"]["cat_total"]) == 11


def test_template_skill_total(tmpl: dict) -> None:
    ctx = {"skill": {"cat_total": 11, "rank_bonus": 3,
                     "item_bonus": 1, "spec_bonus": 0}}
    assert calc.evaluate_block(ctx, tmpl["calc"]["skill_total"]) == 15


def test_template_probes_declare_rr_d100(tmpl: dict) -> None:
    pb = probes_mod.make_probes_block(tmpl["probes"], {})
    assert pb["rr"]["die"] == 100
    assert pb["rr"]["modifier"] == 0


def test_template_rules_declared(tmpl: dict) -> None:
    expected = {
        "pause_bleed_on_heal",
        "rr_resisted", "rr_failed",
        "disease_stage_up", "disease_cured",
        "poison_stage_up", "poison_cured",
        "level_up_cost_checked",
    }
    assert expected.issubset(set(tmpl["rules"].keys()))


# ---------------------------------------------------------------------------
# rules: firing / inert semantics
# ---------------------------------------------------------------------------
def _ev(seq: int = 0, type_: str = "x", **payload) -> Event:
    return Event(seq=seq, char="c", type=type_, actor="gm", payload=payload)


def _fire(tmpl: dict, ev: Event, state: dict | None = None) -> list[dict]:
    return rules.evaluate_rules(tmpl["rules"], [ev], state or {"char": "c"})


def test_rr_resisted_fires_when_resisted(tmpl: dict) -> None:
    out = _fire(tmpl, _ev(type_="rr_check", **{"resisted": 1, "roll": 92, "target": 90}))
    assert any(f.get("rule") == "rr_resisted" for f in out)


def test_rr_failed_fires_when_not_resisted(tmpl: dict) -> None:
    out = _fire(tmpl, _ev(type_="rr_check", **{"resisted": 0, "roll": 12, "target": 90}))
    assert any(f.get("rule") == "rr_failed" for f in out)


def test_rr_rules_do_not_fire_on_unrelated_events(tmpl: dict) -> None:
    # an unrelated event fires neither rr rule
    out = _fire(tmpl, _ev(type_="item_added"))
    assert not any(f.get("rule") in {"rr_resisted", "rr_failed"} for f in out)


def test_pause_bleed_on_heal_fires_only_on_healed_while_bleeding(
        tmpl: dict) -> None:
    assert any(f.get("rule") == "pause_bleed_on_heal"
               for f in _fire(tmpl, _ev(type_="healed_while_bleeding")))
    # and it must NOT fire on unrelated events
    out = _fire(tmpl, _ev(type_="rr_check", **{"resisted": 1}))
    assert not any(f.get("rule") == "pause_bleed_on_heal" for f in out)


def test_disease_cured_fires_only_on_disease_cured_event(tmpl: dict) -> None:
    assert any(f.get("rule") == "disease_cured"
               for f in _fire(tmpl, _ev(type_="disease_cured")))
    out = _fire(tmpl, _ev(type_="rr_check", **{"resisted": 1}))
    assert not any(f.get("rule") == "disease_cured" for f in out)


def test_poison_rules_are_event_type_scoped(tmpl: dict) -> None:
    assert any(f.get("rule") == "poison_cured"
               for f in _fire(tmpl, _ev(type_="poison_cured")))
    assert any(f.get("rule") == "poison_stage_up"
               for f in _fire(tmpl, _ev(type_="poison_rr_failed",
                                     **{"stage_advanced": 1})))
    # stage_up is INERT when stage_advanced != 1 (when-clause is a real filter)
    out = _fire(tmpl, _ev(type_="poison_rr_failed", **{"stage_advanced": 0}))
    assert not any(f.get("rule") == "poison_stage_up" for f in out)
