#!/usr/bin/env python3
'''!
\file attackcheck.py
\package attackcheck
\brief This program can be used to  get the results of  attack and critical tables

This mangages a fight between a player character group and a group of monsters or
other opponents.

\date (c) 2021 - 2022
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.7
'''
__version__ = "0.7"
__updated__ = "23.10.2022"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__me__ = "RM RPG Tools: attack checker module"

from copy import deepcopy
from pprint import pformat
from random import randint
from tkinter import filedialog
from tkinter.ttk import Combobox
import json
import os

from PIL import Image, ImageTk

from gui.window import *
from rpgToolDefinitions.helptools import RMDice as Dice
from rpgToolDefinitions.magic import magicpath
from rpgtoolbox import logbox as log
from rpgtoolbox.combat import *
from rpgtoolbox.confbox import *
from rpgtoolbox.globaltools import *
from rpgtoolbox.handlemagic import getSpellNames

mycnf = chkCfg()
logger = log.createLogger('AT-Window', 'info', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = "attackcheck.log")



class atWin(blankWindow):
    """!
    This class generates a window where you can look up your attack results.
    Results of dice rolls may be entered or a roll may be done by clicking a
    button.

    ----
    @todo
    - change bg color by level of damage
    - adding/deleting single NSCs/monsters to/from loaded groups (from pool file)
    - adding/deleting single character to/from loaded group
    - selection of chars/ncs for fight

    ----
    @bug
    - reload after kill or loading enemy groups does not work properly
    """


    def __init__(self, lang = "en", datadir = "./data/default"):
        """!
        Constructor
        \param lang selected output language
        \param datadir configured default datadir
        """
        logger.debug(f"language: {lang}\n datadir: {datadir}")
        self.lang = lang
        self.datadir = datadir
        logger.debug(f"language: {lang}")
        logger.debug(f"data dir: {datadir}")

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
        ## \var self.weapontab
        # holds the given weapon table as dictionary with short term as master key
        # and all information about the weapon (such as fumble or breaking numbers)
        self.weapontab = getWeaponTab()
        logger.info("Weapon tables successfully read.")
        self.curr_attacker = 0
        self.curr_defender = 0
        self.__oblist = []
        self.defaultnscimg = datadir + "/pics/default.jpg"
        logger.debug(f"default image set to {self.defaultnscimg}")
        self.fmask = [txtwin['grp_files'][self.lang],
                     txtwin['enemygrp_files'][self.lang],
                     txtwin['all_files'][self.lang]]
        self.fmaskc = [txtwin['grp_files'][self.lang],
                     txtwin['all_files'][self.lang]]
        self.fmaske = [txtwin['enemygrp_files'][self.lang],
                     txtwin['all_files'][self.lang]]

        ## \var self.weaponlist
        # a list of dictionaries holding all infomation about all weapons. If a
        # weapon has no specific attack table the standard attack table for it
        # will be documented here.
        self.weaponlist = readCSV(f"{self.datadir}/fight/weapon_stats.csv")
        logger.info("list of weapons read successfully.")
        self.__prepareWL()
        logger.debug("list of weapons successfully prepared for usage.")
        ## \var self.reverseweaponindex
        # This dictionary holds weapon name as key and short form as value
        self.reverseweaponindex = {}

        for key in self.weapontab.keys():
            self.reverseweaponindex[self.weapontab[key]["name"]] = key

        logger.info("weapon index prepared.")

        # read all attack tables
        for table in os.listdir("{}/fight/attacks".format(self.datadir)):

            if table[-4:] == ".csv" and table[-5:] != "-.csv":
                self.attacktbls[table[:-4]] = attacktable("{}/fight/attacks/{}".format(self.datadir, table))
                logger.debug(f"read {table[:-4]} successfully.")

        logger.info("All attack tables loaded.")

        # read all crit tables
        for table in os.listdir("{}/fight/crits".format(self.datadir)):

            if table[-4:] == ".csv" and table[-5:] != "-.csv":
                self.crittbls[table[:-9]] = crittable("{}/fight/crits/{}".format(self.datadir, table))
                logger.debug(f"read {table[:-4]} successfully.")

        logger.info("All critical tables loaded.")

        # get all weapon data
        with open(os.path.join(os.getcwd(), "data/default/fight/weapons_full.json")) as fp:
            self.weapondata = json.load(fp)

        logger.info("All weapon data loaded.")

        self.fumble = fumbletable(lang = self.lang)

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
        logger.debug("help menu build")


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
        logger.debug("file menu build")


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
        logger.debug("edit menu build")


    def openParty(self):
        '''!
        This method reads a character party group file to self.partygrp
        '''

        self.__partypath = askopenfilename(filetypes = self.fmaskc, initialdir = os.getcwd(), defaultextension = ".json")
        logger.debug(f"chosen group file {self.__partypath}")

        try:
            with open(self.__partypath, "r") as fp:
                ##@var self.__fullparty
                # This is holding the full party data
                self.__fullparty = json.load(fp)
            logger.info(f"{self.__partypath} was read")

            if type(self.__fullparty) == type({}):
                self.__fullparty = [self.__fullparty]
            logger.debug("fullparty initialized.")

            self.__prepareChars()

        except Exception as error:
            logger.error(f"{error}")
            self.message = messageWindow()
            self.message.showinfo(f"{error}", "ERROR")

        #self.__prepareChars()


    def openEnemies(self):
        '''!
        This opens an enemy party to fight against
        '''
        self.__enemypath = askopenfilename(filetypes = self.fmaske, defaultextension = "*.csv", initialdir = os.getcwd())
        logger.debug(f"openEnemies: chosen enemies group file {self.__enemypath}")

        if self.__enemypath[-4:].lower() == ".csv":
            self.enemygrp = readCSV(self.__enemypath)
            logger.info(f'openEnemies: {self.__enemypath} read')
        else:
            logger.error("openEnemies: wrong file format! must be CSV")
            self.message("openEnemies: wrong file format: must be CSV")

        self.__prepareNSCs()

   # def __getWeaponStrength(self,weapon="bs"):


    def __prepareNSCs(self, mode = "auto"):
        '''!
        this prepares the read enemy list (of dicts) to 'battle format' - that
        means it splits the OBs into lists.
        @param mode this option handles the modus operandi:
               - auto: the number of opponents is randomly chosen by the 'enc' column
               - first: takes the first number of 'enc' range
               - last: takes the last number of 'enc' range

        ----
        @todo - <strike>append NSCs/Monsters if the enc >1</strike>
              - immunity list
              - weakness list

        '''
        size = "H"
        self.enemygrp = createCombatList(self.enemygrp)
        apendix = []

        for i in range(0, len(self.enemygrp)):

            if "enc" not in self.enemygrp[i].keys():
                logger.warning(f"'enc not in {json.dumps(self.enemygrp[i])}")

            enc = self.enemygrp[i]["enc"].split("-")

            for j in range(0, len(enc)):
                if  enc[j]:
                    enc[j] = int(enc[j])
                else:
                    enc[j] = 0

            if mode.lower() == "first":
                enc[1] = enc[0]

            elif mode.lower() == "last":
                enc[0] = enc[1]

            logger.debug(f'prepareNSCs: enc = {enc}')
            if type(enc) == type([]) and len(enc) == 2:
                self.enemygrp[i]["enc"] = randint(enc[0], enc[1])

            # not elegant but works to remove nscs/monster with enc ==0

            if self.enemygrp[i]["enc"] == 0:
                self.enemygrp[i]["status"]["hits"] = 0
                logger.debug(f'prepareNSCs: "killed" {self.enemygrp[i]["name"]} by setting HP == 0')

            #generate OB lists

            melee = self.enemygrp[i]["OB melee"].split("/")

            for j in range(0, len(melee)):

                if type(melee[j]) == type(""):
                    melee[j] = melee[j].strip(" ")
                    melee[j] = melee[j].split(" ")
                    logger.debug(f'perpareNSCs: melee[{j}] = {melee[j]}')

                if len(melee[j]) == 2:
                    melee[j][-1], melee[j][0] = melee[j][0], melee[j][-1]
                    melee[j].append("H")
                    logger.debug(f'prepareNSCs: size appended {melee[j]}')

                elif len(melee[j]) == 3:
                    melee[j][2], melee[j][1], melee[j][0] = melee[j][1], melee[j][0], melee[j][2]

                if len(melee[j]) == 2:
                    melee[j].insert(1, size)

                ## add fumble number
                #melee[j].append(int(self.weapontab[melee[j][0]]['fumble']))
                ## add breakage number
                #melee[j].append(int(self.weapontab[melee[j][0]]['breakage']))

                melee[j].append(melee[j][0])

                melee[j][0] = self.weapontab[melee[j][0]]['name']

            self.enemygrp[i]["OB melee"] = melee

            missile = self.enemygrp[i]["OB missile"].split("/")

            for j in range(0, len(missile)):
                missile[j] = missile[j].split(" ")

                if len(missile[j]) > 1:
                    missile[j][-1], missile[j][0] = missile[j][0], missile[j][-1]

                if len(missile[j]) == 2:
                    missile[j].insert(2, size)

                if missile[j][0] in self.weapontab.keys():
                    missile[j][0] = self.weapontab[missile[j][0]]["name"]
                else:
                    missile[j][0] = "n/a"

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

                if spelldummy != [""] and ":" in spelldummy and spelldummy.find("/") + spelldummy.find("\\") > 0:

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

            if "enc" not in elem.keys():
                logger.warning(f"no encounter number for\n {json.dumps(elem, indent = 4)}")
                elem["enc"] = 1

            if elem["enc"] > 0:
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
            logger.debug(f"preparing {json.dumps(char,indent=4)}...")

            dummy = dict.fromkeys(cindex, 0)
            dummy["Qu"] = char["Qu"]["total"]
            piclink = char["piclink"]
            logger.debug(piclink)

            if "AT" in char.keys():

                if char["AT"] == 0:
                    char["AT"] = 1
            else:
                char["AT"] = 1

            if os.path.isfile(piclink):
                pass

            else:
                picname = piclink.split("/")[-1]

                if os.path.isfile(self.datadir + "pic/" + picname):
                    char["piclink"] = self.datadir + "pic/" + picname
                    logger.info(f"changed image link to {self.datadir+'pic/'+picname}")

                else:
                    char["piclink"] = self.defaultnscimg
                    logger.warning("could not find character image at {self.datadir+'pic/'+picname} and set it to default")

            for stat in cindex:

                if stat in char.keys():
                    dummy[stat] = char[stat]

            if "armquickpen" in char.keys():
                dummy["DB"] = 3 * char["Qu"]["total"] + char["armquickpen"]

            else:
                char["armquickpen"] = 0
                logger.warning(f"no armorquickpen found in {char['name']}'s data! Set it to 0.")
                dummy["Qu"] = char["Qu"]["total"]

            if char["cat"]["Special Defenses"]["Skill"]["Adrenal Defense"]["total bonus"] > 0:
                dummy["DB"] += char["cat"]["Special Defenses"]["Skill"]["Adrenal Defense"]["total bonus"]

            if dummy["DB"] < 0:
                dummy["DB"] = 0
            logger.debug(f"{dummy['name']}'s DB is: {dummy['DB']}.")

            dummy["init"] = 0
            dummy["hits"] = char["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"]
            dummy["PP"] = char["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"]
            dummy["OB melee"] = []
            dummy["OB missile"] = []
            dummy["spell"] = []
            dummy["weapon type"] = [[], []]
            logger.debug(f"combat concerned parameters initialized for {dummy['name']}")

            for m in melee:

                for skill in char["cat"][m]["Skill"].keys():

                    if skill not in ["Progression", "Stats"] and "+" not in skill:
                        addon = [skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"]

                        if addon not in dummy["OB melee"]:
                            dummy["OB melee"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"])

            logger.info(f"{dummy['name']}'s melee OBs collected")

            #sort melee weapons highest ob first
            dummy["OB melee"] = sorted(dummy["OB melee"], key = lambda k: k[1], reverse = True)
            logger.info(f"{dummy['name']}'s melee OBs sorted")

            for m in missile:

                for skill in char["cat"][m]["Skill"].keys():

                    if skill not in ["Progression", "Stats"] and "+" not in skill and [skill, char["cat"][m]["Skill"][skill]["total bonus"]] not in dummy["OB missile"]:
                        dummy["OB missile"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"]])

            logger.info(f"{dummy['name']}'s missile OBs collected.")
            # sort missle weapons highest ob first
            dummy["OB missile"] = sorted(dummy["OB missile"], key = lambda k: k[1], reverse = True)
            dummy["weapon type"][0] = ["normal"] * len(dummy["OB melee"])
            dummy["weapon type"][1] = ["normal"] * len(dummy["OB missile"])
            logger.info(f"{dummy['name']}'s missile OBs sorted.")

            self.partygrp.append(dummy)
            logger.info(f"{dummy['name']} added to party.")
            logger.debug(f"{json.dumps(dummy,indent=4)}")
            self.__chgImg(attackerpic = self.partygrp[0]["piclink"], defenderpic = "")

        self.partygrp = createCombatList(self.partygrp)
        logger.info(f"combatant list created from party group.")
        logger.debug(f"partygrp length {len(self.partygrp)} ")

        self.initlist += self.partygrp
        logger.info("added partygrp to initlist")
        logger.debug(f"length initlist {len(self.initlist)} ")
        #logger.debug(f"partygrp: \n{pformat(self.partygrp)}")
        self.attackers = []

        for elem in self.initlist:
            self.attackers.append(elem["name"])

        logger.debug("attackers set successfully")
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


    def __prepareWL(self):
        '''!
        This method prepares the  self.weaponlist read from CSV file.
        '''
        logger.info("start preparing internal weapon list.")

        for i in range(0, len(self.weaponlist)):

            # move '---' to None
            for key in self.weaponlist[i].keys():

                if "/" in self.weaponlist[i][key]:
                    self.weaponlist[i][key] = self.weaponlist[i][key].split("/")

                elif "':" in self.weaponlist[i][key]:
                    # distance for missile attacks: dist in feet, mod
                    self.weaponlist[i][key] = self.weaponlist[i][key].split("':")

                    for j in range(0, len(self.weaponlist[i][key])):
                        self.weaponlist[i][key][j] = self.weaponlist[i][key][j]

                if self.weaponlist[i][key] in ["---", ""]:
                    self.weaponlist[i][key] = None

            # build breakage numbers
            bn = int(self.weaponlist[i]["breakage"])
            self.weaponlist[i]["breakage"] = []

            for n in range(1, bn + 1):
                self.weaponlist[i]["breakage"].append(n + 10 * n)

           # print(json.dumps(self.weaponlist[i], indent = 4))
            logger.debug(f"{self.weaponlist[i]['item']} # {self.weaponlist[i]['breakage']}")
            # build strength
            s = self.weaponlist[i]["strength"].split("-")
            self.weaponlist[i]["strength"] = [randint(int(s[0]), int(s[1]))]
            logger.debug(f"{self.weaponlist[i]['item']} # {self.weaponlist[i]['strength']}")

            if len(s) == 3:
                self.weaponlist[i]["strength"].append(s[2])

            else:
                self.weaponlist[i]["strength"].append("m")

            logger.debug(json.dumps(self.weaponlist[i], indent = 4))


    def __rollInit(self):
        '''!
        This rolls the initiative

        '''

        # roll initiative for self.initlist
        cleaner = []

        for i in range(0, len(self.initlist)):

            if "Qu" not in self.initlist[i].keys():
                logger.warning(f"no Qu in \n {json.dumps(self.initlist[i])}")

            self.initlist[i]["init"] = int(self.initlist[i]['Qu']) + randint(1, 10)

            if self.initlist[i] not in cleaner:
                cleaner.append(self.initlist[i])

        self.initlist = deepcopy(cleaner)
        # sort self.initlist reversely
        self.initlist = sorted(self.initlist, key = lambda k: k["init"], reverse = True)

        self.attackers = []
        self.defenders = []

        for elem in self.initlist:

            #if elem['name'] not in self.attackers:
            #    self.attackers.append(elem["name"])
            if elem["status"]["hits"] > 0 and elem["status"]["ooo"] == 0:

                if elem["name"] not in self.attackers:
                    self.attackers.append(elem["name"])

            self.defenders.append(elem["name"])

        #self.defenders = deepcopy(self.initlist)
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


    def checkBreakage(self, roll = 55, weapons = ["Broadsword", "Spear"]):
        '''!
        This methods checks for weapon breakage.
        @param roll dice roll unmodified
        @param weapons list of the attacker and defender weapon
        @retval broken a boolean whether the attackers weapon is broken or not

        ----
        @todo the rest has to be implemented still:
        - load list of weapon specs

        '''
        broken = False
        mod = {"w":5,
               "s":15
               }

        if weapons[0] in self.reversweaponindex.keys():
            attackerw = self.weapontab[self.reversweaponindex[weapons[1]]]

            if weapons[0] in self.reversweaponindex.keys():
                defenderw = self.weapontab[self.reversweaponindex[weapons[1]]]
            else:
                defenderw = deepcopy(attackerw)

            breakage = []
            for i in range(1, int(attackerw["breakage"]) + 1):
                breakage.append(i * 10 + i)

            if roll in breakage:
                dummy = attackerw["strength"].split("-")
                strength = randint(int(dummy[0], int(dummy[1])))

                if attackerw["strength"][-1] in mod.keys() and defenderw["strength"] not in mod.keys():
                    strength -= mod[attackerw["strength"]]
                    #----------- hier weiter machen

        return broken


    def __chgImg(self, attackerpic = "./data/default/pics/default.jpg", defenderpic = "./data/default/pics/default.jpg"):
        '''!
        This method changes attacker's and defender's images when newly selected.

        @param attackerpic path & name of the picture of the attacker (will be downsized to 90x90 px)
        @param defenderpic path & name of the picture of the defender (will be downsized to 90x90 px)
        ----
        @todo add fallback to default if character picture can not be found
        Windows throws FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\Nillorian\\coding\\projects\\rpg-tools\\src\\data\\default\\pics\\bull.png'
        '''
        if attackerpic:
            from PIL import Image, ImageTk
            self.picattacker = Image.open(attackerpic).resize((110, 110), Image.ANTIALIAS)
            self.picattacker = ImageTk.PhotoImage(self.picattacker)
            self.atcanvas.create_image((110, 110), image = self.picattacker, anchor = "se")
        if defenderpic:
            from PIL import Image, ImageTk
            self.picdefender = Image.open(defenderpic).resize((110, 110), Image.ANTIALIAS)
            self.picdefender = ImageTk.PhotoImage(self.picdefender)
            self.defcanvas.create_image((110, 110), image = self.picdefender, anchor = "se")


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
            wo = self.__woItem.get()

            if  result["alternate"] != {} and wo == labels["without"][self.lang]:

                for elem in ["hits", "hits/rnd", "stunned", "parry", "no_parry", "ooo"]:
                    result[elem] = 0

                result["mod"]["mod"] = 0
                result["mod_attacker"]["mod_attacker"] = 0
                result["die"] = -1

                for key in result["alternate"].keys():
                    result[key] = result["alternate"][key]

            self.initlist[pos]["status"]["die"] = result["die"]
            self.initlist[pos]["status"]["hits"] -= result["hits"]

            for key in [ "no_parry", "ooo", "parry", "stunned"]:
                self.initlist[pos]["status"][key] += result[key]
            self.initlist[pos]["status"]["hits/rnd"] -= result["hits/rnd"]
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


    def __updtAttckCombo(self, event = None):
        '''!
        This method updates the list of the self.__attackCombo combobox and the
        other widgets concerned by the attacker
        ----
        '''

        self.__attackCombo.configure(values = self.attackers)

        if not self.initroll:
            self.curr_attacker = self.__selectAttacker.get()

        else:
            self.curr_attacker = self.attackers[0]
            self.__selectAttacker.set(self.curr_attacker)

        self.initroll = False
        self.curr_defender = self.__selectDefender.get()
        self.checkPhysicalCond(combatant = self.__findCombatant(name = self.curr_defender,
                                                                chklist = self.initlist),
                                                                side = "defender")
        at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)
        self.checkPhysicalCond(combatant = at, side = "attacker")

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
        self.__bleedAttacker.set(f"HP/rd: {at['status']['hits/rnd']}")
        self.__deathAttacker.set(f"Death:{at['status']['die']}")
        self.__getAttackType(event = None)
        self.__updOB(event = None)
        self.__updDefCombo(event = None)


    def __updDefCombo(self, event = None):
        '''!
        This method updates the list of the self.__defendCombo combobox and all
        widgets concerned by  the defender

        ----
        @todo following has to be implemented
        -set the currently selected defender
        '''

        self.curr_defender = self.__selectDefender.get()

        if self.curr_defender not in self.defenders:
            self.curr_defender = self.defenders[-1]

        self.curr_attacker = self.__selectAttacker.get()
        self.__defendCombo.configure(values = self.defenders)
        defend = self.__findCombatant(name = self.curr_defender, chklist = self.initlist)
        self.__AT.set(defend["AT"])
        self.__DB.set(defend["DB"])
        self.checkPhysicalCond(combatant = defend, side = "defender")

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
        self.__deathDefender.set(f"Death: {defend['status']['die']}")
        self.attackers = deepcopy(self.defenders)
        self.__updOB(event = None)


    def __nextRnd(self):
        '''!
        This method does all calculations to prepare the next combat round such as
        - subtracting hits per round
        - keeping track of states like 'stunned', "no parry", "parry only"
        - updating self.initlist (deleting dead monsters etc)

        ----
        @todo - check for stunned status: if stunned>0 add -25 to mod_total, but only once; if stunned becomes 0 remove malus
        - update attacker / defender list when combatant was killed

        '''
        self.combatround += 1
        rm = []
        self.__healingpoints.set(0)

        for i in range(0, len(self.initlist)):
            # bleeding
            self.initlist[i]["status"]["hits"] += self.initlist[i]["status"]["hits/rnd"]

            # status check
            #if self.initlist[i]["status"]["stunned"] >= 1:
            #    self.initlist[i]["status"]["mod_total"] -= 25

            for stat in ["parry", "no_parry", "ooo", "die", "stunned"]:

                if  self.initlist[i]["status"][stat] > 0:
                    self.initlist[i]["status"][stat] -= 1

            #mod check: remove modification after their rounds become 0
            rm_mod = []

            for j in range(0, len(self.initlist[i]["status"]["mod"])):
                self.initlist[i]["status"]["mod"][j]["rnd"] -= 1

                if "mod" in self.initlist[i]["status"]["mod"][j].keys():

                    if self.initlist[i]["status"]["mod"][j]["mod"] == 0 or self.initlist[i]["status"]["mod"][j]["rnd"] == 0:
                        rm_mod.append(j)
                        #self.initlist[i]["status"]["mod"]
                else:

                    if self.initlist[i]["status"]["mod"][j]["mod_attacker"] == 0 or self.initlist[i]["status"]["mod"][j]["rnd"] == 0:
                        rm_mod.append(j)

            # select killed combatants
            #if "player" not in self.initlist[i].keys() and (self.initlist[i]["status"]["hits"] < 1 or self.initlist[i]["status"]["die"] == 0):
            if (self.initlist[i]["status"]["hits"] < 1 or self.initlist[i]["status"]["die"] == 0):
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


    def __getAttackType(self, event = None):
        '''!
        This detemines the selected attack type an shows/hide the (not) needed
        Comboboxes for the skills
        '''
        self.curr_attacker = self.__selectAttacker.get()
        at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)
        selected = self.__selectType.get()
        self.__oblist = []

        if selected == attacktypes[self.lang][0]:

            for mob in at["OB melee"]:
                self.__oblist.append(mob[0])

        elif selected == attacktypes[self.lang][1]:

            for mob in at["OB missile"]:
                self.__oblist.append(mob[0])
        else:
            self.notdoneyet(f"{attacktypes[self.lang][2]}")

        self.__selectOB.set(self.__oblist[0])
        self.__obCombo.config(values = self.__oblist)
        self.__updOB(event = None)


    def __updOB(self, event = None):
        '''!
        This updates the attack credentials by the selected attack skills
        ---
        @bug ValueError: 'Battle_Axe' is not in list every time the first list is loaded
        '''
        self.curr_attacker = self.__selectAttacker.get()
        at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)
        self.curr_defender = self.__selectDefender.get()
        defend = self.__findCombatant(name = self.curr_defender, chklist = self.initlist)
        obtype = self.__selectType.get()
        selectedOB = self.__selectOB.get()
        index = self.__oblist.index(selectedOB)

        if obtype == attacktypes[self.lang][0]:
            self.__skill.set(at["OB melee"][index][1])

        elif obtype == attacktypes[self.lang][1]:

            if len(at["OB missile"][index]) > 1:
                self.__skill.set(at["OB missile"][index][1])

            else:
                self.__skill.set(at["OB missile"][index][0])

            if "DBm" in defend.keys():
                self.__DB.set(int(defend["DBm"]))

            else:
                self.__DB.set(0)

        if selectedOB.replace(" ", "_") in self.atlist:
            self.__selectAT.set(selectedOB.replace(" ", "_"))

        else:
            self.__selectAT.set(self.__determineAT(selectedOB))

        if defend["status"]["no_parry"] > 0 or defend["status"]["ooo"] > 0:
            self.__DB.set(0)

        if defend["status"]["stunned"] > 0:
            db = self.__DB.get()

            if db < 25:
                self.__DB.set(0)

            else:
                self.__DB.set(db - 25)

        self.__calcMod(event = None)


    def __determineAT(self, obname = ""):
        """!
        This method delivers the fitting Attack Table to weapons which have not their own.

        """
        result = "Broadsword"
        for elem in self.weaponlist:
            if obname == elem["item"]:
                result = elem["table"]
                break

        return result


    def __calcMod(self, event = None):
        """!
        This method applies during fight generated modifier to OB/DB
        @param evenet UI event given but not used
        """
        self.curr_attacker = self.__selectAttacker.get()
        at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)
        self.curr_defender = self.__selectDefender.get()
        defend = self.__findCombatant(name = self.curr_defender, chklist = self.initlist)

        modob = self.__skill.get() + at["status"]["mod_total"]
        moddb = self.__DB.get() + defend["status"]["mod_total"]

        if moddb < 0:
            moddb = 0

        self.__skill.set(modob)
        self.__DB.set(moddb)


    def __applyHealing(self, event = None):
        """!
        This method applies healing to the combatant

        @param event UI event given but not used
        """
        self.curr_attacker = self.__selectAttacker.get()
        at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist, result = "index")
        key = self.__selectHeal.get()
        value = self.__healingpoints.get()
        self.initlist[at]["status"][key] += value
        self.__updtAttckCombo(event = None)


    def __buildWin(self):
        """!
        This method builds the window content.
        """

        #------------ row 0
        self.atcanvas = Canvas(master = self.window,
                          width = 120,
                          height = 120,
                          bg = "green")
        self.atcanvas.grid(row = 0, rowspan = 5, column = 0, sticky = "NS")

        self.defcanvas = Canvas(master = self.window,
                          width = 120,
                          height = 120,
                          bg = "green")
        self.defcanvas.grid(row = 0, rowspan = 5, column = 6, sticky = "NS")
        self.__chgImg()

        #----- attacker
        self.__lvlAttacker = StringVar()
        self.__lvlAttacker.set("Lvl: 1")
        Label(self.window,
              textvariable = self.__lvlAttacker
              ).grid(column = 1, row = 0, sticky = W)

        self.__curHPAttacker = StringVar()
        self.__curHPAttacker.set("HP: 30/30")
        self.hits_at = Label(self.window,
                              textvariable = self.__curHPAttacker
                              )
        self.hits_at.grid(column = 2, row = 0, sticky = W)

        self.__ppAttacker = StringVar()
        self.__ppAttacker.set("PP: 0/0")
        self.pp_at = Label(self.window,
                          textvariable = self.__ppAttacker
                          )
        self.pp_at.grid(row = 0, column = 3, sticky = W)

        self.__wmodAttacker = StringVar()
        self.__wmodAttacker.set("Mods: 0")
        self.mod_at = Label(self.window,
                          textvariable = self.__wmodAttacker
                          )
        self.mod_at.grid(row = 0, column = 4, sticky = E)

        self.__bleedAttacker = StringVar()
        self.__bleedAttacker.set("HP/rd: 0")
        self.bleed_at = Label(self.window,
                          textvariable = self.__bleedAttacker
                          )
        self.bleed_at.grid(row = 0, column = 5, sticky = W)

        #------------------- Defender ------------------------------------------
        self.__lvlDefender = StringVar()
        self.__lvlDefender.set("Lvl: 1")
        Label(self.window,
              textvariable = self.__lvlDefender
              ).grid(column = 7, row = 0, sticky = W)

        self.__curHPDefender = StringVar()
        self.__curHPDefender.set("HP: 30/30")
        self.hits_def = Label(self.window,
                              textvariable = self.__curHPDefender
                              )
        self.hits_def.grid(column = 8, row = 0, sticky = W)

        self.__ppDefender = StringVar()
        self.__ppDefender.set("PP: 0/0")
        self.pp_def = Label(self.window,
                            textvariable = self.__ppDefender
                            )
        self.pp_def.grid(row = 0, column = 9, sticky = W)

        self.__wmodDefender = StringVar()
        self.__wmodDefender.set("Mods: 0")
        self.mod_def = Label(self.window,
                           textvariable = self.__wmodDefender
                          )
        self.mod_def.grid(row = 0, column = 10, sticky = W)

        self.__bleedDefender = StringVar()
        self.__bleedDefender.set("HP/rd: 0")
        self.bleed_def = Label(self.window,
                               textvariable = self.__bleedDefender
                              )
        self.bleed_def.grid(row = 0, column = 11, sticky = W)

        #----------- row 1 ---------------------------------------------------------
        #----- attacker
        self.__initAttacker = StringVar()
        self.__initAttacker.set("Init: 0")
        Label(self.window,
              textvariable = self.__initAttacker
              ).grid(row = 1, column = 1, sticky = W)

        self.__stunAttacker = StringVar()
        self.__stunAttacker.set(f'{labels["stunned"][self.lang]}: 0')
        self.stunned_at = Label(self.window,
                              textvariable = self.__stunAttacker
                              )
        self.stunned_at.grid(row = 1, column = 2, sticky = W)

        self.__parryAttacker = StringVar()
        self.__parryAttacker.set(f'{labels["parry"][self.lang]}: 0')
        self.parry_at = Label(self.window,
                              textvariable = self.__parryAttacker
                              )
        self.parry_at.grid(row = 1, column = 3, sticky = W)

        self.__noparryAttacker = StringVar()
        self.__noparryAttacker.set(f'{labels["no_parry"][self.lang]}: 0')
        self.noparry_at = Label(self.window,
                              textvariable = self.__noparryAttacker
                              )
        self.noparry_at.grid(row = 1, column = 4, sticky = W)

        self.__koAttacker = StringVar()
        self.__koAttacker.set("k.o.: 0")
        self.ooo_at = Label(self.window,
                          textvariable = self.__koAttacker
                          )
        self.ooo_at.grid(row = 1, column = 5, sticky = W)

        #------------------- Defender -----------------------------------------
        self.__initDefender = StringVar()
        self.__initDefender.set("Init: 0")
        Label(self.window,
              textvariable = self.__initDefender
              ).grid(row = 1, column = 7, sticky = W)

        self.__stunDefender = StringVar()
        self.__stunDefender.set(f'{labels["stunned"][self.lang]}: 0')
        self.stunned_def = Label(self.window,
                                textvariable = self.__stunDefender
                                )
        self.stunned_def.grid(row = 1, column = 8, sticky = W)

        self.__parryDefender = StringVar()
        self.__parryDefender.set(f'{labels["parry"][self.lang]}: 0')
        self.parry_def = Label(self.window,
                              textvariable = self.__parryDefender
                              )
        self.parry_def.grid(row = 1, column = 9, sticky = W)

        self.__noparryDefender = StringVar()
        self.__noparryDefender.set(f'{labels["no_parry"][self.lang]}: 0')
        self.noparry_def = Label(self.window,
                                textvariable = self.__noparryDefender
                                )
        self.noparry_def.grid(row = 1, column = 10, sticky = W)

        self.__koDefender = StringVar()
        self.__koDefender.set("k.o.: 0")
        self.ooo_def = Label(self.window,
                              textvariable = self.__koDefender
                              )
        self.ooo_def.grid(row = 1, column = 11, sticky = W)

        #------------ row 2
        self.__selectType = StringVar()
        self.__selectType.set(attacktypes[self.lang][0])
        self.__typeCombo = Combobox(self.window,
                                    textvariable = self.__selectType,
                                    values = attacktypes[self.lang])
        self.__typeCombo.bind("<<ComboboxSelected>>", self.__getAttackType)
        self.__typeCombo.grid(row = 2, column = 1, sticky = W)

        #---------- row 3
        #self.__selectSkill = StringVar()
        #self.__skillCombo = Combobox(self.window,
        #                            textvariable = self.__selectSkill,
        #                            values = ["--"])
        #self.__skillCombo.bind("<<ComboboxSelected>>", self.__getAttackType)

        self.__selectOB = StringVar()
        self.__selectOB.set("Battle_Axe")
        self.__obCombo = Combobox(self.window,
                        textvariable = self.__selectOB,
                        values = ["Battle_Axe"])
        self.__obCombo.bind("<<ComboboxSelected>>", self.__updOB)
        self.__obCombo.grid(row = 3, column = 1, sticky = W)

        self.__deathAttacker = StringVar()
        self.__deathAttacker.set("Death: -1")
        Label(self.window,
              textvariable = self.__deathAttacker
              ).grid(row = 3, column = 2, sticky = "W")

        #------------------- Defender -----------------------------------------
        self.__deathDefender = StringVar()
        self.__deathDefender.set("Death: -1")
        Label(self.window,
              textvariable = self.__deathDefender
              ).grid(row = 3, column = 7, sticky = "W")

        #------------ row 4

        #------------ row 5
        self.healings = ["hits", "hits/rnd", "stunned", "ooo", "mod_total", "die"]
        self.__selectHeal = StringVar()
        self.__selectHeal.set(self.healings[1])
        self.__healCombo = Combobox(self.window,
                                   textvariable = self.__selectHeal,
                                   values = self.healings)
        #self.__healCombo.bind("<<ComboboxSelected>>",self.__applyHealing)
        self.__healCombo.grid(row = 5, column = 1, sticky = W)

        self.__healingpoints = IntVar()
        self.__healingpoints.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__healingpoints
              ).grid(row = 5, column = 2, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__applyHealing
               ).grid(column = 3, row = 5, sticky = "EW")

        #------------ row 6
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

        #---------- row 7
        Button(self.window,
               text = txtbutton["but_nxtrd"][self.lang],
               command = self.__nextRnd
               ).grid(column = 0, row = 7, rowspan = 3, sticky = "EW")
        #------------ row 8

        #------------ row 9

        #------------ row 10

        Label(self.window,
              text = labels["attack table"][self.lang] + ":",
              ).grid(column = 0, row = 10, sticky = "W")

        ## @var self.atlist
        # List of names of Attack Tables
        self.atlist = list(self.attacktbls.keys())
        self.atlist.sort()
        self.__selectAT = StringVar()
        self.__selectAT.set(self.atlist[0])
        self.__ATOpt = Combobox(self.window,
                                 values = self.atlist,
                                 textvariable = self.__selectAT,
                                 width = 20)
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

        #------------ row 11

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

        #------------ row 12
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

        #------------ row 13
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


    def __setBGColor(self, attrib, bgcolor = "green"):
        """!

        @param attrib tkinter label object
        @param bgcolor background color to set

        """
        attrib.config(bg = bgcolor)


    def checkPhysicalCond(self, combatant, side = "defender"):
        """!
        This method checks the physical condition of an attacked combatant and defines
        a background color code for that condition.

        @param combatant SC / NSC to check the physical condition for
        @param side of the combatant: attacker, defender
        ----
        @todo - set text colors for entry boxes
        """
        ## @var condition_color
        # this holds the physical condition as index and the resulting color as value.
        condition_color = {"die": "black",
                           "ooo": "grey",
                           "no parry": "red",
                           "parry": "deepskyblue",
                           "critical": "darkred",
                           "bad": "darkorange",
                           "not so good":"yellow",
                           "good": "lime",
                           "stunned": "sandybrown",
                           "light bleeding": "khaki",
                           "medium bleeding":"orange",
                           "strong bleeding":"firebrick",
                           "no mod": "whitesmoke",
                           "no stun": "whitesmoke",
                           "no bleed": "whitesmoke",
                           "no bleeding":"whitesmoke",
                           "nono parry":"whitesmoke",
                           "attack again": "whitesmoke",
                           "awake":"whitesmoke",
                           "low mod":"lightgreen",
                           "medium mod":"gold",
                           "high mod": "coral",
                           "critical mod":"orangered"
                          }

        ## @var condition_color
        # this variable holds the color name which shall be finally set when the physical
        # condition is determined.
        condbgcolor = condition_color["good"]

        logger.debug(f"check data: \n{json.dumps(combatant,indent=4)}")
        ## @var hits
        # this holds the remaining hit points in pecent
        hits = combatant['status']["hits"] / int(combatant["hits"]) * 100

        if combatant["status"]["mod_total"] < -50:
            condbgcolor = condition_color["critical mod"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor)

        elif combatant["status"]["mod_total"] < -20:
            condbgcolor = condition_color["high mod"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor)

        elif combatant["status"]["mod_total"] < -9:
            condbgcolor = condition_color["medium mod"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor)

        elif combatant["status"]["mod_total"] < 0:
            condbgcolor = condition_color["low mod"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor)

        else:
            condbgcolor = condition_color["no mod"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor)

        if combatant["status"]["hits/rnd"] < 0:
            condbgcolor = condition_color["light bleeding"]

            if side == "defender":
                self.__setBGColor(attrib = self.bleed_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.bleed_at, bgcolor = condbgcolor)

        elif combatant["status"]["hits/rnd"] < -2:
            condbgcolor = condition_color["medium bleeding"]

            if side == "defender":
                self.__setBGColor(attrib = self.bleed_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.bleed_at, bgcolor = condbgcolor)

        elif combatant["status"]["hits/rnd"] < -6:
            condbgcolor = condition_color["strong bleeding"]

            if side == "defender":
                self.__setBGColor(attrib = self.bleed_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.bleed_at, bgcolor = condbgcolor)
        else:
            condbgcolor = condition_color["no bleeding"]

            if side == "defender":
                self.__setBGColor(attrib = self.bleed_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.bleed_at, bgcolor = condbgcolor)

        if combatant["status"]["stunned"] > 0:
            condbgcolor = condition_color["stunned"]

            if side == "defender":
                self.__setBGColor(attrib = self.stunned_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.stunned_at, bgcolor = condbgcolor)
        else:
            condbgcolor = condition_color["no stun"]

            if side == "defender":
                self.__setBGColor(attrib = self.stunned_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.stunned_at, bgcolor = condbgcolor)

        if combatant["status"]["no_parry"] > 0:
            condbgcolor = condition_color["no parry"]

            if side == "defender":
                self.__setBGColor(attrib = self.noparry_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.noparry_at, bgcolor = condbgcolor)

        else:
            condbgcolor = condition_color["nono parry"]

            if side == "defender":
                self.__setBGColor(attrib = self.noparry_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.noparry_at, bgcolor = condbgcolor)

        if combatant["status"]["ooo"] > 0:
            condbgcolor = condition_color["ooo"]

            if side == "defender":
                self.__setBGColor(attrib = self.ooo_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.ooo_at, bgcolor = condbgcolor)

        else:
            condbgcolor = condition_color["awake"]

            if side == "defender":
                self.__setBGColor(attrib = self.ooo_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.ooo_at, bgcolor = condbgcolor)

        if combatant["status"]["parry"] > 0:
            condbgcolor = condition_color["parry"]

            if side == "defender":
                self.__setBGColor(attrib = self.parry_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.parry_at, bgcolor = condbgcolor)

        else:
            condbgcolor = condition_color["attack again"]

            if side == "defender":
                self.__setBGColor(attrib = self.parry_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.parry_at, bgcolor = condbgcolor)

        if hits == 0.0:
            condbgcolor = condition_color["dead"]

        elif hits < 10.0:
            condbgcolor = condition_color["critical"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.hits_at, bgcolor = condbgcolor)

        elif hits < 25.0:
            condbgcolor = condition_color["bad"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.hits_at, bgcolor = condbgcolor)

        elif hits < 76.0:
            condbgcolor = condition_color["not so good"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.hits_at, bgcolor = condbgcolor)

        elif hits > 75.0:
            condbgcolor = condition_color["good"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.hits_at, bgcolor = condbgcolor)

        if combatant["status"]["die"] >= 0:
            condbgcolor = condition_color["die"]

        if side == "defender":
            self.defcanvas.config(bg = condbgcolor)

        elif side == "attacker":
            self.atcanvas.config(bg = condbgcolor)



class enemySelector(blankWindow):
    '''
    This class opens a window to select differnt monsters or npcs from a data
    file (CSV). This selection
    '''


    def __init__(self, lang = "en", datapool = ""):
        '''
        @param lang chosen display language (default: en; supported; en, de)
        @param datapool (path +) file where the default bestiarium is stored in.
        ----
        '''
        ##\var self.lang
        # display language
        self.lang = lang
        ##\var self.datapool
        # path + file name of the default monster data file.
        self.datapool = datapool
        ##\var self.selection
        # a list of selected monsters/nscs (list of dictionaries)
        self.selection = []
        ## \var self.fmaske
        # file extension mask for "file open" window.
        self.fmaske = [txtwin['enemygrp_files'][self.lang],
                     txtwin['all_files'][self.lang]]

        blankWindow.__init__(self, self.lang)
        self.window.title("Selector: Monster")
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addFileMenu(self):
        '''!
        This methods adds the file menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open_enemy'],
                                  command = self.openNPCs)
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
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_sel_enemy"],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_mod_enemy"],
                                  command = self.notdoneyet)


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


    def getSelection(self):
        '''
        getter method for selection of npcs/monsters
        '''
        return self.selection


    def __quit(self):
        '''!
        This method closes the window
        '''
        self.window.destroy()


    def openNPCs(self):
        """
        This method opens a file of npc/monstaer data for read out.
        """
        ## \var self.__npcpath
        # path+ file name of selected data file
        self.__npcpath = askopenfilename(filetypes = self.fmaske, defaultextension = "*.csv", initialdir = os.getcwd())
        logger.debug(f"openNPCs: chosen npc/monster group file {self.__npcpath}")

        if self.__npcpath[-4:].lower() == ".csv":
            ##\var self.npcgrp
            # content of npc/monster file (csv)
            self.npcgrp = readCSV(self.__enemypath)
            logger.info(f'openNPCs: {self.__enemypath} read successfully.')

        else:
            logger.error("openNPCs: wrong file format! must be CSV!")
            self.message("openNPCs: wrong file format: must be CSV!")

        pass


    def __buildWin(self):
        """
        This method build the window with all elements

        ----
        @todo has to be fully implemented
        """
        pass

#class characterSelector(blankWindow):
#    '''!
#    This class adds a single character to the list.
#    '''
#
#
#    #def __init__(self, lang = "en", datapool):
#    def __init__(self, lang = "en", datapool):
#        '''!
#        @todo has to be fully implemented
#        '''
#        self.lang = lang
#        self.dp = datapool
#        #blankWindow.__init__(self, self.lang)
#        #self.window.title("Combat  Module")
#        #self.__addFileMenu()
#        #self.__addEditMenu()
#        #self.__addHelpMenu()
#        #self.__buildWin()
#        self.window.mainloop()
#        pass
#
#
#    def __addHelpMenu(self):
#        """!
#        This methods defines a help menu.
#        """
#        self.helpmenu = Menu(master = self.menu)
#        self.menu.add_cascade(label = txtmenu['help'][self.lang],
#                              menu = self.helpmenu)
#
#        self.helpmenu.add_separator()
#        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
#                                  command = self._helpAbout)
#        logger.debug("__addHelpMenu: help menu build")
#
#
#    def getSelection(self):
#        '''!
#        getter method for selection
#        '''
#        return self.selection
#
#
#    def __quit(self):
#        '''!
#        This method closes the window
#        '''
#        self.window.destroy()



if __name__ == '__main__':
    win = atWin()
