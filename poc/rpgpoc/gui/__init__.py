"""rpgpoc.gui — PyQt6-Schicht (Anzeige), Logik bleibt testbar (Qt-offscreen).

* ``charform`` / ``inventory`` / ``window``: reine Funktionen + Qt-Widgets
* ``wizardlogic``: CharGenWizard als pure Python (kein Qt-Import)
* ``pages`` / ``wizard``: Qt-Step-Widgets + Wizard-Dialog
"""
from __future__ import annotations

from .charform import build_stats_form, stat_display, stat_values, stats_order
from .inventory import HEADERS, InventoryModel, inventory_rows
from .pages import (
    ComboStep,
    NameStep,
    SelectStep,
    SpinStep,
    StepPage,
    TextStep,
    make_step_page,
    parse_bgos_value,
    parse_equip_value,
    parse_plaintext_items,
    step_page_value,
)
from .window import (
    RpgMainWindow,
    inventory_display_rows,
    pending_display_rows,
    pending_labels,
    stat_summary,
    stats_display_rows,
)
from .wizard import CharGenWizardDialog
from .wizardlogic import STEP_KEYS, STEP_TITLES, CharGenWizard, CharGenWizardError

__all__ = [
    "build_stats_form", "stat_display", "stat_values", "stats_order",
    "HEADERS", "InventoryModel", "inventory_rows",
    "ComboStep", "NameStep", "SelectStep", "SpinStep", "StepPage", "TextStep",
    "make_step_page", "parse_bgos_value", "parse_equip_value",
    "parse_plaintext_items", "step_page_value",
    "RpgMainWindow", "inventory_display_rows", "pending_display_rows",
    "pending_labels", "stat_summary", "stats_display_rows",
    "CharGenWizardDialog",
    "STEP_KEYS", "STEP_TITLES", "CharGenWizard", "CharGenWizardError",
]
