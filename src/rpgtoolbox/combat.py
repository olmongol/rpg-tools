#!/usr/bin/env python
'''!
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
__updated__ = "25.01.2021"
__author__ = "Marcus Schwamberger"

import re
import json
from pprint import pprint

from rpgtoolbox.globaltools import splitExceptBetween as splitE
from rpgtoolbox.globaltools import getCSVNames
from rpgtoolbox.globaltools import sortTupleList
from rpgtoolbox.rpgtools import dice
from rpgtoolbox.lang import attackc, critc

from rpgToolDefinitions.helptools import RMDice

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



def makeCombatant(jcont):
    """!
    This function creates a combatant dictionary out of a character dictionary.
    \param jcont character dictionary
    \retval combatant unified combatant dictionary
    """
    atklvl = {"1":"S",
              "2":"M",
              "3":"L",
              "4":"H"
              }

    combatant = {"name": jcont["name"],
                 "Qu": jcont["Qu"]["total"],
                 "hits": jcont["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"],
                 "PP": jcont["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"],
                 "DB": 3 * jcont["Qu"]["total"] + jcont["armquickpen"],
                 "AT": jcont["AT"],
                 "OB melee":[],
                 "weapon melee":[],
                 "OB missile":[],
                 "weapon missile":[],
                 "ammo":[],
                 "shield":[],
                 "status":{"cur hits":jcont["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"],
                            "mod":0,
                            "temp mod":[],
                            "hits/rnd": 0,
                            "stunned":0,
                            "die":-1,
                            "ooo": 0,
                            "injuries":[],
                            "parry":0,
                            "no_parry":0,
                            "ob_mod":0,
                           },
                 "log": {"gained hits":0,
                          "gained crits": {"A":0,
                                            "B":0,
                                            "C":0,
                                            "D":0,
                                            "E":0
                                            },
                          "crits":{"A":[],
                                    "B":[],
                                    "C":[],
                                    "D":[],
                                    "E":[]
                                    },
                          "kill":[],
                          "spells":{},
                         },
                 "size":"M"

                 }
    # determine weaponless combat skills:
    if ["Brawling", "S", jcont["cat"]["Special Attacks"]["Skill"]["Brawling"]["rank"]] > 0:
        combatant["OB melee"].append(["Brawling", "S", jcont["cat"]["Special Attacks"]["Skill"]["Brawling"]["total bonus"]])
        combatant["OB weapon"].append(["bare hands", "data/default/fight/attacks/Brawling.csv", "data/default/fight/brawling_crit.csv"])

    for c in ["Martial Arts - Striking", "Martial Arts - Sweeps"]:
        dummy = []

        for s in jcont["cat"][c]["Skill"].keys():

            if s not in ["Progression"]:

                if jcont["cat"][c]["Skill"][s]["rank"] > 0:
                    dummy.append(s)

                    if s[-1] in atklvl.keys():
                        dummy.append(atklvl[s[-1]])

                    else:
                        dummy.append(atklvl["1"])

                    dummy.append(jcont["cat"][c]["Skill"][s]["total bonus"])

    if combatant["DB"] < 0:
        combatant["DB"] = 0

    return combatant



def rollInitative(Qu = 0, mod = 0):
    """!
    This rolls a initiative based on Quickness and additional modifiers
    @param Qu Quickness bonus
    @param mod modifier
    @retval roll initiative result
    """
    roll = dice(19)[0] + 1 + Qu + mod
    return roll



def switch(mystr):
    '''!
    This makes a dictionary with int values from the "modifications" column
    @param mystr the cell entry (string)
    @retval result dictionary with "mod" and "rnd" (both int)
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



def createCombatList(filename):
    """!
    This creates a list of combatants for @class combat from a CSV file (NSCs,
    Monster etc.) or JSON (Character/Group file)
    @todo has to be implemented
    """
    pass



class crittable():
    """
    This Class delivers results from crit tables to a combatant.
    """


    def __init__(self, critfilename = "./data/default/fight/crits/puncture_crit.csv", lang = "en"):
        """!
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
                                                                 "rnd":90 * 24 * 60 * 6}

                    if "x" in self.crittable[crit][roll]["mod_attacker"]:
                        mr = self.crittable[crit][roll]["mod_attacker"].split('x')
                        self.crittable[crit][roll]["mod_attacker"] = {"mod_attacker":int(mr[0]),
                                                             "rnd":int(mr[1])}
                    else:

                        if type(self.crittable[crit][roll]["mod_attacker"]) != type({}):
                            self.crittable[crit][roll]["mod_attacker"] = {"mod_attacker":int(self.crittable[crit][roll]["mod_attacker"]),
                                                             "rnd":90 * 24 * 60 * 6}

                    if self.crittable[crit][roll]["alternate"] != "" and type(self.crittable[crit][roll]["alternate"]) == type(""):
                        self.crittable[crit][roll]["alternate"] = switch(self.crittable[crit][roll]["alternate"])

                    elif self.crittable[crit][roll]["alternate"] == "":
                        self.crittable[crit][roll]["alternate"] = {}

                    for elem in ["hits", "hits/rnd", "stunned", "die", "ooo", "parry", "no_parry"]:
                        #debug
                        #print("{} : {} - {} ==> {}".format(crit, roll, elem, self.crittable[crit][roll][elem]))
                        self.crittable[crit][roll][elem] = int(self.crittable[crit][roll][elem])


    def getCrit(self, roll = 50, crit = "A", weapontype = "normal"):
        """
        This determines the critical hit

        """
        self.crithit = {}
        if crit in self.crittable.keys():
            klist = list(self.crittable[crit].keys())

            for i in range(0, len(klist)):
                klist[i] = int(klist[i])

            klist.sort()

            for idx in range(0, len(klist)):
                if roll <= klist[idx]:
                    self.crithit = self.crittable[crit][str(klist[idx])].copy()
                    break

        elif weapontype in self.crittable.keys():
            klist = list(self.crittable[weapontype].keys())

            for i in range(0, len(klist)):
                klist[i] = int(klist[i])

            klist.sort()

            for idx in range(0, len(klist)):
                if roll <= klist[idx]:
                    self.crithit = self.crittable[weapontype][str(klist[idx])].copy()
                    break

        self.showResult()


    def showResult(self):
        """!
        This just prints out the result to stdout
        """
        pprint(self.crithit)



class attacktable():
    """
    this class delivers the result from an attack table
    """


    def __init__(self, tabfilename = "data/default/fight/attacks/Broadsword.csv", lang = "en", override = ""):
        """!
        Constructor
        @param tavfilename name and path of the attack table csv to read
        @param lang configured language: en, de
        """
        self.filename = tabfilename
        self.lang = lang
        self.override = override
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

                if header[j] not in ["pattern", "type"] and dummy[j] != "":
                    self.attack[dummy[0].strip(" ")][header[j].strip(" ")] = int(dummy[j])

                elif self.override:
                    self.attack[dummy[0].strip(" ")][header[j].strip(" ")] = self.override

                else:
                    self.attack[dummy[0].strip(" ")][header[j].strip(" ")] = dummy[j]


    def showResult(self):
        """!
        This prints out the result simply to stdout
        """
        if self.crit == "":
            print("Hits: {}".format(self.hits))
        else:
            print("Hits: {}\nCrit: {}\nType:{}".format(self.hits, self.crit, self.crittype))


    def getHits(self, roll = 50, AT = "1", AS = "H"):
        """!
        Caculates the hitpoints
        @param roll dice roll result on the table
        @param AT armor type to lock up (string)
        @param AS max. attack size: H,L,M,S   - huge, large, medium, small
        """
        attacksize = {"H": 150,
                    "L": 135,
                    "M": 120,
                    "S": 105
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
            if self.attack[AT]["pattern"] != self.attack[AT]["pattern"].lower():
                self.crittype = self.attack[AT]["pattern"][p]
            else:
                self.crittype = self.attack[AT]["pattern"]

        # tables with tiny crits
        for c in ["TA", "TB", "TC", "TD", "TE"]:
            if c in self.attack[AT].keys():
                if  self.attack[AT]["A"] > roll >= self.attack[AT][c]:
                    self.crit = c.strip("T")
                    self.crittype = "T"

        for c in ["F", "G", "H", "I"]:
            if c in self.attack[AT].keys():
                if roll >= self.attack[AT][c]:
                    self.crit = c

        self.showResult()



class combat():
    """!
    This class handles all combat issues
    - combines comatant groups
    - manages battle rounds, initiatives damage etc.
    - vreates a log file of the battle
    """


    def __init__(self, lang = "en", log = "battle.log"):
        """
        Constructor
         @param lang chosen Language
         @param log name an path of the file where to log the battle
        """
        self.attacklog = log
        self.lang = lang
        self.battle = {"initiative": [],
                       "charparty": [],
                       "enemies": []}


    def addCombatants(self, filename, grp = "charparty"):
        """!
        This creates/fills the lists of combatants:
        -# charparty: characters and all who fight with them
        -# enemies: monster, nscs and all who fight against the characters

        @param filename file to load: this might be a JSON for single character
                        file or group of characters or a CSV for NSCs, monsters
                        etc.
        @param grp the group to add data to:
                - charparty: all who fight with the characters
                - enemies: all who fight against the characters

        """
        if ".json" == filename.lower()[-5:]:
            with open(filename, "r") as fp:
                jcont = json.load(fp)

            if type(jcont) == type([]):
                # character group
                pass

            elif type(jcont) == type({}):
                # single character file
                pass

        elif ".csv" == filename.lower()[-4:]:
            pass
        else:
            print("Error: {] has the wrong file type!".format(filename))

#slash = crittable(critfilename = "/home/mongol/git/rpg-tools/src/data/default/fight/crits/slash_crit.csv")
