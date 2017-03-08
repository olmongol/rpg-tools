#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
\file gui/epWins.py
\package gui.epWins
\brief Windows classes for epcalc gui


\date (C) 2017
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
import random
import os
import sys
from Tkinter import *
from PIL.ImageTk import *
from tkFileDialog import *
from ttk import *
from rpgtoolbox.lang import *
from rpgtoolbox.globaltools import *
from rpgtoolbox import logbox as log
from rpgtoolbox.errbox import *
from rpgtoolbox.confbox import *
from rpgtoolbox.rpgtools import getLvl
from gui.winhelper import AutoScrollbar
from gui.winhelper import InfoCanvas
from gui.window import *
from rpgtoolbox.rolemaster import stats
import json
__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015-2017 " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "1.0"
__license__ = "GNU V3.0"
__me__ = "A RPG tool package for Python 2.7"

logger = log.createLogger('window', 'debug', '1 MB', 1, './')

class MainWindow(blankWindow):
    """
    This is the class for the main window object.
    \param lang The chosen language for window's and button's texts. At
                the moment, only English (en, default value) and German
                (de) are supported.
    \param title title of the window
    \param storepath path where things like options have to be stored
    """
    def __init__(self, lang = 'en', storepath = None, title = "Main Window",
                 char = None):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param title title of the window
        \param storepath path where things like options have to be stored
        \param char Character as JSON
        """
        if storepath == None:

            self.mypath = os.path.expanduser('~')
            logger.debug('Set storepath to %s' % (storepath))

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
        with open(self.__filein, 'r') as filecontent:
            if self.__filein[-4:].lower() == "json":
                self.char = json.load(filecontent)
            elif self.__filein[-3:].lower == "grp":
                self.grp = json.load(filecontent)
            else:
                msg = messageWindow()
                msg.showinfo(errmsg['wrong_type'][self.lang])
                pass

    def __saveFile(self):
        '''
        This method opens a file dialogue window (Tk) for saving the results
        of the EP calculation into an .json or .grp file.
        \todo has to be implemented
        '''
        self.notdoneyet("'saveFile'")

#    def __saveCSV(self):
#        '''
#        This method saves the entered data as CSV file
#        '''
#        self.notdoneyet()
#
#    def __openCSV(self):
#        '''
#        This method opens an existing EP CSV file.
#        '''
#        self.notdoneyet()

    def __addEditMenu(self):
        '''
        This method adds an edit menu to the menu bar
        \todo add all entries.
        '''
        self.edtmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_edit'][self.lang],
                              menu = self.edtmenu)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_char'],
                                 command = self.__edcharWin)
        self.edtmenu.add_separator()
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_fight'],
                                 command = self.__edfightWin)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_other'],
                                  command = self.__edotherWin)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_indiv'],
                                  command = self.__indivWin)
        self.edtmenu.add_command(label = submenu['edit'][self.lang]['ed_calc'],
                                 command = self.__edcalcWin)

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
#        self.window = edtchrWin(self.lang)
#        self.notdoneyet()

    def _edtgrpWin(self):
        """
        Opens a window for editing character parties
        \todo edtgrpWin has to be implemented
        """
        self.notdoneyet("edtgrpWin")
        
    def __edfightWin(self):
        '''
        Editing all Hits/Crits/Killed Monsters for calculating EPs
        '''
        self.notdoneyet()

    def __edotherWin(self):
        '''
        Editing all for traveled distance, spells, maneuvers
        '''
        self.notdoneyet()

    def __indivWin(self):
        '''
        Calculating and distributing pool for individual EPs.
        '''
        self.notdoneyet()
#        self.window.destroy()
#        self.window = inputWin(self.lang)

    def __edcalcWin(self):
        '''
        Calculating and displaying the whole EPs for the RPG party.
        '''
        self.notdoneyet()

    def __addGMMenu(self):
        """
        This method adds a Gamemaster Menu for generating special stuff like
        treasures or magical items.
        """
        self.gmmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_gm'][self.lang],
                              menu = self.gmmenu)
        self.gmmenu.add_command(label = submenu['items'][self.lang]['treasure'],
                                command = self.__createTreasure)
        self.gmmenu.add_command(label = submenu['items'][self.lang]['magical'],
                                command = self.__createMagic)
        
    
    def __createTreasure(self):
        """
        This method opens a window for treasure generation.
        \todo createTreasure has to be implemented
        """
        self.notdoneyet("createTreasure")
        
    def __createMagic(self):
        """
        This method opens a window for generation of magical items
        \todo createMagic has to be implemented
        """
        self.notdoneyet("createMagic")
    
    
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

    def helpHandbook(self):
        """
        This method will show the rpg-tools Handbook
        \todo this needs to be implemented
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
    """
    This class builds a window for selecting and saving options of
    rpg-tools. For now it is just choosing the language for menus and
    dialogues.
    \param lang Laguage which shall be used in messages and menus.
    """
    def __init__(self, lang = 'en'):
        """
        Class constructor
        \param lang Laguage which shall be used in messages and menus
        """
        self.lang = lang
        self._cnf = chkCfg(lang = self.lang)
        
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
        if 'rpg' in self._cnf.cnfparam.keys():
            self.RPG.set(self._cnf.cnfparam['rpg'])
        else:
            self.RPG.set('Rolemaster')
        
        self.optMenu = apply(OptionMenu, (self.window, self.RPG) + tuple(supportedrpg[self.lang]))
        self.optMenu.grid(column = 0, row = 0)
        
        
    def __buildWinRadio(self):
        """
        This private method builds the option's window with radio
        buttons of supported languages dynamically.
        \todo switch language chooser from radio buttons to pull-down
              menu
        \todo Switch from pack() to .grid()
        """
        self.sto_path = StringVar()
        self.log_path = StringVar()

        if 'path' in self._cnf.cnfparam.keys():
            self.sto_path.set(self._cnf.cnfparam['datapath'])
  
        else:
            self.sto_path.set("./data")

        if 'lang' in self._cnf.cnfparam.keys():

            if self._cnf.cnfparam['lang'] != self.lang:
                self.lang = self._cnf.cnfparam['lang']

        if 'log' in self._cnf.cnfparam.keys():
            self.log_path.set(self._cnf.cnfparam['log'])

        else:
            self.log_path.set("/tmp/")

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
        """
        A method for saving options in the user directory.
        \todo variables to store have to be completed/adapted
        """
        self.lang = self.wert.get()
        self.path = self.sto_path.get()
        self.log = self.log_path.get()
        self.crpg = self.RPG.get()

        if  self.path[-1:] != '/':
            self.path += '/'

        if self.log[-1:] != '/':
            self.log += '/'

        self.cont = {'lang'     : self.lang,
                     'datapath' : self.path,
                     'logpath'  : self.log,
                     'rpg'      : self.crpg
                     }
        logger.debug('SAVE: lang=%s; datapath=%s; logpath=%s' % (self.lang, self.path, self.log))
        self._cnf.saveCnf(path = './conf',
                          filename = 'rpg-tools.cfg',
                          content = self.cont)

        self.msg = messageWindow()
        self.msg.showinfo(processing['saved'][self.lang] + '\n' + shortcut[self.lang])

    def __closewin(self):
        """
        A method for closing the window and opening the main window.
        \todo give RPG type to main window
        """
        self.path = self.sto_path.get()
        self.window.destroy()
        self.window = MainWindow(self.lang, self.path)

class inputWin(blankWindow):
    """
    Objects of this class type are windows for input the wanted data
    structure. A exp structure will be build of the input.
    \param lang This parameter holds the language chosen for the menus
                and messages. Default value is 'en'.
    \param filename this holds the filename of a read exp file holding
                    the functional structure.
    \param storepath the path where the XML files shall be stored in.
    """
    def __init__(self,
                 lang = 'en',
                 csvcontent = {},
                 filename = None,
                 storepath = None):
        """
        Constructor
        \param lang This parameter holds the language chosen for the
                    menus and messages. Default value is 'en'
        \param csvcontent a dictionary holding the information of CSV
        \param filename this holds the filename and path of a read data
                        file containing the functional structure.
        \param storepath the path where the data files shall be stored
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
        
#        self.window = Tk()
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
#        print "input win --> createchar"
        self.window.destroy()
        self.window3 = genAttrWin(lang = self.lang,
                                 storepath = self.mypath)
       
    def __creategroup(self):
        '''
        Method to create a now character party/group
        \todo chreategroup has to be implemented
        '''
        print "input win --> creategroup"
        self.notdoneyet('creategroup')
        
        
    def __editchar(self):
        '''
        Method to edit a character for the EP sheet.
        \todo editchar is to be implemented
        '''
        print "input win -->  editchar"
        self.notdoneyet('editchar')

    def __editgrp(self):
        '''
        Method to edit a character group and keep track on it
        \todo editgrp has to be implemented
        '''
        self.notdoneyet("editgrp")
        
    def __epfight(self):
        '''
        Method to calculate EPs from a fight (hits and criticals)
        \todo epfight has to be implemented
        '''
        self.notdoneyet('epfight')

    def __epother(self):
        '''
        Method to calculate EPs from Spells, maneuvers, travel.
        \todo epother has to be implemented
        '''
        self.notdoneyet('epother')

    def __epindiv(self):
        '''
        Method for adding invidual EPs
        \todo epindiv has to be implemented
        '''
        self.notdoneyet('epindiv')

    def __epcalc(self):
        '''
        Method to finalize EP calculation for a single gaming date
        \todo epcalc has to be implemented
        '''
        self.notdoneyet('epcalc')
          
    def __fightsim(self):
        '''
        Method for simulating a fight and calculate potential EPs
        \todo fightsim has to be implemented
        '''
        self.notdoneyet('fightsim')

    def __closewin(self):
        """
        Method for closing the window and opening the main window.
        """
        self.window.destroy()
        self.window = MainWindow(self.lang, self.mypath)

    def __helppage(self):
        """
        Method for help on this page.
        \todo helppage has to be implemented
        """
        self.notdoneyet("helppage")
        
    def __helpglobal(self):
        """
        Method to call the handbook as help for this page
        """
        self.handbook("chapter %s" % (wintitle['edit'][self.lang]))
        

class edtchrWin(blankWindow):
    '''
    Window class to generate/edit player character values.  
    \note This may become deprecated soon...  
    '''
    def __init__(self, lang = 'en', storepath = './data'):
        '''
        \param lang Choosen display language (default en)
        \param storepath Path to store data (default: ./data)
        '''
        
        self.lang = lang
        self.spath = storepath
        if self.spath[-1] != "/":
            self.spath += "/"
            
        blankWindow.__init__(self, lang = self.lang)
        
        self.window.title(wintitle['calc_exp'][self.lang] + " - Chars")
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.notdoneyet)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)       
        
        self.groups = readCSV(self.spath + '/groups.csv')
        self.stat = readCSV(self.spath + '/statistics.csv')
        self.charlist = []
        self.playerlist = []
        
        for lmnt in self.stat:
            self.charlist.append(lmnt['Name'])
            self.playerlist.append(lmnt['Player'])
            
        self.grouplist = []
        
        for lmnt in self.groups:
            if lmnt['Group'] not in self.grouplist:
                self.grouplist.append(lmnt['Group'])
            
        self.__createWinStruc()    
        
            
    def __createWinStruc(self):
        """
        This method creates the window structure with list and message 
        boxes. The created window is for reading, generating and 
        editing of elements of the functional structure.
        """

        self._cboxes = {'Name'  : self.charlist,
                       'Group'  : self.grouplist,
                       'Player' : self.playerlist,
                       }
       
        labels = self.stat[0].keys()
        labels.append("Group")
        labels.sort()      
        
        self._fields = {}

        r = 1
        self._set = {}
        
        for l in labels:
            l = l.strip(' \n')
            self._set[l] = ""
            Label(master = self.window,
                  width = 20,
                  text = csvlabels[l][self.lang]
                  ).grid(row = r, column = 0)            
            
            if l in ['Name', 'Group', 'Player']:

                self._fields[l] = Combobox(master = self.window,
                                           width = 30,
                                           textvariable = self._set[l],
                                           values = self._cboxes[l]
                                           )
                self._fields[l].grid(row = r, column = 1)
            else:
                self._fields[l] = Entry(master = self.window,
                                        textvariable = self._set[l],
                                        width = 32
                                        )
                self._fields[l].grid(row = r, column = 1)

            r += 1
            
        Button(master = self.window,
              text = txtbutton['but_take'][self.lang],
              command = self._addItems
              ).grid(row = 0, column = 1)    
              
        Button(master = self.window,
              text = txtbutton['but_refr'][self.lang],
              command = self._refrItems
              ).grid(row = 0, column = 0)                         
                    
    def _refrItems(self):
        '''
        Refreshes selected data sets
        \todo has to be implemented
        '''
        dummy = self._fields['Name'].get()

        for i in range(0, len(self.stat)):
        
            if self.stat[i]['Name'] == dummy:
            
                for k in self.stat[i].keys():
                    self._fields[k].delete(0, END)
                    self._fields[k].insert(0, self.stat[i][k])
                    self._set[k] = self.stat[i][k]
                break
            else:
                
                for k in self.stat[i].keys():
                    self._set[k] = self._fields[k].get()
                    
        for lmnt in self.groups:
            
            if lmnt['Name'] == self._set['Name']:
                self._set['Group'] = lmnt['Group']
                self._fields['Group'].delete(0, END)
                self._fields['Group'].insert(0, lmnt['Group'])
                break
            
            else:
                self._set['Group'] = self._fields['Group'].get()
            
                    
        for k in self._set.keys():  
            print (k, self._set[k]) 
        print "*********************"
        
        
    def _addItems(self):
        '''
        Adding new characters to the list
        '''   
        print "addItems"
        for k in self._set.keys():  
            print (k, self._set[k]) 
        print "=============== "
        dummy = self._set['Name']
        
        for i in range(0, len(self.groups)):
            if dummy == self.groups[i]['Name']:
                self.groups[i]['Group'] = self._set['Group']
                del(self._set['Group'])
                break
                
        if 'Group' in self._set.keys():
            self.groups.append({'Name' : dummy, 'Group': self._set['Group']})
            self.grouplist.append(self._set['Group'])
            del(self._set['Group'])
 
        for i in range(0, len(self.stat)):
            if dummy == self.stat[i]['Name']:
                for k in self.stat[i].keys():
                    self.stat[i][k] = self._set[k]
                self.playerlist.append(self._set['Player'])
                self.charlist.append(dummy)
                del(self._set['Name'])
                break
            
        if 'Name' in self._set.keys():
            self.stat.append(self._set)

        writeCSV(self.spath + "/statistics.csv", self.stat)
        logger.info("epwin: wrote statistics.csv")
        writeCSV(self.spath + "/groups.csv", self.groups)
        logger.info("epwin: wrote groups.csv")
        

    def __closewin(self):
        """
        Method for closing the window and opening the main window.
        """
        self.window.destroy()
        self.window = MainWindow(self.lang, self.spath)

    def _addHelpMenu(self):
        """
        This method adds additional functions to the help menu
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self._templist = {'not done': self.notdoneyet()
                         }
        for key in s_elem_def:
            self.com = self._templist[key]
            self.helpmenu.add_command(label = key,
                                      command = self.com)
        del(self._templist)
        del(key)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['page'],
                                  command = self._showPage)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


class genAttrWin(blankWindow):
    '''
    A window class for generating name, race, profession and attributes of a new
    character.
    '''
    def __init__(self, lang = 'en', storepath = './data', rpg = "RoleMaster"):
        '''
        \param lang Choosen display language (default en)
        \param storepath Path to store data (default: ./data)
        \todo add OptionMenu for culture choice for mixed men and common men.
        '''
        
        if rpg == "RoleMaster":
            from rpgtoolbox import rolemaster as rm

        else:
            self.notdoneyet("support for %s" % (rpg))

        ## \var self.character
        # the attribute where to store the character data in as 'JSON'
        self.character = {}
        ## \var self.lang
        # used language
        self.lang = lang
        ## \var self.spath
        # storage path for character data file
        self.spath = storepath
        
        if self.spath[-1] != "/":
            self.spath += "/"
        
        self.__cultures = rm.cultures[self.lang][:6]
        ## \var self.profs
        # a dictionary/JSON structure where a profession specific data (read from 
        # a CSV file) is stored in 
        self.profs = rm.choseProfession(self.lang)
        ## \var proflist
        # list of all available professions
        proflist = self.profs.keys()
        ## \var rmraces
        # a list of all the RoleMaster races
        rmraces = rm.races[self.lang]
        ## \var rmcultures
        # list of available cultures
        rmcultures = rm.cultures[self.lang]
        ## \var self.stats
        # holds player, name, profession, race, realm and temp stats
        self.stats = {}
        ## \var self.pots
        # holds potential stats (maximum values)
        self.pots = {}
        ## \var self.specs
        # holds special stats if anyrger 
        self.specs = {}
        ## \var self.__race
        # holds race stats bonuses
        self.__race = {}
        ##\var self.__rr
        # holds all resistance roll bonusses
        self.__rr = {}
        self.__labels = {}
        ## \var self..__totals
        # holds total stat bonusses
        self.__totals = {}
        ## \var self.__std
        #  holds standard stat bonusses
        self.__std = {}
        self.__count = 0
        ##\var self.__rmstats
        # list of all stats' short cuts in English
        self.__rmstats = rm.stats
        ##\var self.__rangeOK
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
                                
        Label (master = self.window,
               width = 15,
               relief = RIDGE,
               font = "bold",
               text = rm.labels[self.lang]['stats']
               ).grid(column = 0, row = 4, sticky = "ew")
               
        Label (master = self.window,
               width = 10,
               relief = RIDGE,
               font = "bold",
               text = rm.labels[self.lang]['short']
               ).grid(column = 1, row = 4)       
               
        Label (master = self.window,
               width = 10,
               relief = RIDGE,
               font = "bold",
               text = "Temp"
               ).grid(column = 2, row = 4, sticky = "ew")
               
        Label (master = self.window,
               width = 10,
               relief = RIDGE,
               font = "bold",
               text = "Pot"
               ).grid(column = 3, row = 4, sticky = "ew")
               
        Label (master = self.window,
               width = 10,
               relief = RIDGE,
               font = "bold",
               text = rm.labels[self.lang]['race']
               ).grid(column = 4, row = 4, sticky = "ew")
                
        Label (master = self.window,
               width = 10,
               relief = RIDGE,
               font = "bold",
               text = "Spec"
               ).grid(column = 5, row = 4, sticky = "ew")
               
        Label (master = self.window,
               width = 10,
               relief = RIDGE,
               font = "bold",
               text = "Std"
               ).grid(column = 6, row = 4, sticky = "ew")

        Label (master = self.window,
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
            total = self.__race[s].get() + self.specs[s].get() + self.__std[s].get()
            self.__totals[s].set(total)
            stat = self.stats[s].get()
            self.__used += stat
            self.pots[s].set(self.__creatPot(stat))

        if self.__used > self.points:
            self.showno.set(self.points - self.__used)
            messageWindow(self.lang).showinfo(errmsg['too_much_stats'][self.lang])
        
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
                    messageWindow(self.lang).showinfo(errmsg['wrong_stat'][self.lang] + "\n%s --> 20" % s)
            
            for s in primestats:
                
                if self.stats[s.strip('*')].get() < 90:
                    self.__rangeOK = False
                    self.stats[s.strip('*')].set(90)
                    messageWindow(self.lang).showinfo(errmsg['wrong_stat'][self.lang] + "\ns %s --> 90 " % s)
             
    def __setPStats(self):
        '''
        Sets the primary (and magic) stats for a profession
        \todo set the magic stat for chosen realms to semi spell users
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
                omenu.add_command(label = cult, command = lambda v = cult: self.stats['culture'].set(v))
                self.stats['culture'].set("")
                
        else:
            omenu.add_command(label = testr, command = lambda v = testr: self.stats['culture'].set(v))
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
        '''
        This method checks whether the right magic realm is chosen for the 
        selected profession
        \param event object event given by OptionMenu but not used 
        \bug potential cause for false DP calculations. It is not clear how to 
        reproduce this bug.
        \bug  if testr != self.profs[testp]['Realm'] and self.profs[testp]['Realm'] != "choice": KeyError: ''
        \bug if realm chosen before profession an error occurs (sdtout) 
        \note bug should be fixed
        '''
        testr = self.stats['realm'].get()
        testp = self.stats['prof'].get()
        if testp != "":
            if testr != self.profs[testp]['Realm'] and self.profs[testp]['Realm'] != "choice":
                self.stats['realm'].set(self.profs[testp]['Realm'])
        self.__setPStats()
        self.__calcBonus()
            
    def __setRBonus(self, event):
        '''
        This method sets the races bonusses , the race based RR bonusses, 
        Background Options and Hobby Ranks. 
        \param event object event given by OptionMenu but not used 
        '''
        from rpgtoolbox import rolemaster as rm
        race = self.stats['race'].get()
        pos = rm.races[self.lang].index(race)
        race = rm.races['en'][pos]
        
        for i in rm.raceAbilities[race].keys():
            if "RR" in i:
                self.__rr[i] = rm.raceAbilities[race][i]
                
        self.character['BGO'] = rm.raceAbilities[race]['BGO']
        self.character['Hobby Ranks'] = rm.raceAbilities[race]['Hobby Ranks']

        for a in rm.stats:
            self.__race[a].set(rm.raceAbilities[race][a])
        
        self.__setCulture("")
        
    def __setRealm(self, event):
        '''
        Sets the connected Realm if profession is chosen
        \param event object event given by OptionMenu but not used 
        '''
        testp = self.stats['prof'].get()    
        self.stats['realm'].set(self.profs[testp]['Realm'])
        self.__setPStats()
        
    def __creatPot(self, temp = 20, fixed = False):
        '''
        This method creates a potential stat from a temporary stat.
        \param temp value of the temporary stat
        \param fixed a parameter that turns the fixed creation mode on/off
        \retval result the resulting potential stat value
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
        '''
        This function delivers the result of a dice roll as a list.
        \param sides number of sides of the used dice
        \param number number of used dices/rolls
        \retval result sum of the dice rolls
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
        Creates the pool for stat generation
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
            
        race = rm.races['en'][rm.races[self.lang].index(self.character['race'])]    
        
        for stat in self.__rmstats:
            self.character[stat] = {}
            self.character[stat]['name'] = rm.labels[self.lang][stat]
            self.character[stat]['temp'] = self.stats[stat].get()
            self.character[stat]['pot'] = self.pots[stat].get()
            self.character[stat]['race'] = self.__race[stat].get()
            self.character[stat]['spec'] = self.specs[stat].get()
            self.character[stat]['std'] = self.__std[stat].get()
            self.character[stat]['total'] = self.__totals[stat].get()
            
        self.character['RREss'] = self.character['Em']['total'] * 3 + rm.raceAbilities[race]['RREss']
        self.character['RRChan'] = self.character['In']['total'] * 3 + rm.raceAbilities[race]['RRChan']
        self.character['RRMent'] = self.character['Pr']['total'] * 3 + rm.raceAbilities[race]['RRMent']
        self.character['RRArc'] = self.character['Pr']['total'] + self.character['Em']['total'] + self.character['In']['total']
        self.character['RRC/E'] = self.character['In']['total'] + self.character['Em']['total'] + (rm.raceAbilities[race]['RREss'] + rm.raceAbilities[race]['RRChan']) / 2
        self.character['RRC/M'] = self.character['In']['total'] + self.character['Pr']['total'] + (rm.raceAbilities[race]['RRMent'] + rm.raceAbilities[race]['RRChan']) / 2
        self.character['RRE/M'] = self.character['Pr']['total'] + self.character['Em']['total'] + (rm.raceAbilities[race]['RREss'] + rm.raceAbilities[race]['RRMent']) / 2
        self.character['RRDisease'] = self.character['Co']['total'] * 3 + rm.raceAbilities[race]['RRDisease']
        self.character['RRPoison'] = self.character['Co']['total'] * 3 + rm.raceAbilities[race]['RRPoison']
        self.character['RRFear'] = self.character["SD"]['total'] * 3
        self.character['purse'] = {'GP' : 2,
                                  'SP' : 0,
                                  'CP' : 0,
                                  'TP' : 0,
                                  'IP' : 0}
        self.character['old_exp'] = 0
        self.character['exp'] = 10000
        self.character['lvl'] = 1
        
        self.__addCatnSkills()
        
        if not os.path.exists(self.spath + self.character['player']):
            os.mkdir(self.spath + self.character['player'])
       
        else:
            with open(self.spath + self.character['player'] + '/' + self.character['name'] + ".json", "w") as outfile:
                json.dump(self.character, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
            self.window.destroy()
            self.window3 = priorizeWeaponsWin(self.lang, self.spath, self.character)

    
    def __addCatnSkills(self):
        '''
        This method adds skill categories and skills to the character's dictionary
        as well as bonus (special, profession and items)
        \note Skills wont have a profession bonus. It is already applied to the 
        category.
        \todo replace progession expression with number list for ALL skills and 
        categories
        
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
            skillcat[content[i][0]] = {content[0][2] : content[i][2],
                                     content[0][1] : {},
                                     'spec bonus' :0,
                                     'prof bonus' :0,
                                     'item bonus' :0,
                                     'rank' : 0
                                     }  ##XXX rank insterted
            for pb in self.profs[self.character['prof']]['Profession Bonusses'].keys():
                 
                if pb in content[i][0]:
                    skillcat[content[i][0]]['prof bonus'] = self.profs[self.character['prof']]['Profession Bonusses'][pb]
            
            skillcat[content[i][0]][content[0][1]] = {}    
            
            for skill in content[i][1].split(';'):
                skillcat[content[i][0]][content[0][1]][skill] = {content[0][2] : content[i][2],
                                                                   'rank' : 0,
                                                                   'rank bonus' : 0,
                                                                   'item bonus' :0,
                                                                   'spec bonus' : 0,
                                                                  }
                
        del(content)
        
        fp = open('%s/default/SkillCat_%s.csv' % (self.spath, self.lang), 'r')
        content = fp.readlines()
        fp.close()
          
        content[0] = content[0].strip("\n").split(',')
        
        for  i in range(1, len(content)):
            content[i] = content[i].strip('\n').split(',')
            
            if content[i][0] not in skillcat.keys():
                skillcat[content[i][0]] = {'rank' : 0,
                                           'rank bonus' : 0,
                                           'item bonus' : 0,
                                           'spec bonus' : 0
                                           }
                skillcat[content[i][0]]['Skill'] = {'rank' : 0,
                                                    'rank bonus' : 0,
                                                    'item bonus' : 0,
                                                    'spec bonus' : 0
                                                    }
     
            skillcat[content[i][0]][content[0][2]] = content[i][2]
            skillcat[content[i][0]]["Skill"][content[0][2]] = content[i][2]
            skillcat[content[i][0]][content[0][1]] = content[i][1].split('/')
# this commented out code should avoid Stats in Skills
#            skillcat[content[i][0]]["Skill"][content[0][1]] = content[i][1].split('/')                
            
            if rm.catnames[self.lang]['spells'] in content[i][0][:7]:
                temp = []

                if  '[' in self.character['realm']:
                    self.character['realm'] = self.character['realm'].strip("'[ ]\n").split("', '")
                
                if type(self.character['realm']) == type([]):
                    
                    for r in self.character['realm']:
                        temp.append(rm.realmstats[self.lang][r])
                
                elif self.character['realm'] != "choice":
                    temp.append(rm.realmstats[self.lang][self.character['realm']])
                    temp.append(rm.realmstats[self.lang][self.character['realm']])
                
                skillcat[content[i][0]][content[0][1]] = temp
                skillcat[content[i][0]]["Skill"][content[0][1]] = temp
                
        self.character['cat'] = skillcat
        
        
    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
        self.window = MainWindow(lang = self.lang, char = self.character)

class priorizeWeaponsWin(blankWindow):
    """
    This is the class for a window object to chose the priority of weapon skills
    at the character's generation. It will also set the category and skill ranks 
    during adolescence.
    """
    def __init__(self, lang = 'en', storepath = "./data", char = None):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param title title of the window
        \param storepath path where things like options have to be stored
        \param char Character as JSON
        """
        from rpgtoolbox.rolemaster import catnames
        self.__catnames = catnames
        
        if storepath == None:
            self.spath = os.path.expanduser('~') + "/data"
            logger.debug('Set storepath to %s' % (storepath)) + "/data"

        else:
            self.spath = storepath
            logger.debug('priorizeWeaponsWin: storepath set to %s' % (storepath))

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
            self.__prio["%s - %d" % (self.__catnames[self.lang]['weapon'], i)] = StringVar()
            self.__prio["%s - %d" % (self.__catnames[self.lang]['weapon'], i)].set("%s - %d" % (self.__catnames[self.lang]['weapon'], i))
            Label(master = self.window,
                  width = 15,
                  text = "Prio #%d %s" % (i, self.__catnames[self.lang]['weapon'])
                  ).grid(column = 0, row = i)    
        

            self.__optWdg[str(i)] = OptionMenu(self.window,
                                               self.__prio["%s - %d" % (self.__catnames[self.lang]['weapon'], i)],
                                               *self.weaponcats,
                                               command = self.__getPrio)
            self.__optWdg[str(i)].config(width = 50)
            self.__optWdg[str(i)].grid(column = 1, row = i, sticky = "W")
         
        Button(master = self.window,
               text = txtbutton['but_next'][self.lang],
               width = 10,
               command = self.__nextStep).grid(column = 1, row = i + 1, sticky = "E")         
        
    def __getPrio(self, event):
        '''
        This generates the priority list by the chosen priorities.
        \param event has to be catched but is not used
        \todo check for double priorities. If any don't proceed
        \bug when you chose double entries:  File "/home/mongol/git/rpg-tools/src/gui/epwins.py", line 1808, in __getPrio
        for i in range(len(content) - 7, len(content)):
        IndexError: list index out of range
        '''
        self.__priolist = []
        self.__block = False
        
        for i in range(1, 8):
            dummy = self.__prio["%s - %d" % (self.__catnames[self.lang]['weapon'], i)].get()
            
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
                self.__catDBC[self.__content[0][j]][self.__content[i][0]] = self.__content[i][j]
    
    
    def __addToChar(self):            
        '''
        This method adds the concerned developing costs and category/skill ranks
        during adolescence to the character data structure (JSON). 
        It also calculates the rank bonus for the first time.
        \bug exchange progression numbers for Power Point Development does not work 
        \todo concentrate all PPD stats on concerned Power Point Development and delete the others 
        '''
        from rpgtoolbox.rolemaster import races, labels, progressionType, rankbonus, catnames
        ##\var prof
        # dummy variable that holds character's profession
        prof = self.character['prof']
        ##\var crace
        # dummy variable that holds character's race
        crace = races['en'][races[self.lang].index(self.character['race'])]
       
        for skillcat in self.__catDBC[prof].keys():
            if '/' in self.__catDBC[prof][skillcat]:
                dbcdummy = self.__catDBC[prof][skillcat].split('/')
            else: 
                dbcdummy = list(self.__catDBC[prof][skillcat])
            
            for i in range(0, len(dbcdummy)):
                if dbcdummy != "":
                    dbcdummy[i] = int(dbcdummy[i])

            self.character['cat'][skillcat][labels[self.lang]['costs']] = dbcdummy
            self.character['cat'][skillcat]['Skill'][labels[self.lang]['costs']] = dbcdummy


            if self.character['cat'][skillcat]['Progression'] == "Standard":
                self.character['cat'][skillcat]['Progression'] = progressionType['standard cat']
                self.character['cat'][skillcat]['Skill']['Progression'] = progressionType['standard skill']
            
            elif self.character['cat'][skillcat]['Progression'] == "BD":
                self.character['cat'][skillcat]['Progression'] = progressionType['null']
                self.character['cat'][skillcat]['Skill']['Progression'] = progressionType['BD %s' % crace]
            
            elif self.character['cat'][skillcat]['Progression'] == "Null" or self.character['cat'][skillcat]['Progression'] == "Skill Only":
                self.character['cat'][skillcat]['Skill']['Progression'] = progressionType['skill only'] 
                self.character['cat'][skillcat]['Progression'] = progressionType['null']
                
            elif self.character['cat'][skillcat]['Progression'] == "Combined":
                self.character['cat'][skillcat]['Progression'] = progressionType['null']
                self.character['cat'][skillcat]['Skill']['Progression'] = progressionType['combined']
         
                # PPD exchange does not work :( XXXX
                
                
            elif self.character['cat'][skillcat]['Progression'][:4] == "PPD ":        
                self.character['cat'][skillcat]['Progression'] = progressionType['null']
                self.character['cat'][skillcat]['Skill']['Progression'] = progressionType["%s %s" % (self.character['cat'][skillcat]['Skill']['Progression'],
                                                                                                     crace)
                                                                                          ]  
                
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
                                                                    "rank bonus" : rankbonus(rank = int(content[j][i]),
                                                                                             progression = self.character['cat'][content[j][0]]['Progression']
                                                                                             )
                                                                    }
                    lastcat = content[j][0]
                    if "Skill" not in self.__adoranks[content[0][i]][content[j][0]].keys():
                        self.__adoranks[content[0][i]][content[j][0]]['Skill'] = {}
                    
                
                else:
                    self.__adoranks[content[0][i]][lastcat]['Skill'][content[j][0].strip('-')] = {'rank' : int(content[j][i]),
                                                                                                  'rank bonus' : rankbonus(rank = int(content[j][i]),
                                                                                                  progression = self.character['cat'][lastcat]['Skill']['Progression']
                                                                                                                                     )
                                                                                                } 
        if self.lang != "en": 
                    
            race = races['en'][races[self.lang].index(self.character['race'])] 
        else:
            race = self.character['race']           
        
        for cat in self.__adoranks[race].keys():
            self.character['cat'][cat]['rank'] = self.__adoranks[race][cat]['rank']
            self.character['cat'][cat]['rank bonus'] = self.__adoranks[race][cat]['rank bonus']
            
            if self.__adoranks[race][cat]['Skill'] != {}:
                
                for skill in self.__adoranks[race][cat]['Skill'].keys():
                    
                    if skill not in self.character['cat'][cat]['Skill'].keys():
                        self.character['cat'][cat]['Skill'][skill] = {}

                    self.character['cat'][cat]['Skill'][skill]['rank'] = self.__adoranks[race][cat]['Skill'][skill]['rank']
                    self.character['cat'][cat]['Skill'][skill]['rank bonus'] = self.__adoranks[race][cat]['Skill'][skill]['rank bonus']
        
        self.saveChar()    
        
    def __setPPD(self):
        '''
        This sets Power Point Development and removes the category entries for the specific realms.
        \todo has to be implemented 
        '''
        race = self.character
        print "not done yet"
   
    
    def saveChar(self):  
        
        '''
        This method saves the character as JSON file
        '''
        import json
        with open(self.spath + self.character['player'] + '/' + self.character['name'] + ".json", "w") as outfile:
                json.dump(self.character, outfile, sort_keys = True, indent = 4, ensure_ascii = False)          
        
    
    def __getWeaponCats(self):
        '''
        Extracts the weapon categories from character 
        '''
        self.weaponcats = []
        
        for cat in self.character['cat'].keys():
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
                         + 'die Steigerungskosten und mögliche Anzahl der Steigerungen.\n'
                         + '1 ist die höchste und 7 die geringste Priorität.',
                   'en' : 'It is important to priorize the weapon categoies because of '
                         + 'developing costs and levels possible to develop.\n'
                         + '1 is the highest priority and 7 the lowest.'
                   }
        helper = messageWindow()
        helper.showinfo(helptext[self.lang], 'Info')


class skillcatWin(blankWindow):
    """
    This is the class for a window object to chose the priority of weapon skills
    at the character's generation. It will also set the category and skill ranks 
    during adolescence.
    """
    def __init__(self, lang = 'en', storepath = "./data", char = None):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param title title of the window
        \param storepath path where things like options have to be stored
        \param char Character as JSON
        """
        from rpgtoolbox.rolemaster import catnames, rankbonus
        self.__catnames = catnames
        self.__rankbonus = rankbonus
        
        if storepath == None:
            self.spath = os.path.expanduser('~') + "/data"
            logger.debug('Set storepath to %s' % (storepath)) + "/data"

        else:
            self.spath = storepath
            logger.debug('priorizeWeaponsWin: storepath set to %s' % (storepath))

        self.lang = lang
        # just temporary set to en
#        self.lang = "en"
        self.character = char
        
        
        
        blankWindow.__init__(self, self.lang)
        self.window.title("%s - %s (%s)" % (wintitle['edit'][self.lang],
                                         self.character['name'],
                                         self.character['prof']
                                         )
                          )
        self.filemenu = Menu(master = self.menu)
        self.__addFileMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.__buildTree(
                         )
        self.window.mainloop()  
    
    def __addFileMenu(self):
        '''
        Adds a file menu  to menu bar.
        '''
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.notdoneyet)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)    
        
        
    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
        self.window = MainWindow(lang = self.lang, char = self.character)        
        
        
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
        '''
        Builds the window's elements.
        - a frame containing:
            1. treeview widged
            2. vertical (auto)scrollbar linked to the treeview widget
            3. horizontal (auto)scrollbar linked to the treeview widget
        - Labels for specific category/skill values
        - Entry widget for number of level ups for category/skill
        - finalize button to make the change permanent.
        '''
        from rpgtoolbox.rolemaster import labels as rmlabels
        self.__treeframe = Frame(width = 400, height = 600)
        self.__treeframe.grid(column = 0, row = 0, columnspan = 7)
        self.__rmlabels = rmlabels
        self.__treecolumns = []
        for key in ['skill', 'progress', 'costs', 'rank', 'total']:
            self.__treecolumns.append(rmlabels[self.lang][key]) 
            
        self.__tree = Treeview(columns = self.__treecolumns, show = "headings")
        vscroll = AutoScrollbar(orient = "vertical", command = self.__tree.yview)
        hscroll = AutoScrollbar(orient = "horizontal", command = self.__tree.xview)
        self.__tree.configure(yscrollcommand = vscroll.set, xscrollcommand = hscroll.set)
        self.__tree.grid(column = 0, row = 0, sticky = "NEWS", in_ = self.__treeframe)
        vscroll.grid(column = 1, row = 0, in_ = self.__treeframe, sticky = "NS")
        hscroll.grid(column = 0, row = 1, in_ = self.__treeframe)
        
    def __buildTree(self):
        '''
        Fills the treeview widget with skills and categories etc.
        \todo has to be implemented
        '''
        for col in self.__treecolumns:
            self.__tree.heading(col, text = col.title())
            
        # filling content
        # have to proceed here!! XXXXXX
        catID = {}
        catNo = 0
        ckeys = self.character['cat'].keys()
        ckeys.sort()
        for cat in ckeys:
#            catvalues = (cat)
            ### much to do XXXXXXX
            if cat != None:
                print cat
                catID[cat] = self.__tree.insert("",
                                                catNo,
                                                text = cat,
                                                values = (cat,
                                                          self.character['cat'][cat]['Progression'],
                                                          self.character['cat'][cat][self.__rmlabels[self.lang]['costs']],
                                                          self.character['cat'][cat]['rank'],
                                                          
                                                          )
                                                )
#            for skill in self.character['cat'][cat]['Skill']:
#                self.__tree.insert(catID[cat], 
#                                   "end", 
#                                   values = (skill,
#                                                            )
#                                   )
            catNo += 1

    def __selectTreeItem(self, event):
        '''
        Select an item from the treeview list.
        \param event responding treeview event which is not used for anything.
        \todo further computing of selected data
        '''    
        self.__curItem = self.__tree.focus()
        print self.__tree.item(self.__curItem)
        
        
    def calcRanks(self):
        '''
        This method calculate all rank bonus of categories and skills of the character loaded.
        \todo has to be implemented
        '''
        print "not done yet"
        
    def __helpAWin(self):
        '''
        Help information about this window.
        \todo has to be implemented
        '''
        self.notdoneyet("helpAWin")



