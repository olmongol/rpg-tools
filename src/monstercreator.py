#!/usr/bin/env python
'''!
\file monstercreator.py
\package monstercreator
\brief Tool for creating Monsters, NPCs etc.

This module creates windows for entering and editing beasts & NPCs for the GM's
master DB where creatures can be chosen from for individual campaigns.

\date (c) 2022
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.2
'''
__version__ = "0.2"
__updated__ = "06.12.2023"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__me__ = "RM RPG Tools: nsc/monster creator module"

from copy import deepcopy
from glob import glob
from tkinter import filedialog
from tkinter.ttk import *
import csv
import json
import os
import shutil

from PIL import Image, ImageTk

from gui.window import *
from rpgToolDefinitions.magic import magicpath
from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import *
from rpgtoolbox.globaltools import *
from rpgtoolbox.handlemagic import getSpellNames

mycnf = chkCfg()
logger = log.createLogger('Monster', 'debug', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = "monstercreator.log")



class monstercreatorWin(blankWindow):
    """!
    This class generates a GUI to enter NSCs, monsters etc.

    ----
    @todo The following has to be implemented:
    - speed
    - weaknesses edit/display
    - immunities edit/display
    - OB magic
    """


    def __init__(self, **kwargs):
        """!Constructor:
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
            self.datapath = self.__config.cnfparam["datapath"] + "default/"

            if self.datapath[0:2] == "./":
                self.datapath = self.__currdir + self.datapath[1:]

            if "nscpath" in self.__config.cnfparam.keys():
                self.nscpath = self.__config.cnfparam["nscpath"]

            else:
                self.nscpath = f"{self.datapath}/nscs/"

            if "nscpicpath" in self.__config.cnfparam.keys():
                self.nscpicpath = self.__config.cnfparam["nscpicpath"]

            else:
                self.nscpicpath = f"{self.datapath}/pics_nsc/"

        else:

            if "lang" in kwargs.keys():
                self.lang = kwargs["lang"]

            else:
                self.lang = "en"

            logger.debug(f"language set to: {self.lang}")

            if "datapath" in kwargs.keys():
                self.datapath = kwargs["datapath"] + "/default/"

            else:
                self.datapath = f"os.getcwd()/data/default/"

            if self.datapath[:2] == "./":
                self.datapath = self.__currdir + self.datapath[1:]

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
        os.chdir(self.nscpath)

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
        '''!
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
        '''!
        This adds an Edit menu to the windows menu bar:

        ----
        @todo has to be implemended fully.
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
                                  command = self.notdoneyet)
        self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_show_NPC"],
                                  command = self.notdoneyet)
        #self.editmenu.add_command(label = submenu["edit"][self.lang]["history"],
        #                          command = self.notdoneyet)
        logger.debug("edit menu build")


    def __quit(self):
        '''!
        This method saves changes and closes the window
        '''
        self.saveGM()

        if self.NPCs != []:
            self.saveCP(filename = self.CPtable)

        self.window.destroy()


    def __buildWin(self):
        """!
        This method builds the window content.
        """

        #------------ row 0

        # @bug Image is part of a different package with different functions
        # that's why here is a re-import.
        from PIL import Image, ImageTk
        self.selectedPic = ImageTk.PhotoImage(Image.open(self.GMcontent[0]["piclink"]).resize((300, 300), Image.ANTIALIAS))
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
        self.__meleeCombo.grid(row = 3, column = 4, sticky = W)

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
        #self.__obSizeCombo.bind("<<ComboboxSelected>>", self.__getOB)
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
        #self.__catCombo.bind("<<ComboboxSelected>>", self.__getOBm)
        self.__missileCombo.grid(row = 4, column = 4, sticky = W)

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

        #self.__selectOBsize = StringVar()
        #self.__selectOBsize.set("M")
        #self.__obSizeCombo = Combobox(self.window,
        #                            textvariable = self.__selectOBsize,
        #                            values = ["T", "S", "M", "L", "H"],
        #                            width = 4)
        #self.__obSizeCombo.bind("<<ComboboxSelected>>", self.__getOB)
        #self.__obSizeCombo.grid(row = 3, column = 7, sticky = "EW")

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
        self.__selectOBmagic.set(self.__magiclist)
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
               ).grid(row = 5, column = 6, columnspan = 2, sticky = "NEW")
        self.__magicstring = StringVar()
        self.__magicstring.set("")
        self.__EntryMagicSting = Entry(self.window,
                                       textvariable = self.__magicstring,
                                       width = 8
                                       )
        self.__EntryMagicSting.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryMagicSting.bind("<Return>", self.updateCurrentSet)
        self.__EntryMagicSting.grid(row = 6, column = 7, columnspan = 2, sticky = "NEW")
        #Button(self.window,
        #       text = txtbutton["but_show_magic"][self.lang],
        #       command = self.__editMagic
        #       ).grid(row = 5, column = 7, columnspan = 2, sticky = "NEW")

        #------- row 7
        vscroll = Scrollbar(self.window, orient = VERTICAL)
        self.__displayComment = Text(self.window,
                                  yscrollcommand = vscroll.set,
                                  height = 7
                                  )
        vscroll.config(command = self.__displayComment.yview)
        self.__displayComment.bind("<FocusOut>", self.updateCurrentSet)
        self.__displayComment.grid(row = 7, rowspan = 4, column = 2, columnspan = 3, sticky = "NEWS")
        self.__insertComment()

        Button(self.window,
               text = txtbutton["but_edit_imune"][self.lang],
               command = self.__editImunities
               ).grid(row = 6, column = 5, columnspan = 2, sticky = "NEW")

        self.__LabelImunities = Label(self.window,
                                      text = self.currDataSet["immune"]
                                      )
        self.__LabelImunities.grid(row = 7, column = 5, rowspan = 4, sticky = "NEWS")

        #------- row 8
        Button(self.window,
               text = txtbutton["but_edit_weak"][self.lang],
               command = self.__editWeaknesses
               ).grid(row = 8, column = 5, columnspan = 2, sticky = "NEW")

        #------- row 9
        self.__LabelWeaknesses = Label(self.window,
                                       text = self.currDataSet["weakness"])
        self.__LabelWeaknesses.grid(row = 9, column = 5, columnspan = 4, sticky = "NEWS")


    def __editImunities(self, event = None):
        """!This opens a window to edit Imunities of NPCs / beasts

        ----
        @todo this has to be fully implemented
        """
        self.notdoneyet("__editImunities")


    def __editWeaknesses(self, event = None):
        """!This opens a window to edit Weaknesses of NPCs / beasts

        ----
        @todo this has to be fully implemented
        """
        self.notdoneyet("__editWeaknesses")


    def __editMagic(self, event = None):
        """!This opens a window to edit magic skills of NPCs / beasts

        ----
        @todo this has to be fully implemented"""
        self.magicWin = magicSelectorWin(rootwin = self, lang = self.lang, datapath = self.datapath, magicstring = self.currDataSet["spells"])


    def __showMagic(self, event = None):
        """!This opens a window to show magic skills of NPCs / beasts

        ----
        @todo this has to be fully implemented"""
        self.notdoneyet("__showMagic")


    def __newElement(self, even = None):
        """!
        This adds a new element to the NPC / Beast list
        """
        if self.__datatemplate not in self.GMcontent:
            self.GMcontent.append(self.__datatemplate)
            logger.debug("appended empty element to NSC / Beast list")
            self.__index = len(self.GMcontent) - 1
            self.currDataSet = deepcopy(self.__datatemplate)
            self.updateWindow()


    def __insertComment(self, event = None):
        """!This puts data into comment text widget"""
        self.__displayComment.delete("1.0", "end")
        self.__displayComment.insert(END, self.currDataSet["comment"])


    def __getComment(self, event = None):
        """!This gets data from comment text widget """
        self.currDataSet["comment"] = self.__displayComment.get("1.0", END)


    def __prevItem(self, event = None):
        """!
        This moves to the previous NSC / beast in the GM master table
        """
        self.updateCurrentSet()

        if self.__index > 0:
            self.__index -= 1
            self.GMcontent[self.__index + 1] = deepcopy(self.currDataSet)
            self.currDataSet = deepcopy(self.GMcontent[self.__index])
            self.updateWindow()


    def __nextItem(self, event = None):
        """!
        This moves to the previous NSC / beast in the GM master table
        """
        self.updateCurrentSet()

        if self.__index < len(self.GMcontent) - 1:
            self.__index += 1
            self.GMcontent[self.__index - 1] = deepcopy(self.currDataSet)
            self.currDataSet = deepcopy(self.GMcontent[self.__index])
            self.updateWindow()


    def updateWindow(self, event = None):
        """!
        This updates all window widgets with data of the current data set
        """
        #------- update pic
        if self.currDataSet["piclink"][:2] == "./":
            self.currDataSet["piclink"] = self.__currdir + self.currDataSet["piclink"][1:]

        elif self.currDataSet["piclink"][0] != "/":
            self.currDataSet["piclink"] = self.__currdir + "/" + self.currDataSet["piclink"][1:]

        from PIL import Image
        self.selectedPic = ImageTk.PhotoImage(Image.open(self.currDataSet["piclink"]).resize((300, 300), Image.ANTIALIAS))
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
        self.__enc.set(self.currDataSet["enc"])
        self.__magicstring.set(self.currDataSet["spells"])
        self.__insertComment()
        self.__LabelImunities.config(text = self.currDataSet['immune'])
        self.__LabelWeaknesses.config(text = self.currDataSet["weakness"])


    def updateCurrentSet(self, event = None):
        """!
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
        self.currDataSet["spells"] = self.__magicstring.get()
        if self.currDataSet["OB missile"] == "":
            self.currDataSet["OB missile"] = "0xx"

        self.currDataSet["enc"] = self.__enc.get()
        print(f'DEBUG: {self.currDataSet["name"]} {self.currDataSet["enc"]}')
        self.__getComment()
        self.GMcontent[self.__index] = deepcopy(self.currDataSet)


    def __getCategory(self, event = None):
        '''!
        This detemines the selected category
        '''
        self.currDataSet["category"] = self.__selectCat.get()

        if self.currDataSet["category"] not in self.NPCcat:
            self.NPCcat.append(self.currDataSet["category"])


    def __getOB(self, event = None):
        """! This determines the selected attack for melee OB string

        ---
        @todo this has to be implemented fully.
        """
        self.currDataSet["OB melee"] = f"{self.__obstring.get()}/{self.__obval.get()} {self.__selectOBsize.get()} {self.__attacks[self.__selectOB.get()]}"
        self.updateWindow()


    def __getOBm (self, event = None):
        """! This determines the selected attack for missile OB string

        ---
        @todo this has to be implemented fully.
        """
        #self.updateCurrentSet(event)
        self.currDataSet["OB missile"] = f"{self.__obstringmis.get()}/{self.__obmval.get()} {self.__attacks[self.__selectOBmis.get()]}".strip("/")

        self.updateWindow()


    def __addPic(self, event):
        '''!
        This method adds the link to a NPC's /beast's picture (jpg/png)
        '''
        #os.chdir(self.nscpicpath)
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

        if type(self.piclink) == type(""):
            # @bug Image is part of a different package with different functions
            # that's why here is a re-import.
            from PIL import Image, ImageTk
            self.selectedPic = ImageTk.PhotoImage(Image.open(self.piclink).resize((300, 300), Image.ANTIALIAS))
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
        """!
        This loads the data of the GM default table.
        """
        self.GMcontent = readCSV(self.GMtable)
        logger.info(f"{self.GMtable} loaded successfully.")
        self.__header = list(self.GMcontent[0].keys())
        ## @var self.NPCs
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

        if self.nscpicpath[-1] == "/":
            self.__datatemplate["piclink"] = self.nscpicpath + "default.jpg"

        else:
            self.__datatemplate["piclink"] = self.nscpicpath + "/default.jpg"

        logger.debug("data template set")
        self.GMcontent = sortDictlist(dictlist = self.GMcontent, key = "category", reverse = False)
        self.currDataSet = deepcopy(self.GMcontent[0])


    def loadCP(self):
        """!
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
        '''!
        This opens a new campaign table an the selection window of the GM master
        table.

        ----
        @todo this has to be fully implemented
        '''
        cp = showCPWin(rootwin = self.window, CPtable = [])
        #self.notdoneyet("newCPTable")


    def openCPTable(self):
        '''!This opens an existing campaign table for editing purposes

        ----
        @todo this has to be implemented fully
        '''
        self.loadCP()
        cp = showCPWin(rootwin = self.window, CPtable = self.NPCs)


    def prepareAttackData(self):
        """!
        This prepares the attack data for displaying widgets
        """
        ## @var self.__attacks
        # holding weapon/attack name as index and short form as value
        self.__attacks = {}
        ## @var self.__meleelist
        # list of all melee attack / weapon names
        self.__meleelist = []
        ## @var self.__missilelist
        # list of all missile/thrown attack / weapon names
        self.__missilelist = []
        ## @var self.__magiclist
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

    #def addToOBstring(self, event = None):
    #    """!This adds an additional entry to OB string
    #
    #    ----
    #    @todo has to be implemented fully
    #    """
    #    pass


    def __chooseCP(self):
        """!
        this opens a window to choose NPCs beasts you want to save in a separate
        campaign list.
        """

        CPwin = showNPCWin(rootwin = self.window, GMtable = self.GMcontent,
                           CPtable = self.NPCs, lang = self.lang)



class showNPCWin(blankWindow):
    '''!This generates a window to show / list the content of the GM NPC / Beast DB
    and to select from for individual campaign tables.

    ----
    @todo this has to be implemented fully
    '''


    def __init__(self, rootwin, GMtable = [], CPtable = [], lang = "en", datapath = "",
                 nscpath = "", nscpicpath = ""):
        '''!
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
        '''!
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        #self.filemenu.add_command(label = submenu['file'][self.lang]['save GM'],
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
        '''!
        This adds an Edit menu to the windows menu bar:

        ----
        @todo has to be implemended fully.
        '''
        self.editmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu["menu_edit"][self.lang],
                              menu = self.editmenu)
        #self.editmenu.add_command(label = submenu['edit'][self.lang]["ed_add_enemy"],
        logger.debug("edit menu build")


    def __quit(self):
        '''!
        This method saves changes and closes the window
        '''
        self.__saveCPTable(self.CPtable)
        self.window.destroy()


    def __buildWin(self):
        """!
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
                #self.catid += 1

            else:
                self.cptree.insert(self.catid - 1, END, values = tuple(elem[1:]))

        self.cptree.bind('<<TreeviewSelect>>', self.__CPItemSelected)


    def __GMItemSelected(self, event = None):
        """!This handles the detailed display of the selected treeview item
        """
        self.__gmitem = []
        self.__gm_parent_id = []

        for selected_item in self.gmtree.selection():

            if self.gmtree.item(selected_item)["values"]:
                self.__gmitem.append(self.gmtree.item(selected_item))
                self.__gm_parent_id.append(self.gmtree.parent(selected_item))
                #print(f"DEBUG {json.dumps(self.__gmitem, indent = 3)}")
                #print(f"DEBUG {selected_item}")


    def __CPItemSelected(self, event = None):
        """!This handles the detailed display of the selected treeview item

        ----
        @note currently it is a dummy method

        @todo this has to be fully implemented
        """
        self.__cpitem = []

        for selected_item in self.cptree.selection():
            self.__cpitem.append(self.cptree.item(selected_item))
            #print(json.dumps(self.__cpitem, indent = 3))


    def __pushToCP(self, event = None):
        """!
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
        """!
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
        """!
        This initializes a new (empty) NPC / Beast table for campaigns

        ----
        @todo This has to be fully implemented
        """
        self.notdoneyet("__newCPTable")


    def __existInTreeview(self, treeview, comparevalues = []):
        """!This checks if a value set already exists in a treeview widget

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
        """!
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
        #print(f"DEBUG: save {json.dumps(self.NPCs,indent=4)}")
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


    def prepareDataForTreeview(self, dictlist = [], fields = ["category", "name", "lvl", "enc", "hits", "AT", "size"]):
        """!This prepares data for the treeview widget

        @param dictlist list of dictionaries for preparation
        @param fields fields for the tuples in result
        @retval result list for treeview
        """
        #print(json.dumps(dictlist, indent = 4))
        result = []

        if dictlist:
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
        """!
        This updates teh windows widgets

        ----
        @todo has to be fully implemented
        """

        pass


    def __updateDataLists(self, event = None):
        """!This updates all internal data lists

        ----
        @todo this has ti be fully implemented
        """
        #for catkey in self.cats.keys():
        #    self.cptree.insert('', END, iid = self.cats[catkey], text = catkey)

        for elem in self.CPtree:

            if elem[0] != self.oldcat:
                self.oldcat = elem[0]

                if self.oldcat not in self.cats.keys():
                    print(f"DEBUG: updtdlist {json.dumps(self.cats,indent=3)}")
                    self.cats[self.oldcat] = self.catid
                    self.cptree.insert('', END, iid = self.cats[self.oldcat], text = self.oldcat)
                    self.catid += 1

                self.cptree.insert(self.cats[self.oldcat], END, values = tuple(elem[1:]))
                #self.catid += 1

            else:
                self.cptree.insert(self.catid - 1, END, values = tuple(elem[1:]))



class magicSelectorWin(blankWindow):
    """!
    This generates a window to select spell lists and determine their level for a NPC
    or a beast.
    """


    def __init__(self, rootwin = None, lang = "en", datapath = "./data", magicstring = ""):
        """!
        Constructor

        @param datapath configured data path
        @param magicstring string that holds the spell lists and levels
        """
        ##\var self.rootwin
        # the reference to the root window/object \ref monstercreatorWin to transfer finally the modified
        # #magicstring back
        self.rootwin = rootwin
        self.lang = lang
        self.__datapath = datapath

        if self.__datapath[:2] == "./":
            self.__datapath = os.getcwd() + self.__datapath[1:]

        if  "/magic" not in self.__datapath:
            self.__datapath = self.__datapath.rstrip("/") + "/magic"

        ##\var self.magicstring
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
        #self.topmagic = Toplevel(self.window)
        #self.topmagic.title("NSC/Monster Magic Selector")
        #self.topmagic.grab_set()
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addHelpMenu()
        self.__buildWin()
        #self.window.mainloop()

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
        '''!
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        #self.filemenu.add_command(label = submenu['file'][self.lang]['save GM'],
        #                          command = self.saveGM)
        #self.filemenu.add_separator()
        #self.filemenu.add_command(label = submenu['file'][self.lang]['new CP'],
        #                          command = self.__newCPTable)
        #self.filemenu.add_command(label = submenu['file'][self.lang]['open CP'],
        #                          command = self.__openCPTable)
        #self.filemenu.add_command(label = submenu['file'][self.lang]['save CP'],
        #                          command = self.__saveCPTable)
        #self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)
        logger.debug("file menu build")


    def __addEditMenu(self):
        '''!
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
        '''!
        This method saves changes and closes the window
        '''
        self.__finalize()
        self.__updMagicRoot()
        self.window.destroy()


    def __buildWin(self):
        """!
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
        ## @var self.__magicParents
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
            #for sl in self.__magicdict[oldtype]:
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
        """!
        This initially prepares the internal data structure self.__selectedMagic
        for treeview from self.magicstring
        """
        ##\var self.__selectMagic
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
        """!
        This Loads all the available Spell lists
        """
        allfiles = glob(self.__datapath + "/*/*.csv")

        ## \var self.__magicdict
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
        """!This adds a selected spell list with the selected level to the list

        ----
        @todo this has  to be fully implemented
        """
        self.__getSelectedSL()
        lvl = self.__levelSL.get()
        #print(f"DEBUG: {self.__SLitem}\n\t{self.__SL_parent_id}")

        for i in range(0, len(self.__SLitem)):
            values = self.__SLitem[i]["values"]
            values.append(lvl)

            try:
                # try to insert parent
                self.selectedMagicTree.insert('', END, iid = self.__SL_parent_id[i], text = self.__magicParents[int(self.__SL_parent_id[i])])
                logger.debug(f"add {self.__magicParents[self.__SL_parent_id[i]]} to selection tree")

            except:
                # parent already exists...
                pass

            finally:

                if not self.__existInTreeview(treeview = self.selectedMagicTree, comparevalues = self.__SLitem[i]["values"]):
                    self.selectedMagicTree.insert(self.__SL_parent_id[i], END, values = tuple(values))
                    #print(f"DEBUG Values: {values}")


    def __deleteSpellList(self, event = None):
        """!
        This removes a selected spell list from the list of selected spell lists.
        """
        selected_items = self.selectedMagicTree.selection()
        for item in selected_items:
            self.selectedMagicTree.delete(item)

        self.__finalize()


    def __slComboGet(self, event = None):
        """!
        A dirty workaround because the class has to be re-factored for Toplevel instead mainloop
        """
        self.__levelSL.set(self.__slCombo.get())


    def __getSelectedSL(self):
        """!
        This gets the selection of treeview items
        """
        self.__SLitem = []
        self.__SL_parent_id = []

        for selected_item in self.allMagicTree.selection():

            if self.allMagicTree.item(selected_item)["values"]:
                self.__SLitem.append(self.allMagicTree.item(selected_item))
                self.__SL_parent_id.append(self.allMagicTree.parent(selected_item))


    def __existInTreeview(self, treeview, comparevalues = []):
        """!
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
        """!
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
        """!
        This generates a new #magicstring from data of #selectedMagicTree and
        hands it over to  \ref monstercreatorWin
        """
        self.rootwin.currDataSet["spells"] = deepcopy(self.magicstring).replace("_", " ")
        self.rootwin.updateWindow()
        #self.__quit()


    def __checkMagicString(self):
        """!
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

                        except:
                            pass

                        finally:
                            self.selectedMagicTree.insert(int(index), END, values = (sl, int(lvl)))

                        break



class showCPWin(Toplevel, blankWindow):
    '''!
    This generates a display window for individual campaign tables

    ----
    @todo this has to be fully implemented
    '''


    def __init__(self, rootwin, CPtable = []):
        '''!constructor
        @param CPtable list of dictionaries (NPCs / Monster data) of campaign table
        '''
        super().__init__(rootwin)
        self.CPtable = CPtable
        self.notdoneyet("showCPWin")



if __name__ == '__main__':
    monstercreator = monstercreatorWin(config = mycnf)
    #monstercreator.ref = monstercreator
