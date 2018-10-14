#!/usr/bin/env python
'''
\package rpgtoolbox.epcalc
\file epcalc.py
\brief This  module holds helpers for calculating the EPs and handling NPCs.

\date (C) 2015-2018
\license GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''

from rpgtools import getLvl as calcLvl

__version__ = "0.1"
__updated__ = "10.06.2018"



class experience(object):
    '''
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
        '''
        \param charname name of the character
        \param ep current experience points of the character.

        '''
        self.name = charname
        self.ep = ep
        self.getLvl = calcLvl
        self.lvl = self.getLvl(self.ep)
        self.gainedep = 0
        self.updateInfo()


    def updateInfo(self):
        """
        Update level information. \n
        The following attributes will be set:
        - newep
        - newlvl
        """
        self.newep = self.ep + self.gainedep
        self.newlvl = self.getLvl(self.newep)


    def spell(self, spelllevel = 1, number = 1):
        '''
        Adds EP gained by spells.
        \param spelllevel level of the casted spell
        \param number number of spells casted
        '''
        self.gainedep += (100 - (self.lvl - spelllevel) * 10) * number


    def gainedCrit(self, crittype = "A", number = 0):
        '''
        Adds EPs by gained Crits
        \param crittype Level of Crit
        \param number number of gained crits of that level.
        '''
        crits = {'T' : 0,
                   'A' : 100,
                   'B' : 200,
                   'C' : 300,
                   'D' : 400,
                   'E' : 500
                   }

        self.gainedep += crits[crittype.upper()] * number


    def hitCrit(self, crittype = "A", monsterlvl = 1, number = 1):
        '''
        Adds EPs by caused Crits
        \param crittype Level of the Crit
        \param monsterlvl level of the hit monster
        \param number number of crits of that level against such a monster
        '''
        crits = {'A' : 5,
                'B' : 10,
                'C' : 15,
                'D' : 20,
                'E' : 25
               }

        if monsterlvl == 0:
            monsterlvl = 0.5

        self.gainedep += int(round(monsterlvl * crits[crittype.upper()], 0)) * number


    def travelled(self, km = 0):
        '''
        Adds EPs for traveled km.
        \param km kilometers traveled
        '''
        self.gainedep += km


    def gainedHits(self, hits = 0):
        '''
        Adds EPs for hits
        @param hits number of gained hits
        '''
        self.gainedep += hits


    def ideas(self, eps = 0):
        '''
        EPs for ideas, risk etc of the character.
        @param eps additional EPs givem by GM
        '''
        self.gainedep += eps


    def maneuver(self, manlvl = "routine", number = 0):
        '''
        Adds EPs by maneuvers.
        \param manlvl difficulty of maneuver
        \param number number of maneuvers of this level
        '''
        from rpgToolDefinitions.epcalcdefs import maneuvers

        self.gainedep += maneuvers[manlvl]['ep'] * number


    def killedNPC(self, monsterlvl = 1, number = 1):
        '''
        Adds EPs by killing a NPC/Monster
        \param monsterlvl level of killed monster
        \param number number of killed monsters of that level
        '''
        if monsterlvl == 0:
            self.gainedep += (50 - (monsterlvl + 1 - self.lvl) * 5) * number

        else:
            self.gainedep += (200 + (monsterlvl - self.lvl) * 50) * number



class NPC(object):
    '''
    \todo has to be implemented for fight simulations
    '''


    def __init__(self, npcfile, beast, lvl):
        pass
