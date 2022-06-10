#!/usr/bin/env python
'''!
\file npcbuilder.py
\package npcbuilder
\brief Builder of CSV with NPC or monster statistics

This helper tool generates and changes CSV files  build from statistics of NPCs, monsters or animals.
\date (c) 2022
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "10.06.2022"
__author__ = "Marcus Schwamberger"
__me__ = "npcbulider.py"

import os
import json
from tkinter import filedialog
from tkinter.ttk import Combobox
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

logger = log.createLogger('npcbuilder', 'debug', '1 MB', 1, './', logfile = "npcbuilder.log")



class npcBuilderWin(blankWindow):
    """!
    This class generates the form window  object forNPCs data input.
    """


    def __init__(self, lang = "en", datadir = "./data/default/nscs/"):
        """!
        Constructor
        @param lang language that should be displayed. Currently supported: en, de
        @param datadir the path to the data directory
        """

        self.lang = lang
        self.datadir = datadir
        logger.debug(f"language: {self.lang}; datadir: {self.datadir}")

        self.__npcproto = {'AT': '13',
                           'DB': '30',
                           'DBm': '25',
                           'OB melee': '70 sc',
                           'OB missile': '30 sb',
                           'PP': '0',
                           'Qu': '0',
                           'comment': 'Lesser orcs',
                           'enc': '2-6',
                           'hits': '65',
                           'immune': '',
                           'lvl': '3',
                           'name': 'Orc Warrior',
                           'piclink': '/media/mongol/ferryman/Chronik/ocs_in_woods.png',
                           'size': 'M',
                           'spells': '',
                           'weakness': ''}
        ## \var self.npclist
        # list of monsters/npcs
        self.npclist = [].append(self.__npcproto)
        self.namellist = ["1", "2", "3"]

        self.fmask = [txtwin['enemygrp_files'][self.lang],
                     txtwin['all_files'][self.lang]]

        self.__currdir = os.getcwd()

        if self.datadir[0] == "/":
            self.__currdir = self.datadir

        else:
            self.__currdir += self.datadir

            if "/./" in self.__currdir:
                self.__currdir = self.__currdir.replace("/./", "/")

            elif "./" in self.__currdir:
                self.__currdir = self.__currdir.replace("./", "/")

        logger.debug(f"self.__currdir set to {self.__currdir}")

        #----- window components
        blankWindow.__init__(self, self.lang)
        self.window.title("NPC Builder")

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

        #self.helpmenu.add_separator()
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
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.openFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.saveFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['new'],
                                  command = self.newFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)
        logger.debug("file menu build")


    def __addEditMenu(self):
        '''!
        This adds an Edit menu to the windows menu bar:
        - edit current data set
        - add spells/spellist to NPC

        ----
        @todo all functions have to be  implemented
        '''
        self.editmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu["menu_edit"][self.lang],
                              menu = self.editmenu)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_data"],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_add_spell"],
                                  command = self.notdoneyet)
        self.editmenu.add_separator()
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_copy_from_master"],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_copy_to_master"],
                                  command = self.notdoneyet)


    def openFile(self):
        """!
        This opens a CSV with NPC/monster/animal data
        """
        print(self.__currdir)

        self.__filepath = askopenfilename(filetypes = self.fmask, initialdir = self.__currdir, defaultextension = ".csv")
        logger.debug(f"chosen file {self.__filepath}")
        try:

            if self.__filepath[-4:] == ".csv":
                self.npclist = readCSV(self.__filepath)
                logger.info(f"{self.__filepath} successfully read.")
                self.window.title("NPC Builder - " + self.__filepath[:-4].rsplit("/", 1)[1])
                self.__updateDisplay()

        except Exception as error:
            logger.error(f"{error}")
            messageWindow().showinfo(f"openFile: {error}", "ERROR")


    def saveFile(self):
        """!
        This method saves currently loaded npc/monster data into CSV file
        """
        self.__filepath = asksaveasfilename(defaultextension = ".csv", filetypes = self.mask, initialdir = self.__currdir)
        writeCSV(fname = self.__filepath, cont = self.npclist)
        logger.info(f"data successfully written to {self.__filepath}")


    def newFile(self):
        """!
        This starts a new list of NPCs/Monsters to store at a CSV file.

        ----
        @todo this has to be fully implemented
        """
        self.window.title("NPC Builder")
        self.npclist = [].append(self.__npcproto)
        self.__updateDisplay()
        #self.message.showinfo(message="", title)


    def __quit(self):
        '''!
        This method closes the window
        '''
        self.window.destroy()


    def __buildWin(self):
        """!
        This method buils all components of the window

        ----
        @todo this has to be fully implemented
        """
        #----- composing left frame
        leftframe = LabelFrame(master = self.window,
                               text = txtwin["selection"][self.lang],
                               width = 200,
                               relief = RIDGE)

        self.__nameSelectNPC = StringVar()
        self.__nameSelectNPC.set("")
        Entry(master = leftframe,
              width = 20,
              textvariable = self.__nameSelectNPC
              ).grid(row = 0, column = 0, sticky = "NEWS")

        inframe = Frame(master = leftframe,
                       width = 200,
                       )
        inframe.grid(row = 1, column = 0, sticky = "NEWS")

        scrollbar = Scrollbar(master = inframe, orient = "vertical")
        scrollbar.pack(side = LEFT, fill = Y)

        self.contListNPC = StringVar()
        self.contListNPC.set(self.namellist)
        listNPC = Listbox(master = inframe,
                          width = 40,
                          listvariable = self.contListNPC,
                          yscrollcommand = scrollbar.set
                          )
        listNPC.pack(fill = Y)

        #----- composing right frame
        rightframe = LabelFrame(master = self.window,
                                text = txtwin["details"][self.lang],
                                width = 600,
                                relief = RIDGE)

        #----- show it in window
        leftframe.grid(row = 0, column = 0, sticky = "NEWS")
        rightframe.grid(row = 0, column = 1, sticky = "NEWS")

        pass


    def __updateDisplay(self):
        """!
        This method updates all display widgets

        ----
        @todo this has to be fully implemented
        """
        pass



if __name__ == '__main__':
    builder = npcBuilderWin()
