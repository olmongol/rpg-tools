#!/usr/bin/env python
'''
\file gui/epWins.py
\package gui.epWins
\brief Windows classes for epcalc gui


\date (C) 2017
\author Marcus Schwamberger
\email marcus@lederzeug.de

'''
import os
import sys
from Tkinter import *
from ImageTk import *
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
    def __init__(self, lang = 'en', storepath = None, title = "Main Window"):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param title title of the window
        \param storepath path where things like options have to be stored
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

        blankWindow.__init__(self, self.lang)
        self.window.title(title)
        Label(self.window, width = 60).pack()
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addOptionMenu()
        self.__addHelpMenu()

        self.mask = [txtwin['exp_files'][self.lang],
                    txtwin['all_files'][self.lang]
                    ]

        """
        set picture for the window background of the main window
        """
        self.__canvas = Canvas(self.window, width = '8.0c', height = '8.5c')
        __background = PhotoImage(file = self.picpath + 'skeleton.gif')
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

    def __saveFile(self):
        '''
        This method opens a file dialogue window (Tk) for saving the results
        of the EP calculation into an EXP file.
        '''
        self.notdoneyet("'saveFile'")

    def __saveCSV(self):
        '''
        This method saves the entered data as CSV file
        '''
        self.notdoneyet()

    def __openCSV(self):
        '''
        This method opens an existing EP CSV file.
        '''
        self.notdoneyet()

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
        print "MainWindow edcharWin"
        
        self.window.destroy()
        self.window = edtchrWin(self.lang)
#        self.notdoneyet()

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
        blankWindow.__init__(self, self.lang)
        self.window.title(wintitle['opt_lang'][self.lang])
        self.wert = StringVar()
        self.index = sortIndex(shortcut)
        self.__buildWinRadio()

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
        self._cnf = chkCfg(lang = self.lang)

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

        Label(master = self.window,
              width = 25
              ).pack()

        self.rb = {}

        for key in self.index:
            self.rb[key] = Radiobutton(master = self.window,
                           text = shortcut[key],
                           variable = self.wert,
                           value = key
                           )

            if key == self.lang:
                self.rb[key].select()

            self.rb[key].pack()

        Label(master = self.window,
              width = 35
              ).pack()

        Label(master = self.window,
              width = 35,
              text = labels['cfg_path'][self.lang]
              ).pack()

        Entry(master = self.window,
              width = 35,
              textvariable = self.sto_path
              ).pack()

        Label(master = self.window,
              width = 35
              ).pack()

        Label(master = self.window,
              width = 35,
              text = labels['log_path'][self.lang]
              ).pack()

        Entry(master = self.window,
              width = 35,
              textvariable = self.log_path
              ).pack()

        Button(self.window,
               text = txtbutton['but_sav'][self.lang],
               width = 15,
               command = self.__save).pack()

        Button(self.window,
               text = txtbutton['but_clos'][self.lang],
               width = 15,
               command = self.__closewin).pack()

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

        if  self.path[-1:] != '/':
            self.path += '/'

        if self.log[-1:] != '/':
            self.log += '/'

        self.cont = {'lang'     : self.lang,
                     'datapath' : self.path,
                     'logpath'  : self.log
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
        self.__canvas = Canvas(self.window, width = '7.8c', height = '8.5c')
        __background = PhotoImage(file = self.picpath + 'dragon.gif')
        self.__canvas.create_image(0, 0, image = __background, anchor = NW)
        self.__canvas.pack()
               
        self.window.mainloop()

        
    def __createchar(self):
        '''
        Method to create a new character
        \todo createchar has to be implemented
        '''
        print "input win --> createchar"
        self.notdoneyet('chreatechar')
        
    def __creategroup(self):
        '''
        Method to create a now character party/group
        \todo chreategroup has to be implemented
        '''
        print "input win --> ccreategroup"
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
        
#    def _addHelpMenu(self):
#        """
#        This method adds additional functions to the help menu
#        """
#        self.helpmenu = Menu(master = self.menu)
#        self.menu.add_cascade(label = txtmenu['help'][self.lang],
#                              menu = self.helpmenu)
#        self._templist = {'not done': self.notdoneyet()
#                         }
#        for key in s_elem_def:
#            
#            if key not in self._templist:
#                self._templist[key] = self.notdoneyet(key)
#            
#            self.com = self._templist[key]
#            self.helpmenu.add_command(label = key,
#                                      command = self.com)
#        del(self._templist)
#        del(key)
#
#        self.helpmenu.add_separator()
#        self.helpmenu.add_command(label = submenu['help'][self.lang]['page'],
#                                  command = self._showPage)
#        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
#                                  command = self._helpAbout)

class edtchrWin(blankWindow):
    '''
    Window class to generate/edit player character values.    
    '''
    def __init__(self, lang = 'en', storepath = './data'):
        '''
        \param lang Choosen display language (default en)
        \param storepath Path to store data (default: ./data)
        '''
        
        self.lang = lang
        self.spath = storepath
        
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
        Adding new charaters to the list
        \todo csv saving has to be implemented
        \bug there are data missing while writing new dataset to file
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
