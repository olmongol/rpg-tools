#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
\file gui/gmtools.py
\package gui
\brief Window classes for GM tools gui

In this module you find the window classes for
\li create a treasure
\li create an single magical item

\date (C) 2017
\author Aiko Ruprecht, Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
#import string

from gui.window import *
from rpgtoolbox.treasure import *
from rpgtoolbox import epcalc, rpgtools as rpg
from rpgToolDefinitions.epcalcdefs import maneuvers
import json



class createTreasureWin(blankWindow):
    """
    This class builds a window for treasure generation.
    \todo createTreasureWin layout could be improved
    """


    def __init__(self, lang = 'en', filename = ''):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param filename Path and name of a file which is displayed as default
        """
        self.lang = lang

        # Create window
        self.ctwin = Tk()

        title1 = Label(self.ctwin, text = txtmenu['menu_opt'][self.lang])
        title1.grid()

        # List of categories
        self.__trlist = Listbox(self.ctwin, height = 0)

        for linetext in trtypelist[self.lang]:
            self.__trlist.insert('end', linetext)

        self.__trlist.grid(pady = 3)
        self.__trlist.select_set(2)

        # Text output field
        self.trcontent = ''
        self.__trtext = Text(self.ctwin, height = 10, width = 47, wrap = NONE)
        self.__trtext.insert(END, submenu['items'][self.lang]['itemgen'].strip())
        self.__trtext['bg'] = '#FFFFFF'
        self.__trtext['relief'] = 'groove'
        vs = Scrollbar(self.ctwin, orient = "vertical", command = self.__trtext.yview)
        self.__trtext.config(yscrollcommand = vs.set)
        hs = Scrollbar(self.ctwin, orient = "horizontal", command = self.__trtext.xview)
        self.__trtext.config(xscrollcommand = hs.set)
        self.__trtext.grid(row = 2, sticky = E + W + N + S)
        vs.grid(row = 2, column = 1, sticky = S + N + E)
        hs.grid(sticky = W + E)

        # Button to create a text describing the treasure
        self.__trcreate = Button(self.ctwin, text = submenu['items'][self.lang]['treasure'],
                               command = self.__trcreate)
        self.__trcreate.grid()

        # Label for the saving the text
        self.__entrylabel = Label(self.ctwin, text = '\n' + txtmenu['menu_file'][self.lang])
        self.__entrylabel.grid()

        # Entry field to enter the file path
        self.__filename = Entry(self.ctwin)
        #self.__filename['width'] = 69
        self.__filename['borderwidth'] = 3
        self.__filename.grid(sticky = E + W)
        self.__filename.insert(1, filename)

        # Button to save the text
        self.__bsave = Button(self.ctwin, text = txtbutton['but_sav'][self.lang],
                              command = self.__trsave)
        self.__bsave.grid(sticky = W)

        # Button to close the window
        self.__bquit = Button(self.ctwin, text = txtbutton['but_quit'][self.lang],
                               command = self.__quit)
        self.__bquit.grid()

        # make the canvas expandable
        self.ctwin.grid_rowconfigure(2, weight = 1)
        self.ctwin.grid_columnconfigure(0, weight = 1)


    def __trcreate(self):
        '''
        This private method creates and displays the text describing the treasure
        '''
        # Create Text
        trtype = self.__trlist.curselection()[0] + 1
        items = treasure()
        self.trcontent = items.findTreasure(trtype, output = '')
        trtext = self.trcontent
#        trtext = string.join(trtext, '\n')
        outtext = u''

        for i in range(0, len(trtext)):
            outtext += trtext[i] + u"\n"
#            trtext[i] = trtext[i].encode("utf-8")

        # Display text
        self.__trtext.delete('1.0', END)
        self.__trtext.insert(END, outtext + u'\n')

        # Tidy up
        del items
        del trtext


    def __trsave(self):
        '''
        This private method will save the text describing the treasure
        '''
        outputfile = self.__filename.get()

        if outputfile != '':
            # Create text
            trtext = self.__trtext.get('1.0', END)
            trtext = trtext.encode('utf8')

            try:
                # Write file
                fp = open(outputfile, "w")
                fp.write(trtext)
                fp.close()
                print((screenmesg['file_saved'][self.lang][:-1] + ': ' + outputfile))

                # Reset output frame
                self.__trtext.delete('1.0', END)
                self.__trtext.insert (END, submenu['items'][self.lang]['itemgen'])
                self.trcontent = ''

            except:
                print('Error: Invalid file name')
                print(outputfile)


    def __quit(self):
        '''
        This private method closes the createTreasreWin window
        '''
        self.ctwin.destroy()



class createMagicWin(blankWindow):
    """
    This class creates a window for the generation of magical items. The output text can be edited and copied.
    \todo createMagicWin window layout could be improved
    """


    def __init__(self, lang = 'en'):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        """
        self.lang = lang

        # Create window
        self.cmwin = Tk()

        # Frame for the text output
        self.__output = Entry(self.cmwin)
        self.__output['width'] = 60
        self.__output['borderwidth'] = 3
        self.__output['bg'] = '#FFFFFF'
        self.__output['relief'] = 'groove'
        self.__output.grid(sticky = W + E)
        self.__output.insert(1, submenu['items'][self.lang]['magicgen'])
        self.itemtext = ''
        hs = Scrollbar(self.cmwin, orient = "horizontal", command = self.__output.xview)
        self.__output.config(xscrollcommand = hs.set)
        hs.grid(sticky = E + W)

        # Button to create treasure descriptions
        self.__bcreate = Button(self.cmwin, text = submenu['items'][self.lang]['magical'],
                               command = self.__cmcreate)
        self.__bcreate.grid()

        # Button to close window
        self.__bquit = Button(self.cmwin, text = txtbutton['but_quit'][self.lang],
                               command = self.__quit)
        self.__bquit.grid()

        # make the canvas expandable
        self.cmwin.grid_rowconfigure(0, weight = 1)
        self.cmwin.grid_columnconfigure(0, weight = 1)


    def __cmcreate(self):
        '''
        This private method creates and displays the text describing the magical item
        '''
        # Create text
        item = treasure()
        self.itemtext = item.magicItem()

        # Print text into output frame
        endpos = len(self.__output.get())

        if endpos > 1:
            self.__output.delete(1, endpos - 1)

        self.__output.insert(1, self.itemtext)
        self.__output.icursor(1)

        # Tidy up
        del item


    def __quit(self):
        '''
        This private method closes the createTreasreWin window
        '''
        self.cmwin.destroy()



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
               command = self.__finalize,
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


    def __finalize(self):
        '''
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

        gw = showGrpEP(self.charlist, self.storepath, self.lang)


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()



class showGrpEP(object):
    '''
    Display and save window for group EPs
    '''


    def __init__(self, charlist = [], storepath = "./data", lang = 'en'):
        """
        Constructor
        \param lang contains the chosen display language.
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
        '''
        This method saves all data in character files
        @todo this has to be fully implemented
        '''
        print("not done yet")
        pass


    def saveGroup(self):
        '''
        Saves all data in a groupfile
        '''
        if self.storepath[-1] != "/":
            self.storepath += "/"

        with open(self.storepath + "EPGroup.json", "w") as fp:
            json.dump(self.charlist, fp, indent = 4)
