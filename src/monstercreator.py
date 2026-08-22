#!/usr/bin/env python3
r'''
Monster Creator - neu modularisiert
GUI (monstercreatorWin, showNPCWin, magicSelectorWin, showCPWin) -> gui/modules/attackcheck_gui.py
Logik (prepareAttackData etc.) -> rpgtoolbox.combatcore / rpgtoolbox.combat
'''

from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import chkCfg
from gui.modules.attackcheck_gui import (
    monstercreatorWin,
    showNPCWin,
    magicSelectorWin,
    showCPWin
)


if __name__ == '__main__':
    mycnf = chkCfg()
    logger = log.createLogger('monster', 'info', '4 MB', 1,
                              logpath=mycnf.cnfparam["logpath"],
                              logfile='monstercreator.log')
    logger.debug('Open monster creator window')
    monstercreator = monstercreatorWin(config=mycnf)
