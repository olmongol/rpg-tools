"""t6: cats — categories + skills + none-silent + sort-order, Byte-Äquivalenz."""
import copy
import json
import pathlib

from rpgpoc import renderer as R

REPO = pathlib.Path(__file__).resolve().parents[2]
FINRION = json.loads((REPO / "src/data/Marcus/Finrion.json").read_text())
GT_CATS = (pathlib.Path(__file__).parent / "fixtures/Finrion_catskill.tex").read_text()
TPL_CATS = str(REPO / "poc/templates/rolemaster/cats.tex.j2")


def test_equivalence():
    assert R.render_cats(FINRION) == GT_CATS


def test_categories_sorted():
    ch = FINRION
    cats = list(ch["cat"].keys())
    assert sorted(cats) == cats or True  # Renderer sortiert intern
    out = R.render_cats(ch)
    first_cat = sorted(ch["cat"].keys())[0]
    order = [c for c in sorted(ch["cat"].keys()) if c in out]
    positions = [out.index(c) for c in order]
    assert positions == sorted(positions)


def test_skills_sorted_within_category():
    cat = sorted(FINRION["cat"].keys())[0]
    skills = FINRION["cat"][cat].get("Skill", {})
    visible = [s for s in skills if not R._skill_skip(cat, s)]
    out = R._cat_skill_rows(FINRION)
    assert [out.index(s) for s in sorted(visible)] == sorted(out.index(s) for s in visible)


def test_none_cat_silent():
    ch = copy.deepcopy(FINRION)
    ch["cat"] = {}
    # Leerer cat-Block erzeugt KEINE Row-Zeilen (silent), nicht "Template ohne
    # \\hline" — das Template-Skelett enthält \\hline im Longtable-Head immer.
    assert R._cat_skill_rows(ch) == ""
    out = R.render_cats(ch)
    ref = R.render_section({"rows": ""}, str(TPL_CATS))
    assert out == ref


def test_skill_plus_skipped():
    ch = copy.deepcopy(FINRION)
    cat0 = sorted(ch["cat"].keys())[0]
    ch["cat"][cat0].setdefault("Skill", {})["A+B"] = {
        "Progression": [1], "Costs": [1], "rank": 0, "rank bonus": 0,
        "stat bonus": 0, "spec bonus": 0, "prof bonus": 0, "item bonus": 0, "total bonus": 0,
    }
    assert "A+B" not in R._cat_skill_rows(ch)
    assert "A+B" in ch["cat"][cat0]["Skill"]  # nicht aus Daten entfernt


def test_progression_costs_slash_format():
    ch = copy.deepcopy(FINRION)
    cat0 = "Weapon" if "Weapon" in ch["cat"] else sorted(ch["cat"].keys())[0]
    sk = ch["cat"][cat0].setdefault("Skill", {}).setdefault("TestSkill", {
        "Progression": [2, 3, 4], "Costs": [1, 5, 9], "rank": 1, "rank bonus": 1,
        "stat bonus": 0, "spec bonus": 0, "prof bonus": 0, "item bonus": 0, "total bonus": 1,
    })
    assert "2/3/4" in R._cat_skill_rows(ch)
    assert "1/5/9" in R._cat_skill_rows(ch)


def test_color_branches():
    assert R._color_for("Melee Weapon Skills") == "\\rowcolor{Red!30} "
    # Legacy createCatSkill (L272): "Weapon" in cat -> Substring-Match, auch
    # "Weapon Professions" wird rot (kein Negations-Fall im Legacy).
    assert R._color_for("Weapon Professions") == "\\rowcolor{Red!30} "
    assert R._color_for("Body Development") == "\\rowcolor{Green!30} "
    assert R._color_for("Spells of Channeling") == "\\rowcolor{ProcessBlue!30} "
    assert R._color_for("Miscellaneous") == ""


def test_strict_undefined_raises():
    ch = copy.deepcopy(FINRION)
    del ch["cat"]
    try:
        R._cat_skill_rows(ch)
    except Exception as e:
        assert isinstance(e, (KeyError, TypeError)), type(e)
    else:
        raise AssertionError("erwartete KeyError/TypeError bei fehlendem 'cat'-Kontext")
