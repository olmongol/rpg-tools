"""GUI-Logik: Inventar-TableModel (05: "QTableView für Inventar").

Logik (Zeilenauszug aus State) = reine Funktion ``inventory_rows``
(testbar ohne Qt). Das Qt-Modell ``InventoryModel`` ist nur die
Anzeige-Hülle darum (refresh() ersetzt die Zeilen aus client.sheet()).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt

HEADERS = ("seq", "id", "name", "actor")


def inventory_rows(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Inventar-Zeilen aus reduziertem State (state['inventory']).

    Reihenfolge = reducer-Chronologie (append-only); Zeile =
    {seq, id, name, actor}. Keine Logik hier (Sort = Anzeige-Kosmetik).
    """
    inv = state.get("inventory") or []
    return [
        {"seq": i.get("seq"), "id": i.get("id"),
         "name": i.get("name"), "actor": i.get("actor")}
        for i in inv
    ]


class InventoryModel(QAbstractTableModel):
    """QTableView-Modell über state['inventory']; refresh(state) ersetzt Zeilen."""

    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self._rows: List[Dict[str, Any]] = []

    # -- Qt-TableModel-Interface ------------------------------------------

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(HEADERS)

    def data(self, index: QModelIndex,
             role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return self._rows[index.row()].get(HEADERS[index.column()])
        return None

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return HEADERS[section]
        return section + 1

    # -- Aktualisierung -----------------------------------------------------

    def reset_rows(self, rows: List[Dict[str, Any]]) -> None:
        """Zeilen komplett ersetzen (Reset-Semantik für die Tabelle)."""
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def refresh(self, state: Dict[str, Any]) -> None:
        """Aus Client-State neu befüllen (State = fold(Events))."""
        self.reset_rows(inventory_rows(state))
