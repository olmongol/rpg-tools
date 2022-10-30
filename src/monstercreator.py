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
\version 0.1
'''
__version__ = "0.1"
__updated__ = "30.10.2022"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__me__ = "RM RPG Tools: nsc/monster creator module"

from copy import deepcopy
from tkinter import filedialog
#from tkinter.ttk import Combobox, Treeview, Scrollbar
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
        #self.editmenu.add_command(label = submenu['edit'][self.lang]["ed GM table"],
        #                          command = self.notdoneyet)
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

        ##------------ row 0

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
                           rowspan = 9,
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
        self.__name.set(self.__currDataSet["name"])
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
        self.__lvl.set(self.__currDataSet["lvl"])
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
        self.__hits.set(self.__currDataSet["hits"])
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
        self.__at.set(self.__currDataSet["AT"])
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
        self.__size.set(self.__currDataSet["size"])
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
        self.__pp.set(self.__currDataSet["PP"])
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
        self.__qu.set(self.__currDataSet["Qu"])
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
        self.__dbm.set(self.__currDataSet["DBm"])
        self.__EntryDBm = Entry(self.window,
                                justify = "center",
                                textvariable = self.__dbm,
                                width = 4
                                )
        self.__EntryDBm.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryDBm.grid(row = 2, column = 6, sticky = "EW")

        Label(self.window,
              text = "DB:"
              ).grid(row = 2, column = 7, sticky = "EW")

        self.__db = StringVar()
        self.__db.set(self.__currDataSet["DB"])
        self.__entryDB = Entry(self.window,
                              justify = "center",
                              textvariable = self.__db,
                              width = 4
                              )
        self.__entryDB.bind("<FocusOut>", self.updateCurrentSet)
        self.__entryDB.grid(row = 2, column = 8, sticky = "EW")

        #----------- row 3
        self.__obstring = StringVar()
        self.__obstring.set(self.__currDataSet["OB melee"])
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
        self.__obstringmis.set(self.__currDataSet["OB missile"])
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
        Button(self.window,
               text = txtbutton["but_new_one"][self.lang],
               command = self.__newElement
               ).grid(row = 5, column = 2, sticky = "EW")

        Label(self.window,
              text = "enc:"
              ).grid(row = 5, column = 3, sticky = "EW")

        self.__enc = StringVar()
        self.__enc.set(self.__currDataSet["enc"])
        self.__EntryEnc = Entry(self.window,
                                  justify = "center",
                                  textvariable = self.__enc,
                                  width = 4
                                  )
        self.__EntryEnc.bind("<FocusOut>", self.updateCurrentSet)
        self.__EntryEnc.bind("<Return>", self.updateCurrentSet)
        self.__EntryEnc.grid(row = 5, column = 4, sticky = "EW")
        #------- row 6
        vscroll = Scrollbar(self.window, orient = VERTICAL)
        self.__displayComment = Text(self.window,
                                  yscrollcommand = vscroll.set,
                                  height = 6
                                  )
        vscroll.config(command = self.__displayComment.yview)
        self.__displayComment.bind("<FocusOut>", self.updateCurrentSet)
        self.__displayComment.grid(row = 6, rowspan = 3, column = 2, columnspan = 3, sticky = "NEWS")
        self.__insertComment()


    def __newElement(self, even = None):
        """!
        This adds a new element to the NPC / Beast list
        """
        if self.__datatemplate not in self.GMcontent:
            self.GMcontent.append(self.__datatemplate)
            logger.debug("appended empty element to NSC / Beast list")
            self.__index = len(self.GMcontent) - 1
            self.__currDataSet = deepcopy(self.__datatemplate)
            self.__updateWindow()
        pass


    def __insertComment(self, event = None):
        """!This puts data into comment text widget"""
        self.__displayComment.delete("1.0", "end")
        self.__displayComment.insert(END, self.__currDataSet["comment"])


    def __getComment(self, event = None):
        """!This gets data from comment text widget """
        self.__currDataSet["comment"] = self.__displayComment.get("1.0", END)


    def __prevItem(self, event = None):
        """!
        This moves to the previous NSC / beast in the GM master table
        """
        if self.__index > 0:
            self.__index -= 1
            self.GMcontent[self.__index + 1] = deepcopy(self.__currDataSet)
            self.__currDataSet = deepcopy(self.GMcontent[self.__index])
            self.__updateWindow()


    def __nextItem(self, event = None):
        """!
        This moves to the previous NSC / beast in the GM master table
        """
        if self.__index < len(self.GMcontent) - 1:
            self.__index += 1
            self.GMcontent[self.__index - 1] = deepcopy(self.__currDataSet)
            self.__currDataSet = deepcopy(self.GMcontent[self.__index])
            self.__updateWindow()


    def __updateWindow(self, event = None):
        """!
        This updates all window widgets with data of the current data set
        """
        #------- update pic
        if self.__currDataSet["piclink"][:2] == "./":
            self.__currDataSet["piclink"] = self.__currdir + self.__currDataSet["piclink"][1:]

        elif self.__currDataSet["piclink"][0] != "/":
            self.__currDataSet["piclink"] = self.__currdir + "/" + self.__currDataSet["piclink"][1:]

        from PIL import Image
        self.selectedPic = ImageTk.PhotoImage(Image.open(self.__currDataSet["piclink"]).resize((300, 300), Image.ANTIALIAS))
        self.picLabel.configure(image = self.selectedPic)

        #------- update category, name etc.
        self.__selectCat.set(self.__currDataSet["category"])

        if self.__currDataSet["category"] not in self.NPCcat:
            self.NPCcat.append(self.__currDataSet["category"])
            self.NPCcat.sort()
            self.__catCombo.config(value = self.NPCcat)

        self.__name.set(self.__currDataSet["name"])
        self.__lvl.set(self.__currDataSet["lvl"])
        self.__hits.set(self.__currDataSet["hits"])
        self.__at.set(self.__currDataSet["AT"])
        self.__size.set(self.__currDataSet["size"])
        self.__pp.set(self.__currDataSet["PP"])
        self.__qu.set(self.__currDataSet["Qu"])
        self.__dbm.set(self.__currDataSet["DBm"])
        self.__db.set(self.__currDataSet["DB"])
        self.__obstring.set(self.__currDataSet["OB melee"])
        self.__obstringmis.set(self.__currDataSet["OB missile"])
        self.__enc.set(self.__currDataSet["enc"])
        self.__insertComment()


    def updateCurrentSet(self, event = None):
        """!
        This updates the current data set
        """
        self.__currDataSet["category"] = self.__selectCat.get()
        self.__currDataSet["name"] = self.__name.get()
        self.__currDataSet["lvl"] = self.__lvl.get()
        self.__currDataSet["hits"] = self.__hits.get()
        self.__currDataSet["AT"] = self.__at.get()
        self.__currDataSet["size"] = self.__size.get()
        self.__currDataSet["PP"] = self.__pp.get()
        self.__currDataSet["Qu"] = self.__qu.get()
        self.__currDataSet["DBm"] = self.__dbm.get()
        self.__currDataSet["DB"] = self.__db.get()
        self.__currDataSet["OB melee"] = self.__obstring.get()
        self.__currDataSet["OB missile"] = self.__obstringmis.get()

        if self.__currDataSet["OB missile"] == "":
            self.__currDataSet["OB missile"] = "0xx"

        self.__currDataSet["enc"] = self.__enc.get()
        print(f'DEBUG: {self.__currDataSet["name"]} {self.__currDataSet["enc"]}')
        self.__getComment()
        self.GMcontent[self.__index] = deepcopy(self.__currDataSet)


    def __getCategory(self, event = None):
        '''!
        This detemines the selected category
        '''
        self.__currDataSet["category"] = self.__selectCat.get()

        if self.__currDataSet["category"] not in self.NPCcat:
            self.NPCcat.append(self.__currDataSet["category"])


    def __getOB(self, event = None):
        """! This determines the selected attack for melee OB string

        ---
        @todo this has to be implemented fully.
        """
        self.__currDataSet["OB melee"] = f"{self.__obstring.get()}/{self.__obval.get()} {self.__selectOBsize.get()} {self.__attacks[self.__selectOB.get()]}"
        self.__updateWindow()


    def __getOBm (self, event = None):
        """! This determines the selected attack for missile OB string

        ---
        @todo this has to be implemented fully.
        """
        #self.updateCurrentSet(event)
        self.__currDataSet["OB missile"] = f"{self.__obstringmis.get()}/{self.__obmval.get()} {self.__attacks[self.__selectOBmis.get()]}".strip("/")

        self.__updateWindow()


    def __addPic(self, event):
        '''!
        This method adds the link to a NPC's /beast's picture (jpg/png)
        '''
        #os.chdir(self.nscpicpath)
        pmask = [txtwin['jpg_files'][self.lang],
                 txtwin['jpeg_files'][self.lang],
                 txtwin['png_files'][self.lang]
                 ]
        beastNPCpic = askopenfilename(filetypes = pmask,
                                      initialdir = self.nscpicpath
                                      )
        if self.nscpicpath[-1] == "/":
            self.piclink = f"{self.nscpicpath}{beastNPCpic.split('/')[-1]}"

        else:
            self.piclink = f"{self.nscpicpath}/{beastNPCpic.split('/')[-1]}"

        logger.debug(f"piclink set to {self.piclink}")
        self.__currDataSet["piclink"] = self.piclink

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
        self.__currDataSet = deepcopy(self.GMcontent[0])


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

        for w in self.__weaponlist:

            if w["wtype"] not in ["th", "mis"]:
                self.__meleelist.append(w["item"])

            if  w["wtype"] in ["th", "mis"] or "th" in w["wtype"]:
                self.__missilelist.append(w["item"])
                #print(self.__missilelist)
            self.__attacks[w["item"]] = w["shortc"]

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
        @todo This has to be fully implemented
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
        #self.gmtree.column("#0", minwidth = 0, width = 100, stretch = YES)

        self.gmtree.heading(self.__columns[1], text = self.__columns[1])
        #self.gmtree.column(self.__columns[1], minwidth = 0, width = 100, stretch = YES)

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
        #self.cptree.column("#0", minwidth = 0, width = 100, stretch = YES)

        self.cptree.heading(self.__columns[1], text = self.__columns[1])
        #self.cptree.column(self.__columns[1], minwidth = 0, width = 100, stretch = YES)

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
                print(f"DEBUG {json.dumps(self.__gmitem, indent = 3)}")
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
            print(json.dumps(self.__cpitem, indent = 3))


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

        if 'I' in rowid:
            self.cptree.delete(rowid)


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



class showCPWin(blankWindow):
    '''!
    This generates a display window for individual campaign tables

    ----
    @todo this has to be fully implemented
    '''


    def __init__(self, rootwin, CPtable = []):
        '''!constructor
        @param CPtable list of dictionaries (NPCs / Monster data) of campaign table
        '''

        self.CPtable = CPtable
        self.notdoneyet("showCPWin")



if __name__ == '__main__':
    monstercreator = monstercreatorWin(config = mycnf)
