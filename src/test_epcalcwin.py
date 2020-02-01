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
        self.players =[]
        ## \var self.group
        # dictionary of EP objects per player
        self.group = {}
        
        for elem in self.charlist:
            self.players.append(elem["player"])
            self.group[elem["player"]] = epcalc.experience(elem["player"],elem["exp"])
            self.group[elem["player"]].updateInfo()
        
        self.__selecPlayer = StringVar(self.window)
        self.__selecPlayer.set(self.players[0])

        self.__playerOpt = OptionMenu(self.window,
                                      self.__selecPlayer,
                                      *self.players,
                                      command=self.__updSelec)
        self.__playerOpt.grid(column=0,row=0,sticky="W")
      
        self.__charname = StringVar()
        self.__charname.set(self.charlist[0]["name"])
        Label(self.window,
              width = 20,
              textvariable = self.__charname,
              ).grid(row=0,column=1,sticky="W")

        self.__charprof = StringVar()
        self.__charprof.set("{} ({})".format(self.charlist[0]["prof"],self.group[self.charlist[0]["player"]].lvl))
        Label(self.window,
              width = 15,
              textvariable = self.__charprof,
              ).grid(row=0,column=2,sticky="W")

        self.__charexp = StringVar()
        self.__charexp.set(str(self.charlist[0]["exp"]))
        Label(self.window,
              width = 15,
              textvariable = self.__charexp,
              ).grid(row=0,column=3,sticky="W")

        self.__gained = StringVar()
        self.__gained.set("+{}".format(self.group[self.charlist[0]["player"]].gainedep))
        Label(self.window,
              width = 10,
              textvariable = self.__gained,
              ).grid(row=0,column=4,sticky="W")

        self.__newep = StringVar()
        self.__newep.set("<{}>".format(self.group[self.charlist[0]["player"]].gainedep+self.group[self.charlist[0]["player"]].ep))
        Label(self.window,
              width = 10,
              textvariable = self.__newep,
              ).grid(row=0,column=5,sticky="W")
                         
        self.__newlvl =IntVar()
        self.__newlvl.set(self.group[self.charlist[0]["player"]].lvl)
        Label(self.window,
              width=10,
              textvariable = self.__newlvl,
              ).grid(row=0,column=6,sticky="EW")
        #row 1
        Label(self.window,
              text = s_elem_def['MANEUVER'][self.lang]+":",
              ).grid(row=1,column=0,sticky="EW")
        
        self.manlist = list(maneuvers.keys())
        self.__selecman = StringVar()
        self.__selecman.set(self.manlist[0])
        OptionMenu(self.window,
                    self.__selecman,
                    *self.manlist,
                    command = self.notdoneyet
                   ).grid(row=1,column=1,sticky="EW")
        Label(self.window,
              text = s_elem_def["COUNT"][self.lang]+":"
              ).grid(row=1,column=2,sticky="EW")
        
        self.__cMan = IntVar()
        self.__cMan.set(0)
        Entry(self.window,
              justify="center",
              textvariable = self.__cMan,
              ).grid(row=1,column=3,sticky="EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.notdoneyet
               ).grid(row=1,column=4,sticky="EW")

        Button(self.window,
               text = labels["win_man"][self.lang],
               command = self.notdoneyet
               ).grid(row=1,column=6,sticky="EW")

        #row 2
        Label(self.window,
              text = s_elem_def["SPELL"][self.lang]+":",
              ).grid(row=2,column=0,sticky="W")

        self.__lvlSpell = IntVar()
        self.__lvlSpell.set(1)
        Entry(self.window,
              justify="center",
              textvariable = self.__lvlSpell
              ).grid(row=2,column=1,sticky="EW")
        
        Label(self.window,
              text = s_elem_def["COUNT"][self.lang]+":"
              ).grid(row=2,column=2,sticky="EW")
        
        self.__cSpell = IntVar()
        self.__cSpell.set(0)
        Entry(self.window,
              justify="center",
              textvariable = self.__cSpell,
              ).grid(row=2,column=3,sticky="EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.notdoneyet
               ).grid(row=2,column=4,sticky="EW")       

        Button(self.window,
               text = labels["win_casting"][self.lang],
               command = self.notdoneyet
               ).grid(row=2,column=6,sticky="EW")
        #row 3
        Label(self.window,
              text = s_elem_def["HITS"][self.lang]+":",
              ).grid(row=3,column=0,sticky="W")
        
        self.__hits = IntVar()
        self.__hits.set(0)
        Entry(self.window,
              justify="center",
              textvariable = self.__hits,
              ).grid(row=3,column=1,sticky="EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.notdoneyet
               ).grid(row=3,column=4,sticky="EW")

        Button(self.window,
               text = labels["win_fight"][self.lang],
               command = self.notdoneyet
               ).grid(row=3,column=6, rowspan=3,sticky="NEWS")
        
        #row 4
        self.critlist = ['T','A','B','C','D','E']
        Label(self.window,
              text = s_elem_def["H_CRITS"][self.lang]+":",
              ).grid(row=4,column=0,sticky="W")
        self.__gcrit = StringVar()
        self.__gcrit.set("T")
        OptionMenu(self.window,
                    self.__gcrit,
                    *self.critlist,
                    command = self.notdoneyet
                   ).grid(row=4,column=1,sticky="EW")
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.notdoneyet
               ).grid(row=4,column=4,sticky="EW")
        #row 5
        Label(self.window,
              text = s_elem_def["CRITICAL"][self.lang]+":",
              ).grid(row=5,column=0,sticky="W")
        self.__crit = StringVar()
        self.__crit.set("T")
        OptionMenu(self.window,
                    self.__crit,
                    *self.critlist,
                    command = self.notdoneyet
                   ).grid(row=5,column=1,sticky="EW")
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.notdoneyet
               ).grid(row=5,column=4,sticky="EW")
        #row 6
        Label(self.window,
              text = s_elem_def["TRAVEL"][self.lang]+":",
              ).grid(row=6,column=0,sticky="W")

        self.__travel = IntVar()
        self.__travel.set(0)
        Entry(self.window,
              justify="center",
              textvariable = self.__travel,
              ).grid(row=6,column=1,sticky="EW")
        Label(self.window,
              text = labels["comment"][self.lang]+":",
              ).grid(row=6,column=2,sticky="EW")
        
        self.__comtravel = StringVar()
        self.__comtravel.set("")
        Entry(self.window,
              justify="center",
              textvariable = self.__comtravel,
              ).grid(row=6,column=3,sticky="EW")
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.notdoneyet
               ).grid(row=6,column=4,sticky="EW")
        #row 7
        Label(self.window,
              text = s_elem_def["IDEAS"][self.lang]+":",
              ).grid(row=7,column=0,sticky="W")
        
        self.__ideas = IntVar()
        self.__ideas.set(0)
        Entry(self.window,
              justify="center",
              textvariable = self.__ideas,
              ).grid(row=7,column=1,sticky="EW")
        Label(self.window,
              text = labels["comment"][self.lang]+":",
              ).grid(row=7,column=2,sticky="EW")        
        self.__comideas = StringVar()
        self.__comideas.set("")
        Entry(self.window,
              justify="center",
              textvariable = self.__comideas,
              ).grid(row=7,column=3,sticky="EW")
        
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.notdoneyet
               ).grid(row=7,column=4,sticky="EW")

    def __updSelec(self,event):
        """
        Update selected Player data
        """
        selected = self.__selecPlayer.get()
        ind = self.players.index(selected)
        self.__charname.set(self.charlist[ind]["name"])
        self.__charprof.set("{} ({})".format(self.charlist[ind]["prof"],self.group[selected].lvl))
        self.__charexp.set(str(self.charlist[ind]["exp"]))
        self.__gained.set("+{}".format(self.group[self.charlist[ind]["player"]].gainedep))
        self.__newep.set("<{}>".format(self.group[self.charlist[ind]["player"]].gainedep+self.group[self.charlist[ind]["player"]].ep))
        self.__newlvl.set(self.group[self.charlist[ind]["player"]].lvl)
        
        
    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()


with open("epdata.json","r") as fp:
    cl = json.load(fp)

win = EPCalcWin(charlist=cl)
