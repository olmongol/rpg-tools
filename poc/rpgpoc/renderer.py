"""Print-Renderer: jinja2 statt ==>Key-Replace-Kette (Dok 09).

Sektionen:
- render_stats(ctx, tpl)          (bestehend, Task 8)
- render_rr_at_db(ctx, tpl)       (Task 9 — RR/AT/DB)
- render_cats(ctx, tpl)           (Task 10 — Kategorien + Skills, byte-equiv. legacy)
- build_rr_at_db_ctx(char)        (char sheet context, 1:1 legacy.createRRATDB)
- build_cats_ctx(char, short)     (char sheet context, 1:1 legacy.createCatSkill)
- _cat_skill_rows(char, short)    (interne, byte-exakte Replikation)
"""
from __future__ import annotations


def _d(value):
    """d-Filter: int(value); None oder bruchig -> Fehler (kein Still-Schwund)."""
    if value is None:
        raise ValueError("d: None (Wert fehlt)")
    n = int(value)
    if n != value:
        raise ValueError("d: nicht ganzzahlig %r" % (value,))
    return n


def render_section(ctx, template_path):
    """Gemeinsamer jinja2-Aufruf für eine Sektion. StrictUndefined, no autoescape."""
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
    from pathlib import Path
    p = Path(template_path)
    env = Environment(
        loader=FileSystemLoader(str(p.parent)),
        undefined=StrictUndefined,
        autoescape=False,
        keep_trailing_newline=True,
    )
    env.filters["d"] = _d
    good = {k: v for k, v in ctx.items() if isinstance(k, str) and k.isidentifier()}
    return env.get_template(p.name).render(ctx=ctx, **good)


# Alias für Abwärtskompatibilität mit Task 8
def render_stats(ctx, template_path):
    return render_section(ctx, template_path)


def build_context(state, template_root, system="rolemaster", definition=None):
    """Stats-Context aus State (bestehend, Task 8).

    Reihenfolge/Abkürzungen aus definition.yaml; jeder Entry braucht die
    sechs Felder (temp, pot, std, race, spec, total).
    """
    import yaml
    from pathlib import Path
    path = Path(definition) if definition else Path(template_root) / "templates" / system / "definition.yaml"
    d = yaml.safe_load(path.read_text())
    need = ("temp", "pot", "std", "race", "spec", "total")
    ctx = {}
    for s in d["stats"]:
        a = s["abbr"]
        st = state.get(a)
        if not isinstance(st, dict):
            raise ValueError("Stat fehlt: " + a)
        for f in need:
            if f not in st:
                raise ValueError("Stat %s: Feld %s fehlt" % (a, f))
        ctx[a] = {f: st[f] for f in need}
    return ctx


# -----------------------------------------------------------------------------
# Task 9: RR / AT / DB
# 1:1 Replikation von latexexport.charSheet.createRRATDB (L225-252).
# -----------------------------------------------------------------------------

def build_rr_at_db_ctx(char: dict) -> dict:
    """Context für templates/rolemaster/rr_at_db.tex.j2.

    Tokens (identisch zu legacy template_rr_at_db.tex):
    RRChan, RRC/E, RREss, RRC/M, RRMent, RRE/M, RRArc, RRDisease, RRFear, RRPoison
    + AT, missilepen, armmanmod, MMP, armquickpen (15 Tokens, int(char[v]) wenn
       vorhanden else '______')
    + ThreeQ = int(char['Qu']['total']) * 3
    + BD    = char['cat']['Body Development']['Skill']['Body Development']['total bonus']
    + PP    = char['cat']['Power Point Development']['Skill']['Power Point Development']['total bonus']
    + AdrenalDef = rank>0 ? total bonus : '______'
    """
    ctx: dict = {}
    vals = [
        "RRArc", "RRC/E", "RRChan", "RRDisease", "RRE/M",
        "RRC/M", "RREss", "RRFear", "RRMent", "RRPoison",
        "AT", "misslepen", "armmanmod", "MMP", "armquickpen",
    ]
    for v in vals:
        ctx[v] = str(int(char[v])) if v in char else "\\_\\_"
    ctx["ThreeQ"] = str(int(char["Qu"]["total"]) * 3)
    # Legacy createRRATDB (L234-241) castet die Bonuswerte explizit str(); 1:1.
    ctx["BD"] = str(char["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"])
    ctx["PP"] = str(char["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"])
    ad = char["cat"]["Special Defenses"]["Skill"]["Adrenal Defense"]
    ctx["AdrenalDef"] = str(ad["total bonus"]) if ad["rank"] > 0 else "\\_\\_"
    return ctx


def render_rr_at_db(ctx, template_path):
    return render_section(ctx, template_path)


# -----------------------------------------------------------------------------
# Task 10: Kategorien + Skills (1:1 legacy.createCatSkill, incl. Quirks)
# -----------------------------------------------------------------------------

def _fmt_seq(x):
    """str(list).replace('', '/') für Progression/Costs (legacy-Byte-Verhalten)."""
    return str(x).replace(", ", "/")


def _color_for(cat_name: str) -> str:
    """legacy.createCatSkill: Reihenfolge-Winner."""
    if "Weapon" in cat_name:
        return "\\rowcolor{Red!30} "
    elif "Development" in cat_name:
        return "\\rowcolor{Green!30} "
    elif "Spells" in cat_name:
        return "\\rowcolor{ProcessBlue!30} "
    return ""


def _cat_row(color: str, cat: str, d: dict) -> str:
    return (
        color
        + "{} & {} & {} & {} & {} & {} &{} &{} &{}&{}\\\\\n".format(
            cat,
            _fmt_seq(d["Progression"]),
            _fmt_seq(d["Costs"]),
            str(d["rank"]),
            str(d["rank bonus"]),
            str(d["stat bonus"]),
            str(d["spec bonus"]),
            str(d["prof bonus"]),
            str(d["item bonus"]),
            str(d["total bonus"]),
        )
    )


def _skill_row(color: str, name: str, d: dict) -> str:
    return (
        color
        + "\\hspace{4mm} "
        + "{} & {} & {} & {} & {} & {} &{} &-- &{}&{}\\\\\n".format(
            name,
            _fmt_seq(d["Progression"]),
            _fmt_seq(d["Costs"]),
            str(d["rank"]),
            str(d["rank bonus"]),
            "--",
            str(d["spec bonus"]),
            str(d["item bonus"]),
            str(d["total bonus"]),
        )
    )


def _skill_skip(cat_name: str, skill_name: str) -> bool:
    """1:1 legacy.createCatSkill: skill-Übersprung je Kategorie-Zweig.

    Weapon/Spells-Zweig: skill not in ['Progression','Costs']  (Costs korrekt als String)
    Development/Plain-Zweig: skill not in ['Progression',['Costs']]  (legacy-Typo: Costs als Liste
      -> niemals als String matcht; praktisch: nur 'Progression' wird übersprungen, 'Costs' NICHT).
    Alle Zweige: '+' im Skill-Namen -> Übersprung.
    Spells: zusätzlich 'Stats' übersprungen.
    """
    if "+" in skill_name:
        return True
    if skill_name == "Progression":
        return True
    if "Weapon" in cat_name and skill_name == "Costs":
        return True
    if "Spells" in cat_name and skill_name in ("Costs", "Stats"):
        return True
    return False


def _cat_branch(cat_name: str) -> str:
    if "Weapon" in cat_name:
        return "weapon"
    elif "Development" in cat_name:
        return "development"
    elif "Spells" in cat_name:
        return "spells"
    return "plain"


def _cat_skill_rows(char: dict) -> str:
    """1:1 legacy.createCatSkill, short=False. Rohe Row-Zeilen (ohne Table-Wrapper)."""
    rows: list[str] = []
    for cat in sorted(char["cat"].keys()):
        cd = char["cat"][cat]
        color = _color_for(cat)
        rows.append("\\hline\n")
        rows.append(_cat_row(color, cat, cd))
        sk = cd.get("Skill", {})
        for skill in sorted(sk):
            if _skill_skip(cat, skill):
                continue
            sd = sk[skill]
            if not isinstance(sd, dict):
                continue
            rows.append(_skill_row(color, skill, sd))
    return "".join(rows)


def build_cats_ctx(char: dict) -> dict:
    return {"rows": _cat_skill_rows(char)}


def render_cats(char: dict, template_path: str | None = None) -> str:
    """Komplettes Catskill-Sheet: Template + Rows (1:1 legacy.createCatSkill)."""
    if template_path is None:
        from pathlib import Path
        template_path = str(Path(__file__).resolve().parents[1] / "templates" / "rolemaster" / "cats.tex.j2")
    return render_section(build_cats_ctx(char), str(template_path))


# -----------------------------------------------------------------------------
# Task 11: Gen-Info (Hintergrund) + Main-Doc (1:1 legacy.createGenInfo/L128)
# -----------------------------------------------------------------------------

def build_gen_info_ctx(char: dict) -> dict:
    """Context für templates/rolemaster/gen_info.tex.j2.

    1:1 legacy.charsheet.createGenInfo (L136-206), short-unabhängig:
    - realm:      str(char['realm']).replace(', ', '/').strip('[]')
    - 28 Datenfelder: char[top-level] → str(x).strip('[]'); sonst
      char['background']; sonst recovery/pprecovery-Formel; sonst '______'.
    - soul dep → Key 'souldeparture' (Template-Token ==souldeparture), + ' rd'.
    """
    data = ["name", "prof", "race", "culture", "lord", "parents", "siblings", "partner",
            "children", "deity", "sex", "skin", "eyes", "hair", "height", "weight", "app_age",
            "act_age", "looking", "soul dep", "recovery", "pprecovery", "lvl", "piclink",
            "pers", "motiv", "exp", "home"]
    ctx: dict = {}
    ctx["realm"] = str(char["realm"]).replace(", ", "/").strip("[]")

    for index in data:
        if index in char.keys():
            if index == "soul dep":
                ctx["souldeparture"] = str(char[index]).strip("[]") + " rd"
            else:
                ctx[index] = str(char[index]).strip("[]")
        elif index in char["background"].keys():
            ctx[index] = str(char["background"][index])
        elif index == "recovery":
            rest = 1
            if round(char["Co"]["total"] / 2) > rest:
                rest = round(char["Co"]["total"] / 2)
            sleepcycle = 1
            if char["Co"]["total"] * 2 > sleepcycle:
                sleepcycle = char["Co"]["total"] * 2
            ctx["recovery"] = "1 p. 3h/{} p. 1h pause/{} p. 3h zzZZZ".format(rest, sleepcycle)
        elif index == "pprecovery":
            sleepcycle = 1
            tb = char["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"]
            if round(tb / 2) >= 1:
                sleepcycle = round(tb / 2)
            rest = 1
            if char["realm"] == "Essence" and round(char["Em"]["total"] / 2) > 1:
                rest = round(char["Em"]["total"] / 2)
            elif char["realm"] == "Channeling" and round(char["In"]["total"] / 2) > 1:
                rest = round(char["Em"]["total"] / 2)
            elif char["realm"] == "Mentalism" and round(char["Pr"]["total"] / 2) > 1:
                rest = round(char["Pr"]["total"] / 2)
            elif type(char["realm"]) == type([]):
                calc = 0
                for realm in char["realm"]:
                    if realm == "Essence":
                        calc += char["Em"]["total"]
                    elif realm == "Channeling":
                        calc += char["In"]["total"]
                    elif realm == "Mentalism":
                        calc += char["Pr"]["total"]
                calc = round(calc / 4)
                if calc > rest:
                    rest = calc
            ctx["pprecovery"] = "1 p. 3h/{} p. 1h pause/{} p. 3h zzZZZ".format(rest, sleepcycle)
        else:
            ctx[index] = "\\_\\_\\_\\_\\_"
    return ctx


def render_gen_info(char: dict, template_path: str | None = None) -> str:
    """Gen-Info-Sektion (1:1 legacy.createGenInfo)."""
    if template_path is None:
        from pathlib import Path
        template_path = str(Path(__file__).resolve().parents[1] / "templates" / "rolemaster" / "gen_info.tex.j2")
    return render_section(build_gen_info_ctx(char), str(template_path))


def render(char: dict, template_root=None, system: str = "rolemaster") -> str:
    """Hauptdokument (1:1 legacy.createMainLatex, L123-130).

    Preamble + \\input{{name_<sektion>.tex}} — Sektionen werden gemäß
    Doku 09 ("jinja2 rendert jede Sektion separat") über die
    render_<sektion>-Aufrufe als eigene Dateien erzeugt; dieses Main-Doc
    verlinkt sie nur (Legacy-Struktur bleibt erhalten).
    """
    from pathlib import Path
    root = Path(template_root) if template_root else Path(__file__).resolve().parents[1]
    tpl = root / "templates" / system / "charsheet.tex.j2"
    return render_section({"NAME": char["name"].replace(" ", "-")}, str(tpl))