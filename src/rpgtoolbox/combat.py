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
__updated__ = "27.11.2020"
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

#                        print("Debug mod -> {}".format(self.crittable[crit][roll]["mod"]))
                        if type(self.crittable[crit][roll]["mod"]) != type({}):
                            self.crittable[crit][roll]["mod"] = {"mod":int(self.crittable[crit][roll]["mod"]),
                                                             "    rnd":90 * 24 * 60 * 6}

                    if "x" in self.crittable[crit][roll]["mod_attacker"]:
                        mr = self.crittable[crit][roll]["mod_attacker"].split('x')
                        self.crittable[crit][roll]["mod_attacker"] = {"mod_attacker":int(mr[0]),
                                                             "rnd":int(mr[1])}
                    else:
#                        print("Debug mod_attacker -> {}".format(self.crittable[crit][roll]["mod_attacker"]))
                        if type(self.crittable[crit][roll]["mod_attacker"]) != type({}):
                            self.crittable[crit][roll]["mod_attacker"] = {"mod_attacker":int(self.crittable[crit][roll]["mod_attacker"]),
                                                             "rnd":90 * 24 * 60 * 6}

                    if self.crittable[crit][roll]["alternate"] != "" and type(self.crittable[crit][roll]["alternate"]) == type("") :
                        self.crittable[crit][roll]["alternate"] = switch(self.crittable[crit][roll]["alternate"])

                    else:
                        self.crittable[crit][roll]["alternate"] = {}

                    for elem in ["hits", "hits/rnd", "stunned", "die", "ooo", "parry", "no_parry"]:
                        self.crittable[crit][roll][elem] = int(self.crittable[crit][roll][elem])

#slash = crittable(critfilename = "/home/mongol/git/rpg-tools/src/data/default/fight/crits/slash_crit.csv")
