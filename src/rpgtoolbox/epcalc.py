#!/usr/bin/env python
'''!
\package rpgtoolbox.epcalc
\file epcalc.py
\brief This  module holds helpers for calculating the EPs and handling NPCs.

\date (C) 2015-2022
\license GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
__version__ = "1.0"
__updated__ = "08.10.2022"
__me__ = "rpgtoolbox.epcalc"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__license__ = "GPL V3"

from .rpgtools import getLvl as calcLvl
from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import *

mycnf = chkCfg()
logger = log.createLogger('epcalc', 'debug', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = "epcalc.log")



class experience(object):
    '''!
    This class will generate an object to handle a character's gained experience.
    It holds the following attributes:
    - \b name: character name
    - \b ep: experience points
    - \b newep: new experience points after adding the gained ones
    - \b lvl: current character's level based on given initial EPs
    - \b newlvl: new character's level based on newep
    - \b gainedep: gained EPs by different actions

    '''


    def __init__(self, charname = "Conan", ep = 0):
        '''!
        Constructor experience
        \param charname name of the character
        \param ep current experience points of the character.

        '''
        self.name = charname
        logger.debug(f"character: {self.name}")
        self.ep = ep
        self.getLvl = calcLvl
        self.lvl = self.getLvl(self.ep)
        self.gainedep = 0
        self.updateInfo()


    def updateInfo(self):
        """!
        Update level information. \n
        The following attributes will be set:
        - newep
        - newlvl
        """
        self.newep = self.ep + self.gainedep
        logger.debug(f"EPs: {self.ep} + {self.gainedep} = {self.newep}")
        self.newlvl = self.getLvl(self.newep)
        logger.debug(f" lvl ==> {self.newlvl}")


    def spell(self, spelllevel = 1, number = 1):
        '''!
        Adds EP gained by spells.
        \param spelllevel level of the casted spell
        \param number number of spells casted
        '''
        self.gainedep += (100 - (self.lvl - spelllevel) * 10) * number
        logger.debug(f"added spell EP: {self.gainedep}")


    def gainedCrit(self, crittype = "A", number = 0):
        '''!
        Adds EPs by gained Crits
        \param crittype Level of Crit
        \param number number of gained crits of that level.
        '''
        crits = {'T': 0,
                   'A': 100,
                   'B': 200,
                   'C': 300,
                   'D': 400,
                   'E': 500
                   }

        self.gainedep += crits[crittype.upper()] * number
        logger.debug(f"added gained Crit EP: {self.gainedep}")


    def hitCrit(self, crittype = "A", monsterlvl = 1, number = 1):
        '''!
        Adds EPs by caused Crits
        \param crittype Level of the Crit
        \param monsterlvl level of the hit monster
        \param number number of crits of that level against such a monster
        '''
        crits = {'A': 5,
                'B': 10,
                'C': 15,
                'D': 20,
                'E': 25
               }

        if monsterlvl == 0:
            monsterlvl = 0.5

        self.gainedep += int(round(monsterlvl * crits[crittype.upper()], 0)) * number
        logger.debug(f"added Crit EP: {self.gainedep}")


    def travelled(self, km = 0):
        '''!
        Adds EPs for traveled km.
        \param km kilometers traveled
        '''
        self.gainedep += km
        logger.debug(f"added travelled EP: {self.gainedep}")


    def gainedHits(self, hits = 0):
        '''!
        Adds EPs for hits
        @param hits number of gained hits
        '''
        self.gainedep += hits
        logger.debug(f"added hits EP: {self.gainedep}")


    def ideas(self, eps = 0):
        '''!
        EPs for ideas, risk etc of the character.
        @param eps additional EPs givem by GM
        '''
        self.gainedep += eps
        logger.debug(f"added ideas EP: {self.gainedep}")


    def maneuver(self, manlvl = "routine", number = 0):
        '''!
        Adds EPs by maneuvers.
        \param manlvl difficulty of maneuver
        \param number number of maneuvers of this level
        '''
        from rpgToolDefinitions.epcalcdefs import maneuvers

        self.gainedep += maneuvers[manlvl]['ep'] * number
        logger.debug(f"added maneuvers EP: {self.gainedep}")


    def killedNPC(self, monsterlvl = 1, number = 1):
        '''!
        Adds EPs by killing a NPC/Monster
        \param monsterlvl level of killed monster
        \param number number of killed monsters of that level
        '''
        if monsterlvl == 0:
            self.gainedep += (50 - (monsterlvl + 1 - self.lvl) * 5) * number

        else:
            self.gainedep += (200 + (monsterlvl - self.lvl) * 50) * number

        logger.debug(f"added Kill EP: {self.gainedep}")
