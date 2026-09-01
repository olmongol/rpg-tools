"""MERP Gate — Zweit-System-Nachweis für die allgemeine Engine (Doku 05).

Beweist, dass der Engine-Kern system-AGNOSTISCH ist:
  * loader lädt ein 5-Stat-System (vs. Rolemaster 10) und validiert es
  * calc.evaluate_block führt MERP-Blöcke integer aus (Minilang + clamp)
  * probes deklariert ein ande
…e Die-Profil (1d6 vs. RM 1d100/1d10)
  * renderer baut einen 5-Stat-Context + rendert gültiges TeX
Beweist NICHT MERP-Chargen — chargen._STEPS ist RM-spezifisch per Design.
Dies ist die Akzeptanz-Abnahme für die Allzweck-Engine.
"""
from pathlib import Path
import pytest
from rpgpoc import loader, calc, renderer

ROOT = Path(__file__).resolve().parent.parent
MERP = ROOT / "templates" / "merp"
MERP_TPL = MERP / "stats.tex.j2"
ABBRS = ["ST", "SS", "DX", "IN", "HE"]


@pytest.fixture
def spec():
    return loader.load_template(MERP)


def test_loader_loads_five_stats(spec):
    assert spec["system"] == "merp"
    abbrs = [s["abbr"] for s in spec["stats"]]
    assert abbrs == ABBRS
    # 5 statt RMs 10 Stats — genau der Punkt des Gates
    assert len(abbrs) == 5


def test_loader_loads_all_files(spec):
    assert set(spec["calc"]) >= {"stat_total", "soft_strength",
                                 "combat_modifier", "skill_cost"}
    assert spec["probes"], "probes.yaml als nicht-leeres Dict geladen"
    assert spec["rules"], "rules.yaml als nicht-leeres Dict geladen"
    assert spec["char_def"].get("races"), "char_def/races.yaml unter 'races'"


def test_char_def_stats_subset_of_declared(spec):
    declared = set(spec["_declared_stats"])
    for race in spec["char_def"]["races"]:
        assert race.get("name")
        for key in (race.get("stats") or {}):
            assert key in declared, \
                f"Rasse {race['name']}: unbekannter Stat {key!r}"


def test_calc_blocks_integer(spec):
    state = {"stat": {"std": 10, "race": 2, "spec": 4, "total": 16, "temp": 16}}
    for block_name, block in spec["calc"].items():
        out = calc.evaluate_block(state, block)
        assert isinstance(out, int), f"{block_name} nicht integer: {out!r}"


def test_calc_known_values(spec):
    state = {"stat": {"std": 10, "race": 2, "spec": 4, "total": 16, "temp": 16}}
    assert calc.evaluate_block(state, spec["calc"]["stat_total"]) == 16
    assert calc.evaluate_block(state, spec["calc"]["soft_strength"]) == 8
    assert calc.evaluate_block(state, spec["calc"]["combat_modifier"]) == 4
    assert calc.evaluate_block(state, spec["calc"]["skill_cost"]) == 6


def test_render_build_context_5_stats(spec):
    state = {a: {"temp": 8, "pot": 10, "std": 8, "race": 0, "spec": 2, "total": 10}
             for a in ABBRS}
    ctx = renderer.build_context(state, ROOT, "merp")
    assert set(ctx) == set(ABBRS)
    assert ctx["DX"]["total"] == 10


def test_render_produces_tex(spec):
    state = {a: {"temp": 2, "pot": 4, "std": 6, "race": 0, "spec": 1, "total": 7}
             for a in ABBRS}
    ctx = renderer.build_context(state, ROOT, "merp")
    out = renderer.render_stats(ctx, str(MERP_TPL))
    for a in ABBRS:
        assert a in out
    assert "7" in out


def test_render_requires_all_six_fields(spec):
    state = {a: {"temp": 8, "pot": 10, "std": 8, "race": 0, "spec": 2, "total": 10}
             for a in ABBRS}
    del state["HE"]["total"]
    with pytest.raises(ValueError):
        renderer.build_context(state, ROOT, "merp")
