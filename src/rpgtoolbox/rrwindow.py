#!/usr/bin/env python
'''!
@file rrwindow.py
@package rpgtoolbox
@brief This holds the GUI for Resistance Rolls

Resistance Rolls Package

@date (c) 2020 - 2022
@license GNU V3.0
@author Marcus Schwamberger
@email marcus@lederzeug.de
@version 0.1
'''

import os
import json
from gui.window import *
from rpgtoolbox import epcalc, rpgtools as rpg
from rpgToolDefinitions.epcalcdefs import maneuvers
from pprint import pprint
from rpgToolDefinitions.helptools import RMDice as dice
from rpgtoolbox.rpgtools import RRroll
from tkinter import filedialog
from . import logbox as log
from rpgtoolbox.confbox import *

__version__ = "0.1"
__updated__ = "03.10.2022"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__copyright__ = "2018 - %s" % __updated__[-4:]
__version__ = "0.1"

mycnf = chkCfg()
logger = log.createLogger('RR', 'debug', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = 'rrwindow.log')



class RRWin(blankWindow):
    """
    This is a GUI for Resistance Rolls for your character party and NSCs.
    """


    def __init__(self, lang = "en", selected = "", charlist = [], storepath = "./data"):
        """!
        Class constructor RRWin
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param charlist list of dictionaries holding: player, charname, EPs
        @param storepath path for storing the data into the character files.
        """

        self.lang = lang
        self.charlist = charlist
        self.selP = selected
#
#        if self.charlist == []:
#            self.charlist.append({  "player": "Nobody",
#                                    "exp": 10000,
#                                    "lvl": 1,
#                                    "prof": "Layman",
#                                    "name": "Nobo Dy",
#                                    "RRArc": 0,
#                                    "RRC/E": 0,
#                                    "RRC/M": 0,
#                                    "RRChan": 0,
#                                    "RRDisease": 0,
#                                    "RRE/M": 0,
#                                    "RREss": 0,
#                                    "RRFear": 0,
#                                    "RRMent": 0,
#                                    "RRPoison": 0
#                                })
        self.storepath = storepath
        self.dice = dice
        blankWindow.__init__(self, self.lang)
        self.window.title(wintitle["rm_RR"][self.lang])
        self.__addMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addMenu(self):
        '''
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__open)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)


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


    def __open(self):
        '''
        This opens a file dialog window for opening a character or group file.
        '''
        self.targets = []
        opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Char (Group) Files", ".json")])

        with open(opendir, "r") as fp:
            self.charlist = json.load(fp)

        #set up new player group list

#        self.group = {}
#        for elem in self.charlist:
#            self.players.append(elem["player"])
#        self.players.append("ALL")
#        self.__selectPlayer.set(self.players[-1])
        self.__buildWin()

        if type(self.charlist) == type([]):
            self.targets += self.charlist

        elif type(self.charlist) == type({}):
            self.targets.append(self.charlist)

        else:
            print("Error:Wrong file content")
            messageWindow("WARNING: Could not compute file: wrong content!")
            pass
#            for elem in self.charlist:
#                self.players.append(elem["player"])
#                self.group[elem["player"]] = epcalc.experience(elem["player"], elem["exp"])
#                self.group[elem["player"]].updateInfo()

#        self.__selecPlayer.set(self.players[0])
#        self.__playerOpt = OptionMenu(self.window,
#                                      self.__selecPlayer,
#                                      *self.players,
#                                      command = self.__updSelec)
#        self.__playerOpt.grid(column = 0, row = 0, sticky = "W")


    def __quit(self):
        '''!
        This method closes the window
        '''
        self.window.destroy()


    def __buildWin(self):
        """
        This method builds the window content.
        """
        self.players = []
#        self.group={}

        for elem in self.charlist:
            self.players.append(elem["player"])

        self.players.append("ALL")
        self.__selectPlayer = StringVar(self.window)

        if self.selP:
            self.__selectPlayer.set(self.selP)
        else:
            self.__selectPlayer.set(self.players[0])

        self.__playerOpt = OptionMenu(self.window,
                                      self.__selectPlayer,
                                      *self.players,
                                      command = self.__updSelec

                                      )
        self.__playerOpt.config(width = 10)
        self.__playerOpt.grid(column = 0, row = 0, padx = 1, pady = 1, sticky = "WE")
        self.__charname = StringVar(self.window)

        if self.selP:
            self.__charname.set("{} ({})".format(self.charlist[self.players.index(self.selP)]["name"],
                                                 self.charlist[self.players.index(self.selP)]["lvl"]))
        else:
            self.__charname.set("ALL")

        # row 0
        Label(self.window,
              width = 20,
              textvariable = self.__charname,
              ).grid(row = 0, column = 1, sticky = "W")

#        self.rrlist = ['RRArc', 'RRC/E', 'RRC/M', 'RRChan', 'RRDisease', 'RRE/M', 'RREss', 'RRFear', 'RRMent', 'RRPoison']
        self.rrlist = rrtypes[self.lang]
        self.__selectRR = StringVar(self.window)
        self.__selectRR.set(self.rrlist[0])
        self.__playerOpt = OptionMenu(self.window,
                                      self.__selectRR,
                                      *self.rrlist,
                                      command = self.__updSelec)
        self.__playerOpt.grid(column = 2, row = 0, sticky = "WE")

        #row 1
        Label(self.window,
              text = labels["roll"][self.lang] + ":",
              justify = LEFT
              ).grid(column = 0,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        self.diceroll = IntVar(self.window)
        self.diceroll.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.diceroll,
              ).grid(row = 1, column = 1, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_roll"][self.lang],
               command = self.__rollDice,
               bg = "grey",
               fg = "white",
#               image = "./data/default/pics/d10.png"
               ).grid(row = 1, column = 2, sticky = "NEWS")

        # row 2
#        self.attacker = StringVar()
        Label(self.window,
              text = labels["attack lvl"][self.lang] + ":",
              justify = LEFT
              ).grid(column = 0,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        self.atcklvl = IntVar(self.window)
        self.atcklvl.set(1)
        Entry(self.window,
              justify = "center",
              textvariable = self.atcklvl,
              ).grid(row = 2, column = 1, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self.__checkResult,
               bg = "grey",
               fg = "white",
#               image = "./data/default/pics/d10.png"
               ).grid(row = 2, column = 2, sticky = "NEWS")
        #row 3
        vscroll = Scrollbar(self.window, orient = VERTICAL)
        self.displayTxt = Text(self.window,
                               yscrollcommand = vscroll.set,
                               height = 10
                               )
        vscroll.config(command = self.displayTxt.yview)
#        vscroll.grid(row = 2, colum = 10, sticky = "NSW")
        self.displayTxt.grid(row = 3,
                             column = 0,
                             columnspan = 3,
                             sticky = "NEWS")


    def __rollDice(self):
        '''!
        This trows a d100. Result ist ([dice result], [unmodified])
        ----
        @todo set dice(rules="RM")
        '''
        self.result = self.dice()

        if self.result[1] == []:
            self.diceroll.set(str(self.result[0][0]))
        else:
            self.diceroll.set("um {}".format(self.result[1][0]))


    def __checkResult(self):
        """!
        checks the result from the RR test

        """
        chklist = []
        self.displayTxt.delete("1.0", "end")
        if self.__charname.get() == "ALL":
            chklist += self.charlist
        else:
            ind = self.players.index(self.__selectPlayer.get())
            chklist.append(self.charlist[ind])

        result = ""

        for elem in chklist:
            rrcat = rrtypes["param"][self.rrlist.index(self.__selectRR.get())]
            roll = self.diceroll.get() + int(elem[rrcat])
            targetlvl = elem["lvl"]
            rrres = RRroll(self.atcklvl.get(), targetlvl, roll)
            if rrres[0]:
                erg = labels["success"][self.lang]
            else:
                erg = labels["fail"][self.lang]
            result += "{} ({}): {} -> {}\n".format(elem["name"], elem["player"], erg, roll - rrres[1])

        self.displayTxt.insert(END, result)


    def __updSelec(self, event):
        """!
        Update Selected Character Data

        """
        selected = self.__selectPlayer.get()
        ind = self.players.index(selected)
        if selected != "ALL":
            self.__charname.set("{} ({})".format(self.charlist[ind]["name"],
                                                 self.charlist[ind]["lvl"]))
        else:
            self.__charname.set("ALL")
