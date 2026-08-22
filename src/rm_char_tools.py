#!/usr/bin/env python3
r'''
Char Tools - neu modularisiert
GUI (MainWindow) -> gui.epwins / gui/modules/char_tools_gui.py
'''

from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import chkCfg
from gui.epwins import MainWindow


if __name__ == '__main__':
    mycnf = chkCfg()
    logger = log.createLogger('rpg', 'warning', '4 MB', 1,
                              mycnf.cnfparam["logpath"],
                              logfile='rm_char_tools.log')
    logger.debug("Open main window: lang - {}; storepath - {}".format(
        mycnf.cnfparam['lang'], mycnf.cnfparam['datapath']))
    mywindow = MainWindow(
        lang=mycnf.cnfparam['lang'],
        title='EP Calculator',
        storepath=mycnf.cnfparam['datapath']
    )
    logger.info("Program finished")
