#!/usr/bin/env python
'''!
@file handlemagic.py
@package rpgtoolbox.handlemagic

@brief This  module holds helpers handling all spell list/magical issues.

@date (C) 2015-2022
@license GNU V3.0
@author Marcus Schwamberger
@email marcus@lederzeug.de
@version 0.8
'''
__version__ = "0.8"
__updated__ = "06.08.2023"

from pprint import pprint
import json
import os

from rpgtoolbox.confbox import *

from . import logbox as log
from .globaltools import readCSV
from .globaltools import readFile as readNotes
from .rolemaster import DPCostSpells

mycnf = chkCfg()
logger = log.createLogger('magic', 'debug', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = 'handlemagic.log')



class getSpells(object):
    '''!
    @class getSpells
    This class generates an object to get all spell lists into the right context
    for a single character.

    '''


    def __init__(self, datadir = "./data", charprof = "", charrealm = [], charlvl = 1):
        '''!
        This class generates an object to get all spell lists into the right context
        for a single character.
        @param datadir directory where to find the magic directory
        @param charprof profession of the character
        @param charrealm realm(s) of magic
        @param charlvl character's lvl to calculate costs
        @callgraph

        '''
        self.prof = charprof
        self.realm = charrealm
        self.lvl = charlvl
        self.spelllists = {}

        if datadir[-1] == "/":
            datadir = datadir[:-1]

        self.__getAllLists(datadir + "/default/magic/")
        self.__categorizeSLs()

        if type(self.realm) != type([]):
            self.realm = [self.realm]


    def __getAllLists(self, datadir):
        '''!
        Get all spell lists and spell categories from disc
        @param datadir path to the magic directory
        '''
        spellcat = os.listdir(datadir)
        spellcat.sort()
        logger.info("spellcat {}".format(spellcat))

        for i in range(0, len(spellcat)):
            slcat = spellcat[i].replace('_', ' ')
            slcat = slcat.replace("-", ' ')
            self.spelllists[slcat] = {}
            logger.info(f"Spell Cat. : {slcat}")

            try:
                splst = os.listdir(datadir + spellcat[i])
                logger.info("spell lists: {}".format(splst))

            except Exception as error:
                logger.error(" {} -> {}".format(datadir + spellcat[i], error))
                print(error)
                pass

            for j in range(0, len(splst)):

                if splst[j].endswith(".csv"):
                    slist = splst[j].replace('_', ' ')[:-4]
                    self.spelllists[slcat][slist] = {}
                    self.spelllists[slcat][slist]["Special Notes"] = readNotes(datadir + spellcat[i], splst[j][:-4] + ".sn")
                    self.spelllists[slcat][slist]['Spells'] = readCSV(datadir + spellcat[i] + "/" + splst[j])

        logger.debug(f"self.spelllists:\n{json.dumps(self.spelllists,indent=4)}")


    def __categorizeSLs(self):
        '''!
        This private method categorizes spell lists for identifying the developing
        costs for a player character
        @callgraph
        @todo categorize Base lists for non-spell users
        '''
        purespellusers = {"Animist": ["Channeling"],
                          "Cleric": ["Channeling"],
                          "Illusionist": ["Essence"],
                          "Magician": ["Essence"],
                          "Lay Healer": ["Mentalism"],
                          "Mentalist": ["Mentalism"],
                          }
        hybridspellusers = {"Healer": ["Channeling", "Mentalism"],
                            "Mystic": ["Essence", "Mentalism"],
                            "Sorcerer": ["Channeling", "Essence"]
                            }
        semispellusers = {"Paladin": ["Channeling"],
                          "Ranger": ["Channeling"],
                          "Dabbler": ["Essence"],
                          "Monk": ["Essence"],
                          "Bard": ["Mentalism"],
                          "Magent": ["Mentalism"],
                          "Taoist Monk": ["Essence"],
                          "Zen Monk": ["Mentalism"]
                          }
        nonspellusers = {"Fighter":['choice'],
                         "Thief":['choice'],
                         "Rogue":["choice"],
                         "Warrior Monk":['choice'],
                         "Layman":['choice']
                        }
        if type(self.realm) != type([]):
            self.realm = [self.realm]

        for listcat in list(self.spelllists.keys()):
            lcat = listcat.split(' ')
            logger.debug(f"SL categories: {lcat}")

            if len(lcat) > 3:
                profcheck = "{} {}".format(lcat[2], lcat[3])

                if profcheck in purespellusers.keys() or \
                   profcheck in hybridspellusers.keys() or \
                   profcheck in semispellusers.keys():

                    lcat[2] = "{} {}".format(lcat[2], lcat[3])

                del(lcat[3])

            logger.info("lcat: {}".format(lcat))

            if "Lay" in lcat:
                lcat[-2:-1] = [lcat[-2] + " " + lcat[-1]]

            logger.info("prof: {} --> {}".format(self.prof, listcat))

            if lcat[0] == "Base" and self.prof in listcat:
                self.spelllists[listcat]["Category"] = "Own Realm Own Base Lists"
                logger.info("spellist[{}][Category]=Own Realm Own Base Lists".format(listcat))

            elif lcat[0] == "Base"  and self.prof not in listcat:

                if lcat[2] in list(purespellusers.keys()):
                    logger.info("identified pure spell user")

                    if purespellusers[lcat[2]][0] in self.realm:
                        self.spelllists[listcat]["Category"] = "Own Realm Other Base Lists"
                        logger.info(f"spellist[{listcat}][Category]=Own Realm Other Base Lists")

                    else:
                        self.spelllists[listcat]["Category"] = "Other Realm Base Lists"
                        logger.info(f"spellist[{listcat}][Category]=Other Realm  Base Lists")

                elif lcat[2] in list(hybridspellusers.keys()):
                    logger.info("identified hybrid spell user")

                    for item in hybridspellusers[lcat[2]]:

                        if item in self.realm:

                            self.spelllists[listcat]['Category'] = "Own Realm Other Base Lists"
                            break

                        else:
                            self.spelllists[listcat]['Category'] = "Other Realm Base Lists"

                elif lcat[2] in list(semispellusers.keys()):
                    logger.info("identified semi spell user")

                    if semispellusers[lcat[2]] in self.realm:
                        self.spelllists[listcat]["Category"] = "Own Realm Other Base Lists"

                    else:
                        self.spelllists[listcat]["Category"] = "Other Realm Base Lists"

                else:
                    if self.realm not in ["none", "choice"]:

                        if lcat[2] in list(purespellusers.keys()):

                            if purespellusers[lcat[2]] == self.realm:
                                self.spelllists[listcat]['Category'] = "Own Realm Other Base Lists"

                            else:
                                self.spelllists[listcat]['Category'] = "Other Realm Base Lists"

#XXXX go on XXXX
#                elif self.realm in lcat[2] in list(nonspellusers.keys()):
#                    logger.info("categorizeSLs: identified non spell user")

            elif lcat[0] != "Base":

                if lcat[0] in self.realm and lcat[1] == "Open":
                    self.spelllists[listcat]["Category"] = "Own Realm Open Lists"

                elif lcat[0] in self.realm and lcat[1] != "Open":
                    self.spelllists[listcat]["Category"] = "Own Realm Closed Lists"

                elif lcat[0] not in self.realm and lcat[1] == "Open":
                    self.spelllists[listcat]["Category"] = "Other Realm Open Lists"

                elif lcat[0] not in self.realm and lcat[1] != "Open":
                    self.spelllists[listcat]["Category"] = "Other Realm Closed Lists"

        logger.debug("self.spelllists\n{}".format(self.spelllists))



def updateSL(character = {}, datadir = "./data"):
    '''!
    This function updates the character's spell abilities if new spells/spell lists
    are defined.
    @param character a dictionary holding the character's full data.
    @param datadir default data directory

    ----

    @todo this has to be implemented fully:
    - updating costs if implemented one day
    '''
    spellcats = []

    for cat in character["cat"].keys():

        if "Spells - " in cat:
            spellcats.append(cat)

    spellbook = getSpells(datadir = datadir,
                          charprof = character['prof'],
                          charrealm = character["realm"],
                          charlvl = character["lvl"])
    logger.info("Spellbook read")

    for magic in spellbook.spelllists.keys():
        logger.debug(f"working on spell list type: {magic}")

        for spcat in spellcats:

            if spellbook.spelllists[magic]["Category"] in spcat:

                for splist in spellbook.spelllists[magic].keys():
                    logger.debug(f"Spell List: {splist}")
                    ## @bug if a Key Error rises things were not done but the program won't stop either...

                    if splist not in character["cat"][spcat]["Skill"].keys():
                        logger.error(f"{splist} not in character's spell index!")
                        logger.debug(f'character\'s spell index: {character["cat"][spcat]["Skill"].keys()}')
                        character["cat"][spcat]["Skill"][splist] = {"Spells":"",
                                                                   "Special Notes":""}
                        logger.warn(f"{splist} added to character's spell index! - Check for corpse entries.")

                        #----- @todo add a cleaner for character's spell index here
                    if splist != "Category":
                        character["cat"][spcat]["Skill"][splist]["Spells"] = spellbook.spelllists[magic][splist]["Spells"]
                        character["cat"][spcat]["Skill"][splist]["Special Notes"] = spellbook.spelllists[magic][splist]["Special Notes"]

                    else:
                        pass

            if "Category" in  character["cat"][spcat]["Skill"].keys():
                del(character["cat"][spcat]["Skill"]["Category"])
                logger.debug(f"category spell deleted {spcat}")

    logger.info("Spell Lists updated.")



def getSpellNames(slfile = "./data/default/magic/Channeling_Open/Barrier_Law.csv", lvl = 1):
    '''!
    This function reads a spell list file and delivers a list of names and levels up to the requested level
    @param slfile path + file name of the spell list file
    @param lvl the maximum spell level which should be listed
    @retval result list of dictionaries holding all spell information
    '''
    wholelist = readCSV(fname = slfile)
    logger.info(f"getSpellNames: {slfile} read successfully.")
    result = []

    for spell in wholelist:

        if int(spell["Lvl"]) <= lvl:
            result.append(spell)

    return result

