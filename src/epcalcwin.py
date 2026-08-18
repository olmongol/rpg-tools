#!/usr/bin/env python3
r'''
EP Calc Win - neu modularisiert: gui/modules/epcalcwin_gui.py

Importiert jetzt alle GUI-Klassen aus dem neuen Modul.
Die Berechnungslogik (EP-Bonus etc.) wird in rpgtoolbox/epCalcBonus ausgelagert.
'''
__version__ = "1.2"

from gui.modules.epcalcwin_gui import (
    EPCalcWin,
    showGrpEP,
    manWin
)
