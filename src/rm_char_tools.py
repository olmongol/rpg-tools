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
\li Export characters/party information as JSON, LaTex, PDF
\li Buying/keeping track of character's equipment & treasures

\date (C) 2015-2018
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 1.0.0

\todo design: Critical Hits/Killed Monster/Combat/injuries --> auto EP calculation
\todo design: enter/save/load character list/party
\todo desigN: Character sheet display on screen
\todo design: GM Screen for display (with infos about character group)
\todo design: maneuver tests (static, movement, spells) --> auto EP calculation
\todo design: additional EP calculation (traveled km, role-play etc.)
\todo design: individual/group history. maybe create an in-time calendar module...
\todo design: Export functions (LaTeX/PDF)
\todo design: Equipment, Shop, Treasures (Chris) 
\todo improve integration of magical item/treasure generator into project
\todo desing: herb store and search

----
\bug in gui.epwins some DP costs >9 are shown as 1 0 for example.
'''
from gui.epwins import *
from rpgtoolbox.lang import *
from rpgtoolbox.confbox import *
from rpgtoolbox import logbox as log

__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015-2018" + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "1.0.0"
__license__ = "GNU V3.0"
__me__ = "A MERS/RM RPG Toolbox for Python 2.7"
__updated__ = "26.05.2018"

if __name__ == '__main__':
    logger = log.createLogger('rpg', 'debug', '1 MB', 1, './')
    mycnf = chkCfg()
    logger.info("Read config file.")
    mywindow = MainWindow(lang = mycnf.cnfparam['lang'], title = "EP Calculator", storepath = mycnf.cnfparam['datapath'])
    logger.info("Program finished")
