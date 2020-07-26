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

        """
        self.data = data
        self.dtype = datatype
        self.lang = lang
        self.storepath = storepath
        pass


    def setAttributes(self):
        pass


    def calcCurrDB(self):
        pass


    def calcCurrOB(self):
        pass


    def rollAttack(self, ob = 0, db = 0):
        pass


    def rollCrit(self, crittype = "A", crittab = "slash"):
        pass


    def writeCritResult(self, critresult = {}):
        pass


    def storeDamage(self):
        pass

