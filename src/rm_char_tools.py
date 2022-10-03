#!/usr/bin/python3
'''!
@file rm_char_tools.py
@package rm_char_tools.py
@brief This is a little tool for creating and keeping track of Role Master Characters

This tool handles
@li Creation of new RM characters
@li Creation and keeping track of RM character parties to select specific information to GM
@li level development of characters (simple character history included)
@li Calculation of EPs
@li Export characters/party information as JSON, LaTex, PDF
@li Buying/keeping track of character's equipment & treasures

@date (C) 2015-2022
@author Marcus Schwamberger
@email marcus@lederzeug.de
@license GNU V3.0
@version 1.1.0

@todo design: individual/group history. maybe create an in-time calendar module...
@todo desing: herb store and search

'''
from gui.epwins import *
from rpgtoolbox.lang import *
from rpgtoolbox.confbox import *
from rpgtoolbox import logbox as log

__author__ = "Marcus Schwamberger"
__updated__ = "02.10.2022"
__copyright__ = "(C) 2015-" + __updated__[-4:] + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "1.1.0"
__license__ = "GNU V3.0"
__me__ = "A MERS/RM RPG Toolbox for Python 3.x"

if __name__ == '__main__':

    mycnf = chkCfg()
    logger = log.createLogger('rpg', 'warning', '4 MB', 1, mycnf.cnfparam["logpath"])
    print(mycnf.cnfparam["logpath"])
    logger.debug("Open main window: lang - {}; storepath - {}".format(mycnf.cnfparam['lang'], mycnf.cnfparam['datapath']))
    mywindow = MainWindow(lang = mycnf.cnfparam['lang'], title = "EP Calculator", storepath = mycnf.cnfparam['datapath'])
    logger.info("Program finished")
