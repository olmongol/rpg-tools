"""GUI: Stats-Form (05: "QFormLayout für Stats").

Logik = reine Funktionen ``stats_order(definition)`` und
``stat_value(state, abbr)`` (testbar ohne Qt). Die Qt-Widgets in
``build_stats_form(parent, definition, client)`` sind die Anzeige:
ein Read-only QFormLayout mit einer Zeile pro Stat (Abkürzung, Temp,
Potential, Standard, Bonus), befüllt aus ``client.sheet()``.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from PyQt6.QtWidgets import (
    QFormLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


def stats_order(definition: Dict[str, Any]) -> List[str]:
    """Stat-Abkürzungen in Template-Definition-Reihenfolge.

    Erwartet definition['stats'] = [{abbr, ...}, ...]; leerer Fall = [].
    """
    out: List[str] = []
    for s in (definition.get("stats") or []):
        if isinstance(s, dict) and s.get("abbr"):
            out.append(str(s["abbr"]))
    return out


def stat_display(state: Dict[str, Any], abbr: str) -> Optional[str]:
    """Kurz-Zeile für ein Stat aus dem (chargen) State.

    state[abbr] = {base, race, temp, bonus, cost} (chargen.step_stats)
    -> "Temp 59 (+9)  [Base 50, Race +2, Bonus +9, Cost 120]".
    Fehlend -> None (Anzeige zeigt dann das Feld leer).
    """
    st = state.get(abbr)
    if not isinstance(st, dict):
        return None
    try:
        return (
            f"Temp {st.get('temp')} (+{st.get('bonus')})"
            f"  [Base {st.get('base')}, Race {st.get('race')},"
            f" Cost {st.get('cost')}]"
        )
    except (TypeError, ValueError):
        return None


def stat_values(state: Dict[str, Any], abbr: str) -> Dict[str, Optional[int]]:
    """Zerlegt ein Stats-Stat in die einzelnen ganzzahligen Felder."""
    st = state.get(abbr)
    if not isinstance(st, dict):
        return {}
    out: Dict[str, Optional[int]] = {}
    for k in ("base", "race", "temp", "bonus", "cost"):
        v = st.get(k)
        out[k] = int(v) if v is not None else None
    return out


def build_stats_form(parent: QWidget, definition: Dict[str, Any],
                     state: Optional[Dict[str, Any]] = None) -> QFormLayout:
    """Erzeugt ein QFormLayout mit einer QLabel-Zeile pro Stat.

    ``state=None`` -> leere Felder; sonst befüllt aus ``stat_display``.
    """
    form = QFormLayout(parent)
    form.setContentsMargins(0, 0, 0, 0)
    abbrs = stats_order(definition)
    if state is None:
        state = {}
    for abbr in abbrs:
        text = stat_display(state, abbr) or ("—" * 8)
        form.addRow(abbr, QLabel(text, parent=parent))
    return form
