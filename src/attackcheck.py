#!/usr/bin/env python3
r'''
Attack Check - neu modularisiert
GUI (atWin, enemySelector, calFightEP; MonsterCreator: monstercreatorWin,
     showNPCWin, magicSelectorWin, showCPWin) -> gui/modules/attackcheck_gui.py
Logik (prepareAttackData etc.) -> rpgtoolbox/combatcore.py, rpgtoolbox/combat.py

Dieses File bootet den Kampfsimulator (atWin). Die MonsterCreate-Fenster
werden von src/monstercreator.py gestartet (User-Entscheidung TR-004:
Klassen in attackcheck_gui.py belassen).
'''
__version__ = "1.0"
__updated__ = "30.10.2024"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"

from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import chkCfg
from gui.modules.attackcheck_gui import atWin, enemySelector, calFightEP


if __name__ == '__main__':
    mycnf = chkCfg()
    loglevel = mycnf.cnfparam.get("loglvl", "debug")
    logger = log.createLogger('AT-Window', loglevel, '4 MB', 1,
                              logpath=mycnf.cnfparam["logpath"],
                              logfile='attackcheck.log')
    logger.debug("Open attack-check window")
    win = atWin()
    logger.info("Program finished")
