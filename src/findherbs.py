#!/usr/bin/env python3
r'''
Herb finding tool - neu modularisiert
Logik (findHerbs, string2worth, sumDices) -> rpgtoolbox/herbalogic.py
GUI (searchHerbsWin) -> gui/modules/findherbs_gui.py
'''

from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import chkCfg
from rpgtoolbox.herbalogic import findHerbs, string2worth, sumDices
from gui.modules.findherbs_gui import searchHerbsWin


if __name__ == '__main__':
    mycnf = chkCfg()
    logger = log.createLogger('foraging', 'info', '4 MB', 1,
                              logpath=mycnf.cnfparam["logpath"],
                              logfile='findherbs.log')
    logger.debug('Open herb-finding window')
    win = searchHerbsWin()
