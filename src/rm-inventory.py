#!/usr/bin/python3
'''
\file rm-inventory.py
\package rm_char_tools.py
\brief This is a little tool for creating and keeping track of character's inventory

This tool handles
\li buying/finding/selling/dropping items
\li enchanting items
\li design special items
\li equipp items/pack items into containers and calculate carried weights
\li Export inventory as JSON, LaTex, PDF

\date (C) 2020
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 1.1.0

'''
import os
import json
import random
from gui.window import *
from gui.winhelper import AutoScrollbar
from rpgtoolbox import epcalc, rpgtools as rpg
from rpgToolDefinitions.epcalcdefs import maneuvers
from rpgToolDefinitions.inventory import *
from rpgtoolbox.rolemaster import realms, spellists
from rpgToolDefinitions import inventory as inv
from tkinter import filedialog
from tkinter.ttk import *
import re
from PIL import Image, ImageTk
from pprint import pprint

__updated__ = "11.06.2020"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__version__ = "0.5"



class InventoryWin(blankWindow):
    """
    This is a GUI character's inventory window.
    """


    def __init__(self, lang = "en", char = {}, storepath = "./data"):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param charlist list of dictionaries holding: player, charname, EPs
        \param storepath path for storing the data into the character files.
        """

        self.lang = lang
        self.character = char

        if self.character == {}:
            self.character = {  "player": "Marcus",
                                "exp": 10000,
                                'lvl' :1,
                                "prof": "Ranger",
                                "race" : "Woodmen",
                                "name": "Woody",
                                'realm' : 'Channeling',
                                "piclink" : "./data/default/pics/default.jpg"

                                }
        self.wcont = {}
        self.filterlist = ['player', 'exp', 'lvl', 'prof', 'race', 'name', 'piclink', 'realm']
        self.bgfilter = ['act_age', 'carr_weight', "sex", "height", "weight"]
        self.storepath = storepath
        blankWindow.__init__(self, self.lang)
        self.window.title("Rucksack")
        self.__addMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addMenu(self):
        '''
        This method adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__open)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)
        self.invmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_inventory'][self.lang],
                              menu = self.invmenu)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]['armor'],
                                 command = self.__armor)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]['weapon'],
                                 command = self.__weapon)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]['gear'],
                                                 command = self.__gear)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["gems"],
                                 command = self.__gems)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["herbs"],
                                 command = self.__herbs)
        self.invmenu.add_separator()
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["spells"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["daily"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["PP_spell"],
                                  command = self.notdoneyet)
        self.invmenu.add_separator()
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["transport"],
                                 command = self.__transport)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["services"],
                                 command = self.__services)


    def __addHelpMenu(self):
        """
        This method defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __buildWin(self):
        """
        This method defines the window's layout
        """
        self.updWidgedCont()
        self.picLabel = Label(master = self.window,
                              image = self.wcont['piclink']
                              )
        # row 0
        self.picLabel.grid(column = 0,
                           row = 0,
                           columnspan = 2,
                           rowspan = 8,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)
        Label(self.window,
              textvariable = self.wcont["player"],
              justify = LEFT
              ).grid(column = 2,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["exp"],
              justify = LEFT
              ).grid(column = 3,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = "Level:",
              justify = RIGHT
              ).grid(column = 4,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["lvl"],
              justify = LEFT
              ).grid(column = 5,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        # row 1
        Label(self.window,
              textvariable = self.wcont["name"],
              justify = LEFT
              ).grid(column = 2,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["sex"],
              justify = LEFT
              ).grid(column = 3,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["prof"],
              justify = LEFT
              ).grid(column = 4,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["race"],
              justify = LEFT
              ).grid(column = 5,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 2
        Label(self.window,
              text = charattribs['act_age'][self.lang] + ":"
              ).grid(column = 2,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["act_age"]
              ).grid(column = 3,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = charattribs['height'][self.lang] + ":"
              ).grid(column = 4,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["height"]
              ).grid(column = 5,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 3
        Label(self.window,
              text = charattribs['weight'][self.lang] + ":",
              justify = RIGHT,
              ).grid(column = 2,
                     row = 3,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["weight"]
              ).grid(column = 3,
                     row = 3,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        #row 4
        Label(self.window,
              text = charattribs['carr_weight'][self.lang] + ":"
              ).grid(column = 2,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["carr_weight"]
              ).grid(column = 3,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = labels['MMP'][self.lang] + ":"
              ).grid(column = 4,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["MMP"]
              ).grid(column = 5,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        # row 5/6
        c = 2
        for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
            Label(self.window,
                  text = coin + ":",
                  ).grid(column = c,
                         row = 5,
                         padx = 1,
                         pady = 1,
                         sticky = "EW"
                         )
            Label(self.window,
                  textvariable = self.wcont[coin],
                  ).grid(column = c,
                         row = 6,
                         padx = 1,
                         pady = 1,
                         sticky = "EW"
                         )
            c += 1


    def updWidgedCont(self):
        '''
        This method updates widget content like texts or images
        '''

        for elem in self.filterlist:

            if elem == "piclink":

                if elem in self.wcont.keys():
                    self.wcont[elem] = ImageTk.PhotoImage(Image.open(self.character[elem]).resize((210, 210), Image.ANTIALIAS))
                    self.picLabel.config(image = self.wcont[elem])

                else:
                    self.wcont[elem] = ImageTk.PhotoImage(Image.open(self.character[elem]).resize((210, 210), Image.ANTIALIAS))

            elif type(self.character[elem]) == type(""):

                if elem not in self.wcont.keys():
                    self.wcont[elem] = StringVar()

                self.wcont[elem].set(self.character[elem])

            elif type(self.character[elem]) == type(0):
                if elem not in self.wcont.keys():
                    self.wcont[elem] = IntVar()

                self.wcont[elem].set(self.character[elem])

        for elem in self.bgfilter:

            if "background" in self.character.keys():

                if type(self.character["background"][elem]) == type(""):

                    if elem not in self.wcont.keys():
                        self.wcont[elem] = StringVar()

                    self.wcont[elem].set(self.character["background"][elem])

                elif type(self.character["background"][elem]) == type(0):

                    if elem not in self.wcont.keys():
                        self.wcont[elem] = IntVar()

                    self.wcont[elem].set(self.character["background"][elem])
            else:
                self.wcont[elem] = StringVar()
                self.wcont[elem].set("--")

        if "MMṔ" not in self.wcont.keys():
            self.wcont["MMP"] = IntVar()
            self.wcont["MMP"].set(0)

        elif "MMP" not in self.character.keys():
            self.character["MMP"] = calcMMP(self.character)
            self.wcont["MMP"].set(self.character["MMP"])

        for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
            if "purse" not in self.character.keys():
                self.character["purse"] = {}

            if coin not in self.character['purse'].keys():
                self.character["purse"][coin] = 0

            if coin not in self.wcont.keys():
                self.wcont[coin] = IntVar()

            self.wcont[coin].set(self.character["purse"][coin])


    def calcMMP(self, char = {}):
        """
        This method calculates the Movement Maneuver Penalty (MMP)
        @param char full character data as dictionary
        @retval mmp Movement Maneuver Penalty as integer
        ----
        @todo has to be fully implemented
        """
        mmp = 0
        return mmp


    def __open(self):
        """
        this method opens a character file
        ----
        @todo computation of character groups
        """
        self.opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Character Files", ".json")])
        with open(self.opendir, "r") as fp:
            self.charlist = json.load(fp)

        if type(self.charlist) == type({}):
            self.character = dict(self.charlist).copy()
            self.updWidgedCont()
        elif type(self.charlist) == [] :
            print("char list computing is not implemented yet")
            pass
        else:
            print("ERROR: wrong data format in {}".format(self.opendir))

        if "inventory" not in self.character.keys():
            self.character["inventory"] = {'weapon' :[],
                                           'armor' :[],
                                           'gear' :[],
                                           'transport':[],
                                           'herbs':[],
                                           'runes':[],
                                           'constant item':[],
                                           'daily item' :[],
                                           'gems' :[]
                                           }
        self.inv_char = self.character["inventory"].copy()


    def __save(self):
        '''
        This opens a file dialog window for saving
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Character & Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.character, fp, indent = 4)


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()


    def __armor(self):
        """
        This opens a window for armor
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "armor")


    def __weapon(self):
        """
        This opens a window for weapons
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "weapon")


    def __gear(self):
        """
        This opens a window for equipment
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "gear")


    def __transport(self):
        """
        This opens a window for animals and transports
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "transport")


    def __services(self):
        """
        This opens a window for equipment
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "services")


    def __gems(self):
        """
        This opens a window for gems and jewelery
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "gems")


    def __herbs(self):
        """
        This opens a window for portions, herbs and poisons
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "herbs")



class shopWin(blankWindow):
    """
    Window class for character's different inventory categories
    """


    def __init__(self, lang = "en", char = {}, storepath = "./data", shoptype = "armor"):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param charlist list of dictionaries holding: player, charname, EPs
        \param storepath path for storing the data into the character files.
        """

        self.lang = lang
        self.character = char
        if "inventory" in self.character.keys():
            self.inv_char = self.character["inventory"].copy()
        else:
            self.inv_char = {'weapon' :[],
                             'armor' :[],
                             'gear' :[],
                             'transport':[],
                             'herbs':[],
                             'runes':[],
                             'constant item':[],
                             'daily item' :[],
                             'gems' :[],
                             "services":[],
                           }
        self.shoptype = shoptype
        if self.character == {}:
            self.character = {  "player": "Marcus",
                                "exp": 10000,
                                'lvl' :1,
                                "prof": "Ranger",
                                "race" : "Woodmen",
                                "name": "Woody",
                                'realm' : 'Channeling',
                                "piclink" : "./data/default/pics/default.jpg"

                                }
        self.wcont = {}
        self.filterlist = ['player', 'exp', 'lvl', 'prof', 'race', 'name', 'piclink', 'realm']
        self.bgfilter = ['act_age', 'carr_weight', "sex", "height", "weight"]
        self.storepath = storepath
        self.datafile = "{}/default/inventory/{}.csv".format(storepath, shoptype)
        self.loadData()
        blankWindow.__init__(self, self.lang)
        self.window.title(submenu["inventory"][self.lang][shoptype])
        self.__addMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addMenu(self):
        '''
        This method adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__open)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['pdf'],
                                  command = self.__latexExport)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)

        self.invmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_inventory'][self.lang],
                              menu = self.invmenu)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]['armor'],
                                 command = self.__armor)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]['weapon'],
                                 command = self.__weapon)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]['gear'],
                                                 command = self.__gear)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["gems"],
                                 command = self.__gems)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["herbs"],
                                 command = self.__herbs)
        self.invmenu.add_separator()
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["spells"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["daily"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["PP_spell"],
                                  command = self.notdoneyet)
        self.invmenu.add_separator()
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["transport"],
                                 command = self.__transport)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["services"],
                                 command = self.__services)
#        self.addmenu = Menu(master=self.menu)
#        self.addmenu.add_command(label=submenu["add items"][self.lang][])


    def __addHelpMenu(self):
        """
        This method defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __buildWin(self):
        """
        This method defines the window's layout
        """
        self.updWidgedCont()
        self.picLabel = Label(master = self.window,
                              image = self.wcont['piclink']
                              )
        # row 0
        self.picLabel.grid(column = 0,
                           row = 0,
                           columnspan = 2,
                           rowspan = 8,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)
        Label(self.window,
              textvariable = self.wcont["player"],
              anchor = W,
              justify = LEFT
              ).grid(column = 2,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["exp"],
              anchor = W,
              justify = LEFT
              ).grid(column = 3,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = "Level:",
              anchor = W,
              justify = RIGHT
              ).grid(column = 4,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["lvl"],
              anchor = W,
              justify = LEFT
              ).grid(column = 5,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        # row 1
        Label(self.window,
              textvariable = self.wcont["name"],
              anchor = W,
              justify = LEFT
              ).grid(column = 2,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["sex"],
              anchor = W,
              justify = LEFT
              ).grid(column = 3,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["prof"],
              anchor = W,
              justify = LEFT
              ).grid(column = 4,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["race"],
              anchor = W,
              justify = LEFT
              ).grid(column = 5,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 2
        Label(self.window,
              text = charattribs['act_age'][self.lang] + ":",
              anchor = W,
              justify = LEFT
              ).grid(column = 2,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["act_age"],

              ).grid(column = 3,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = charattribs['height'][self.lang] + ":",
              anchor = W,
              justify = LEFT
              ).grid(column = 4,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["height"]
              ).grid(column = 5,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 3
        Label(self.window,
              text = charattribs['weight'][self.lang] + ":",
              anchor = W,
              justify = RIGHT,
              ).grid(column = 2,
                     row = 3,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["weight"]
              ).grid(column = 3,
                     row = 3,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        #row 4
        Label(self.window,
              text = charattribs['carr_weight'][self.lang] + ":",
              anchor = W,
              justify = LEFT
              ).grid(column = 2,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["carr_weight"]
              ).grid(column = 3,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = labels['MMP'][self.lang] + ":",
              anchor = W,
              justify = LEFT
              ).grid(column = 4,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["MMP"]
              ).grid(column = 5,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 5/6
        c = 2
        for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
            self.wcont[coin].set(self.character["purse"][coin])
            Label(self.window,
                  text = coin + ":",
                  anchor = N,
                  justify = CENTER
                  ).grid(column = c,
                         row = 5,
                         padx = 1,
                         pady = 1,
                         sticky = "EW"
                         )
            # this may be replaced by a text widget
            Label(self.window,
                  textvariable = self.wcont[coin],
                  anchor = N,
                  justify = RIGHT
                  ).grid(column = c,
                         row = 6,
                         padx = 1,
                         pady = 1,
                         sticky = "EW"
                         )
            c += 1
        # row 8
        self.shoplabel = Label(self.window,
                              text = labels['armor shop'][self.lang],
                              anchor = N
                #              bg = "white"
                              )
        self.shoplabel.grid(column = 0,
                             row = 8,
                             columnspan = 10,
                             pady = 3,
                             sticky = "NEWS"
                             )
        self.shoplabel.config(background = "white")
        # row 9
        self.treeframe = Frame(self.window)
        self.treeframe.grid(column = 0,
                            columnspan = 9,
                            row = 9,
                            rowspan = 4,
                            sticky = "NEWS")
        self.shoptree = Treeview(self.treeframe,
                                 columns = self.data[0],
                                 show = "headings"
                                 )
        vscroll = AutoScrollbar(orient = "vertical",
                                command = self.shoptree.yview
                                )
        hscroll = AutoScrollbar(orient = "horizontal",
                                command = self.shoptree.xview)
        self.shoptree.configure(yscrollcommand = vscroll.set,
                                xscrollcommand = hscroll.set
                                )
        vscroll.grid(column = 1,
                     row = 0,
                     sticky = "NS",
                     in_ = self.treeframe
                     )
        hscroll.grid(column = 0,
                     row = 1,
                     sticky = "EW",
                     in_ = self.treeframe
                     )
        for header in  self.data[0]:
            if header in treeformat.keys():
                self.shoptree.column(header, width = treeformat[header])
            self.shoptree.heading(header, text = header)

        self.shoptree.grid(column = 0,
                           row = 0,
                           sticky = "NEWS", in_ = self.treeframe)
        self.shoptree.bind('<Double-Button-1>', self.selectShopItem)

        Button(self.window,
               text = txtbutton["but_magic"][self.lang],
               command = self.createMagicShop).grid(column = 9,
                                             row = 9,
                                             sticky = "NEWS")
        Button(self.window,
               text = txtbutton["but_buy"][self.lang],
               command = self.buyItem).grid(column = 9,
                                             row = 10,
                                             sticky = "NEWS")
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.addShopItem).grid(column = 9,
                                             row = 11,
                                             sticky = "NEWS")
        Button(self.window,
               text = txtbutton["but_sav"][self.lang],
               command = self.__quicksave).grid(column = 9,
                                             row = 12,
                                             sticky = "NEWS")
#        self.window.columnconfigure(0, weight = 1)
#        self.window.rowconfigure(9, weight = 1)
#        self.treeframe.rowconfigure(0, weight = 1)

        self.fillShoppe()

        self.invlabel = Label(self.window,
                              text = submenu["inventory"][self.lang]["armor"] + " " + self.character["name"],
                              anchor = N
                              )
        self.invlabel.grid(column = 0,
                           row = 14,
                           columnspan = 10,
                           pady = 3,
                           sticky = "NEWS")
        self.invlabel.config(background = "white")
        self.invframe = Frame(self.window)
        self.invframe.grid(column = 0,
                           columnspan = 9,
                           row = 15,
                           rowspan = 5,
                           sticky = "EW")
        self.invtree = Treeview(self.invframe,
                                columns = char_inv_tv[self.shoptype],
                                show = "headings"
                                )
        vscroll_inv = AutoScrollbar(orient = "vertical",
                                   command = self.invtree.yview
                                   )
        hscroll_inv = AutoScrollbar(orient = "horizontal",
                                  command = self.invtree.xview
                                  )
        self.invtree.configure(yscrollcommand = vscroll_inv.set,
                               xscrollcommand = hscroll_inv.set
                               )
        vscroll_inv.grid(column = 1,
                         row = 0,
                         sticky = "NS",
                         in_ = self.invframe
                         )
        hscroll_inv.grid(column = 0,
                         row = 1,
                         sticky = "EW",
                         in_ = self.invframe
                         )
        for header in char_inv_tv[self.shoptype]:
            if header in treeformat.keys():
                self.invtree.column(header, width = treeformat[header])
            self.invtree.heading(header, text = header)

        self.invtree.grid(column = 0,
                          row = 0,
                          sticky = "NEWS",
                          in_ = self.invframe
                          )
        self.fillInventory()

        Button(self.window,
               text = txtbutton["but_sell"][self.lang],
               command = self.sellItem).grid(column = 9,
                                             row = 15,
                                             sticky = "NEWS")
        Button(self.window,
               text = txtbutton["but_away"][self.lang],
               command = self.removeItem).grid(column = 9,
                                             row = 16,
                                             sticky = "NEWS")
        Button(self.window,
               text = txtbutton["but_magic"][self.lang],
               command = self.createMagic).grid(column = 9,
                                             row = 17,
                                             sticky = "NEWS")

        Button(self.window,
               text = txtbutton["but_edit"][self.lang],
               command = self.editItem).grid(column = 9,
                                             row = 18,
                                             sticky = "NEWS")
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.addItem).grid(column = 9,
                                             row = 19,
                                             sticky = "NEWS")


    def fillInventory(self):
        """
        This fills the  inventory treeview with character's items if there are any
        """
        for i in self.invtree.get_children():
            self.invtree.delete(i)

        count = 1

        for item in self.inv_char[self.shoptype]:
            inpline = []

            for column in char_inv_tv[self.shoptype]:

                if column != "worth":
                    inpline.append(item[column])
                else:
                    purse = ""

                    for coin in coins['long']:

                        if item["worth"][coin] > 0:
                            purse += str(item["worth"][coin]) + coin[0] + "p"

                    inpline.append(purse)

            self.invtree.insert("", count, value = tuple(inpline))
            count += 1


    def createMagicShop(self):
        """
        This is for creating a magic item from standard items
        ----
        @todo has to be fully implemented
        """
        if self.shoptype == "herbs":
            messageWindow(self.lang).showinfo("Herbs/potions/poisons may not be enchanted!", "WARNING!")
        else:
            self.notdoneyet()


    def createMagic(self):
        """
        This is for creating a magic item from standard items
        ----
        @todo has to be fully implemented
        """
        if self.shoptype == "herbs":
            messageWindow(self.lang).showinfo("Herbs/potions/poisons may not be enchanted!", "WARNING!")
        else:
            self.curr_inv = self.invtree.focus()
            self.curr_invitem = self.invtree.item(self.curr_inv)["values"]
            #add changes to charracter's inventory
            self.character["inventory"] = self.inv_char.copy()
            # transform selected treeview item into character's inventory data struct
            selected = {}

            if self.shoptype == "weapon":
                selected = weapon.copy()
            elif self.shoptype == "armor" :
                selected = armor.copy()
            elif self.shoptype == "gear":
                selected = gear.copy()
            elif self.shoptype == "gems":
                selected = gems.copy()
            elif self.shoptype == "runes":
                selected = runes.copy()
            elif self.shoptype == "herbs" :
                selected = herbs.copy()
            elif self.shoptype == "services":
                selected = services.copy()
            elif self.shoptype == "constant item":
                selected = constant_item.copy()
            elif self.shoptype == "daily item":
                selected = daily_item.copy()
            elif self.shoptype == "transport":
                selected = transport.copy()
            else:
                print("ERROR: wrong shoptype")

            for item in self.character["inventory"][self.shoptype]:
                count = 1

                for i in range(0, len(char_inv_tv[self.shoptype])):

                    if char_inv_tv[self.shoptype][i] != "worth" and str(item[char_inv_tv[self.shoptype][i]]) == str(self.curr_invitem[i]):
                       count += 1
                if count >= len(char_inv_tv[self.shoptype]) - 1:

                    for key in char_inv_tv[self.shoptype]:
                        selected[key] = item[key]

            self.window.destroy()
            self.enchantWin = enchantItem(self.lang, self.character, self.storepath, selected, self.shoptype)


    def selectShopItem(self, event):
        """
        Gets dataset from shop treeview
        """
        self.curr_shop = self.shoptree.focus()


    def buyItem(self):
        """
        This is for buying a piece of equipment
        @todo a message window has to be implemented if not enoug money
        """
        self.curr_shop = self.shoptree.focus()
        self.curr_item = self.shoptree.item(self.curr_shop)['values']
        worth = self.data[0].index("cost")
        price = int(self.curr_item[worth][:-2])
        coin = self.curr_item[worth][-2:]
        mymoney = self.character["purse"]["IP"]
        cu = coins["short"].index(coin)
        price *= 10 ** (len(coins["short"]) - cu - 1)
        cu = coins["short"].index("ip")
        ocu = cu

        # subtract the money
        while mymoney < price and cu >= 0:
            cu -= 1

            while self.character["purse"][coins["short"][cu].upper()] > 0 and mymoney < price:
                self.character["purse"][coins["short"][cu + 1].upper()] = 0
                self.character["purse"][coins["short"][cu].upper()] -= 1
                mymoney += 10 ** (ocu - cu)

        if mymoney < price:
            messageWindow(self.lang).showinfo("not enough money - ohne Moos nix los!", "WARNING")
            print("not enough money!!")

        else:
            result = mymoney - price

            for i in range(cu + 1, ocu + 1):
                self.character["purse"][coins["short"][i].upper()] = (result) // 10 ** (ocu - i)
                result -= (result) // 10 ** (ocu - i) * 10 ** (ocu - i)

            for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
                self.wcont[coin].set(self.character["purse"][coin])

            # add item
            self.addShopItem()


    def sellItem(self):
        """
        This is for selling a piece of equipment
        """
        self.curr_inv = self.invtree.focus()
        self.curr_invitem = self.invtree.item(self.curr_inv)["values"]
        worth = char_inv_tv[self.shoptype].index("worth")

        for item in self.inv_char[self.shoptype]:
            count = 1

            for i in range(0, len(char_inv_tv[self.shoptype])):

                if char_inv_tv[self.shoptype][i] != "worth" and str(item[char_inv_tv[self.shoptype][i]]) == self.curr_invitem[i]:
                    count += 1

            if count >= len(char_inv_tv[self.shoptype]) - 1:
                price = int(self.curr_invitem[worth][:-2])
                coin = self.curr_invitem[worth][-2:]

                if "PP" not in self.character["purse"].keys():
                    self.character["purse"]["PP"] = 0

                for cu in self.character["purse"].keys():

                    if cu.lower() == coin:
                        self.character["purse"][cu] += price

                self.inv_char[self.shoptype].remove(item)
                self.character["inventory"] = self.inv_char
                self.fillInventory()

                for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
                    self.wcont[coin].set(self.character["purse"][coin])
                break


    def removeItem(self):
        """
        This is for removing a piece of equipment (throw away)
        """
        self.curr_inv = self.invtree.focus()
        self.curr_invitem = self.invtree.item(self.curr_inv)["values"]

        for item in self.inv_char[self.shoptype]:
            count = 1
            for i in range(0, len(char_inv_tv[self.shoptype])):
                if char_inv_tv[self.shoptype][i] != "worth" and str(item[char_inv_tv[self.shoptype][i]]) == self.curr_invitem[i]:
                    count += 1

            if count >= len(char_inv_tv[self.shoptype]) - 1:
                self.inv_char[self.shoptype].remove(item)
                self.character["inventory"] = self.inv_char
                self.fillInventory()
                break


    def addShopItem(self):
        """
        This is for adding a piece of equipment to shop
        """
        self.curr_shop = self.shoptree.focus()
        self.curr_item = self.shoptree.item(self.curr_shop)['values']
        newitem = {}

        if self.shoptype == "weapon":
            newitem = weapon.copy()
        elif self.shoptype == "armor" :
            newitem = armor.copy()
        elif self.shoptype == "gear":
            newitem = gear.copy()
        elif self.shoptype == "gems":
            newitem = gems.copy()
        elif self.shoptype == "runes":
            newitem = runes.copy()
        elif self.shoptype == "herbs" :
            newitem = herbs.copy()
        elif self.shoptype == "services":
            newitem = services.copy()
        elif self.shoptype == "constant item":
            newitem = constant_item.copy()
        elif self.shoptype == "daily item":
            newitem = daily_item.copy()
        elif self.shoptype == "transport":
            newitem = transport.copy()
        else:
            print("ERROR: wrong shoptype")

        newitem["worth"] = money.copy()

        for  i in range(0, len(self.data[0])):

            if self.data[0][i] == "item":
                newitem["name"] = self.curr_item[i]

            elif self.data[0][i] == "comment":
                newitem["description"] = self.curr_item[i]

            elif self.data[0][i] == "weight" :
                if "-" in self.curr_item[i]:
                    a, b = self.curr_item[i].strip(" lbs.").split("-")
                    newitem["weight"] = round(random.uniform(float(a), float(b)), 2)
                else:
                    newitem["weight"] = float(self.curr_item[i].strip(" lbs."))

            elif self.data[0][i] == "effect":
                newitem["medical use"] = self.curr_item[i]

            elif self.data[0][i] == "cost":

                price = self.curr_item[i][:-2]
                if self.curr_item[i][-2:] == "mp":
                    newitem["worth"]["mithril"] = int(price)
                elif self.curr_item[i][-2:] == "pp":
                    newitem["worth"]["platinium"] = int(price)
                elif self.curr_item[i][-2:] == "gp":
                    newitem["worth"]["gold"] = int(price)
                elif self.curr_item[i][-2:] == "sp":
                    newitem["worth"]["silver"] = int(price)
                elif self.curr_item[i][-2:] == "bp":
                    newitem["worth"]["bronze"] = int(price)
                elif self.curr_item[i][-2:] == "cp":
                    newitem["worth"]["copper"] = int(price)
                elif self.curr_item[i][-2:] == "tp":
                    newitem["worth"]["tin"] = int(price)
                elif self.curr_item[i][-2:] == "ip":
                    newitem["worth"]["iron"] = int(price)

            elif self.data[0][i] != "ID":
                newitem[self.data[0][i]] = self.curr_item[i]

        self.inv_char[self.shoptype].append(newitem.copy())
        del(newitem)
        self.fillInventory()


    def addItem(self):
        """
        This is for adding a piece of equipment to shop
        ----
        @todo has to be fully implemented
        """

        self.notdoneyet()


    def editShopItem(self):
        """
        This is for editing a single shop item
        ----
        @todo has to be fully implemented
        """
        self.notdoneyet()


    def editItem(self):
        """
        This is for editing a single shop item
        ----
        @todo has to be fully implemented
        """
        self.notdoneyet()


    def saveShop(self):
        """
        This is for saving shop inventory
        ----
        @todo has to be fully implemented
        """
        self.notdoneyet()


    def fillShoppe(self):
        """
        This fills the treview widget of the shop items
        """
        for i in range(1, len(self.data)):
            self.shoptree.insert("", i, values = tuple(self.data[i]))


    def loadData(self):
        """
        Loads and prepares shop data
        """
        with open(self.datafile) as fp:
            cont = fp.read()

        self.data = cont.split("\n")
        for i in range(0, len(self.data)):
            self.data[i] = self.data[i].split(",")


    def updWidgedCont(self):
        '''
        This method updates widget content like texts or images
        '''

        for elem in self.filterlist:

            if elem == "piclink":

                if elem in self.wcont.keys():
                    self.wcont[elem] = ImageTk.PhotoImage(Image.open(self.character[elem]).resize((210, 210), Image.ANTIALIAS))
                    self.picLabel.config(image = self.wcont[elem])

                else:
                    self.wcont[elem] = ImageTk.PhotoImage(Image.open(self.character[elem]).resize((210, 210), Image.ANTIALIAS))

            elif type(self.character[elem]) == type(""):

                if elem not in self.wcont.keys():
                    self.wcont[elem] = StringVar()

                self.wcont[elem].set(self.character[elem])

            elif type(self.character[elem]) == type(0):
                if elem not in self.wcont.keys():
                    self.wcont[elem] = IntVar()

                self.wcont[elem].set(self.character[elem])

        for elem in self.bgfilter:

            if "background" in self.character.keys():

                if type(self.character["background"][elem]) == type(""):

                    if elem not in self.wcont.keys():
                        self.wcont[elem] = StringVar()

                    self.wcont[elem].set(self.character["background"][elem])

                elif type(self.character["background"][elem]) == type(0):

                    if elem not in self.wcont.keys():
                        self.wcont[elem] = IntVar()

                    self.wcont[elem].set(self.character["background"][elem])
            else:
                self.wcont[elem] = StringVar()
                self.wcont[elem].set("--")

        if "MMṔ" not in self.wcont.keys():
            self.wcont["MMP"] = IntVar()
            self.wcont["MMP"].set(0)

        elif "MMP" not in self.character.keys():
            self.character["MMP"] = calcMMP(self.character)
            self.wcont["MMP"].set(self.character["MMP"])

        for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
            if "purse" not in self.character.keys():
                self.character["purse"] = {}

            if coin not in self.character['purse'].keys():
                self.character["purse"][coin] = 0

            if coin not in self.wcont.keys():
                self.wcont[coin] = IntVar()

            self.wcont[coin].set(self.character["purse"][coin])


    def calcMMP(self, char = {}):
        """
        This method calculates the Movement Maneuver Penalty (MMP)
        @param char full character data as dictionary
        @retval mmp Movement Maneuver Penalty as integer
        ----
        @todo has to be fully implemented
        """
        mmp = 0
        return mmp


    def __latexExport(self):
        """
        This exports data into  LaTeX template for PDF generation
        ----
        @todo has to be fully implemented
        """
        self.notdoneyet("LaTeX export")


    def __open(self):

        """
        this method opens a character file
        ----
        @todo computation of character groups
        """
        self.opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Character Files", ".json")])
        with open(self.opendir, "r") as fp:
            self.charlist = json.load(fp)

        if type(self.charlist) == type({}):
            self.character = dict(self.charlist).copy()
            self.updWidgedCont()
            self.invlabel.config(text = submenu["inventory"][self.lang]["armor"] + " " + self.character["name"])

        elif type(self.charlist) == [] :
            print("char list computing is not implemented yet")

        else:
            print("ERROR: wrong data format in {}".format(self.opendir))

        if "inventory" not in self.character.keys():
            self.character["inventory"] = {'weapon' :[],
                                           'armor' :[],
                                           'gear' :[],
                                           'transport':[],
                                           'herbs':[],
                                           'runes':[],
                                           'constant item':[],
                                           'daily item' :[],
                                           'gems' :[]
                                           }
        if "PP" not in self.character["purse"].keys():
            self.character["purse"] = 0
        self.inv_char = self.character['inventory'].copy()
        self.fillInventory()


    def __save(self):
        '''
        This opens a file dialog window for saving
        '''
        self.character["inventory"] = self.inv_char.copy()
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Character & Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.character, fp, indent = 4)


    def __quicksave(self):
        '''
        This does a character quick save without opening a window
        '''
        self.character["inventory"] = self.inv_char.copy()
        try:
            with open(self.opendir, "w") as fp:
                json.dump(self.character, fp, indent = 4)

            print("{} saved".format(self.opendir))
        except:
            self.__save()


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()


    def __armor(self):
        """
        This opens a window for armor
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "armor")


    def __weapon(self):
        """
        This opens a window for weapons
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "weapon")


    def __gear(self):
        """
        This opens a window for equipment
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "gear")


    def __transport(self):
        """
        This opens a window for animals and transports
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "transport")


    def __services(self):
        """
        This opens a window for equipment
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "services")


    def __gems(self):
        """
        This opens a window for gems and jewelery
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "gems")


    def __herbs(self):
        """
        This opens a window for portions, herbs and poisons
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "herbs")



class enchantItem(blankWindow):
    """
    This is a GUI for EP calculation for your character party.
    """


    def __init__(self, lang = "en", char = {}, storepath = "./data", item = {}, shoptype = ""):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param charlist list of dictionaries holding: player, charname, EPs
        \param storepath path for storing the data into the character files.
        """

        self.lang = lang
        self.character = char.copy()

        if self.character == {}:
            self.character = {  "player": "Marcus",
                                "exp": 10000,
                                'lvl' :1,
                                "prof": "Ranger",
                                "race" : "Woodmen",
                                "name": "Woody",
                                'realm' : 'Channeling',
                                "piclink" : "./data/default/pics/default.jpg"

                                }
        self.item = item.copy()
        self.price = self.item["worth"].copy()
        self.enchantment = ("chose enchantment", "charged magic item", "daily item", "magic bonus item", "permanent magic item")
        self.shoptype = shoptype
        self.wcont = {}
        self.weight_mod = 0
        self.bonus_mod = 0
        self.filterlist = ['player', 'exp', 'lvl', 'prof', 'race', 'name', 'piclink', 'realm']
        self.bgfilter = ['act_age', 'carr_weight', "sex", "height", "weight"]
        self.storepath = storepath
        blankWindow.__init__(self, self.lang)
        self.__findItemInv()
        self.window.title("Rucksack")
        self.__addMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __findItemInv(self):
        """
        This copies the complete data to the selected item from characters inventory
        """
        self.elem = 0
        for invitem in self.character["inventory"][self.shoptype]:
            count = 0

            for h in char_inv_tv[self.shoptype]:

                if self.item[h] == invitem[h]:
                    count += 1

            if count == len(char_inv_tv[self.shoptype]):
                self.item = invitem.copy()
                self.elem = self.character["inventory"][self.shoptype].index(invitem)
                break


    def __addMenu(self):
        '''
        This method adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__open)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu["file"][self.lang]['sv_item'])
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)


    def __addHelpMenu(self):
        """
        This method defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __buildWin(self):
        """
        This method defines the window's layout
        """
        self.updWidgedCont()
        self.picLabel = Label(master = self.window,
                              image = self.wcont['piclink']
                              )
        # row 0
        self.picLabel.grid(column = 0,
                           row = 0,
                           columnspan = 2,
                           rowspan = 8,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)
        Label(self.window,
              textvariable = self.wcont["player"],
              justify = LEFT
              ).grid(column = 2,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["exp"],
              justify = LEFT
              ).grid(column = 3,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = "Level:",
              justify = RIGHT
              ).grid(column = 4,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["lvl"],
              justify = LEFT
              ).grid(column = 5,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        # row 1
        Label(self.window,
              textvariable = self.wcont["name"],
              justify = LEFT
              ).grid(column = 2,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["sex"],
              justify = LEFT
              ).grid(column = 3,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["prof"],
              justify = LEFT
              ).grid(column = 4,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["race"],
              justify = LEFT
              ).grid(column = 5,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 2
        Label(self.window,
              text = charattribs['act_age'][self.lang] + ":"
              ).grid(column = 2,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["act_age"]
              ).grid(column = 3,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = charattribs['height'][self.lang] + ":"
              ).grid(column = 4,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["height"]
              ).grid(column = 5,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 3
        Label(self.window,
              text = charattribs['weight'][self.lang] + ":",
              justify = RIGHT,
              ).grid(column = 2,
                     row = 3,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["weight"]
              ).grid(column = 3,
                     row = 3,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        #row 4
        Label(self.window,
              text = charattribs['carr_weight'][self.lang] + ":"
              ).grid(column = 2,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["carr_weight"]
              ).grid(column = 3,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = labels['MMP'][self.lang] + ":"
              ).grid(column = 4,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["MMP"]
              ).grid(column = 5,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        # row 5/6
        c = 2
        for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
            Label(self.window,
                  text = coin + ":",
                  ).grid(column = c,
                         row = 5,
                         padx = 1,
                         pady = 1,
                         sticky = "EW"
                         )
            Label(self.window,
                  textvariable = self.wcont[coin],
                  ).grid(column = c,
                         row = 6,
                         padx = 1,
                         pady = 1,
                         sticky = "EW"
                         )
            c += 1

        # row 8
        self.shoplabel = Label(self.window,
                              text = labels['magic shop'][self.lang],
                              anchor = N,
                              background = "grey"
                              )
        self.shoplabel.grid(column = 0,
                             row = 8,
                             columnspan = 10,
                             pady = 3,
                             sticky = "NEWS"
                             )
        # row 9
        Label(self.window,
              text = labels["item"][self.lang] + ":",
              ).grid(column = 0,
                     row = 9,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = self.item["name"]
              ).grid(column = 1,
                     row = 9,
                     padx = 3,
                     pady = 1,
                     sticky = "EW"
                     )
        self.chosen = StringVar(self.window)
        self.chosen.set(self.enchantment[0])

        self.opt = OptionMenu(self.window,
                           self.chosen,
                           *tuple(self.enchantment),
                           command = self.getChoice
                           )
        self.opt.grid(column = 2,
                      row = 9,
                      padx = 1,
                      pady = 1,
                      sticky = "EW"
                      )

        Label(self.window,
              text = labels["cost"][self.lang] + ":"
              ).grid(column = 3,
                     row = 9,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        self.cost = StringVar()
        self.cost.set(self.getCosts())
        Label(self.window,
              textvariable = self.cost
              ).grid(column = 4,
                     row = 9,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        # Buttons ------------------------------
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.addMagicItem
               ).grid(column = 5,
                     columnspan = 2,
                     row = 9,
                     padx = 2, pady = 1,
                     sticky = "EW"
                     )

        Button(self.window,
               text = txtbutton["but_buy"][self.lang],
               command = self.payEnchantement
               ).grid(column = 7,
                      columnspan = 3,
                      row = 9,
                      padx = 1,
                      pady = 1,
                      sticky = "EW"
                      )
        # here comes the selected item
        #row 10
        self.frame = {}

        for i in range(1, len(self.enchantment)):
            self.frame[self.enchantment[i]] = Frame(self.window)

        realm_list = []

        for r in realms[self.lang]:

            if type(r) == type(""):
                realm_list.append(r)

            elif type(r) == type([]):
                dummy = str(r)
                dummy = dummy.strip("[']")
                dummy = dummy.replace("', '", "/")
                realm_list.append(dummy)

        # Bonus/weight reduced items ---------------------
        Label(self.frame["magic bonus item"],
              text = labels["bonus item"][self.lang],
              background = "grey",
              anchor = N
             ).grid(column = 0,
                    columnspan = 9,
                    row = 0,
                    sticky = "NEWS")
        Label(self.frame["magic bonus item"],
              text = "Bonus:"
              ).grid(column = 0,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "EW"
                     )

        self.bonus = IntVar(self.frame["magic bonus item"])
        self.bonus.set(0)
        OptionMenu(self.frame["magic bonus item"],
                   self.bonus,
                   *(0, 0, 5, 10, 15, 20, 25),
                   command = self.calcBonusItem
                   ).grid(column = 1,
                          row = 1,
                          pady = 5,
                          padx = 5,
                          sticky = "EW")

        Label(self.frame["magic bonus item"],
              text = labels["bonus c/s"][self.lang] + ":",
              ).grid(column = 2,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "EW"
                     )

        self.catskill = StringVar()

        if "skill" in self.item.keys():
            self.catskill.set(self.item["skill"])

        else:
            self.catskill.set("<category>/<skill>")

        Entry(self.frame["magic bonus item"],
              textvariable = self.catskill,
              width = 42,
              ).grid(column = 3,
                     row = 1,
                     padx = 5,
                     pady = 5,
                     sticky = "EW")

        Label(self.frame["magic bonus item"],
              text = labels["weight"][self.lang] + u"(%):"
              ).grid(column = 4,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "EW")

        self.weight = IntVar(self.frame["magic bonus item"])
        self.weight.set(100)
        OptionMenu(self.frame["magic bonus item"],
                   self.weight,
                   *(100, 100, random.randint(80, 99), random.randint(60, 79), random.randint(40, 59)),
                   command = self.calcBonusItem
                   ).grid(column = 5,
                          row = 1,
                          pady = 5,
                          padx = 5,
                          sticky = "NEWS")

        Label(self.frame["magic bonus item"],
              text = labels["descr"][self.lang] + ":",
              ).grid(column = 6,
                     row = 1,
                     padx = 5,
                     pady = 5,
                     sticky = "NEWS")

        self.description = StringVar()
        self.description.set(self.item["description"])
        Entry(self.frame["magic bonus item"],
              justify = "left",
              textvariable = self.description,
              width = 48
              ).grid(column = 7,
                     row = 1,
                     padx = 5,
                     pady = 5,
                     sticky = "NEWS"
                     )

        # charged items --------------------------------
        Label(self.frame["charged magic item"],
             text = labels["charged item"][self.lang],
             background = "gray52",
             anchor = N
             ).grid(column = 0,
                    columnspan = 9,
                    row = 0,
                    sticky = "NEWS")

        Label(self.frame["charged magic item"],
              text = labels["type"][self.lang] + ":"
              ).grid(column = 0,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")

        self.typus = StringVar()
        self.typus.set(charged_item[self.lang][0])
        OptionMenu(self.frame["charged magic item"],
                   self.typus,
                   *([charged_item[self.lang][0]] + charged_item[self.lang]),
                   command = self.updCharged
                   ).grid(column = 1,
                          row = 1,
                          pady = 5,
                          padx = 5,
                          sticky = "NEWS")

        Label(self.frame["charged magic item"],
              text = labels["loads"][self.lang] + ":"
              ).grid(column = 2,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")

        self.loads = IntVar()
        self.loads.set(0)
        self.loadsE = Entry(self.frame["charged magic item"],
                          justify = "left",
                          textvariable = self.loads,
                          width = 4
                          )
        self.loadsE.grid(column = 3,
                         row = 1,
                         padx = 5,
                         pady = 5,
                         sticky = "NEWS"
                         )

        self.loadsE.bind('<FocusOut>', self.updCharged)
        Label(self.frame["charged magic item"],
              text = "max. " + labels["loads"][self.lang] + ":"
              ).grid(column = 4,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")

        self.maxloads = IntVar()
        self.maxloads.set(1)
        Label(self.frame["charged magic item"],
              textvariable = self.maxloads

              ).grid(column = 5,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")
        Label(self.frame["charged magic item"],
              text = "To do:",
              ).grid(column = 6,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")

        self.action = StringVar()
        self.action.set(charge_action[self.lang][0])

        OptionMenu(self.frame["charged magic item"],
                   self.action,
                   *([charge_action[self.lang][0]] + charge_action[self.lang]),
                   command = self.updCharged
                   ).grid(column = 7,
                          columnspan = 2,
                          row = 1,
                          pady = 5,
                          padx = 5,
                          sticky = "NEWS")

        Label(self.frame["charged magic item"],
              text = labels["realm"][self.lang].title() + ":",
              ).grid(column = 0,
                     row = 2,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")

        self.realm = StringVar()
        self.realm.set(realm_list[0])
        OptionMenu(self.frame["charged magic item"],
                   self.realm,
                   *realm_list,
                   command = self.updCharged
                   ).grid(column = 1,
                          row = 2,
                          pady = 5,
                          padx = 5,
                          sticky = "NEWS")

        Label(self.frame["charged magic item"],
              text = labels["spell list"][self.lang] + ":"
              ).grid(column = 2,
                     row = 2,
                     pady = 5,
                     padx = 1,
                     sticky = "NEWS")

        self.spell_list = StringVar()
        self.spell_list.set("")
        Entry(self.frame["charged magic item"],
              justify = "left",
              textvariable = self.spell_list,
              width = 48
              ).grid(column = 3,
                     row = 2,
                     padx = 5,
                     pady = 5,
                     sticky = "NEWS"
                     )

        Label(self.frame["charged magic item"],
              text = labels["spell"][self.lang] + ":"
              ).grid(column = 4,
                     row = 2,
                     pady = 5,
                     padx = 1,
                     sticky = "NEWS")

        self.spell = StringVar()
        self.spell.set("")
        self.spell_E = Entry(self.frame["charged magic item"],
                            justify = "left",
                            textvariable = self.spell,
                            width = 48
                            )
        self.spell_E.grid(column = 5,
                         row = 2,
                         padx = 5,
                         pady = 5,
                         sticky = "NEWS"
                         )
        self.spell_E.bind('<FocusOut>', self.updCharged)

        Label(self.frame["charged magic item"],
              text = labels["spell"][self.lang] + " " + labels["lvl"][self.lang] + ":"
              ).grid(column = 6,
                     row = 2,
                     pady = 5,
                     padx = 1,
                     sticky = "NEWS")

        self.spell_lvl = IntVar()
        self.spell_lvl.set(1)
        self.spell_lvlE = Entry(self.frame["charged magic item"],
                                textvariable = self.spell_lvl,
                                width = 4
                                )
        self.spell_lvlE.grid(column = 7,
                             row = 2,
                             padx = 5,
                             pady = 5,
                             sticky = "NEWS"
                             )
        self.spell_lvlE.bind('<FocusOut>', self.updCharged)

        self.maxlvl = StringVar()
        self.maxlvl.set("/10")
        Label(self.frame["charged magic item"],
              textvariable = self.maxlvl
              ).grid(column = 8,
                     row = 2,
                     pady = 5,
                     padx = 0,
                     sticky = "NEWS")

        Label(self.frame["charged magic item"],
              text = labels["descr"][self.lang].title() + ":"
              ).grid(column = 0,
                     row = 3,
                     pady = 5,
                     padx = 0,
                     sticky = "NEWS")

        self.description = StringVar()
        self.description.set(self.item["description"])
        Entry(self.frame["charged magic item"],
              justify = "left",
              textvariable = self.description,
              width = 40
              ).grid(column = 1,
                     row = 3,
                     columnspan = 8,
                     padx = 5,
                     pady = 5,
                     sticky = "NEWS"
                     )

        # daily items -----------------------------------
        Label(self.frame["daily item"],
              text = labels["daily item"][self.lang],
              background = "gray89",
              anchor = N
             ).grid(column = 0,
                    columnspan = 9,
                    row = 0,
                    sticky = "NEWS")

        Label(self.frame["daily item"],
              text = labels["realm"][self.lang] + ":"
              ).grid(column = 0,
                    row = 1,
                    sticky = "NEWS")

        self.realm = StringVar()
        self.realm.set(realm_list[0])
        OptionMenu(self.frame["daily item"],
                   self.realm,
                   *realm_list,
                   command = self.updDaily
                   ).grid(column = 1,
                          row = 1,
                          pady = 5,
                          padx = 5,
                          sticky = "NEWS")

        Label(self.frame["daily item"],
              text = labels["spell list"][self.lang] + ":"
              ).grid(column = 2,
                     row = 1,
                     pady = 5,
                     padx = 1,
                     sticky = "NEWS")

#        self.spell_list = StringVar()
#        self.spell_list.set("")
        Entry(self.frame["daily item"],
              justify = "left",
              textvariable = self.spell_list,
              width = 48
              ).grid(column = 3,
                     row = 1,
                     padx = 5,
                     pady = 5,
                     sticky = "NEWS"
                     )

        Label(self.frame["daily item"],
              text = labels["spell"][self.lang] + ":"
              ).grid(column = 4,
                     row = 1,
                     pady = 5,
                     padx = 1,
                     sticky = "NEWS")

#        self.spell = StringVar()
#        self.spell.set("")
        self.spellE = Entry(self.frame["daily item"],
                            justify = "left",
                            textvariable = self.spell,
                            width = 48
                            )
        self.spellE.grid(column = 5,
                         row = 1,
                         padx = 5,
                         pady = 5,
                         sticky = "NEWS"
                         )
        self.spellE.bind('<FocusOut>', self.updDaily)

        Label(self.frame["daily item"],
              text = labels["spell"][self.lang] + " " + labels["lvl"][self.lang] + ":"
              ).grid(column = 6,
                     row = 1,
                     pady = 5,
                     padx = 1,
                     sticky = "NEWS")

#        self.spell_lvl = IntVar()
        self.spell_lvl.set(1)
        Entry(self.frame["daily item"],
                                justify = "left",
                                textvariable = self.spell_lvl,
                                width = 4
                                ).grid(column = 7,
                             row = 1,
                             padx = 5,
                             pady = 5,
                             sticky = "NEWS"
                             )

        Label(self.frame["daily item"],
              text = labels["daily"][self.lang] + ":",
              ).grid(column = 0,
                     row = 2,
                     pady = 5,
                     padx = 1,
                     sticky = "NEWS")

        self.daily = IntVar()
        self.daily.set(0)
        self.dailyE = Entry(self.frame["daily item"],
              justify = "left",
              textvariable = self.daily,
              width = 4
              )
        self.dailyE.bind('<FocusOut>', self.updDaily)
        self.dailyE.grid(column = 1,
                        row = 2,
                        padx = 5,
                        pady = 5,
                        sticky = "NEWS"
                        )

        Label(self.frame["daily item"],
              text = labels["descr"][self.lang] + ":"
              ).grid(column = 2,
                     row = 2,
                     pady = 5,
                     padx = 1,
                     sticky = "NEWS")

        self.description.set(self.item["description"])
        Entry(self.frame["daily item"],
              justify = "left",
              textvariable = self.description,
              width = 40
              ).grid(column = 3,
                     row = 2,
                     columnspan = 9,
                     padx = 5,
                     pady = 5,
                     sticky = "NEWS"
                     )

        # permanent items --------------------------------
        Label(self.frame["permanent magic item"],
              text = labels["perm item"][self.lang],
              anchor = N,
              background = "white"
             ).grid(column = 0,
                    columnspan = 15,
                    row = 0,
                    sticky = "NEWS")

        Label(self.frame["permanent magic item"],
              text = labels["spell adder"][self.lang] + ":"
              ).grid(column = 0,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")
        sa_list = ["+0"] + list(perm_item["spell adder"].keys())
        sa_list.sort()
        self.spell_adder = StringVar()
        self.spell_adder.set(sa_list[0])
        OptionMenu(self.frame["permanent magic item"],
                   self.spell_adder,
                   *sa_list,
                   command = self.updPerm
                   ).grid(column = 1,
                          row = 1,
                          pady = 5,
                          padx = 5,
                          sticky = "NEWS")

        Label(self.frame["permanent magic item"],
              text = labels["pp mult"][self.lang] + ":"
              ).grid(column = 2,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")

        ppm_list = ["x1"] + list(perm_item["pp mult"].keys())
        ppm_list.sort()
        self.pp_mult = StringVar()
        self.pp_mult.set(ppm_list[0])
        OptionMenu(self.frame["permanent magic item"],
                   self.pp_mult,
                   *ppm_list,
                   command = self.updPerm
                   ).grid(column = 3,
                          row = 1,
                          pady = 5,
                          padx = 5,
                          sticky = "NEWS")

        Label(self.frame["permanent magic item"],
              text = labels["descr"][self.lang] + ":",
              ).grid(column = 4,
                     row = 1,
                     pady = 5,
                     padx = 5,
                     sticky = "NEWS")

        self.description.set(self.item["description"])
        Entry(self.frame["permanent magic item"],
              justify = "left",
              textvariable = self.description,
              width = 40
              ).grid(column = 5,
                     row = 1,
                     columnspan = 9,
                     padx = 5,
                     pady = 5,
                     sticky = "NEWS"
                     )


    def updCharged(self, selection):
        """
        Updates charged items display
        """
        itemtype = self.typus.get()
        itemtype = itemtype.lower().split(" ")[0]
        self.maxloads.set(info_charged[itemtype][0])
        print(self.spell.get())
        desc = self.item["description"] + ";({}, Lvl {}, lds {}/{})".format(self.spell_list.get() + "/" + self.spell.get(), self.spell_lvl.get(), self.loads.get(), self.maxloads.get())
        print(desc)
        self.description.set(desc)

        if self.action.get() == charge_action[self.lang][0]:
            mult = 1
        else:
            mult = 0.5

        self.loads.set(self.maxloads.get())

        if self.loads.get() > info_charged[itemtype][0]:
            self.loads.set(info_charged(itemtype)[0])

        if self.spell_lvl.get() >= len(info_charged[itemtype]):
            self.spell_lvl.set(len(info_charged[itemtype]) - 1)

        self.maxlvl.set("/" + str(len(info_charged[itemtype]) - 1))
        self.price = self.item["worth"].copy()
        self.price["gold"] += info_charged[itemtype][0] + round(mult * info_charged[itemtype][self.spell_lvl.get()])
        self.cost.set(self.getCosts())


    def updPerm(self, event):
        """
        Updates display for permanent items
        """
        sa_selec = self.spell_adder.get()
        ppm_selec = self.pp_mult.get()
        desc = ""

        if sa_selec != "+0":
            desc += "; {} {}".format(labels["spell adder"][self.lang], sa_selec)

        if ppm_selec != "x1":
            desc += "; {} {}".format(labels["pp mult"][self.lang], ppm_selec)

        self.description.set(self.item["description"] + desc)
        self.price = self.item["worth"].copy()
        self.price["gold"] += perm_item["spell adder"][sa_selec] + perm_item["pp mult"][ppm_selec]
        self.cost.set(self.getCosts())


    def updDaily(self, event):
        """
        Updates display for daily items
        """
        self.spellrealm = self.realm.get()
        self.splvl = self.spell_lvl.get()
        self.price = self.item["worth"].copy()
        descadd = "; Enhancement({}-daily x{}): {}, lvl {}".format(self.spellrealm, self.daily.get(), self.spell.get(), self.splvl)

        if "; Enhancement(" in self.item["description"]:
            self.item["description"] = self.item["description"][:self.item["description"].find("; Enhancement(")]

#        self.item["description"] += descadd
        self.description.set(self.item["description"] + descadd)
        self.calcDaily()
        self.cost.set(self.getCosts())


    def calcDaily(self):
        """
        This method calculates the price for a daily item
        """
        spell_prices = [15, 50, 100, 150, 200, 300, 400, 500, 600, 750]
        daily_use = self.daily.get()
        sum = 20

        if ("Channeling" or "Leitmagie") in self.spellrealm:
            chan = 2
        else:
            chan = 1

        daily_mult = 1

        for i in range(1, daily_use + 1):
            sum += chan * daily_mult * spell_prices[self.splvl - 1]
            daily_mult = 0.5

        self.price["gold"] += round(sum)


    def getChoice(self, selection):
        '''
        This switches the specific frames for the different types of magic items
        '''
        #"charged magic item", "daily item", "magic bonus item", "permanent magic item"
        try:
            for elem in self.enchantment[1:]:
                self.frame[elem].grid_forget()
        except:

            pass

        finally:
            self.frame[selection].grid(column = 0,
                                       columnspan = 9,
                                       row = 10,
                                       rowspan = 6,
                                       padx = 3,
                                       pady = 3,
                                       sticky = "NEWS"
                                       )
        self.item = self.character["inventory"][self.shoptype][self.elem].copy()
        self.price = self.item["worth"].copy()
        self.description.set(self.item["description"])
        self.cost.set(self.getCosts())


    def calcBonusItem(self, selection):
        """
        This calculates the cost for weight reduced and/or bonus items
        """
        bonus_mult = {0:1,
                      5:10,
                      10:50,
                      15:250,
                      20:1000,
                      25:5000
                      }
        weight_mult = 1

        bonus_choice = self.bonus.get()
        weight_choice = self.weight.get()

        if 79 < weight_choice < 100:
            weight_mult = 10

        elif 59 < weight_choice < 80:
            weight_mult = 50

        elif 39 < weight_choice < 60:
            weight_mult = 100

        elif weight_choice == 100:
            weight_mult = 1

        mb = "; magic bonus (+{})".format(bonus_choice)
        wb = "; magic weight reduced ({}%)".format(weight_choice)
        desc = self.item["description"]

        if bonus_mult[bonus_choice] > 1:
            desc += mb

        if weight_mult > 1:
            desc += wb

        self.description.set(desc)

        for key in self.item["worth"]:
            self.price[key] = self.item["worth"][key] * weight_mult * bonus_mult[bonus_choice]

        self.cost.set(self.getCosts())


    def payEnchantement(self):
        """
        This does the payment of the enchantment
        """
        choice = self.chosen.get()
        self.item["magic"] = True
        if self.price != self.character["inventory"][self.shoptype][self.elem]["worth"]:
            self.item["worth"] = self.price.copy()
            pos = -1

            # calculate worth in smallest unit.
            for i in range(len(coins["long"]) - 1, -1, -1):

                if self.item["worth"][coins["long"][i]] > 0:
                    pos = i
                    break

            for j in range(pos - 1, -1, -1):
                self.item["worth"][coins["long"][pos]] += self.item["worth"][coins["long"][j]] * 10 ** (pos - j)
                self.item["worth"][coins["long"][j]] = 0

            if choice == "magic bonus item":
                self.item['bonus'] = int(self.item["bonus"]) + int(self.bonus.get())
                self.item["skill"] = self.catskill.get()
                self.item['description'] = self.description.get()
                self.item["weight"] = round(self.item["weight"] * float(self.weight.get()) / 100.0, 2)
                self.item["magic"] = True

            elif choice == "charged magic item":
                self.item["type"] = self.typus.get()
                self.item["spell"] = "{}\{}".format(self.spell_list.get(), self.spell.get())
                self.item["lvl"] = self.spell_lvl.get()
                self.item["description"] = self.description.get()
                self.item["realm"] = self.realm.get()

            elif choice == "daily item":
                self.item["daily"] = self.daily.get()
                self.item["description"] = self.description.get()
                self.item["realm"] = self.realm.get()
                self.item["spell list"] = self.spell_list.get()
                self.item["spell"] = self.spell.get()
                self.item["lvl"] = self.spell_lvl.get()

            elif choice == "permanent magic item":
                self.item["description"] = self.description.get()
                self.item["pp mult"] = int(self.pp_mult.get()[1])
                self.item["add spell"] = int(self.spell_adder.get()[1])

        else:
            pass

        # subtract the costs from purse
        newpurse = buyStuff(purse = self.character["purse"], prize = self.item["worth"])

        if newpurse != self.character["purse"]:

            for i in range(0, len(coins["long"])):
                self.character["purse"][coins["short"][i].upper()] = newpurse[coins["long"][i]]

            self.character["inventory"][self.shoptype][self.elem] = self.item.copy()
            self.__quit()

        else:
            print("not enough money - ohne Moos nix los!")


    def getCosts(self):
        """
        Creates display string of costs
        """
        result = ""
        for key in coins["long"]:
            if self.price[key] > 0:
                result += str(self.price[key]) + key[0] + "p"
        return result


    def addMagicItem(self):
        '''
        This method siply adds magic itemes instead of paying the bill
        '''
        choice = self.chosen.get()
        self.item["magic"] = True
        if self.price != self.character["inventory"][self.shoptype][self.elem]["worth"]:
            self.item["worth"] = self.price.copy()
            pos = -1

            # calculate worth in smallest unit.
            for i in range(len(coins["long"]) - 1, -1, -1):
                if self.item["worth"][coins["long"][i]] > 0:
                    pos = i
                    break
            for j in range(pos - 1, -1, -1):
                self.item["worth"][coins["long"][pos]] += self.item["worth"][coins["long"][j]] * 10 ** (pos - j)
                self.item["worth"][coins["long"][j]] = 0

            if choice == "magic bonus item":
                self.item['bonus'] = int(self.item["bonus"]) + int(self.bonus.get())
                self.item["skill"] = self.catskill.get()
                self.item['description'] = self.description.get()
                self.item["weight"] = round(self.item["weight"] * float(self.weight.get()) / 100.0, 2)
                self.item["magic"] = True

            elif choice == "charged magic item":
                self.item["type"] = self.typus.get()
                self.item["spell"] = "{}\{}".format(self.spell_list.get(), self.spell.get())
                self.item["lvl"] = self.spell_lvl.get()
                self.item["description"] = self.description.get()
                self.item["realm"] = self.realm.get()

            elif choice == "daily item":
                self.item["daily"] = self.daily.get()
                self.item["description"] = self.description.get()
                self.item["realm"] = self.realm.get()
                self.item["spell list"] = self.spell_list.get()
                self.item["spell"] = self.spell.get()
                self.item["lvl"] = self.spell_lvl.get()

            elif choice == "permanent magic item":
                self.item["description"] = self.description.get()
                self.item["pp mult"] = int(self.pp_mult.get()[1])
                self.item["add spell"] = int(self.spell_adder.get()[1])

        else:
            pass

        self.character["inventory"][self.shoptype][self.elem] = self.item.copy()
        self.__quit()


    def updWidgedCont(self):
        '''
        This method updates widget content like texts or images
        '''

        for elem in self.filterlist:

            if elem == "piclink":

                if elem in self.wcont.keys():
                    self.wcont[elem] = ImageTk.PhotoImage(Image.open(self.character[elem]).resize((210, 210), Image.ANTIALIAS))
                    self.picLabel.config(image = self.wcont[elem])

                else:
                    self.wcont[elem] = ImageTk.PhotoImage(Image.open(self.character[elem]).resize((210, 210), Image.ANTIALIAS))

            elif type(self.character[elem]) == type(""):

                if elem not in self.wcont.keys():
                    self.wcont[elem] = StringVar()

                self.wcont[elem].set(self.character[elem])

            elif type(self.character[elem]) == type(0):
                if elem not in self.wcont.keys():
                    self.wcont[elem] = IntVar()

                self.wcont[elem].set(self.character[elem])

        for elem in self.bgfilter:

            if "background" in self.character.keys():

                if type(self.character["background"][elem]) == type(""):

                    if elem not in self.wcont.keys():
                        self.wcont[elem] = StringVar()

                    self.wcont[elem].set(self.character["background"][elem])

                elif type(self.character["background"][elem]) == type(0):

                    if elem not in self.wcont.keys():
                        self.wcont[elem] = IntVar()

                    self.wcont[elem].set(self.character["background"][elem])
            else:
                self.wcont[elem] = StringVar()
                self.wcont[elem].set("--")

        if "MMṔ" not in self.wcont.keys():
            self.wcont["MMP"] = IntVar()
            self.wcont["MMP"].set(0)

        elif "MMP" not in self.character.keys():
            self.character["MMP"] = calcMMP(self.character)
            self.wcont["MMP"].set(self.character["MMP"])

        for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
            if "purse" not in self.character.keys():
                self.character["purse"] = {}

            if coin not in self.character['purse'].keys():
                self.character["purse"][coin] = 0

            if coin not in self.wcont.keys():
                self.wcont[coin] = IntVar()

            self.wcont[coin].set(self.character["purse"][coin])


    def __open(self):
        """
        this method opens a character file
        ----
        @todo computation of character groups
        """
        self.opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Character Files", ".json")])
        with open(self.opendir, "r") as fp:
            self.charlist = json.load(fp)

        if type(self.charlist) == type({}):
            self.character = dict(self.charlist).copy()
            self.updWidgedCont()
        elif type(self.charlist) == [] :
            print("char list computing is not implemented yet")
            pass
        else:
            print("ERROR: wrong data format in {}".format(self.opendir))

        if "inventory" not in self.character.keys():
            self.character["inventory"] = {'weapon' :[],
                                           'armor' :[],
                                           'gear' :[],
                                           'transport':[],
                                           'herbs':[],
                                           'runes':[],
                                           'constant item':[],
                                           'daily item' :[],
                                           'gems' :[]
                                           }
        self.inv_char = self.character["inventory"].copy()


    def __save(self):
        '''
        This opens a file dialog window for saving
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Character & Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.character, fp, indent = 4)


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, self.shoptype)



class editinventory(blankWindow):
    '''
    Class for Editing indiviudal items and/or equip them as well adding newly edited items to a shop.
    '''


    def __init__(self, lang = "en", char = {}, item = {}, shoptype = "armor", storepath = "./data"):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param char dictionary holding chracter's data
        \param item dictionary holding item values
        \param shoptype item category
        \param storepath path for storing the data into the character files.
        """

        self.lang = lang
        self.character = char
        self.item = item
        self.shoptype = shoptype

        if self.character == {}:
            self.character = {  "player": "Marcus",
                                "exp": 10000,
                                'lvl' :1,
                                "prof": "Ranger",
                                "race" : "Woodmen",
                                "name": "Woody",
                                'realm' : 'Channeling',
                                "piclink" : "./data/default/pics/default.jpg"

                                }
        self.wcont = {}
        self.filterlist = ['player', 'exp', 'lvl', 'prof', 'race', 'name', 'piclink', 'realm']
        self.bgfilter = ['act_age', 'carr_weight', "sex", "height", "weight"]
        self.storepath = storepath
        blankWindow.__init__(self, self.lang)
        self.window.title("Item")
        self.__addMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addMenu(self):
        '''
        This method adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__open)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)
        self.invmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_inventory'][self.lang],
                              menu = self.invmenu)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]['armor'],
                                 command = self.__armor)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]['weapon'],
                                 command = self.__weapon)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]['gear'],
                                                 command = self.__gear)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["gems"],
                                 command = self.__gems)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["herbs"],
                                 command = self.__herbs)
        self.invmenu.add_separator()
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["spells"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["daily"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["PP_spell"],
                                  command = self.notdoneyet)
        self.invmenu.add_separator()
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["transport"],
                                 command = self.__transport)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["services"],
                                 command = self.__services)


    def __addHelpMenu(self):
        """
        This method defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __buildWin(self):
        """
        This method defines the window's layout
        """
        self.updWidgedCont()
        self.picLabel = Label(master = self.window,
                              image = self.wcont['piclink']
                              )
        # row 0
        self.picLabel.grid(column = 0,
                           row = 0,
                           columnspan = 2,
                           rowspan = 8,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)
        Label(self.window,
              textvariable = self.wcont["player"],
              justify = LEFT
              ).grid(column = 2,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["exp"],
              justify = LEFT
              ).grid(column = 3,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = "Level:",
              justify = RIGHT
              ).grid(column = 4,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["lvl"],
              justify = LEFT
              ).grid(column = 5,
                     row = 0,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        # row 1
        Label(self.window,
              textvariable = self.wcont["name"],
              justify = LEFT
              ).grid(column = 2,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["sex"],
              justify = LEFT
              ).grid(column = 3,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["prof"],
              justify = LEFT
              ).grid(column = 4,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["race"],
              justify = LEFT
              ).grid(column = 5,
                     row = 1,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 2
        Label(self.window,
              text = charattribs['act_age'][self.lang] + ":"
              ).grid(column = 2,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["act_age"]
              ).grid(column = 3,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = charattribs['height'][self.lang] + ":"
              ).grid(column = 4,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["height"]
              ).grid(column = 5,
                     row = 2,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )

        # row 3
        Label(self.window,
              text = charattribs['weight'][self.lang] + ":",
              justify = RIGHT,
              ).grid(column = 2,
                     row = 3,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["weight"]
              ).grid(column = 3,
                     row = 3,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        #row 4
        Label(self.window,
              text = charattribs['carr_weight'][self.lang] + ":"
              ).grid(column = 2,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["carr_weight"]
              ).grid(column = 3,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              text = labels['MMP'][self.lang] + ":"
              ).grid(column = 4,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        Label(self.window,
              textvariable = self.wcont["MMP"]
              ).grid(column = 5,
                     row = 4,
                     padx = 1,
                     pady = 1,
                     sticky = "EW"
                     )
        # row 5/6
        c = 2
        self.moneyEntry = {}
        for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
            Label(self.window,
                  text = coin + ":",
                  ).grid(column = c,
                         row = 5,
                         padx = 1,
                         pady = 1,
                         sticky = "EW"
                         )
            self.moneyEntry[coin] = VarInt()
            self.moneyEntry[coin].set(self.wcont[coin])
            Entry(self.window,
                  text = self.moneyEntry[coin],
                  justify = "right"
                  ).grid(column = c,
                         row = 6,
                         padx = 1,
                         pady = 1,
                         sticky = "EW"
                         )
            c += 1


    def updWidgedCont(self):
        '''
        This method updates widget content like texts or images
        '''

        for elem in self.filterlist:

            if elem == "piclink":

                if elem in self.wcont.keys():
                    self.wcont[elem] = ImageTk.PhotoImage(Image.open(self.character[elem]).resize((210, 210), Image.ANTIALIAS))
                    self.picLabel.config(image = self.wcont[elem])

                else:
                    self.wcont[elem] = ImageTk.PhotoImage(Image.open(self.character[elem]).resize((210, 210), Image.ANTIALIAS))

            elif type(self.character[elem]) == type(""):

                if elem not in self.wcont.keys():
                    self.wcont[elem] = StringVar()

                self.wcont[elem].set(self.character[elem])

            elif type(self.character[elem]) == type(0):
                if elem not in self.wcont.keys():
                    self.wcont[elem] = IntVar()

                self.wcont[elem].set(self.character[elem])

        for elem in self.bgfilter:

            if "background" in self.character.keys():

                if type(self.character["background"][elem]) == type(""):

                    if elem not in self.wcont.keys():
                        self.wcont[elem] = StringVar()

                    self.wcont[elem].set(self.character["background"][elem])

                elif type(self.character["background"][elem]) == type(0):

                    if elem not in self.wcont.keys():
                        self.wcont[elem] = IntVar()

                    self.wcont[elem].set(self.character["background"][elem])
            else:
                self.wcont[elem] = StringVar()
                self.wcont[elem].set("--")

        if "MMṔ" not in self.wcont.keys():
            self.wcont["MMP"] = IntVar()
            self.wcont["MMP"].set(0)

        elif "MMP" not in self.character.keys():
            self.character["MMP"] = calcMMP(self.character)
            self.wcont["MMP"].set(self.character["MMP"])

        for coin in ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]:
            if "purse" not in self.character.keys():
                self.character["purse"] = {}

            if coin not in self.character['purse'].keys():
                self.character["purse"][coin] = 0

            if coin not in self.wcont.keys():
                self.wcont[coin] = IntVar()

            self.wcont[coin].set(self.character["purse"][coin])


    def calcMMP(self, char = {}):
        """
        This method calculates the Movement Maneuver Penalty (MMP)
        @param char full character data as dictionary
        @retval mmp Movement Maneuver Penalty as integer
        ----
        @todo has to be fully implemented
        """
        mmp = 0
        return mmp


    def __open(self):
        """
        this method opens a character file
        ----
        @todo computation of character groups
        """
        self.opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Character Files", ".json")])
        with open(self.opendir, "r") as fp:
            self.charlist = json.load(fp)

        if type(self.charlist) == type({}):
            self.character = dict(self.charlist).copy()
            self.updWidgedCont()
        elif type(self.charlist) == [] :
            print("char list computing is not implemented yet")
            pass
        else:
            print("ERROR: wrong data format in {}".format(self.opendir))

        if "inventory" not in self.character.keys():
            self.character["inventory"] = {'weapon' :[],
                                           'armor' :[],
                                           'gear' :[],
                                           'transport':[],
                                           'herbs':[],
                                           'runes':[],
                                           'constant item':[],
                                           'daily item' :[],
                                           'gems' :[]
                                           }
        self.inv_char = self.character["inventory"].copy()


    def __save(self):
        '''
        This opens a file dialog window for saving
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Character & Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.character, fp, indent = 4)


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()


    def __armor(self):
        """
        This opens a window for armor
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "armor")


    def __weapon(self):
        """
        This opens a window for weapons
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "weapon")


    def __gear(self):
        """
        This opens a window for equipment
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "gear")


    def __transport(self):
        """
        This opens a window for animals and transports
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "transport")


    def __services(self):
        """
        This opens a window for equipment
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "services")


    def __gems(self):
        """
        This opens a window for gems and jewelery
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "gems")


    def __herbs(self):
        """
        This opens a window for portions, herbs and poisons
        """
        self. window.destroy()
        self.armorwin = shopWin(self.lang, self.character, self.storepath, shoptype = "herbs")



def buyStuff(purse = {}, prize = {}):
    """
    This function does the payment calculations
    \param purse of character
    \param prize to pay
    \retvar result new
    """
    clong = list(coins['long'])
    clong.reverse()
    cshort = list(coins["short"])
    cshort.reverse()
    for c in coins["short"]:
        if purse[c.upper()] > 0:
            pos = coins["short"].index(c)
            break

    result = money.copy()
    prize_tp = 0
    purse_tp = 0
    for i in range(0, len(clong)):
        prize_tp += prize[clong[i]] * 10 ** i
        purse_tp += purse[cshort[i].upper()] * 10 ** i

    result_tp = purse_tp - prize_tp

    if result_tp < 0:
        print("not enough money - ohne Moos nix los")
        result = purse.copy()
    else:
        for i in range(pos, len(coins["long"])):
            result[coins["long"][i]] = result_tp // 10 ** (len(coins["long"]) - 1 - i)
            result_tp -= (result_tp // 10 ** (len(coins["long"]) - 1 - i)) * 10 ** (len(coins["long"]) - 1 - i)

    return result



win = InventoryWin()
