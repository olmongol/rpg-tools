#!/usr/bin/env python
'''!
\file /home/mongol/git/rpg-tools/src/rolemaster/encounters.py
\package rolemaster.encounters
\brief This module holds all classes and functions to handle encounters (animals, monsters, NPCS etc.)

This is a package with classes and funtions for
- create/improve individual tables with data of NPCs, animals, monsters etc.
- fast and easy create encounter value tables for GMs (play preparation) from default table(s)
- create tables for random encounters
- determine random encounters (and use them in the attackmodule

\date (c) 2022
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "25.02.2022"
__author__ = "Marcus Schwamberger"
__me__ = "encounters"

import os
import json
from tkinter import filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
#from pprint import pformat
from copy import deepcopy
from random import randint
from rpgtoolbox.combat import *
#from rpgtoolbox.rpgtools import dice
from rpgToolDefinitions.helptools import RMDice as Dice
from rpgToolDefinitions.magic import magicpath
from gui.window import *
from rpgtoolbox import logbox as log
from rpgtoolbox.globaltools import *
from rpgtoolbox.handlemagic import getSpellNames
from rpgtoolbox.confbox import *

chkcnf = chkCfg(path = "../" + defaultconfigpath)
logger = log.createLogger('encounters module', 'debug', '1 MB', 1, chkcnf.cnfparam["logpath"], logfile = "encounters.log")



class tableCheck():
    '''!
    This checks the syntax of a table csv
    '''


    def __init__(self, filename, lang = chkcnf.cnfparam["lang"]):
        '''
        @todo still a dummy. has to be fully implemented
        '''
        pass

