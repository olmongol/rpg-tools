#!/usr/bin/env python
'''!
@file /home/mongol/git/rpg-tools/src/rpgtoolbox/combat.py
@package rpgtoolbox.combat
@brief Rolemaster combat module

This module holds everything needed to handle melee/ranged/magical combat

@date (c) 2020
@license GNU V3.0
@author Marcus Schwamberger
@email marcus@lederzeug.de
@version 0.1
'''
__version__ = "0.1"
__updated__ = "03.10.2022"
__me__ = "rpgtoolbox.combat"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__license__ = "GPL V3"

import re
import json
import os
from pprint import pprint

from rpgtoolbox.globaltools import splitExceptBetween as splitE
from rpgtoolbox.globaltools import getCSVNames
from rpgtoolbox.globaltools import sortTupleList
from rpgtoolbox.rpgtools import dice
from rpgtoolbox.lang import attackc, critc
from rpgtoolbox.globaltools import *
from rpgToolDefinitions.helptools import RMDice
from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import *

mycnf = chkCfg()
logger = log.createLogger('combat', 'debug', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = "combat.log")



def getAttackSpec(shortterm = "", longterm = "", stattable = "data/default/fight/weapon_stats.csv"):
    '''!
    This function checks out specific weapon/attack data and returns all needed additional
    information
    @param shortterm of the weapon/attack: e.g., 'bs' for 'Broadsword'
    @param longterm of the weapon/attack
    @param stattable CSV file where to look up the additional data

    ----
    @todo has to be implemented fully.

    '''
    pass



def sortIniti(cl = []):
    """!
    Sorts list of tuples decending by the first tuple entry.
    @param cl list of tuple
    @return sorted tuple list
    """
    return sorted(cl, key = lambda x: x[0], reverse = True)



def getWeaponTab(filename = "data/default/fight/weapons_sc.json"):
    """!
    Reads weapon/attack data table from json file
    """
    with open(os.path.join(os.getcwd(), filename), "r") as fp:
        content = json.load(fp)
    logger.debug(f'{filename} loaded.')
    return content



def convertNSC(filename = "data/default/nscs/default.csv"):
    """!
    Converts CSV NSCs/monsters into combatants
    """

    weapons = getWeaponTab()
    r = r"([1-9][0-9]{1,2})([HLMST]*)([A-Za-z][a-z])"
    check = re.compile(r)

    with open(filename, "r") as fp:
        cont = fp.read()

    logger.debug(r"{filename} loaded.")
    cont = cont.strip("\n").split("\n")
    header = splitE(cont[0])
    nsclist = []

    for l in range(1, len(cont)):
        dummy = splitE(cont[l])
        monster = {'log': {'crits': {'A': [],
                                      'B': [],
                                      'C': [],
                                      'D': [],
                                      'E': []
                                      },
                            'gained crits': {'A': 0,
                                             'B': 0,
                                             'C': 0,
                                             'D': 0,
                                             'E': 0},
                            'gained hits': 0,
                            'kill': [],
                            'spells': {}
                            },
                    'status': {'cur hits': 61,
                               'die':-1,
                               'hits/rnd': 0,
                               'injuries': [],
                               'mod': 0,
                               'no_parry': 0,
                               'ob_mod': 0,
                               'ooo': 0,
                               'parry': 0,
                               'stunned': 0,
                               'temp mod': []
                               },
                    'ammo':[],
                    'shield':[],
                    'weapon melee':[],
                    'weapon missile':[],
                    }
        for i in range(0, len(header)):

            #check for different OBs
            if header[i] in ["OB melee", "OB missile"]:

                if dummy[i] != "0xx":
                    dummy[i] = dummy[i].strip("\t ").split("/")

                    #divide data into OB (value), size, and attack/weapon type
                    for j in range(0, len(dummy[i])):
                        passed = check.match(dummy[i][j])

                        if passed:
                            dummy[i][j] = ["{}: {}".format(weapons[passed.groups()[2]]["name"],
                                                        weapons[passed.groups()[2]]["table"]),
                                                        passed.groups()[0], passed.groups()[1]]
                            if passed.groups()[1] == "":
                                dummy[i][j][2] = "H"

                else:
                    dummy[i] = []

            monster[header[i]] = dummy[i]

        nsclist.append(monster)

    logger.info(f'NSCs successfully transformed.')
    return nsclist



def makeCombatant(achar = {}):
    """!
    This function creates a combatant dictionary out of a character dictionary.
    @param achar character dictionary
    @retval combatant unified combatant dictionary
    """
    atklvl = {"1":"S",
              "2":"M",
              "3":"L",
              "4":"H"
              }

    combatant = {"name": achar["name"],
                 "Qu": achar["Qu"]["total"],
                 "hits": achar["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"],
                 "PP": achar["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"],
                 "DB": 3 * achar["Qu"]["total"] + achar["armquickpen"],
                 "AT": achar["AT"],
                 "OB melee":[],
                 "weapon melee":[],
                 "OB missile":[],
                 "weapon missile":[],
                 "ammo":[],
                 "shield":[],
                 "status":{"cur hits":achar["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"],
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

    # defermine fighting skills

    for cat in achar["cat"].keys():
        combatant["lvl"] = achar["lvl"]
        if "Weapon" in cat or "Martial" in cat or "Directed" in cat or "Special Attacks" == cat:

            for skill in achar["cat"][cat]["Skill"].keys():

                if achar["cat"][cat]["Skill"][skill] not in ["Standard", "Combined"]:

                    if skill not in ["Striking Degree 1", "Striking Degree 3", "Striking Degree 3",
                                     "Sweeps Degree 1", "Sweeps Degree 3", "Sweeps Degree 3",
                                     "Boxing", "Wrestling"]:
                        size = "H"
                    else:
                        if "3" in skill:
                            size = "L"
                        elif "2" in skill:
                            size = "M"
                        else:
                            size = "S"

                    if achar["cat"][cat]["Skill"][skill]["rank"] > 0:
                        dummy = ["{}: {}".format(cat, skill), achar["cat"][cat]["Skill"][skill]["total bonus"], size]

                        if cat in ["Directed Spells", "Weapon - Missile", "Weapon - Missile Arillery", "Weapon - Thrown"]:
                            combatant["OB missile"].append(dummy)
                        else:
                            combatant["OB melee"].append(dummy)

    if combatant["DB"] < 0:
        combatant["DB"] = 0

    logger.debug(f"{achar['name']} tranformed.")
    return combatant



def addStatusParam(cmbtlist = []):
    """!
    This function adds vitial stats to combattant list
    @param cmbtlist list of combatants (dictionatries)
    @retval result new list with modified elements/comatants
    """

    result = []

    for elem in cmbtlist:
        logger.debug("add {elem['name']} to list of combatants. ")
        if "status" not in elem.keys():
            elem["status"] = {"cur hits":elem["hits"],
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
                           }

        if "log" not in elem.keys():
            elem["log"] = {"gained hits":0,
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
                          }

        result.append(elem)

    logger.debug("successfully added.")
    return result



def rollInitative(Qu = 0, mod = 0):
    """!
    This rolls a initiative based on Quickness and additional modifiers
    @param Qu Quickness bonus
    @param mod modifier
    @retval roll initiative result
    """
    roll = dice(10)[0] + 1 + Qu + mod
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

    logger.debug(f"result:\n{json.dumps(result)}")
    return result



def createCombatList(comlist = []):
    """!
    This adds a status and combat log section to combatants in a  list.

    @param comlist a list of combatants (dictionaries)
    @return modified list

    ----
    @todo has to be implemented fully
    """
    #r = r'([1-9][0-9]{1,2})([HLMST]*)([A-Za-z][a-z])'
    #checkob = re.compile(r)
    #clist = ["lvl", "hits", "AT", "OB", "DB", "Qu", "name", "type", "ooo", "status", "die", "parry", "no_parry", "mod", "hits/rnd", "weapon", "PP", "spell lvl"]
    status = {"ooo":0,
              "hits/rnd":0,
              "mod":[{"mod":0, "rnd":0}],
              "mod_total":0,
              "parry":0,
              "no_parry":0,
              "stunned":0,
              "die":-1,
              "log":[]
              }
    comlog = {"gained": {"hits":0,
                        "crits": {"A":0,
                                 "B":0,
                                 "C":0,
                                 "D":0,
                                 "E":0,
                                 "T":0
                                 },
                        },
             "caused":{"crits": [],
                       "lvls": [],
                       "kills": []
                      },
             "spells": []
             }

    for i in range(0, len(comlist)):
        comlist[i]["status"] = status.copy()

        if comlist[i]["hits"]:
            comlist[i]["status"]["hits"] = int(comlist[i]["hits"])

        else:
            comlist[i]["status"]["hits"] = 0

        if "PP" in comlist[i].keys() and comlist[i]["PP"]:
            comlist[i]["status"]["PP"] = int(comlist[i]["PP"])
        else:
            comlist[i]["status"]["pp"] = 0

        comlist[i]["comlog"] = comlog.copy()
        comlist[i]["switch"] = 0

    logger.debug("combat list type convert successfully done.")
    return comlist



class crittable():
    """!
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
        logger.debug(f"read file: {self.filename}")


    def __readTable(self):
        """
        This reads the crit table from file and creates the dictionary structure
        for further computation.
        """
        #read file content
        with open(self.filename, "r") as fp:
            self.fcont = fp.read()

        logger.info(f"read file: {self.filename}")
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

        logger.info("successfully converted from csv to dictionary")


    def getCrit(self, roll = 50, crit = "A", weapontype = "normal"):
        """
        This determines the critical hit

        @param roll result of the dice roll
        @param crit level of critical damage: A, B, C, D, E, T
        @param weapontype type of weapon: normal, magic, Mithril, holy
        """
        self.crithit = {}
        logger.debug("self.crithit initalized.")

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

        logger.debug(f"result critical hit:\n{json.dumps(self.crithit)}")
        self.showResult()


    def showResult(self):
        """!
        This just prints out the result to stdout
        """
        print("Result")
        pprint(self.crithit)



class attacktable():
    """!
    this class delivers the result from an attack table
    """


    def __init__(self, tabfilename = "data/default/fight/attacks/Broadsword.csv", lang = "en", override = ""):
        """!
        Constructor
        @param tabfilename name and path of the attack table csv to read
        @param lang configured language: en, de
        @param override
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



class fumbletable():
    """!
    This class creates a combat fumble table for all types of weapon and non-weapon
    fumbles.
    """


    def __init__(self, tablefilename = "data/default/fight/fumble/combat_fumble.csv"):
        """!
        Constructor
        @param tablefilename path+filename of the fumble table to read
        """
        self.tablename = tablefilename


    def __getTable(self):
        """!
        This reads the fumble table from file an transfers it to the internal data structure

        ----
        @todo this has to be implemented fully
        """
        pass


    def getResult(self, fumbletype = "1he", roll = 50):
        """!
        This method delivers the result from the fumble table by fumble type and
        fumble roll.

        @param fumbletype type of the fumble
        @param roll fumble roll result

        ----
        @todo has to be fully implemented
        """
        pass



class combat():
    """!
    This class handles all combat issues
    - combines comatant groups
    - manages battle rounds, initiatives damage etc.
    - vreates a log file of the battle
    @deprecated
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
