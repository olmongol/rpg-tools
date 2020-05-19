import os
import json
from gui.window import *
from rpgtoolbox import epcalc, rpgtools as rpg
from rpgToolDefinitions.epcalcdefs import maneuvers
from pprint import pprint
from rpgToolDefinitions import inventory as inv
from tkinter import filedialog
import re

__updated__ = "19.05.2020"



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

        self.filerlist = ['player', 'exp', 'lvl', 'prof', 'race', 'name', 'piclink', 'realm']
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
                                 command = self.notdoneyet)
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
        from PIL import Image, ImageTk
        self.cpic = ImageTk.PhotoImage(Image.open(self.character["piclink"]).resize((210, 210), Image.ANTIALIAS))
        self.picLabel = Label(master = self.window,
                              image = self.cpic
                              )
        # row 0
        self.picLabel.grid(column = 0,
                           row = 0,
                           columnspan = 2,
                           rowspan = 8,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)


    def updWidgedCont(self):
        '''
        This method updates widget content like texts or images
        '''


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
