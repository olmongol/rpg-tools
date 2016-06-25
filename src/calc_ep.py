#!/usr/bin/env python
'''
\file calc_ep.py
\package calc_ep
\brief This is a little tool for calculating EPs for MERS/RM


\date (C) 2015-2016
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 0.3

\todo design edit window: Critical Hits
\todo design edit window: Killed Monsters
\todo design edit window: used spells
\todo design: enter/save/load character list/party
\todo design: successful maneuvers
\todo design: traveled distance
\todo design: individual EPs

'''
#import ConfigParser as CP
import Tkinter
from gui.epwins import *
from rpgtoolbox.lang import *
from rpgtoolbox.confbox import *
from rpgtoolbox import logbox as log
from rpgToolDefinitions.epcalcdefs import *

__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015 " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "0.5.5 alpha"
__license__ = "GNU V3.0"
__me__ = "A MERS/RM EP Calculator for Python 2.x"


class epSheet(object):
    '''
    Class for calculating EP sheets
    '''
    def __init__(self, charList = ['Digger the Dwarf']):
        self.party = {}

        for pchar in charList:
            self.party[pchar] = epchr

        logger.debug('epSheet: self.party initialized')


    def notdoneyet(self):
        '''
        Most important dummy function.
        '''
        print "Sorry this feature is not done yet!! :("



if __name__ == '__main__':
    logger = log.createLogger('rpg', 'debug', '1 MB', 1, './')
    mycnf = chkCfg()
    mywindow = MainWindow(lang = mycnf.cnfparam['lang'], title = "EP Calculator", storepath = mycnf.cnfparam['datapath'])
