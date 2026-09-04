r'''
\file renderer.py
\brief Print-Renderer: jinja2 statt ==>Key-Replace-Kette (Dok 09).

Rendert die RoLe-Sheet-Sektionen aus Jinja2-Templates
(``templates/rolemaster/*.tex.j2``), 1:1 repliziert die legacy
``latexexport``-CharSheet-Methoden:

- ``render_stats``          (Task 8 — Stats)
- ``render_rr_at_db``       (Task 9 — RR/AT/DB, 1:1 ``createRRATDB``)
- ``render_cats``           (Task 10 — Kategorien + Skills, 1:1 ``createCatSkill``)
- ``render_gen_info``       (Task 11 — Hintergrund, 1:1 ``createGenInfo``)
- ``render``                (Main-Doc, 1:1 ``createMainLatex``)
'''
from __future__ import annotations


def _d(value):
    """d-Filter: int(value); None oder bruchig -> Fehler (kein Still-Schwund).

    @param value Zahl aus dem Charakter-State
    @return int, unverändert (nur Typ-/Integritäts-Check)
    """
    if value is None:
        raise ValueError("d: None (Wert fehlt)")
    n = int(value)
    if n != value:
        raise ValueError("d: nicht ganzzahlig %r" % (value,))
    return n


def render_section(ctx, template_path):
    """Gemeinsamer jinja2-Aufruf für eine Sektion. StrictUndefined, no autoescape.

    @param ctx dict mit den Template-Variablen (String-Keys)
    @param template_path absolute Pfad zum .tex.j2-Template
    @return gerendert Text (str)
    """
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
    """Rendert stats.tex.j2 (Task 8, 1:1 legacy.createStats).

    @param ctx dict {Abkürzung: {temp, pot, std, race, spec, total}}
    @param template_path absolute Pfad zum template
    @return gerendert Text (str)
    """
    return render_section(ctx, template_path)


def build_context(state, template_root, system="rolemaster", definition=None):
    """Stats-Context aus State (bestehend, Task 8).

    Reihenfolge/Abkürzungen aus definition.yaml; jeder Entry braucht die
    sechs Felder (temp, pot, std, race, spec, total).

    @param state Charakter-State aus dem Reducer
    @param template_root root für ``templates/<system>/``
    @param system Systemname (default: "rolemaster")
    @param definition optional: direkter Pfad auf definition.yaml
    @return ctx dict für render_stats
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

    1:1 Replikation von ``latexexport.charSheet.createRRATDB`` (L225-252).
    MMP = **Movement Maneuver Penalty** (``char["MMP"]``) — NICHT
    ``shop_logic.calc_mmp`` (Max. Market Power, Preisleiste).

    Tokens (identisch zu legacy template_rr_at_db.tex):
    RRChan, RRC/E, RREss, RRC/M, RRMent, RRE/M, RRArc, RRDisease, RRFear, RRPoison
    + AT, missilepen, armmanmod, MMP, armquickpen (15 Tokens, int(char[v]) wenn
       vorhanden else '______')
    + ThreeQ = int(char['Qu']['total']) * 3
    + BD    = char['cat']['Body Development']['Skill']['Body Development']['total bonus']
    + PP    = char['cat']['Power Point Development']['Skill']['Power Point Development']['total bonus']
    + AdrenalDef = rank>0 ? total bonus : '______'

    @param char Charakter-State (legacy-JSON-Struktur)
    @return ctx dict mit den Template-Variablen (als Strings)
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
    """Rendert rr_at_db.tex.j2 (Task 9, 1:1 legacy.createRRATDB-Byte).

    @param ctx aus build_rr_at_db_ctx
    @param template_path absolute Pfad zum template
    @return gerendert Text (str)
    """
    return render_section(ctx, template_path)


# -----------------------------------------------------------------------------
# Task 10: Kategorien + Skills (1:1 legacy.createCatSkill, incl. Quirks)
# -----------------------------------------------------------------------------

def _fmt_seq(x):
    """str(list).replace(', ', '/') für Progression/Costs (legacy-Byte-Verhalten).

    @param x Liste von Zahlen (Progression/Costs-Skilling-Entry)
    @return String mit '/'-Trennung (identisch zu legacy-L197)
    """
    return str(x).replace(", ", "/")


def _color_for(cat_name: str) -> str:
    """Zeilen-Farbe einer Kategorie, legacy createCatSkill-Reihenfolge-Winner-Regel.

    @param cat_name Kategorien-Name (String)
    @return ``\\rowcolor{...} ``-Präfix (leer wenn keine Regel matcht)
    @return ``\rowcolor{...} ``-Präfix (leer wenn keine Regel matcht)
    """
    if "Weapon" in cat_name:
        return "\\rowcolor{Red!30} "
    elif "Development" in cat_name:
        return "\\rowcolor{Green!30} "
    elif "Spells" in cat_name:
        return "\\rowcolor{ProcessBlue!30} "
    return ""


def _cat_row(color: str, cat: str, d: dict) -> str:
    """Single Kategorie-Zeile (inkl. 8 Bonus-Spalten + 10 &), 1:1 legacy-Row.

    @param color Zeilen-Farben-Präfix (aus _color_for)
    @param cat Kategorien-Name
    @param d Kategorien-Dict (Progression/Costs/rank/.../total bonus)
    @return eine TeX-Zeile inkl. Zeilenende
    """
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
    """Einzelne Skill-Zeile unter der Kategorie (7 Spalten, -- für Stat-Bonus).

    @param color Zeilen-Farben-Präfix
    @param name Skill-Name
    @param d Skill-Dict (Progression/Costs/rank/.../total bonus)
    @return eine TeX-Zeile inkl. Zeilenende
    """
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

    @param cat_name Kategorien-Name (bestimmt den Zweig)
    @param skill_name Skill-Name
    @return True, wenn der Skill in diesem Zweig nicht als eigene Zeile erscheint
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
    """Branch-Label für Templates (legacy-if-Else-Kette, 1:1 createCatSkill).

    @param cat_name Kategorien-Name
    @return ``weapon`` | ``development`` | ``spells`` | ``plain``
    """
    if "Weapon" in cat_name:
        return "weapon"
    elif "Development" in cat_name:
        return "development"
    elif "Spells" in cat_name:
        return "spells"
    return "plain"


def _cat_skill_rows(char: dict) -> str:
    """1:1 legacy.createCatSkill, short=False. Rohe Row-Zeilen (ohne Table-Wrapper).

    @param char Charakter-State (legacy-JSON-Struktur)
    @return concatenated Row-Zeilen-Block (str)
    """
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
    """Context für templates/rolemaster/cats.tex.j2 (Template erwartet das eine
    Schlüsselwort 'rows'; sonst StrictUndefined-Fehler).

    @param char Charakter-State (legacy-JSON-Struktur)
    @return dict {"rows": <concatenierter Row-Block>}
    """
    return {"rows": _cat_skill_rows(char)}


def render_cats(char: dict, template_path: str | None = None) -> str:
    """Komplettes Catskill-Sheet: Template + Rows (1:1 legacy.createCatSkill).

    @param char Charakter-State (legacy-JSON-Struktur)
    @param template_path optional Pfad; default: templates/rolemaster/cats.tex.j2
    @return gerendert Text (str)
    """
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

    @param char Charakter-State (legacy-JSON-Struktur)
    @return ctx dict mit den Template-Variablen (Strings)
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
    """Gen-Info-Sektion (1:1 legacy.createGenInfo).

    @param char Charakter-State (legacy-JSON-Struktur)
    @param template_path optional Pfad; default: templates/rolemaster/gen_info.tex.j2
    @return gerendert Text (str)
    """
    if template_path is None:
        from pathlib import Path
        template_path = str(Path(__file__).resolve().parents[1] / "templates" / "rolemaster" / "gen_info.tex.j2")
    return render_section(build_gen_info_ctx(char), str(template_path))


def render(char: dict, template_root=None, system: str = "rolemaster") -> str:
    """Hauptdokument (1:1 legacy.createMainLatex, L123-130).

    Preamble + \\input{name_<sektion>.tex} — Sektionen werden gemäß
    Doku 09 ("jinja2 rendert jede Sektion separat") über die
    render_<sektion>-Aufrufe als eigene Dateien erzeugt; dieses Main-Doc
    verlinkt sie nur (Legacy-Struktur bleibt erhalten).

    @param char Charakter-State (legacy-JSON-Struktur)
    @param template_root optional Root; default: <poc-Verzeichnis>
    @param system Systemname (default: "rolemaster")
    @return gerendertes Main-Doc (str)
    """
    from pathlib import Path
    root = Path(template_root) if template_root else Path(__file__).resolve().parents[1]
    tpl = root / "templates" / system / "charsheet.tex.j2"
    return render_section({"NAME": char["name"].replace(" ", "-")}, str(tpl))