#!/usr/bin/env python3
'''!
\file attackcheck.py
\package attackcheck
\brief Thia program can be used to  get the results of  attack and critical tables

lorem ipsum

\date (c) 2021
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "07.08.2021"
__author__ = "Marcus Schwamberger"

import os
import json
from tkinter import filedialog
from tkinter.ttk import Combobox

from rpgtoolbox.combat import *
#from rpgtoolbox.rpgtools import dice
from rpgToolDefinitions.helptools import RMDice as Dice
from gui.window import *
from rpgtoolbox import logbox as log
from rpgtoolbox.globaltools import *

logger = log.createLogger('AT-Window', 'debug', '1 MB', 1, './', logfile = "attackcheck.log")



class atWin(blankWindow):
    """!
    This class generates a window where you can look up your attack results.
    Results of dice rolls may be entered or a roll may be done by clicking a
    button.
    """


    def __init__(self, lang = "en", datadir = "data/default"):
        """!
        Constructor
        \param lang selected output language
        \param datadir configured default datadir
        """
        self.lang = lang
        self.datadir = datadir
        self.attacktbls = {}
        self.crittbls = {}
        self.__partypath = None
        self.partygrp = None
        self.__enemypath = None
        self.enemygrp = None
        self.mask = [txtwin['json_files'][self.lang],
                     txtwin['grp_files'][self.lang],
                     txtwin['csv_files'][self.lang],
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
        self.window.title("Attack  & Crit Table Checker")
        self.__addMenu()
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


    def __addMenu(self):
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


    def openParty(self):
        '''!
        This method reads a character party group file to self.partygrp
        '''
        self.__partypath = askopenfilename(filetypes = self.mask, initialdir = os.getcwd())
        logger.debug(f"openParty: chosen group file {self.__partypath}")
        try:
            with open(self.__partypath, "r") as fp:
                ##@var self.__fullparty
                # This is holding the full party data
                self__fullparty = json.load(fp)
                logger.info(f"openParty: {self.__partypath} was read")
                #xxxxxxx

        except Exception as error:
            logger.error(f"openParty: {error}")
            self.message(f"openParty: {error}")


    def openEnemies(self):
        '''!
        This opens an enemy party to fight against
        '''
        self.__enemypath = askopenfilename(filetypes = self.mask, initialdir = os.getcwd())
        logger.debug(f"openEnemies: chosen enemies group file {self.__enemiespath}")

        if self.__enemypath[-4:].lower() == ".csv":
            self.enemygrp = readCSV(self.__enemypath)
        pass


    def __quit(self):
        '''!
        This method closes the window
        '''
        self.window.destroy()


    def __rollAttack(self):
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


    def __buildWin(self):
        """!
        This method builds the window content.

        ----
        @todo the row 0 has to be build:\n
        Initative | Attacker | DEfender (pd) | next button

        """
        # row 0

        # row 1
        Label(self.window,
              text = labels["attack table"][self.lang] + ":",
              ).grid(column = 0, row = 0, sticky = "W")

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
                          row = 1,
                          sticky = "W")

        Label(self.window,
              text = labels['skill'][self.lang] + ":"
              ).grid(column = 2, row = 1, sticky = "W")

        self.__skill = IntVar()
        self.__skill.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__skill,
              width = 5
              ).grid(column = 3, row = 1, sticky = "EW")

        Label(self.window,
              text = labels['roll'][self.lang] + ":"
              ).grid(column = 4, row = 1, sticky = "W")

        self.__atroll = IntVar()
        self.__atroll.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__atroll,
              width = 5
              ).grid(column = 5, row = 1, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_roll"][self.lang],
               command = self.__rollAttack
               ).grid(column = 6, row = 1, sticky = "EW")

        Label(self.window,
              text = "AT:"
              ).grid(column = 7, row = 1, sticky = "W")

        self.__AT = StringVar()
        self.__AT.set("1")
        Entry(self.window,
              textvariable = self.__AT,
              width = 5,
              justify = "center"
              ).grid(column = 8, row = 1, sticky = "EW")

        Label(self.window,
              text = "max:"
              ).grid(column = 9, row = 1, sticky = "W")

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
        self.__maxOpt.grid(column = 10, row = 1, sticky = "W")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self.checkAttack
               ).grid(column = 11, row = 1, sticky = "EW")

        # row 2

        self.__resultAT = StringVar()
        self.__resultAT.set("--")
        Label(self.window,
              justify = "center",
              textvariable = self.__resultAT,
              borderwidth = 2,
              relief = "sunken"
              ).grid(column = 0, columnspan = 6, row = 2, sticky = "EW", pady = 2)

        Label(self.window,
              text = "DB:"
              ).grid(column = 7, row = 2, sticky = "E")

        self.__DB = IntVar()
        self.__DB.set(0)
        Entry(self.window,
              textvariable = self.__DB,
              width = 5,
              justify = "center"
              ).grid(column = 8, row = 2, sticky = "EW")

        # row 3
        Label(self.window,
              text = labels["crit table"][self.lang] + ":"
              ).grid(column = 0, row = 3, sticky = "W")

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
        self.__CritOpt.grid(column = 1, row = 3, sticky = "W")

        Label(self.window,
              text = "Crit:"
              ).grid(column = 2, row = 3, sticky = "W")

        self.__critType = StringVar()
        self.__critType.set("")
        Entry(self.window,
              justify = "center",
              width = 5,
              textvariable = self.__critType
              ).grid(column = 3, row = 3, sticky = "EW")

        Label(self.window,
              text = labels['roll'][self.lang] + ":"
              ).grid(column = 4, row = 3, sticky = "W")

        self.__critroll = IntVar()
        self.__critroll.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__critroll,
              width = 5
              ).grid(column = 5, row = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_roll"][self.lang],
               command = self.__rollCrit
               ).grid(column = 6, row = 3, sticky = "EW")

        Label(self.window,
              text = labels["weapon"][self.lang] + ":"
              ).grid(column = 7, columnspan = 2, row = 3, sticky = "W")

        self.__weaponType = StringVar()
        self.__weaponType.set(weapontypes["en"][0])

        self.__weaponOpt = OptionMenu(self.window,
                                      self.__weaponType,
                                      *weapontypes["en"]
                                      )
        self.__weaponOpt.grid(column = 9, columnspan = 2, row = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self.checkCrit
               ).grid(column = 11, row = 3, sticky = "EW")

        # row 4
        vscroll = Scrollbar(self.window, orient = VERTICAL)
        self.__displayCrit = Text(self.window,
                                  yscrollcommand = vscroll.set,
                                  height = 20
                                  )
        vscroll.config(command = self.__displayCrit.yview)
        self.__displayCrit.grid(column = 0, columnspan = 12, row = 4, sticky = "NEWS")


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
