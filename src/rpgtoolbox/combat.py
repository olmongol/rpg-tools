#!/usr/bin/env python
'''
@file /home/mongol/git/rpg-tools/src/rpgtoolbox/combat.py
@package rpgtoolbox
@brief Rolemaster combat module

This module holds everything needed to handle melee/ranged/magical combat

@date (c) 2020
@license GNU V3.0
@author Marcus Schwamberger
@email marcus@lederzeug.de
@version 0.1
'''
__version__ = "0.1"
__updated__ = "04.12.2020"
__author__ = "Marcus Schwamberger"

import re
from rpgtoolbox.globaltools import splitExceptBetween as splitE

#def splitExceptBetween(inputstr, delimiter, quotes):
#    inside = -1
#    result = []
#    oldt = 0
#    for index, letter in enumerate(inputstr):
#        if letter==quotes:
#            inside = -inside
#        elif letter==delimiter and inside == -1:
#            result.append(inputstr[oldt:index])
#            oldt = index+1
#    if oldt<len(inputstr):
#        result.append(inputstr[oldt:])
#    return result



def switch(mystr):
    '''
    '''
    result = {}
    dummy = mystr.split(";")

    for elem in dummy:

        if ":" in elem:
            dummy2 = elem.split(':')

            if dummy2[0] == "mod" and "x" in dummy2[1]:
                result[dummy2[0]] = {"mod":int(dummy2[1].split("x")[0]),
                                     "rnd":int(dummy2[1].split("x")[1])}
            elif dummy2[0] == "mod":
                result[dummy2[0]] = {"mod":int(dummy2[1]),
                                     "rnd":90 * 24 * 60 * 6}
            else:
                result[dummy2[0]] = int(dummy2[1])

    return result



class crittable():
    """
    This Class delivers results from crit tables to a combatant.
    """


    def __init__(self, lang = "en", critfilename = "./data/default/fight/crits/puncture_crit.csv"):
        """
        Constructor
        @param lang configured language: en, de
        @param critfilename name and path of the crit table csv to read
        """
        self.lang = lang
        self.filename = critfilename
        self.__readTable()


    def __readTable(self):
        """
        This reads the crit table from file and creates the dictionary structure
        for further computation.
        """
        #read file content
        with open(self.filename, "r") as fp:
            self.fcont = fp.read()

        print("read {}".format(self.filename))

        #transform csv to json
        self.fcont = self.fcont.strip("\n").split("\n")
        self.crittable = {}
        header = self.fcont[0].split(",")

        for i in range(1, len(self.fcont)):

            if '"' in self.fcont[i]:
                line = splitE(self.fcont[i], ",", '"')

            else:
                line = self.fcont[i].split(",")

            if line[0] not in self.crittable.keys():
                self.crittable[line[0]] = {}

            self.crittable[line[0]][line[1]] = {}

            for j in range(2, len(header)):
                self.crittable[line[0]][line[1]][header[j]] = line[j]

            for crit in self.crittable.keys():

                for roll in self.crittable[crit].keys():

                    if "x" in self.crittable[crit][roll]["mod"]:
                        mr = self.crittable[crit][roll]["mod"].split('x')
                        self.crittable[crit][roll]["mod"] = {"mod":int(mr[0]),
                                                             "rnd":int(mr[1])}

                    else:

                        if type(self.crittable[crit][roll]["mod"]) != type({}):
                            self.crittable[crit][roll]["mod"] = {"mod":int(self.crittable[crit][roll]["mod"]),
                                                             "    rnd":90 * 24 * 60 * 6}

                    if "x" in self.crittable[crit][roll]["mod_attacker"]:
                        mr = self.crittable[crit][roll]["mod_attacker"].split('x')
                        self.crittable[crit][roll]["mod_attacker"] = {"mod_attacker":int(mr[0]),
                                                             "rnd":int(mr[1])}
                    else:

                        if type(self.crittable[crit][roll]["mod_attacker"]) != type({}):
                            self.crittable[crit][roll]["mod_attacker"] = {"mod_attacker":int(self.crittable[crit][roll]["mod_attacker"]),
                                                             "rnd":90 * 24 * 60 * 6}

                    if self.crittable[crit][roll]["alternate"] != "" and type(self.crittable[crit][roll]["alternate"]) == type("") :
                        self.crittable[crit][roll]["alternate"] = switch(self.crittable[crit][roll]["alternate"])

                    else:
                        self.crittable[crit][roll]["alternate"] = {}

                    for elem in ["hits", "hits/rnd", "stunned", "die", "ooo", "parry", "no_parry"]:
                        self.crittable[crit][roll][elem] = int(self.crittable[crit][roll][elem])


    def getCrit(self, roll = 50, crit = "A"):
        """
        This determines the critical hit
        """
        self.crithit = {}
        klist = list(self.crittable[crit].keys())

        for i in range(0, len(klist)):
            klist[i] = int(klist[i])

        klist.sort()
        idx = 0

        while roll > klist[idx]:
            self.crithit = self.crittable[crit][str(klist[idx])].copy()
            idx += 1



class attacktable():
    """
    this class delivers the result from an attack table
    """


    def __init__(self, lang = "en", tabfilename = "data/default/fight/attacks/Broadsword.csv"):
        """
        Constructor
        @param lang configured language: en, de
        @param tavfilename name and path of the attack table csv to read
        """
        self.lang = lang
        self.filename = tabfilename

        self.__makeTable()


    def __makeTable(self):
        """
        Reads table data from csv file and creates the dictionary structures
        """
        with open(self.filename, "r") as fp:
            cont = fp.read()

        cont = cont.strip("\n").split("\n")
        header = cont[0].split(",")
        self.attack = {}

        for i in range(1, len(cont)):
            dummy = cont[i].split(",")
            self.attack[dummy[0].strip(" ")] = {}

            for j in range(1, len(header)):

                if header[j] not in ["pattern", "type"]:
                    self.attack[dummy[0].strip(" ")][header[j].strip(" ")] = int(dummy[j])

                else:
                    self.attack[dummy[0].strip(" ")][header[j].strip(" ")] = dummy[j]


    def getHits(self, roll = 50, AT = "1", AS = "H"):
        """
        Caculates the hitpoints
        @param roll dice roll result on the table
        @param AT armor type to lock up (string)
        @param AS max. attack size: H,L,M,S   - huge, large, medium, small
        """
        attacksize = {"H" : 150,
                    "L" : 135,
                    "M" : 120,
                    "S" : 105
                    }

        if roll > attacksize[AS]:
            roll = attacksize[AS]

        self.crit = ""
        self.crittype = ""
        self.hits = 0

        if roll >= self.attack[AT]["start"]:
            #calc quotient
            q = int((150 - self.attack[AT]["start"]) / (self.attack[AT]["high"] - self.attack[AT]["low"]))
            self.hits = int(self.attack[AT]["low"] + (roll - self.attack[AT]["start"]) / q)

        for c in "ABCDE":
            if roll >= self.attack[AT][c]:
                self.crit = c
        if roll >= self.attack[AT]["first"]:
            self.crittype = self.attack[AT]["type"]

        else:
            p = (roll - self.attack[AT]["start"]) % len(self.attack[AT]["pattern"])
            self.crittype = self.attack[AT]["pattern"][p]



class combat():
    """
    This class handles all combat issues
    - combines comatant groups
    - manages battle rounds, initiatives damage etc.
    - vreates a log file of the battle
    """


    def __init__(self, lang = "en", attacker = [], defender = [], log = "battle.log"):
        """
        Constructor
         @param lang chosen Language
         @param attacker list of dictionaries of "attackers"
         @param defender list of dictionaries of "defenders"
         @param log name an path of the file where to log the battle
        """
        pass
#slash = crittable(critfilename = "/home/mongol/git/rpg-tools/src/data/default/fight/crits/slash_crit.csv")
