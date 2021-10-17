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
__updated__ = "17.10.2021"
__author__ = "Marcus Schwamberger"

import os
import json
from tkinter import filedialog
from tkinter.ttk import Combobox
from pprint import pformat

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


    def openParty(self):
        '''!
        This method reads a character party group file to self.partygrp
        '''
        self.__partypath = askopenfilename(filetypes = self.fmask, initialdir = os.getcwd())
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
        self.__enemypath = askopenfilename(filetypes = self.fmask, initialdir = os.getcwd(), defaultextension = ".csv")
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
        @todo - the weapon short terms have to be replaced by the full names to get
              the right weapon table.
              - immunity list
              - weakness list
        '''
        size = "H"
        pprint(self.enemygrp)
        self.enemygrp = createCombatList(self.enemygrp)
        for i in range(0, len(self.enemygrp)):

            enc = self.enemygrp[i]["enc"].split("-")
            print(f"Debug: {self.enemygrp[i]} --> Enc {enc}")
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

                    self.enemygrp[i]["spells"] = spellists.copy()

                else:
                    self.enemygrp[i]["spells"] = []

            else:
                self.enemygrp[i]["spells"] = []

            self.enemygrp[i]["init"] = 0

        self.initlist += self.enemygrp
        self.attackers = []

        for elem in self.initlist:
            self.attackers.append(elem["name"])

        self.defenders = self.attackers.copy()
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
        @todo learned spell casting lists have to be selected and added
        '''
        self.partygrp = []
        cindex = ["player", "name", "DB", "DB mod", "OB melee", "OB missile", "hits", "PP",
                "AT", "lvl", "spell", "init", "piclink"]

        melee = ["Martial Arts - Striking", "Martial Arts - Sweeps", "Weapon - 1-H Concussion",
                "Weapon - 1-H Edged", "Weapon - 2-Handed", "Weapon - Pole Arms",
                "Weapon - 1-H Concussion", "Weapon - 1-H Edged", "Weapon - 2-Handed", "Special Attacks"]
        missile = ["Weapon - Missile", "Weapon - Missile Artillery", "Weapon - Thrown", "Directed Spells"]

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
            dummy["pp"] = char["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"]
            dummy["OB melee"] = []
            dummy["OB missile"] = []
            dummy["spell"] = []
            dummy["weapon type"] = [[], []]

            for m in melee:

                for skill in char["cat"][m]["Skill"].keys():

                    if skill not in ["Progression", "Stats"] and "+" not in skill:
                        dummy["OB melee"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"])

            for m in missile:

                for skill in char["cat"][m]["Skill"].keys():

                    if skill not in ["Progression", "Stats"] and "+" not in skill:
                        dummy["OB missile"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"]])
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
        self.defenders = self.attackers.copy()
        self.__updtAttckCombo()
        self.__updDefCombo()


    def __quit(self):
        '''!
        This method closes the window
        '''
        self.window.destroy()


    def __rollInit(self):
        '''!
        This rolls the initiative

        ----
        @todo: has to be fully implemented:
        - roll 6 store initative
        - sort list by intiative and build a name list in that order (for combobox)
        - update attacker combobox
        '''
        pass


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


    def __findCombatant(self, name = "Egon", chklist = ["Egon"]):
        """!
        this method returns the combatant data for the given name
        @param name of the combatant to search for
        @return the conbatant's data dictionary
        """
        for elem in chklist:
            #pprint(elem)
            if name == elem["name"]:
                return elem

        return {"name":"Egon"}


    def __updtAttckCombo(self, event = None):
        '''!
        This method updates the list of the self.__attackCombo combobox

        ----
        @todo following has to be implemented
        - set the current character

        '''

        self.__attackCombo.configure(values = self.attackers)
        #self.__attackCombo.current(self.curr_attacker)
        self.curr_attacker = self.__selectAttacker.get()
        self.curr_defender = self.__selectDefender.get()
        #print(f"Debug: {self.curr_attacker} --> {self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)}\n {self.attackers}")
        at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)
        print("---------\nAttacker\n\n")
        pprint(at)

        if "piclink" in at.keys():
            imglink = at["piclink"]
        else:
            imglink = "./data/default/pics/default.jpg"

        self.__chgImg(attackerpic = imglink, defenderpic = None)


    def __updDefCombo(self, event = None):
        '''!
        This method updates the list of the self.__defendCombo combobox

        ----
        @todo following has to be implemented
        -set the currently selected defender
        '''

        #self.__defendCombo.current(self.curr_defender)
        self.curr_defender = self.__selectDefender.get()
        self.curr_attacker = self.__selectAttacker.get()
        self.__defendCombo.configure(values = self.defenders)
        defend = self.__findCombatant(name = self.curr_defender, chklist = self.initlist)
        #print(f"{self.defenders}")
        print("********\nDefender\n\n")
        pprint(defend)

        self.__AT.set(defend["AT"])
        self.__DB.set(defend["DB"])
        if "piclink" in defend.keys():
            imglink = defend["piclink"]
        else:
            imglink = "./data/default/pics/default.jpg"

        self.__chgImg(attackerpic = None, defenderpic = imglink)


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

        #atlabel = Label(master = self.window,
        #              image = ImageTk.PhotoImage(Image.open(self.defaultnscimg).resize((80, 80), Image.ANTIALIAS)),
        #              text = "PC"
        #
        #              )
        #atlabel.grid(column = 0, row = 0, rowspan = 2, sticky = "NEWS")
        #
        #deflabel = Label(master = self.window,
        #              image = ImageTk.PhotoImage(Image.open(self.defaultnscimg).resize((60, 60), Image.ANTIALIAS)),
        #              text = "NPC"
        #              )
        #deflabel.grid(column = 7, row = 0, sticky = "NEWS")
        #self.window.update_idletasks()

        self.atcanvas = Canvas(master = self.window,
                          width = 90,
                          height = 90,
                          bg = "green")
        self.atcanvas.grid(row = 0, rowspan = 3, column = 0, sticky = "NEWS")

        self.defcanvas = Canvas(master = self.window,
                          width = 90,
                          height = 90,
                          bg = "green")
        self.defcanvas.grid(row = 0, rowspan = 3, column = 7, sticky = "NEWS")
        self.__chgImg()
        # row 1

        # row 2

        # row 3

        # row 4

        self.__selectAttacker = StringVar()
        self.__selectAttacker.set("Egon")
        self.__attackCombo = Combobox(self.window,
                                      textvariable = self.__selectAttacker,
                                      values = self.attackers)
        self.__attackCombo.bind("<<ComboboxSelected>>", self.__updtAttckCombo)
        self.__attackCombo.grid(column = 0, row = 4, sticky = "W")
        #Label(master = self.window,
        #      text = "PC Name"
        #      ).grid(row = 4, column = 0, sticky = "EW")

        self.__selectDefender = StringVar()
        self.__selectDefender.set("Anton")
        self.__defendCombo = Combobox(self.window,
                                      textvariable = self.__selectDefender,
                                      values = self.defenders)
        self.__defendCombo.bind("<<ComboboxSelected>>", self.__updDefCombo)
        self.__defendCombo.grid(column = 7, row = 4, sticky = "EW")
        #Label(master = self.window,
        #      text = "NPC Name"
        #      ).grid(row = 4, column = 7, sticky = "EW")
        # row 5

        # row 6

        # row 7

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

            if self.crittbls[self.__selectCrit.get()].crithit["damage_type"] == "":
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
