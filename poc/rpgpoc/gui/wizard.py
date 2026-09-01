"""GUI: 8-Schritt-CharGen-Wizard-Dialog (offscreen-testbar, 05: K8).

Architektur (GUI/Logik-Entkopplung):
  * Logik: ``rpgpoc.gui.wizardlogic.CharGenWizard``  (reines Python, kein Qt)
  * Pages: ``rpgpoc.gui.pages.make_step_page``       (Qt-Widgets pro Schritt)
  * Shell: ``CharGenWizardDialog`` (dieses Modul)     (Stacking + Buttons)

Der Dialog zeigt die aktuelle Seite, ``Weiter`` ruft ``w.set(key, value)``,
``w.advance()``. Fehler -> QLabel + Cursor bleibt stehen. Nach ``finalize``
wird ``done_event`` gesetzt und ein akzeptierter Return.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from PyQt6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
)

from .pages import StepPage, make_step_page, step_page_value
from .wizardlogic import STEP_KEYS, STEP_TITLES, CharGenWizard, CharGenWizardError


class CharGenWizardDialog(QDialog):
    """8 Schritte gegen ``CharGenWizard``; ``result()`` = character_created Event."""

    def __init__(self, definition: Dict[str, Any],
                 char_def: Optional[Dict[str, Any]] = None,
                 seed: Optional[int] = None,
                 parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Charaktererzeugung")
        self.definition = definition or {}
        # char_def liegt optional in definition.char_def (Rassen etc.)
        self.char_def = char_def or self.definition.get("char_def") or {}
        self.wiz = CharGenWizard(self.definition, self.char_def, seed=seed)

        self.pages: Dict[str, StepPage] = {}
        self.stack = QStackedWidget()

        # Seiten-Leiste (ListWidget) -- zeigt Status der 8 Schritte
        self.step_list = QListWidget()
        self.step_list.setMaximumWidth(230)

        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.status = QProgressBar()
        self.status.setRange(0, len(STEP_KEYS))
        self.status.setTextVisible(True)
        self.status.setFormat("%p%")

        nav = QHBoxLayout()
        self.btn_back = QPushButton("Zurück")
        self.btn_next = QPushButton("Weiter")
        self.btn_finish = QPushButton("Fertig")
        self.btn_next.setDefault(True)
        self.btn_finish.setEnabled(False)
        nav.addWidget(self.btn_back)
        nav.addStretch(1)
        nav.addWidget(self.btn_finish)
        nav.addWidget(self.btn_next)

        self.btn_back.setObjectName("btn_back")
        self.btn_next.setObjectName("btn_next")

        self.step_list.setObjectName("step_list")
        self.error_label.setObjectName("error_label")

        self.btn_back.clicked.connect(self.on_back)
        self.btn_next.clicked.connect(self.on_next)
        self.btn_finish.clicked.connect(self.finish_wizard)

        # Hauptlayout
        root = QVBoxLayout(self)
        hrow = QHBoxLayout()
        hrow.addWidget(self.step_list, 0)
        hrow.addWidget(self.stack, 1)
        root.addLayout(hrow)
        root.addWidget(self.status)
        root.addWidget(self.error_label)
        root.addLayout(nav)

        # Seiten bauen
        for key in STEP_KEYS:
            page = make_step_page(key, self.definition, self.char_def)
            self.pages[key] = page
            self.stack.addWidget(page)

        self._rebuild_step_list()
        self._show_current()

    # -- Rendering -----------------------------------------------------------

    def _rebuild_step_list(self) -> None:
        self.step_list.clear()
        for s in self.wiz.steps():
            icon_mark = {"done": "✓", "current": "→", "todo": " "}[s["status"]]
            self.step_list.addItem(f"{icon_mark} {s['index']+1}. {s['title']}")

    def _current_page(self) -> Optional[StepPage]:
        key = self.wiz.current_step()
        return self.pages.get(key)

    def _show_current(self) -> None:
        key = self.wiz.current_step()
        if key == "done":
            self.stack.setCurrentIndex(len(STEP_KEYS) - 1)
            self.btn_next.setEnabled(False)
            self.btn_back.setEnabled(False)
            self.btn_finish.setEnabled(True)
        else:
            self.stack.setCurrentIndex(list(STEP_KEYS).index(key))
            self.btn_next.setEnabled(True)
            self.btn_back.setEnabled(self.wiz._cursor > 0)
            self.btn_finish.setEnabled(False)
        self._sync_input_to_pages()
        self._rebuild_step_list()
        self.error_label.setText(self.wiz.error() or "")
        idx = list(STEP_KEYS).index(key) if key != "done" else len(STEP_KEYS)
        self.status.setValue(idx)

    def _sync_input_to_pages(self) -> None:
        # Jede Seite bekommt ihre Option-Liste aus wizard.options()
        # (hier: nur die aktuelle Seite, weil options() auf current_step greift)
        key = self.wiz.current_step()
        page = self.pages.get(key)
        if page is None:
            return
        try:
            opts = self.wiz.options()
        except Exception:
            opts = None
        if isinstance(page, (object,)) and hasattr(page, "combo"):
            # ComboStep: Option-Auswahl aus wizard.options() laden (falls noch leer)
            if page.combo.count() == 0 and opts:
                for o in opts:
                    page.combo.addItem(str(o))
        # Rest: keine dynamischen Updates nötig (Seiten-Options sind statisch)

    # -- Aktionen ------------------------------------------------------------

    def on_next(self) -> None:
        key = self.wiz.current_step()
        page = self.pages.get(key)
        if page is None:
            self.error_label.setText("Interner Fehler: keine Page")
            return
        try:
            val = step_page_value(page, key)
        except Exception as e:  # noqa: BLE001
            self.error_label.setText(f"Invalid value für {key}: {e}")
            return
        # Option-Hinweis: wenn wizard.options() für die Seite definiert ist,
        # prüfen wir nur dass val nicht leer ist (Chargen macht die echte
        # Validierung in advance()).
        if key in ("race", "folk", "occupation") and not str(val).strip():
            self.error_label.setText(f"Bitte {STEP_TITLES[key]} wählen.")
            return
        if key == "categories" and not list(val or []):
            self.error_label.setText("Wähle mindestens einen Grundkategorie.")
            return
        if key == "finalize" and not str(val or "").strip():
            self.error_label.setText("Bitte Charakter-Name angeben.")
            return
        try:
            self.wiz.set(key, val)
            self.wiz.advance()
        except CharGenWizardError as e:
            self.error_label.setText(str(e))
            return
        except Exception as e:  # ChargenError, ChargenStepError
            self.error_label.setText(f"Schritt {key} fehlgeschlagen: {e}")
            return
        self._show_current()

    def on_back(self) -> None:
        try:
            self.wiz.back()
        except CharGenWizardError:
            self.error_label.setText("Kann nicht zurück")
            return
        self._show_current()

    def finish_wizard(self) -> None:
        try:
            ev = self.wiz.result()
        except CharGenWizardError as e:
            self.error_label.setText(str(e))
            return
        self.result_event = ev
        self.accept()

    # -- Public --------------------------------------------------------------

    @property
    def result(self):
        return getattr(self, "result_event", None)

    def set_state(self, wiz: CharGenWizard) -> None:
        self.wiz = wiz
        self._show_current()
