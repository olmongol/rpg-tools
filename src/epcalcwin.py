#!/usr/bin/env python3
r'''
EP Calc Win - neu modularisiert: gui/modules/epcalcwin_gui.py

Importiert jetzt alle GUI-Klassen aus dem neuen Modul.
Die Berechnungslogik (EP-Bonus etc.) wird in rpgtoolbox ausgelagert.
'''
__version__ = "1.2"

import json

from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import chkCfg
import rpgtoolbox.rpgtools as rpg
from gui.modules.epcalcwin_gui import (
    EPCalcWin,
    showGrpEP,
    manWin
)


if __name__ == '__main__':
    mycnf = chkCfg()
    logger = log.createLogger('epcalc', 'info', '4 MB', 1,
                              logpath=mycnf.cnfparam["logpath"],
                              logfile='epcalcwin.log')
    logger.debug('Open EP calculator window')

    with open("/home/mongol/git/rpg-tools/src/data/groups/charparty.json", "r") as fp:
        cl = json.load(fp)

    mantan = rpg.statManeuver
    rrtab = rpg.RRroll

    win = EPCalcWin()
