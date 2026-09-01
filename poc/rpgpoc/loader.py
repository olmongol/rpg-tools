"""Template loader: parse + validate a rolemaster (or future) template dir."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml


class TemplateLoadError(ValueError):
    """Raised when a template file cannot be loaded or fails validation."""


def _load_yaml(path: Path) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise TemplateLoadError(f"YAML syntax error in {path}: {exc}") from exc
    except OSError as exc:
        raise TemplateLoadError(f"cannot read {path}: {exc}") from exc


def load_template(root: str | os.PathLike) -> Dict[str, Any]:
    """Load and validate a template package rooted at ``root``.

    Expected layout (08 §1):
        root/
            definition.yaml   # engine_contract, stats, rounding, ...
            calc.yaml         # calc blocks (stat_total, category_total, ...)
            probes.yaml       # probe/dice blocks (optional)
            rules.yaml        # reactive rules (optional)

    Returns a merged dict. Validation performed:
      * definition.yaml exists and has a declared ``stats`` list.
      * Every referenced ``stats.<abbr>`` in calc.yaml exists in stats.
    """
    root = Path(root)
    if not root.is_dir():
        raise TemplateLoadError(f"template root not found: {root}")

    def_path = root / "definition.yaml"
    if not def_path.exists():
        raise TemplateLoadError(f"missing {def_path}")

    spec: Dict[str, Any] = _load_yaml(def_path)
    if not isinstance(spec, dict):
        raise TemplateLoadError("definition.yaml must be a mapping")
    if not spec.get("system"):
        raise TemplateLoadError("definition.yaml missing 'system'")

    declared_stats: set = set()
    stats_def = spec.get("stats") or []
    if isinstance(stats_def, list):
        for s in stats_def:
            if isinstance(s, dict) and s.get("abbr"):
                declared_stats.add(str(s["abbr"]))
            elif isinstance(s, str):
                declared_stats.add(s)
    spec["_declared_stats"] = sorted(declared_stats)

    calc_path = root / "calc.yaml"
    calc: Dict[str, Any] = {}
    if calc_path.exists():
        calc = _load_yaml(calc_path) or {}
    spec["calc"] = calc if isinstance(calc, dict) else {}

    probes_path = root / "probes.yaml"
    probes: Dict[str, Any] = {}
    if probes_path.exists():
        probes = _load_yaml(probes_path) or {}
    spec["probes"] = probes if isinstance(probes, dict) else {}

    rules_path = root / "rules.yaml"
    rules: Dict[str, Any] = {}
    if rules_path.exists():
        rules = _load_yaml(rules_path) or {}
    spec["rules"] = rules if isinstance(rules, dict) else {}

    # char_def (Task 4/9): Rassen-Daten für CharGen (stats-Boni, RR, BGO-Budget)
    char_def: Dict[str, Any] = {}
    cd_path = root / "char_def"
    if cd_path.is_dir():
        for fn in sorted(cd_path.iterdir()):
            if fn.suffix in (".yaml", ".yml") and fn.is_file():
                data = _load_yaml(fn) or {}
                if not isinstance(data, dict):
                    raise TemplateLoadError(
                        f"{fn} must contain a mapping")
                # top-level key = domain (races, bgo_catalog, items, …)
                for domain, body in data.items():
                    if domain in char_def:
                        raise TemplateLoadError(
                            f"char_def domain {domain!r} mehrfach definiert")
                    char_def[domain] = body
    spec["char_def"] = char_def

    _validate_calc_refs(spec)
    _validate_char_def(spec)
    return spec


def _validate_calc_refs(spec: Dict[str, Any]) -> None:
    """Ensure every ``stats.<abbr>.<field>`` used in calc resolves to a stat."""
    import re
    calc = spec.get("calc") or {}
    declared = set(spec.get("_declared_stats") or [])
    pattern = re.compile(r"stats\.([A-Za-z_][A-Za-z0-9_]*)")
    for block_name, block in calc.items():
        if not isinstance(block, dict):
            continue
        terms = block.get("pipeline") or block.get("terms") or []
        for term in terms:
            if not isinstance(term, dict):
                continue
            for key in ("expr", "term", "condition"):
                val = term.get(key)
                if not isinstance(val, str):
                    continue
                for abbr in pattern.findall(val):
                    if declared and abbr not in declared:
                        raise TemplateLoadError(
                            f"calc block {block_name!r} references unknown "
                            f"stat {abbr!r} (declared: {sorted(declared)})"
                        )


def _validate_char_def(spec: Dict[str, Any]) -> None:
    """Rassen-Daten müssen zu den deklarierten Stats passen (Task 4)."""
    declared = set(spec.get("_declared_stats") or [])
    races = (spec.get("char_def") or {}).get("races") or []
    if isinstance(races, dict):
        races = list(races.values())
    for race in races:
        if not isinstance(race, dict) or not race.get("name"):
            raise TemplateLoadError(
                f"char_def.races-Eintrag ohne 'name': {race!r}")
        name = race["name"]
        for domain in ("stats", "rr"):
            for key in (race.get(domain) or {}):
                if domain == "stats" and declared and \
                        str(key) not in declared:
                    raise TemplateLoadError(
                        f"Rasse {name!r}: stat {key!r} nicht in definition.stats")
        budget = race.get("bgo")
        if budget is not None and not isinstance(budget, int):
            raise TemplateLoadError(
                f"Rasse {name!r}: bgo-Budget muss int sein, ist {budget!r}")
