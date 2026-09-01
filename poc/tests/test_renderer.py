"""Task 8: build_context + jinja2 Stats-Rendering == Finrion-Fixture."""
import json
from pathlib import Path
import pytest
from rpgpoc import renderer as R

# conftest sits in tests/; this test sits next to it -> two up == poc/ base
POC = Path(__file__).resolve().parent.parent
FIN = Path("/home/mongol/git/rpg-tools/src/data/Marcus/Finrion.json")
FIX = POC / "tests" / "fixtures" / "Finrion_stats.tex"
TPL = POC / "templates" / "rolemaster" / "stats.tex.j2"


def test_render_matches_fixture() -> None:
    state = json.loads(FIN.read_text(encoding="utf-8"))
    ctx = R.build_context(state, POC, "rolemaster")
    out = R.render_stats(ctx, str(TPL))
    expected = FIX.read_text(encoding="utf-8")
    assert out == expected


def test_build_context_requires_all_fields() -> None:
    good = json.loads(FIN.read_text(encoding="utf-8"))
    ab = {k: v for k, v in good.items() if isinstance(v, dict)}
    bad = {k: dict(v) for k, v in ab.items()}
    bad["St"].pop("total")
    with pytest.raises(ValueError):
        R.build_context(bad, POC, "rolemaster")


def test_d_filter_rejects_fractions() -> None:
    with pytest.raises(ValueError):
        R._d(2.5)


def test_d_filter_passes_ints() -> None:
    assert R._d(7) == 7


# --- f3/f4: Replikations-Diff gegen legacy latexexport.py (Kriterium 7) ---
# Legacy: src/rpgtoolbox/latexexport.py createStats() (Zeilen 211-223):
# template_stats.tex +  ==>STAT_val  ->  str(char[stat][val])-Ersetzung.
# Der Legacy-Module-Import ist von gui/confbox/config gekoppelt und läuft
# nicht isoliert; die 4 Zeilen Ersetzungs-Logik werden daher 1:1 repliziert
# und gegen den PoC-Renderer (jinja2) für den GLEICHEN Charakter verglichen.
LEGACY_TPL = Path("/home/mongol/git/rpg-tools/src/data/default/latex/template_stats.tex")
LEGACY_STATS = ["Ag", "Co", "Me", "Re", "SD", "Em", "In", "Pr", "Qu", "St"]
LEGACY_FIELDS = ["pot", "race", "spec", "std", "temp", "total"]


def _legacy_create_stats(char: dict) -> str:
    """1:1-Kopie von latexexport.charSheet.createStats() (L215-220)."""
    template = LEGACY_TPL.read_text(encoding="utf-8")
    for s in LEGACY_STATS:
        for v in LEGACY_FIELDS:
            template = template.replace("==>{}_{}".format(s, v), str(char[s][v]))
    return template


def test_equivalence_with_legacy_latexexport() -> None:
    """Kriterium 7: PoC-Renderer == latexexport.py createStats() (identisch).

    Gleicher Charakter (Finrion.json), gleicher Ausgangstext: byte-identisch.
    Strenger als das Kriterium selbst ("bis auf Whitespace").
    """
    char = json.loads(FIN.read_text(encoding="utf-8"))
    legacy = _legacy_create_stats(char)
    ctx = R.build_context(char, POC, "rolemaster")
    poc = R.render_stats(ctx, str(TPL))
    assert legacy == poc



