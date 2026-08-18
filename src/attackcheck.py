#!/usr/bin/env python3
r'''!
\package monstercreator
\brief Monster Creator - neu modularisiert abgui/ modules/attackcheck_gui

Dieses File importiert jetzt nur noch die GUI-Klassen aus gui.modules.attackcheck_gui.
Die Berechnungslogik (prepareAttackData etc.) bleibt als standalone Funktion in rpgtoolbox.combatcore.
'''
__version__ = "0.3"
__updated__ = "08.12.2023"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"

# Importiere die GUI-Klassen aus dem neuen Modul
from gui.modules.attackcheck_gui import (
    monstercreatorWin,
    showNPCWin,
    magicSelectorWin,
    showCPWin
)
