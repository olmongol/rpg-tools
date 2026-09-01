"""GUI: Pro-Schritt-Step-Widgets fur den 8-Schritt-CharGen-Wizard.

Design: jeder Schritt ist eine eigene QWidget-Subklasse, die ihre
Eingabe-Widgets als Attribute halt (``self.combo``, ``self.spin``,
``self.edit``, ``self.list`` ...) und ``value``/``set_value`` implementiert.
``make_step_page(key, definition, char_def)`` = Fabrik; ``step_page_value``
mappt den Widget-Wert pro Schritt auf das, was ``CharGenWizard.set``
erwartet (z. B. Equipment-PlainText -> (items, purse)).

Kern-Prinzip: Die Widget-Auswahl ist IMMER die Wertquelle -- keine
findChild-Extraktion. Freitext-Felder sind frei editierbar; ComboBoxen
sind editierbar (RM-Volber/Beruf = Freitext nach Rassenwahl, Rassenliste =
optional). Die Wizard-Logik (``rpgpoc.gui.wizardlogic``) validiert.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QSpinBox,
    QWidget,
)


# ---------------------------------------------------------------------------
# Rein testbare Text-Zerleger (kein Qt)
# ---------------------------------------------------------------------------

_TAS_RE = re.compile(r"^\s*(tasche|purse|beutel)\s*:\s*(\S+)", re.IGNORECASE)


def parse_plaintext_items(text: str) -> Tuple[List[Dict[str, Any]], int]:
    """Freitext -> (items, purse).

    Zeile = Item-Name (Leerzeilen ignorieren); eine Zeile ``<tasche|purse>:
    <N>`` (Name optional) definiert den Geldbeutel; alles ab dort
    weiterhin Item-Zeilen. Keine Items -> items=[].
    """
    items: List[Dict[str, Any]] = []
    purse = 0
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        m = _TAS_RE.match(line)
        if m:
            tail = m.group(2)
            try:
                purse = int(tail)
            except ValueError:
                purse = 0
            continue
        items.append({"name": line})
    return items, int(purse)


_BGO_RE = re.compile(r"^\s*(vorteil|nachteil)\s*:\s*(.+?)\s*(?:\|\s*(-?\d+))?\s*$",
                     re.IGNORECASE)


def parse_bgo_lines(text: str) -> List[Dict[str, Any]]:
    """Freitext -> BGO-Liste (je Zeile ``art:name[|cost]``).

    art = vorteil|nachteil (sonst ignoriert). cost fehlt: 1 (vorteil).
    nachteil kostet ausserhalb der Kosten-Tabelle 0.
    """
    out: List[Dict[str, Any]] = []
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        m = _BGO_RE.match(line)
        if not m:
            continue
        kind = m.group(1).lower()
        name = m.group(2).strip()
        cost_s = m.group(3)
        cost = int(cost_s) if cost_s is not None else (0 if kind == "nachteil" else 1)
        if not name:
            continue
        out.append({"kind": kind, "name": name, "cost": cost})
    return out


def parse_equip_value(text: str) -> Tuple[List[Dict[str, Any]], int]:
    """Step-Value fuer ``equipment``: PlainText -> (items, purse)."""
    return parse_plaintext_items(text)


def parse_bgos_value(text: str) -> List[Dict[str, Any]]:
    """Step-Value fuer ``bgos``: PlainText -> Eintraege-Liste."""
    return parse_bgo_lines(text)


# ---------------------------------------------------------------------------
# Step-Widgets (eine pro Schritt-Typ)
# ---------------------------------------------------------------------------

class StepPage(QWidget):
    """Widget-Basis fuer einen einzelnen CharGen-Schritt."""

    def __init__(self, label: str = "") -> None:
        super().__init__()
        self.label = label
        self._lay = QFormLayout(self)
        self._lay.setContentsMargins(8, 8, 8, 8)

    def value(self) -> Any:
        raise NotImplementedError

    def set_value(self, v: Any) -> None:
        raise NotImplementedError


class ComboStep(StepPage):
    """Editierbare ComboBox: Rassen/Volber/Beruf/Name.

    Optionen sind optional (Rassen aus ``char_def.races``); bei
    leerer Liste bleibt das Feld als freie Texteingabe.
    """

    def __init__(self, label: str, opts: Sequence[str] = (),
                 value: str = "") -> None:
        super().__init__(label)
        self.combo = QComboBox()
        self.combo.setEditable(True)
        if opts:
            self.combo.addItems([str(o) for o in opts])
        if value:
            i = self.combo.findText(str(value))
            if i >= 0:
                self.combo.setCurrentIndex(i)
            else:
                self.combo.setEditText(str(value))
        self._lay.addRow(label, self.combo)

    def value(self) -> str:
        return self.combo.currentText().strip()

    def set_value(self, v: Any) -> None:
        self.combo.setEditText(str(v or ""))


class SpinStep(StepPage):
    """SpinBox-Step (DP-Pool)."""

    def __init__(self, label: str, default: int = 600) -> None:
        super().__init__(label)
        self.spin = QSpinBox()
        self.spin.setRange(0, 10_000_000)
        self.spin.setValue(int(default))
        self._lay.addRow(label, self.spin)

    def value(self) -> int:
        return int(self.spin.value())

    def set_value(self, v: Any) -> None:
        self.spin.setValue(int(v))


class SelectStep(StepPage):
    """Multi-Selection (Kategorien): QListWidget, value() = gewählte Namen."""

    def __init__(self, label: str, opts: Sequence[str] = (),
                 selected: Sequence[str] = ()) -> None:
        super().__init__(label)
        self.list = QListWidget()
        self.list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        for o in opts:
            self.list.addItem(QListWidgetItem(str(o)))
        self._select(selected)
        self._lay.addRow(label, self.list)

    def _select(self, names: Sequence[str]) -> None:
        want = {str(n).lower() for n in (names or [])}
        for i in range(self.list.count()):
            it = self.list.item(i)
            it.setSelected(str(it.text()).lower() in want)

    def options(self) -> List[str]:
        return [self.list.item(i).text() for i in range(self.list.count())]

    def value(self) -> List[str]:
        return [it.text() for it in self.list.selectedItems()]

    def set_value(self, v: Any) -> None:
        self.list.clearSelection()
        self._select(v or [])


class TextStep(StepPage):
    """Freitext-Mehrzeilen (equipment, bgos)."""

    def __init__(self, label: str, placeholder: str = "",
                 height: int = 120) -> None:
        super().__init__(label)
        self.text = QPlainTextEdit()
        self.text.setPlaceholderText(placeholder or "")
        self.text.setFixedHeight(height)
        self._lay.addRow(label, self.text)

    def value(self) -> str:
        return self.text.toPlainText()

    def set_value(self, v: Any) -> None:
        self.text.setPlainText(str(v if v is not None else ""))


class NameStep(StepPage):
    """Charakter-Name (einzelwertig)."""

    def __init__(self, label: str = "Charakter-Name") -> None:
        super().__init__(label)
        self.edit = QLineEdit()
        self.edit.setPlaceholderText(label)
        self._lay.addRow(label, self.edit)

    def value(self) -> str:
        return self.edit.text().strip()

    def set_value(self, v: Any) -> None:
        self.edit.setText(str(v if v is not None else ""))


# ---------------------------------------------------------------------------
# Fabrik + Wert-Entnahme
# ---------------------------------------------------------------------------

def make_step_page(step_key: str,
                   definition: Dict[str, Any],
                   char_def: Optional[Dict[str, Any]] = None) -> StepPage:
    """Neues Step-Widget fuer ``step_key`` (aus ``wizardlogic.STEP_KEYS``)."""
    d = definition or {}
    cd = char_def or {}
    races = cd.get("races") or d.get("races") or []
    race_opts = [str(r.get("name")) for r in races
                 if isinstance(r, dict) and r.get("name")]

    if step_key == "race":
        return ComboStep("Rasse", race_opts)
    if step_key == "folk":
        # RM: freie Eingabe (kein fixer Volber-Liste in der PoC-Definition)
        return ComboStep("Volk/Affinitaet")
    if step_key == "occupation":
        return ComboStep("Beruf/Taetigkeit")
    if step_key == "stats":
        pool = int((d.get("chargen") or {}).get("default_pool") or 600)
        return SpinStep("DP-Pool", default=pool)
    if step_key == "categories":
        cats = [c["name"] for c in (d.get("categories") or [])
                if isinstance(c, dict) and c.get("name")]
        return SelectStep("Grundkategorien (mind. 1)", cats)
    if step_key == "equipment":
        return TextStep(
            "Ausruestung (Zeile je Item; 'Tasche: N' = purse)",
            "Schild\nLangschwert\nTasche: 12")
    if step_key == "bgos":
        return TextStep(
            "BGOs (vorteil:nachteil; optional |cost)",
            "vorteil: Nahsicht|1\nnachteil: Geiz|0")
    if step_key == "finalize":
        return NameStep()
    raise ValueError(f"unbekannter Schritt {step_key!r}")


def step_page_value(widget: StepPage, step_key: str) -> Any:
    """Wert aus einem Step-Widget, gemass dem Schritt-Kontrakt."""
    v = widget.value()
    if step_key in ("race", "folk", "occupation"):
        return str(v or "").strip()
    if step_key == "stats":
        return int(v)
    if step_key == "categories":
        return list(v)
    if step_key == "equipment":
        return parse_equip_value(str(v or ""))
    if step_key == "bgos":
        return parse_bgos_value(str(v or ""))
    if step_key == "finalize":
        return str(v or "").strip()
    return v
