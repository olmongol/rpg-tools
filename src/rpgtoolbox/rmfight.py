#!/usr/bin/python3
'''
\file rmfight.py
\package rpgtoolbox.py
\brief fighting module (home rules - based on RM)


\date (C) 2020
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 0.1.

'''
from rpgToolDefinitions.helptools import RMDice as rolld100
__updated__ = ""
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__version__ = "0.1"



class combatant(object):
    """
    This creates a combatant in a battle.
    """


    def __init__(self, data = {}, datatype = "char", lang = "en", storepath = "./data/"):
        """
        Constructor
        @param data dictionary that holds the fight credentials of an opponent: chat, monster,creature,nsc
        @param datatype tells wich kind of dataset \param data is,
        @param lang display language
        @param storepath global sorage path
        """
        self.data = data
        self.dtype = datatype
        self.lang = lang
        self.storepath = storepath
        self.setAttributes()
        self.calcCurrDB()
        self.calcCurrOB()
        pass


    def setAttributes(self):
        """
        Sets all needed fight atrributes for combatant.
        """
        pass


    def calcCurrDB(self):
        """
        This (re-)calculates) the totol DB for the  combatant
        """
        pass


    def calcCurrOB(self):
        """
        Thsi (re-)calculates the combatant's current OB
        """
        pass


    def rollAttack(self, obindex = 0, dbtarget = 0, roll = None):
        """
        This executes & solves the attack roll
        @param obindex index of OB list which indicates which attack (bonus, table etc) to use.
        @param dbtarget the attack roll's modification by the defensive abilities of the target.
        @param roll if you do not want to use the digital dice you can give an int as number for a roll.
        """
        pass

        self.roll = rolld100()

        if type(roll) == type(0):
            self.roll = roll


    def rollCrit(self, crittype = "A", crittab = "slash"):
        pass


    def writeCritResult(self, critresult = {}):
        pass


    def storeDamage(self):
        pass
