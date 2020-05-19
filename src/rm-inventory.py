import os
import json
from gui.window import *
from rpgtoolbox import epcalc, rpgtools as rpg
from rpgToolDefinitions.epcalcdefs import maneuvers
from pprint import pprint
from rpgToolDefinitions import inventory as inv
from tkinter import filedialog
import re
from PIL import Image, ImageTk
__updated__ = "19.05.2020"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__version__ = "0.1"



class InventoryWin(blankWindow):
    """
    This is a GUI for EP calculation for your character party.
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
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]['gear'],
                                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["gems"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["herbs"],
                                 command = self.notdoneyet)
        self.invmenu.add_separator()
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["spells"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["daily"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["PP_spell"],
                                  command = self.notdoneyet)


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
        for coin in ["MP", "GP", "SP", "BP", "CP", "TP", "IP"]:
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

        for coin in ["MP", "GP", "SP", "BP", "CP", "TP", "IP"]:
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
        opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Character Files", ".json")])
        with open(opendir, "r") as fp:
            self.charlist = json.load(fp)

        if type(self.charlist) == type({}):
            self.character = dict(self.charlist).copy()
            self.updWidgedCont()
        elif type(self.charlist) == [] :
            print("char list computing is not implemented yet")
            pass
        else:
            print("ERROR: wrong data format in {}".format(opendir))


    def __save(self):
        '''
        This opens a file dialog window for saving
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Character & Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.charlist, fp, indent = 4)


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()


    def __armor(self):
        """
        This opens a window for armor
        """
        if "inventory" not in self.character.keys():
            self.character["inventory"] = {'weapon' :[],
                                           'armor' :[],
                                           'gear' :[],
                                           'animal':[],
                                           'herbs':[],
                                           'runes':[],
                                           'constant item':[],
                                           'daily item' :[],
                                           'gems' :[]
                                           }
        self. window.destroy()
        self.armorwin = armorWin(self.lang, self.character, self.storepath)



class armorWin(blankWindow):
    """
    Window class for character's armor
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
        self.window.title(submenu["inventory"][self.lang]["armor"])
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
        self.invmenu.add_command(label = submenu["inventory"][self.lang]['weapon'],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]['gear'],
                                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["gems"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["herbs"],
                                 command = self.notdoneyet)
        self.invmenu.add_separator()
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["spells"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu["inventory"][self.lang]["daily"],
                                 command = self.notdoneyet)
        self.invmenu.add_command(label = submenu['inventory'][self.lang]["PP_spell"],
                                  command = self.notdoneyet)
        self.addmenu


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
        for coin in ["MP", "GP", "SP", "BP", "CP", "TP", "IP"]:
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

        # row 9
        self.treeframe = Frame(self.window)
        self.treeframe.grid(colum = 0, columnspan = 6, row = 9, sticky = "NEWS")
        #XXXXXXXXXX


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

        for coin in ["MP", "GP", "SP", "BP", "CP", "TP", "IP"]:
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
        opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Character Files", ".json")])
        with open(opendir, "r") as fp:
            self.charlist = json.load(fp)

        if type(self.charlist) == type({}):
            self.character = dict(self.charlist).copy()
            self.updWidgedCont()
        elif type(self.charlist) == [] :
            print("char list computing is not implemented yet")
            pass
        else:
            print("ERROR: wrong data format in {}".format(opendir))


    def __save(self):
        '''
        This opens a file dialog window for saving
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Character & Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.charlist, fp, indent = 4)


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()



win = InventoryWin()
