#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''!
@file epwins.py
@package gui.epwins
@brief Windows classes for epcalc gui

This holds window classes for generating and updating (level ups) characters.
@date (C) 2016-2020
@author Marcus Schwamberger
@email marcus@lederzeug.de
@version 1.5

----
@todo The following has to be implemented:
- a separate Character Status Window which shows the following:
 -# name, culture, race, profession
 -# old & new EPs
 -# No of level-ups
 -# remaining DPs
 -# remaining stat gain rolls

'''
import random
import os
import sys
import json
from tkinter import *
#from PIL import Image, ImageTk
from tkinter.filedialog import *
from tkinter.ttk import *
from rpgtoolbox.lang import *
from rpgtoolbox.globaltools import *
from rpgtoolbox import logbox as log
from rpgtoolbox import handlemagic
from rpgtoolbox.errbox import *
from rpgtoolbox.confbox import *
from rpgtoolbox.rpgtools import getLvl
from rpgtoolbox.rolemaster import stats
from rpgtoolbox.rpgtools import calcTotals
from gui.winhelper import AutoScrollbar
from gui.winhelper import InfoCanvas
from gui.window import *
from gui.gmtools import *
from gui.mangroup import *
from pprint import pprint  # for debugging purposes only

__updated__ = "28.12.2020"

__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015-" + __updated__[-4:] + " " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "1.5"
__license__ = "GNU V3.0"
__me__ = "A RPG tool package for Python 3.6"

logger = log.createLogger('window', 'debug', '1 MB', 1, './')



class MainWindow(blankWindow):
    """!
    This is the class for the main window object.
    @param lang The chosen language for window's and button's texts. At
                the moment, only English (en, default value) and German
                (de) are supported.
    @param title title of the window
    @param storepath path where things like options have to be stored
    @todo storepath has to be changed to default installation path empty
    """


    def __init__(self, lang = 'en', storepath = None, title = "Main Window",
                 char = None):
        """
        Class constructor
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param title title of the window
        @param storepath path where things like options have to be stored
        @param char Character as JSON
        """
        if storepath == None:
            #needs to be changed
#            self.mypath = os.path.expanduser('~')
            self.mypath = os.getcwd() + "/data/"
            logger.debug('mainwindow: Set storepath to %s' % (storepath))

        else:
            self.mypath = storepath
            logger.debug('mainwindow: storepath set to %s' % (storepath))

        self.picpath = "./gui/pic/"
        self.lang = lang
        self.myfile = "MyRPG.exp"
        self.char = char

        blankWindow.__init__(self, self.lang)
        self.window.title(title)
        Label(self.window, width = 60).pack()
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addGMMenu()
        self.__addOptionMenu()
        self.__addHelpMenu()

        self.mask = [txtwin['json_files'][self.lang],
                     txtwin['grp_files'][self.lang],
                     txtwin['all_files'][self.lang]
                     ]

        """
        set picture for the window background of the main window
        """
        self.__canvas = Canvas(self.window, width = '11.0c', height = '13.0c')
        __background = PhotoImage(file = self.picpath + 'demon.gif')
        self.__canvas.create_image(0, 0, image = __background, anchor = NW)
        self.__canvas.pack()

        self.window.mainloop()


    def __addFileMenu(self):
        """
        This method adds a File menu to the windows menu bar.
        """
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['new'],
                                  command = self.__newFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__openFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__saveFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['sv_as'],
                                  command = self.__saveFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['export'] + "(LaTeX/PDF)",
                                  command = self.__exportLaTeX)
        self.filemenu.add_command(label = "{} {} {}".format("short format",
                                                            submenu['file'][self.lang]['export'],
                                                            "(LaTeX/PDF)"),
                                  command = self.__exportShortLaTeX)
        self.filemenu.add_command(label = "{} {} {}".format(labels["spellbook"][self.lang],
                                                            submenu['file'][self.lang]['export'],
                                                            "(LaTeX/PDF)"),
                                  command = self.__exportSpellbook)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['quit'],
                                  command = self.window.destroy)


    def __newFile(self):
        """
        This method opens a new window for generation of a new
        functional structure.
        """
        self.window.destroy()
        logger.debug("newfile: %s " % (self.mypath))
        self.window = inputWin(lang = self.lang,
                               filename = None,
                               storepath = self.mypath)


    def __openFile(self):
        """
        This method opens a dialogue window (Tk) for opening files.
        The content of the opened file will be saved in \e file
        \e content as an array.
        """
        self.__filein = askopenfilename(filetypes = self.mask,
                                        initialdir = self.mypath)
        if self.__filein != "" and type(self.__filein) == type(""):
            with open(self.__filein, 'r') as filecontent:

                if self.__filein[-4:].lower() == "json":
                    self.char = json.load(filecontent)

                elif self.__filein[-3:].lower == "grp":
                    self.grp = json.load(filecontent)

                else:
                    msg = messageWindow()
                    msg.showinfo(errmsg['wrong_type'][self.lang])
                    logger.warn(errmsg['wrong_type'][self.lang])
                    pass


    def __saveFile(self):
        '''!
        This method opens a file dialogue window (Tk) for saving the results
        of the EP calculation into an .json or .grp file.
        @todo has to be implemented
        '''
        self.notdoneyet("'saveFile'")


    def __exportLaTeX(self):
        '''
        This method exports character data into a LaTeX file from which a PDF
        will be generated
        '''
        from rpgtoolbox import latexexport

        if self.char == None:
            msg = messageWindow()
            msg.showinfo(errmsg['no_data'][self.lang])

        else:
            export = latexexport.charsheet(self.char, "./data/", short = False)
            msg = messageWindow()
            msg.showinfo("LaTeX generated")


    def __exportShortLaTeX(self):
        '''
        This method exports character data into a LaTeX file from which a PDF
        will be generated
        '''
        from rpgtoolbox import latexexport

        if self.char == None:
            msg = messageWindow()
            msg.showinfo(errmsg['no_data'][self.lang])

        else:
            export = latexexport.charsheet(self.char, "./data/", short = True)
            msg = messageWindow()
            msg.showinfo("short LaTeX generated")  #


    def __exportSpellbook(self):
        '''
        This generates a Spellbook PDF out aof character's data
        '''
        from rpgtoolbox.latexexport import spellbook
        if self.char == None:
            msg = messageWindow()
            msg.showinfo(errmsg['no_data'][self.lang])

        else:
            spellbook(self.char, self.mypath)
            msg = messageWindow()
            msg.showinfo("Spellbook generated")


    def __addEditMenu(self):
        '''
        This method adds an edit menu to the menu bar
        '''
        self.edtmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_edit'][self.lang],
                              menu = self.edtmenu)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_char'],
                                 command = self.__edcharWin)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['char_back'],
                                 command = self.__bckgrndWin)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['statgain'],
                                 command = self.__statGainRoll)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_BGO'],
                                 command = self.__BGOWin)
        self.edtmenu.add_separator()
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_EP'],
                                 command = self.__edtEPWin)
        self.edtmenu.add_separator()
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_fight'],
                                 command = self.__edfightWin)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_grp'],
                                 command = self.__edtgrpWin)
#        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_indiv'],
#                                 command = self.__indivWin)
#        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_calc'],
#                                 command = self.__edcalcWin)


    def __edcharWin(self):
        '''
        Generating a window for editing Characters/Character lists/Parties
        '''
        if self.char != None:
            self.window.destroy()
            self.window2 = skillcatWin(self.lang, self.mypath, self.char)

        else:
            msg = messageWindow()
            msg.showinfo(errmsg['no_data'][self.lang])


    def __edtgrpWin(self):
        """
        Opens a window for editing character parties
        """
        grpwin = groupWin(self.lang)


    def __BGOWin(self):
        '''!
        Opens a window to enter and store new EPs in character data
        @todo edtEPWin has to be fully implemented
        '''
        self.notdoneyet("BGOWin")


    def __edtEPWin(self):
        '''
        Opens a window to enter and store new EPs in character data
        '''
        if self.char != None:
            self.window.destroy()
            self.window2 = editEPWin(self.lang, self.mypath, self.char)

        else:
            msg = messageWindow()
            msg.showinfo(errmsg['no_data'][self.lang])


    def __edfightWin(self):
        '''!
        Editing all Hits/Crits/Killed Monsters for calculating EPs
        @todo has to be implemented
        '''
        self.notdoneyet()


    def __edcalcWin(self):
        '''!
        Calculating and displaying the whole EPs for the RPG party.
        @todo not implemented yet
        '''
        self.notdoneyet()


    def __statGainRoll(self):
        '''
        This opens a window for Stats Gain Roll for the character.
        '''
        self.window.destroy()

        self.window2 = statGainWin(lang = self.lang, storepath = self.mypath, char = self.char)


    def __addGMMenu(self):
        """
        This method adds a Gamemaster Menu for generating special stuff like
        treasures or magical items.
        """
        self.gmmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_gm'][self.lang],
                              menu = self.gmmenu)
        self.gmmenu.add_command(label = submenu['items'][self.lang]['treasure'],
                                command = self.__treasureWin)
        self.gmmenu.add_command(label = submenu['items'][self.lang]['magical'],
                                command = self.__magicWin)
        logger.debug("GM Menu build...")


    def __treasureWin(self):
        """
        This privat method invokes a window to generate descriptions of a treasures (gmtools.py).
        """
        createTreasureWin(lang = self.lang, filename = 'treasure.txt')


    def __magicWin(self):
        """
        This privat method invokes a window to generate descriptions of magic items (gmtools.py).
        """
        createMagicWin(lang = self.lang)


    def __addOptionMenu(self):
        """
        This method adds an option/preferences menu to the menu bar.
        """
        self.optmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_opt'][self.lang],
                              menu = self.optmenu)
        self.optmenu.add_command(label = submenu['opts'][self.lang]['lang'],
                                 command = self.__optWin)


    def __optWin(self):
        '''
        Opens an options window and closes the main window.
        '''
        self.window.destroy()
        self.window = confWindow(self.lang)


    def __addMenu(self):
        '''
        This private method just adds the menu bar into the window's
        layout
        '''
        self.menu = Menu(self.window)
        self.window.configure(menu = self.menu)


    def __addHelpMenu(self):
        """
        This methods defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['global'],
                                  command = self.helpHandbook)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self.helpAbout)


    def __bckgrndWin(self):
        '''
        This opens the background window of a loaded character
        '''
        if self.char != None:
            self.window.destroy()
            self.window2 = charInfo(self.lang, self.mypath, self.char)
        else:
            msg = messageWindow()
            msg.showinfo(errmsg['no_data'][self.lang])


    def helpHandbook(self):
        """!
        This method will show the rpg-tools Handbook
        @todo this needs to be implemented
        """
        self.notdoneyet()


    def helpAbout(self):
        '''
        This method just opens a message window with the basic
        information about the PROGRAM (like version and
        copyright)
        '''
        self.about = "%s\nVersion %s\n\n%s\n%s\n%s" % (__me__,
                                                       __version__,
                                                       __copyright__,
                                                       __license__,
                                                       __email__)
        self.msg = messageWindow()
        self.msg.showinfo(self.about)



class confWindow(blankWindow):
    """!
    This class builds a window for selecting and saving options of
    rpg-tools. For now it is just choosing the language for menus and
    dialogues.
    @param lang Laguage which shall be used in messages and menus.

    ----
    @todo The following has to be implemented:
    - improve design of options window

    """


    def __init__(self, lang = 'en'):
        """
        Class constructor
        @param lang Laguage which shall be used in messages and menus
        """
        self.lang = lang
        self._cnf = chkCfg(lang = self.lang)
        logger.debug("read cfg data: {}".format(self._cnf.cnfparam))
        blankWindow.__init__(self, self.lang)
        self.window.title(wintitle['opt_lang'][self.lang])
        self.wert = StringVar()
        self.index = sortIndex(shortcut)
        self.__buildOptMenu()
        self.__buildWinRadio()


    def __buildOptMenu(self):
        """
        This private method builds an option menu button in the option's window
        to make a choice between the used supported RPGs.
        """
        self.RPG = StringVar()
        if 'rpg' in list(self._cnf.cnfparam.keys()):
            self.RPG.set(self._cnf.cnfparam['rpg'])
        else:
            self.RPG.set('Rolemaster')

        self.optMenu = OptionMenu(*(self.window, self.RPG) + tuple(supportedrpg[self.lang]))
        self.optMenu.grid(column = 0, row = 0)


    def __buildWinRadio(self):
        """!
        This private method builds the option's window with radio
        buttons of supported languages dynamically.
        @todo switch language chooser from radio buttons to pull-down
              menu
        """
        self.sto_path = StringVar()
        self.log_path = StringVar()

        if 'datapath' in list(self._cnf.cnfparam.keys()):
            self.sto_path.set(self._cnf.cnfparam['datapath'])

        else:

            self.sto_path.set(str(str(os.getcwd())) + "/data")

        if 'lang' in list(self._cnf.cnfparam.keys()):

            if self._cnf.cnfparam['lang'] != self.lang:
                self.lang = self._cnf.cnfparam['lang']

        if 'logpath' in list(self._cnf.cnfparam.keys()):
            self.log_path.set(self._cnf.cnfparam['logpath'])

        else:
            self.log_path.set("./")

        self.rb = {}
        i = 1

        for key in self.index:
            self.rb[key] = Radiobutton(master = self.window,
                                       text = shortcut[key],
                                       variable = self.wert,
                                       value = key
                                       )

            if key == self.lang:
                self.rb[key].select()

            self.rb[key].grid(column = 0, row = i)
            i += 1

        i += 1
        Label(master = self.window,
              width = 35
              ).grid(column = 0, row = i)

        i += 1
        Label(master = self.window,
              width = 35,
              text = labels['cfg_path'][self.lang]
              ).grid(column = 0, row = i)

        i += 1
        Entry(master = self.window,
              width = 35,
              textvariable = self.sto_path
              ).grid(column = 0, row = i)

        i += 1
        Label(master = self.window,
              width = 35
              ).grid(column = 0, row = i)

        i += 1
        Label(master = self.window,
              width = 35,
              text = labels['log_path'][self.lang]
              ).grid(column = 0, row = i)
        i += 1
        Entry(master = self.window,
              width = 35,
              textvariable = self.log_path
              ).grid(column = 0, row = i)

        i += 1
        Button(self.window,
               text = txtbutton['but_sav'][self.lang],
               width = 15,
               command = self.__save).grid(column = 0, row = i)
        i += 1
        Button(self.window,
               text = txtbutton['but_clos'][self.lang],
               width = 15,
               command = self.__closewin).grid(column = 0, row = i)


    def chosenLang(self):
        """
        A public method which return the string value of the chosen
        language.
        """
        return self.wert.get()


    def __save(self):
        """!
        A method for saving options in the user directory.
        @todo variables to store have to be completed/adapted
        """
        self.lang = self.wert.get()
        self.path = self.sto_path.get()
        self.log = self.log_path.get()
        self.crpg = self.RPG.get()

        if self.path[-1:] != '/':
            self.path += '/'

        if self.log[-1:] != '/':
            self.log += '/'

        self.cont = {'lang': self.lang,
                     'datapath': self.path,
                     'logpath': self.log,
                     'rpg': self.crpg
                     }
        logger.debug('SAVE: lang=%s; datapath=%s; logpath=%s' %
                     (self.lang, self.path, self.log))
        self._cnf.saveCnf(path = './conf',
                          filename = 'rpg-tools.cfg',
                          content = self.cont)

        self._cnf = chkCfg(lang = self.lang)
        logger.debug("saved cfg: {}".format(self._cnf.cnfparam))
        self.msg = messageWindow()
        self.msg.showinfo(processing['saved']
                          [self.lang] + '\n' + shortcut[self.lang])


    def __closewin(self):
        """!
        A method for closing the window and opening the main window.
        @todo give RPG type to main window
        """
        self.path = self.sto_path.get()
        self.window.destroy()
        self.window = MainWindow(self.lang, self.path)



class inputWin(blankWindow):
    """!
    Objects of this class type are windows for input the wanted data
    structure. A exp structure will be build of the input.
    @param lang This parameter holds the language chosen for the menus
                and messages. Default value is 'en'.
    @param filename this holds the filename of a read exp file holding
                    the functional structure.
    @param storepath the path where the XML files shall be stored in.
    """


    def __init__(self,
                 lang = 'en',
                 csvcontent = {},
                 filename = None,
                 storepath = None):
        """
        Constructor!
        @param lang This parameter holds the language chosen for the
                    menus and messages. Default value is 'en'
        @param csvcontent a dictionary holding the information of CSV
        @param filename this holds the filename and path of a read data
                        file containing the functional structure.
        @param storepath the path where the data files shall be stored
                         in.
        """
        self.lang = lang
        self.csvcont = csvcontent
        self.fname = filename
        self.picpath = "./gui/pic/"

        if self.fname != "" and self.fname != None:
            self._last = getLast(string = self.fname, sep = "/")

        else:
            self._last = ""

        self.mypath = storepath
        blankWindow.__init__(self, self.lang)

        self.window.title(wintitle['edit'][self.lang] + " - " + self._last)

        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['new_char'],
                                  command = self.__createchar)
        self.filemenu.add_command(label = submenu['file'][self.lang]['new_grp'],
                                  command = self.__creategroup)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)

        self.edtmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_edit'][self.lang],
                              menu = self.edtmenu)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_char'],
                                 command = self.__editchar)
        self.edtmenu.add_separator()
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_fight'],
                                 command = self.__epfight)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_other'],
                                 command = self.__epother)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_indiv'],
                                 command = self.__epindiv)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_calc'],
                                 command = self.__epcalc)
        self.edtmenu.add_separator()
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_sim'],
                                 command = self.__fightsim)

        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['page'],
                                  command = self.__helppage)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['global'],
                                  command = self.__helpglobal)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)

        """
        set picture for the window background of the main window
        """
        self.__canvas = Canvas(self.window, width = '11.5c', height = '13.5c')
        __background = PhotoImage(file = self.picpath + 'assassin.gif')
        self.__canvas.create_image(0, 0, image = __background, anchor = NW)
        self.__canvas.pack()

        self.window.mainloop()


    def __createchar(self):
        '''
        Method to open a new window for character creation.
        '''
        self.window.destroy()
        self.window3 = genAttrWin(lang = self.lang,
                                  storepath = self.mypath)


    def __creategroup(self):
        '''!
        Method to create a now character party/group
        @todo chreategroup has to be implemented
        '''
        print("input win --> creategroup")
        self.notdoneyet('creategroup')


    def __editchar(self):
        '''!
        Method to edit a character for the EP sheet.
        @todo editchar is to be implemented
        '''
        print("input win -->  editchar")
        self.notdoneyet('editchar')


    def __editgrp(self):
        '''!
        Method to edit a character group and keep track on it
        @todo editgrp has to be implemented
        '''
        self.notdoneyet("editgrp")


    def __epfight(self):
        '''!
        Method to calculate EPs from a fight (hits and criticals)
        @todo epfight has to be implemented
        '''
        self.notdoneyet('epfight')


    def __epother(self):
        '''!
        Method to calculate EPs from Spells, maneuvers, travel.
        @todo epother has to be implemented
        '''
        self.notdoneyet('epother')


    def __epindiv(self):
        '''!
        Method for adding invidual EPs
        @todo epindiv has to be implemented
        '''
        self.notdoneyet('epindiv')


    def __epcalc(self):
        '''!
        Method to finalize EP calculation for a single gaming date
        @todo epcalc has to be implemented
        '''
        self.notdoneyet('epcalc')


    def __fightsim(self):
        '''!
        Method for simulating a fight and calculate potential EPs
        @todo fightsim has to be implemented
        '''
        self.notdoneyet('fightsim')


    def __closewin(self):
        """
        Method for closing the window and opening the main window.
        """
        self.window.destroy()
        self.window = MainWindow(self.lang, self.mypath)


    def __helppage(self):
        """!
        Method for help on this page.
        @todo helppage has to be implemented
        """
        self.notdoneyet("helppage")


    def __helpglobal(self):
        """
        Method to call the handbook as help for this page
        """
        self.handbook("chapter %s" % (wintitle['edit'][self.lang]))



class genAttrWin(blankWindow):
    '''
    A window class for generating name, race, profession and attributes of a new
    character.
    '''


    def __init__(self, lang = 'en', storepath = './data', rpg = "RoleMaster"):
        '''!
        @param lang Choosen display language (default en)
        @param storepath Path to store data (default: ./data)
        '''

        if rpg == "RoleMaster":
            from rpgtoolbox import rolemaster as rm

        else:
            self.notdoneyet("support for %s" % (rpg))

        # @var self.character
        # the attribute where to store the character data in as 'JSON'
        self.character = {}
        # @var self.lang
        # used language
        self.lang = lang
        # @var self.spath
        # storage path for character data file
        self.spath = storepath

        if self.spath[-1] != "/":
            self.spath += "/"

        self.__cultures = rm.cultures[self.lang][:6]
        # @var self.profs
        # a dictionary/JSON structure where a profession specific data (read from
        # a CSV file) is stored in
        self.profs = rm.choseProfession(self.lang)
        # @var proflist
        # list of all available professions
        proflist = list(self.profs.keys())
        # @var rmraces
        # a list of all the RoleMaster races
        rmraces = rm.races[self.lang]
        # @var rmcultures
        # list of available cultures
        rmcultures = rm.cultures[self.lang]
        # @var self.stats
        # holds player, name, profession, race, realm and temp stats
        self.stats = {}
        # @var self.pots
        # holds potential stats (maximum values)
        self.pots = {}
        # @var self.specs
        # holds special stats if anyrger
        self.specs = {}
        # @var self.__race
        # holds race stats bonuses
        self.__race = {}
        # @var self.__rr
        # holds all resistance roll bonusses
        self.__rr = {}
        self.__labels = {}
        # @var self..__totals
        # holds total stat bonusses
        self.__totals = {}
        # @var self.__std
        #  holds standard stat bonusses
        self.__std = {}
        self.__count = 0
        # @var self.__rmstats
        # list of all stats' short cuts in English
        self.__rmstats = rm.stats
        # @var self.__rangeOK
        # just for check up whether the stats are in the correct ranges
        self.__rangeOK = True

        blankWindow.__init__(self, lang = self.lang)
        self.window.title(wintitle['rm_charg'][self.lang] + " - Attributes")
        self.showno = IntVar()
        self.showno.set(660)
        self.points = 660
        dummy = ['player', 'name', 'prof', 'race', 'realm', 'culture']

        for a in dummy:
            self.stats[a] = StringVar()

        for a in rm.stats:
            self.stats[a] = IntVar()
            self.stats[a].set(0)
            self.pots[a] = IntVar()
            self.pots[a].set(0)
            self.specs[a] = IntVar()
            self.specs[a].set(0)
            self.__labels[a] = StringVar()
            self.__labels[a].set(rm.labels[self.lang][a])
            self.__race[a] = IntVar()
            self.__race[a].set(0)
            self.__std[a] = IntVar()
            self.__std[a].set(0)
            self.__totals[a] = IntVar()
            self.__totals[a].set(0)

        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.notdoneyet)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)
        self.__addHelpMenu()

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)

        Label(master = self.window,
              width = 25,
              text = rm.labels[self.lang]['player']
              ).grid(column = 0, row = 0, columnspan = 2)

        Entry(master = self.window,
              width = 35,
              textvariable = self.stats['player'],
              ).grid(column = 2, row = 0, columnspan = 2)

        Label(master = self.window,
              width = 15,
              text = rm.labels[self.lang]['culture']
              ).grid(column = 4, row = 0, columnspan = 2)

        self.optMenu0 = OptionMenu(self.window,
                                   self.stats['culture'],
                                   *rmcultures,
                                   command = self.__setCulture)
        self.optMenu0.grid(column = 6, row = 0, columnspan = 2, sticky = "ew")

        Label(master = self.window,
              width = 25,
              text = rm.labels[self.lang]['name']
              ).grid(column = 0, row = 1, columnspan = 2)

        Entry(master = self.window,
              width = 35,
              textvariable = self.stats['name'],
              ).grid(column = 2, row = 1, columnspan = 2)

        Label(master = self.window,
              width = 15,
              text = rm.labels[self.lang]['race']
              ).grid(column = 4, row = 1, columnspan = 2)

        self.optMenu1 = OptionMenu(self.window,
                                   self.stats['race'],
                                   *rmraces,
                                   command = self.__setRBonus)
        self.optMenu1.grid(column = 6, row = 1, columnspan = 2, sticky = "ew")

        Label(master = self.window,
              width = 25,
              text = rm.labels[self.lang]['prof']
              ).grid(column = 0, row = 2, columnspan = 2)

        self.optMenu2 = OptionMenu(self.window,
                                   self.stats['prof'],
                                   *proflist,
                                   command = self.__setRealm)
        self.optMenu2.grid(column = 2, row = 2, columnspan = 2, sticky = "ew")

        Label(master = self.window,
              width = 15,
              text = rm.labels[self.lang]['realm']
              ).grid(column = 4, row = 2, columnspan = 2)

        self.optMenu3 = OptionMenu(self.window,
                                   self.stats['realm'],
                                   *rm.realms[self.lang],
                                   command = self.__chkRealm)
        self.optMenu3.grid(column = 6, row = 2, columnspan = 2, sticky = "ew")

        Button(master = self.window,
               text = txtbutton['but_roll'][self.lang],
               width = 15,
               command = self.rollDice).grid(column = 4, row = 3)

        Label(master = self.window,
              text = rm.labels[self.lang]['DP'],
              ).grid(column = 5, row = 3, columnspan = 2)

        Message(master = self.window,
                width = 35,
                textvariable = self.showno,
                font = "bold"
                ).grid(column = 7, row = 3)

        Label(master = self.window,
              width = 15,
              relief = RIDGE,
              font = "bold",
              text = rm.labels[self.lang]['stats']
              ).grid(column = 0, row = 4, sticky = "ew")

        Label(master = self.window,
              width = 10,
              relief = RIDGE,
              font = "bold",
              text = rm.labels[self.lang]['short']
              ).grid(column = 1, row = 4)

        Label(master = self.window,
              width = 10,
              relief = RIDGE,
              font = "bold",
              text = "Temp"
              ).grid(column = 2, row = 4, sticky = "ew")

        Label(master = self.window,
              width = 10,
              relief = RIDGE,
              font = "bold",
              text = "Pot"
              ).grid(column = 3, row = 4, sticky = "ew")

        Label(master = self.window,
              width = 10,
              relief = RIDGE,
              font = "bold",
              text = rm.labels[self.lang]['race']
              ).grid(column = 4, row = 4, sticky = "ew")

        Label(master = self.window,
              width = 10,
              relief = RIDGE,
              font = "bold",
              text = "Spec"
              ).grid(column = 5, row = 4, sticky = "ew")

        Label(master = self.window,
              width = 10,
              relief = RIDGE,
              font = "bold",
              text = "Std"
              ).grid(column = 6, row = 4, sticky = "ew")

        Label(master = self.window,
              width = 10,
              relief = RIDGE,
              font = "bold",
              text = rm.labels[self.lang]['total']
              ).grid(column = 7, row = 4, sticky = "ew")

        i = 5

        for s in rm.stats:
            Label(master = self.window,
                  width = 15,
                  textvariable = self.__labels[s]
                  ).grid(column = 0, row = i, sticky = "ew")

            Label(master = self.window,
                  text = s  # momentary only English shortcuts
                  ).grid(column = 1, row = i, sticky = "ew")

            Entry(master = self.window,
                  width = 15,
                  textvariable = self.stats[s]
                  ).grid(column = 2, row = i)

            Message(master = self.window,
                    width = 25,
                    textvariable = self.pots[s],
                    ).grid(column = 3, row = i)

            Message(master = self.window,
                    width = 15,
                    textvariable = self.__race[s],
                    ).grid(column = 4, row = i)

            Entry(master = self.window,
                  width = 15,
                  textvariable = self.specs[s]
                  ).grid(column = 5, row = i)

            Message(master = self.window,
                    width = 25,
                    textvariable = self.__std[s],
                    ).grid(column = 6, row = i)

            Message(master = self.window,
                    width = 25,
                    font = "bold",
                    textvariable = self.__totals[s],
                    ).grid(column = 7, row = i)

            i += 1

        Button(master = self.window,
               text = txtbutton['but_calc'][self.lang],
               width = 15,
               command = self.__calcBonus).grid(column = 0, row = i)

        Button(master = self.window,
               text = txtbutton['but_next'][self.lang],
               width = 10,
               command = self.__nextStep).grid(column = 7, row = i)

        self.window.mainloop()


    def __addHelpMenu(self):
        """!
        This methods defines a help menu.
        @todo The following has to be implemented:
        - global help information (function)
        - window help information
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['win'],
                                  command = self.__winHelp)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['global'],
                                  command = self.notdoneyet)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __winHelp(self):
        '''
        This displays a window speciffic helper message box
        '''
        messageWindow(self.lang).showinfo(winhelpmsg["genAttrWin"][self.lang], "getnAttrWin")


    def __nextStep(self):
        '''
        Checks whether all developing points (and not more) are used and player
        and character names are set. If so it proceeds with collecting all data.
        '''
        if self.points != self.__used:
            messageWindow(self.lang).showinfo(errmsg['stats_dp'][self.lang])

        elif self.stats['player'].get() == "":
            messageWindow(self.lang).showinfo(errmsg['player'][self.lang])

        elif self.stats['name'].get() == "":
            messageWindow(self.lang).showinfo(errmsg['name'][self.lang])

        else:
            self.__collectData()


    def __calcBonus(self):
        '''
        Totals and update all bonusses. If that sum is higher than the developing
        points for the stats it raises an error message window.
        '''
        self.__statBonus()
        self.__used = 0

        for s in self.__rmstats:
            total = self.__race[s].get() + \
                self.specs[s].get() + self.__std[s].get()
            self.__totals[s].set(total)
            stat = self.stats[s].get()
            self.__used += stat
            self.pots[s].set(self.__creatPot(stat))

        if self.__used > self.points:
            self.showno.set(self.points - self.__used)
            messageWindow(self.lang).showinfo(
                errmsg['too_much_stats'][self.lang])

        self.showno.set(self.points - self.__used)
        self.__testStats()


    def __testStats(self):
        '''
        This checks the temp value of the  stats and warns if they are correct.
        That means the primary have to be at least 90+ and the others not below
        20.
        '''
        testp = self.stats['prof'].get()
        if testp != "":
            primestats = self.profs[testp]['Prime Stats']
            self.__rangeOK = True

            for s in self.__rmstats:
                if self.stats[s.strip('*')].get() < 20:
                    self.__rangeOK = False
                    self.stats[s.strip('*')].set(20)
                    messageWindow(self.lang).showinfo(
                        errmsg['wrong_stat'][self.lang] + "\n%s --> 20" % s)

            for s in primestats:

                if self.stats[s.strip('*')].get() < 90:
                    self.__rangeOK = False
                    self.stats[s.strip('*')].set(90)
                    messageWindow(self.lang).showinfo(
                        errmsg['wrong_stat'][self.lang] + "\ns %s --> 90 " % s)


    def __setPStats(self):
        '''!
        Sets the primary (and magic) stats for a profession
        @todo set the magic stat for chosen realms to semi spell users
        '''
        testp = self.stats['prof'].get()

        if testp != "":
            primestats = self.profs[testp]['Prime Stats']

            for s in self.__rmstats:
                dummy = self.__labels[s].get()
                dummy = dummy.strip(" ()+*")

                if s in primestats:
                    self.__labels[s].set(dummy + ' (+)')

                    if self.stats[s].get() < 90:
                        self.stats[s].set(90)

                elif s + '*' in primestats:
                    self.__labels[s].set(dummy + ' (+)(*)')

                    if self.stats[s].get() < 90:
                        self.stats[s].set(90)

                else:
                    self.__labels[s].set(dummy)

                    if self.stats[s].get() < 20:
                        self.stats[s].set(20)

                potstat = self.__creatPot(self.stats[s].get())
                self.pots[s].set(potstat)

        self.__calcBonus()


    def __setCulture(self, event):
        '''
        Sets the right culture selection dependent on the chosen race.
        If the race is set this method will adapt the list of choice concerning
        to the chosen race.

        ----

        @todo -# set the initial language ranks for the culture based languages
              -# add the additional cultured from MERP

        '''
        from rpgtoolbox.rolemaster import races, cultures
        from rpgtoolbox.lang import errmsg

        testc = self.stats['culture'].get()
        testr = self.stats['race'].get()
        omenu = self.optMenu0.children['menu']
        omenu.delete(0, "end")

        if testr == "" or testr == None:
            msg = messageWindow()
            msg.showinfo(errmsg['no_race'][self.lang], 'Info')

        elif testr in races[self.lang][:2]:
            for cult in cultures[self.lang][:6]:
                omenu.add_command(
                    label = cult, command = lambda v = cult: self.stats['culture'].set(v))
                self.stats['culture'].set("")

        else:
            omenu.add_command(
                label = testr, command = lambda v = testr: self.stats['culture'].set(v))
            self.stats['culture'].set(testr)


    def __statBonus(self):
        '''
        Sets/calculates standard stat bonus
        '''
        from rpgtoolbox.rolemaster import statbonus
        for s in self.__rmstats:
            value = self.stats[s].get()
            self.__std[s].set(statbonus(value))


    def __chkRealm(self, event):
        '''!
        This method checks whether the right magic realm is chosen for the
        selected profession
        @param event object event given by OptionMenu but not used


        ----
        @bug potential cause for false DP calculations. It is not clear how to
        reproduce this bug.
        @bug  if testr != self.profs[testp]['Realm'] and self.profs[testp]['Realm'] != "choice": KeyError: ''
        @bug if realm chosen before profession an error occurs (sdtout)

        @note bug should be fixed
        '''
        testr = self.stats['realm'].get()
        testp = self.stats['prof'].get()
        if testp != "":
            if testr != self.profs[testp]['Realm'] and self.profs[testp]['Realm'] != "choice":
                self.stats['realm'].set(self.profs[testp]['Realm'])
        self.__setPStats()
        self.__calcBonus()


    def __setRBonus(self, event):
        '''!
        This method sets the races bonusses , the race based RR bonusses,
        Background Options and Hobby Ranks.
        @param event object event given by OptionMenu but not used

        ----

        @todo prepare race based additional bonusses which may be added when going to
        the next window.
        '''
        from rpgtoolbox import rolemaster as rm
        race = self.stats['race'].get()
        pos = rm.races[self.lang].index(race)
        race = rm.races['en'][pos]

        for i in list(rm.raceAbilities[race].keys()):
            if "RR" in i:
                self.__rr[i] = rm.raceAbilities[race][i]

        self.character['BGO'] = rm.raceAbilities[race]['BGO']
        self.character['Hobby Ranks'] = rm.raceAbilities[race]['Hobby Ranks']

        for a in rm.stats:
            self.__race[a].set(rm.raceAbilities[race][a])

        self.__setCulture("")


    def __setRealm(self, event):
        '''!
        Sets the connected Realm if profession is chosen
        @param event object event given by OptionMenu but not used
        '''
        testp = self.stats['prof'].get()
        self.stats['realm'].set(self.profs[testp]['Realm'])
        self.__setPStats()


    def __creatPot(self, temp = 20, fixed = False):
        '''!
        This method creates a potential stat from a temporary stat.
        @param temp value of the temporary stat
        @param fixed a parameter that turns the fixed creation mode on/off
        @retval result the resulting potential stat value
        '''

        result = 1

        if 19 < temp < 25:

            if not fixed:
                result = 20 + self.dice(10, 8)

            else:
                result = temp + 44

        elif 24 < temp < 35:

            if not fixed:
                result = 30 + self.dice(10, 7)

            else:
                result = temp + 39

        elif 34 < temp < 45:

            if not fixed:
                result = 40 + self.dice(10, 6)

            else:
                result = temp + 33

        elif 44 < temp < 55:

            if not fixed:
                result = 50 + self.dice(10, 5)

            else:
                result = temp + 28

        elif 54 < temp < 65:

            if not fixed:
                result = 60 + self.dice(10, 4)

            else:
                result = temp + 22

        elif 64 < temp < 75:

            if not fixed:
                result = 70 + self.dice(10, 3)

            else:
                result = temp + 17

        elif 74 < temp < 85:

            if not fixed:
                result = 80 + self.dice(10, 2)

            else:
                result = temp + 11

        elif 84 < temp < 92:

            if not fixed:
                result = 90 + self.dice(10, 1)

            else:
                result = temp + 6

        elif temp == 92:

            if not fixed:
                result = temp - 1 + self.dice(9, 1)

            else:
                result = temp + 5

        elif temp == 93:

            if not fixed:
                result = temp - 1 + self.dice(8, 1)

            else:
                result = temp + 4

        elif temp == 94:

            if not fixed:
                result = temp - 1 + self.dice(7, 1)

            else:
                result = temp + 4

        elif temp == 95:

            if not fixed:
                result = temp - 1 + self.dice(6, 1)

            else:
                result = temp + 3

        elif temp == 96:

            if not fixed:
                result = temp - 1 + self.dice(5, 1)

            else:
                result = temp + 3

        elif temp == 97:

            if not fixed:
                result = temp - 1 + self.dice(4, 1)

            else:
                result = temp + 2

        elif temp == 98:

            if not fixed:
                result = temp - 1 + self.dice(3, 1)

            else:
                result = temp + 2

        elif 98 < temp:

            if not fixed:
                result = temp - 1 + self.dice(2, 1)

            else:
                result = temp + 1

        if result < temp:
            result = temp

        return result


    def dice(self, sides = 6, number = 1):
        '''!
        This function delivers the result of a dice roll as a list.
        @param sides number of sides of the used dice
        @param number number of used dices/rolls
        @retval result sum of the dice rolls
        '''
        i = 0
        result = 0

        while i < number:
            roll = random.randint(1, sides)
            result += roll
            i += 1
        return result


    def rollDice(self):
        """
        Creates the pool for stat generation by rolling the dices.
        """
        self.__count += 1

        if 0 < self.__count < 4:
            result = 600 + self.dice(10, 10)
            self.showno.set(result)

        self.points = self.showno.get()


    def __collectData(self):
        '''
        This method collects all data, adds them to the character's data structure
        and saves that on disk.
        After that it destroys the current window and opens the window for the #
        next creation step.
        '''
        from rpgtoolbox import rolemaster as rm
        import json

        for key in ['player', 'name', 'prof', 'race', 'realm', 'culture']:
            self.character[key] = self.stats[key].get()

        race = rm.races['en'][rm.races[self.lang].index(
            self.character['race'])]

        for stat in self.__rmstats:
            self.character[stat] = {}
            self.character[stat]['name'] = rm.labels[self.lang][stat]
            self.character[stat]['temp'] = self.stats[stat].get()
            self.character[stat]['pot'] = self.pots[stat].get()
            self.character[stat]['race'] = self.__race[stat].get()
            self.character[stat]['spec'] = self.specs[stat].get()
            self.character[stat]['std'] = self.__std[stat].get()
            self.character[stat]['total'] = self.__totals[stat].get()

        self.character['RREss'] = self.character['Em']['total'] * \
            3 + rm.raceAbilities[race]['RREss']
        self.character['RRChan'] = self.character['In']['total'] * \
            3 + rm.raceAbilities[race]['RRChan']
        self.character['RRMent'] = self.character['Pr']['total'] * \
            3 + rm.raceAbilities[race]['RRMent']
        self.character['RRArc'] = self.character['Pr']['total'] + \
            self.character['Em']['total'] + self.character['In']['total']
        self.character['RRC/E'] = self.character['In']['total'] + self.character['Em']['total'] + \
            (rm.raceAbilities[race]['RREss'] +
             rm.raceAbilities[race]['RRChan']) / 2
        self.character['RRC/M'] = self.character['In']['total'] + self.character['Pr']['total'] + \
            (rm.raceAbilities[race]['RRMent'] +
             rm.raceAbilities[race]['RRChan']) / 2
        self.character['RRE/M'] = self.character['Pr']['total'] + self.character['Em']['total'] + \
            (rm.raceAbilities[race]['RREss'] +
             rm.raceAbilities[race]['RRMent']) / 2
        self.character['RRDisease'] = self.character['Co']['total'] * \
            3 + rm.raceAbilities[race]['RRDisease']
        self.character['RRPoison'] = self.character['Co']['total'] * \
            3 + rm.raceAbilities[race]['RRPoison']
        self.character['RRFear'] = self.character["SD"]['total'] * 3
        self.character['purse'] = {'GP': 2,
                                   'SP': 0,
                                   'CP': 0,
                                   'TP': 0,
                                   'IP': 0}
        self.character['old_exp'] = 0
        self.character['exp'] = 10000
        self.character['lvl'] = 1
        self.character["soul dep"] = rm.raceHealingFactors[self.character["race"]]["soul dep"]
        self.character["Stat Loss"] = rm.raceHealingFactors[self.character["race"]]["Stat Loss"]
        self.character["Recovery"] = rm.raceHealingFactors[self.character["race"]]["Recovery"]

        self.__addCatnSkills()

        if not os.path.exists(self.spath + self.character['player']):
            os.mkdir(self.spath + self.character['player'])

        else:
            try:
                with open(self.spath + self.character['player'] + '/' + self.character['name'] + ".json", "w") as outfile:
                    json.dump(self.character, outfile, sort_keys = True,
                              indent = 4, ensure_ascii = False)
            except:
                with open(self.spath + self.character['player'] + '/' + self.character['name'] + ".json", "w") as outfile:
                    json.dump(self.character, outfile, indent = 4)
            self.window.destroy()
            self.window3 = priorizeWeaponsWin(
                self.lang, self.spath, self.character)


    def __addCatnSkills(self):
        '''!
        This method adds skill categories and skills to the character's dictionary
        as well as bonus (special, profession and items)
        @note Skills wont have a profession bonus. It is already applied to the
        category.
        '''
        from rpgtoolbox import rolemaster as rm
        fp = open("%sdefault/Skills_%s.csv" % (self.spath, self.lang))
        content = fp.readlines()
        fp.close()

        if '\n' in content:
            content.remove('\n')

        for i in range(0, len(content)):
            content[i] = content[i].strip('\n\t ').split(',')

        skillcat = {}

        for i in range(1, len(content)):
            skillcat[content[i][0]] = {content[0][2]: content[i][2],
                                       content[0][1]: {},
                                       'spec bonus': 0,
                                       'prof bonus': 0,
                                       'item bonus': 0,
                                       'rank': 0
                                       }

            for pb in list(self.profs[self.character['prof']]['Profession Bonusses'].keys()):

                if pb in content[i][0]:
                    skillcat[content[i][0]]['prof bonus'] = self.profs[self.character['prof']
                                                                       ]['Profession Bonusses'][pb]

            skillcat[content[i][0]][content[0][1]] = {}

            for skill in content[i][1].split(';'):
                skillcat[content[i][0]][content[0][1]][skill] = {content[0][2]: content[i][2],
                                                                 'rank': 0,
                                                                 'rank bonus': 0,
                                                                 'item bonus': 0,
                                                                 'spec bonus': 0,
                                                                 }

        del(content)
        self.profs = rm.choseProfession(self.lang)

        for key in skillcat.keys():

            for pbonus in self.profs[self.character['prof']]['Profession Bonusses'].keys():

                if pbonus in skillcat.keys():
                    skillcat[key]['prof bonus'] = int(self.profs[self.character['prof']]['Profession Bonusses'][pbonus])

        fp = open('%s/default/SkillCat_%s.csv' % (self.spath, self.lang), 'r')
        content = fp.readlines()
        fp.close()

        content[0] = content[0].strip("\n").split(',')

        for i in range(1, len(content)):
            content[i] = content[i].strip('\n').split(',')

            if content[i][0] not in list(skillcat.keys()):
                skillcat[content[i][0]] = {'rank': 0,
                                           'rank bonus': 0,
                                           'item bonus': 0,
                                           'spec bonus': 0
                                           }
                skillcat[content[i][0]]['Skill'] = {}

            skillcat[content[i][0]][content[0][2]] = content[i][2]
            skillcat[content[i][0]]["Skill"][content[0][2]] = content[i][2]
            skillcat[content[i][0]][content[0][1]] = content[i][1].split('/')

            if rm.catnames[self.lang]['spells'] in content[i][0][:7]:
                temp = []

                if '[' in self.character['realm']:
                    self.character['realm'] = self.character['realm'].strip(
                        "'[ ]\n").split("', '")

                if type(self.character['realm']) == type([]):

                    for r in self.character['realm']:
                        temp.append(rm.realmstats[self.lang][r])

                elif self.character['realm'] != "choice":

                    if " " in self.character['realm']:
                        self.character['realm'] = self.character['realm'].strip("(')")
                        self.character['realm'] = self.character['realm'].split("', '")

                        for r in self.character['realm']:
                            temp.append(rm.realmstats[self.lang][r])

                    else:
                        temp.append(rm.realmstats[self.lang][self.character['realm']])

                skillcat[content[i][0]][content[0][1]] = temp
                skillcat[content[i][0]]["Skill"][content[0][1]] = temp

        self.character['cat'] = skillcat
        if self.character['realm'] != "choice":
            self.spellbook = handlemagic.getSpells(self.spath,
                                                   self.character['prof'],
                                                   self.character['realm'],
                                                   self.character['lvl']
                                                   )
            logger.debug("addCatnSkills: path: {}, prof: {}, realm: {}, lvl:{}".format(self.spath,
                                                   self.character['prof'],
                                                   self.character['realm'],
                                                   self.character['lvl']))

            for cat in list(self.character['cat'].keys()):

                if cat[:8] == "Spells -":

                    for slcat in list(self.spellbook.spelllists.keys()):
                        print("DeBUG: addCatnSkills (slcat) {}".format(slcat))
                        print("Debug: keys: {}".format(list(self.spellbook.spelllists[slcat].keys())))

                        if self.spellbook.spelllists[slcat]['Category'] in cat:
                            for spell in list(self.spellbook.spelllists[slcat].keys()):

                                if spell != "Category":
                                    self.character['cat'][cat]['Skill'][spell] = self.spellbook.spelllists[slcat][spell]
                                    self.character['cat'][cat]['Skill'][spell]['rank'] = 0
                                    self.character['cat'][cat]['Skill'][spell]["Progression"] = "Skill Only"
                                    self.character['cat'][cat]['Skill'][spell]['rank bonus'] = 0
                                    self.character['cat'][cat]['Skill'][spell]['item bonus'] = 0
                                    self.character['cat'][cat]['Skill'][spell]["spec bonus"] = 0
#                            break
#XXXXXXXXXXXXXXXXXx


    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
        self.window = MainWindow(
            lang = self.lang, char = self.character, storepath = self.spath)



class priorizeWeaponsWin(blankWindow):
    """!
    This is the class for a window object to chose the priority of weapon skills
    at the character's generation. It will also set the category and skill ranks
    during adolescence.
    @bug sometimes double chosen weapon categories cause list index errors and
    were not detected as doublets.
    """


    def __init__(self, lang = 'en', storepath = os.getcwd() + "/data", char = None):
        """!
        Class constructor
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param title title of the window
        @param storepath path where things like options have to be stored
        @param char Character as JSON
        """
        from rpgtoolbox.rolemaster import catnames
        self.__catnames = catnames

        if storepath == None:
            self.spath = os.getcwd() + "/data"
            logger.debug('Set storepath to %s' % (storepath)) + "/data"

        else:
            self.spath = storepath
            logger.debug('priorizeWeaponsWin: storepath set to %s' %
                         (storepath))

        self.lang = lang
        self.character = char

        blankWindow.__init__(self, self.lang)
        self.window.title('%s - %s (%s)' % (wintitle['rm_create'][self.lang],
                                            self.character['name'],
                                            self.character['prof']
                                            )
                          )
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.notdoneyet)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)
        self.__addHelpMenu()

        self.__getWeaponCats()
        self.__buildWin()

        self.window.mainloop()


    def __buildWin(self):
        '''
        Sets up all the needed Widgets in the window
        '''
        self.__prio = {}
        self.__optWdg = {}

        for i in range(1, 8):
            self.__prio["%s - %d" %
                        (self.__catnames[self.lang]['weapon'], i)] = StringVar()
            self.__prio["%s - %d" % (self.__catnames[self.lang]['weapon'], i)].set(
                "%s - %d" % (self.__catnames[self.lang]['weapon'], i))
            Label(master = self.window,
                  width = 15,
                  text = "Prio #%d %s" % (
                      i, self.__catnames[self.lang]['weapon'])
                  ).grid(column = 0, row = i)

            self.__optWdg[str(i)] = OptionMenu(self.window,
                                               self.__prio["%s - %d" %
                                                           (self.__catnames[self.lang]['weapon'], i)],
                                               *self.weaponcats,
                                               command = self.__getPrio)
            self.__optWdg[str(i)].config(width = 50)
            self.__optWdg[str(i)].grid(column = 1, row = i, sticky = "W")

        Button(master = self.window,
               text = txtbutton['but_next'][self.lang],
               width = 10,
               command = self.__nextStep).grid(column = 1, row = i + 1, sticky = "E")


    def __getPrio(self, event):
        '''!
        This generates the priority list by the chosen priorities.
        @param event has to be catched but is not used
        @todo check for double priorities. If any don't proceed
        @bug when you chose double entries:  File "/home/mongol/git/rpg-tools/src/gui/epwins.py", line 1808, in __getPrio
        for i in range(len(content) - 7, len(content)):
        IndexError: list index out of range
        '''
        self.__priolist = []
        self.__block = False

        for i in range(1, 8):
            dummy = self.__prio["%s - %d" %
                                (self.__catnames[self.lang]['weapon'], i)].get()

            if dummy not in self.__priolist and dummy != "":
                self.__priolist.append(dummy)

            elif dummy in self.__priolist and i < 7:
                self.__block = True
                msg = messageWindow()
                msg.showinfo(errmsg['double'][self.lang], "Info")
                break

        if not self.__block:
            fp = open('./data/default/CatDPC_%s.csv' % self.lang, 'r')
            content = fp.readlines()
            fp.close()

            j = 1

            for i in range(len(content) - 7, len(content)):
                content[i] = content[i].replace("%s - %d" % (self.__catnames[self.lang]['weapon'], j),
                                                self.__priolist[j - 1])
                j += 1
            self.__content = content


    def __buildJSON(self):
        '''
        Makes a JSON out of CatDPC.csv
        Skill cat --> Profession : costs
        '''
        self.__catDBC = {}
        self.__content[0] = self.__content[0].strip('\n \t').split(',')

        for i in range(1, len(self.__content[0])):
            self.__catDBC[self.__content[0][i]] = {}

        for i in range(1, len(self.__content)):
            self.__content[i] = self.__content[i].strip('\n').split(',')
            self.__content[i][0] = self.__content[i][0].strip(' \t')

            for j in range(1, len(self.__content[0])):
                self.__catDBC[self.__content[0][j]
                              ][self.__content[i][0]] = self.__content[i][j]


    def __addToChar(self):
        '''
        This method adds the concerned developing costs and category/skill ranks
        during adolescence to the character data structure (JSON).
        It also calculates the rank bonus for the first time.
        '''
        from rpgtoolbox.rolemaster import races, labels, progressionType, rankbonus, catnames, exceptions, cultures
        # @var prof
        # dummy variable that holds character's profession
        prof = self.character['prof']
        # @var crace
        # dummy variable that holds character's race
        crace = races['en'][races[self.lang].index(self.character['race'])]

        for skillcat in list(self.__catDBC[prof].keys()):
            dbcdummy = self.__catDBC[prof][skillcat].split('/')
            skprog = ""

            for i in range(0, len(dbcdummy)):

                if dbcdummy != "":
                    dbcdummy[i] = int(dbcdummy[i])

            self.character['cat'][skillcat][labels["en"]['costs']] = dbcdummy

            for s in list(self.character['cat'][skillcat]['Skill'].keys()):
                if s not in exceptions:
                    self.character['cat'][skillcat]['Skill'][s][labels["en"]
                                                                ['costs']] = dbcdummy

            if self.character['cat'][skillcat]['Progression'] == "Standard":
                self.character['cat'][skillcat]['Progression'] = progressionType['standard cat']
                skprog = progressionType['standard skill']

            elif self.character['cat'][skillcat]['Progression'] == "BD":
                self.character['cat'][skillcat]['Progression'] = progressionType['null']
                skprog = progressionType['BD %s' % crace]

            elif self.character['cat'][skillcat]['Progression'] == "Null" or self.character['cat'][skillcat]['Progression'] == "Skill Only":
                self.character['cat'][skillcat]['Progression'] = progressionType['null']
                skprog = progressionType['skill only']

            elif self.character['cat'][skillcat]['Progression'] == "Combined":
                self.character['cat'][skillcat]['Progression'] = progressionType['null']
                skprog = progressionType['combined']

            for skill in list(self.character['cat'][skillcat]['Skill'].keys()):

                if skill not in exceptions:
                    self.character['cat'][skillcat]['Skill'][skill]['Progression'] = skprog

        self.__setPPD()
        self.saveChar()

        # adding adolescence skill ranks

        fp = open('./data/default/AdoRanks_%s.csv' % self.lang, "r")
        content = fp.readlines()
        fp.close()
        self.__adoranks = {}
        content[0] = content[0].strip('\n').split(',')

        for i in range(1, len(content[0])):
            self.__adoranks[content[0][i]] = {}

        for j in range(1, len(content)):
            content[j] = content[j].strip('\n').split(',')
            content[j][0] = content[j][0].strip(' \t')

            for i in range(1, len(content[0])):

                if content[j][0][:1] != "-":
                    self.__adoranks[content[0][i]][content[j][0]] = {"rank": int(content[j][i]),
                                                                     "rank bonus": rankbonus(rank = int(content[j][i]),
                                                                                             progression = self.character['cat'][
                                                                                                 content[j][0]]['Progression']
                                                                                             )
                                                                     }
                    lastcat = content[j][0]

                    if "Skill" not in list(self.__adoranks[content[0][i]][content[j][0]].keys()):
                        self.__adoranks[content[0][i]
                                        ][content[j][0]]['Skill'] = {}

                else:
                    self.__adoranks[content[0][i]][lastcat]['Skill'][content[j][0].strip('-')] = {'rank': int(content[j][i]),
                                                                                                  'rank bonus': 0,
                                                                                                  }
        if self.lang != "en":

            race = races['en'][races[self.lang].index(self.character['race'])]
            culture = cultures['en'][cultures[self.lang].index(
                self.character['culture'])]

        else:
            race = self.character['race']
            culture = self.character['culture']

        if race in ['Common Men', 'Mixed Men']:
            race = culture

        for cat in list(self.__adoranks[race].keys()):
            self.character['cat'][cat]['rank'] = self.__adoranks[race][cat]['rank']
            self.character['cat'][cat]['rank bonus'] = self.__adoranks[race][cat]['rank bonus']

            if self.__adoranks[race][cat]['Skill'] != {}:

                for skill in list(self.__adoranks[race][cat]['Skill'].keys()):

                    if skill not in list(self.character['cat'][cat]['Skill'].keys()):
                        self.character['cat'][cat]['Skill'][skill] = {}

                    self.character['cat'][cat]['Skill'][skill]['rank'] = self.__adoranks[race][cat]['Skill'][skill]['rank']
                    self.character['cat'][cat]['Skill'][skill]['rank bonus'] = self.__adoranks[race][cat]['Skill'][skill]['rank bonus']

        self.saveChar()


    def __setPPD(self):
        '''
        This sets the Progression and Stats for Power Point Development

        '''
        from rpgtoolbox.rolemaster import races, realms, ppds, magicstats, progressionType, speccat
        param = {}
        param['realm'] = self.character['realm']

        for l in list(races.keys()):

            if self.character['race'] in races[l]:
                param['lang'] = l
                param['race'] = races['en'][races[l].index(self.character['race'])]

            if self.character['realm'] in realms[l]:
                param['ppd'] = ppds[realms[l].index(self.character['realm'])]
                param['Stats'] = magicstats[realms[l].index(self.character['realm'])]

        if type(param['ppd']) == type(''):
            param['ppd'] = progressionType[param['ppd'] + param['race']]

        elif type(param['ppd']) == type([]):

            for i in range(0, len(param['ppd'])):
                param['ppd'][i] = progressionType[param['ppd'][i] + param['race']]

            if param['ppd'][0] > param['ppd'][1]:
                param['ppd'] = param['ppd'][0]

            else:
                param['ppd'] = param['ppd'][1]

        self.character['cat'][speccat[param['lang']][1]]['Progression'] = progressionType['null']
        self.character['cat'][speccat[param['lang']][1]]['Stats'] = param['Stats']
        self.character['cat'][speccat[param['lang']][1]]['Skill'][speccat[param['lang']][1]]['Progression'] = param['ppd']


    def saveChar(self):
        '''
        This method saves the character as JSON file
        '''
        import json
        charname = self.character['name']  #.replace(" ", "_")

        try:
            with open(self.spath + self.character['player'] + '/' + charname + ".json", "w") as outfile:
                json.dump(self.character, outfile, sort_keys = True,
                          indent = 4, ensure_ascii = False)
        except:
            logger.error("saveChar: could not save {} sorted".format(self.spath + self.character['player'] + '/' + charname + ".json"))
            with open(self.spath + self.character['player'] + '/' + charname + ".json", "w") as outfile:
                json.dump(self.character, outfile, indent = 4)


    def __getWeaponCats(self):
        '''
        Extracts the weapon categories from character
        '''
        self.weaponcats = []

        for cat in list(self.character['cat'].keys()):
            if self.__catnames[self.lang]['weapon'] in cat:
                self.weaponcats.append(cat)

        self.weaponcats.sort()


    def __nextStep(self):
        '''
        Opens the next window to modify categories and skills
        '''
        self.__getPrio("")
        self.__buildJSON()
        self.__addToChar()
        self.window.destroy()
        self.window2 = skillcatWin(self.lang, self.spath, self.character)


    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
        self.window = MainWindow(lang = self.lang, char = self.character)


    def __addHelpMenu(self):
        """
        This methods defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['global'],
                                  command = self._helpPriorize)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def _helpPriorize(self):
        '''
        Opens a message window with help text
        '''
        helptext = {'de': 'Die Priorisierung der Waffenfertigkeiten ist wichtig für '
                    +'die Steigerungskosten und mögliche Anzahl der Steigerungen.\n'
                    +'1 ist die höchste und 7 die geringste Priorität.',
                    'en': 'It is important to priorize the weapon categoies because of '
                    +'developing costs and levels possible to develop.\n'
                    +'1 is the highest priority and 7 the lowest.'
                    }
        helper = messageWindow()
        helper.showinfo(helptext[self.lang], 'Info')



class skillcatWin(blankWindow):
    """!
    This is the class for a window object to chose the priority of weapon skills
    at the character's generation. It will also set the category and skill ranks
    during adolescence.

    ----
    @todo  not finished yet:
      - selecting items here can make changes undone or change them again
      - hide skill/cat line when not selected in treeview
    @bug - DP are not always shown correctly
    - you lose DPs when you try to level up a skill/cat in multiple times
    """


    def __init__(self, lang = 'en', storepath = os.getcwd() + "/data", char = None):
        """
        Class constructor
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param title title of the window
        @param storepath path where things like options have to be stored
        @param char Character as JSON
        """
        from rpgtoolbox.rolemaster import catnames, rankbonus

        self.__catnames = catnames
        self.__rankbonus = rankbonus

        if storepath == None:
#            self.spath = os.path.expanduser('~') + "/data"
            self.spath = os.getcwd() + "/data"
            logger.debug('Set storepath to %s' % (storepath)) + "/data"

        else:
            self.spath = storepath
            logger.debug('priorizeWeaponsWin: storepath set to %s' %
                         (storepath))

        self.lang = lang
        self._character = dict(calcTotals(char))
        self.__save()

        if os.path.isfile("{}/{}/{}_changes.json".format(self.spath, self._character['player'], self._character['name'])):
            self.__changed = readJSON("{}/{}/{}_changes.json".format(self.spath, self._character['player'], self._character['name']))

        else:
            # @var self.__changed
            # dictionary with the changed categories/skills
            self.__changed = {'name': self._character['name'],
                              'player': self._character['player'],
                              'cat': {}
                              }

        self.__calcLvlup()

        blankWindow.__init__(self, self.lang)
        self.window.title("%s - %s (%s)" % (wintitle['edit'][self.lang],
                                            self._character['name'],
                                            self._character['prof']
                                            )
                          )
        self.filemenu = Menu(master = self.menu)
        self.__addFileMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.__buildTree()
        self.window.mainloop()


    def __addFileMenu(self):
        '''
        Adds a file menu  to menu bar.
        '''
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)


    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        if self.__usedDP > 0:
            self._character['lvlup'] -= 1
#            self._character['DP'] -= self.__usedDP
#            self.__usedDP = 0

            if self._character['lvlup'] < 0:
                self._character['lvlup'] = 0

        self.window.destroy()
        self.window = MainWindow(lang = self.lang, storepath = self.spath , char = self._character)


    def __addHelpMenu(self):
        '''
        Adds a help menu entry to menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['win'],
                                  command = self.__helpAWin)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __buildWin(self):
        '''!
        Builds the window's elements.
        - a frame containing:
            -# treeview widget
            -# vertical (auto)scrollbar linked to the treeview widget
            -# horizontal (auto)scrollbar linked to the treeview widget
        - Labels for specific category/skill values

        '''
        from rpgtoolbox.rolemaster import labels as rmlabels
#        self.__treeframe = Frame(width = 800, height = 600)
        self.__treeframe = Frame()
        self.__treeframe.grid(column = 0, row = 0, columnspan = 7, rowspan = 3, sticky = "NEWS")
        self.__rmlabels = rmlabels
        self.__treecolumns = []
        self.catentry = StringVar()
        self.skillentry = ""
        self.catrank = StringVar()
        self.skillrank = StringVar()

        self.__usedDP = 0
        self.catcost = []
        self.skillcost = []
        self.__calcDP()
        # @var self.__changes
        # list of edited/added skills and categories
        self.__changes = {}

        for key in ['skill', 'progress', 'costs', 'rank', 'total']:
            self.__treecolumns.append(rmlabels[self.lang][key])

        ## @var self.__tree
        # The first Treeview widget with the character data to change
        self.__tree = Treeview(self.__treeframe,
                               columns = self.__treecolumns,
                               show = "headings"
                               )
        vscroll = AutoScrollbar(orient = "vertical", command = self.__tree.yview)
        hscroll = AutoScrollbar(orient = "horizontal", command = self.__tree.xview)
        self.__tree.configure(yscrollcommand = vscroll.set,
                              xscrollcommand = hscroll.set)
        self.__tree.grid(column = 0, row = 0, sticky = "NEWS", in_ = self.__treeframe)
        vscroll.grid(column = 1, row = 0, in_ = self.__treeframe, sticky = "NS")
        hscroll.grid(column = 0, row = 1, in_ = self.__treeframe, sticky = "EW")
        ## @var self.__chgtree
        # The second Treeview widged where the changes will be shown.
        self.__chgtree = Treeview(self.window,
                                  columns = self.__treecolumns,
                                  show = "headings",
                                  )
        chgvscroll = AutoScrollbar(
            orient = "vertical", command = self.__chgtree.xview)
        self.__chgtree.configure(yscrollcommand = chgvscroll.set)

        self.__chgtree.grid(column = 0,
                            row = 7,
                            columnspan = 7,
                            rowspan = 3,
                            sticky = "NEW"
                            )
        chgvscroll.grid(column = 7, row = 7, rowspan = 3, in_ = self.window, sticky = "NS")

        Label(master = self.window, width = 30,
              justify = LEFT,
              text = labels['name'][self.lang]).grid(column = 0,
                                                   row = 3,
                                                   sticky = "W",
                                                   padx = 5,
                                                   pady = 5)

        Label(master = self.window,
              width = 10,
              justify = LEFT,
              text = labels['dp_costs'][self.lang]).grid(column = 1,
                                                       row = 3,
                                                       sticky = "W",
                                                       padx = 5,
                                                       pady = 5)

        Label(master = self.window,
              width = 20,
              justify = LEFT,
              text = labels['progr'][self.lang]).grid(column = 2,
                                                    row = 3,
                                                    sticky = "W",
                                                    padx = 5,
                                                    pady = 5)

        Label(master = self.window, width = 4,
              justify = LEFT,
              text = labels['ranks'][self.lang]).grid(column = 3,
                                                    row = 3,
                                                    sticky = "W",
                                                    padx = 5,
                                                    pady = 5)

        Label(master = self.window, width = 4,
              justify = LEFT,
              text = labels['total'][self.lang]).grid(column = 4,
                                                    row = 3,
                                                    sticky = "W",
                                                    padx = 5,
                                                    pady = 5)

        self._catentry = Label(master = self.window,
                               width = 30,
                               justify = LEFT,
                               textvariable = self.catentry
                               )
        self._catentry.grid(column = 0, row = 4, sticky = "NW", padx = 5, pady = 2)

        self.SpinSkillVal = StringVar()
        self.SpinCatVal = StringVar()
        self.CatProg = StringVar()
        self.SkillProg = StringVar()
        self.SpinSkillVal.set(0)
        self.SpinCatVal.set(0)
        self.CatProg.set("0 0 0 0 0")
        self.SkillProg.set("0 0 0 0 0")

        self._catprog = Label(master = self.window,
                              width = 20,
                              justify = LEFT,
                              textvariable = self.CatProg
                              )
        self._catprog.grid(column = 2,
                           row = 4,
                           sticky = "NW",
                           padx = 5,
                           pady = 2
                           )

        self._skillprog = Label(master = self.window,
                                width = 20,
                                justify = LEFT,
                                textvariable = self.SkillProg
                                )
        self._skillprog.grid(column = 2,
                             row = 5,
                             sticky = "NW",
                             padx = 5,
                             pady = 2
                             )

        self._catspin = Spinbox(master = self.window,
                                from_ = 0,
                                to = len(self.catcost),
                                width = 2,
                                textvariable = self.SpinCatVal
                                )
        self._catspin.grid(column = 3,
                           row = 4,
                           sticky = "NW",
                           padx = 5,
                           pady = 2
                           )

        self._skillspin = Spinbox(master = self.window,
                                  from_ = 0,
                                  to = len(self.skillcost),
                                  width = 2,
                                  textvariable = self.SpinSkillVal
                                  )
        self._skillspin.grid(column = 3,
                             row = 5,
                             sticky = "NW",
                             padx = 5,
                             pady = 2
                             )

        self._skillentry = Entry(master = self.window,
                                 width = 30,
                                 textvariable = self.skillentry
                                 )
        self._skillentry.grid(column = 0,
                              row = 5,
                              sticky = "NW",
                              padx = 5,
                              pady = 2
                              )

        Label(master = self.window,
              text = "remaining DPs:").grid(column = 5,
                                          row = 3,
                                          sticky = "NW")
        self.DPtext = StringVar()
        self._remainDP = Label(master = self.window,
                               width = 4,
                               justify = LEFT,
                               textvariable = self.DPtext
                               )
        self._remainDP.grid(column = 6,
                            row = 3,
                            sticky = "NW",
                            padx = 5,
                            pady = 2
                            )
        self.DPtext.set(str(self._character['DP'] - self.__usedDP))

        self.DPcost = StringVar()
        self._lDPcostcat = Label(master = self.window,
                                 width = 6,
                                 justify = CENTER,
                                 textvariable = self.DPcost
                                 )
        self._lDPcostcat.grid(column = 1,
                              row = 4,
                              sticky = "NW",
                              padx = 5,
                              pady = 2
                              )

        self._lDPcostskill = Label(master = self.window,
                                   width = 6,
                                   justify = CENTER,
                                   textvariable = self.DPcost
                                   )
        self._lDPcostskill.grid(column = 1,
                                row = 5,
                                sticky = "NW",
                                padx = 5,
                                pady = 2
                                )
        self.DPcost.set("---")
        # add a 'take over changes' button (submit)
        Button(self.window,
               text = txtbutton['but_take'][self.lang],
               command = self.__takeValsCat).grid(column = 5,
                                                row = 4,
                                                sticky = "NW"
                                                )
        # add a 'take over changes' button (submit)
        Button(self.window,
               text = txtbutton['but_take'][self.lang],
               command = self.__takeValsSkill).grid(column = 5,
                                                  row = 5,
                                                  sticky = "NW"
                                                  )
        # add a 'finalize' button to save changes and proceed.
        Button(self.window,
               text = txtbutton['but_fin'][self.lang],
               command = self.__finalize).grid(column = 6,
                                             row = 4,
                                             sticky = "NW"
                                             )
        # add a 'rename' button for skills.
        Button(self.window,
               text = txtbutton['but_ren'][self.lang],
               command = self.__renameSkill).grid(column = 6,
                                                row = 5,
                                                sticky = "NW"
                                                )


    def __buildTree(self):
        '''!
        Fills the treeview widget with skills and categories etc.
        @todo this has to be implemented:
            - Menu save functionality will save the current work state if not finalized.
            - force a name modify of skills with +
            - If not finalized clicking on items in edit skill/cat treeview will
              cause an editing option. That means:
              -# create a JSON structure with modified but not finalized cats/skills.
              -# put it into the treeview and update it after every change
              -# remove it from treeview if changes were reversed

        '''
        from rpgtoolbox.rolemaster import exceptions

        for col in self.__treecolumns:
            self.__tree.heading(col, text = col.title())
            self.__tree.column(col, width = 200)

        catID = {}
        catNo = 0
        ckeys = list(self._character['cat'].keys())
        ckeys.sort()

        for cat in ckeys:

            if cat != None:
                catID[cat] = self.__tree.insert("",
                                                catNo,
                                                text = cat,
                                                values = (cat,
                                                        self._character['cat'][cat]['Progression'],
                                                        self._character['cat'][cat][self.__rmlabels['en']['costs']],
                                                        self._character['cat'][cat]['rank'],
                                                        self._character['cat'][cat]['total bonus']
                                                        ),
                                                tag = "category"
                                                )

            for skill in list(self._character['cat'][cat]['Skill'].keys()):

                if skill not in exceptions:
                    self.__tree.insert(catID[cat],
                                       "end",
                                       text = skill,
                                       values = (skill,
                                               self._character['cat'][cat]['Skill'][skill]['Progression'],
                                               self._character['cat'][cat][self.__rmlabels['en']['costs']],
                                               self._character['cat'][cat]['Skill'][skill]['rank'],
                                               self._character['cat'][cat]['Skill'][skill]['total bonus']
                                               ),
                                       tag = cat
                                       )

            catNo += 1
        self.__tree.tag_configure('category', background = 'lightblue')
        self.__tree.bind('<ButtonRelease-1>', self.__selectTreeItem)


    def __buildChangedTree(self):
        '''!
        Adding all Changed cat/skill entries to the self.__chgtree
        @todo the following has to be done:
            -# selected items have to be taken to the entry fields
            -# if changes have been taken back add the DP again
        @bug  - slider does not work
        '''
        from rpgtoolbox.rolemaster import exceptions

        for kids in self.__chgtree.get_children():
            self.__chgtree.delete(kids)

        for col in self.__treecolumns:
            self.__chgtree.heading(col, text = col.title())
            self.__chgtree.column(col, width = 200)

        catID = {}
        catNo = 0
        ckeys = list(self.__changed['cat'].keys())
        ckeys.sort()
        dummy = "--"

        for cat in ckeys:

            if cat != None:

                if 'Progression' in list(self.__changed['cat'][cat].keys()):
                    progression = self.__changed['cat'][cat]['Progression']
                else:
                    progression = dummy

                if self.__rmlabels['en']['costs'] in list(self.__changed['cat'][cat].keys()):
                    costs = self.__changed['cat'][cat][self.__rmlabels['en']['costs']]
                else:
                    costs = dummy

                if 'rank' in list(self.__changed['cat'][cat].keys()):
                    rank = self.__changed['cat'][cat]['rank']
                else:
                    rank = "n/a"

                if 'total bonus' in list(self.__changed['cat'][cat].keys()):
                    total = str(self.__changed['cat'][cat]['total bonus'])
                else:
                    total = "n/a"

                catID[cat] = self.__chgtree.insert("",
                                                   catNo,
                                                   text = cat,
                                                   values = (cat,
                                                             progression,
                                                             costs,
                                                             rank,
                                                             total
                                                             ),
                                                tag = "category"
                                                   )
                if 'Skill' in list(self.__changed['cat'][cat].keys()):

                    for skill in list(self.__changed['cat'][cat]['Skill'].keys()):
                        if skill != "Progression" and skill != "Stats":

                            if 'Progression' in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                                progression = self.__changed['cat'][cat]['Skill'][skill]['Progression']

                            if self.__rmlabels['en']['costs'] in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                                costs = self.__changed['cat'][cat]['Skill'][skill][self.__rmlabels['en']['costs']]

                            if 'rank' in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                                srank = self.__changed['cat'][cat]['Skill'][skill]['rank']

                            else:
                                srank = -1

                            if 'total bonus' in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                                stotal = self.__changed['cat'][cat]['Skill'][skill]['total bonus']
                            else:
                                stotal = -1

                            self.__chgtree.insert(catID[cat],
                                                  'end',
                                                  text = skill,
                                                  values = (skill,
                                                           progression,
                                                           costs,
                                                           srank,
                                                           stotal
                                                           ),
                                                  tag = cat
                                                  )
                catNo += 1
        self.__chgtree.tag_configure('category', background = 'lightblue')
        self.__chgtree.bind('<ButtonRelease-1>', self.__selectChangedItem)


    def __selectTreeItem(self, event):
        '''!
        Select an item from the treeview list.
        @param event responding treeview event which is not used for anything.
        '''
        self.__curItem = self.__tree.focus()
        self.DPcost.set(self.__tree.item(self.__curItem)['values'][2])

        if self.__tree.item(self.__curItem)['tags'][0] == 'category':
            self.catentry.set(self.__tree.item(self.__curItem)['text'])
            self._skillentry.delete(0, END)
            self.SpinSkillVal.set(0)
            self.catcost = self.__tree.item(self.__curItem)['values'][2]
            self.CatProg.set(self.__tree.item(self.__curItem)['values'][1])
            self.SpinCatVal.set(self.__tree.item(self.__curItem)['values'][3])

            if type(self.catcost) == type(2):
                self.catcost = [self.catcost]

            elif type(self.catcost) == type("") or type(self.catcost) == type(""):
                self.catcost = self.catcost.split(' ')

                for i in range(0, len(self.catcost)):
                    self.catcost[i] = int(self.catcost[i])

            else:
                self.catcost = []

            self._catspin.config(from_ = self.__tree.item(self.__curItem)['values'][3],
                                 to = self.__tree.item(self.__curItem)['values'][3] + len(self.catcost),
                                 )

            if self.__tree.item(self.__curItem)['tags'][0] == "category":
                self.catrank = str(self.__tree.item(self.__curItem)['values'][-2])

        else:
            self._skillentry.delete(0, END)
            self._skillentry.insert(
                0, self.__tree.item(self.__curItem)['values'][0])
            self.skillcost = self.__tree.item(self.__curItem)['values'][2]
            self.SkillProg.set(self.__tree.item(self.__curItem)['values'][1])

            if type(self.skillcost) == type(2):
                self.skillcost = [self.skillcost]

            elif type(self.skillcost) == type("") or type(self.skillcost) == type(""):
                self.skillcost = self.skillcost.split(' ')

                for i in range(0, len(self.skillcost)):
                    self.skillcost[i] = int(self.skillcost[i])

            else:
                self.skillcost = []

            self._skillspin.config(from_ = self.__tree.item(self.__curItem)['values'][3],
                                   to = self.__tree.item(self.__curItem)['values'][3] + len(self.skillcost),
                                   )
            self.SpinSkillVal.set(self.__tree.item(self.__curItem)['values'][3])

            if self.__tree.item(self.__curItem)['tags'][0] != "category":
                self.skillrank = self.__tree.item(self.__curItem)['values'][-2]

        if self.__tree.item(self.__curItem)['tags'] != "category":
            linkedcat = ""

            for elem in self.__tree.item(self.__curItem)['tags']:
                linkedcat += elem + " "

            self.linkedcat = linkedcat.strip(" ")


    def __selectChangedItem(self, event):
        '''!
        Getting cat/skill entries from  self.__chgtree for further modification.
        @todo It has to be fully implemented
        '''
        pass


    def __calcLvlup(self):
        '''
        This determines current level by current EPs and calculates number of
        level-ups by the level difference of old EP's level and current EP's
        level
        '''
        self._character['lvl'] = int(getLvl(self._character['exp']))
        oldlvl = int(getLvl(self._character['old_exp']))
        if "lvlup" in self._character.keys():
            self._character['lvlup'] += self._character['lvl'] - oldlvl
        else:
            self._character['lvlup'] = 1
            self._character['statgain'] = 0
        self._character['statgain'] = int(self._character['lvlup'] * 10)


    def __calcDP(self):
        '''
        This calculates the number of Development Points (DP) of a character per level up.
        In case of remaining DPs of the last level up this will be added too.
        '''
        attrlist = ['Ag', 'Co', 'Me', 'Re', 'SD']
        if 'DP' not in list(self._character.keys()):
            self._character['DP'] = 0

        if 'lvlup' in list(self._character.keys()):

            if self._character['lvlup'] > 0:
                devpoints = 0

                for attr in attrlist:
                    devpoints += self._character[attr]['temp']
                if 'lvlup' in self._character.keys():

                    if self._character['lvlup'] > 0:
                        self._character['DP'] = int(devpoints / 5)
                else:
                    self._character['DP'] = int(devpoints / 5)

        if self._character['Hobby Ranks'] > 0:
            self._character['DP'] += self._character['Hobby Ranks']
            self._character['Hobby Ranks'] = 0


    def __calcRanks(self, progression, rank):
        '''!
        This method calculates the rank bonusses of a category or skill. if a
        single category or skill is given to this method only this single one will
        be (re-)calculated

        @param progression A list containing the progression values as int
        @param rank rank value for which the bonus has to be calculated

        '''
        if rank == 0:
            result = progression[0]
        elif 0 < rank < 11:
            result = progression[1] * rank
        elif 10 < rank < 21:
            result = progression[1] * 10 + progression[2] * (rank % 10)
        elif 20 < rank < 31:
            result = (progression[1] + progression[2]) * 10 + progression[3] * (rank % 10)
        elif 30 < rank:
            result = (progression[1] + progression[2] + progression[3]) * 10 + progression[3] * (rank % 10)

        return int(result)


    def __calcTotals(self):
        '''
        This method calculate all rank bonus of categories and skills of the
        character loaded.
        At least it is a wrapper for rpgtoobox.rpgtools.calcTotals()
        '''
        self._character = calcTotals(self._character)


    def __takeValsSkill(self):
        '''!
        This method takes added/modified skills/cats to a dict and treeview
        @todo The following__chgtree has to be implemented:
        -# check whether it is a new skill.
        @bug
        - after finalize button use 'edit' and levelups of already parially leveled skills can not be leveled to the given limit.
        '''

        ## @var oldval
        # old catefory's rank value
        oldval = self.__tree.item(self.__curItem)['values'][3]
        ## @var newrank
        # new/changed skills's rank value
        newrank = int(self._skillspin.get())

        if type(self.__tree.item(self.__curItem)['values'][1]) != type(2):
            ## @val currdev
            # list of current development progression
            currdev = self.__tree.item(self.__curItem)['values'][1].split(" ")
        else:
            currdev = [str(self.__tree.item(self.__curItem)['values'][1])]

        for i in range(0, len(currdev)):
            currdev[i] = float(currdev[i])

        ## @var oldtotal
        # Total bonus before any manipulation.
        oldtotal = self.__tree.item(self.__curItem)['values'][-1]
        newtotal = self.__calcRanks(currdev, int(newrank)) - self.__calcRanks(currdev, int(oldval)) + int(oldtotal)
        newbonus = self.__calcRanks(currdev, int(newrank))
        # prepare category name
        cat = ""

        dpCosts = self.__tree.item(self.__curItem)['values'][2]

        if type(dpCosts) == type("") or type(dpCosts) == type(""):
            dpCosts = dpCosts.split(' ')

        elif type(dpCosts) == type(1):
            dpCosts = [dpCosts]

        for elem in self.__tree.item(self.__curItem)["tags"]:
            cat += elem + " "

        cat = cat.strip(" ")
        skill = self.__tree.item(self.__curItem)['text']
        diff = newrank - oldval
        diffcost = 0

        if cat not in list(self.__changed['cat'].keys()):
            self.__changed['cat'][cat] = self._character['cat'][cat]
            newtotal = newbonus + self.__changed['cat'][cat]['total bonus']

            if 'Skill' in list(self.__changed['cat'][cat].keys()):

                if 'Progression' in list(self.__changed['cat'][cat]['Skill'].keys()):
                    del(self.__changed['cat'][cat]['Skill']['Progression'])

                if skill in list(self.__changed['cat'][cat]['Skill'].keys()):
                    diff = newrank - self.__changed['cat'][cat]['Skill'][skill]['rank']
                    diffcost = 0

                    if 'lvlups' not in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                        ##@var lowval
                        # if a skill was not leveled up maximum times this is a marker where to
                        # start with further leveling.
                        lowval = 0

                    elif len(dpCosts) > self.__changed['cat'][cat]['Skill'][skill]['lvlups'] >= 0:
                        lowval = self.__changed['cat'][cat]['Skill'][skill]['lvlups']

                    else:
                        lowval = diff

                    if diff >= 0:

                        for i  in range(lowval, diff):
                            diffcost += int(dpCosts[i])
                    else:
                        for i in range(diff, lowval):
                            diffcost -= int(dpCosts[i])

                    if (self._character['DP'] - (self.__usedDP + diffcost)) >= 0:

                        if 'lvlups' not in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                            self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank

                        else:
                            self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank - self.__changed['cat'][cat]['Skill'][skill]['lvlups']

                        self.__changed['cat'][cat]["Skill"][skill]['lvlups'] = diff
                        self.__changed['cat'][cat]['Skill'][skill]['total bonus'] = newtotal
                        self.__usedDP += diffcost

                    else:
                        self.__info(screenmesg['epwins_no_dp'][self.lang])

                else:

                    if diff >= 0:

                        for i  in range(0, diff):
                            diffcost += int(dpCosts[i])
                    else:
                        for i in range(diff, 0):
                            diffcost -= int(dpCosts[i])

                    if (self._character['DP'] - (self.__usedDP + diffcost)) >= 0:
                        self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank
                        self.__changed['cat'][cat]["Skill"][skill]['lvlups'] = diff
                        self.__changed['cat'][cat]['Skill'][skill]['total bonus'] = newtotal
                        self.__usedDP += diffcost

                    else:
                        self.__info(screenmesg['epwins_no_dp'][self.lang])

            else:

                if self.__changed['cat'][cat]['Skill'][skill]['rank'] > newrank:
                    diff = -diff

                diffcost = 0

                if diff >= 0:

                    for i  in range(0, diff):
                            diffcost += int(dpCosts[i])
                else:
                    for i in range(diff, 0):
                        diffcost -= int(dpCosts[i])

                if (self._character['DP'] - (self.__usedDP + diffcost)) >= 0:

                    if 'lvlups' not in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                            self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank
                    else:
                        self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank - self.__changed['cat'][cat]['Skill'][skill]['lvlups']

                    self.__changed['cat'][cat]["Skill"][skill]['lvlups'] = diff
                    self.__changed['cat'][cat]['Skill'][skill]['total bonus'] = newtotal
                    self.__usedDP += diffcost

                else:
                    self.__info(screenmesg['epwins_no_dp'][self.lang])

        else:

            newtotal = newbonus + self.__changed['cat'][cat]['total bonus']

            if skill in list(self.__changed['cat'][cat]['Skill'].keys()):

                if self.__changed['cat'][cat]['Skill'][skill]['rank'] > newrank:
                    diff = newrank - self.__changed['cat'][cat]['Skill'][skill]['rank']

                diffcost = 0

                if diff >= 0:

                    for i  in range(0, diff):
                            diffcost += int(dpCosts[i])
                else:
                    for i in range(diff, 0):
                        diffcost -= int(dpCosts[i])

                if (self._character['DP'] - (self.__usedDP + diffcost)) >= 0:

                    if 'lvlups' not in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                            self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank
                    else:
                        self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank - self.__changed['cat'][cat]['Skill'][skill]['lvlups']

                    self.__changed['cat'][cat]["Skill"][skill]['lvlups'] = diff
                    self.__changed['cat'][cat]['Skill'][skill]['total bonus'] = newtotal
                    self.__usedDP += diffcost

                else:
                    messg = messageWindow()
                    messg.showinfo(screenmesg['epwins_no_dp'][self.lang])

            else:
                self.__changed['cat'][cat]['Skill'] = self._character['cat'][cat]['Skill']

                if skill not in list(self.__changed['cat'][cat]['Skill'].keys()):
                    self.__changed['cat'][cat]['Skill'][skill] = {}

                diffcost = 0

                if diff >= 0:

                    for i  in range(0, diff):
                            diffcost += int(dpCosts[i])
                else:
                    for i in range(diff, 0):
                        diffcost -= int(dpCosts[i])

                if (self._character['DP'] - (self.__usedDP + diffcost)) >= 0:

                    if 'lvlups' not in list(self.__changed['cat'][cat]['Skill'][skill].keys()):
                            self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank

                    else:
                        self.__changed['cat'][cat]['Skill'][skill]['rank'] = newrank - self.__changed['cat'][cat]['Skill'][skill]['lvlups']

                    self.__changed['cat'][cat]["Skill"][skill]['lvlups'] = diff
                    self.__changed['cat'][cat]['Skill'][skill]['total bonus'] = newtotal
                    self.__usedDP += diffcost

                else:
                    messg = messageWindow()
                    messg.showinfo(screenmesg['epwins_no_dp'][self.lang])

        self.DPtext.set(str(self._character['DP'] - self.__usedDP))
        self.__buildChangedTree()


    def __takeValsCat(self):
        '''
        This method takes added/modified skills/cats to a dict and treeview
        '''
        ## @var currcat
        # current category name
        currcat = self.__tree.item(self.__curItem)['text']
        ## @var olval
        # old catefory's rank value
        oldval = self.__tree.item(self.__curItem)['values'][3]
        ## @var newval
        # new/changed category's rank value
        newval = int(self._catspin.get())
        ## @val currdev
        # list of current development progression
        currdev = self.__tree.item(self.__curItem)['values'][1].split(" ")

        for i in range(0, len(currdev)):
            currdev[i] = float(currdev[i])

        ## @var oldtotal
        # Total bonus before any manipulation.
        oldtotal = self.__tree.item(self.__curItem)['values'][-1]
        ## @var newtotal
        # Total bonus after manipulation
        newtotal = self.__calcRanks(currdev, int(newval)) - self.__calcRanks(currdev, int(oldval)) + int(oldtotal)
        # calc DP consume:
        dpCosts = self.__tree.item(self.__curItem)['values'][2]

        if type(dpCosts) == type("") or type(dpCosts) == type(""):
            dpCosts = dpCosts.split(' ')

        elif type(dpCosts) == type(1):
            dpCosts = [dpCosts]

        if currcat not in list(self.__changed['cat'].keys()) and currcat in list(self._character['cat'].keys()):
            diff = newval - oldval
            self.__changed['cat'][currcat] = self._character["cat"][currcat]
            self.__changed['cat'][currcat]['rank'] = newval

            self.__changed['cat'][currcat]['lvlups'] = diff
            lowval = 0

        else:
            self.__changed['cat'][currcat]['rank'] = newval
            if "lvlups" in list(self.__changed['cat'][currcat].keys()):
                lowval = self.__changed['cat'][currcat]['lvlups']

                if self.__changed['cat'][currcat]['lvlups'] < len(dpCosts):
                    diff = newval - self.__changed['cat'][currcat]['rank']

                else:
                    diff = 0
                    newval = oldval
                    newtotal = self.__calcRanks(currdev, int(newval)) - self.__calcRanks(currdev, int(oldval)) + int(oldtotal)

            else:
                lowval = 0
                diff = newval - self.__changed['cat'][currcat]['rank']
                self.__changed['cat'][currcat]['lvlups'] = diff

        bkpusedDP = int(self.__usedDP)

        if diff > 0:

            for i in range(lowval, diff):
                self.__usedDP += int(dpCosts[i])

        elif diff < 0:

            for i in range(diff, lowval):
                self.__usedDP -= int(dpCosts[i])

        if (self._character['DP'] - self.__usedDP) >= 0:

            if currcat not in list(self.__changed['cat'].keys()) and currcat in list(self._character['cat'].keys()):
                self.__changed['cat'][currcat] = self._character['cat'][currcat]

                if "Skill" in list(self._character['cat'][currcat].keys()):
                    self.__changed['cat'][currcat]['Skill'] = self._character['cat'][currcat]['Skill']

                else:
                    self.__changed['cat'][currcat]['Skill'] = {}

            if "lvlups" in list(self.__changed['cat'][currcat].keys()):
                self.__changed['cat'][currcat]['rank'] = newval

                if self.__changed['cat'][currcat]['lvlups'] < newval:
                    self.__changed['cat'][currcat]['lvlups'] += 1

            else:
                self.__changed['cat'][currcat]['rank'] = newval

            self.__changed['cat'][currcat]['total bonus'] = newtotal

        else:
            self.__usedDP = bkpusedDP
            messg = messageWindow()
            messg.showinfo(screenmesg['epwins_no_dp'][self.lang])

        self.DPtext.set(str(self._character['DP'] - self.__usedDP))
        self.__buildChangedTree()


    def __finalize(self):
        '''
        This method finalizes and saves all changes into character data

        The changes done before are saved in the file <charname>_changes.json
        '''
        from rpgtoolbox import rolemaster as rm
        self.profs = rm.choseProfession(self.lang)
        #refreshing/recalculating stat bonusses
        self._character = rm.refreshStatBonus(self._character)
        # remove usedDP from character's available DP
        self._character['DP'] -= self.__usedDP
#        handlemagic.updateSL(character = self._character, datadir = self.spath)
        self._character["soul dep"] = rm.raceHealingFactors[self._character["race"]]["soul dep"]
        self._character["Stat Loss"] = rm.raceHealingFactors[self._character["race"]]["Stat Loss"]
        self._character["Recovery"] = rm.raceHealingFactors[self._character["race"]]["Recovery"]

        if self._character['DP'] == 0 and self._character['lvlup'] > 0:
            self._character['lvlup'] -= 1

            for c in self._character["cat"].keys():
                self._character['cat'][c]['lvlups'] = 0

                for sk in self._character["cat"][c]['Skill'].keys():

                    if type(self._character["cat"][c]['Skill'][sk]) == type({}):
                        self._character["cat"][c]['Skill'][sk]['lvlups'] = 0

        self._character["old_exp"] = int(self._character['exp'])

        for cat in list(self.__changed["cat"].keys()):
            self._character['cat'][cat]["rank"] = self.__changed["cat"][cat]["rank"]
            self._character['cat'][cat]["total bonus"] = self.__changed['cat'][cat]["total bonus"]

            for skill in list(self.__changed["cat"][cat]["Skill"].keys()):

                if skill != "Progression" and skill != "Stats":

                    if skill not in list(self._character["cat"][cat]["Skill"].keys()):
                        self._character["cat"][cat]["Skill"][skill] = self.__changed['cat'][cat]["Skill"][skill]

                    else:
                        self._character["cat"][cat]["Skill"][skill]["rank"] = self.__changed["cat"][cat]["Skill"][skill]["rank"]
                        self._character["cat"][cat]["Skill"][skill]["total bonus"] = self.__changed["cat"][cat]["Skill"][skill]["total bonus"]

        # setting prof bonusses again
        for cat in self._character['cat'].keys():

            for pb in self.profs[self._character['prof']]['Profession Bonusses']:

                if pb in cat:
                    self._character['cat'][cat]['prof bonus'] = int(self.profs[self._character['prof']]['Profession Bonusses'][pb])
                    break

                else:
                    self._character['cat'][cat]['prof bonus'] = 0
        handlemagic.updateSL(character = self._character, datadir = self.spath)
        # save character data
        self.__save('.json')
        if  self._character['DP'] > 0:
            # save changes
            writeJSON("{}/{}/{}_changes.json".format(self.spath, self._character['player'], self._character['name']), self.__changed)

        else:

            if os.path.isfile("{}/{}/{}_changes.json".format(self.spath, self._character['player'], self._character['name'])):
                os.remove("{}/{}/{}_changes.json".format(self.spath, self._character['player'], self._character['name']))
        self.window.destroy()

        if "background" in self._character.keys():
            self.window2 = MainWindow(lang = self.lang, storepath = self.spath, char = self._character)

        else:
            self.window2 = charInfo(self.lang, self.spath, self._character)


    def __renameSkill(self):
        '''!
        This method renames all skill+ and adds new ones
        ----
        @todo checkup whether values exist in self.__changed. If so take rank value from self.__changed.

        '''
        from rpgtoolbox.rolemaster import progressionType
        self._character['DP'] -= self.__usedDP
        self.__usedDP = 0
        curitem = self.__tree.item(self.__curItem)
        skillentry = self._skillentry.get()
        cat = ""

        for elem in curitem['tags']:
            cat += elem + " "

        cat = cat.strip(" ")
        skill = {skillentry: {"item bonus":0,
                             "rank": int(curitem["values"][3]),
                             "rank bonus": 0,
                             "spec bonus": 0,
                             "total bonus": 0,
                             "Progression": list(progressionType["standard skill"]),  #list(self._character['cat'][cat]["Skill"]['Progression']),
                             "Costs": list(self._character['cat'][cat]['Costs'])
                             }
                }
        if skillentry in self.__changed['cat'][cat]['Skill'].keys():
            skill[skillentry]["rank"] = self.__changed['cat'][cat]['Skill'][skillentry]["rank"]

        self._character['cat'][cat]["Skill"][skillentry] = skill[skillentry]

        dummyDP = int(self._character['DP'])

        for entry in ["item bonus", "rank"]:
            self._character['cat'][cat]["Skill"][curitem['text']][entry] = 0

        self.__calcTotals()
        self.__buildWin()
        self.__buildTree()
        self.__buildChangedTree()
        self._character['DP'] = dummyDP


    def __save(self, ending = '.snap'):
        '''
        This method quickly saves a snapshot of current character's data into
        a file.

        @param ending ending of the filename
        '''
        pathfile = self.spath + "/" + \
            self._character['player'] + "/" + self._character['name'] + ending
        writeJSON(pathfile, self._character)


    def __info(self, text = ""):
        '''!
        This method just opens a message window to display information.
        @param text the text to display

        '''
        self.__mesg = messageWindow(self.lang)
        self.__mesg.showinfo(str(text))


    def __helpAWin(self):
        '''!
        Help information about this window.
        @todo has to be implemented
        '''
        self.notdoneyet("helpAWin")



class charInfo(blankWindow):
    """
    This is the class for the window with all the background information such as hair color, height etc.
    """


    def __init__(self, lang = 'en', storepath = os.getcwd() + "/data", char = None):
        """!
        Class constructor charInfo
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param title title of the window
        @param storepath path where things like options have to be stored
        @param char Character as JSON/dictionary
        """

        if storepath == None:
#            self.spath = os.path.expanduser('~') + "/data"
            self.spath = os.getcwd() + "/data"
            logger.info('Set storepath to %s' % (storepath)) + "/data"

        else:
            self.spath = storepath
            logger.info('charInfo: storepath set to %s' %
                         (storepath))
        self.lang = lang
        self._character = dict(calcTotals(char))
        self.mypath = storepath + "default/pics"
        self.cmask = [txtwin['json_files'][self.lang],
                     txtwin['grp_files'][self.lang],
                     txtwin['all_files'][self.lang]
                     ]
        self.pmask = [txtwin['jpg_files'][self.lang],
                     txtwin['jpeg_files'][self.lang],
                     txtwin['png_files'][self.lang]
                     ]

        if "piclink" in list(self._character.keys()) and self._character["piclink"] != "":
            self.charpic = self._character["piclink"]
        else:
            self.charpic = "./data/default/pics/default.jpg"
            self._character['piclink'] = "./data/default/pics/default.jpg"

        blankWindow.__init__(self, self.lang)
        self.window.title("%s - %s (%s)" % (wintitle['background'][self.lang],
                                            self._character['name'],
                                            self._character['prof']
                                            )
                          )
        self.filemenu = Menu(master = self.menu)
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addFileMenu(self):
        '''
        Adds a file menu to menu bar.
        '''
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['export'],
                                  command = self.notdoneyet)
        self.filemenu.add_command(label = submenu['file'][self.lang]['print'],
                                  command = self.notdoneyet)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.notdoneyet)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)


    def __addEditMenu(self):
        '''
        This adds an edit menu to the menu bar.
        '''
        self.edtmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_edit'][self.lang],
                              menu = self.edtmenu)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['add_pic'],
                                 command = self.__addPicMenue)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['add_story'],
                                 command = self.__addStory)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['statgain'],
                                 command = self.__statGainRoll)


    def __addHelpMenu(self):
        '''
        Adds a help menu entry to menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['win'],
                                  command = self.__helpWin)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
        logger.debug("charInfo: Call MainWindow(lang={},storepath={},char={}".format(self.lang, self.spath, self._character))
        self.window = MainWindow(lang = self.lang, storepath = self.spath , char = self._character)


    def __openFile(self):
        """
        This method opens a dialogue window (Tk) for opening files.
        The content of the opened file will be saved in \e file
        \e content as an array.
        """
        self.__filein = askopenfilename(filetypes = self.cmask,
                                        initialdir = self.mypath)
        if self.__filein != "":
            with open(self.__filein, 'r') as filecontent:

                if self.__filein[-4:].lower() == "json":
                    self.char = json.load(filecontent)
                    logger.debug("charInfo:(character) content read from {}.".fomat(self.__filein))

                elif self.__filein[-3:].lower == "grp":
                    self.grp = json.load(filecontent)
                    logger.debug("charInfo:(group) content read from {}.".fomat(self.__filein))

                else:
                    msg = messageWindow()
                    msg.showinfo(errmsg['wrong_type'][self.lang])
                    logger.warn(errmsg['wrong_type'][self.lang])
                    pass


    def __buildWin(self):
        '''
        Builds the window's elements.

        '''
        self.background = {}

        for elem in charattribs.keys():
            self.background[elem] = StringVar()

        alreadyset = False

        if "background" in list(self._character.keys()):
            alreadyset = True

        # row 0; column 0 -3
        Label(master = self.window,
              width = 15,
              text = self._character["player"]
              ).grid(column = 0, row = 0)

        Label(master = self.window,
              width = 30,
              text = self._character['name']
              ).grid(column = 1, row = 0)

        Label(master = self.window,
              width = 20,
              text = self._character['prof']
              ).grid(column = 2, row = 0)

        Label(master = self.window,
              width = 20,
              text = self._character['race']
              ).grid(column = 3, row = 0)

        # row 1 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['sex'][self.lang] + ":"
              ).grid(column = 0,
                     row = 1)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['sex']
              ).grid(column = 1, row = 1)

        # row 2 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['hair'][self.lang] + ":"
              ).grid(column = 0, row = 2)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['hair']
              ).grid(column = 1, row = 2)
        # row 3 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['eyes'][self.lang] + ":"
              ).grid(column = 0, row = 3)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['eyes']
              ).grid(column = 1, row = 3)
        # row 4 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['skin'][self.lang] + ":"
              ).grid(column = 0, row = 4)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['skin']
              ).grid(column = 1, row = 4)
        # row 5 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['height'][self.lang] + ":"
              ).grid(column = 0, row = 5)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['height']
              ).grid(column = 1, row = 5)
        # row 6 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['weight'][self.lang] + ":"
              ).grid(column = 0, row = 6)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['weight']
              ).grid(column = 1, row = 6)
        # row 7 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['app_age'][self.lang] + ":"
              ).grid(column = 0, row = 7)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['app_age']
              ).grid(column = 1, row = 7)
        # row 8 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['act_age'][self.lang] + ":"
              ).grid(column = 0, row = 8)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['act_age']
              ).grid(column = 1, row = 8)
        # row 9 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['parents'][self.lang] + ":"
              ).grid(column = 0, row = 9)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['parents']
              ).grid(column = 1, row = 9)
        # row 10 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['siblings'][self.lang] + ":"
              ).grid(column = 0, row = 10)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['siblings']
              ).grid(column = 1, row = 10)
        # row 11 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['partner'][self.lang] + ":"
              ).grid(column = 0, row = 11)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['partner']
              ).grid(column = 1, row = 11)
        # row 12 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['kids'][self.lang] + ":"
              ).grid(column = 0, row = 12)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['kids']
              ).grid(column = 1, row = 12)
        # row 13 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['deity'][self.lang] + ":"
              ).grid(column = 0, row = 13)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['deity']
              ).grid(column = 1, row = 13)
        # row 14 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['home'][self.lang] + ":"
              ).grid(column = 0, row = 14)
        Entry(master = self.window,
              width = 35,
              textvariable = self.background['home']
              ).grid(column = 1, row = 14)

        #set values into Entry widgets if there are any
        if alreadyset:
            for elem  in self._character['background'].keys():
                self.background[elem].set(self._character['background'][elem])

        # row 15-19 column 0-1
        Label(master = self.window,
              width = 15,
              text = charattribs['pers'][self.lang] + ":"
              ).grid(column = 0, row = 15, columnspan = 2)
        self.tw1 = Text(master = self.window,
                 width = 50,
                 height = 20,
                 wrap = WORD
                 )
        if "history" in list(self._character.keys()):
            self.tw1.insert(1.0, self._character['history'])

        self.tw1.grid(column = 0, row = 16, columnspan = 2)
        # row 15-19 column 2-3
        Label(master = self.window,
              width = 15,
              text = charattribs['motiv'][self.lang] + ":"
              ).grid(column = 2, row = 15, columnspan = 2)
        self.tw2 = Text(master = self.window,
                 width = 50,
                 height = 20,
                 wrap = WORD
                 )

        if "motivation" in list(self._character.keys()):
            self.tw2.insert(1.0, self._character['motivation'])

        self.tw2.grid(column = 2, row = 16, columnspan = 2)

        Button(self.window,
        text = txtbutton['but_story'][self.lang],
        command = self.__addStory).grid(column = 0,
                                        row = 17,
                                        sticky = "NW",
                                        columnspan = 2
                                        )
        Button(self.window,
        text = txtbutton['but_sav'][self.lang] + "\n" + txtbutton['but_quit'][self.lang],
        command = self.__saveAndExit).grid(column = 3,
                                        row = 17,
                                        sticky = "NW",
                                        columnspan = 2
                                        )
        #charpic row 1-8 column 2-4
        #BUG pic does not work
        from PIL import Image, ImageTk
        self.cpic = ImageTk.PhotoImage(Image.open(self.charpic).resize((310, 310), Image.ANTIALIAS))
        self.picLabel = Label(master = self.window,
                              image = self.cpic
                              )

        self.picLabel.grid(column = 2,
                           row = 1,
                           columnspan = 2,
                           rowspan = 14,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)
        self.picLabel.bind("<Button-1>", self.__addPic)


    def __addPic(self, event):
        '''
        This method adds the link to a character's picture (jpg/png)
        '''
        self.charpic = askopenfilename(filetypes = self.pmask,
                                        initialdir = self.mypath)
        if type(self.charpic) == type(""):
            self._character['piclink'] = self.charpic
            from PIL import Image, ImageTk
            self.cpic = ImageTk.PhotoImage(Image.open(self.charpic).resize((300, 300), Image.ANTIALIAS))
            self.picLabel.configure(image = self.cpic)


    def __addPicMenue(self):
        '''
        This method adds the link to a character's picture (jpg/png)
        '''
        self.charpic = askopenfilename(filetypes = self.pmask,
                                        initialdir = self.mypath)
        if type(self.charpic) == type(""):
            self._character['piclink'] = self.charpic
            from PIL import Image, ImageTk
            self.cpic = ImageTk.PhotoImage(Image.open(self.charpic).resize((300, 300), Image.ANTIALIAS))
            self.picLabel.configure(image = self.cpic)


    def __statGainRoll(self):
        '''
        This opens a window for Stats Gain Roll for the character.
        '''
        self.window.destroy()

        self.window2 = statGainWin(lang = self.lang, storepath = self.spath, char = self._character)


    def __addStory(self):
        self.notdoneyet("charInfo.addStory: \n not done yet")


    def __saveAndExit(self):
        '''
        This method gets all data from entries, puts them into character data struct
        and saves the updated character.
        '''
        if self.spath[-1] not in ["\\", "/"]:
            self.spath += "/"
        bg = {}
        self._character["motivation"] = self.tw2.get("0.0", END)
        self._character['history'] = self.tw1.get("0.0", END)
        for el in list(self.background.keys()):
            bg[el] = self.background[el].get()

        self._character["background"] = bg
        self._character["background"]["motiv"] = self.tw2.get("0.0", END)
        self._character['background']['pers'] = self.tw1.get("0.0", END)

        with open(self.spath + '/' + self._character['player'] + '/' + self._character['name'] + ".json", "w") as outfile:
                json.dump(self._character,
                          outfile,
                          sort_keys = True,
                          indent = 4,
                          ensure_ascii = False)

        self.window.destroy()
        self.window = MainWindow(lang = self.lang, storepath = self.spath, char = self._character)


    def __helpWin(self):
        self.notdoneyet("charInfo.__helpWin:\ņ\n not done yet")



class statGainWin(blankWindow):
    """
    This is the class for the window to execute Stat gain rolls.
    """


    def __init__(self, lang = 'en', storepath = os.getcwd() + "/data", char = None):
        """!
        Class constructor statGainWin
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param title title of the window
        @param storepath path where things like options have to be stored
        @param char Character as JSON/dictionary
        """

        if storepath == None:
#            self.spath = os.path.expanduser('~') + "/data"
            self.spath = os.getcwd() + "/data"
            logger.debug('Set storepath to %s' % (os.getcwd())) + "/data"

        elif "/data" not in storepath:
            self.spath = os.getcwd() + "/data"

        else:
            self.spath = storepath
            logger.debug('statGainWin: storepath set to %s' %
                         (storepath))
        self.lang = lang
        self._character = dict(calcTotals(char))
        self.statgain = 10

        if "statgain" in self._character.keys():

            if self._character['statgain'] > 0:
                self.statgain = int(self._character['statgain'])
            else:
                self.statgain = 0

        self.mypath = storepath + '/' + self._character['player'] + '/'
        self.cmask = [txtwin['json_files'][self.lang],
                     txtwin['grp_files'][self.lang],
                     txtwin['all_files'][self.lang]
                     ]

        blankWindow.__init__(self, self.lang)
        self.window.title("%s - %s (%s)" % (wintitle['rm_statgain'][self.lang],
                                            self._character['name'],
                                            self._character['prof']
                                            )
                          )
        self.filemenu = Menu(master = self.menu)
        self.__addFileMenu()
#        self.__addEditMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addFileMenu(self):
        '''
        Adds a file menu to menu bar.
        '''
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)

        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'] + " & " + submenu['file'][self.lang]['close'],
                                  command = self.saveData)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)

        self.__stats = stats

#    def __addEditMenu(self):
#        '''
#        This adds an edit menu to the menu bar.
#        '''
#        self.edtmenu = Menu(master = self.menu)
#        self.menu.add_cascade(label = txtmenu['menu_edit'][self.lang],
#                              menu = self.edtmenu)
#        self.edtmenu.add_command(label = submenu['edit'][self.lang]['add_pic'],
#                                 command = self.__addPic)
#        self.edtmenu.add_command(label = submenu['edit'][self.lang]['add_story'],
#                                 command = self.__addStory)
#        self.edtmenu.add_command(label = submenu['edit'][self.lang]['statgain'],
#                                 command = self.__statGainRoll)


    def __addHelpMenu(self):
        '''
        Adds a help menu entry to menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['win'],
                                  command = self.__helpWin)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
        self.window = MainWindow(lang = self.lang, char = self._character)

#    def __openFile(self):
#        """
#        This method opens a dialogue window (Tk) for opening files.
#        The content of the opened file will be saved in \e file
#        \e content as an array.
#        """
#        self.__filein = askopenfilename(filetypes = self.cmask,
#                                        initialdir = self.mypath)
#        if self.__filein != "":
#            with open(self.__filein, 'r') as filecontent:
#
#                if self.__filein[-4:].lower() == "json":
#                    self.char = json.load(filecontent)
#
#                elif self.__filein[-3:].lower == "grp":
#                    self.grp = json.load(filecontent)
#
#                else:
#                    msg = messageWindow()
#                    msg.showinfo(errmsg['wrong_type'][self.lang])
#                    logger.warn(errmsg['wrong_type'][self.lang])
#                    pass


    def __helpWin(self):
        self.notdoneyet("charInfo.__helpWin:\ņ\n not done yet")


    def __buildWin(self):
        '''
        Builds the window's elements.

        '''
        Label(master = self.window,
              width = 20,
              text = self._character["player"]
              ).grid(column = 0, row = 0)

        Label(master = self.window,
              width = 20,
              text = self._character['name']
              ).grid(column = 1, row = 0)

        Label(master = self.window,
              width = 20,
              text = self._character['race']
              ).grid(column = 2, row = 0)

        Label(master = self.window,
              width = 20,
              text = self._character['prof']
              ).grid(column = 3, row = 0)

        Label(master = self.window,
              width = 20,
              text = "Stats"
              ).grid(column = 0, row = 1, pady = 5, padx = 2)

        Label(master = self.window,
              width = 20,
              text = "Temp"
              ).grid(column = 1, row = 1, pady = 5, padx = 2)

        Label(master = self.window,
              width = 20,
              text = "Pot"
              ).grid(column = 2, row = 1, pady = 5, padx = 2)

        Label(master = self.window,
              width = 20,
              text = labels['new_val'][self.lang]
              ).grid(column = 3, row = 1, pady = 5, padx = 2)

        self.var = {}
        self.__cb = {}
        self.__nl = {}
        self.__nv = {}
        #row and column
        r = 2

        self.__sgr = StringVar()
        self.__sgr.set(labels['count'][self.lang] + ": " + str(self.statgain))

        for s in self.__stats:
            self.var[s] = IntVar()
            self.__nv[s] = StringVar()
            self.__nv[s].set("--")

            self.__cb[s] = Checkbutton(master = self.window,
                                     text = self._character[s]["name"],
                                     variable = self.var[s]
                                     )
            self.__cb[s].grid(column = 0, row = r, pady = 2, padx = 2, sticky = W)

            Label(master = self.window,
                  width = 20,
                  text = str(self._character[s]['temp'])
                  ).grid(column = 1, row = r, pady = 2, padx = 2, sticky = E)

            Label(master = self.window,
                  width = 20,
                  text = str(self._character[s]['pot'])
                  ).grid(column = 2, row = r, pady = 2, padx = 2, sticky = E)

            Label(master = self.window,
                  width = 20,
                  textvariable = self.__nv[s],
                  ).grid(column = 3, row = r, pady = 2, padx = 2, sticky = E)

            r += 1

            if self.statgain == 10:
                self.var[s].set(1)

            else:
                self.var[s].set(0)

        Button(self.window,
               text = txtbutton['but_all'][self.lang],
               command = self.__selectAll,
               width = 20
               ).grid(column = 0,
                      row = r,
                      pady = 2,
                      sticky = "NW"
                      )

        Button(self.window,
               text = txtbutton['but_none'][self.lang],
               command = self.__selectNone,
               width = 20
               ).grid(column = 1,
                      row = r,
                      pady = 2,
                      sticky = "NW"
                      )
        Label(master = self.window,
              width = 20,
              textvariable = self.__sgr
              ).grid(column = 2,
                     row = r)
        Button(self.window,
               text = txtbutton['but_roll'][self.lang],
               command = self.statGainRoll,
               width = 20
               ).grid(column = 3,
                      row = r,
                      pady = 2,
                      sticky = "NW"
                      )


    def __selectAll(self):
        '''
        This method selects all Checkbuttons
        '''
        for s in self.__stats:
            self.var[s].set(1)


    def __selectNone(self):
        '''
        This method unselects all Checkbuttons
        '''
        for s in self.__stats:
            self.var[s].set(0)


    def statGainRoll(self):
        '''
        This method does Stat Gain Rolls for all selected stats
        '''
        from rpgtoolbox.rolemaster import statbonus
        from rpgtoolbox.rpgtools import dice, statGain
        self.newstats = {}

        for s in self.__stats:
            doGainRoll = self.var[s].get()

            if doGainRoll and self.statgain > 0:
                d = dice(10, 2)

                self.newstats[s] = statGain(d[0], d[1], self._character[s]['temp'], self._character[s]['pot'])
                self.__nv[s].set(self.newstats[s])

                self.statgain -= 1
                self.__sgr.set(labels['count'][self.lang] + ": " + str(self.statgain))

        if self.statgain <= 0:

            for elem in self.newstats.keys():
                self._character[elem]['temp'] = int(self.newstats[elem])
                self._character[elem]['std'] = statbonus(self._character[elem]['temp'])
                self._character[elem]['total'] = self._character[elem]['std'] + self._character[elem]['race'] + self._character[elem]['spec']
            self._character['statgain'] = 0

            Button(self.window,
                   text = txtbutton['but_sav'][self.lang] + " & " + txtbutton['but_quit'][self.lang],
                   command = self.saveData,
                   width = 40
                   ).grid(column = 1,
                          row = 13,
                          columnspan = 2,
                          pady = 3,
                          sticky = "NEWS"
                          )


    def saveData(self):
        '''
        This recalculates character's category and skill bonusses, saves character and goes back to main window.
        '''
        self._character = dict(calcTotals(self._character))

        with open(self.spath + '/' + self._character['player'] + '/' + self._character['name'] + ".json", "w") as outfile:
            json.dump(self._character,
                      outfile,
                      sort_keys = True,
                      indent = 4,
                      ensure_ascii = False)

        self.window.destroy()
        self.window = MainWindow(lang = self.lang, storepath = self.spath, char = self._character)



class editEPWin(blankWindow):
    '''
    This window class generates a window to enter new EPs manually to character data
    '''


    def __init__(self, lang = 'en', storepath = os.getcwd() + "/data", char = None):
        """!
        Class constructor editEPWin
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param title title of the window
        @param storepath path where things like options have to be stored
        @param char Character as JSON/dictionary
        """

        if storepath == None:
#            self.spath = os.path.expanduser('~') + "/data"
            self.spath = os.getcwd() + "/data"
            logger.debug('Set storepath to %s' % (storepath)) + "/data"

        else:
            self.spath = storepath
            logger.debug('editEPWin: storepath set to %s' %
                         (storepath))
        self.lang = lang
        self._character = dict(calcTotals(char))

        self.mypath = storepath + '/' + self._character['player'] + '/'
        self.cmask = [txtwin['json_files'][self.lang],
                     txtwin['grp_files'][self.lang],
                     txtwin['all_files'][self.lang]
                     ]

        blankWindow.__init__(self, self.lang)
        self.window.title("%s - %s (%s)" % (wintitle['rm_statgain'][self.lang],
                                            self._character['name'],
                                            self._character['prof']
                                            )
                          )
        self.filemenu = Menu(master = self.menu)
        self.__addFileMenu()
#        self.__addEditMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addFileMenu(self):
        '''
        Adds a file menu to menu bar.
        '''
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)

        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.saveData)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)

        self.__stats = stats

#    def __addEditMenu(self):
#        '''
#        This adds an edit menu to the menu bar.
#        '''
#        self.edtmenu = Menu(master = self.menu)
#        self.menu.add_cascade(label = txtmenu['menu_edit'][self.lang],
#                              menu = self.edtmenu)
#        self.edtmenu.add_command(label = submenu['edit'][self.lang]['add_pic'],
#                                 command = self.__addPic)
#        self.edtmenu.add_command(label = submenu['edit'][self.lang]['add_story'],
#                                 command = self.__addStory)
#        self.edtmenu.add_command(label = submenu['edit'][self.lang]['statgain'],
#                                 command = self.__statGainRoll)


    def __addHelpMenu(self):
        '''
        Adds a help menu entry to menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['win'],
                                  command = self.__helpWin)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
        self.window = MainWindow(lang = self.lang, char = self._character, storepath = self.spath)


    def __openFile(self):
        """
        This method opens a dialogue window (Tk) for opening files.
        The content of the opened file will be saved in \e file
        \e content as an array.
        """
        self.__filein = askopenfilename(filetypes = self.cmask,
                                        initialdir = self.mypath)
        if self.__filein != "":
            with open(self.__filein, 'r') as filecontent:

                if self.__filein[-4:].lower() == "json":
                    self.char = json.load(filecontent)

                elif self.__filein[-3:].lower == "grp":
                    self.grp = json.load(filecontent)

                else:
                    msg = messageWindow()
                    msg.showinfo(errmsg['wrong_type'][self.lang])
                    logger.warn(errmsg['wrong_type'][self.lang])
                    pass


    def __helpWin(self):
        self.notdoneyet("charInfo.__helpWin:\ņ\n not done yet")


    def saveData(self):
        '''
        This recalculates character's category and skill bonusses, saves character and goes back to main window.
        '''
        self._character = dict(calcTotals(self._character))

        with open(self.spath + '/' + self._character['player'] + '/' + self._character['name'] + ".json", "w") as outfile:
            json.dump(self._character,
                      outfile,
                      sort_keys = True,
                      indent = 4,
                      ensure_ascii = False)

#        self.window.destroy()
#        self.window = MainWindow(lang = self.lang, storepath = self.spath, char = self._character)


    def __buildWin(self):
        '''
        Builds the window's elements.

        '''
        self.epval = StringVar()
        self.inputval = StringVar()
        self.lvlval = StringVar()
        self.statbar = StringVar()

        Label(master = self.window,
              width = 20,
              text = "{}: {}".format(labels["player"][self.lang], self._character['player'])
              ).grid(column = 0,
                     row = 0,
                     padx = 3,
                     pady = 5)

        Label(master = self.window,
              width = 20,
              text = "{}: {}".format(labels["name"][self.lang], self._character['name'])
              ).grid(column = 1,
                     row = 0,
                     padx = 3,
                     pady = 5)

        Label(master = self.window,
              width = 20,
              text = "{}: {}".format(labels["prof"][self.lang], self._character['prof'])
              ).grid(column = 2,
                     row = 0,
                     padx = 3,
                     pady = 5)

        Label(master = self.window,
              width = 20,
              textvariable = self.lvlval
              ).grid(column = 3,
                     row = 0,
                     padx = 3,
                     pady = 5)
        self.lvlval.set("{}: {}".format(labels["lvl"][self.lang], self._character['lvl']))

        Label(master = self.window,
              width = 20,
              textvariable = self.epval
              ).grid(column = 0,
                     row = 1,
                     padx = 3,
                     pady = 5)
        self.epval.set("EP: {}".format(self._character['exp']))

        Label(master = self.window,
              width = 20,
              text = "+ {}:".format(labels["new_ep"][self.lang])
              ).grid(column = 1,
                     row = 1,
                     padx = 3,
                     pady = 5,
                     sticky = EW)

        Entry(master = self.window,
              width = 20,
              textvariable = self.inputval
              ).grid(column = 2,
                     row = 1,
                     padx = 3,
                     pady = 5,
                     sticky = W)

        Button(self.window,
               text = txtbutton['but_take'][self.lang],
               width = 20,
               command = self.__add).grid(column = 3, row = 1)

        Label(master = self.window,
              width = 20,
              textvariable = self.statbar,
              relief = SUNKEN
              ).grid(column = 0,
                     row = 3,
                     pady = 10,
                     columnspan = 4,
                     sticky = EW)

        self.statbar.set(screenmesg["input_eps"][self.lang])


    def __add(self):
        '''
        This method adds new EPs to character's old EP count.
        '''
        newep = int(self.inputval.get())
        self._character["exp"] += newep
        self.epval.set("EP: {}".format(self._character['exp']))
        # calc new level if any
        self._character['lvl'] = int(getLvl(self._character['exp']))
        self.lvlval.set("{}: {}".format(labels["lvl"][self.lang], self._character['lvl']))
        #save new EP data
        self.saveData()
        self.statbar.set(screenmesg["file_saved"][self.lang])



class BGOselectWin(blankWindow):
    '''!
    This window class will display the choices one have for his BGOs
    @todo The following has to be impemented
    - window building
    - special items
    - more money
    - spec Bonus Cat/Skill
    - Edges/Flaws
    '''


    def __init__(self, lang = 'en', storepath = os.getcwd() + "/data", char = None):
        """!
        Class constructor BGOselectWin
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param title title of the window
        @param storepath path where things like options have to be stored
        @param char Character as JSON/dictionary
        """

        if storepath == None:
#            self.spath = os.path.expanduser('~') + "/data"
            self.spath = os.getcwd() + "/data"
            logger.debug('Set storepath to %s' % (storepath)) + "/data"

        else:
            self.spath = storepath
            logger.debug('editEPWin: storepath set to %s' %
                         (storepath))
        self.lang = lang
        self._character = dict(calcTotals(char))

        self.mypath = storepath + '/' + self._character['player'] + '/'
        self.cmask = [txtwin['json_files'][self.lang],
                     txtwin['grp_files'][self.lang],
                     txtwin['all_files'][self.lang]
                     ]

        blankWindow.__init__(self, self.lang)
        self.window.title("%s - %s (%s)" % (wintitle['rm_statgain'][self.lang],
                                            self._character['name'],
                                            self._character['prof']
                                            )
                          )
        self.filemenu = Menu(master = self.menu)
        self.__addFileMenu()
        self.__addSelectMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addFileMenu(self):
        '''
        Adds a file menu to menu bar.
        '''
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)

        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__openFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)

        self.__stats = stats


    def __addEditMenu(self):
        '''!
        This adds an select menu to the menu bar.
        @todo to be implemented:
        -# extra money
        -# stat gain rolls
        -# extra items
        -# languages
        -# spec skill
        -# spec cats
        -# talents/flaws
        '''
        self.edtmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_select'][self.lang],
                              menu = self.edtmenu)
        self.edtmenu.add_command(label = submenu['select'][self.lang]['bgo_money'],
                                 command = self.notdoneyet)
        self.edtmenu.add_command(label = submenu['select'][self.lang]['bgo_stats'],
                                 command = self.notdoneyet)
        self.edtmenu.add_command(label = submenu['select'][self.lang]['bgo_items'],
                                 command = self.notdoneyet)
        self.edtmenu.add_command(label = submenu['select'][self.lang]['bgo_lang'],
                                 command = self.notdoneyet)
        self.edtmenu.add_command(label = submenu['select'][self.lang]['bgo_spec_skill'],
                                 command = self.notdoneyet)
        self.edtmenu.add_command(label = submenu['select'][self.lang]['bgo_spec_cat'],
                                 command = self.notdoneyet)
        self.edtmenu.add_command(label = submenu['select'][self.lang]['bgo_talens'],
                                 command = self.notdoneyet)


    def __addHelpMenu(self):
        '''
        Adds a help menu entry to menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['win'],
                                  command = self.__helpWin)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
        self.window = MainWindow(lang = self.lang, char = self._character)


    def __openFile(self):
        """
        This method opens a dialogue window (Tk) for opening files.
        The content of the opened file will be saved in \e file
        \e content as an array.
        """
        self.__filein = askopenfilename(filetypes = self.cmask,
                                        initialdir = self.mypath)
        if self.__filein != "":
            with open(self.__filein, 'r') as filecontent:

                if self.__filein[-4:].lower() == "json":
                    self.char = json.load(filecontent)

                elif self.__filein[-3:].lower == "grp":
                    self.grp = json.load(filecontent)

                else:
                    msg = messageWindow()
                    msg.showinfo(errmsg['wrong_type'][self.lang])
                    logger.warn(errmsg['wrong_type'][self.lang])
                    pass


    def __helpWin(self):
        '''!
        Help windows
        @todo this has to be fully implemented
        '''
        self.notdoneyet("charInfo.__helpWin:\ņ\n not done yet")


    def __buildWin(self):
        '''!
        This method builds all window components
        @todo This has to be fully implemented.
        '''
        self._f_money = Frame(master = self.window)

