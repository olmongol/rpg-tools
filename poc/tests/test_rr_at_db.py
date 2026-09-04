"""t5: rr_at_db — Generisch, Byte-Äquivalenz, Edge-cases."""
import copy
import json
import pathlib

from rpgpoc import renderer as R

REPO = pathlib.Path(__file__).resolve().parents[2]
FINRION = json.loads((REPO / "src/data/Marcus/Finrion.json").read_text())
GT_RR = (pathlib.Path(__file__).parent / "fixtures/Finrion_rr_at_db.tex").read_text()
TPL = str(REPO / "poc/templates/rolemaster/rr_at_db.tex.j2")

EXPECTED_KEYS = {
    "RRArc", "RRC/E", "RRChan", "RRDisease", "RRE/M", "RRC/M", "RREss", "RRFear",
    "RRMent", "RRPoison", "AT", "misslepen", "armmanmod", "MMP", "armquickpen",
    "ThreeQ", "BD", "PP", "AdrenalDef",
}
PH = "\\_\\_"  # RR-Platzhalter (2× LaTeX-escaped Underscore)


def test_equivalence():
    ctx = R.build_rr_at_db_ctx(FINRION)
    assert R.render_rr_at_db(ctx, TPL) == GT_RR


def test_context_generic_shape():
    ctx = R.build_rr_at_db_ctx(FINRION)
    assert set(ctx) == EXPECTED_KEYS
    for k in EXPECTED_KEYS:
        assert isinstance(ctx[k], str), k
    # ThreeQ = Qu.total * 3 (ganzzahlig)
    assert ctx["ThreeQ"] == str(int(FINRION["Qu"]["total"]) * 3)


def test_deterministic():
    ctx = R.build_rr_at_db_ctx(FINRION)
    a = R.render_rr_at_db(ctx, TPL)
    b = R.render_rr_at_db(R.build_rr_at_db_ctx(copy.deepcopy(FINRION)), TPL)
    assert a == b


def test_missing_token_placeholder():
    ch = copy.deepcopy(FINRION)
    for k in ["AT", "MMP", "RRFear"]:
        ch.pop(k, None)
    out = R.render_rr_at_db(R.build_rr_at_db_ctx(ch), TPL)
    assert out.count(PH) >= 3
    assert R.build_rr_at_db_ctx(ch)["AT"] == PH


def test_adrenal_def_rank_zero_placeholder():
    ch = copy.deepcopy(FINRION)
    ad = ch["cat"]["Special Defenses"]["Skill"]["Adrenal Defense"]
    old = ad["rank"]
    ad["rank"] = 0
    try:
        assert R.build_rr_at_db_ctx(ch)["AdrenalDef"] == PH
    finally:
        ad["rank"] = old


def test_int_cast_float():
    ch = copy.deepcopy(FINRION)
    ch["AT"] = 15.0  # float kommt aus JSON; Legacy castet int()
    assert R.build_rr_at_db_ctx(ch)["AT"] == "15"
