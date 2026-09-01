"""Print-Renderer: jinja2 Stats-Sektion statt ==>Key-Replace-Kette (Dok 09)."""
from __future__ import annotations
from pathlib import Path


def _d(value):
    """d-Filter: int(value); None oder bruchig -> Fehler (kein Still-Schwund)."""
    if value is None:
        raise ValueError("d: None (Wert fehlt)")
    n = int(value)
    if n != value:
        raise ValueError("d: nicht ganzzahlig %r" % (value,))
    return n


def render_stats(ctx, template_path):
    """Rendert stats.tex.j2 -> Text. ctx = {Abkuerzung: {temp,pot,std,race,
    spec,total}} (exakt wie Finrion.json stats). StrictUndefined + d-Filter."""
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
    p = Path(template_path)
    env = Environment(loader=FileSystemLoader(str(p.parent)),
                      undefined=StrictUndefined, autoescape=False,
                      keep_trailing_newline=True)
    env.filters["d"] = _d
    return env.get_template(p.name).render(**ctx)


def build_context(state, template_root, system="rolemaster", definition=None):
    """Context aus State + Stat-Validierung gegen definition.yaml.

    Reihenfolge/Abkuerzungen kommen aus der Template-Definition; jeder
    Entry braucht die sechs Felder (Dok 09: fehlend = Fehler).
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
