#!/usr/bin/env python3
r'''!
\file monstercreator.py
\package monstercreator
\brief Tool for creating Monsters, NPCs etc.

This module creates windows for entering and editing beasts & NPCs for the GM's
master DB where creatures can be chosen from for individual campaigns.

\date (c) 2022
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.3
'''
__version__ = "0.3"
__updated__ = "08.12.2023"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__me__ = "RM RPG Tools: nsc/monster creator module"

from copy import deepcopy
from glob import glob
from pprint import pprint
from tkinter import filedialog
from tkinter.ttk import *
import csv
import json
import os
import shutil

from PIL import Image as _pilimg, Image, ImageTk
from pprint import pformat
from random import randint

from gui.window import *
from rpgToolDefinitions.magic import magicpath
from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import *
from rpgtoolbox.globaltools import *
from rpgtoolbox.handlemagic import getSpellNames

from rpgtoolbox.combatcore import prepare_attack_data, saveGMTable, loadGMTable as _loadGMTable
from rpgtoolbox.combat import getWeaponTab, createCombatList, attacktable, crittable, fumbletable


mycnf = chkCfg()
logger = log.createLogger('Monster', 'debug', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = "monstercreator.log")




class monstercreatorWin(blankWindow):
    r"""!
    This class generates a GUI to enter NSCs, monsters etc.

    ----
    @todo The following has to be implemented:
    - speed
    - weaknesses edit/display
    - immunities edit/display
    - OB magic
    """


    def __init__(self, **kwargs):
        r"""!Constructor:
        This generates the NSC/monster creator window with the read configuration given.
        @param kwargs dictionary of free key/value pairs. The following parameters will
               be computed:
               - \b config    configuration dictionary
               - \b lang    given output language
               - \b datapath    default path to store/read/find data
        """
        self.__currdir = os.getcwd()
        logger.debug(f"current dir: {self.__currdir}")
        self.__index = 0

        if "config" in kwargs.keys():
            self.__config = kwargs["config"]
            logger.debug(f"config get: {json.dumps(self.__config.cnfparam,indent=4)}")
            self.lang = self.__config.cnfparam["lang"]
            self.datapath = self.__config.cnfparam["datapath"] + "/default/"

            if self.datapath[0:2] == "./":
                self.datapath = self.__currdir + self.datapath[1:]

            if "nscpath" in self.__config.cnfparam.keys():
                self.nscpath = self.__config.cnfparam["nscpath"]

            else:
                self.nscpath = f"{self.datapath}/nscs/"

            if "nscpicpath" in self.__config.cnfparam.keys():
                self.nscpicpath = self.__config.cnfparam["nscpicpath"]

            elif "datapath" in self.__config.cnfparam.keys():
                self.nscpicpath = f"{self.datapath}/pics_nsc/"

            else:
                logger.error(f"datapath not set! Please set parameter in rpg-tools.cfg")
                firsttry = self.__currdir + "/data/default"
                logger.warn(f"Try to set datapath to {firsttry}")

                if os.path.exists(firsttry):
                    self.datapath = firsttry
                    logger.warn(f"set datapath :{self.datapath}")
                    self.nscpath = self.datapath + "/nscs/"
                    logger.warning(f"set nscpath: {self.nscpath}")
                    self.nscpicpath = self.datapath + "/pics_nsc/"
                    logger.warn(f"set nscpicpath: {self.nscpicpath}")

        else:

            if "lang" in kwargs.keys():
                self.lang = kwargs["lang"]

            else:
                self.lang = "en"

            logger.debug(f"language set to: {self.lang}")

            if "datapath" in kwargs.keys():
                self.datapath = kwargs["datapath"] + "/default/"
                logger.debug(f"datapath: {self.datapath}")

            else:
                self.datapath = f"{os.getcwd()}/data/default/"
                logger.debug(f"datapath: {self.datapath}")

            self.nscpath = f"{self.datapath}/nscs/"
            self.nscpicpath = f"{self.datapath}/pics_nsc/"

        if self.nscpath[:2] == "./":
            self.nscpath = self.__currdir + self.nscpath[1:]

        self.GMtable = self.nscpath + "gamemaster.csv"
        self.CPtable = self.nscpath + "campaigntable.csv"
        logger.debug(f"datapath set to {self.datapath}")
        logger.debug(f"nscs:     {self.nscpath}\nnscpics: {self.nscpicpath}")
        logger.debug(f"language: {self.lang}")
        self.__weaponlist = readCSV(f"{self.datapath}/fight/weapon_stats.csv")

        if self.nscpicpath[:2] == "./":
            self.nscpicpath = self.__currdir + self.nscpicpath[1:]

        self.prepareAttackData()
        self.loadGMTable()

        #---- window components
        blankWindow.__init__(self, self.lang)
        self.window.title("NSC/Monster Creator")
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
        r'''!
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save GM'],
                                  command = self.saveGM)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['new CP'],
                                  command = self.newCPTable)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open CP'],
                                  command = self.openCPTable)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save CP'],
                                  command = self.saveCP)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)
        logger.debug("file menu build")


    def __addEditMenu(self):
        r'''!
        This adds an Edit menu to the windows menu bar:

        '''
        self.editmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu["menu_edit"][self.lang],
                              menu = self.editmenu)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed choose CP"],
                                  command = self.__chooseCP)
        self.editmenu.add_separator()
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed GM table"],
                                  command = self.__newElement)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_rem_enemy"],
                                  command = self.__remoCurrentElement)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_show_NPC"],
                                  command = self.__showElements)
        self.editmenu.add_command(label = submenu["edit"][self.lang]["ed_filter"],
                                 command = self.__filterElements)
        logger.debug("edit menu build")


    def __quit(self):
        r'''!
        This method saves changes and closes the window
        '''
        self.saveGM()

        if self.NPCs != []:
            self.saveCP(filename = self.CPtable)

        self.window.destroy()


    def __buildWin(self):
        r"""!
        This method builds the window content.
        """

        #------------ row 0

        try:
            picpath = self.GMcontent[0].get("piclink", "")
            if not picpath:
                raise ValueError("piclink is empty or None")
            _img = _pilimg.open(picpath).resize((300, 300), _pilimg.Resampling.LANCZOS)
            self.selectedPic = ImageTk.PhotoImage(_img)
        except (FileNotFoundError, _pilimg.UnidentifiedImageError, OSError, ValueError) as _e:
            logger.error(f"Failed to load image: {_e}")
            self.selectedPic = ImageTk.PhotoImage()
        self.picLabel = Label(master = self.window,
                              image = self.selectedPic
                              )

        self.picLabel.grid(row = 0,
                           column = 0,
                           columnspan = 2,
                           rowspan = 12,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)
        self.picLabel.bind("<Button-1>", self.__addPic)

        self.__selectCat = StringVar()
        self.__selectCat.set(self.NPCcat[0])
        self.__catCombo = Combobox(self.window,
                                    textvariable = self.__selectCat,
                                    values = self.NPCcat)
        self.__catCombo.bind("<<ComboboxSelected>>", self.__getCategory)
        self.__catCombo.bind("<FocusOut>", self.updateCurrentSet)
        self.__catCombo.grid(row = 0, column = 2, sticky = "EW")

        Label(self.window,
              text = "Name:"
              ).grid(row = 0, column = 3, sticky = "EW")

        self.__name = StringVar()
        self.__name.set(self.currDataSet["name"])
        self.__EntryName = Entry(self.window,
                                 justify = "center",
                                 textvariable = self.__name
                                 )
        self.__EntryName.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryName.grid(row = 0, column = 4, sticky = "EW")

        Label(self.window,
              text = "Level:"
              ).grid(row = 0, column = 5, sticky = "EW")

        self.__lvl = StringVar()
        self.__lvl.set(self.currDataSet["lvl"])
        self.__EntryLvl = Entry(self.window,
                                justify = "center",
                                textvariable = self.__lvl,
                                width = 4
                                )
        self.__EntryLvl.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryLvl.grid(row = 0, column = 6, sticky = "EW")

        Label(self.window,
              text = "Hits:",
              ).grid(row = 0, column = 7, sticky = "EW")

        self.__hits = StringVar()
        self.__hits.set(self.currDataSet["hits"])
        self.__Entryhits = Entry(self.window,
                               justify = "center",
                               textvariable = self.__hits,
                               width = 8
                              )
        self.__Entryhits.bind("<FocusOut>", self.updateCurrentSet)
        self.__Entryhits.grid(row = 0, column = 8, sticky = "EW")

        #----------- row 1

        Button(self.window,
               text = txtbutton["but_prev"][self.lang],
               command = self.__prevItem
               ).grid(row = 1, column = 2, sticky = "EW")

        Label(self.window,
              text = "AT:"
              ).grid(row = 1, column = 3, sticky = "EW")

        self.__at = StringVar()
        self.__at.set(self.currDataSet["AT"])
        self.__EntryAT = Entry(self.window,
              justify = "center",
              textvariable = self.__at,
              width = 4
              )
        self.__EntryAT.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryAT.grid(row = 1, column = 4, sticky = "EW")

        Label(self.window,
              text = "Size:"
              ).grid(row = 1, column = 5, sticky = "EW")

        self.__size = StringVar()
        self.__size.set(self.currDataSet["size"])
        self.__EntrySize = Entry(self.window,
              justify = "center",
              textvariable = self.__size,
              width = 4
              )
        self.__EntrySize.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntrySize.grid(row = 1, column = 6, sticky = "EW")

        Label(self.window,
              text = "PP:"
              ).grid(row = 1, column = 7, sticky = "EW")

        self.__pp = StringVar()
        self.__pp.set(self.currDataSet["PP"])
        self.__EntryPP = Entry(self.window,
                             justify = "center",
                             textvariable = self.__pp,
                             width = 4
                             )
        self.__EntryPP.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryPP.grid(row = 1, column = 8, sticky = "EW")

        #----------- row 2

        Button(self.window,
               text = txtbutton["but_next"][self.lang],
               command = self.__nextItem
               ).grid(row = 2, column = 2, sticky = "EW")

        Label(self.window,
              text = "Qu:"
              ).grid(row = 2, column = 3, sticky = "EW")

        self.__qu = StringVar()
        self.__qu.set(self.currDataSet["Qu"])
        self.__EntryQu = Entry(self.window,
                               justify = "center",
                               textvariable = self.__qu,
                               width = 4
                               )
        self.__EntryQu.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryQu.grid(row = 2, column = 4, sticky = "EW")

        Label(self.window,
              text = "DB mis.:"
              ).grid(row = 2, column = 5, sticky = "EW")

        self.__dbm = StringVar()
        self.__dbm.set(self.currDataSet["DBm"])
        self.__EntryDBm = Entry(self.window,
                                textvariable = self.__dbm,
                                width = 4,
                                justify = "center",
                                )
        self.__EntryDBm.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryDBm.grid(row = 2, column = 6, sticky = "EW")

        Label(self.window,
              text = "DB:"
              ).grid(row = 2, column = 7, sticky = "EW")

        self.__db = StringVar()
        self.__db.set(self.currDataSet["DB"])
        self.__entryDB = Entry(self.window,
                              justify = "center",
                              textvariable = self.__db,
                              width = 4
                              )
        self.__entryDB.bind("<FocusOut>", self.updateCurrentSet)
        self.__entryDB.grid(row = 2, column = 8, sticky = "EW")

        #----------- row 3
        self.__obstring = StringVar()
        self.__obstring.set(self.currDataSet["OB melee"])
        self.__EntryOBString = Entry(self.window,
                                     justify = "center",
                                     textvariable = self.__obstring,
                                     width = 10
                                     )
        self.__EntryOBString.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryOBString.grid(row = 3, column = 2, sticky = "EW")

        Label(self.window,
              text = "OB:"
              ).grid(row = 3, column = 3, sticky = "EW")

        self.__selectOB = StringVar()
        self.__selectOB.set(self.__meleelist[0])
        self.__meleeCombo = Combobox(self.window,
                                    textvariable = self.__selectOB,
                                    values = self.__meleelist)
        self.__meleeCombo.bind("<<ComboboxSelected>>", self.__getOB)
        self.__meleeCombo.grid(row = 3, column = 4, sticky = EW)

        Label(self.window,
              text = "value:"
              ).grid(row = 3, column = 5, sticky = "EW")

        self.__obval = StringVar()
        self.__obval.set("")
        self.__EntryOBVal = Entry(self.window,
                                  justify = "center",
                                  textvariable = self.__obval,
                                  width = 10
                                  )
        self.__EntryOBVal.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryOBVal.grid(row = 3, column = 6, sticky = "EW")

        self.__selectOBsize = StringVar()
        self.__selectOBsize.set("H")
        self.__obSizeCombo = Combobox(self.window,
                                    textvariable = self.__selectOBsize,
                                    values = ["T", "S", "M", "L", "H"],
                                    width = 4)
        # self.__obSizeCombo.bind("<<ComboboxSelected>>", self.__getOB)
        self.__obSizeCombo.grid(row = 3, column = 7, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__getOB
               ).grid(row = 3, column = 8, sticky = "EW")

        #----------- row 4
        self.__obstringmis = StringVar()
        self.__obstringmis.set(self.currDataSet["OB missile"])
        self.__EntryOBMStringMis = Entry(self.window,
                                        justify = "center",
                                        textvariable = self.__obstringmis,
                                        width = 10
                                        )
        self.__EntryOBMStringMis.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryOBMStringMis.grid(row = 4, column = 2, sticky = "EW")

        Label(self.window,
              text = "OB:"
              ).grid(row = 4, column = 3, sticky = "EW")

        self.__selectOBmis = StringVar()
        self.__selectOBmis.set(self.__missilelist[0])
        self.__missileCombo = Combobox(self.window,
                                    textvariable = self.__selectOBmis,
                                    values = self.__missilelist)
        # self.__catCombo.bind("<<ComboboxSelected>>", self.__getOBm)
        self.__missileCombo.grid(row = 4, column = 4, sticky = EW)

        Label(self.window,
              text = "value:"
              ).grid(row = 4, column = 5, sticky = "EW")

        self.__obmval = StringVar()
        self.__obmval.set("")
        self.__EntryOBmVal = Entry(self.window,
                                  justify = "center",
                                  textvariable = self.__obmval,
                                  width = 10
                                  )
        self.__EntryOBmVal.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryOBmVal.grid(row = 4, column = 6, sticky = "EW")

        # self.__selectOBsize = StringVar()
        # self.__selectOBsize.set("M")
        # self.__obSizeCombo = Combobox(self.window,
        #                            textvariable = self.__selectOBsize,
        #                            values = ["T", "S", "M", "L", "H"],
        #                            width = 4)
        # self.__obSizeCombo.bind("<<ComboboxSelected>>", self.__getOB)
        # self.__obSizeCombo.grid(row = 3, column = 7, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__getOBm
               ).grid(row = 4, column = 8, sticky = "EW")

        #------- row 5
        self.__obstringmagic = StringVar()
        self.__obstringmagic.set(self.currDataSet["OB magic"])
        self.__EntryOBMStringMagic = Entry(self.window,
                                           justify = "center",
                                           textvariable = self.__obstringmagic,
                                           width = 10
                                           )
        self.__EntryOBMStringMagic.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryOBMStringMagic.bind("<Return>", self.updateCurrentSet)
        self.__EntryOBMStringMagic.grid(row = 5, column = 2, sticky = "EW")

        Label(self.window,
              text = "mag. OB:",
              ).grid(row = 5, column = 3, sticky = "EW")

        self.__selectOBmagic = StringVar()
        self.__selectOBmagic.set(self.__magiclist[0])
        self.__magicCombo = Combobox(self.window,
                                     textvariable = self.__selectOBmagic,
                                     values = self.__magiclist
                                     )
        self.__magicCombo.grid(row = 5, column = 4, sticky = "EW")

        Label(self.window,
              text = "value:"
              ).grid(row = 5, column = 5, sticky = "EW")

        self.__obmagval = StringVar()
        self.__obmagval.set("")

        self.__EntryOBmagVal = Entry(self.window,
                                  justify = "center",
                                  textvariable = self.__obmagval,
                                  width = 10
                                  )
        self.__EntryOBmagVal.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryOBmagVal.grid(row = 5, column = 6, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__getOBmag
               ).grid(row = 5, column = 8, sticky = "EW")
        #----------- XXXXXXXXXXXX
        #------- row 6
        Button(self.window,
               text = txtbutton["but_new_one"][self.lang],
               command = self.__newElement
               ).grid(row = 6, column = 2, sticky = "EW")

        Label(self.window,
              text = "enc:"
              ).grid(row = 6, column = 3, sticky = "EW")

        self.__enc = StringVar()
        self.__enc.set(self.currDataSet["enc"])
        self.__EntryEnc = Entry(self.window,
                                  justify = "center",
                                  textvariable = self.__enc,
                                  width = 4
                                  )
        self.__EntryEnc.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryEnc.bind("<Return>", self.updateCurrentSet)
        self.__EntryEnc.grid(row = 6, column = 4, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_edit_magic"][self.lang],
               command = self.__editMagic
               ).grid(row = 6, column = 5, columnspan = 2, sticky = "NEW")
        self.__magicstring = StringVar()
        self.__magicstring.set("")
        self.__EntryMagicSting = Entry(self.window,
                                       textvariable = self.__magicstring,
                                       width = 8
                                       )
        self.__EntryMagicSting.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryMagicSting.bind("<Return>", self.updateCurrentSet)
        self.__EntryMagicSting.grid(row = 6, column = 7, columnspan = 2, sticky = "NEW")
        # Button(self.window,
        #       text = txtbutton["but_show_magic"][self.lang],
        #       command = self.__editMagic
        #       ).grid(row = 5, column = 7, columnspan = 2, sticky = "NEW")

        #------- row 7
        vscroll = Scrollbar(self.window, orient = VERTICAL)
        self.__displayComment = Text(self.window,
                                  yscrollcommand = vscroll.set,
                                  height = 10
                                  )
        vscroll.config(command = self.__displayComment.yview)
        self.__displayComment.bind("<FocusOut>", self.updateCurrentSet)
        self.__displayComment.grid(row = 7, rowspan = 4, column = 2, columnspan = 4, sticky = "NEWS")
        self.__insertComment()

        Button(self.window,
               text = txtbutton["but_edit_imune"][self.lang],
               command = self.__editImunities
               ).grid(row = 7, column = 6, columnspan = 2, sticky = "NEW")

        #------- row 8

        self.__LabelImunities = Label(self.window,
                                      text = self.currDataSet["immune"]
                                      )
        self.__LabelImunities.grid(row = 8, column = 8, columnspan = 2, sticky = "NEWS")

        #------- row 9
        Button(self.window,
               text = txtbutton["but_edit_weak"][self.lang],
               command = self.__editWeaknesses
               ).grid(row = 9, column = 6, columnspan = 2, sticky = "NEW")

        #-------- row 10
        self.__LabelWeaknesses = Label(self.window,
                                       text = self.currDataSet["weakness"])
        self.__LabelWeaknesses.grid(row = 10, column = 8, columnspan = 2, sticky = "NEWS")


    def __editImunities(self, event = None):
        r"""!This opens a window to edit Imunities of NPCs / beasts

        ----
        @todo this has to be fully implemented
        """
        self.notdoneyet("__editImunities")


    def __editWeaknesses(self, event = None):
        r"""!This opens a window to edit Weaknesses of NPCs / beasts

        ----
        @todo this has to be fully implemented
        """
        self.notdoneyet("__editWeaknesses")


    def __editMagic(self, event = None):
        r"""!This opens a window to edit magic skills of NPCs / beasts

        ----
        @todo this has to be fully implemented"""
        self.magicWin = magicSelectorWin(rootwin = self, lang = self.lang, datapath = self.datapath, magicstring = self.currDataSet["spells"])


    def __showMagic(self, event = None):
        r"""!This opens a window to show magic skills of NPCs / beasts

        ----
        @todo this has to be fully implemented"""
        self.notdoneyet("__showMagic")


    def __remoCurrentElement(self, event = None):
        r"""!
        This removes the current element from the gamemaster's table

        ----
        @todo this has to be fully implemented
        """
        self.notdoneyet("removing current element is not yet implemented")


    def __newElement(self, event = None):
        r"""!
        This adds a new element to the NPC / Beast list
        """
        if self.__datatemplate not in self.GMcontent:
            self.GMcontent.append(self.__datatemplate)
            logger.debug("appended empty element to NSC / Beast list")
            self.__index = len(self.GMcontent) - 1
            self.currDataSet = deepcopy(self.__datatemplate)
            self.updateWindow()


    def __insertComment(self, event = None):
        r"""!This puts data into comment text widget"""
        self.__displayComment.delete("1.0", "end")
        self.__displayComment.insert(END, self.currDataSet["comment"])


    def __getComment(self, event = None):
        r"""!This gets data from comment text widget """
        self.currDataSet["comment"] = self.__displayComment.get("1.0", END)


    def __showElements(self, event = None):
        r"""!
        shows a table of all elements (NSCs, monsters, creatures etc.) of one category.

        ----
        @todo this hast to be fully implemented
        """
        self.notdoneyet("showElements")


    def __filterElements(self, event = None):
        r"""!
        This function filters all entries by chosen / entered options

        ----
        @todo this has to be fully implemented
        """
        self.notdoneyet("filterElements.")


    def __prevItem(self, event = None):
        r"""!
        This moves to the previous NSC / beast in the GM master table
        """
        self.updateCurrentSet()

        if self.__index > 0:
            self.__index -= 1
            self.GMcontent[self.__index + 1] = deepcopy(self.currDataSet)
            self.currDataSet = deepcopy(self.GMcontent[self.__index])
            self.updateWindow()


    def __nextItem(self, event = None):
        r"""!
        This moves to the previous NSC / beast in the GM master table
        """
        self.updateCurrentSet()

        if self.__index < len(self.GMcontent) - 1:
            self.__index += 1
            self.GMcontent[self.__index - 1] = deepcopy(self.currDataSet)
            self.currDataSet = deepcopy(self.GMcontent[self.__index])
            self.updateWindow()


    def updateWindow(self, event = None):
        r"""!
        This updates all window widgets with data of the current data set
        """
        #------- update pic
        # if self.currDataSet["piclink"][:2] == "./":
        #     self.currDataSet["piclink"] = self.__currdir + self.currDataSet["piclink"][1:]

        # elif self.currDataSet["piclink"][0] != "/":
        #     self.currDataSet["piclink"] = self.__currdir + "/" + self.currDataSet["piclink"][1:]

        try:
            picpath = self.GMcontent[0].get("piclink", "")
            if not picpath:
                raise ValueError("piclink is empty or None")
            _img = _pilimg.open(picpath).resize((300, 300), _pilimg.Resampling.LANCZOS)
            self.selectedPic = ImageTk.PhotoImage(_img)
        except (FileNotFoundError, _pilimg.UnidentifiedImageError, OSError, ValueError) as _e:
            logger.error(f"Failed to load image: {_e}")
            self.selectedPic = ImageTk.PhotoImage()
        self.picLabel.configure(image = self.selectedPic)

        #------- update category, name etc.
        self.__selectCat.set(self.currDataSet["category"])

        if self.currDataSet["category"] not in self.NPCcat:
            self.NPCcat.append(self.currDataSet["category"])
            self.NPCcat.sort()
            self.__catCombo.config(value = self.NPCcat)

        self.__name.set(self.currDataSet["name"])
        self.__lvl.set(self.currDataSet["lvl"])
        self.__hits.set(self.currDataSet["hits"])
        self.__at.set(self.currDataSet["AT"])
        self.__size.set(self.currDataSet["size"])
        self.__pp.set(self.currDataSet["PP"])
        self.__qu.set(self.currDataSet["Qu"])
        self.__dbm.set(self.currDataSet["DBm"])
        self.__db.set(self.currDataSet["DB"])
        self.__obstring.set(self.currDataSet["OB melee"])
        self.__obstringmis.set(self.currDataSet["OB missile"])
        self.__obstringmagic.set(self.currDataSet["OB magic"])
        self.__enc.set(self.currDataSet["enc"])
        self.__magicstring.set(self.currDataSet["spells"])
        self.__insertComment()
        self.__LabelImunities.config(text = self.currDataSet['immune'])
        self.__LabelWeaknesses.config(text = self.currDataSet["weakness"])


    def updateCurrentSet(self, event = None):
        r"""!
        This updates the current data set
        """
        self.currDataSet["category"] = self.__selectCat.get()
        self.currDataSet["name"] = self.__name.get()
        self.currDataSet["lvl"] = self.__lvl.get()
        self.currDataSet["hits"] = self.__hits.get()
        self.currDataSet["AT"] = self.__at.get()
        self.currDataSet["size"] = self.__size.get()
        self.currDataSet["PP"] = self.__pp.get()
        self.currDataSet["Qu"] = self.__qu.get()
        self.currDataSet["DBm"] = self.__dbm.get()
        self.currDataSet["DB"] = self.__db.get()
        self.currDataSet["OB melee"] = self.__obstring.get()
        self.currDataSet["OB missile"] = self.__obstringmis.get()
        self.currDataSet["OB magic"] = self.__obstringmagic.get()
        self.currDataSet["spells"] = self.__magicstring.get()
        if self.currDataSet["OB missile"] == "":
            self.currDataSet["OB missile"] = "0xx"

        self.currDataSet["enc"] = self.__enc.get()
        self.__getComment()
        self.GMcontent[self.__index] = deepcopy(self.currDataSet)


    def __getCategory(self, event = None):
        r'''!
        This detemines the selected category
        '''
        self.currDataSet["category"] = self.__selectCat.get()

        if self.currDataSet["category"] not in self.NPCcat:
            self.NPCcat.append(self.currDataSet["category"])


    def __getOB(self, event = None):
        r"""! This determines the selected attack for melee OB string

        ---
        @todo this has to be implemented fully.
        """
        self.updateCurrentSet()
        self.currDataSet["OB melee"] = f"{self.__obstring.get()}/{self.__obval.get()} {self.__selectOBsize.get()} {self.__attacks[self.__selectOB.get()]}"
        self.updateWindow()


    def __getOBm (self, event = None):
        r"""! This determines the selected attack for missile OB string


        """
        self.currDataSet["OB missile"] = f"{self.__obstringmis.get()}/{self.__obmval.get()} {self.__attacks[self.__selectOBmis.get()]}".strip("/")

        self.updateCurrentSet()
        self.updateWindow()


    def __getOBmag(self, event = None):
        r"""! This determins the selected attack for magic OB string
         ---
        @todo this has to be implemented fully.
        """
        self.currDataSet["OB magic"] = f"{self.__obstringmagic.get()}/{self.__obmagval.get()} {self.__attacks[self.__selectOBmagic.get()]}".strip("/")

        self.updateCurrentSet()
        self.updateWindow()


    def __addPic(self, event):
        r'''!
        This method adds the link to a NPC's /beast's picture (jpg/png)
        '''
        # os.chdir(self.nscpicpath)
        pmask = [txtwin['jpg_files'][self.lang],
                 txtwin['jpeg_files'][self.lang],
                 txtwin['png_files'][self.lang],
                 txtwin['all_files'][self.lang]
                 ]
        beastNPCpic = askopenfilename(filetypes = pmask,
                                      initialdir = self.nscpicpath
                                      )
        if self.nscpicpath[-1] == "/":
            self.piclink = f"{self.nscpicpath}{beastNPCpic.split('/')[-1]}"

        else:
            self.piclink = f"{self.nscpicpath}/{beastNPCpic.split('/')[-1]}"

        logger.debug(f"piclink set to {self.piclink}")
        self.currDataSet["piclink"] = self.piclink

        if beastNPCpic != self.piclink:
            shutil.copyfile(src = beastNPCpic, dst = self.piclink)
            logger.info(f"file copied to {self.piclink}")

        if type(self.piclink) == type("") and self.piclink:
            try:
                _img = _pilimg.open(self.piclink).resize((300, 300), _pilimg.Resampling.LANCZOS)
                self.selectedPic = ImageTk.PhotoImage(_img)
                self.picLabel.configure(image = self.selectedPic)
            except (FileNotFoundError, _pilimg.UnidentifiedImageError, OSError) as _e:
                logger.error(f"Failed to load image: {_e}")
                self.selectedPic = ImageTk.PhotoImage()
                self.picLabel.configure(image = self.selectedPic)


    def saveGM(self):
        '''
        This saves all data in the GM table
        '''
        if self.GMtable[:2] == "./":
            self.GMtable = self.__currdir + self.GMtable[1:]

        shutil.copyfile(src = self.GMtable, dst = self.GMtable[:-4] + ".old")
        self.GMcontent = remDoubletsFromList(self.GMcontent)

        with open(self.GMtable, "w") as csvfile:
            writer = csv.DictWriter(f = csvfile, fieldnames = self.__header)
            writer.writeheader()

            for entry in self.GMcontent:
                if entry["name"]:
                    writer.writerow(entry)

        logger.info(f"{self.GMtable} written successfully")
        print(f"{self.GMtable} written successfully")


    def loadGMTable(self):
        r"""!
        This loads the data of the GM default table.
        """
        self.GMcontent = readCSV(self.GMtable)
        logger.info(f"{self.GMtable} loaded successfully.")
        self.__header = list(self.GMcontent[0].keys())
        # # @var self.NPCs
        # a list of NPCs / monsters for campaigns
        self.NPCs = [dict.fromkeys(self.__header, "")]
        logger.debug(f"table header: {self.__header}")
        self.NPCcat = []

        for elem in self.GMcontent:

            if elem['category'] not in self.NPCcat:
                self.NPCcat.append(elem["category"])

        logger.info("NPCcat set")
        logger.debug(self.NPCcat)
        self.__datatemplate = dict.fromkeys(list(self.GMcontent[0].keys()), "")
        pprint(self.__datatemplate)
        if self.nscpicpath[-1] == "/":
            self.__datatemplate["piclink"] = self.nscpicpath + "default.jpg"

        else:
            self.__datatemplate["piclink"] = self.nscpicpath + "/default.jpg"

        logger.debug("data template set")
        self.GMcontent = sortDictlist(dictlist = self.GMcontent, key = "category", reverse = False)
        self.currDataSet = deepcopy(self.GMcontent[0])


    def loadCP(self):
        r"""!
        This loads a campaign NSC/monster file
        """

        loadCP = filedialog.askopenfilename(defaultextension = ".csv", filetypes = [("Table Files", ".csv")])
        self.NPCs = readCSV(loadCP)
        logger.info(f"{loadCP} loaded successfully.")


    def saveCP(self, filename = ""):
        '''
        This saves all data in the CP (campaign) table
        '''
        if self.NPCs != []:

            if not filename:
                self.CPtable = filedialog.asksaveasfilename(defaultextension = ".csv", filetypes = [("Table Files", ".csv")])

            else:
                self.CPtable = filename

            with open(self.CPtable, "w") as csvfile:
                writer = csv.DictWriter(f = csvfile, fieldnames = self.__header)
                writer.writeheader()

                for entry in self.NPCs:
                    writer.writerow(entry)

            logger.info(f"{self.CPtable} saved successfully.")


    def newCPTable(self):
        r'''!
        This opens a new campaign table an the selection window of the GM master
        table.

        ----
        @todo this has to be fully implemented
        '''
        cp = showCPWin(rootwin = self.window, CPtable = None)


    def openCPTable(self):
        r'''!This opens an existing campaign table for editing purposes

        ----
        @todo this has to be implemented fully
        '''
        self.loadCP()
        cp = showCPWin(rootwin = self.window, CPtable = self.NPCs)


    def prepareAttackData(self):
        r"""!
        This prepares the attack data for displaying widgets
        """
        # # @var self.__attacks
        # holding weapon/attack name as index and short form as value
        self.__attacks = {}
        # # @var self.__meleelist
        # list of all melee attack / weapon names
        self.__meleelist = []
        # # @var self.__missilelist
        # list of all missile/thrown attack / weapon names
        self.__missilelist = []
        # # @var self.__magiclist
        # list of elemental attack spells
        self.__magiclist = ["Fire Bolt", "Ice Bolt", "Lightning Bolt", "Shock Bolt", "Water Bolt", "Fire Ball", "Cold Ball"]
        self.__magicsc = ["Fb", "Ib", "Lb", "Sb", "Wb", "FB", "CB"]
        for w in self.__weaponlist:

            if w["wtype"] not in ["th", "mis"]:
                self.__meleelist.append(w["item"])

            if  w["wtype"] in ["th", "mis"] or "th" in w["wtype"]:
                self.__missilelist.append(w["item"])

            self.__attacks[w["item"]] = w["shortc"]

        logger.info("finished melee & missile lists and shortcuts")
        # add magic attacks and shortcuts
        for i in range(0, len(self.__magiclist)):
            self.__attacks[self.__magiclist[i]] = self.__magicsc[i]


    def __chooseCP(self):
        r"""!
        this opens a window to choose NPCs beasts you want to save in a separate
        campaign list.
        """

        CPwin = showNPCWin(rootwin = self.window, GMtable = self.GMcontent,
                           CPtable = self.NPCs, lang = self.lang)




class showNPCWin(blankWindow):
    r'''!This generates a window to show / list the content of the GM NPC / Beast DB
    and to select from for individual campaign tables.

    ----
    @todo this has to be implemented fully
    '''


    def __init__(self, rootwin, GMtable = None, CPtable = None, lang = "en", datapath = "",
                 nscpath = "", nscpicpath = ""):
        r'''!
        Constructor

        @param GMtable list of dictionaries (GM master table to select from
        @param CPtable list for individual campaign table creatures / NPCs
        @paran lang choosen language for GUI
        '''
        self.GMtable = GMtable
        self.GMtree = self.prepareDataForTreeview(self.GMtable)
        self.NPCs = CPtable
        self.CPtree = self.prepareDataForTreeview(self.NPCs)
        self.lang = lang
        self.datapath = datapath
        self.nscpath = nscpath
        self.nscpicpath = nscpicpath
        self.CPtable = f"{self.nscpath}/campaign.csv"
        self.__columns = ("category", "name", "lvl", "enc", "hits", "AT", "size")
        self.__gmitem = {}
        self.__cpitem = {}

        #---- window components
        blankWindow.__init__(self, self.lang)
        self.window.title("NSC/Monster Creator")
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
        r'''!
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        # self.filemenu.add_command(label = submenu['file'][self.lang]['save GM'],
        #                          command = self.saveGM)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['new CP'],
                                  command = self.__newCPTable)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open CP'],
                                  command = self.__openCPTable)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save CP'],
                                  command = self.__saveCPTable)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)
        logger.debug("file menu build")


    def __addEditMenu(self):
        r'''!
        This adds an Edit menu to the windows menu bar:

        ----
        @todo has to be implemended fully.
        '''
        self.editmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu["menu_edit"][self.lang],
                              menu = self.editmenu)
        # self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_add_enemy"],
        logger.debug("edit menu build")


    def __quit(self):
        r'''!
        This method saves changes and closes the window
        '''
        self.__saveCPTable(self.CPtable)
        self.window.destroy()


    def __buildWin(self):
        r"""!
        This method builds the window content.

        ----
        @todo This has to be fully implemented:
        - magic / spell lists are still missing
        """

        self.gmtree = Treeview(self.window,
                               selectmode = "extended",
                               columns = self.__columns[1:],
                               height = 20
                               )
        self.gmtree.grid(row = 0, column = 0, rowspan = 5, sticky = "NEWS")
        self.oldcat = ""
        self.catid = 0
        self.cats = {}

        #------- build header for self.gmtree
        self.gmtree.heading("#0", text = self.__columns[0])

        self.gmtree.heading(self.__columns[1], text = self.__columns[1])

        for header in self.__columns[2:]:
            self.gmtree.heading(header, text = header)
            self.gmtree.column(header, minwidth = 0, width = 50, stretch = NO)

        #------- add a scrollbar to self.gmtree
        gmscrollbar = Scrollbar(self.window, orient = VERTICAL, command = self.gmtree.yview)
        self.gmtree.configure(yscroll = gmscrollbar.set)
        gmscrollbar.grid(row = 0, column = 1, rowspan = 5, sticky = "NS")

        #------- fill self.gmtree with content
        for elem in self.GMtree:

            if elem[0] != self.oldcat:
                self.oldcat = elem[0]
                self.cats[self.oldcat] = self.catid
                self.gmtree.insert('', END, iid = self.catid, text = self.oldcat)
                self.gmtree.insert(self.catid, END, values = tuple(elem[1:]))
                self.catid += 1

            else:
                self.gmtree.insert(self.catid - 1, END, values = tuple(elem[1:]))

        self.gmtree.bind('<<TreeviewSelect>>', self.__GMItemSelected)

        #------- column between the 2 treeviews
        Button(self.window,
               text = txtbutton["but_right"][self.lang],
               command = self.__pushToCP
               ).grid(row = 1, column = 2, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_left"][self.lang],
               command = self.__remFromCP
               ).grid(row = 2, column = 2, sticky = "EW")

        #------- self.cptree for campaigns
        self.cptree = Treeview(self.window,
                               selectmode = "extended",
                               columns = self.__columns[1:],
                               height = 20
                               )
        self.cptree.grid(row = 0, column = 3, rowspan = 5, sticky = "NEWS")

        #------- build header for self.cptree
        self.cptree.heading("#0", text = self.__columns[0])

        self.cptree.heading(self.__columns[1], text = self.__columns[1])

        for header in self.__columns[2:]:
            self.cptree.heading(header, text = header)
            self.cptree.column(header, minwidth = 0, width = 50, stretch = NO)

        #------- add a scrollbar to self.cptree
        cpscrollbar = Scrollbar(self.window, orient = VERTICAL, command = self.cptree.yview)
        self.cptree.configure(yscroll = cpscrollbar.set)
        cpscrollbar.grid(row = 0, column = 4, rowspan = 5, sticky = "NS")

        #------- fill self.cptree with content
        for catkey in self.cats.keys():
            self.cptree.insert('', END, iid = self.cats[catkey], text = catkey)

        for elem in self.CPtree:

            if elem[0] != self.oldcat:
                self.oldcat = elem[0]

                if self.oldcat not in self.cats.keys():
                    self.cats[self.oldcat] = self.catid
                    self.catid += 1

                self.cptree.insert('', END, iid = self.cats[self.oldcat], text = self.oldcat)
                self.cptree.insert(self.cats[self.oldcat], END, values = tuple(elem[1:]))
                # self.catid += 1

            else:
                self.cptree.insert(self.catid - 1, END, values = tuple(elem[1:]))

        self.cptree.bind('<<TreeviewSelect>>', self.__CPItemSelected)


    def __GMItemSelected(self, event = None):
        r"""!This handles the detailed display of the selected treeview item
        """
        self.__gmitem = []
        self.__gm_parent_id = []

        for selected_item in self.gmtree.selection():

            if self.gmtree.item(selected_item)["values"]:
                self.__gmitem.append(self.gmtree.item(selected_item))
                self.__gm_parent_id.append(self.gmtree.parent(selected_item))
                # print(f"DEBUG {json.dumps(self.__gmitem, indent = 3)}")
                # print(f"DEBUG {selected_item}")


    def __CPItemSelected(self, event = None):
        r"""!This handles the detailed display of the selected treeview item

        ----
        @note currently it is a dummy method

        @todo this has to be fully implemented
        """
        self.__cpitem = []

        for selected_item in self.cptree.selection():
            self.__cpitem.append(self.cptree.item(selected_item))
            # print(json.dumps(self.__cpitem, indent = 3))


    def __pushToCP(self, event = None):
        r"""!
        This copies items from the GM NPC list / treeview to the campaign list / treeview
        """
        for i in range(0, len(self.__gmitem)):
            values = self.__gmitem[i]["values"]

            if not self.__existInTreeview(treeview = self.cptree, comparevalues = self.__gmitem[i]["values"]):
                self.cptree.insert(self.__gm_parent_id[i], END, values = tuple(values))

            #------- find in GMtable
            for npc in self.GMtable:

                if npc["name"] == values[0] and npc["lvl"] == str(values[1]) and npc not in self.NPCs:
                    self.NPCs.append(npc)
                    logger.debug(f"{npc['name']} added to campaign list")
                    self.NPCs = sortDictlist(self.NPCs, "category", False)
                    break


    def __remFromCP(self, event = None):
        r"""!
        This removes items from the campaign list / treeview
        """
        rowid = self.cptree.focus()
        values = self.cptree.item(rowid)["values"]

        if 'I' in rowid:
            self.cptree.delete(rowid)

        for elem in self.NPCs:

            if elem["name"] == values[0] and elem["lvl"] == str(values[1]):
                self.NPCs.remove(elem)
                logger.debug(f"removed {elem['name']} from list.")
                break


    def __newCPTable(self, event = None):
        r"""!
        This initializes a new (empty) NPC / Beast table for campaigns

        ----
        @todo This has to be fully implemented
        """
        self.notdoneyet("__newCPTable")


    def __existInTreeview(self, treeview, comparevalues = None):
        r"""!This checks if a value set already exists in a treeview widget

        @param treeview treeview widget to check
        @param comparevalues values to check for existence in the treeview

        @return result is a boolean with indicates if comparevalues found in the treeview
        """
        toplvl = treeview.get_children()

        for parents in toplvl:
            children = treeview.get_children(parents)

            for child in children:
                logger.debug("working on {child}/{children}")
                values = treeview.item(child)["values"]

                if comparevalues == values:
                    logger.debug(f"found {comparevalues} in treeview")
                    return True

        logger.debug(f"does not find {comparevalues} in treeview")
        return False


    def __openCPTable(self):
        r"""!
        This loads a campaign NSC/monster file
        """

        loadCP = filedialog.askopenfilename(defaultextension = ".csv", filetypes = [("Table Files", ".csv")])
        self.NPCs = readCSV(loadCP)
        self.CPtree = self.prepareDataForTreeview(self.NPCs)
        logger.info(f"{loadCP} loaded successfully.")
        self.__updateDataLists()


    def __saveCPTable(self, filename = ""):
        '''
        This saves all data in the CP (campaign) table
        '''
        # print(f"DEBUG: save {json.dumps(self.NPCs,indent=4)}")
        if self.NPCs != []:

            if not filename:
                self.CPtable = filedialog.asksaveasfilename(defaultextension = ".csv", filetypes = [("Table Files", ".csv")])

            else:
                self.CPtable = filename

            with open(self.CPtable, "w") as csvfile:
                writer = csv.DictWriter(f = csvfile, fieldnames = list(self.NPCs[0].keys()))
                writer.writeheader()

                for entry in self.NPCs:

                    if entry["name"]:
                        writer.writerow(entry)

            logger.info(f"{self.CPtable} saved successfully.")


    def prepareDataForTreeview(self, dictlist = None, fields = None):
        if fields is None:
            fields = ["category", "name", "lvl", "enc", "hits", "AT", "size"]
        r"""!This prepares data for the treeview widget

        @param dictlist list of dictionaries for preparation
        @param fields fields for the tuples in result
        @retval result list for treeview
        """
        # print(json.dumps(dictlist, indent = 4))
        result = []

        # Sort dictlist so 'Other' appears last, rest alphabetically
        def cat_sort_key(entry):
            cat = entry.get('category', '').lower()
            return (cat == 'other', cat)
        if dictlist:
            dictlist = sorted(dictlist, key=cat_sort_key)
            dummy = []

            for creature in dictlist:

                if creature["name"]:

                    for field in fields:
                        dummy.append(creature[field])

                    result.append(dummy)
                    logger.debug(f"entry: {dummy}")
                    dummy = []

                else:
                    pass
            logger.debug(f"result: {json.dumps(result,indent=4)}")

        return result


    def __updateWin(self, event = None):
        r"""!
        This updates teh windows widgets

        ----
        @todo has to be fully implemented
        """

        pass


    def __updateDataLists(self, event = None):
        r"""!This updates all internal data lists

        ----
        @todo this has ti be fully implemented
        """
        # for catkey in self.cats.keys():
        #    self.cptree.insert('', END, iid = self.cats[catkey], text = catkey)

        for elem in self.CPtree:

            if elem[0] != self.oldcat:
                self.oldcat = elem[0]

                if self.oldcat not in self.cats.keys():
                    logger.debug(f"updtdlist cats={json.dumps(self.cats,indent=3)}")
                    self.cats[self.oldcat] = self.catid
                    self.cptree.insert('', END, iid = self.cats[self.oldcat], text = self.oldcat)
                    self.catid += 1

                self.cptree.insert(self.cats[self.oldcat], END, values = tuple(elem[1:]))
                # self.catid += 1

            else:
                self.cptree.insert(self.catid - 1, END, values = tuple(elem[1:]))




class magicSelectorWin(blankWindow):
    r"""!
    This generates a window to select spell lists and determine their level for a NPC
    or a beast.
    """


    def __init__(self, rootwin = None, lang = "en", datapath = "./data", magicstring = ""):
        r"""!
        Constructor

        @param datapath configured data path
        @param magicstring string that holds the spell lists and levels
        """
        # #\var self.rootwin
        # the reference to the root window/object \ref monstercreatorWin to transfer finally the modified
        # #magicstring back
        self.rootwin = rootwin
        self.lang = lang
        self.__datapath = datapath

        if self.__datapath[:2] == "./":
            self.__datapath = os.getcwd() + self.__datapath[1:]

        if  "/magic" not in self.__datapath:
            self.__datapath = self.__datapath.rstrip("/") + "/magic"

        # #\var self.magicstring
        # this is the string for all the spell lists, their types and their levels
        self.magicstring = magicstring.strip(" ").replace(" ", "_")

        if self.magicstring:
            self.magiclist = self.magicstring.split(";")

        else:
            self.magiclist = []

        self.__loadMagic()
        self.__prepSelectedMagic()

        #---- window components
        blankWindow.__init__(self, self.lang)
        self.window.title("NSC/Monster Magic Selector")
        # self.topmagic = Toplevel(self.window)
        # self.topmagic.title("NSC/Monster Magic Selector")
        # self.topmagic.grab_set()
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addHelpMenu()
        self.__buildWin()
        # self.window.mainloop()

        pass


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
        r'''!
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        # self.filemenu.add_command(label = submenu['file'][self.lang]['save GM'],
        #                          command = self.saveGM)
        # self.filemenu.add_separator()
        # self.filemenu.add_command(label = submenu['file'][self.lang]['new CP'],
        #                          command = self.__newCPTable)
        # self.filemenu.add_command(label = submenu['file'][self.lang]['open CP'],
        #                          command = self.__openCPTable)
        # self.filemenu.add_command(label = submenu['file'][self.lang]['save CP'],
        #                          command = self.__saveCPTable)
        # self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)
        logger.debug("file menu build")


    def __addEditMenu(self):
        r'''!
        This adds an Edit menu to the windows menu bar:

        ----
        @todo has to be implemended fully.
        '''
        self.editmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu["menu_edit"][self.lang],
                              menu = self.editmenu)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_filter"],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_search"],
                                  command = self.notdoneyet)
        logger.debug("edit menu build")


    def __quit(self):
        r'''!
        This method saves changes and closes the window
        '''
        self.__finalize()
        self.__updMagicRoot()
        self.window.destroy()


    def __buildWin(self):
        r"""!
        This method builds the window content.

        ----
        @todo This has to be fully implemented
        """
        header = ["Spell List Type", "Spell List", "Level"]

        #------- row 0
        Label(self.window,
              text = labels["avail magic"][self.lang],
              ).grid(row = 0, column = 1, columnspan = 3, pady = 5, sticky = "EW")

        Label(self.window,
              text = labels["selected magic"][self.lang]
              ).grid(row = 0, column = 5, columnspan = 3, pady = 5, sticky = "NEWS")

        #------- row 1
        self.allMagicTree = Treeview(self.window,
                                     selectmode = "extended",
                                     columns = header[1:-1],
                                     height = 20
                                     )
        self.allMagicTree.grid(row = 1, column = 0, rowspan = 5, columnspan = 3, sticky = "NEWS")
        self.allMagicTree.heading("#0", text = header[0])
        self.allMagicTree.heading(header[1], text = header[1])

        allMscrollbar = Scrollbar(self.window, orient = VERTICAL, command = self.allMagicTree.yview)
        self.allMagicTree.configure(yscroll = allMscrollbar.set)
        allMscrollbar.grid(row = 1, column = 4, rowspan = 5, sticky = "NS")

        #----- fill self.allMagicTree with self.__magicdict
        oldtype = ""
        index = 0
        keylist = list(self.__magicdict.keys())
        keylist.sort()
        # # @var self.__magicParents
        # a dictionary holding  the spell list type as value and the concerned
        # treeview index as index (for faster identification later on)
        self.__magicParents = {}

        for key in keylist:

            if oldtype != key:
                index += 1
                oldtype = key
                self.__magicParents[index] = oldtype

            self.allMagicTree.insert('', END, iid = index, text = oldtype)

            for sl in self.__magicdict[oldtype]:
                self.allMagicTree.insert(index, END, values = (sl))
            # for sl in self.__magicdict[oldtype]:
            #    self.allMagicTree.insert(index,E)

        Label(self.window,
              text = labels["lvl"][self.lang],
              ).grid(row = 1, column = 5, pady = 5, padx = 5, sticky = "EWs")

        self.selectedMagicTree = Treeview(self.window,
                                          selectmode = "extended",
                                          columns = header[1:],
                                          height = 20
                                          )
        self.selectedMagicTree.grid(row = 1, column = 6, rowspan = 5, columnspan = 3, sticky = "NEWS")
        self.selectedMagicTree.heading("#0", text = header[0])
        self.selectedMagicTree.heading(header[1], text = header[1])
        self.selectedMagicTree.heading(header[2], text = header[2])

        selMscrollbar = Scrollbar(self.window, orient = VERTICAL, command = self.selectedMagicTree.yview)
        self.selectedMagicTree.configure(yscroll = selMscrollbar.set)
        selMscrollbar.grid(row = 1, column = 9, rowspan = 5, sticky = "NS")
        self.__checkMagicString()
        #------- row 2

        self.__splvl = []

        for elem in list(range(1, 21)) + [25, 30, 50]:
            self.__splvl.append(elem)

        self.__levelSL = IntVar()
        self.__levelSL.set(1)
        self.__slCombo = Combobox(self.window,
                                  textvariable = self.__levelSL,
                                  values = self.__splvl,
                                  width = 4,
                                  justify = "center"
                                  )
        self.__slCombo.grid(row = 2, column = 5, sticky = "NEW")
        self.__slCombo.bind("<<ComboboxSelected>>", self.__slComboGet)

        #------- row 3
        Button(self.window,
               text = txtbutton["but_right"][self.lang],
               command = self.__addSpellList
               ).grid(row = 3, column = 5, sticky = "NEWS")

        #------- row 4
        Button(self.window,
               text = txtbutton["but_left"][self.lang],
               command = self.__deleteSpellList
               ).grid(row = 4, column = 5, sticky = "NEWS")

        #------- row 5

        Button(self.window,
               text = txtbutton["but_fin"][self.lang],
               command = self.__finalize
               ).grid(row = 5, column = 5, sticky = "EW")


    def __prepSelectedMagic(self):
        r"""!
        This initially prepares the internal data structure self.__selectedMagic
        for treeview from self.magicstring
        """
        # #\var self.__selectMagic
        # a dictionary that holds the type of spell list as primary index, the
        # spell list as secondary and the level as value
        self.__selectedMagic = {}
        spellists = self.magicstring.split(";")

        for elem in spellists:
            dummy = elem.split("/")

            if dummy[0] not in self.__selectedMagic.keys():
                self.__selectedMagic[dummy[0]] = {}

            if len(dummy) > 1:
                dummy2 = dummy[1].split(":")
                self.__selectedMagic[dummy[0]][dummy2[0]] = dummy2[1]


    def __loadMagic(self):
        r"""!
        This Loads all the available Spell lists
        """
        allfiles = glob(self.__datapath + "/*/*.csv")

        # # \var self.__magicdict
        # a dictionary for all available spell lists with spell list kind as index
        # and spell list name as value.
        self.__magicdict = {}

        for elem in allfiles:
            dummy = elem[:-4].rsplit("/", 2)

            if dummy[1] not in self.__magicdict.keys():
                self.__magicdict[dummy[1]] = [dummy[2]]

            else:
                self.__magicdict[dummy[1]].append(dummy[2])

        logger.debug(f"magicdict: {json.dumps(self.__magicdict,indent=4)}")


    def __addSpellList(self, event = None):
        r"""!This adds a selected spell list with the selected level to the list

        ----
        @todo this has  to be fully implemented
        """
        self.__getSelectedSL()
        lvl = self.__levelSL.get()
        # print(f"DEBUG: {self.__SLitem}\n\t{self.__SL_parent_id}")

        for i in range(0, len(self.__SLitem)):
            values = self.__SLitem[i]["values"]
            values.append(lvl)

            try:
                # try to insert parent
                self.selectedMagicTree.insert('', END, iid = self.__SL_parent_id[i], text = self.__magicParents[int(self.__SL_parent_id[i])])
                logger.debug(f"add {self.__magicParents[self.__SL_parent_id[i]]} to selection tree")

            except Exception as e:
                # parent already exists... or duplicate ID — expected in normal flow
                logger.debug(f"insert parent failed (likely already exists): {e}")
                pass

            finally:

                if not self.__existInTreeview(treeview = self.selectedMagicTree, comparevalues = self.__SLitem[i]["values"]):
                    self.selectedMagicTree.insert(self.__SL_parent_id[i], END, values = tuple(values))
                    # print(f"DEBUG Values: {values}")


    def __deleteSpellList(self, event = None):
        r"""!
        This removes a selected spell list from the list of selected spell lists.
        """
        selected_items = self.selectedMagicTree.selection()
        for item in selected_items:
            self.selectedMagicTree.delete(item)

        self.__finalize()


    def __slComboGet(self, event = None):
        r"""!
        A dirty workaround because the class has to be re-factored for Toplevel instead mainloop
        """
        self.__levelSL.set(self.__slCombo.get())


    def __getSelectedSL(self):
        r"""!
        This gets the selection of treeview items
        """
        self.__SLitem = []
        self.__SL_parent_id = []

        for selected_item in self.allMagicTree.selection():

            if self.allMagicTree.item(selected_item)["values"]:
                self.__SLitem.append(self.allMagicTree.item(selected_item))
                self.__SL_parent_id.append(self.allMagicTree.parent(selected_item))


    def __existInTreeview(self, treeview, comparevalues = None):
        r"""!
        This checks if a value set already exists in a treeview widget

        @param treeview treeview widget to check
        @param comparevalues values to check for existence in the treeview

        @return result is a boolean with indicates if comparevalues found in the treeview
        """
        toplvl = treeview.get_children()

        for parents in toplvl:
            children = treeview.get_children(parents)

            for child in children:
                logger.debug(f"working on {child}/{children}")
                values = treeview.item(child)["values"]
                logger.debug(f"values {values}/{comparevalues}")

                if comparevalues == values:
                    logger.info(f"found {comparevalues} in treeview")
                    return True

        logger.info(f"does not find {comparevalues} in treeview")
        return False


    def __finalize(self, event = None):
        r"""!
        This builds a new #magicstring
        """
        self.magicstring = ""

        for parent in  self.selectedMagicTree.get_children():
            spcat = self.selectedMagicTree.item(parent)["text"]

            for child in self.selectedMagicTree.get_children(parent):
                values = self.selectedMagicTree.item(child)["values"]
                self.magicstring += f"{spcat}/{values[0]}:{values[1]};"

        self.magicstring = self.magicstring.strip(";")
        logger.debug(f"magicstring: {self.magicstring}")
        self.__updMagicRoot()


    def __updMagicRoot(self):
        r"""!
        This generates a new #magicstring from data of #selectedMagicTree and
        hands it over to  \ref monstercreatorWin
        """
        self.rootwin.currDataSet["spells"] = deepcopy(self.magicstring).replace("_", " ")
        self.rootwin.updateWindow()
        # self.__quit()


    def __checkMagicString(self):
        r"""!
        This enters the data of an existing #magicstring into the #selectedMagicTree
        """
        if self.magiclist:

            for elem in self.magiclist:
                cat, sl = elem.split("/")
                sl, lvl = sl.split(":")

                for index in self.__magicParents.keys():

                    if cat == self.__magicParents[index]:

                        try:
                            self.selectedMagicTree.insert('', END, iid = int(index), text = cat)

                        except Exception as e:
                            logger.debug(f"insert magic parent failed (likely already exists): {e}")
                            pass

                        finally:
                            self.selectedMagicTree.insert(int(index), END, values = (sl, int(lvl)))

                        break




class showCPWin(Toplevel, blankWindow):
    r'''!
    This generates a display window for individual campaign tables

    ----
    @todo this has to be fully implemented
    '''


    def __init__(self, rootwin, CPtable = None):
        r'''!constructor
        @param CPtable list of dictionaries (NPCs / Monster data) of campaign table
        '''
        super().__init__(rootwin)
        self.CPtable = CPtable
        self.notdoneyet("showCPWin")


# ============================================================================
# --- Recovery block (TR-003): original attackcheck classes from b30b498 -----
# The following classes were lost during the s3/s3d modularization refactor
# (commits c2f6531 & 30e1e8a) and are restored here from the last healthy
# commit (b30b498) to recreate the "attack check / fight" feature.
#
#   calFightEP        – combat EP calculation helpers
#   atWin             – main "attack check" window (party vs. enemies)
#   enemySelector     – enemy-group picker window
#
# The launcher src/attackcheck.py now instantiates atWin() (see TR-001).
# ============================================================================

# Imports required by the recovered block (not already in this module's header)
from random import randint
from rpgToolDefinitions.helptools import RMDice as Dice
from rpgToolDefinitions.magic import magicpath
from rpgtoolbox.handlemagic import getSpellNames
import json
from rolemaster.specials import *


class calFightEP():
    """!
    @todo has to be fully implemented: shall store EPs for fights
    """


    def __init__(self, charlist = {}, tempfile = "./epfight.json"):
        pass


class atWin(blankWindow):
    """!
    This class generates a window where you can look up your attack results.
    Results of dice rolls may be entered or a roll may be done by clicking a
    button.

    ----
    @todo
    - adding fight with ball magic
    - adding & Storing ammo for missile combat (inventory)
    - adding Weapon bonus if equipped in inventory
    - adding DB of amor & artefacts if equipped from inventory.
    - use breakage tests
    - storing character status (hits, mods etc.)

    ----
    @bug known bugs are the following:
    - you cannot proceed with next attacker if missile weapons are selected
    - you cannot proceed with next attacker if he was disabled by damage (stun, etc)
    - Bastard Sword goes on Brawling Table
    """


    def __init__(self, lang = "en", datadir = "./data/default"):
        r"""!
        Constructor
        \param lang selected output language
        \param datadir configured default datadir
        """
        logger.debug(f"language: {lang}\n datadir: {datadir}")
        self.lang = lang
        self.datadir = datadir

        if "/default" not in self.datadir:
            self.datadir = self.datadir.strip("/") + "/default"

        logger.info(f"language: {lang}")
        logger.info(f"data dir: {datadir}")
        # # @var self.fumbletype
        # attack type for fumble checks
        self.fumbletype = 'one-handed arms'
        self.fumbleroll = 0
        self.umr = 5
        # # @var self.maxfumble
        # the maximum value for fumble results.
        self.maxfumble = 4
        # # @var self.attacktbls
        # dictionary holding all (found) attack tables
        self.attacktbls = {}
        # # @var self.crittbls
        # dictionaray holding all (found) crit tables
        self.crittbls = {}
        # # @var self.attackers
        # list of all combatants able to attack
        self.attackers = ["Egon"]
        # # @var self.defenders
        # list of all combatants who are still alive
        self.defenders = ["Anton"]
        # # @var self.combatants
        # inital list of all combatants (at the begin of battle)
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
        # # \var self.weapontab
        # holds the given weapon table as dictionary with short term as master key
        # and all information about the weapon (such as fumble or breaking numbers)
        self.weapontab = getWeaponTab()
        logger.info("Weapon tables successfully read.")

        self.__modstun = 0
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

        # # \var self.weaponlist
        # a list of dictionaries holding all infomation about all weapons. If a
        # weapon has no specific attack table the standard attack table for it
        # will be documented here.
        self.weaponlist = readCSV(f"{self.datadir}/fight/weapon_stats.csv")
        logger.info("list of weapons read successfully.")
        self.__prepareWL()
        logger.debug("list of weapons successfully prepared for usage.")
        # # \var self.reverseweaponindex
        # This dictionary holds weapon name as key and short form as value
        self.reverseweaponindex = {}

        self.weaponfumble = fumbletable(tablefilename = self.datadir + f"/fight/fumble/combat_fumble_{self.lang}.csv", lang = self.lang)
        self.magicfumble = fumbletable(tablefilename = self.datadir + f"/fight/fumble/spell_fumble_{self.lang}.csv", lang = self.lang)

        for key in self.weapontab.keys():
            self.reverseweaponindex[self.weapontab[key]["name"]] = key

        logger.info("weapon index prepared.")

        # read all attack tables
        for table in os.listdir("{}/fight/attacks".format(self.datadir)):
            logger.debug(f"working on {table}")

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

        # window components
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
        self.editmenu.add_separator()
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_add_wpn"],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = labels["ammo"][self.lang],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_heal_char"],
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["init"],
                                  command = self.__rollInit)
        self.editmenu.add_separator()
        self.editmenu.add_command(label = submenu["edit"][self.lang]["history"],
                                  command = self.notdoneyet)
        self.editmenu.add_separator()
        self.editmenu.add_command(label = "Save Party Status",
                                  command = self.savePartyStatus)
        logger.debug("edit menu build")


    def savePartyStatus(self):
        """
        Save combat status (hits, PP, conditions) back to character JSON files.
        Reads initlist status and writes it to loaded __fullparty.
        Returns: number of combatants saved, or 0 on error.
        """
        if not hasattr(self, '__source_party_file') or not self.__source_party_file:
            logger.warning("No party file loaded, cannot save status.")
            return 0

        if not hasattr(self, '__fullparty') or not self.__fullparty:
            logger.warning("No party data loaded, cannot save status.")
            return 0

        # map name -> index in __fullparty
        name_to_idx = {}
        for i, c in enumerate(self.__fullparty):
            if 'name' in c:
                name_to_idx[c['name']] = i

        saved_count = 0

        for ic in self.initlist:
            name = ic.get('name', '')
            if name not in name_to_idx:
                logger.warning("Combatant '%s' not found in loaded party, skipping.", name)
                continue

            char_entry = self.__fullparty[name_to_idx[name]]

            # Ensure status dict exists
            if 'status' not in char_entry or not isinstance(char_entry['status'], dict):
                char_entry['status'] = {}

            # Write initlist values back to status
            cur_hp = ic.get('hits', 0)
            char_entry['status']['current_hp'] = cur_hp
            char_entry['status']['max_hp'] = ic.get('max_hits', cur_hp)
            char_entry['status']['current_pp'] = ic.get('PP', 0)
            char_entry['status']['max_pp'] = ic.get('PPmax', 0)
            char_entry['status']['stunned'] = ic['status'].get('stunned', 0)
            char_entry['status']['ooo'] = ic['status'].get('ooo', 0)
            char_entry['status']['bleed'] = ic['status'].get('bleed', 0)
            char_entry['status']['mod_total'] = ic['status'].get('mod_total', 0)
            char_entry['status']['no_parry'] = ic['status'].get('no_parry', 0)
            saved_count += 1

        # Write back to file
        if saved_count:
            try:
                with open(self.__source_party_file, 'w') as fp:
                    json.dump(self.__fullparty, fp, indent=4, ensure_ascii=False)
                logger.info("Saved combat status for %d combatant(s) %s", saved_count, self.__source_party_file)
            except Exception as e:
                logger.error("Failed to save party status: %s", e)
            return saved_count
        else:
            logger.warning("No combatants were saved.")
            return 0


    def openParty(self):
        '''!
        This method reads a character party group file to self.partygrp
        '''
        self.__partypath = askopenfilename(filetypes = self.fmaskc, initialdir = os.getcwd(), defaultextension = ".json")
        logger.debug(f"chosen group file {self.__partypath}")

        try:
            with open(self.__partypath, "r") as fp:
                # #@var self.__fullparty
                # This is holding the full party data
                self.__fullparty = json.load(fp)

            logger.info(f"{self.__partypath} was read")

            if type(self.__fullparty) == type({}):
                self.__fullparty = [self.__fullparty]

            logger.debug("fullparty initialized.")

            self.__source_party_file = self.__partypath  # for savePartyStatus()
            self.__prepareChars()

        except Exception as error:
            logger.error(f"{error}")
            self.message = messageWindow()
            self.message.showinfo(f"{error}", "ERROR")

        # self.__prepareChars()


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
              - set max level of attack
              - implement Weapon breakage
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

            # generate OB lists

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

                # # add fumble number
                # melee[j].append(int(self.weapontab[melee[j][0]]['fumble']))
                # # add breakage number
                # melee[j].append(int(self.weapontab[melee[j][0]]['breakage']))

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
                # #@var wt
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
        self.__selectDefender.set(self.defenders[0])
        self.__updDefCombo()
        self.__updtAttckCombo()
        self.__chgImg(attackerpic = "", defenderpic = self.enemygrp[0]["piclink"])
        logger.info("__prepareNSCs: enemygrp set")
        logger.debug(f"__prepareNSCs: \n{pformat(self.enemygrp)}")


    def __prepareChars(self):
        '''!
        This method reduces character data to combatant data

        ----
        '''
        self.partygrp = []
        cindex = ["player", "name", "DB", "DB mod", "OB melee", "OB missile", "hits", "PP",
                "AT", "lvl", "spells", "init", "piclink"]

        melee = ["Martial Arts - Striking", "Martial Arts - Sweeps", "Weapon - 1-H Concussion",
                "Weapon - 1-H Edged", "Weapon - 2-Handed", "Weapon - Pole Arms",
                "Weapon - 1-H Concussion", "Weapon - 1-H Edged", "Weapon - 2-Handed", "Special Attacks"]
        missile = ["Weapon - Missile", "Weapon - Missile Artillery", "Weapon - Thrown"]
        magic = ["Directed Spells"]
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
            logger.debug(f"character's Qu: {dummy['Qu']}")

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

            # read status section from JSON (persisted combat state)
            if "status" in char and isinstance(char["status"], dict):
                dummy["hits"] = char["status"].get("current_hp", 0)
                dummy["max_hits"] = char["status"].get("max_hp", dummy["hits"])
                dummy["PP"] = char["status"].get("current_pp", 0)
                dummy["PPmax"] = char["status"].get("max_pp", dummy["PP"])
                dummy["status"] = {
                    "stunned": char["status"].get("stunned", 0),
                    "ooo": char["status"].get("ooo", 0),
                    "bleed": char["status"].get("bleed", 0),
                    "mod_total": char["status"].get("mod_total", 0),
                    "no_parry": char["status"].get("no_parry", 0),
                }
            else:
                # legacy: calculate from Body Development
                base_hpsp = char["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"]
                dummy["hits"] = base_hpsp
                dummy["max_hits"] = base_hpsp
                dummy["PP"] = char["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"]
                dummy["PPmax"] = dummy["PP"]
                dummy["status"] = {
                    "stunned": 0,
                    "ooo": 0,
                    "bleed": 0,
                    "mod_total": 0,
                    "no_parry": 0,
                }
            dummy["OB melee"] = []
            dummy["OB missile"] = []
            dummy["OB magic"] = []
            dummy["spell"] = []
            dummy["weapon type"] = [[], []]
            logger.debug(f"combat concerned parameters initialized for {dummy['name']}")

            for m in melee:

                for skill in char["cat"][m]["Skill"].keys():

                    # if skill not in ["Progression", "Stats"] and "+" not in skill:
                    if skill not in ["Progression", "Stats"]:
                        addon = [skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"]

                        if addon not in dummy["OB melee"]:
                            dummy["OB melee"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"])

            logger.info(f"{dummy['name']}'s melee OBs collected")

            # sort melee weapons highest ob first
            dummy["OB melee"] = sorted(dummy["OB melee"], key = lambda k: k[1], reverse = True)
            logger.debug(f"{dummy['OB melee']}")
            logger.info(f"{dummy['name']}'s melee OBs sorted")

            for m in missile:

                for skill in char["cat"][m]["Skill"].keys():

                    if skill not in ["Progression", "Stats"] and [skill, char["cat"][m]["Skill"][skill]["total bonus"]] not in dummy["OB missile"]:
                        dummy["OB missile"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"]])

            logger.info(f"{dummy['name']}'s missile OBs collected.")
            # sort missile weapons highest ob first
            dummy["OB missile"] = sorted(dummy["OB missile"], key = lambda k: k[1], reverse = True)
            dummy["weapon type"][0] = ["normal"] * len(dummy["OB melee"])
            dummy["weapon type"][1] = ["normal"] * len(dummy["OB missile"])
            logger.debug(f"{dummy['OB missile']}")
            logger.info(f"{dummy['name']}'s missile OBs sorted.")

            for m in magic:

                for skill in char["cat"][m]["Skill"].keys():

                    if skill not in ["Progression", "Stats"]:
                        addon = [skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"]

                        if addon not in dummy["OB magic"]:
                            dummy["OB magic"].append([skill, char["cat"][m]["Skill"][skill]["total bonus"], "H"])

            logger.info(f"{dummy['name']}'s magic OBs collected.")
            # sort magic attacks' highest ob first
            dummy["OB magic"] = sorted(dummy["OB magic"], key = lambda k: k[1], reverse = True)
            logger.debug(f"{dummy['OB magic']}")
            logger.info(f"{dummy['name']}'s magic OBs sorted")

            self.partygrp.append(dummy)
            logger.info(f"{dummy['name']} added to party.")
            # logger.debug(f"{json.dumps(dummy,indent=4)}")
            self.__chgImg(attackerpic = self.partygrp[0]["piclink"], defenderpic = "")

        self.partygrp = createCombatList(self.partygrp)
        logger.info(f"combatant list created from party group.")
        logger.info(f"partygrp length {len(self.partygrp)} ")
        logger.debug(f"partygrp: \n{format(self.partygrp)}")
        self.initlist += self.partygrp
        logger.info("added partygrp to initlist")
        logger.info(f"length initlist {len(self.initlist)} ")
        logger.debug(f"partygrp: \n{format(self.partygrp)}")
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

        ----
        @todo magical and elemental attacks have to be added.
        '''
        logger.info("start preparing internal weapon list.")

        # self.weaponindex = {"melee":[],
        #                   "missile":[],
        #                   "magic":[]}
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

        # sort weaponlist
        # self.weaponlist = sorted(self.weaponlist, key = lambda d: d['shortc'])
        self.weaponlist = self.sortList(self.weaponlist, "shortc")
        logger.debug(f"weaponlist: \n {self.weaponlist}")
        self.weaponslisted = []

        for elem in self.weaponlist:

            if type(elem["item"]) == type(""):
                self.weaponslisted.append(elem["item"])

            else:
                self.weaponslisted.append(str(elem["item"]).strip("[]").replace("'", ""))


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

            if self.initlist[i]["status"]["stunned"] > 0:
                self.initlist[i]["init"] -= 25

            #----- TODO: think about filter out killed & unconcious combatants right here
            if self.initlist[i] not in cleaner:
                cleaner.append(self.initlist[i])
                logger.debug(f"Initiative for {self.initlist[i]['name']}: {self.initlist[i]['init']}")

        self.initlist = deepcopy(cleaner)
        # sort self.initlist reversely
        self.initlist = sorted(self.initlist, key = lambda k: k["init"], reverse = True)

        self.attackers = []
        self.defenders = []

        for elem in self.initlist:

            #----- think over
            if elem["status"]["hits"] > 0 and elem["status"]["ooo"] == 0 and \
            elem["status"]["die"] != 0 and elem["status"]["parry"] == 0 and \
            elem["status"]["no_parry"] == 0 and elem["status"]["stunned"] == 0:

                if elem["name"] not in self.attackers:
                    self.attackers.append(elem["name"])

            self.defenders.append(elem["name"])

        # self.defenders = deepcopy(self.initlist)
        self.combatround += 1
        self.cbround.set(f"Round \n{self.combatround}")
        self.initroll = True
        self.__updDefCombo(None)
        self.__updtAttckCombo(None)


    def __resetCounter(self, event = None):
        self.combatround = 0
        self.cbround.set("Round \n0")


    def __rollAttack(self):
        '''!
        This does an attack role using RM rules
        '''
        result, self.umr = Dice(rules = "RM")
        self.__atroll.set(result[0])
        self.checkFumble(rollresult = result[0], fumbletype = "weapon")


    def resultMethod(self, data = 10):
        self.fumbleroll = int(data)
        obtype = self.__selectType.get()

        if obtype != "magic":
            self.fumbleresult = self.weaponfumble.getResult(fumbletype = self.fumbletype, roll = self.fumbleroll)

        else:
            self.fumbleresult = self.magicfumble.getResult(fumbletype = self.fumbletype, roll = self.fumbleroll)

        self.__displayCrit.delete("1.0", "end")
        self.__displayCrit.insert(END, "FUMBLE: " + self.fumbleresult)


    def checkFumble(self, rollresult = 5, fumbletype = "one-Handed arms"):
        """!
        This checks whether the result of an unmodified roll was a fumble

        @param rollresult result of dice roll to check for fumble
        @param fumbletype type of fumble: weapon, magic
        """
        logger.debug(f"roll: {rollresult}  fumble type: {fumbletype}")
        self.fumblestat = False

        if rollresult <= self.maxfumble:
            self.fumblestat = True
            testRollWindow(rootwin = self, lang = self.lang, resultwidget = self.resultMethod)


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
        - weapon breakage

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
            self.picattacker = Image.open(attackerpic).resize((110, 110), Image.Resampling.LANCZOS)
            self.picattacker = ImageTk.PhotoImage(self.picattacker)
            self.atcanvas.create_image((110, 110), image = self.picattacker, anchor = "se")
        if defenderpic:
            from PIL import Image, ImageTk
            self.picdefender = Image.open(defenderpic).resize((110, 110), Image.Resampling.LANCZOS)
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
        @todo if a spell level for attack spells may be added it should be subtraced
        from the "ammo" of magic attacks (instead of 1)
        '''
        self.curr_defender = self.__selectDefender.get()
        self.curr_attacker = self.__selectAttacker.get()
        pos = self.__findCombatant(name = self.curr_defender, chklist = self.initlist, result = "index")
        posa = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist, result = "index")
        crit = self.__critType.get()
        attacktype = self.__selectType.get()
        attackskill = self.__selectOB.get()
        self.initlist[pos]["status"]["hits"] -= self.hits

        # ## DEBUG
        # print(f"DEBUG: attackskill: {attackskill}")
        if attackskill not in self.initlist[posa]["ammo"].keys():
            self.initlist[posa]["ammo"][attackskill] = 0

        if attacktype in ["missile", "magic"] and self.initlist[posa]["ammo"][attackskill] > 0:
            self.initlist[posa]["ammo"][attackskill] -= 1

            if attacktype == "magic":
                self.initlist[posa]["status"]["PP"] -= 1

        if crit in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J" "T"]:
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
        '''
        for attacker in self.attackers:
            at = self.__findCombatant(name = attacker, chklist = self.initlist)

            if int(at["status"]["hits"]) < 1 or int(at["status"]["die"]) == 0 or \
            int(at["status"]["no_parry"]) or int(at["status"]["parry"]) or \
            int(at["status"]["ooo"]) or int(at["status"]["stunned"]):
                self.attackers.remove(attacker)

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

            if len(ob) > 2:
                self.__maxlvl.set(ob[2])

        self.__lvlAttacker.set(f"Lvl: {at['lvl']}")
        self.__curHPAttacker.set(f"HP: {at['status']['hits']}/{at['hits']}")
        self.__initAttacker.set(f"Init: {at['init']}")

        if "PP" in at["status"].keys() and "PP" in at.keys():
            self.__ppAttacker.set(f"PP: {at['status']['PP']}/{at['PP']}")

        else:
            self.__ppAttacker.set("PP: 0/0")

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
            self.curr_defender = self.defenders[0]
            self.__selectDefender.set(self.defenders[0])

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

        if "PP" in defend["status"].keys() and "PP" in defend.keys():
            self.__ppDefender.set(f"PP: {defend['status']['PP']}/{defend['PP']}")

        else:
            self.__ppDefender.set(f"PP: 0/0")

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
        rm = []
        self.__healingpoints.set(0)
        self.__modstun = 0

        for i in range(0, len(self.initlist)):
            # bleeding
            self.initlist[i]["status"]["hits"] += self.initlist[i]["status"]["hits/rnd"]

            # status check
            for stat in ["parry", "no_parry", "ooo", "die", "stunned"]:

                if  self.initlist[i]["status"][stat] > 0:
                    self.initlist[i]["status"][stat] -= 1

            # mod check: remove modification after their rounds become 0
            rm_mod = []

            for j in range(0, len(self.initlist[i]["status"]["mod"])):
                self.initlist[i]["status"]["mod"][j]["rnd"] -= 1

                if "mod" in self.initlist[i]["status"]["mod"][j].keys():

                    if self.initlist[i]["status"]["mod"][j]["mod"] == 0 or self.initlist[i]["status"]["mod"][j]["rnd"] <= 0:
                        rm_mod.append(j)

                else:

                    if self.initlist[i]["status"]["mod"][j]["mod_attacker"] == 0 or self.initlist[i]["status"]["mod"][j]["rnd"] <= 0:
                        rm_mod.append(j)

            # select killed combatants
            # if "player" not in self.initlist[i].keys() and (self.initlist[i]["status"]["hits"] < 1 or self.initlist[i]["status"]["die"] == 0):
            if (self.initlist[i]["status"]["hits"] < 1 or self.initlist[i]["status"]["die"] == 0):
                rm.append(self.initlist[i]["name"])

        # remove killed NSCs/Monster/Characters
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

            print(f"1207 Debug: {self.__oblist}")
            self.__ammo.set("n/a")

        elif selected == attacktypes[self.lang][1]:

            for mob in at["OB missile"]:
                self.__oblist.append(mob[0])

                if at["ammo"] == {}:

                    if mob[0] in at["ammo"].keys():
                        self.__ammo.set(str(at["ammo"][mob[0]]))

                else:
                    # at["ammo"][mob[0]] = 0
                    self.__ammo.set(str(0))

        elif selected == attacktypes[self.lang][2]:

            if at["OB magic"]:

                for mob in at["OB magic"]:
                    self.__oblist.append(mob[0])

                    if at["ammo"]:

                        if mob[0] not in at["ammo"].keys():
                            at["ammo"][mob[0]] = at["status"]["PP"]
                    else:
                        at["ammo"][mob[0]] = at["status"]["PP"]

            self.__ammo.set(str(at["status"]["PP"]))

        self.__selectOB.set(self.__oblist[0])
        self.__obCombo.config(values = self.__oblist)
        self.__updOB(event = None)


    def determineWeapon(self):
        """!
        This determines the used weapon of the attacker of if a spell is used.

        ----
        @todo the following has to be implemented:
        - breakage and strength for weapons

        """
        self.distance = {"near": [3, 0],
                        "short": [4, -1000],
                        "medium": [5, -1000],
                        "long": [6, -1000],
                        "extreme":[7, -1000],
                        "very extreme":[8, -1000]
                        }
        translation = {"1he": "one-handed arms",
                      "1hc": "one-handed arms",
                      "2h": "two-handed arms",
                      "mis": "missile weapons",
                      "pa": "polearms and spears",
                      "th": "thrown arms",
                      "melee": "animal"
                      }
        selectedOB = self.__selectOB.get()
        logger.debug(f"selectedOB: {selectedOB}")
        attype = self.__selectType.get()

        if selectedOB in self.weaponslisted:
            logger.debug(f"{selectedOB} found in weaponlist")
            index = self.weaponslisted.index(selectedOB)
            weapon = self.weaponlist[index]

            if type(weapon["wtype"]) == type(""):
                self.fumbletype = translation[weapon["wtype"]]
                self.maxfumble = int(weapon["fumble"])

            else:
                attype = self.__selectType.get()

                if attype == "magic":
                    self.fumbletype = "force"
                    self.maxfumble = 4

                elif attype == "missile":
                    self.fumbletype = translation[weapon["wtype"][1]]
                    self.maxfumble = int(weapon["fumble"])

                else:
                    self.fumbletype = translation[weapon["wtype"][0]]
                    self.maxfumble = int(weapon["fumble"])

            logger.debug(f"set fumbletype: {self.fumbletype}")
            logger.debug(f"set maxfumble; {self.maxfumble}")
            self.ftype.set(self.fumbletype)
            # self.maxfumble = int(weapon["fumble"])
            lastdist = 3

            #------- determining the distance modifiers for ranged combat

            if attype == "magic":
                self.distance = {"near": [3, 35],
                                "short": [15, 0],
                                "medium": [30, -25],
                                "long": [60, -40],
                                "extreme":[90, -55],
                                "very extreme":[200, -75]
                                }

                self.fumbletype = "force"
                self.ftype.set(self.fumbletype)
                logger.debug(f"set fumbletype: {self.fumbletype}")
                logger.debug(f"set maxfumble; {self.maxfumble}")

            elif attype == "missile":

                for dist in ["near", "short", "medium", "long", "extreme"]:

                    if weapon[dist] == None:

                        if dist == "near":
                            self.distance[dist] = [3, 0]
                            lastdist += 1
                        else:
                            self.distance[dist] = [lastdist, -1000]
                            lastdist += 1

                    else:
                        lastdist = int(weapon[dist][0])
                        mod = int(weapon[dist][1])
                        self.distance[dist] = [lastdist, mod]

            logger.debug(f"distance mods set to:\n{json.dumps(self.distance)}")


    def getFumbleType(self):
        """!
        The determines the fumble type by the selected Attack type and skill.

        ----
        @todo has to be fully implemented
        - mounted combat is missing
        - spell combat / attacks & crits have to be implemented
        - magic combat fumble
        """
        self.fumbletype = self.ftype.get()
        self.fumblerange = 4
        obtype = self.__selectType.get()
        selectedOB = self.__selectOB.get()
        selectedOB.replace("_", " ")
        print(f"1356 DEBUG(getFumbleType): {selectedOB}")

        if obtype == "missile":

            if "bow" in selectedOB.lower() or "missile" in selectedOB.lower():
                self.fumbletype = "missile weapons"
                self.fumblerange = 5

            else:
                self.fumbletype = "thrown arms"
                self.fumblerange = 5

        elif obtype == "melee":

            if "striking" in selectedOB.lower() or "tackling" in selectedOB.lower() \
             or "boxing" in selectedOB.lower():
                self.fumbletype = "MA strikes"
                self.fumblerange = 2

            elif "sweeps" in selectedOB.lower() or "blocking" in selectedOB.lower() \
             or "wrestling" in selectedOB.lower():
                self.fumbletype = "MA sweeps"
                self.fumblerange = 2

            elif "1-H" in selectedOB:
                self.fumbletype = "one-handed arms"
                self.fumblerange = 4

            elif "2-H" in selectedOB:
                self.fumbletype = "two-handed arms"
                self.fumblerange = 5

            elif "brawling" in selectedOB.lower():
                self.fumbletype = "brawling"
                self.fumblerange = 2

            elif "pole" in selectedOB.lower() and "+" in selectedOB:
                self.fumbletype = "polearms and spears"
                self.fumblerange = 5

        elif obtype == "magic":
            self.fumbletype = "force"
            #----- TODO: magic fumble range has to be corrected by the entry in
            # the connected attack table XXXXXXXXXXXX
            self.fumblerange = 2

        self.determineWeapon()
        self.ftype.set(self.fumbletype)


    def __updOB(self, event = None):
        '''!
        This updates the attack credentials by the selected attack skills
        ---
        @todo add more logging and debuging
        '''
        self.getFumbleType()
        self.updateRange()
        self.curr_attacker = self.__selectAttacker.get()
        at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)
        self.curr_defender = self.__selectDefender.get()
        defend = self.__findCombatant(name = self.curr_defender, chklist = self.initlist)
        obtype = self.__selectType.get()
        selectedOB = self.__selectOB.get()
        index = self.__oblist.index(selectedOB)

        if obtype == attacktypes[self.lang][0]:
            self.__skill.set(at["OB melee"][index][1])

            if "DB" in defend.keys():
                self.__DB.set(int(defend["DB"]))
                logger.debug(f"DB set to {defend['DB']}")

            else:
                self.__DB.set(0)
                logger.debug("DB set to 0")

        elif obtype == attacktypes[self.lang][1]:

            if len(at["OB missile"][index]) > 1:
                self.__skill.set(at["OB missile"][index][1])
                skillname = at["OB missile"][index][0]

                if skillname in at["ammo"].keys():
                    self.__ammo.set(str(at["ammo"][skillname]))
                    logger.debug(f"ammo: {at['ammo'][skillname]}")

                else:
                    self.__ammo.set("0")
                    at["ammo"][index] = 0
                    logger.debug("ammo: empty / not available")
            else:
                self.__skill.set(at["OB missile"][index][0])

            if "DBm" in defend.keys():
                self.__DB.set(int(defend["DBm"]))
                logger.debug(f"DB set to {defend['DBm']}")

            else:
                self.__DB.set(0)
                logger.debug("DB set to 0")

        elif obtype == attacktypes[self.lang][2]:
            if len(at["OB magic"][index]) > 1:
                self.__skill.set(at["OB magic"][index][1])

        if selectedOB.replace(" ", "_") in self.atlist:
            self.__selectAT.set(selectedOB.replace(" ", "_"))

        else:
            self.__selectAT.set(self.__determineAT(selectedOB))

        if defend["status"]["no_parry"] > 0 or defend["status"]["ooo"] > 0:
            self.__DB.set(0)
            logger.debug("DB set to 0 (no parry)")

        if defend["status"]["stunned"] > 0:
            db = self.__DB.get()

            if db < 25:
                self.__DB.set(0)
                logger.debug("DB set to 0 (stunned)")

            else:
                self.__DB.set(db - 25)
                logger.debug("reduced DB set to {db-25} (stunned)")

        self.__calcMod(event = None)


    def __determineAT(self, obname = ""):
        """!
        This method delivers the fitting Attack Table to weapons which have not their own.

        """
        result = "Brawling"

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


    def __applyHealingOthers(self, event = None):
        """!
        This method applies healing to the combatant

        @param event UI event given but not used
        """
        self.curr_defender = self.__selectDefender.get()
        at = self.__findCombatant(name = self.curr_defender, chklist = self.initlist, result = "index")
        key = self.__selectHeal.get()
        value = self.__healingpoints.get()
        self.initlist[at]["status"][key] += value
        # self.__updtAttckCombo(event = None)
        self.__updDefCombo(event = None)


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
        # # @var self.__typeCombo
        # This Combobox gives a selection of which type of attack is chosen:
        # - melee
        # - missile
        # - magic
        self.__typeCombo = Combobox(self.window,
                                    textvariable = self.__selectType,
                                    values = attacktypes[self.lang])
        self.__typeCombo.bind("<<ComboboxSelected>>", self.__getAttackType)
        self.__typeCombo.grid(row = 2, column = 1, sticky = W)

        Label(self.window,
              text = f'{labels["ammo"][self.lang]}:',
              ).grid(row = 2, column = 2, sticky = W)

        self.__ammo = StringVar()
        self.__ammo.set("n/a")
        self.__ammoEntry = Entry(self.window,
                                textvariable = self.__ammo,
                                justify = "center",
                                width = 5
                                )
        self.__ammoEntry.grid(row = 2, column = 3, sticky = "EW")
        self.__ammoEntry.bind("<Return>", self.setAmmo)
        self.__ammoEntry.bind("<<FocusOut>>", self.setAmmo)

        #---------- row 3

        self.__selectOB = StringVar()
        self.__selectOB.set("Battle Axe")
        # # @var self.__obCombo
        # This Combobox gives a selection of  offensive bonus/skill
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

        self.healings = ["hits", "hits/rnd", "stunned", "no parry" , "ooo", "mod_total", "die"]
        self.__selectHeal = StringVar()
        self.__selectHeal.set(self.healings[1])
        # # @var self.__healCombo
        # This Combobox gives a selection of  different type of healings during the battle
        self.__healCombo = Combobox(self.window,
                                   textvariable = self.__selectHeal,
                                   values = self.healings)
        # self.__healCombo.bind("<<ComboboxSelected>>",self.__applyHealing)
        self.__healCombo.grid(row = 5, column = 1, sticky = W)

        self.__healingpoints = IntVar()
        self.__healingpoints.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__healingpoints,
              width = 5
              ).grid(row = 5, column = 2, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__applyHealing
               ).grid(column = 3, row = 5, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_heal"][self.lang],
               command = self.__applyHealingOthers
               ).grid(column = 4, row = 5, sticky = "EW")

        #------------ row 6

        self.__selectAttacker = StringVar()
        self.__selectAttacker.set("Egon")
        # # @var self.__attackCombo
        # This Combobox gives a selection of attackers during the battle
        self.__attackCombo = Combobox(self.window,
                                      textvariable = self.__selectAttacker,
                                      values = self.attackers)
        self.__attackCombo.bind("<<ComboboxSelected>>", self.__updtAttckCombo)
        self.__attackCombo.grid(column = 0, row = 6, sticky = "W")

        self.ftype = StringVar()
        self.ftype.set("one handed arms")
        Label(self.window,
              textvariable = self.ftype,
              justify = "center",
              borderwidth = 2,
              relief = "sunken"
              ).grid(column = 1, row = 6, sticky = "EW")

        self.__atdistance = IntVar()
        self.__atdistance.set(0)
        self.__EntryDistance = Entry(self.window,
                                     textvariable = self.__atdistance,
                                     justify = "center",
                                     width = 5
                                     )
        self.__EntryDistance.grid(column = 2, row = 6, sticky = "EW")
        self.__EntryDistance.bind("<FocusOut>", self.updateRange)
        self.__EntryDistance.bind("<Return>", self.updateRange)
        Label(self.window,
              text = "m  -->",
              justify = "left"
              ).grid(column = 3, row = 6, sticky = "EW")

        self.__range = StringVar()
        self.__range.set("near")
        Label(self.window,
              textvariable = self.__range,
              justify = "left",
              borderwidth = 2,
              relief = "sunken"
              ).grid(column = 4, row = 6, sticky = "EW")

        self.__rangemod = IntVar()
        self.__rangemod.set(0)
        Label(self.window,
              textvariable = self.__rangemod,
              justify = "center"
              ).grid(column = 5, row = 6, sticky = "EW")
        #------------------- Defender ------------------------------------------

        self.__selectDefender = StringVar()
        self.__selectDefender.set("Anton")
        # # @var self.__defendCombo
        # This Combobox gives a selection of defenders during the battle
        self.__defendCombo = Combobox(self.window,
                                      textvariable = self.__selectDefender,
                                      values = self.defenders)
        self.__defendCombo.bind("<<ComboboxSelected>>", self.__updDefCombo)
        self.__defendCombo.grid(column = 6, row = 6, sticky = "EW")

        #---------- row 7
        #------------------- Attacker ------------------------------------------
        Button(self.window,
               text = txtbutton["but_nxtrd"][self.lang],
               command = self.__nextRnd
               ).grid(column = 0, row = 7, rowspan = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_next_at"][self.lang],
               command = self.__nextAttacker
               ).grid(column = 1, row = 7, rowspan = 3, sticky = "EW")

        self.cbround = StringVar()
        self.cbround.set("Round: \n0")
        Label(self.window,
              textvariable = self.cbround,
              justify = "center",
              borderwidth = 2,
              relief = "sunken",
              font = ("Helvetica", 16, "bold")
              ).grid(column = 2, columnspan = 2, row = 7, rowspan = 3, sticky = "NEWS")

        Button(self.window,
               text = txtbutton["but_reset"][self.lang] + "\n<--",
               command = self.__resetCounter
               ).grid(column = 4, row = 7, rowspan = 3, sticky = "EW")
        #------------ row 8

        #------------ row 9

        #------------ row 10

        Label(self.window,
              text = labels["attack table"][self.lang] + ":",
              ).grid(column = 0, row = 10, sticky = "W")

        # # @var self.atlist
        # List of names of Attack Tables
        self.atlist = list(self.attacktbls.keys())
        self.atlist.sort()
        self.__selectAT = StringVar()
        self.__selectAT.set(self.atlist[0])
        # # @var self.__ATOptCombo
        # This Combobox gives a selection of Attack Tables (weapons etc)
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
        # # @var self.__maxOpt
        # This Combobox gives a selection of the maximum level of an attack
        self.__maxOpt = Combobox(self.window,
                                 values = ["S", "M", "L", "H"],
                                 textvariable = self.__maxlvl,
                                 width = 3)

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


    def setAmmo(self, event = None):
        """!
        This sets the ammo of a distance weapons
        """
        # set ammo count for current attacker for current distance weapon
        if self.__selectType.get() in ["missile", "magic"]:
            self.curr_attacker = self.__selectAttacker.get()
            pos = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist, result = "index")
            newammo = int(self.__ammo.get())
            skill = self.__selectOB.get()
            self.initlist[pos]["ammo"][skill] = newammo
            logger.debug(f"For {self.curr_attacker} set ammo[{skill}] to {newammo}")


    def updateRange(self, event = None):
        """!
        This updates Range and RangeMod after entering the combat distance"""
        currdist = self.__atdistance.get()
        self.getFumbleType()

        for range in ["near", "short", "medium", "long", "extreme"]:

            if currdist <= self.distance[range][0]:
                self.__range.set(range)
                self.__rangemod.set(self.distance[range][1])
                break

            else:
                self.__range.set("n/a")
                self.__rangemod.set(-1000)


    def __nextAttacker(self, event = None):
        """!Gets the next attacker if any from the init list (on button click)"""
        self.__updtAttckCombo()
        self.curr_attacker = self.__selectAttacker.get()
        logger.debug(f"current Attacker: {self.curr_attacker}")

        if self.curr_attacker in self.__attackCombo["values"]:
            self.__pos = self.__attackCombo["values"].index(self.curr_attacker)

        while self.__pos < len(self.__attackCombo["values"]) - 1:
            at = self.__findCombatant(name = self.curr_attacker, chklist = self.initlist)
            print(f"DEBUG: {json.dumps(at,indent=4)}")

            if int(at["status"]["hits"]) < 1 or int(at["status"]["die"]) == 0 or \
            int(at["status"]["no_parry"]) > 0 or int(at["status"]["parry"]) > 0 or \
            int(at["status"]["ooo"]) > 0 or int(at["status"]["stunned"]) > 0:
                self.__pos += 1
                print(f"DEBUG: found {at['name']}")

            else:
                self.__pos += 1

                self.__selectAttacker.set(self.__attackCombo["values"][self.__pos])
                self.__updtAttckCombo()
                break


    def checkAttack(self):
        """!
        This checks the result of a roll against an attack table


        ----
        @todo
        The attack checker for magic ball spell attacks has to  be implemented
        """
        self.checkFumble(rollresult = self.__atroll.get(), fumbletype = "weapon")

        if not self.fumblestat:

            if self.umr == 100 or self.__atroll.get() == 100:
                umroll = 100

            else:
                umroll = self.umr

            if self.__selectType.get() == "melee":

                self.attacktbls[self.__selectAT.get()].getHits(self.__skill.get() + self.__atroll.get() - self.__DB.get(),
                                                               self.__AT.get(),
                                                               self.__maxlvl.get(),
                                                               UM = umroll
                                                               )
            elif self.__selectType.get() == "missile":
                self.attacktbls[self.__selectAT.get()].getHits(self.__skill.get() + self.__atroll.get() + self.__rangemod.get() - self.__DB.get(),
                                                               self.__AT.get(),
                                                               self.__maxlvl.get(),
                                                               UM = umroll
                                                               )
            elif self.__selectType.get() == "magic":
                self.attacktbls[self.__selectAT.get()].getHits(self.__skill.get() + self.__atroll.get() + self.__rangemod.get() - self.__DB.get(),
                                                               self.__AT.get(),
                                                               self.__maxlvl.get(),
                                                               UM = umroll
                                                               )
                self.maxfumble = self.attacktbls[self.__selectAT.get()].fumble
                self.checkFumble(rollresult = self.__atroll.get(), fumbletype = "magic")
                #----- TODO: the directed spell skill selection and the determination of AT result
                # has to be implemented
                # pass

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
        @todo
        -# handling of Crits higher than E with a loop on the crit table; output of all the text & results as sum

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
                # self.hits +=self.crittbls[self.__selectCrit.get()].crithit["hits"]
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


    def __setBGColor(self, attrib, bgcolor = "green", fgcolor = "black"):
        """!
        This sets the backgroun colors for label widgets
        @param attrib tkinter label object
        @param bgcolor background color to set
        @param fgcolor foreground (text) color to set
        """
        attrib.config(bg = bgcolor, fg = fgcolor)


    def checkPhysicalCond(self, combatant, side = "defender"):
        """!
        This method checks the physical condition of an attacked combatant and defines
        a background color code for that condition.

        @param combatant PC / NPC to check the physical condition for
        @param side of the combatant: attacker, defender

        ----
        @todo the long if-statements in this method have to be re-factored.
        """
        # # @var condition_color
        # this holds the physical condition as index and the resulting color as value.
        condition_color = {"die": "black",
                           "die_fg": "white",
                           "dead": "black",
                           "dead_fg": "white",
                           "ooo": "grey",
                           "ooo_fg": "black",
                           "no parry": "red",
                           "no parry_fg": "whitesmoke",
                           "parry": "deepskyblue",
                           "parry_fg": "black",
                           "critical": "darkred",
                           "critical_fg": "yellow",
                           "bad": "darkorange",
                           "bad_fg": "black",
                           "not so good":"yellow",
                           "not so good_fg": "black",
                           "good": "lime",
                           "good_fg": "black",
                           "stunned": "sandybrown",
                           "stunned_fg": "black",
                           "light bleeding": "khaki",
                           "light bleeding_fg": "black",
                           "medium bleeding": "orange",
                           "medium bleeding_fg": "black",
                           "strong bleeding":"firebrick",
                           "strong bleeding_fg": "yellow",
                           "no mod": "whitesmoke",
                           "no mod_fg": "black",
                           "no stun": "whitesmoke",
                           "no stun_fg": "black",
                           "no bleed": "whitesmoke",
                           "no bleed_fg": "black",
                           "no bleeding":"whitesmoke",
                           "no bleeding_fg": "black",
                           "nono parry":"whitesmoke",
                           "nono parry_fg": "black",
                           "attack again": "whitesmoke",
                           "attack again_fg": "black",
                           "awake":"whitesmoke",
                           "awake_fg": "black",
                           "low mod":"lightgreen",
                           "low mod_fg": "black",
                           "medium mod":"gold",
                           "medium mod_fg": "black",
                           "high mod": "coral",
                           "high mod_fg": "black",
                           "critical mod":"orangered",
                           "critical mod_fg": "black"
                          }

        # # @var condition_color
        # this variable holds the color name which shall be finally set when the physical
        # condition is determined.
        condbgcolor = condition_color["good"]
        # # @var txtcolor
        # this hold the  text color to keep all readable.
        txtcolor = "black"

        logger.debug(f"check data: \n{json.dumps(combatant,indent=4)}")
        # # @var hits
        # this holds the remaining hit points in pecent
        hits = combatant['status']["hits"] / int(combatant["hits"]) * 100

        if combatant["status"]["mod_total"] < -50:
            condbgcolor = condition_color["critical mod"]
            txtcolor = condition_color["critical mod_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBmod_totalGColor(attrib = self.mod_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif combatant["status"]["mod_total"] < -20:
            condbgcolor = condition_color["high mod"]
            txtcolor = condition_color["high mod_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif combatant["status"]["mod_total"] < -9:
            condbgcolor = condition_color["medium mod"]
            txtcolor = condition_color["medium mod_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif combatant["status"]["mod_total"] < 0:
            condbgcolor = condition_color["low mod"]
            txtcolor = condition_color["low mod_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        else:
            condbgcolor = condition_color["no mod"]
            txtcolor = condition_color["no mod_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.mod_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.mod_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        if combatant["status"]["hits/rnd"] < 0:
            condbgcolor = condition_color["light bleeding"]
            txtcolor = condition_color["light bleeding_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.bleed_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.bleed_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif combatant["status"]["hits/rnd"] < -2:
            condbgcolor = condition_color["medium bleeding"]
            txtcolor = condition_color["medium bleeding_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.bleed_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.bleed_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif combatant["status"]["hits/rnd"] < -6:
            condbgcolor = condition_color["strong bleeding"]
            txtcolor = condition_color["strong bleeding_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.bleed_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.bleed_at, bgcolor = condbgcolor, fgcolor = txtcolor)
        else:
            condbgcolor = condition_color["no bleeding"]
            txtcolor = condition_color["no bleeding_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.bleed_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.bleed_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        if combatant["status"]["stunned"] > 0:
            condbgcolor = condition_color["stunned"]
            txtcolor = condition_color["stunned_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.stunned_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.stunned_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        else:
            condbgcolor = condition_color["no stun"]
            txtcolor = condition_color["no stun_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.stunned_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.stunned_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        if combatant["status"]["no_parry"] > 0:
            condbgcolor = condition_color["no parry"]
            txtcolor = condition_color["no parry_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.noparry_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.noparry_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        else:
            condbgcolor = condition_color["nono parry"]
            txtcolor = condition_color["nono parry_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.noparry_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.noparry_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        if combatant["status"]["ooo"] > 0:
            condbgcolor = condition_color["ooo"]
            txtcolor = condition_color["ooo_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.ooo_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.ooo_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        else:
            condbgcolor = condition_color["awake"]
            txtcolor = condition_color["awake_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.ooo_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.ooo_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        if combatant["status"]["parry"] > 0:
            condbgcolor = condition_color["parry"]
            txtcolor = condition_color["parry_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.parry_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.parry_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        else:
            condbgcolor = condition_color["attack again"]
            txtcolor = condition_color["attack again_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.parry_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.parry_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        if hits == 0.0:
            condbgcolor = condition_color["dead"]
            txtcolor = condition_color["dead_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif hits < 10.0:
            condbgcolor = condition_color["critical"]
            txtcolor = condition_color["critical_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.hits_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif hits < 25.0:
            condbgcolor = condition_color["bad"]
            txtcolor = condition_color["bad_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.hits_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif hits < 76.0:
            condbgcolor = condition_color["not so good"]
            txtcolor = condition_color["not so good_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.hits_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        elif hits > 75.0:
            condbgcolor = condition_color["good"]
            txtcolor = condition_color["good_fg"]

            if side == "defender":
                self.__setBGColor(attrib = self.hits_def, bgcolor = condbgcolor, fgcolor = txtcolor)

            elif side == "attacker":
                self.__setBGColor(attrib = self.hits_at, bgcolor = condbgcolor, fgcolor = txtcolor)

        if combatant["status"]["die"] >= 0:
            condbgcolor = condition_color["die"]
            txtcolor = condition_color["die_fg"]

        if side == "defender":
            self.defcanvas.config(bg = condbgcolor)

        elif side == "attacker":
            self.atcanvas.config(bg = condbgcolor)


class enemySelector(blankWindow):
    '''
    This class opens a window to select different monsters or npcs from a data
    file (CSV). This selection
    '''


    def __init__(self, lang = "en", datapool = ""):
        '''
        @param lang chosen display language (default: en; supported; en, de)
        @param datapool (path +) file where the default bestiarium is stored in.
        ----
        '''
        # #\var self.lang
        # display language
        self.lang = lang
        # #\var self.datapool
        # path + file name of the default monster data file.
        self.datapool = datapool
        # #\var self.selection
        # a list of selected monsters/nscs (list of dictionaries)
        self.selection = []
        # # \var self.fmaske
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
        # # \var self.__npcpath
        # path+ file name of selected data file
        self.__npcpath = askopenfilename(filetypes = self.fmaske, defaultextension = "*.csv", initialdir = os.getcwd())
        logger.debug(f"openNPCs: chosen npc/monster group file {self.__npcpath}")

        if self.__npcpath[-4:].lower() == ".csv":
            # #\var self.npcgrp
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



if __name__ == '__main__':
    # Original attackcheck entry point (restored TR-003)
    win = atWin()
    # The Monster Creator windows (showNPCWin, magicSelectorWin, showCPWin,
    # monstercreatorWin) are still importable from this module for the
    # src/monstercreator.py launcher — see TR-004 decision: kept here.

