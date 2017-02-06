#!/usr/bin/env python
'''
\file rm_char_tools.py
\package rm_char_tools.py
\brief This is a little tool for creating and keeping track of Role Master Characters

This tool handles
\li Creation of new RM characters
\li Creation and keeping track of RM character parties to select specific information to GM
\li level development of characters (simple character history included)
\li Calculation of EPs 
\li Export characters/party infomation as JSON, LaTex, PDF
\li Buying/keeping track of character's equipment & treasures

\date (C) 2015-2017
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 0.3.1

\todo design edit window: Critical Hits
\todo design edit window: Killed Monsters
\todo design edit window: used spells
\todo design: enter/save/load character list/party
\todo design: successful maneuvers
\todo design: traveled distance
\todo design: individual EPs
\todo design: Export functions
\todo design: Equipment, Shop, Treasures (Chris) 
\todo integrate magical item generator into project (Aiko)
\todo integrate (and program) treasure generator (Aiko)
'''
#import ConfigParser as CP
#import Tkinter
from gui.epwins import *
from rpgtoolbox.lang import *
from rpgtoolbox.confbox import *
from rpgtoolbox import logbox as log
#from rpgToolDefinitions.epcalcdefs import *

__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2017 " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "0.3.1"
__license__ = "GNU V3.0"
__me__ = "A MERS/RM EP Calculator for Python 2.7"




if __name__ == '__main__':
    logger = log.createLogger('rpg', 'debug', '1 MB', 1, './')
    mycnf = chkCfg()
    mywindow = MainWindow(lang = mycnf.cnfparam['lang'], title = "EP Calculator", storepath = mycnf.cnfparam['datapath'])
