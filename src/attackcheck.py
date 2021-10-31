#!/usr/bin/env python3
'''!
\file attackcheck.py
\package attackcheck
\brief Thia program can be used to  get the results of  attack and critical tables

This mangages a fight between a player character group and a group of monsters or
other opponents.

\date (c) 2021
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.5
'''
__version__ = "0.5"
__updated__ = "31.10.2021"
__author__ = "Marcus Schwamberger"

import os
import json
from tkinter import filedialog
from tkinter.ttk import Combobox
from pprint import pformat
from copy import deepcopy
from random import randint
from rpgtoolbox.combat import *
#from rpgtoolbox.rpgtools import dice
from rpgToolDefinitions.helptools import RMDice as Dice
from rpgToolDefinitions.magic import magicpath
from gui.window import *
from rpgtoolbox import logbox as log
from rpgtoolbox.globaltools import *
from rpgtoolbox.handlemagic import getSpellNames
from PIL import Image, ImageTk
logger = log.createLogger('AT-Window', 'debug', '1 MB', 1, './', logfile = "attackcheck.log")



class atWin(blankWindow):
    """!
    This class generates a window where you can look up your attack results.
    Results of dice rolls may be entered or a roll may be done by clicking a
    button.
    """


    def __init__(self, lang = "en", datadir = "./data/default"):
        """!
        Constructor
        \param lang selected output language
        \param datadir configured default datadir
        """
        self.lang = lang
        self.datadir = datadir
        self.attacktbls = {}
        self.crittbls = {}
        self.attackers = ["Egon"]
        self.defenders = ["Anton"]
        self.combatants = []
        self.combatround = 0
        self.curphase = 0
        self.hits = 0
        self.damachoice = [labels["with"][self.lang], labels["without"][self.lang]]
        self.initroll = False
        self.initlist = []
        self.__partypath = None
        self.partygrp = None
        self.__enemypath = None
        self.enemygrp = None
        self.weapontab = getWeaponTab()
        self.curr_attacker = 0
        self.curr_defender = 0
        self.defaultnscimg = datadir + "/pics/default.jpg"
        self.fmask = [txtwin['grp_files'][self.lang],
                     txtwin['enemygrp_files'][self.lang],
                     txtwin['all_files'][self.lang]]
        self.fmaskc = [txtwin['grp_files'][self.lang],
                     txtwin['all_files'][self.lang]]
        self.fmaske = [txtwin['enemygrp_files'][self.lang],
                     txtwin['all_files'][self.lang]]
        # read all attack tables
        for table in os.listdir("{}/fight/attacks".format(self.datadir)):
            if table[-4:] == ".csv" and table[-5:] != "-.csv":
                self.attacktbls[table[:-4]] = attacktable("{}/fight/attacks/{}".format(self.datadir, table))

        # read all crit tables
        for table in os.listdir("{}/fight/crits".format(self.datadir)):
            if table[-4:] == ".csv" and table[-5:] != "-.csv":
                self.crittbls[table[:-9]] = crittable("{}/fight/crits/{}".format(self.datadir, table))

        #window components
        blankWindow.__init__(self, self.lang)
        self.window.title("Combat  Module")
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addHelpMenu(self):
        """
        This methods defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)
        logger.debug("__addHelpMenu: help menu build")


    def __addFileMenu(self):
        '''!
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open_party'],
                                  command = self.openParty)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open_enemy'],
                                  command = self.openEnemies)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)
        logger.debug("__addHelpMenu: file menu build")


    def __addEditMenu(self):
        '''!
        This adds an Edit menu to the winwos menu bar:
        - add enemies to the opponent's list
        - remove enemies from the opponent's list

        ----
        @todo the add/remove functions of single NSCS/SCS/Monsters has to be fully implemented
        '''
        self.editmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu["menu_edit"][self.lang],
                              menu = self.editmenu)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_add_enemy"],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_rem_enemy"],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["init"],
                                  command = self.__rollInit)
        self.editmenu.add_command(label = submenu["edit"][self.lang]["history"],
                                  command = self.notdoneyet)


    def openParty(self):
        '''!
        This method reads a character party group file to self.partygrp
        '''
        self.__partypath = askopenfilename(filetypes = self.fmaskc, initialdir = os.getcwd(), defaultextension = ".json")
        logger.debug(f"openParty: chosen group file {self.__partypath}")
        try:
            with open(self.__partypath, "r") as fp:
                ##@var self.__fullparty
                # This is holding the full party data
                self.__fullparty = json.load(fp)
            logger.info(f"openParty: {self.__partypath} was read")

            if type(self.__fullparty) == type({}):
                self.__fullparty = [self.__fullparty]
            self.__prepareChars()

        except Exception as error:
            logger.error(f"openParty: {error}")
            self.message = messageWindow()
            self.message.showinfo(f"openParty: {error}", "ERROR")

        self.__prepareChars()


    def openEnemies(self):
        '''!
        This opens an enemy party to fight against
        '''
        self.__enemypath = askopenfilename(filetypes = self.fmaske, defaultextension = "*.csv", initialdir = os.getcwd())
        logger.debug(f"openEnemies: chosen enemies group file {self.__enemypath}")

        if self.__enemypath[-4:].lower() == ".csv":
            self.enemygrp = readCSV(self.__enemypath)
        else:
            logger.error("penEnemies: wrong file format! must be CSV")
            self.message("openEnemies: wrong file format: must be CSV")

        self.__prepareNSCs()


    def __prepareNSCs(self, mode = "auto"):
        '''!
        this prepares the read enemy list (of dicts) to 'battle format' - that
        means it splits the OBs into lists.
        @param mode this option handles the modus operandi:
               - auto: the number of opponents is randomly chosen by the 'enc' column
               - first: takes the first number of 'enc' range
               - last: takes the last number of 'enc' range

        ----
        @todo - append NSCs/Monsters if the enc >1
              - immunity list
              - weakness list
        '''
        size = "H"
        self.enemygrp = createCombatList(self.enemygrp)
        apendix = []

        for i in range(0, len(self.enemygrp)):

            enc = self.enemygrp[i]["enc"].split("-")

            for j in range(0, len(enc)):
                enc[j] = int(enc[j])

            if mode.lower() == "first":
                enc[1] = enc[0]

            elif mode.lower() == "last":
                enc[0] = enc[1]

            self.enemygrp[i]["enc"] = randint(enc[0], enc[1])

            #generate OB lists

            melee = self.enemygrp[i]["OB melee"].split("/")

            for j in range(0, len(melee)):

                if type(melee[j]) == type(""):
                    melee[j] = melee[j].split(" ")

                    if len(melee[j]) == 2:
                        melee[j][-1], melee[j][0] = melee[j][0], melee[j][-1]
                        melee[j].append("H")

                    elif len(melee[j]) == 3:
                        melee[j][2], melee[j][0], melee[j][1] = melee[j][1], melee[j][0], melee[j][2]

                if len(melee[j]) == 2:
                    melee[j].insert(1, size)

                melee[j][0] = self.weapontab[melee[j][0]]['name']

            self.enemygrp[i]["OB melee"] = melee

            missile = self.enemygrp[i]["OB missile"].split("/")

            for j in range(0, len(missile)):
                missile[j] = missile[j].split(" ")

                if len(missile[j]) > 1:
                    missile[j][-1], missile[j][0] = missile[j][0], missile[j][-1]

                if len(missile[j]) == 2:
                    missile[j].insert(1, size)

                missile[j][0] = self.weapontab[missile[j][0]]["name"]

            self.enemygrp[i]["OB missile"] = missile

            if "weapon type" in self.enemygrp[i].keys():
                ##@var wt
                # list of two lists: [0] contains melee weapon types and [1] missile weapon types
                # they all will be stored in self.enemygrp
                wt = self.enemygrp[i]["weapon type"].split("//")

            else:
                wt = "normal"

            for j in range(0, len(wt)):
                if "/" in wt[j]:
                    wt[j] = wt[j].split("/")

            # xxxx spell lists path/sl:lvl;path/sl:lvl[;...]

            # spells need to have the format: "Channeling Open/Barrier Law:5;<next list>"
            if "spells" in self.enemygrp[i].keys():
                spelldummy = self.enemygrp[i]["spells"].split(";")
                spellists = {}

                if spelldummy != [""]:

                    for s in range(0, len(spelldummy)):
                        spelldummy[s] = spelldummy[s].split(":")
                        spelldummy[s][0] = spelldummy[s][0].replace("\\", "/")
                        spelldummy[s][1] = int(spelldummy[s][1])

                        if magicpath in spelldummy[s][0]:
                            pathadd = ""

                        else:
                            pathadd = magicpath

                        spellists[spelldummy[s][0].split("/")[-1]] = {"spells": getSpellNames(slfile = pathadd + spelldummy[s][0].replace(" ", "_") + ".csv", lvl = spelldummy[s][1]),
                                                                      "skill": spelldummy[s][1]
                                                                      }
                        logger.info(f"__prepareNSCs: {pathadd + spelldummy[s][0].replace(' ', '_') + '.csv'} read")
                        #logger.debug(f"__prepareNSCs: spellists[{spelldummy[s][0].split('/')[-1]}] = \n{pformat(spellists[spelldummy[s][0].split('/')[-1]])}")

                    self.enemygrp[i]["spells"] = deepcopy(spellists)

                else:
                    self.enemygrp[i]["spells"] = []

            else:
                self.enemygrp[i]["spells"] = []

            self.enemygrp[i]["init"] = 0

            # add
            if self.enemygrp[i]["enc"] > 1:
                for j in range(1, self.enemygrp[i]["enc"]):
                    apdummy = deepcopy(self.enemygrp[i])
                    apdummy["name"] += f"_{j}"
                    apendix.append(apdummy)

        self.enemygrp += apendix
        self.initlist += self.enemygrp
        self.attackers = []

        for elem in self.initlist:
            self.attackers.append(elem["name"])

        self.defenders = deepcopy(self.attackers)
        self.__selectAttacker.set(self.attackers[0])
        self.__selectDefender.set(self.defenders[-1])
        self.__updDefCombo()
        self.__updtAttckCombo()
        self.__chgImg(attackerpic = "", defenderpic = self.enemygrp[0]["piclink"])
        logger.info("__prepareNSCs: enemygrp set")
        logger.debug(f"__prepareNSCs: \n{pformat(self.enemygrp)}")


    def __prepareChars(self):
        '''!
        This method reduces character data to combatant data

        ----
        @todo learned spell casting lists and bonusses have to be selected and added
        '''
        self.partygrp = []
        cindex = ["player", "name", "DB", "DB mod", "OB melee", "OB missile", "hits", "PP",
                "AT", "lvl", "spells", "init", "piclink"]

        melee = ["Martial Arts - Striking", "Martial Arts - Sweeps", "Weapon - 1-H Concussion",
                "Weapon - 1-H Edged", "Weapon - 2-Handed", "Weapon - Pole Arms",
                "Weapon - 1-H Concussion", "Weapon - 1-H Edged", "Weapon - 2-Handed", "Special Attacks"]
        missile = ["Weapon - Missile", "Weapon - Missile Artillery", "Weapon - Thrown", "Directed Spells"]
        spellcats = ["Spells - Arcane Open Lists",
                    "Spells - Other Realm Base Lists",
                    "Spells - Other Realm Closed Lists",
                    "Spells - Other Realm Open Lists",
                    "Spells - Own Realm Closed Lists",
                    "Spells - Own Realm Open Lists",
                    "Spells - Own Realm Other Base Lists",
                    "Spells - Own Realm Own Base Lists"
                   ]  # Skill -> SPList -> rank>0 -> append "Spells"[i]["Lvl"] <= "rank"; "total bonus"
        spnogo = ["Progression", "Stats"]
        for char in self.__fullparty:
            dummy = dict.fromkeys(cindex, 0)

            for stat in cindex:

                if stat in char.keys():
                    dummy[stat] = char[stat]

            dummy["DB"] = 3 * char["Qu"]["total"] + char["armquickpen"]

            if char["cat"]["Special Defenses"]["Skill"]["Adrenal Defense"]["total bonus"] > 0:
                dummy["DB"] += char["cat"]["Special Defenses"]["Skill"]["Adrenal Defense"]["total bonus"]

            if dummy["DB"] < 0:
                dummy["DB"] = 0

            dummy["Qu"] = char["Qu"]["total"]
            dummy["init"] = 0
            dummy["hits"] = char["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"]
            dummy["PP"] = char["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"]
            dummy["OB melee"] = []
            dummy["OB missile"] = []
            dummy["spell"] = []
            dummy["weapon type"] = [[], []]

            for m in melee:

                for skill in char["cat"][m]["Skill"].keys():

                    if skill not in ["Progression", "Stats"] and "+" not in skill:
                        addon = [skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"]

                        if addon not in dummy["OB melee"]:
                            dummy["OB melee"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"])

            #sort melee weapons highest ob first
            dummy["OB melee"] = sorted(dummy["OB melee"], key = lambda k: k[1], reverse = True)

            for m in missile:

                for skill in char["cat"][m]["Skill"].keys():

                    if skill not in ["Progression", "Stats"] and "+" not in skill and [skill, char["cat"][m]["Skill"][skill]["total bonus"]] not in dummy["OB missile"]:
                        dummy["OB missile"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"]])

            # sort missle weapons highest ob first
            dummy["OB missile"] = sorted(dummy["OB missile"], key = lambda k: k[1], reverse = True)
            dummy["weapon type"][0] = ["normal"] * len(dummy["OB melee"])
            dummy["weapon type"][1] = ["normal"] * len(dummy["OB missile"])

            self.partygrp.append(dummy)
            self.__chgImg(attackerpic = self.partygrp[0]["piclink"], defenderpic = "")

        self.partygrp = createCombatList(self.partygrp)
        self.initlist += self.partygrp
        logger.info("__prepareChars: partygrp set")
        logger.debug(f"__prepareChars: \n{pformat(self.partygrp)}")
        self.attackers = []

        for elem in self.initlist:
            self.attackers.append(elem["name"])

        self.__selectAttacker.set(self.initlist[0]["name"])
        self.__selectDefender.set(self.initlist[-1]["name"])
        self.defenders = deepcopy(self.attackers)
        self.__updtAttckCombo()
        self.__updDefCombo()


    def sortList(self, mylist = [], key = 1):
        '''!
        Sorts reversely a list of lists/dictionaries by an index key of the elements.
        @param mylist list to be sorted
        @param key key/index for sorting
        '''
        result = sorted(mylist, key = lambda k: k[key], reverse = True)
        return result


    def __quit(self):
        '''!
        This method closes the window
        '''
        self.window.destroy()


    def __rollInit(self):
        '''!
        This rolls the initiative

        '''

        # roll initiative for self.initlist
        for i in range(0, len(self.initlist)):
            self.initlist[i]["init"] = int(self.initlist[i]['Qu']) + randint(1, 10)

        # sort self.initlist reversely
        self.initlist = sorted(self.initlist, key = lambda k: k["init"], reverse = True)
        self.attackers = []

        for elem in self.initlist:

            if elem['name'] not in self.attackers:
                self.attackers.append(elem["name"])

        self.defenders = deepcopy(self.attackers)
        self.combatround += 1
        self.initroll = True
        self.__updtAttckCombo(None)
        self.__updDefCombo(None)


    def __rollAttack(self):
        '''!
        This does an attack role using RM rules
        '''
        result, self.umr = Dice(rules = "RM")
        self.__atroll.set(result[0])


    def __rollCrit(self):
        """!
        This method roles the dice for critical hits.
        """
        if self.__selectCrit.get() in ["large", "superlarge"]:
            result, self.umr = Dice(rules = "RM")

        else:
            result, self.umr = Dice(rules = "")
        self.__critroll.set(result[0])


    def __chgImg(self, attackerpic = "./data/default/pics/default.jpg", defenderpic = "./data/default/pics/default.jpg"):
        '''!
        This method changes attacker's and defender's images when newly selected.

        @param attackerpic path & name of the picture of the attacker (will be downsized to 90x90 px)
        @param defenderpic path & name of the picture of the defender (will be downsized to 90x90 px)
        '''
        if attackerpic:
            self.picattacker = Image.open(attackerpic).resize((90, 90), Image.ANTIALIAS)
            self.picattacker = ImageTk.PhotoImage(self.picattacker)
            self.atcanvas.create_image((90, 90), image = self.picattacker, anchor = "se")
        if defenderpic:
            self.picdefender = Image.open(defenderpic).resize((90, 90), Image.ANTIALIAS)
            self.picdefender = ImageTk.PhotoImage(self.picdefender)
            self.defcanvas.create_image((90, 90), image = self.picdefender, anchor = "se")


    def __findCombatant(self, name = "Egon", chklist = ["Egon"], result = "value"):
        """!
        this method returns the combatant data for the given name
        @param name of the combatant to search for
        @param chklist list of dicts to search thru
        @param result type of return: "index", "value"
        @return the conbatant's data dictionary
        """
        pos = -1
        for elem in chklist:
            pos += 1
            if name == elem["name"]:
                if result != "index":
                    return elem
                else:
                    return pos

        return {"name":"Egon"}


    def __applyDamage(self, event = None):
        '''!
        This method applies all modifications by a hit/critical hit to a combatant.

        ----
        @todo has to be fully implemented

        '''
        self.curr_defender = self.__selectDefender.get()
        self.curr_attacker = self.__selectAttacker.get()
        pos = self.__findCombatant(name = self.curr_defender, chklist = self.initlist, result = "index")
        posa = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist, result = "index")
        crit = self.__critType.get()
        self.initlist[pos]["status"]["hits"] -= self.hits

        if crit in ["A", "B", "C", "D", "E", "T"]:
            result = self.crittbls[self.__selectCrit.get()].crithit
            print("Apply Damage:")
            pprint(self.crittbls[self.__selectCrit.get()].crithit)

            if  result["alternate"] != {} and self.__woItem.get() == labels["without"][self.lang]:

                for key in result["alternate"].keys():
                    result[key] = result["alternate"][key]

            self.initlist[pos]["status"]["die"] = result["die"]
            self.initlist[pos]["status"]["hits"] -= result["hits"]

            for key in ["hits/rnd", "no_parry", "ooo", "parry", "stunned"]:
                self.initlist[pos]["status"][key] += result[key]

            self.initlist[pos]["status"]["mod"].append(result["mod"])
            self.initlist[pos]["status"]["mod_total"] += result["mod"]["mod"]
            #self.initlist[pos]["status"]["mod"][0]["mod"] += self.initlist[pos]["status"]["mod"][-1]["mod"]
            #self.initlist[pos]["status"]["mod"][0]["rnd"] += self.initlist[pos]["status"]["mod"][-1]["rnd"]
            self.initlist[pos]["status"]["log"].append(f"damage type:{result['damage_type']}\nmod: {result['mod']['mod']}\nhits/rnd: {result['hits/rnd']}\nrnds: {result['mod']['rnd']}\n\n{result['description']}")

            if result["mod_attacker"]["mod_attacker"]:
                self.initlist[posa]["status"]["mod"].append(result["mod_attacker"])
                self.initlist[posa]["status"]["mod_total"] += result["mod_attacker"]["mod_attacker"]

        self.__updDefCombo(event = None)
        self.__updtAttckCombo(event = None)


    def __selectCritDamage(self):
        '''!
        This method choses the selected choice at Crit damages if there are any.

        ----
        @todo this has ti be fully implemented

        '''
        print("#### selectCritDamage ###")
        pprint(self.crittbls)
        self.notdoneyet("__selectCritDamage")


    def __updtAttckCombo(self, event = None):
        '''!
        This method updates the list of the self.__attackCombo combobox

        ----
        @todo following has to be implemented
        - set the current character

        '''

        self.__attackCombo.configure(values = self.attackers)

        if not self.initroll:
            self.curr_attacker = self.__selectAttacker.get()

        else:
            self.curr_attacker = self.attackers[0]
            self.__selectAttacker.set(self.curr_attacker)

        self.initroll = False

        self.curr_defender = self.__selectDefender.get()
        at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)
        print("---------\nAttacker\n\n")
        pprint(at)

        if "piclink" in at.keys():
            imglink = at["piclink"]
        else:
            imglink = "./data/default/pics/default.jpg"

        self.__chgImg(attackerpic = imglink, defenderpic = None)

        ob = self.sortList(mylist = at['OB melee'], key = 1)[0]
        ob[0] = ob[0].replace(" ", "_")

        if ob[0] in self.atlist:
            self.__selectAT.set(ob[0])
            self.__skill.set(ob[1])

        self.__lvlAttacker.set(f"Lvl: {at['lvl']}")
        self.__curHPAttacker.set(f"HP: {at['status']['hits']}/{at['hits']}")
        self.__initAttacker.set(f"Init: {at['init']}")
        self.__ppAttacker.set(f"PP: {at['status']['PP']}/{at['PP']}")
        self.__wmodAttacker.set(f'Mod: {at["status"]["mod_total"]}')
        self.__stunAttacker.set(f'{labels["stunned"][self.lang]}: {at["status"]["stunned"]}')
        self.__parryAttacker.set(f'{labels["parry"][self.lang]}: {at["status"]["parry"]}')
        self.__noparryAttacker.set(f'{labels["no_parry"][self.lang]}: {at["status"]["no_parry"]}')
        self.__koAttacker.set(f'k.o.: {at["status"]["ooo"]}')


    def __updDefCombo(self, event = None):
        '''!
        This method updates the list of the self.__defendCombo combobox

        ----
        @todo following has to be implemented
        -set the currently selected defender
        '''

        self.curr_defender = self.__selectDefender.get()
        self.curr_attacker = self.__selectAttacker.get()
        self.__defendCombo.configure(values = self.defenders)
        defend = self.__findCombatant(name = self.curr_defender, chklist = self.initlist)
        print("********\nDefender\n\n")
        pprint(defend)

        self.__AT.set(defend["AT"])
        self.__DB.set(defend["DB"])

        if "piclink" in defend.keys():
            imglink = defend["piclink"]
        else:
            imglink = "./data/default/pics/default.jpg"

        self.__chgImg(attackerpic = None, defenderpic = imglink)
        self.__lvlDefender.set(f"Lvl: {defend['lvl']}")
        self.__curHPDefender.set(f"HP: {defend['status']['hits']}/{defend['hits']}")
        self.__initDefender.set(f"Init: {defend['init']}")
        self.__ppDefender.set(f"PP: {defend['status']['PP']}/{defend['PP']}")
        self.__wmodDefender.set(f'Mod: {defend["status"]["mod_total"]}')
        self.__bleedDefender.set(f"HP/rd: {defend['status']['hits/rnd']}")
        self.__stunDefender.set(f"{labels['stunned'][self.lang]}: {defend['status']['stunned']}")
        self.__parryDefender.set(f'{labels["parry"][self.lang]}: {defend["status"]["parry"]}')
        self.__noparryDefender.set(f'{labels["no_parry"][self.lang]}: {defend["status"]["no_parry"]}')
        self.__koDefender.set(f'k.o.: {defend["status"]["ooo"]}')


    def __nextRnd(self):
        '''!
        This method does all calculations to prepare the next combat round such as
        - subtracting hits per round
        - keeping track of states like 'stunned', "no parry", "parry only"
        - updating self.initlist (deleting dead monsters etc)
        ---
        @todo has to be fully implemented
        '''
        #raise combatround
        self.combatround += 1
        rm = []

        for i in range(0, len(self.initlist)):
            self.initlist[i]["status"]["hits"] -= self.initlist[i]["status"]["hits/rnd"]

            # status check
            if self.initlist[i]["status"]["stunned"] == 1:
                self.initlist[i]["status"]["mod_total"] -= 25

            for stat in ["parry", "no_parry", "ooo", "die", "stunned"]:

                if  self.initlist[i]["status"][stat] > 0:
                    self.initlist[i]["status"][stat] -= 1

            #mod check
            rm_mod = []
            for j in range(0, len(self.initlist[i]["status"]["mod"])):
                self.initlist[i]["status"]["mod"][j]["rnd"] -= 1
                print(f'Debug nxtrnd: {i},{j} {self.initlist[i]["status"]["mod"][j]}')
                if "mod" in self.initlist[i]["status"]["mod"][j].keys():
                    if self.initlist[i]["status"]["mod"][j]["mod"] <= 0 or self.initlist[i]["status"]["mod"][j]["rnd"] <= 0:
                        rm_mod.append(j)
                else:
                    if self.initlist[i]["status"]["mod"][j]["mod_attacker"] <= 0 or self.initlist[i]["status"]["mod"][j]["rnd"] <= 0:
                        rm_mod.append(j)

                #xxxxxxxxxxxx

            # select killed combatants
            if "player" not in self.initlist[i].keys() and (self.initlist[i]["status"]["hits"] < 1 or self.initlist[i]["status"]["die"] == 0):
                rm.append(self.initlist[i]["name"])

        # remove killed NSCs/Monster
        for combatant in rm:
            self.__rmCombatant(name = combatant)

        self.__rollInit()


    def __rmCombatant(self, name = ""):
        '''!
        This method removes combatants from self.initliast
        @param name of the combatant to remove from self.initlist
        '''
        for elem in self.initlist:
            if name == elem["name"]:
                self.initlist.remove(elem)
                break


    def __buildWin(self):
        """!
        This method builds the window content.

        ----
        @todo
        - the row 0 has to be build:
            -Initiative
            - Attacker (name & Pic)
            - select opponent combo (display name of defender) & image Display
            - next button
        - row 1:
            - frame 1 attacker/defender:
                - remaining hits #/#
                - remaining pp #/#
                - modificator (wounds)
                - stunned # Rds
                - only parry # rds
                - k.o. # rds
                - bleeding #/Rd
                - dies in # rds
            - frame 2 attacker/defender:
                - lvl #
                - AT #

            - frame 3 attacker:
                - healing mod
                - reduce wound mods
                - imrpove OB
                - imporve DB
            - frame 4: Attack results
        """

        # row 0
        self.atcanvas = Canvas(master = self.window,
                          width = 95,
                          height = 95,
                          bg = "green")
        self.atcanvas.grid(row = 0, rowspan = 5, column = 0, sticky = "NS")

        self.defcanvas = Canvas(master = self.window,
                          width = 95,
                          height = 95,
                          bg = "green")
        self.defcanvas.grid(row = 0, rowspan = 5, column = 6, sticky = "NS")
        self.__chgImg()

        self.__lvlAttacker = StringVar()
        self.__lvlAttacker.set("Lvl: 1")
        Label(self.window,
              textvariable = self.__lvlAttacker
              ).grid(column = 1, row = 0, sticky = W)

        self.__curHPAttacker = StringVar()
        self.__curHPAttacker.set("HP: 30/30")
        Label(self.window,
              textvariable = self.__curHPAttacker
              ).grid(column = 2, row = 0, sticky = W)

        self.__ppAttacker = StringVar()
        self.__ppAttacker.set("PP: 0/0")
        Label(self.window,
              textvariable = self.__ppAttacker
              ).grid(row = 0, column = 3, sticky = W)

        self.__wmodAttacker = StringVar()
        self.__wmodAttacker.set("Mods: 0")
        Label(self.window,
              textvariable = self.__wmodAttacker
              ).grid(row = 0, column = 4, sticky = E)

        self.__bleedAttacker = StringVar()
        self.__bleedAttacker.set("HP/rd: 0")
        Label(self.window,
              textvariable = self.__bleedAttacker
              ).grid(row = 0, column = 5, sticky = W)

        #------------------- Defender ------------------------------------------
        self.__lvlDefender = StringVar()
        self.__lvlDefender.set("Lvl: 1")
        Label(self.window,
              textvariable = self.__lvlDefender
              ).grid(column = 7, row = 0, sticky = W)

        self.__curHPDefender = StringVar()
        self.__curHPDefender.set("HP: 30/30")
        Label(self.window,
              textvariable = self.__curHPDefender
              ).grid(column = 8, row = 0, sticky = W)

        self.__ppDefender = StringVar()
        self.__ppDefender.set("PP: 0/0")
        Label(self.window,
              textvariable = self.__ppDefender
              ).grid(row = 0, column = 9, sticky = W)

        self.__wmodDefender = StringVar()
        self.__wmodDefender.set("Mods: 0")
        Label(self.window,
              textvariable = self.__wmodDefender
              ).grid(row = 0, column = 10, sticky = W)

        self.__bleedDefender = StringVar()
        self.__bleedDefender.set("HP/rd: 0")
        Label(self.window,
              textvariable = self.__bleedDefender
              ).grid(row = 0, column = 11, sticky = W)

        #----------- row 1 ---------------------------------------------------------
        self.__initAttacker = StringVar()
        self.__initAttacker.set("Init: 0")
        Label(self.window,
              textvariable = self.__initAttacker
              ).grid(row = 1, column = 1, sticky = W)

        self.__stunAttacker = StringVar()
        self.__stunAttacker.set(f'{labels["stunned"][self.lang]}: 0')
        Label(self.window,
              textvariable = self.__stunAttacker
              ).grid(row = 1, column = 2, sticky = W)

        self.__parryAttacker = StringVar()
        self.__parryAttacker.set(f'{labels["parry"][self.lang]}: 0')
        Label(self.window,
              textvariable = self.__parryAttacker
              ).grid(row = 1, column = 3, sticky = W)

        self.__noparryAttacker = StringVar()
        self.__noparryAttacker.set(f'{labels["no_parry"][self.lang]}: 0')
        Label(self.window,
              textvariable = self.__noparryAttacker
              ).grid(row = 1, column = 4, sticky = W)

        self.__koAttacker = StringVar()
        self.__koAttacker.set("k.o.: 0")
        Label(self.window,
              textvariable = self.__koAttacker
              ).grid(row = 1, column = 5, sticky = W)

        #------------------- Defender row1 1-----------------------------------------
        self.__initDefender = StringVar()
        self.__initDefender.set("Init: 0")
        Label(self.window,
              textvariable = self.__initDefender
              ).grid(row = 1, column = 7, sticky = W)

        self.__stunDefender = StringVar()
        self.__stunDefender.set(f'{labels["stunned"][self.lang]}: 0')
        Label(self.window,
              textvariable = self.__stunDefender
              ).grid(row = 1, column = 8, sticky = W)

        self.__parryDefender = StringVar()
        self.__parryDefender.set(f'{labels["parry"][self.lang]}: 0')
        Label(self.window,
              textvariable = self.__parryDefender
              ).grid(row = 1, column = 9, sticky = W)

        self.__noparryDefender = StringVar()
        self.__noparryDefender.set(f'{labels["no_parry"][self.lang]}: 0')
        Label(self.window,
              textvariable = self.__noparryDefender
              ).grid(row = 1, column = 10, sticky = W)

        self.__koDefender = StringVar()
        self.__koDefender.set("k.o.: 0")
        Label(self.window,
              textvariable = self.__koDefender
              ).grid(row = 1, column = 5, sticky = W)
        # row 2

        # row 3

        # row 4

        # row 5

        # row 6
        self.__selectAttacker = StringVar()
        self.__selectAttacker.set("Egon")
        self.__attackCombo = Combobox(self.window,
                                      textvariable = self.__selectAttacker,
                                      values = self.attackers)
        self.__attackCombo.bind("<<ComboboxSelected>>", self.__updtAttckCombo)
        self.__attackCombo.grid(column = 0, row = 6, sticky = "W")

        #------------------- Defender ------------------------------------------

        self.__selectDefender = StringVar()
        self.__selectDefender.set("Anton")
        self.__defendCombo = Combobox(self.window,
                                      textvariable = self.__selectDefender,
                                      values = self.defenders)
        self.__defendCombo.bind("<<ComboboxSelected>>", self.__updDefCombo)
        self.__defendCombo.grid(column = 6, row = 6, sticky = "EW")

        # row 7
        Button(self.window,
               text = txtbutton["but_nxtrd"][self.lang],
               command = self.__nextRnd
               ).grid(column = 0, row = 7, rowspan = 3, sticky = "EW")
        # row 8

        # row 9

        # row 10

        Label(self.window,
              text = labels["attack table"][self.lang] + ":",
              ).grid(column = 0, row = 10, sticky = "W")

        self.atlist = list(self.attacktbls.keys())
        self.atlist.sort()
        self.__selectAT = StringVar()
        self.__selectAT.set(self.atlist[0])
        self.__ATOpt = Combobox(self.window,
                                 values = self.atlist,
                                 textvariable = self.__selectAT,
                                 width = 20)
#        self.__ATOpt = OptionMenu(self.window,
#                                  self.__selectAT,
#                                  *self.atlist,
#                                  )
        self.__ATOpt.grid(column = 1,
                          row = 10,
                          sticky = "W")

        Label(self.window,
              text = labels['skill'][self.lang] + ":"
              ).grid(column = 2, row = 10, sticky = "W")

        self.__skill = IntVar()
        self.__skill.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__skill,
              width = 5
              ).grid(column = 3, row = 10, sticky = "EW")

        Label(self.window,
              text = labels['roll'][self.lang] + ":"
              ).grid(column = 4, row = 10, sticky = "W")

        self.__atroll = IntVar()
        self.__atroll.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__atroll,
              width = 5
              ).grid(column = 5, row = 10, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_roll"][self.lang],
               command = self.__rollAttack
               ).grid(column = 6, row = 10, sticky = "EW")

        Label(self.window,
              text = "AT:"
              ).grid(column = 7, row = 10, sticky = "W")

        self.__AT = StringVar()
        self.__AT.set("1")
        Entry(self.window,
              textvariable = self.__AT,
              width = 5,
              justify = "center"
              ).grid(column = 8, row = 10, sticky = "EW")

        Label(self.window,
              text = "max:"
              ).grid(column = 9, row = 10, sticky = "W")

        self.__maxlvl = StringVar()
        self.__maxlvl.set("H")
        self.__maxOpt = Combobox(self.window,
                                 values = ["S", "M", "L", "H"],
                                 textvariable = self.__maxlvl,
                                 width = 3)
#        self.__maxOpt.bind('<<ComboboxSelected>>', output)
#        self.__maxOpt = OptionMenu(self.window,
#                                   self.__maxlvl,
#                                   *["S", "M", "L", "H"]
#                                   )
        self.__maxOpt.grid(column = 10, row = 10, sticky = "W")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self.checkAttack
               ).grid(column = 11, row = 10, sticky = "EW")

        # row 11

        self.__resultAT = StringVar()
        self.__resultAT.set("--")
        Label(self.window,
              justify = "center",
              textvariable = self.__resultAT,
              borderwidth = 2,
              relief = "sunken"
              ).grid(column = 0, columnspan = 6, row = 11, sticky = "EW", pady = 2)

        Label(self.window,
              text = "DB:"
              ).grid(column = 7, row = 11, sticky = "E")

        self.__DB = IntVar()
        self.__DB.set(0)
        Entry(self.window,
              textvariable = self.__DB,
              width = 5,
              justify = "center"
              ).grid(column = 8, row = 11, sticky = "EW")

        self.__woItem = StringVar()
        self.__woItem.set(labels["with"][self.lang])
        self.__dmgOpt = OptionMenu(self.window,
                                   self.__woItem,
                                   *self.damachoice,
                                   )
        self.__dmgOpt.grid(row = 11, column = 9, columnspan = 2, sticky = "NEWS")

        Button(self.window,
               text = txtbutton["but_dmg"][self.lang],
               command = self.__applyDamage
               ).grid(row = 11, column = 11)

        # row 12
        Label(self.window,
              text = labels["crit table"][self.lang] + ":"
              ).grid(column = 0, row = 12, sticky = "W")

        self.critlist = list(self.crittbls.keys())
        self.critlist.sort()
        self.__selectCrit = StringVar()
        self.__selectCrit.set(self.critlist[0])
        self.__CritOpt = Combobox(self.window,
                                 values = self.critlist,
                                 textvariable = self.__selectCrit,
                                 width = 20)
#        self.__CritOpt = OptionMenu(self.window,
#                                  self.__selectCrit,
#                                  *self.critlist,
#                                  )
        self.__CritOpt.grid(column = 1, row = 12, sticky = "W")

        Label(self.window,
              text = "Crit:"
              ).grid(column = 2, row = 12, sticky = "W")

        self.__critType = StringVar()
        self.__critType.set("")
        Entry(self.window,
              justify = "center",
              width = 5,
              textvariable = self.__critType
              ).grid(column = 3, row = 12, sticky = "EW")

        Label(self.window,
              text = labels['roll'][self.lang] + ":"
              ).grid(column = 4, row = 12, sticky = "W")

        self.__critroll = IntVar()
        self.__critroll.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__critroll,
              width = 5
              ).grid(column = 5, row = 12, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_roll"][self.lang],
               command = self.__rollCrit
               ).grid(column = 6, row = 12, sticky = "EW")

        Label(self.window,
              text = labels["weapon"][self.lang] + ":"
              ).grid(column = 7, columnspan = 2, row = 12, sticky = "W")

        self.__weaponType = StringVar()
        self.__weaponType.set(weapontypes["en"][0])

        self.__weaponOpt = OptionMenu(self.window,
                                      self.__weaponType,
                                      *weapontypes["en"]
                                      )
        self.__weaponOpt.grid(column = 9, columnspan = 2, row = 12, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self.checkCrit
               ).grid(column = 11, row = 12, sticky = "EW")

        # row 13
        vscroll = Scrollbar(self.window, orient = VERTICAL)
        self.__displayCrit = Text(self.window,
                                  yscrollcommand = vscroll.set,
                                  height = 20
                                  )
        vscroll.config(command = self.__displayCrit.yview)
        self.__displayCrit.grid(column = 0, columnspan = 12, row = 13, sticky = "NEWS")


    def checkAttack(self):
        """!
        This checks the result of a roll against an attack table

        """
        self.attacktbls[self.__selectAT.get()].getHits(self.__skill.get() + self.__atroll.get() - self.__DB.get(),
                                                       self.__AT.get(),
                                                       self.__maxlvl.get()
                                               )
        self.hits = self.attacktbls[self.__selectAT.get()].hits
        self.__resultAT.set("Hits: {}\t Crit: {}\t Type: {}".format(self.attacktbls[self.__selectAT.get()].hits,
                                                                self.attacktbls[self.__selectAT.get()].crit,
                                                                critc[self.attacktbls[self.__selectAT.get()].crittype][self.lang]))
        self.__selectCrit.set(critc[self.attacktbls[self.__selectAT.get()].crittype]["en"])
        self.__critType.set(self.attacktbls[self.__selectAT.get()].crit)


    def checkCrit(self):
        """!
        This checks the result of a roll against a critical table

        ----
        @todo error catching: if no crit was rolled (but hits)
        """
        words = {"hits": "additional hits: {}\n",
               "mod": "Modifier {} for {} rounds ({} d : {} h : {} m : {} s)\n",
               "mod_attacker": "Attacker's Modifier {} for {} rounds\n",
               "die":"the foe dies in {} rounds\n",
               "ooo": "foe is out of order for {} rounds\n",
               "hits/rnd": "foe bleeds {} hits/rnd\n",
               "parry": "foe can only parry for {} rounds\n",
               "no_parry": "foe cannot parry for {} rounds\n",
               "stunned": "foe is stunned for {} rounds\n"}
        wordlist = list(words.keys())
        wordlist.sort()

        self.crittbls[self.__selectCrit.get()].getCrit(roll = self.__critroll.get(),
                                                       crit = self.__critType.get(),
                                                       weapontype = self.__weaponType.get())

        if (self.__selectCrit.get() not in ["large", "superlarge"]) or \
        (self.__selectCrit.get() == "large" and self.__critType.get() in ["B", "C", "D", "E", "F", "G", "H", "I"]) or \
        (self.__selectCrit.get() == "superlarge" and self.__critType.get() in ["D", "E", "F", "G", "H", "I"]):
            result = "Damage Type: "

            if "damage_type" not in self.crittbls[self.__selectCrit.get()].crithit.keys():
                result += "hits"
            elif self.crittbls[self.__selectCrit.get()].crithit["damage_type"] == "":
                result += "Flesh Wound\n"

            else:
                result += self.crittbls[self.__selectCrit.get()].crithit["damage_type"] + "\n"

            result += "{}\n\n".format(self.crittbls[self.__selectCrit.get()].crithit["description"])

            if self.crittbls[self.__selectCrit.get()].crithit["cover"] != "":
                result += "==> without armor at {}\n ".format(self.crittbls[self.__selectCrit.get()].crithit["cover"])

                for key in wordlist:

                    if key in self.crittbls[self.__selectCrit.get()].crithit["alternate"].keys():

                        if key in ["mod_attacker"]:
                            result += words[key].format(self.crittbls[self.__selectCrit.get()].crithit["alternate"][key][key],
                                                        self.crittbls[self.__selectCrit.get()].crithit["alternate"][key]["rnd"])
                        elif key == "mod":
                            result += words[key].format(self.crittbls[self.__selectCrit.get()].crithit["alternate"][key][key],
                                                        self.crittbls[self.__selectCrit.get()].crithit["alternate"][key]["rnd"],
                                                        self.crittbls[self.__selectCrit.get()].crithit["alternate"][key]["rnd"] // (24 * 360),
                                                        self.crittbls[self.__selectCrit.get()].crithit["alternate"][key]["rnd"] % (24 * 360) // 360,
                                                        self.crittbls[self.__selectCrit.get()].crithit["alternate"][key]["rnd"] % (24 * 360) % 360 // 6,
                                                        self.crittbls[self.__selectCrit.get()].crithit["alternate"][key]["rnd"] % (24 * 360) % 360 % 6 * 10
                                                        )
                        else:
                            result += words[key].format(self.crittbls[self.__selectCrit.get()].crithit["alternate"][key])

                result += "\n\n==>with armor at {}\n".format(self.crittbls[self.__selectCrit.get()].crithit["cover"])

            if self.crittbls[self.__selectCrit.get()].crithit["die"] >= 0:
                result += words["die"].format(self.crittbls[self.__selectCrit.get()].crithit["die"])

            if self.crittbls[self.__selectCrit.get()].crithit["hits"] > 0:
                result += words["hits"].format(self.crittbls[self.__selectCrit.get()].crithit["hits"])
                # wip
                #self.hits +=self.crittbls[self.__selectCrit.get()].crithit["hits"]
            if self.crittbls[self.__selectCrit.get()].crithit["hits/rnd"] > 0:
                result += words["hits/rnd"].format(self.crittbls[self.__selectCrit.get()].crithit["hits/rnd"])

            if self.crittbls[self.__selectCrit.get()].crithit["mod"]["mod"] != 0:
                result += words["mod"].format(self.crittbls[self.__selectCrit.get()].crithit["mod"]["mod"],
                                             self.crittbls[self.__selectCrit.get()].crithit["mod"]["rnd"],
                                             self.crittbls[self.__selectCrit.get()].crithit["mod"]["rnd"] // (24 * 360),
                                             self.crittbls[self.__selectCrit.get()].crithit["mod"]["rnd"] % (24 * 360) // 360,
                                             self.crittbls[self.__selectCrit.get()].crithit["mod"]["rnd"] % (24 * 360) % 360 // 6,
                                             self.crittbls[self.__selectCrit.get()].crithit["mod"]["rnd"] % (24 * 360) % 360 % 6 * 10
                                             )

            if self.crittbls[self.__selectCrit.get()].crithit["mod_attacker"]["mod_attacker"] != 0:
                result += words["mod_attacker"].format(self.crittbls[self.__selectCrit.get()].crithit["mod_attacker"]["mod_attacker"],
                                             self.crittbls[self.__selectCrit.get()].crithit["mod_attacker"]["rnd"])

            if self.crittbls[self.__selectCrit.get()].crithit["no_parry"] > 0:
                result += words["no_parry"].format(self.crittbls[self.__selectCrit.get()].crithit["no_parry"])

            if self.crittbls[self.__selectCrit.get()].crithit["ooo"] > 0:
                result += words["ooo"].format(self.crittbls[self.__selectCrit.get()].crithit["ooo"])

            if self.crittbls[self.__selectCrit.get()].crithit["parry"] > 0:
                result += words["parry"].format(self.crittbls[self.__selectCrit.get()].crithit["parry"])

            if self.crittbls[self.__selectCrit.get()].crithit["stunned"] > 0:
                result += words["stunned"].format(self.crittbls[self.__selectCrit.get()].crithit["stunned"])

        else:
            result = "No Critical result"

        self.__displayCrit.delete("1.0", "end")
        self.__displayCrit.insert(END, result)

#class combatWin(atWin):
#    '''! This class is for opponents fighing against each other
#    '''
#
#
#    def __init__(self, lang = "en", datadir = "data/default"):
#        """!
#        Constructor
#        \param lang selected output language
#        \param datadir configured default datadir
#        """
#        self.lang = lang
#        self.datadir = datadir
#        self.attacktbls = {}
#        self.crittbls = {}
#
#        atWin.__addMenu(self)
#        # read all attack tables
#        for table in os.listdir("{}/fight/attacks".format(self.datadir)):
#            if table[-4:] == ".csv" and table[-5:] != "-.csv":
#                self.attacktbls[table[:-4]] = attacktable("{}/fight/attacks/{}".format(self.datadir, table))
#
#        # read all crit tables
#        for table in os.listdir("{}/fight/crits".format(self.datadir)):
#            if table[-4:] == ".csv" and table[-5:] != "-.csv":
#                self.crittbls[table[:-9]] = crittable("{}/fight/crits/{}".format(self.datadir, table))
#
#        #window components
#        #atWin.__init__(self, self.lang)
#        #self.__quit()
#        blankWindow.__init__(self, self.lang)
#        self.window.title("Attack Round Helper")
#        self.__addMenu()
#        self.__addHelpMenu()
#        self.__buildWin()
#        self.window.mainloop()
#
#
#    def __openParty(self):
#        '''! Opens a Character Group file for combat'''
#
#        pass
#
#
#    def __openEnemy(self):
#        '''! Opens a Enemy Group file for combat'''
#
#        pass
#
#    #def __addMenu(self):
#    #    '''!
#    #    This methods adds the menu bar to the window
#    #    '''
#    #    self.filemenu = Menu(master = self.menu)
#    #    self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
#    #                          menu = self.filemenu)
#    #    self.filemenu.add_command(label = submenu['file'][self.lang]['open_party'],
#    #                              command = self.__openParty)
#    #    self.filemenu.add_command(label = submenu['file'][self.lang]['open_enemy'],
#    #                              command = self.__openEnemy)
#    #    self.filemenu.add_separator()
#    #    self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
#    #                              command = self.__quit)
#
#
#    def __quit(self):
#        '''!
#        This method closes the window
#        '''
#        self.window.destroy()



if __name__ == '__main__':
    win = atWin()
    #win2 = combatWin()
