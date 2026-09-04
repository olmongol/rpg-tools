"""t7: charsheet (main-doc) — Byte-Äquivalenz + pdflatex-kompilierbar (offscreen)."""
import json
import os
import pathlib
import shutil
import subprocess

import pytest
from rpgpoc import renderer as R

REPO = pathlib.Path(__file__).resolve().parents[2]
FINRION = json.loads((REPO / "src/data/Marcus/Finrion.json").read_text())
GT_MAIN = (pathlib.Path(__file__).parent / "fixtures/Finrion_main.tex").read_text()

HERE = pathlib.Path(__file__).parent
FIX = HERE / "fixtures"


def test_byte_equivalence():
    assert R.render(FINRION) == GT_MAIN


def test_input_names_use_dashed_charname():
    out = R.render(FINRION)
    assert "\\input{Finrion_gen_info.tex}" in out
    assert "\\input{Finrion_stats.tex}" in out
    assert "\\input{Finrion_rr_at_db.tex}" in out
    assert "\\input{Finrion_catskill.tex}" in out


def test_name_with_space_dashed():
    ch = dict(FINRION, name="Iron Hills")
    assert "\\input{Iron-Hills_gen_info.tex}" in R.render(ch)


def test_preamble_present():
    out = R.render(FINRION)
    assert "\\documentclass" in out
    assert "\\begin{document}" in out
    assert "\\end{document}" in out
    # "Maroon" kommt NICHT aus der Preamble, sondern aus xcolor[dvipsnames]
    # (Legacy createMainLatex ersetzt nur "name_" — kein Color-Definition im Template).
    assert "xcolor" in out


def test_pdflatex_compiles_offscreen(tmp_path):
    pdflatex = shutil.which("pdflatex")
    if pdflatex is None:
        pytest.skip("pdflatex fehlt")
    outdir = tmp_path / "latex"
    outdir.mkdir()
    name = FINRION["name"].replace(" ", "-")
    files = {
        f"{name}.tex": GT_MAIN,
        f"{name}_stats.tex": (FIX / "Finrion_stats.tex").read_text(),
        f"{name}_rr_at_db.tex": (FIX / "Finrion_rr_at_db.tex").read_text(),
        f"{name}_catskill.tex": (FIX / "Finrion_catskill.tex").read_text(),
        f"{name}_gen_info.tex": (FIX / "Finrion_gen_info.tex").read_text(),
    }
    for fn, body in files.items():
        (outdir / fn).write_text(body, encoding="utf-8")
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", TEXINPUTS=str(outdir) + os.pathsep)
    p = subprocess.run(
        [pdflatex, "-interaction=nonstopmode", "-halt-on-error", f"{name}.tex"],
        cwd=str(outdir), env=env, capture_output=True, text=True, timeout=300,
    )
    pdf = outdir / f"{name}.pdf"
    logerr = False
    log = (outdir / f"{name}.log").read_text(errors="replace") if (outdir / f"{name}.log").exists() else ""
    logerr = ("! " in log)
    assert p.returncode == 0, p.stdout[-2000:] + p.stderr[-2000:]
    assert not logerr
    assert pdf.exists() and pdf.stat().st_size > 1000
