"""GUI: Hauptfenster (05: K8+K9) -- Stats + Inventar-Tabelle + offene
GM-Vorschläge. Logik (State -> Zeilen) = reine Funktionen (testbar ohne
Qt); das Fenster zeigt sie nur.

Verdrahtung: ``RpgMainWindow(definition, client)``. ``refresh(client)``
liest State = client.sheet() und füllt die drei Panels. Zweiter
Client auf denselben Store sieht exakt dasselbe (append-only, 05:
K9).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from PyQt6.QtWidgets import (
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
)


# ---------------------------------------------------------------------------
# Reine Funktionen (offscreen / ohne Qt testbar)
# ---------------------------------------------------------------------------

def _char_created_payload(state: Dict[str, Any]) -> Dict[str, Any]:
    """character_created.payload as Dict (or {} if none)."""
    cc = state.get("character_created") or {}
    if not isinstance(cc, dict):
        return {}
    pl = cc.get("payload") or {}
    return pl if isinstance(pl, dict) else {}


def stats_display_rows(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Stats-Zeilen (abbr + Temp/Bonus/Base/Race/Cost) für die Anzeige."""
    pl = _char_created_payload(state)
    stats = pl.get("stats") if isinstance(pl, dict) else None
    if not isinstance(stats, dict):
        return []
    rows: List[Dict[str, Any]] = []
    for abbr in ("St", "Ag", "Re", "Co", "Pr", "Me", "In", "Qu", "Em", "SD"):
        row = stats.get(abbr)
        if not isinstance(row, dict):
            continue
        rows.append({
            "abbr": abbr,
            "base": row.get("base"),
            "race": row.get("race"),
            "temp": row.get("temp"),
            "bonus": row.get("bonus"),
            "cost": row.get("cost"),
        })
    return rows


def stat_summary(row: Dict[str, Any]) -> str:
    """Kurz-Zeile für ein Stat aus ``stats_display_rows``."""
    v = lambda k: row.get(k)
    return (f"Temp {v('temp')} (+{v('bonus')})"
            f"  [Base {v('base')}, Race {v('race')}, Cost {v('cost')}]")


def inventory_display_rows(state: Dict[str, Any]) -> List[List[Any]]:
    """Inventar-Zeilen [seq, id, name, actor]."""
    out: List[List[Any]] = []
    for item in (state.get("inventory") or []):
        if not isinstance(item, dict):
            continue
        out.append([item.get("seq"), item.get("id") or "",
                    item.get("name"), item.get("actor")])
    return out


def pending_display_rows(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Offene Stat-Vorschläge (status != 'approved')."""
    out: List[Dict[str, Any]] = []
    for sid, entry in (state.get("pending_stats") or {}).items():
        if not isinstance(entry, dict):
            continue
        status = entry.get("status", "pending")
        if status == "approved":
            continue
        out.append({
            "stat": sid, "value": entry.get("value"),
            "actor": entry.get("actor"), "seq": entry.get("seq"),
            "status": status,
        })
    out.sort(key=lambda r: (r.get("seq") is None, r.get("seq") or 0))
    return out


def pending_labels(rows: List[Dict[str, Any]]) -> List[str]:
    """Zeilen -> anzeigefertige Label-Strings."""
    STATUS_DE = {"pending": "offen", "rejected": "abgelehnt"}
    out: List[str] = []
    for r in rows:
        status = r.get("status", "pending")
        label = STATUS_DE.get(status, status)
        out.append(f"{r.get('stat')}={r.get('value')} "
                   f"({label}, von {r.get('actor') or '?'}, seq {r.get('seq')})")
    return out


# ---------------------------------------------------------------------------
# Qt-Fenster
# ---------------------------------------------------------------------------

def _make_stats_table(n_rows: int) -> QTableWidget:
    tbl = QTableWidget(n_rows, 6)
    tbl.setHorizontalHeaderLabels(["Stat", "Base", "Race", "Temp", "Bonus", "Cost"])
    tbl.verticalHeader().setVisible(False)
    tbl.setMinimumWidth(260)
    return tbl


def _make_inv_table(n_rows: int) -> QTableWidget:
    tbl = QTableWidget(n_rows, 4)
    tbl.setHorizontalHeaderLabels(["seq", "id", "name", "actor"])
    tbl.verticalHeader().setVisible(False)
    tbl.setMinimumWidth(340)
    return tbl


class RpgMainWindow(QMainWindow):
    """Hauptfenster (Stats / Inventar / offene Vorschläge / Item-Eingabe)."""

    def __init__(self, definition: Dict[str, Any], client,
                 parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self.definition = definition or {}
        self.client = client
        self.setWindowTitle(f"RPG — {getattr(client, 'char_name', getattr(client, 'char', '?'))}")

        # Stats
        self.stats_table = _make_stats_table(0)

        # Inventar
        self.inv_table = _make_inv_table(0)

        # Offene Vorschläge
        self.pending_list = QListWidget()
        self.pending_list.setMinimumWidth(220)

        # Item-Eingabe
        self.item_id = QLineEdit()
        self.item_id.setPlaceholderText("Item-ID (optional)")
        self.item_name = QLineEdit()
        self.item_name.setPlaceholderText("Item-Name (z. B. 'Schild')")
        self.btn_add = QPushButton("Hinzufügen")
        self.btn_refresh = QPushButton("Aktualisieren")

        # Layout
        stats_widget = QWidget()
        sl = QVBoxLayout(stats_widget)
        sl.addWidget(QLabel("Stats"))
        sl.addWidget(self.stats_table)
        sl.addStretch(1)

        inv_widget = QWidget()
        il = QVBoxLayout(inv_widget)
        il.addWidget(QLabel("Inventar"))
        il.addWidget(self.inv_table)
        row = QHBoxLayout()
        row.addWidget(self.item_id)
        row.addWidget(self.item_name)
        row.addWidget(self.btn_add)
        il.addLayout(row)
        il.addWidget(QLabel("Offene Vorschläge (GM):"))
        il.addWidget(self.pending_list)
        il.addStretch(1)

        splitter = QSplitter()
        splitter.addWidget(stats_widget)
        splitter.addWidget(inv_widget)
        self.setCentralWidget(splitter)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.btn_add.clicked.connect(self.on_add_item)
        self.btn_refresh.clicked.connect(self.refresh)

        self.refresh()

    # ------------------------------------------------------------------

    def refresh(self, client: Optional[Any] = None) -> None:
        """View aus Client-State aktualisieren (State = fold(Events))."""
        if client is not None:
            self.client = client
        state = self.client.sheet()

        # Stats
        srows = stats_display_rows(state)
        self.stats_table.setRowCount(len(srows))
        for r, row in enumerate(srows):
            for c, col in enumerate(("base", "race", "temp", "bonus", "cost")):
                self.stats_table.setItem(r, 1 + c, QTableWidgetItem(str(row[col])))
            self.stats_table.setItem(r, 0, QTableWidgetItem(row["abbr"]))

        # Inventar
        irows = inventory_display_rows(state)
        self.inv_table.setRowCount(len(irows))
        for r, row in enumerate(irows):
            for c, val in enumerate(row):
                self.inv_table.setItem(r, c, QTableWidgetItem(str(val)))

        # Offene Vorschläge
        prows = pending_display_rows(state)
        self.pending_list.clear()
        for lbl in pending_labels(prows):
            self.pending_list.addItem(QListWidgetItem(lbl))

        seq = self.client.last_seq()
        self.status.showMessage(
            f"seq {seq} · char {self.client.char}"
            f" · Items {len(state.get('inventory', []))}"
            f" · offen {len(prows)}",
        )

    # ------------------------------------------------------------------
    # Aktionen
    # ------------------------------------------------------------------

    def on_add_item(self) -> None:
        name = self.item_name.text().strip()
        item_id = self.item_id.text().strip()
        if not name:
            self.status.showMessage("Item-Name fehlt")
            return
        try:
            self.client.item_add(name=name, item_id=item_id or None)
        except Exception as e:  # ClientError
            self.status.showMessage(f"Item fehlgeschlagen: {e}")
            return
        self.item_name.clear()
        self.item_id.clear()
        self.refresh()
