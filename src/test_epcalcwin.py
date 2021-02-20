#!/usr/bin/python3
'''!
@file test_epcalcwin.py
@package test_epcalcwin.py
@brief This is a little tool for tracking the EPs  of Role Master Characters

@date (C) 2015-2021
@author Marcus Schwamberger
@email marcus@lederzeug.de
@license GNU V3.0
@version 1.2.0
----
@todo
- adding a RR window
- adding a cat/skill checker window for the whole group (select skill once and check for all)
- adding spellcasting windpw (stat man)


'''
import os
import json
from gui.window import *
from rpgtoolbox import epcalc, rpgtools as rpg
from rpgtoolbox.rrwindow import *
from rpgToolDefinitions.epcalcdefs import maneuvers
from pprint import pprint
from rpgToolDefinitions.helptools import RMDice as dice
from tkinter import filedialog
import re
import pickle



class EPCalcWin(blankWindow):
    """!
    This is a GUI for EP calculation for your character party.
    """


    def __init__(self, lang = "en", charlist = [], storepath = "./data"):
        """!
        Class constructor
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param charlist list of dictionaries holding: player, charname, EPs
        @param storepath path for storing the data into the character files.
        """

        self.lang = lang
        self.charlist = charlist
        if self.charlist == []:
            self.charlist.append({  "player": "Marcus",
                                    "exp": 10000,
                                    "prof": "Ranger",
                                    "name": "Player1"
                                })
        self.storepath = storepath
        blankWindow.__init__(self, self.lang)
        self.window.title("EP Calculator")
        self.__addMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.__loadAutosave()
        self.window.mainloop()


    def __addMenu(self):
        '''!
        This methods adds the menu bar to the window
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


    def __addHelpMenu(self):
        """!
        This methods defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __buildWin(self):
        """!
        This method builds the window content.
        """
        ## \var self.players
        # list of given player names
        self.players = []
        ## \var self.group
        # dictionary of EP objects per player
        self.group = {}

        for elem in self.charlist:
            self.players.append(elem["player"])
            self.group[elem["player"]] = epcalc.experience(elem["player"], elem["exp"])
            self.group[elem["player"]].updateInfo()

        self.__selecPlayer = StringVar(self.window)
        self.__selecPlayer.set(self.players[0])

        self.__playerOpt = OptionMenu(self.window,
                                      self.__selecPlayer,
                                      *self.players,
                                      command = self.__updSelec)
        self.__playerOpt.grid(column = 0, row = 0, sticky = "W")

        self.__charname = StringVar()
        self.__charname.set(self.charlist[0]["name"])
        Label(self.window,
              width = 20,
              textvariable = self.__charname,
              ).grid(row = 0, column = 1, sticky = "W")

        self.__charprof = StringVar()
        self.__charprof.set("{} ({})".format(self.charlist[0]["prof"], self.group[self.charlist[0]["player"]].lvl))
        Label(self.window,
              width = 15,
              textvariable = self.__charprof,
              ).grid(row = 0, column = 2, sticky = "W")

        self.__charexp = StringVar()
        self.__charexp.set(str(self.charlist[0]["exp"]))
        Label(self.window,
              width = 15,
              textvariable = self.__charexp,
              ).grid(row = 0, column = 3, sticky = "W")

        self.__gained = StringVar()
        self.__gained.set("+{}".format(self.group[self.charlist[0]["player"]].gainedep))
        Label(self.window,
              width = 10,
              textvariable = self.__gained,
              ).grid(row = 0, column = 4, sticky = "W")

        self.__newep = StringVar()
        self.__newep.set("<{}>".format(self.group[self.charlist[0]["player"]].gainedep + self.group[self.charlist[0]["player"]].ep))
        Label(self.window,
              width = 10,
              textvariable = self.__newep,
              ).grid(row = 0, column = 5, sticky = "W")

        self.__newlvl = IntVar()
        self.__newlvl.set(self.group[self.charlist[0]["player"]].lvl)
        Label(self.window,
              width = 10,
              textvariable = self.__newlvl,
              ).grid(row = 0, column = 6, sticky = "EW")

        #row 1
        Label(self.window,
              text = s_elem_def['MANEUVER'][self.lang] + ":",
              ).grid(row = 1, column = 0, sticky = "EW")

        self.manlist = list(maneuvers.keys())
        self.__selecman = StringVar()
        self.__selecman.set(self.manlist[0])

        self.__manOpt = OptionMenu(self.window,
                                   self.__selecman,
                                   *self.manlist
                                   )
        self.__manOpt.grid(row = 1, column = 1, sticky = "EW")

        Label(self.window,
              text = s_elem_def["COUNT"][self.lang] + ":"
              ).grid(row = 1, column = 2, sticky = "EW")

        self.__cMan = IntVar()
        self.__cMan.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__cMan,
              ).grid(row = 1, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcMan
               ).grid(row = 1, column = 4, sticky = "EW")

        Button(self.window,
               text = labels["win_man"][self.lang],
               command = self.__callManWin
               ).grid(row = 1, column = 6, sticky = "EW")

        #row 2
        Label(self.window,
              text = s_elem_def["SPELL"][self.lang] + ":",
              ).grid(row = 2, column = 0, sticky = "W")

        self.__lvlSpell = IntVar()
        self.__lvlSpell.set(1)
        Entry(self.window,
              justify = "center",
              textvariable = self.__lvlSpell
              ).grid(row = 2, column = 1, sticky = "EW")

        Label(self.window,
              text = s_elem_def["COUNT"][self.lang] + ":"
              ).grid(row = 2, column = 2, sticky = "EW")

        self.__cSpell = IntVar()
        self.__cSpell.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__cSpell,
              ).grid(row = 2, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcSpell
               ).grid(row = 2, column = 4, sticky = "EW")

        Button(self.window,
               text = labels["win_casting"][self.lang],
               command = self.notdoneyet
               ).grid(row = 2, column = 6, sticky = "EW")
        #row 3
        self.critlist = ['T', 'A', 'B', 'C', 'D', 'E', "KILL"]
        Label(self.window,
              text = s_elem_def["H_CRITS"][self.lang] + ":",
              ).grid(row = 3, column = 0, sticky = "W")

        self.__gcrit = StringVar()
        self.__gcrit.set("T")
        OptionMenu(self.window,
                    self.__gcrit,
                    *self.critlist
                   ).grid(row = 3, column = 1, sticky = "EW")

        Label(self.window,
              text = s_elem_def["HITS"][self.lang] + ":",
              ).grid(row = 3, column = 2, sticky = "W")

        self.__hits = IntVar()
        self.__hits.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__hits,
              ).grid(row = 3, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcGCrit
               ).grid(row = 3, column = 4, sticky = "EW")

        Button(self.window,
               text = labels["win_fight"][self.lang],
               command = self.notdoneyet
               ).grid(row = 3, column = 6, sticky = "NEWS")

        #row 4
        Label(self.window,
              text = s_elem_def["CRITICAL"][self.lang] + ":",
              ).grid(row = 4, column = 0, sticky = "W")

        self.__crit = StringVar()
        self.__crit.set("T")
        OptionMenu(self.window,
                    self.__crit,
                    *self.critlist
                   ).grid(row = 4, column = 1, sticky = "EW")
        Label(self.window,
              text = labels["lvl_enemy"][self.lang] + ":",
              ).grid(row = 4, column = 2, sticky = "WE")

        self.__lvlenem = IntVar()
        self.__lvlenem.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__lvlenem,
              ).grid(row = 4, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcCrit
               ).grid(row = 4, column = 4, sticky = "EW")
        Button(self.window,
               text = txtbutton["but_rr"][self.lang],
               command = self.__rrroll
               ).grid(row = 4, column = 6, sticky = "EW")

        #row 5
        Label(self.window,
              text = s_elem_def["TRAVEL"][self.lang] + ":",
              ).grid(row = 5, column = 0, sticky = "W")

        self.__travel = IntVar()
        self.__travel.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__travel,
              ).grid(row = 5, column = 1, sticky = "EW")
        Label(self.window,
              text = labels["comment"][self.lang] + ":",
              ).grid(row = 5, column = 2, sticky = "EW")

        self.__comtravel = StringVar()
        self.__comtravel.set("")
        Entry(self.window,
              justify = "center",
              textvariable = self.__comtravel,
              ).grid(row = 5, column = 3, sticky = "EW")
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcTravel
               ).grid(row = 5, column = 4, sticky = "EW")

        Button(self.window,
               text = labels["diary"][self.lang],
               command = self.notdoneyet
               ).grid(row = 5, column = 6, sticky = "EW")
        #row 6
        Label(self.window,
              text = s_elem_def["IDEAS"][self.lang] + ":",
              ).grid(row = 6, column = 0, sticky = "W")

        self.__ideas = IntVar()
        self.__ideas.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__ideas,
              ).grid(row = 6, column = 1, sticky = "EW")
        Label(self.window,
              text = labels["comment"][self.lang] + ":",
              ).grid(row = 6, column = 2, sticky = "EW")
        self.__comideas = StringVar()
        self.__comideas.set("")
        Entry(self.window,
              justify = "center",
              textvariable = self.__comideas,
              ).grid(row = 6, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcIdeas
               ).grid(row = 6, column = 4, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_fin"][self.lang],
               command = self.__finalize,
               bg = "grey",
               fg = "white"
               ).grid(row = 6, column = 6, sticky = "EW")


    def __updDispay(self, curPlayer = ""):
        '''!
        Updates display of current player
        @param curPlayer name of selected player
        '''
        self.group[curPlayer].updateInfo()
        self.__gained.set("+{}".format(self.group[curPlayer].gainedep))
        self.__newep.set("<{}>".format(self.group[curPlayer].newep))
        self.__newlvl.set(self.group[curPlayer].newlvl)


    def __updSelec(self, event):
        """!
        Update selected Player data
        """
        selected = self.__selecPlayer.get()
        ind = self.players.index(selected)
        self.__charname.set(self.charlist[ind]["name"])
        self.__charprof.set("{} ({})".format(self.charlist[ind]["prof"], self.group[selected].lvl))
        self.__charexp.set(str(self.charlist[ind]["exp"]))
        self.__gained.set("+{}".format(self.group[self.charlist[ind]["player"]].gainedep))
        self.__newep.set("<{}>".format(self.group[self.charlist[ind]["player"]].gainedep + self.group[self.charlist[ind]["player"]].newep))
        self.__newlvl.set(self.group[self.charlist[ind]["player"]].newlvl)


    def __autoSave(self):
        """!
        This function is for aut saving the group object in case of a program / computer crash
        """
        with open("autosave.pkl", "wb") as fp:
            pickle.dump(self.group, fp)


    def __loadAutosave(self):
        """!
        This loads an autosave file if there is any
        """
        if os.path.exists("autosave.pkl"):
            with open("autosave.pkl", "rb") as fp:
                self.group = pickle.load(fp)

            os.remove("autosave.pkl")


    def __grpBonus(self):
        '''!
        This methods calculates the group bonus while finalize process.
        '''
        grpbonus = 0

        for name in self.group.keys():
            grpbonus += self.group[name].gainedep

        grpbonus = int(round(grpbonus / len(self.group.keys())))

        for name in self.group.keys():
            self.group[name].gainedep += grpbonus
            self.group[name].updateInfo()

        self.__autoSave()


    def __calcMan(self):
        '''!
        This computes EPs for each successful maneuver and add them to character's
        gained EPs
        '''
        curPlayer = self.__selecPlayer.get()
        curManLvl = self.__selecman.get()
        number = self.__cMan.get()

        self.group[curPlayer].maneuver(curManLvl, number)
        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcSpell(self):
        '''!
        This computes EPs for a given number aof spells aof the same level
        '''
        curPlayer = self.__selecPlayer.get()
        spellLvl = self.__lvlSpell.get()
        spellNo = self.__cSpell.get()
        self.group[curPlayer].spell(spellLvl, spellNo)
        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcGCrit(self):
        '''!
        This calculates EP for gained criticals and hits
        '''
        curPlayer = self.__selecPlayer.get()
        gCrit = self.__gcrit.get()
        hits = self.__hits.get()

        if gCrit in ["T", "KILL"]:
            self.group[curPlayer].gainedHits(hits)

        else:
            self.group[curPlayer].gainedHits(hits)
            self.group[curPlayer].gainedCrit(gCrit, 1)

        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcCrit(self):
        '''!
        This calculates EP for caused criticals against an enemy of a certain level
        '''
        curPlayer = self.__selecPlayer.get()
        crit = self.__crit.get()
        lvlEnem = self.__lvlenem.get()

        if crit not in ["T", "KILL"]:
            self.group[curPlayer].hitCrit(crit, lvlEnem, 1)
        elif crit == "KILL":
            self.group[curPlayer].killedNPC(lvlEnem, 1)

        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcTravel(self):
        '''!
        Travelled EPs
        ----
        @todo The comments have to be added to the  character's diary
        '''
        curPlayer = self.__selecPlayer.get()
        travel = self.__travel.get()
        comm = self.__comtravel.get()
        self.group[curPlayer].travelled(travel)

        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcIdeas(self):
        '''!
        EPs for ideas and role-playing
        ----
        @todo The comments have to be added to the character's diary
        '''
        curPlayer = self.__selecPlayer.get()
        ideas = self.__ideas.get()
        comm = self.__comideas.get()
        self.group[curPlayer].ideas(ideas)

        self.__autoSave()
        self.__updDispay(curPlayer)


    def __finalize(self):
        '''!
        Do all finalizing steps:
        -# adding new EPs to characters
        -# open display window for whole group EPs
        -# store new levels
         - in character's files
         - in group file
        '''
        self.__grpBonus()
        for i in range(0, len(self.charlist)):
            name = self.charlist[i]['player']
            self.charlist[i]["exp"] = self.group[name].newep
            self.charlist[i]['old_exp'] = self.group[name].ep

        self.__autoSave()
        gw = showGrpEP(self.charlist, self.storepath, self.lang)


    def __callManWin(self):
        '''!
        Opens Maneuver Window for maneuver rolls
        '''
        who = self.__selecPlayer.get()
        for elem in self.charlist:
            if elem['player'] == who:
                manWin(elem, self.lang)


    def __rrroll(self):
        '''!
        This opens a resistance roll window
        ----
        @todo has to be implemented fully
        '''
        who = self.__selecPlayer.get()
#        for elem in self.charlist:
#            if elem['player'] == who:
#                RRWin(self.lang, elem, self.charlist, self.storepath)
        RRWin(self.lang, who, self.charlist, self.storepath)


    def __save(self):
        '''!
        This opens a file dialog window for saving
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.charlist, fp, indent = 4)


    def __open(self):
        '''!
        This opens a file dialog window for opening a group file.
        '''
        opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])
        with open(opendir, "r") as fp:
            self.charlist = json.load(fp)
        #set up new player group list
        self.players = []
        self.group = {}
        for elem in self.charlist:
            self.players.append(elem["player"])
            self.group[elem["player"]] = epcalc.experience(elem["player"], elem["exp"])
            self.group[elem["player"]].updateInfo()

        self.__selecPlayer.set(self.players[0])
        self.__playerOpt = OptionMenu(self.window,
                                      self.__selecPlayer,
                                      *self.players,
                                      command = self.__updSelec)
        self.__playerOpt.grid(column = 0, row = 0, sticky = "W")


    def __quit(self):
        '''!
        This method closes the window
        '''
        self.window.destroy()



class showGrpEP(object):
    '''!
    Display and save window for group EPs
    '''


    def __init__(self, charlist = [], storepath = "./data", lang = 'en'):
        """!
        Constructor
        @param lang contains the chosen display language.
        """
        self.lang = lang
        self.storepath = storepath
        self.charlist = charlist
        self.window = Toplevel()
        self.title = wintitle["rm_groupEP"][self.lang]

        self.window.title(self.title)
        for i in range(0, len(self.charlist)):
            Label(self.window,
                  text = "{} ({}):".format(self.charlist[i]["player"],
                                         self.charlist[i]["name"])
                  ).grid(row = i, column = 0, sticky = "EW")
            Label(self.window,
                  text = "+{} -> {}".format(self.charlist[i]["exp"] - self.charlist[i]["old_exp"],
                                            self.charlist[i]['exp'])
                  ).grid(row = i, column = 1, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_save_char"][self.lang],
               command = self.saveChars,
               bg = "grey",
               fg = "white"
               ).grid(row = i + 1, column = 0, sticky = "NEWS")
        Button(self.window,
               text = txtbutton["but_save_grp"][self.lang],
               command = self.saveGroup
               ).grid(row = i + 1, column = 1, sticky = "NEWS")

        self.window.mainloop()


    def saveChars(self):
        '''!
        This saves all single characters separated from group
        '''
        if self.storepath[-1] != "/":
            self.storepath += "/"
        if os.path.exists(self.storepath):

            for char in self.charlist:
                charpath = self.storepath + "/" + char["player"] + "/"

                if os.path.exists(charpath):
                    with open(charpath + char['name'] + ".json", "w") as fp:
                        json.dump(char, fp, indent = 4)
                    print("data saved to {}".format(charpath + char['name'] + ".json"))
                else:
                    print("{} not found -> {}".format(charpath, os.getcwd()))

#        if os.path.exists("autosave.pkl"):
#            os.remove("autosave.pkl")


    def saveGroup(self):
        '''!
        Saves all data in a groupfile
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.charlist, fp, indent = 4)

        if os.path.exists("autosave.pkl"):
            os.remove("autosave.pkl")



class manWin(object):
    '''
    Maneuver Window
    '''


    def __init__(self, character = {}, lang = "en"):
        '''!
        Constructor
        @param character whole character daa
        @param lang interface language; default: English
        '''
        self.character = character
        self.lang = lang
        self.man_ep = 0
        ## @var self.total
        # total result of skill check
        self.total = 0
        self.category = "Armor - Heavy"
        self.skill = ""
        self.man = "routine"
        self.maneuver = maneuvers
        self.mantab = rpg.statManeuver()
        self.dice = dice
        self.window = Toplevel()
        self.title = "{}: {} - {}".format(wintitle['rm_maneuver'][self.lang], self.character['player'], self.character['name'])
        self.window.title(self.title)
        self._buildwin()
        self.window.mainloop()


    def _buildwin(self):
        '''
        This defines the different element in the window layout
        '''
        # row 0
        Label(self.window,
              text = self.character["player"]
              ).grid(row = 0, column = 0, sticky = "NEWS")
        Label(self.window,
              text = self.character["name"]
              ).grid(row = 0, column = 2, sticky = "NEWS")
        Label(self.window,
              text = "{}/{} ({})".format(self.character["race"],
                                         self.character["prof"],
                                         self.character["lvl"])
              ).grid(row = 0, column = 4, sticky = "NEWS")
        from PIL import Image, ImageTk
        self.cpic = ImageTk.PhotoImage(Image.open(self.character["piclink"]).resize((210, 210), Image.ANTIALIAS))
        self.picLabel = Label(master = self.window,
                              image = self.cpic
                              )

        self.picLabel.grid(column = 5,
                           row = 0,
                           columnspan = 2,
                           rowspan = 8,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)
        # row 1
        vcscroll = Scrollbar(self.window, orient = VERTICAL)
        self.catlb = Listbox(self.window,
                             yscrollcommand = vcscroll.set,
                              width = 30,
                              height = 5)
        vcscroll.config(command = self.catlb.yview)
        vcscroll.grid(row = 1, column = 1, sticky = "WNS")
        self.catlb.grid(row = 1, column = 0, sticky = "NEW")
        for cat in  self.character["cat"].keys():
            self.catlb.insert(END, cat)
        self.catlb.bind("<Button-1>", self._fillSkill)

        vsscroll = Scrollbar(self.window, orient = VERTICAL)
        self.skilllb = Listbox(self.window,
                               yscrollcommand = vsscroll.set,
                              width = 30,
                              height = 5)
        vsscroll.config(command = self.skilllb.yview)
        vsscroll.grid(row = 1, column = 3, sticky = "WNS")
        self.skilllb.grid(row = 1, column = 2, sticky = "NEW")
        for skill in self.character["cat"]["Armor - Heavy"]["Skill"].keys():
            if skill not in ["Progression", "Stats"] and skill[-1] != "+":
                self.skilllb.insert(END, skill)
        self.skilllb.bind("<Button-1>", self._getSkill)

        vmscroll = Scrollbar(self.window, orient = VERTICAL)
        self.manlb = Listbox(self.window,
                             yscrollcommand = vmscroll.set,
                             height = 5)
        vmscroll.config(command = self.manlb.yview)
        vmscroll.grid(row = 1, column = 5, sticky = "WNS")
        self.manlb.grid(row = 1, column = 4, sticky = "NEW")

        for skill in self.maneuver.keys():
            self.manlb.insert(END, skill)
        self.manlb.bind("<Button-1>", self._getMan)
        # row 2
        self.catlabel = Label(self.window,
                              text = self.category)
        self.catlabel.grid(row = 2, column = 0, sticky = "EWS")

        self.skilllabel = Label(self.window,
                                text = self.skill)
        self.skilllabel.grid(row = 2, column = 2, sticky = "EWS")

        self.manlabel = Label(self.window,
                              text = self.man)
        self.manlabel.grid(row = 2, column = 4, sticky = "EWS")
        #row 3
        Label(self.window,
              text = "+ {}:".format(labels['modifier'][self.lang])
              ).grid(row = 3, column = 0, sticky = "NEWS")

        Button(self.window,
               text = txtbutton["but_roll"][self.lang],
               command = self._rollDice,
               bg = "grey",
               fg = "white",
#               image = "./data/default/pics/d10.png"
               ).grid(row = 3, column = 2, sticky = "NEWS")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self._chkResult
               ).grid(row = 3, column = 4, sticky = "NEWS")
        # row 4
        self.mod = IntVar()
        self.mod.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.mod
              ).grid(row = 4, column = 0, sticky = "EW")
        self.diceroll = StringVar()
        self.diceroll.set("0")
        Entry(self.window,
              justify = "center",
              textvariable = self.diceroll,
              ).grid(row = 4, column = 2, sticky = "EW")

        self.totallabel = StringVar()
        self.totallabel.set("--")
        Label(self.window,
              textvariable = self.totallabel,
              justify = "center"
              ).grid(row = 4, column = 4, sticky = "NEWS")
        # row 5
        Label(self.window,
              text = labels['class'][self.lang] + ":"
              ).grid(row = 5, column = 0, sticky = "NEWS")

        Label(self.window,
              text = labels['perc'][self.lang] + ":"
              ).grid(row = 5, column = 2, sticky = "NEWS")

        Label(self.window,
              text = labels['time'][self.lang] + ":"
              ).grid(row = 5, column = 4, sticky = "NEWS")
        # row 6
        self.classif = StringVar()
        self.classif.set("--")
        Label(self.window,
              textvariable = self.classif,
              ).grid(row = 6, column = 0, sticky = "NEWS")

        self.perc = StringVar()
        self.perc.set("--")
        Label(self.window,
              textvariable = self.perc,
              ).grid(row = 6, column = 2, sticky = "NEWS")

        self.timef = StringVar()
        self.timef.set("--")
        Label(self.window,
              textvariable = self.timef,
              ).grid(row = 6, column = 4, sticky = "NEWS")
        #row 7
        Label(self.window,
              text = labels['modifier'][self.lang] + ":"
              ).grid(row = 7, column = 0, sticky = "NEWS")

        self.modif = StringVar()
        self.modif.set("--")
        Label(self.window,
              textvariable = self.modif
              ).grid(row = 7, column = 2, sticky = "NEWS")
        #row 8
        self.desc = StringVar()
        self.desc.set("")
        Label(self.window,
              wraplength = 700,
              textvariable = self.desc
              ).grid(row = 8,
                     rowspan = 2,
                     column = 0,
                     columnspan = 5,
                     sticky = "NEWS")


    def _fillSkill(self, event):
        '''
        Depending on the selected category fill the skill listbox
        '''

        self.skilllb.delete(0, END)
        selcat = self.catlb.curselection()
        self.catlabel.config(text = "")

        if selcat != ():
            self.category = self.catlb.get(selcat[0])
            self.catlabel.config(text = self.category)
            self.skilllabel.config(text = "")

            for skill in self.character["cat"][self.category]["Skill"].keys():
                if skill not in ["Progression", "Stats"] and skill[-1] != "+":
                    self.skilllb.insert(END, skill)
                else:
                    print("-->".format(skill))


    def _getSkill(self, event):
        '''
        Getting selected Skill
        '''
        selskill = self.skilllb.curselection()
        if selskill != ():
            self.skill = self.skilllb.get(selskill[0])
            self.skilllabel.config(text = self.skill)


    def _getMan(self, event):
        '''
        Get maneuver level
        '''

        selman = self.manlb.curselection()
        if selman != ():
            self.man = self.manlb.get(selman[0])
            self.manlabel.configure(text = self.man)
        print("{} - {} - {}".format(self.category, self.skill, self.man))


    def _rollDice(self):
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


    def _chkResult(self):
        '''
        '''
        dummy = self.diceroll.get()
        um = re.compile(r"(um|Um|UM) ([0-9]{1,3})")
        sr = re.compile(r"[-]*[0-9]+")

        if um.match(dummy):
            self.total = int(um.match(dummy).group(2))

        elif sr.match(dummy):
            self.total = int(sr.match(dummy).group())

        else:
            self.total = 0

        if self.category:
            skilladd = self.character["cat"][self.category]["total bonus"]

            if self.skill:
                skilladd = self.character["cat"][self.category]["Skill"][self.skill]["total bonus"]

        mod = self.mod.get()
        man = maneuvers[self.man]["mod"]
        self.total += skilladd + mod + man

        self.probe = self.mantab.checkRoll(self.total)
        self._updTotal()


    def _updTotal(self):
        self.totallabel.set(str(self.total))
        self.classif.set(self.probe["classification"])
        self.perc.set(self.probe['success'])
        self.timef.set(self.probe['time'])
        self.modif.set(self.probe['mod'])
        self.desc.set(self.probe['description'])
#    def maneuver_ep(self, manlvl = "routine", number = 0):
#        '''
#        Adds EPs by maneuvers.
#        @param manlvl difficulty of maneuver
#        @param number number of maneuvers of this level
#        '''
#        from rpgToolDefinitions.epcalcdefs import maneuvers
#
#        self.man_ep += maneuvers[manlvl]['ep'] * number



if __name__ == '__main__':
    with open("/home/mongol/git/rpg-tools/src/data/groups/charparty.json", "r") as fp:
        cl = json.load(fp)

    mantan = rpg.statManeuver
    rrtab = rpg.RRroll

    win = EPCalcWin()
