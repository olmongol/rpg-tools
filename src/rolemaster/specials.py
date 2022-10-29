#!/usr/bin/env python
'''!
\file /home/mongol/git/rpg-tools/src/rolemaster/specials.py
\package rolemaster.specials
\brief short description

lorem ipsum

\date (c) 2022
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "21.10.2022"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__license__ = "GNU V3"
__copyright__ = f"2022 - {__updated__[-4:]}"

from rpgToolDefinitions.helptools import RMDice
from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import *
from rpgtoolbox.globaltools import readCSV

mycnf = chkCfg()
logger = log.createLogger('Specials', 'debug', '1 MB', 2, logpath = mycnf.cnfparam["logpath"], logfile = "rm_specials.log")



class fumbletable():
    """!
    This class creates a combat fumble table for all types of weapon and non-weapon
    fumbles.
    """


    def __init__(self, tablefilename = "data/default/fight/fumble/combat_fumble.csv", lang = "en"):
        """!
        Constructor
        @param tablefilename path+filename of the fumble table to read
        """
        self.tablename = f"{tablefilename[:-4]}_{lang}{tablefilename[-4:]}"
        #logger.info(f"get fumble table from {self.tablename}")
        #self.fumbetypes = ['one-handed arms', 'two-handed arms', 'polearms and spears',
        #                   'mounted arms', 'thrown arms', 'missile weapons',
        #                   'MA strikes', 'MA sweeps', 'brawling', 'animal']

        self.fumble = readCSV(self.tablename)
        self.fumbletypes = list(self.fumble[0].keys())[1:]


    def getResult(self, fumbletype = "one-handed arms", roll = 50):
        """!
        This method delivers the result from the fumble table by fumble type and
        fumble roll.It may be used for weapon and spell fumbles.

        @param fumbletype type of the fumble concerning of the table header
        @param roll fumble roll result
        @retval result string holding the result of the fumble

        """
        result = ""

        if fumbletype not in self.fumbletypes:
            fumbletype = 'brawling'
            logger.warning(f"fumbletype not found! Set it to {fumbletype}")

        for row in self.fumble:

            if roll <= int(row["roll"]):
                result = row[fumbletype]
                break

        return result

