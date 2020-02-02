import os
import json
from gui.window import *
from rpgtoolbox import epcalc, rpgtools as rpg
from rpgToolDefinitions.epcalcdefs import maneuvers
from pprint import pprint



class EPCalcWin(blankWindow):
    """
    This is a GUI for EP calculation for your character party.
    """


    def __init__(self, lang = "en", charlist = [], storepath = "./data"):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param charlist list of dictionaries holding: player, charname, EPs
        \param storepath path for storing the data into the character files.
        """

        self.lang = lang
        self.charlist = charlist
        self.storepath = storepath
        blankWindow.__init__(self, self.lang)
        self.window.title("EP Calculator")
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
                                  command = self.notdoneyet)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.notdoneyet)
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


    def __buildWin(self):
        """
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
               command = self.notdoneyet
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
               ).grid(row = 3, column = 6, rowspan = 2, sticky = "NEWS")

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
               command = self.notdoneyet,
               bg = "grey",
               fg = "white"
               ).grid(row = 6, column = 6, sticky = "EW")


    def __updDispay(self, curPlayer = ""):
        '''
        Updates display of current player
        \param curPlayer name of selected player
        '''
        self.group[curPlayer].updateInfo()
        self.__gained.set("+{}".format(self.group[curPlayer].gainedep))
        self.__newep.set("<{}>".format(self.group[curPlayer].newep))
        self.__newlvl.set(self.group[curPlayer].newlvl)


    def __updSelec(self, event):
        """
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


    def __grpBonus(self):
        '''
        This methods calculates the group bonus while finalize process.
        '''
        grpbonus = 0

        for name in self.group.keys():
            grpbonus = self.group[name].gainedep

        grpbonus = int(round(grpbonus / len(self.group.keys())))

        for name in self.group.keys():
            self.group[name].gainedep += grpbonus
            self.group[name].updateInfo()


    def __calcMan(self):
        '''
        This computes EPs for each successful maneuver and add them to character's
        gained EPs
        '''
        curPlayer = self.__selecPlayer.get()
        curManLvl = self.__selecman.get()
        number = self.__cMan.get()

        self.group[curPlayer].maneuver(curManLvl, number)
        self.__updDispay(curPlayer)


    def __calcSpell(self):
        '''
        This computes EPs for a given number aof spells aof the same level
        '''
        curPlayer = self.__selecPlayer.get()
        spellLvl = self.__lvlSpell.get()
        spellNo = self.__cSpell.get()
        self.group[curPlayer].spell(spellLvl, spellNo)
        self.__updDispay(curPlayer)


    def __calcGCrit(self):
        '''
        This calculates EP for gained Criticals and hits
        '''
        curPlayer = self.__selecPlayer.get()
        gCrit = self.__gcrit.get()
        hits = self.__hits.get()

        if gCrit in ["T", "KILL"]:
            self.group[curPlayer].gainedHits(hits)

        else:
            self.group[curPlayer].gainedHits(hits)
            self.group[curPlayer].gainedCrit(gCrit, 1)

        self.__updDispay(curPlayer)


    def __calcCrit(self):
        '''
        This calculates EP for caused criticals against an enemy of a certain level
        '''
        curPlayer = self.__selecPlayer.get()
        crit = self.__crit.get()
        lvlEnem = self.__lvlenem.get()

        if crit not in ["T", "KILL"]:
            self.group[curPlayer].hitCrit(crit, lvlEnem, 1)
        elif crit == "KILL":
            self.group[curPlayer].killedNPC(lvlEnem, 1)

        self.__updDispay(curPlayer)


    def __calcTravel(self):
        '''
        Travelled EPs
        ----
        @todo The comments have to be added to the  character's diary
        '''
        curPlayer = self.__selecPlayer.get()
        travel = self.__travel.get()
        comm = self.__comtravel.get()
        self.group[curPlayer].travelled(travel)

        self.__updDispay(curPlayer)


    def __calcIdeas(self):
        '''
        EPs for ideas and role-playing
        ----
        @todo The comments have to be added to the character's diary
        '''
        curPlayer = self.__selecPlayer.get()
        ideas = self.__ideas.get()
        comm = self.__comideas.get()
        self.group[curPlayer].ideas(ideas)

        self.__updDispay(curPlayer)


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()



with open("epdata.json", "r") as fp:
    cl = json.load(fp)

win = EPCalcWin(charlist = cl)
