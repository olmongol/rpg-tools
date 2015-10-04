#!/usr/bin/env python

'''
\file window2.py
\brief All classes and functions for Tk used for Python 2.6+

This module contains all needed classes/functions to build up a GUI 
with Tk and Python 2.6+ 

\author Marcus Schwamberger
\email Marcus@lederzeug.de
\date (c) 2015
\version 1.0a
'''

__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015 " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "0.5.5 alpha"
__me__ = "A Tkinter window tool package"

import os
import sys
import pydot
from Tkinter import *
from ImageTk import *
from tkFileDialog import *
from toolbox.xmlbox import *
from toolbox.xmltools import *
from toolbox.lang import *
from toolbox.globaltools import *
from toolbox.logbox import *
from toolbox.errbox import *
from toolbox.confbox import *
from gui.winhelper import AutoScrollbar
from gui.winhelper import InfoCanvas

class messageWindow(object):
    """
    A class to build a message window containing version, author and 
    email on default. 
    \param lang contains the chosen display language.
    """
    def __init__(self, lang = 'en'):
        """
        Constructor
        \param lang contains the chosen display language.
        """
        self.lang = lang
        self.window = Toplevel()
        self.logger = createLogger(logpath = '/tmp/')

    def showinfo(self, message = '', title = 'Info'):
        """
        This method adds and displays content to the message window.

        \param message contains a message to be displayed in the 
                       message window. It may be an array, a string or 
                       a number (integer/float).
        \param title   sets the title of the message window. The 
                       default is 'Info'.
        """
        self.title = title

        self.window.title(self.title)
        Label(self.window, width = 35).pack()

        if type(message) == type([]):
            dummy = ""
            
            for key in message:
                dummy = dummy + str(key) + '\n'

        elif type(message) == type(1) or type(message) == type(1.1):
            message = str(message)

        elif type(message) != type(""):
            self.logger.debug('Message Window gets the wrong data type for message!')
            exit(1)

        label = Label(self.window,
                      text = message,
                      wraplength = 300,
                      padx = 10,
                      pady = 10,
                      font = ('Arial', 10))

        button = Button(self.window,
                        text = txtmenu['but_ok'][self.lang],
                        command = self.window.destroy)
        label.pack()
        Label(self.window, width = 35).pack()
        button.pack()
        self.window.mainloop()

class blankWindow(object):
    '''
    A simple window class with  a not filled menu bar.
    \param lang  chosen language for the menu.
    '''
    def __init__(self, lang = 'en'):
        '''
        Class constructor
        \param lang  chosen language for the menu.
        '''
        self.lang = lang
        self.window = Tk()
        self.__addMenu()
        
        '''This is for the file I/O window'''
        self.mask = [txtwin['xml_files'][self.lang],
                     txtwin['all_files'][self.lang]
                     ]
        
    def __addMenu(self):
        '''
        This private method just adds the menu bar into the window's 
        layout
        '''
        self.menu = Menu(self.window)
        self.window.configure(menu = self.menu)
    
    def _helpAbout(self):
        '''
        This method just opens a message window with the basic 
        information about the ADaManT XML Generator (like version and 
        copyright)
        '''
        self.about = "%s\nVersion %s\n\n%s\n%s\n%s" % (__me__,
                                                      __version__,
                                                      __copyright__,
                                                      __institute__,
                                                      __email__)
        self.msg = messageWindow()
        self.msg.showinfo(self.about)
    
    def notdoneyet(self):
        '''
        a simple dummy method for not yet implemented methods
        '''
        self._info = messageWindow()
        self._info.showinfo("This feature is not done yet!",
                            "SOOOORRRRYYY")        
    
class MainWindow(blankWindow):
    '''
    This is the class for the main window object.
    \param lang The chosen language for window's and button's texts. At 
                the moment, only English (en, default value) and German 
                (de) are supported. 
    '''
    def __init__(self, lang = 'en', storepath = None):
        """
        Class constructor
        \param lang The chosen language for window's and button's 
                    texts. At the moment, only English (en, default 
                    value) and German (de) are supported. 
        """
        if storepath == None:
            self.mypath = os.path.expanduser('~')
        else:
            self.mypath = storepath

        self.picpath = "./gui/pic/"
        self.lang = lang
        blankWindow.__init__(self, self.lang)
        self.window.title(wintitle['main'][self.lang])
        Label(self.window, width = 40).pack()
        self.__addFileMenu()
        self.__addOptionMenu()
        self.__addHelpMenu()

        self.mask = [txtwin['xml_files'][self.lang],
                     txtwin['all_files'][self.lang]
                    ]        
        
        """
        set picture for the window background of the main window
        """
        self.__canvas = Canvas(self.window, width = '8.0c', height = '8.5c')
        __background = PhotoImage(file = self.picpath + 'axpg-logo.gif')       
        self.__canvas.create_image(0, 0, image = __background, anchor = NW)
        self.__canvas.pack()
        
        self.window.mainloop()
        
        
    def __openFile(self):
        """
        This method opens a dialogue window (Tk) for opening files. 
        The content of the opened file will be saved in \e file 
        \e content as an array. 
        """
        self.__filein = askopenfilename(filetypes = self.mask,
                                        initialdir = self.mypath)
        if self.__filein != "":
            self.xml = handleXML(filename = self.__filein, action = 'r')
            self.xml.readStrucXML(self.__filein)
            
        self.window.destroy()
        self.window = inputWin(lang = self.lang,
                               xmlcontent = self.xml.dic,
                               filename = self.__filein,
                               storepath = self.mypath)

    def __openStrJmp(self):
        """
        This method opens a structure XML file and jumps directly to 
        the meta data field editor.
        """
        self.__filein = askopenfilename(filetypes = self.mask,
                                        initialdir = self.mypath)
        self.xml = handleXML(filename = self.__filein, action = 'r')
        self.xml.readStrucXML(self.__filein)
        self.window.destroy()
        self.window = metaWin(lang = self.lang,
                              struc = self.xml.dic,
                              fn_struc = self.__filein,
                              storepath = self.mypath)
        
    def __newFile(self):
        """
        This method opens a new window for generation of a new 
        functional structure.
        """
        self.window.destroy()
        self.window = inputWin(lang = self.lang,
                               filename = None,
                               storepath = self.mypath)
        
    def helpAbout(self):
        '''
        This method just opens a message window with the basic 
        information about the ADaManT XML Generator (like version and 
        copyright)
        '''
        self.about = "%s\nVersion %s\n\n%s\n%s\n%s" % (__me__,
                                                      __version__,
                                                      __copyright__,
                                                      __institute__,
                                                      __email__)
        self.msg = messageWindow()
        self.msg.showinfo(self.about)
    
    def optWin(self):
        '''
        Opens an option window and closes the main window.
        '''
        self.window.destroy()
        self.window = confWindow(self.lang)

    def notdoneyet(self):
        """
        An IMPORTANT dummy for methods which are not implemented yet ;-)
        """
        print("MainWindow: not done yet")
        self._info = messageWindow()
        self._info.showinfo("MainWindow: this feature is not done yet!",
                            "SOOOORRRRYYY")
        
    def __addFileMenu(self):
        """
        This method adds a File menu to the windows menu bar.
        """
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['new'],
                                  command = self.__newFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open_struc'],
                                  command = self.__openFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open_saj'],
                                  command = self.__openStrJmp)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['quit'],
                                  command = self.window.destroy)

    def __addOptionMenu(self):
        """
        This method adds an option/preferences menu to the menu bar.
        """
        self.optmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_opt'][self.lang],
                              menu = self.optmenu)
        self.optmenu.add_command(label = submenu['opts'][self.lang]['lang'],
                                 command = self.optWin)

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
        This method will show the ADaManT Handbook
        \todo this needs to be implemented
        """
        self.notdoneyet()

class confWindow(blankWindow):
    """
    This class builds a window for selecting and saving options of 
    ADaManT. For now it is just chosing the language for menus and 
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
        self._cnf = chkCfg()
        
        if 'path' in self._cnf.cnfparam.keys():
            self.sto_path.set(self._cnf.cnfparam['path'])
        else:
            self.sto_path.set(home)
            
        if 'lang' in self._cnf.cnfparam.keys():
            
            if self._cnf.cnfparam['lang'] != self.lang:
                self.lang = self._cnf.cnfparam['lang']
        
        if 'log' in self._cnf.cnfparam.keys():
            self.log_path.set(self._cnf.cnfparam['log'])
        else:
            self.log_path = "/tmp/"
            
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
        """
        self.lang = self.wert.get()
        self.path = self.sto_path.get()
        self.log = self.log_path.get()
        
        if  self.path[-1:] != '/':
            self.path += '/'
        
        if self.log[-1:] != '/':
            self.log += '/'
            
        self.cont = {'lang' : self.lang,
                     'path' : self.path,
                     'log'  : self.log
                     }
        self._cnf.saveCnf(path = self.path, content = self.cont)
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
    structure. A XML structure will be build of the input. 
    \param lang This parameter holds the language chosen for the menus 
                and messages. Default value is 'en'.
    \param xmlcontent a dictionary holding the XML structure/tags
    \param filename this holds the filename of a read XML file holding 
                    the functional structure.
    \param storepath the path where the XML files shall be stored in.
    """
    def __init__(self,
                 lang = 'en',
                 xmlcontent = {},
                 filename = None,
                 storepath = None):
        """
        Constructor
        \param lang This parameter holds the language chosen for the 
                    menus and messages. Default value is 'en'
        \param xmlcontent a dictionary holding the XML structure/tags
        \param filename this holds the filename and path of a read XML 
                        file containing the functional structure.
        \param storepath the path where the XML files shall be stored 
                         in.
        """
        self.lang = lang
        self.xmlcont = xmlcontent
        self.fname = filename
        
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
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)
        self._addHelpMenu()
        self.createWinStruc()
    
    def notdoneyet(self):
        """
        Most important dummy method!
        """
        self._info = messageWindow()
        self._info.showinfo("inputWin: this feature is not done yet!",
                            "SOOOORRRRYYY")    
        print "inputWin: this feature is not done yet!"
         
    def __closewin(self):
        """
        Method for closing the window and opening the main window.
        """
        self.window.destroy()
        self.window = MainWindow(self.lang, self.mypath)
        
    def _addHelpMenu(self):
        """
        This method adds additional functions to the help menu
        """    
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self._templist = {'PROJECT' : self._showProject,
                          'PERSON' : self._showPerson,
                          'PROCEDURE' : self._showProcedure,
                          'EXPERIMENT' : self._showExperiment,
                          'PROGRAM' : self._showProgram,
                          'DATAFILE' : self._showDatafile,
                          'FILESET' : self._showFileset,
                          'ANIMAL' : self._showAnimal
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
        
    def _showProject(self):
        '''
        This method just shows information about the PROJECT element 
        of the functional structure in a message box.
        '''
        self._shownMessage.set(s_elem_def['PROJECT'][self.lang])
        
    def _showPerson(self):
        '''
        This method just shows information about the PERSON element of 
        the functional structure in a message box.
        ''' 
        self._shownMessage.set(s_elem_def['PERSON'][self.lang])
        
    def _showProcedure(self):
        '''
        This method just shows information about the PROCEDURE element 
        of the functional structure in a message box.
        '''        
        self._shownMessage.set(s_elem_def['PROCEDURE'][self.lang])
        
    def _showExperiment(self):
        '''
        This method just shows information about the EXPERIMENT element 
        of the functional structure in a message box.
        '''
        self._shownMessage.set(s_elem_def['EXPERIMENT'][self.lang])
        
    def _showProgram(self):
        '''
        This method just shows information about the PROGRAM element 
        of the functional structure in a message box.
        '''        
        self._shownMessage.set(s_elem_def['PROGRAM'][self.lang])
        
    def _showDatafile(self):
        '''
        This method just shows information about the DATAFILE element 
        of the functional structure in a message box.
        '''        
        self._shownMessage.set(s_elem_def['DATAFILE'][self.lang])
        
    def _showFileset(self):
        '''
        This method just shows information about the FILESET element 
        of the functional structure in a message box.
        '''        
        self._shownMessage.set(s_elem_def['FILESET'][self.lang])
        
    def _showAnimal(self):
        '''
        This method just shows information about the ANIMAL element 
        of the functional structure in a message box.
        '''
        self._shownMessage.set(s_elem_def['ANIMAL'][self.lang])
        
    def _showPage(self):
        '''
        This method just shows general information about this window 
        (structure).
        '''
        self._shownMessage.set(infomsg['help_selem'][self.lang])
        
    def createWinStruc(self):
        """
        This method creates the window structure with list and message 
        boxes. The created window is for reading, generating and 
        editing of elements of the functional structure.
        """
        self._defaultList = StringVar()
        self._chosenList = StringVar()
        self._addEntry = StringVar()
        self._shownMessage = StringVar()
        
        self._shownMessage.set(infomsg['help_info'][self.lang])
        self.defaultLB = Listbox(master = self.window,
                                  selectmode = EXTENDED,
                                  width = 30,
                                  height = 30,
                                  borderwidth = 4,
                                  listvariable = self._defaultList)
        
        self.chosenLB = Listbox(master = self.window,
                                  selectmode = EXTENDED,
                                  width = 30,
                                  height = 30,
                                  borderwidth = 4,
                                  listvariable = self._chosenList)
        
        self._infoBox = Message(master = self.window,
                                bd = 2,
                                relief = SUNKEN,
                                width = 250,
                                textvariable = self._shownMessage
                                )
        self._dummy = ''
        self._strkeys = struct.keys()
        self._strkeys.sort()
        
        for key in self._strkeys:
            self._dummy += key + ' '
        
        self._defaultList.set(self._dummy)
        
        self._dummy = ''
        self._strkeys = self.xmlcont.keys()
        self._strkeys.sort()
        
        for key in self._strkeys:
            self._dummy += key + ' '
            
        self._chosenList.set(self._dummy)
        
        self._addSelBut = Button(master = self.window,
                                 text = txtbutton['but_right'][self.lang],
                                 command = self._setChoice
                                 )
        self._remSelBut = Button(master = self.window,
                                 text = txtbutton['but_del'][self.lang],
                                 command = self._remChoice
                                 )
        self._nextBut = Button(master = self.window,
                               text = txtbutton['but_next'][self.lang],
                               command = self._nextStep
                               )
        self._newEntry = Entry(master = self.window,
                               textvariable = self._addEntry,
                               width = 70)
        self._addEntBut = Button(master = self.window,
                                 text = txtbutton['but_add'][self.lang],
                                 command = self._addItems
                                 )
        del(self._dummy)
        del(self._strkeys)
        del(key)
        
        Label(master = self.window,
              width = 30,
              text = labels['default_c'][self.lang]
              ).grid(row = 0, column = 0)
              
        Label(master = self.window,
              width = 30,
              text = labels['select_c'][self.lang]
              ).grid(row = 0, column = 2)
              
        Label(master = self.window,
              width = 30,
              text = 'Info'
              ).grid(row = 0, column = 3)
              
        self.defaultLB.grid(row = 1, column = 0)
        self.chosenLB.grid(row = 1, column = 2)
        self._infoBox.grid(row = 1, column = 3, sticky = N) 
        self._addSelBut.grid(row = 1, column = 1)
        self._remSelBut.grid(row = 2, column = 2)
        self._nextBut.grid(row = 2, column = 3)
        
        Label(master = self.window,
              width = 60,
              text = labels['add_elem'][self.lang]
              ).grid(row = 3, column = 0, columnspan = 3)
              
        self._newEntry.grid(row = 4, column = 0, columnspan = 3)
        self._addEntBut.grid(row = 4, column = 3, sticky = W)
        
    def _setChoice(self):
        """
        This method transfers the selected structure elements to the 
        list.
        """
        self._selection = self.defaultLB.get(0, END)
        self._selected = self.defaultLB.curselection()
        self._chosen = self._chosenList.get()
        self._chosen = tstr2list(self._chosen)
        self._dummy = ''
        
        for key in self._chosen:
            self._dummy += ' ' + key.strip(' \'')
        
        self._dummy = self._dummy.strip()
            
        for key in self._selected:
            if self._selection[int(key)] not in self._dummy:
                self._dummy += ' ' + self._selection[int(key)]
        
        self._chosenList.set(self._dummy)
        
        del(key)
        del(self._dummy)
        del(self._chosen)
        del(self._selected)
        del(self._selection)
        
    def _remChoice(self):
        """
        This method removes selected items from the list of chosen 
        structure elements.
        """
        self._selected = self.chosenLB.curselection()
        
        for key in sorted(self._selected, reverse = True):
            self.chosenLB.delete(int(key))
            
    def _addItems(self):
        """
        This method adds items from a comma separated list to the 
        chosen structure list.
        \todo It will be a nice feature if non-default elements will be 
        stored in a file (e.g., the config file)
        """
        self._dummy = self._addEntry.get()
        self._dummy = self._dummy.split(',')

        for key in self._dummy:
            if key.strip() != '':
                self.chosenLB.insert(END, key.strip().upper())
            
        self._addEntry.set('')
        del(self._dummy)
        
    def _nextStep(self):
        """
        Method for the NEXT (step) button
        """
        self.mystruct = {}
        self._dummy = list(self.chosenLB.get(0, END))

        if self.xmlcont == {}:
        
            for key in self._dummy:
                self.mystruct[key.upper()] = {'attrib' : {'type'   : '',
                                                          'name'   : key.lower(),
                                                          'dbtype' : ''
                                                         },
                                             'subelem' : [],
                                             'parent'  : []
                                             }
        
            if self.mystruct != {}:
                self.window.destroy()
                self.window = attribWin(lang = self.lang,
                                        struc = self.mystruct,
                                        filename = self.fname,
                                        storepath = self.mypath)
        else:
            for key in self.xmlcont:

                if key in self._dummy:
                    self._dummy.remove(key)
                    
            for key in self._dummy:
                self.xmlcont[key.upper()] = {'attrib' : {'type'   : '',
                                                          'name'   : key.lower(),
                                                          'dbtype' : ''
                                                         },
                                             'subelem' : [],
                                             'parent'  : []
                                             }
            
            self.window.destroy()
            self.window = attribWin(lang = self.lang,
                                    struc = self.xmlcont,
                                    filename = self.fname,
                                    storepath = self.mypath)
        
class attribWin(blankWindow):
    """
    This generates a window where attributes can be added to chosen 
    elements of structure.
    \param lang this holds the chosen display language.
    \param struc this holds the elements of structure in a dictionary
    \param filename name and path of the XML file where the structure 
                    were read from. 
    \param storepath path of the default storage location.
    """
    def __init__(self,
                 lang = "en",
                 struc = {},
                 filename = None,
                 storepath = None):
        """
        Constructor
        \param lang this holds the chosen display language.
        \param struc this holds the elements of structure in a 
                     dictionary
        \param filename name of the XML file where the structure were 
                        read from. 
        """
        self.lang = lang
        self.struc = struc
        self.fname = filename
        
        if self.fname != "" and self.fname != None:
            self._last = getLast(self.fname)
        
        else:
            self._last = ""
            
        if storepath != None:
            self.mypath = storepath
        else:
            self.mypath = os.path.expanduser('~')
        blankWindow.__init__(self, self.lang)
       
        self.window.title(wintitle['edit'][self.lang] + " - " + self._last)
        self.window.resizable(width = FALSE, height = TRUE)

        self._addFileMenu()
        self._addHelpMenu()
        self._buildWin()
        
    def notdoneyet(self):
        """
        Most important dummy method!
        """
        print "attribWin: this feature is not done yet!"
        self._info = messageWindow()
        self._info.showinfo("attribWin: this feature is not done yet!",
                            "SOOOORRRRYYY")
               
    def _addFileMenu(self):
        """
        Adds the file menu to the menu bar
        """
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu) 
        self.filemenu.add_command(label = submenu['file'][self.lang]['next'],
                                  command = self._nextStep)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__closewin)               
             
    def _addHelpMenu(self):
        """
        This method adds additional functions to the help menu
        """    
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['win'],
                                  command = self._helpAboutWin)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)
    
        
    def _helpAboutWin(self):
        '''
        This shows some specific help about the current window.
        \todo this has to be implemented yet
        '''
        self.notdoneyet()
        
        
    def __closewin(self):
        """
        Method for closing the window and opening the main window.
        """
        self.window.destroy()
        self.window = MainWindow(self.lang, self.mypath)
        
    def _buildWin(self):
        """
        Builds internal window structure. A table with name of the 
        element of structure and two option fields (pull down) for 
        type (single/multi) and database type (nested/collection) are 
        generated. 
        \todo list the single entries in alphabetical order
        """
        Label(master = self.window,
              text = screentext['label'][self.lang],
              width = 20
              ).grid(row = 0, column = 0, sticky = W + E)
        Label(master = self.window,
              text = screentext['dbtype'][self.lang],
              width = 20
              ).grid(row = 0, column = 1, sticky = W + E)
        Label(master = self.window,
              text = screentext['type'][self.lang],
              width = 20
              ).grid(row = 0, column = 2, sticky = W + E)         
        self.vscroll = AutoScrollbar(self.window)
        self.vscroll.grid(row = 1,
                          column = 3,
                          sticky = N + S)
        self.canvas = Canvas(master = self.window,
                             width = 500,
                             yscrollcommand = self.vscroll.set)
        self.canvas.grid(row = 1,
                         column = 0,
                         columnspan = 3,
                         sticky = N + E + W + S)
        
        
        self.vscroll.config(command = self.canvas.yview)

        self.window.grid_rowconfigure(1, weight = 1)
        self.window.grid_columnconfigure(0, weight = 1)
        
        self.frame = Frame(self.canvas)
        self.frame.rowconfigure(2, weight = 1)
        self.frame.columnconfigure(1, weight = 1)
        self.elem = {}
        self.om = {}
        
        r = 0
        self.structures = self.struc.keys()
        self.structures.sort()
        
        for entry in self.structures:
            self.elem[entry] = {}
            self.om[entry] = {}
            c = 1
            Label(master = self.frame,
                 text = entry,
                 width = 20,
                 justify = LEFT
                 ).grid(row = r, column = 0, sticky = E + W)
                 
            for attrib in attrib_struc:
                self.elem[entry][attrib] = StringVar()
                
                if self.struc[entry]['attrib'][attrib] == '':
                    self.elem[entry][attrib].set(attrib_struc[attrib][1])
                else:
                    i = 0
                    while i < len(attrib_struc[attrib]):
                        if self.struc[entry]['attrib'][attrib] == \
                        attrib_struc[attrib][i]:
                            self.elem[entry][attrib].set(attrib_struc[attrib][i])
                        i += 1
                    
                self.om[entry][attrib] = apply(OptionMenu,
                                              (self.frame,
                                               self.elem[entry][attrib])\
                                                + tuple(attrib_struc[attrib]))
                
                self.om[entry][attrib]['width'] = 15
                self.om[entry][attrib].grid(row = r, column = c, sticky = E + W)
                c += 1
                
            r += 1
        self.canvas.create_window(0, 0,
                                  anchor = NW,
                                  window = self.frame)
        self.frame.update_idletasks()
        self.canvas.config(scrollregion = self.canvas.bbox("all"))
        
        self._nextBut = Button(master = self.window,
                              text = txtbutton['but_next'][self.lang],
                              command = self._nextStep
                              )
        self._prevBut = Button(master = self.window,
                               text = txtbutton['but_prev'][self.lang],
                               command = self._stepBack)
        self._nextBut.grid(row = 3, column = 2)
        self._prevBut.grid(row = 3 , column = 1)
        
        
    def _nextStep(self):
        """
        This method collects data of the current window and starts the 
        window for generating functional dependencies.
        """
        for entry in self.struc.keys():
            for attrib in attrib_struc:
                self.struc[entry]['attrib'][attrib] = self.elem[entry][attrib].get()
        
        if self.struc != {}:
            self.window.destroy()
            self.window = connectElem(lang = self.lang,
                                      struc = self.struc,
                                      filename = self.fname,
                                      storepath = self.mypath)
            
    def _stepBack(self):
        """
        This methode makes a back step to the previous window.
        Eventually selected entries will be lost.
        """
        if self.struc != {}:
            self.window.destroy()
            self.window = inputWin(lang = self.lang,
                                   xmlcontent = self.struc,
                                   filename = self.fname,
                                   storepath = self.mypath
                                   )
        
class connectElem(blankWindow):
    """
    This creates a window to connect elements of structure logically.
    \param lang holds the chosen diplay language
    \param struc holds a ditionary with the funtional structure
    \param filename contains the filename and path where the structure 
                    may be read from
    \param storepath holds the default storage location for the XML 
                     files. 
    """
    def __init__(self,
                 lang = 'en',
                 struc = {},
                 filename = None,
                 storepath = None):
        """
        Constructor
        \param lang this holds the chosen display language.
        \param struc this holds the elements of structure in a 
                     dictionary
        \param filename path and name of the XML file where the 
                        structure were read from.
        \param storepath holds the default storage location for the 
                         XML files. 
        """
        self.__rmdElems = []
        self.lang = lang
        self.struc = struc
        self.fname = filename
        
        if self.fname != "" and self.fname != None:
            self._last = getLast(self.fname)
        else:
            self._last = ""
            
        if storepath != None:
            self.mypath = storepath
        else:
            self.mypath = os.path.expanduser('~')
            
        self.myRoot = ""
        blankWindow.__init__(self, self.lang)
        self.window.title(wintitle['struc_elem'][self.lang] + ' - ' + self._last)
        
        self._addFileMenu()
        self._addHelpMenu()
        self._createWinStruc()
        if self.fname != None:
            self.myRoot = findElem(self.struc, [])
            self._showStruc()
        
    def notdoneyet(self):
        """
        Most important dummy method!
        """
        print "connectElem: this feature is not done yet!"
        self._info = messageWindow()
        self._info.showinfo("connectElem: this feature is not done yet!",
                            "SOOOORRRRYYY")
             
    def _closewin(self):
        """
        Method for closing the window and opening the main window.
        """
        self.window.destroy()
        self.window = MainWindow(lang = self.lang,
                                 storepath = self.mypath)
                     
    def _addFileMenu(self):
        """
        adds File menu to menu bar
        """
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self._saveStruc)
        self.filemenu.add_command(label = submenu['file'][self.lang]['sv_as'],
                                  command = self._saveStrucAs)
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self._closewin)

    def _addHelpMenu(self):
        """
        adds Help menu to menu bar
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['page'],
                                  command = self.notdoneyet)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)

    def _createWinStruc(self):
        """
        This creates the internal window structure. Buttons entry fields 
        etc.
        """
        self._parentList = StringVar()
        self._childList = StringVar()
        self._rootElem = StringVar()
        self._strucMess = StringVar()
        self._strucElem = self.struc.keys()
        self._rootElem.set(labels['sel_root'][self.lang])
        self._elemStr = list2str(self._strucElem)
        self._parentList.set(self._strucElem[0])
        self._childList.set(self._elemStr)
        
        # definition of buttons, boxes and all the other window elements
        
        self._frame = Frame(master = self.window,
                            width = 25,
                            height = 30)  
              
        self._labelParent = Label(master = self._frame,
                                  text = labels['sel_par'][self.lang],
                                  width = 25,
                                  height = 2,
                                  bg = "green",
                                  )
        self._labelRoot = Label(master = self._frame,
                                text = labels['sel_root'][self.lang],
                                width = 25,
                                height = 2,
                                bg = "green"
                                )
        self._labelChild = Label(master = self.window,
                                 text = labels['sel_child'][self.lang],
                                 width = 25
                                 )
        self._labelPrev = Label(master = self.window,
                                text = labels['preview'][self.lang],
                                width = 40)

        self._selectParent = apply(OptionMenu,
                                  (self._frame, self._parentList)\
                                  + tuple(self._strucElem)
                                  )
        self._selectParent['width'] = 25
        self._selectParent['state'] = DISABLED
        
        self._childBox = Listbox(master = self.window,
                                selectmode = EXTENDED,
                                width = 30,
                                height = 30,
                                borderwidth = 4,
                                state = DISABLED,
                                listvariable = self._childList)
        
        self._canvas = InfoCanvas(master = self.window,
                                  textvariable = self._strucMess,
                                  row = 1,
                                  column = 2)
        
        self._selectRoot = apply(OptionMenu,
                                (self._frame, self._rootElem)\
                                + tuple(self._strucElem))
        self._selectRoot['width'] = 25       
        
        self._crLinkBut = Button(master = self._frame,
                                 text = txtbutton['but_cre_link'][self.lang],
                                 width = 25,
                                 state = DISABLED,
                                 command = self._createLink)
        self._rmLinkBut = Button(master = self._frame,
                                 text = txtbutton['but_rem_link'][self.lang],
                                 width = 25,
                                 state = DISABLED,
                                 command = self._removeLink)
        self._selRootBut = Button(master = self._frame,
                                 text = txtbutton['but_sel_root'][self.lang],
                                 width = 25,
                                 command = self._choseRoot)
        self._rmRootBut = Button(master = self._frame,
                                 text = txtbutton['but_rem_root'][self.lang],
                                 width = 25,
                                 state = DISABLED,
                                 command = self._removeRoot)
        self._saveNextBut = Button(master = self._frame,
                               text = txtbutton['but_save_next'][self.lang],
                               width = 25,
                               state = DISABLED,
                               command = self._saveStruc)
        self._stepBackBut = Button(master = self._frame,
                                  text = txtbutton['but_prev'][self.lang],
                                  width = 25,
                                  command = self._stepBack)
        self._refrBut = Button(master = self._frame,
                              text = txtbutton['but_refr'][self.lang],
                              width = 25,
                              command = self._refreshGraph)
        self._dispBut = Button(master = self._frame,
                               text = txtbutton['but_show_graph'][self.lang],
                               width = 25,
                               command = self._drawGraph)
        
        # elements connected to window
        
        self._frame.grid(row = 0, rowspan = 2, column = 0, sticky = N + S)
        self._labelChild.grid(row = 0, column = 1)
        self._labelPrev.grid(row = 0, column = 2)
        self._childBox.grid(row = 1, column = 1, sticky = N)
        
        # elements connectet to self._frame
        
        self._labelParent.grid(row = 0, column = 0)
        self._selectParent.grid(row = 1, column = 0)
        self._crLinkBut.grid(row = 2, column = 0)
        self._rmLinkBut.grid(row = 3, column = 0)
        self._refrBut.grid(row = 4, column = 0)
        self._labelRoot.grid(row = 5, column = 0)
        self._selectRoot.grid(row = 6, column = 0)
        self._selRootBut.grid(row = 7, column = 0)
        self._rmRootBut.grid(row = 8, column = 0)
        self._saveNextBut.grid(row = 9, column = 0)
        self._stepBackBut.grid(row = 10 , column = 0)
        self._dispBut.grid(row = 11, column = 0)
        
        
    def _createLink(self):
        """
        This method creates a link between parent and child elements. 
        With that you get the structure needed for the XML.
        """
        self._parent = self._parentList.get()
        self._selecChild = self._childList.get()
        self._chosen = self._childBox.curselection()
        self._dummy = list(self.struc[self._parent]['subelem'])
        self._selecChild = tstr2list(self._selecChild)
        for key in self._chosen:
            self._dummy.append(self._selecChild[int(key)])

        self.struc[self._parent]['subelem'] = self._dummy
        
        for self._child in self._dummy:
            if self._parent not in self.struc[self._child]['parent']:
                self.struc[self._child]['parent'].append(self._parent)
                
        self._strucMess.set(self._displayStruc())
        self._showStruc()
#        self._checkAll()
        
    def _removeLink(self):
        """
        This method removes links between a parent and child elements.
        """

        self._parent = self._parentList.get()
        self._selecChild = self._childList.get()
        self._chosen = self._childBox.curselection()
        self._selecChild = tstr2list(self._selecChild)
        self._child = []
        
        for key in self._chosen:
            self._child.append(self._selecChild[int(key)])
        
        for key in self._child:
            self.struc[key]['parent'].remove(self._parent)
            self.struc[self._parent]['subelem'].remove(key)
            
        self._strucMess.set(self._displayStruc())
#        self._showStruc()

    def _choseRoot(self):
        """
        This method choses and confirms the root element of the 
        structure/tree. The idea is to let the user define the root 
        element so the program knows which is root from the begin.
        """
        self.myRoot = self._rootElem.get()
        self._selRootBut['state'] = DISABLED
        self._selectRoot['state'] = DISABLED
        self._rmRootBut['state'] = NORMAL
        
        self._childBox['state'] = NORMAL
        self._selectParent['state'] = NORMAL
        self._crLinkBut['state'] = NORMAL
        self._rmLinkBut['state'] = NORMAL
        
        self._parentList.set(self.myRoot)
        self._rmElem(self.myRoot)
        self.__rmdElems += [self.myRoot]        
        self._strucMess.set(self._displayStruc())

    def _removeRoot(self):
        """
        This method removes an existing root element out of the 
        structure/tree. With that the whole structure is more or less 
        removed. It might be used to start things over. 
        """
        for self._item in self.struc:
            self.struc[self._item]['parent'] = []
            self.struc[self._item]['subelem'] = []
        self._addElem(self.__rmdElems)
        self._strucMess.set('')
        self._selRootBut['state'] = NORMAL
        self._selectRoot['state'] = NORMAL
        self._rmRootBut['state'] = DISABLED
        self._childBox['state'] = DISABLED
        self._selectParent['state'] = DISABLED
        self._crLinkBut['state'] = DISABLED
        self._rmLinkBut['state'] = DISABLED
        
    def _rmElem(self, elem = None):
        """
        Removes an element from the child list box. This elements are 
        just deleted from the view not from default entries or so.
        \param elem a list/string of element(s) to be removed
        """
        self.elem = elem
        
        if self.elem != None:
            self._list = tstr2list(self._childList.get())
            
            if type(self.elem) == type([]):
                for key in self.elem: 
                    if key in self._list:              
                        self._list.remove(key)
            
            elif type(self.elem) == type("") and self.elem in self._list:
                self._list.remove(self.elem)
            
            self._childList.set(list2str(self._list))
        
    def _addElem(self, elem = None):
        """
        adds an element to the child list box
        \param elem list/string of element(s) to be added.
        """
        self.elem = elem
        
        if self.elem != None:
            self._list = tstr2list(self._childList.get())
            
            if type(self.elem) == type([]):               
                self._list += self.elem
                for key in self.elem:
                    self.__rmdElems.remove(key)
            
            elif type(self.elem) == type(""):
                self._list += [self.elem]
                self.__rmdElems.remove(self.elem)
                
            self._childList.set(list2str(self._list))
            
    def _drawGraph(self):
        """
        This method should draw a graph of the structure of the 
        connections between all the elements.
        """
        self.graph = drawTree(lang = self.lang,
                              struc = self.struc,
                              storepath = self.mypath)
        
    def _refreshGraph(self):
        """
        This method refreshed the view of the graph structure.
        """
        try:
            self.graph._closeWin()
        finally:
            self.graph = drawTree(lang = self.lang,
                              struc = self.struc,
                              storepath = self.mypath)
        
    def _saveStrucAs(self):
        """
        This method saves teh structure XML file under a different 
        name.
        \todo this needs to be implemented
        """
#        self.notdoneyet()        
        self.fname = None
        self._saveStruc()
        
    def _saveStruc(self):
        """
        This method saves the connected structure of elements as XML 
        in a file. It opens a file dialog window if the data does not 
        come from a read and edited file. Otherwise, it just saves it 
        with the same file name as loaded. 
        """
        self.loop = findLoops(struc = self.struc,
                              elem = self.myRoot,
                              way = [],
                              result = []
                              )
        if len(self.loop) == 0:
            self.mask = [txtwin['xml_files'][self.lang],
                         txtwin['all_files'][self.lang]
                         ]
            if self.fname == None:            
                self._myfile = asksaveasfilename(defaultextension = '.xml',
                                                 filetypes = self.mask,
                                                 initialdir = self.mypath
                                                 )
            else: 
                self._myfile = self.fname
                
            self.xmlhandle = handleXML(xmlstruct = self.struc,
                                       filename = self._myfile, action = "w")
            self._nextStep()
        else:
            self.mesg = screenmesg['loop'][self.lang] + '\n\n'
            
            i = 0
            while i < len(self.loop):
                sl = asciLoops(self.loop[i][0], self.loop[i][1]) 
                self.mesg += sl + '\n------------------------------------\n'
                i += 1
                
            self._info = messageWindow(self.lang)
            self._info.showinfo(self.mesg, 'Loop Detector')
    
    def _nextStep(self):
        '''
        This method closes the currend window object and opens a 
        metaWin object for the next step of the generation process.
        '''
        self.window.destroy()
        self.window = metaWin(lang = self.lang,
                              struc = self.struc,
                              fn_struc = self._myfile,
                              storepath = self.mypath)

    def _stepBack(self):
        """
        This goes back to the last window.
        \todo this method has to be implemented
        """
        self.notdoneyet()
        
    def _displayStruc(self):
        """
        This method displays the configured structure in the Messagebox.
        \retval self._string string containing the logical parent/child 
                structure.
        """
        self._string = '<<<' + self.myRoot + '>>> \n'
       
        for self._item in self.struc[self.myRoot]['subelem']:
            self._string += "'--->" + self._item + '\n'
        self._string += '\n'
        
        for self._item in self.struc:
        
            if self.struc[self._item]['subelem'] == [] \
            and self.struc[self._item]['parent'] == []:
                print "connectElem: %s not configured yet" % (self._item)
                
            else:
                if self._item != self.myRoot:
                    self._string += self._item + "\n"
                    
                    for self._child in self.struc[self._item]['subelem']:
                        self._string += "'--->" + self._child + '\n' 
                        
                    if self.struc[self._item]['subelem'] == []:
                        for self._par in self.struc[self._item]['parent']:
                            self._string += '^---' + self._par + '\n'
                        
        return self._string
    
    def _checkAll(self):
        """
        This method checks whether all elements were used in the 
        building process.
        \todo multi-language support for error messages.
        \todo error messages in a message window and not only in 
              sdtout.
        """
        self._unconf = 0
        self._root = 0
        self._leave = 0
        
        for self._item in self.struc:
            if self.struc[self._item]['parent'] == [] \
            and self.struc[self._item]['subelem'] == []:
                self._unconf += 1
            elif self.struc[self._item]['parent'] == [] \
            and self.struc[self._item]['subelem'] != []:
                self._root += 1
            elif self.struc[self._item]['parent'] != []\
            and self.struc[self._item]['subelem'] == []:
                self._leave += 1
                
        if self._root != 1:
            print "Fehler beim Root-Element"
            self._saveNextBut['state'] = DISABLED
        elif self._leave < 1:
            print "Fehler beim Blatt"
            self._saveNextBut['state'] = DISABLED
        elif self._unconf > 0:
            print "noch nicht alles konfiguriert"
            self._saveNextBut['state'] = DISABLED
        else:
            self._saveNextBut['state'] = NORMAL

    def _showStruc(self):
        """
        this displays a loaded structure from XML file
        """
        self._rootElem.set(self.myRoot)
        self._choseRoot()
        self._displayStruc()
        self._checkAll()

class metaWin(blankWindow):
    """
    Creates a window for generating meta data fields
    \param lang this holds the chosen display language.
    \param struc this holds the elements of structure in a dictionary
    \param struc this holds the elements of meta data in a dictionary
    \param fn_struc path and name of the XML file where the structure 
                    were read from.
    \param fn_meta path and name of the XML file where the meta data 
                        will be saved in.
    \param storepath path of the default storage location of the XML 
                     files. 
    """
    
    def __init__(self,
                 lang = "en",
                 struc = {},
                 meta = {},
                 fn_struc = None,
                 fn_meta = None,
                 storepath = None):
        """
        Constructor
        \param struc this holds the elements of structure in a 
                     dictionary.
        \param fn_struc path and name of the XML file where the 
                        structure were read from.
        \param fn_meta path and name of the XML file where the meta 
                       data will be saved in.
        \param storepath path of the default storage location of the 
                         XML files.         
        """
        self.lang = lang
        self.mask = [txtwin['xml_files'][self.lang],
                     txtwin['all_files'][self.lang]
                    ]
        self.struc = struc
        self.fn_struc = fn_struc
        self._lastStruc = getLast(self.fn_struc)
        self.fn_meta = fn_meta

        if self.fn_meta != "" and self.fn_meta != None:
            self._lastMeta = getLast(self.fn_meta)
        else:
            self._lastMeta = ""
            
        self.meta = meta
        
        if storepath == None:
            self.mypath = os.path.expanduser('~')
        else: 
            self.mypath = storepath
                
        if self.struc != {} and self.meta == {}:
            
            for key in self.struc.keys():
                self.meta[key] = {}
                    
        blankWindow.__init__(self, self.lang)
        self.window.title(wintitle['meta_1'][self.lang] + 
                          " - " + 
                          self._lastStruc + 
                          self._lastMeta)
        self._addFileMenu()
        self._addHelpMenu()
        self._createWinStruc()
        
    def notdoneyet(self):
        """
        Most important dummy method!
        """
        print "metaWin: this feature is not done yet!"
        self._info = messageWindow()
        self._info.showinfo("metaWin: this feature is not done yet!",
                            "SOOOORRRRYYY")
             
    def _closewin(self):
        """
        Method for closing the window (by destroying the object) and 
        opening the main window (by constructing a new onbject).
        """
        self.window.destroy()
        self.window = MainWindow(lang = self.lang,
                                 storepath = self.mypath
                                 )
                     
    def _addFileMenu(self):
        """
        adds File menu to menu bar.
        """
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open_struc'],
                                  command = self._openStruc)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open_meta'],
                                  command = self._openMeta)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['sv_as_struc'],
                                  command = self._saveStrucAs)
        self.filemenu.add_command(label = submenu['file'][self.lang]['sv_as_meta'],
                                  command = self._saveMetaAs)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self._closewin)


    def _addHelpMenu(self):
        """
        adds Help menu to menu bar.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['page'],
                                  command = self._helpPage)
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)
        
    def _helpPage(self):
        '''
        Displays a page content help.
        \todo this method has to be implemented
        '''
        self.notdoneyet()

    def _openStruc(self):
        """
        This opens a structure XML where a meta data XML should be 
        generated from.#
        \bug Opening a struct file at this place mixup data somehow...
        """
        self.fn_struc = askopenfilename(filetypes = self.mask,
                                        initialdir = self.mypath)
        
        if self.fn_struc != "" and self.fn_struc != None:
            self._lastStruc = getLast(self.fn_struc)
            self.window.title(wintitle['meta_1'][self.lang] + 
                              " - " + 
                              self._lastStruc + 
                              self._lastMeta)
            del(self.struc)
            self.struc = handleXML(filename = self.fn_struc, action = 'r')
            self.struc.readStrucXML(self.fn_struc)
                

            
    def _openMeta(self):
        """
        this opens a meta data XML for editing purposes
        """

        if self.fn_struc == None:
            self._info = messageWindow()
            self._info.showinfo(errmsg['ld_struc'][self.lang])
        
        else:
            self.fn_meta = askopenfilename(filetypes = self.mask,
                                initialdir = self.mypath)
            
            if self.fn_meta != "":
                self.xml = handleXML(filename = self.fn_meta,
                                     linkfile = self.fn_struc,
                                     action = 'r')
                self.meta = self.xml.readMetaXML(self.fn_meta)
                
        if self.fn_meta != "" and self.fn_meta != None:
            self._lastMeta = getLast(self.fn_meta)
            self.window.title(wintitle['meta_1'][self.lang] + 
                              " - " + 
                              self._lastStruc + 
                              self._lastMeta)        
        self._refrCanvas()

    def _saveStrucAs(self):
        """
        This saves a (loaded) structure file under a different name.
        """
        self.fn_struc = asksaveasfilename(defaultextension = '.xml',
                                           filetypes = self.mask,
                                           initialdir = self.mypath
                                           )
        self.xmlhandle = handleXML(xmlstruct = self.struc,
                                   filename = self.fn_struc,
                                   action = "w"
                                   )
        self._info = messageWindow()
        self._info.showinfo(self.fn_struc + "\n" + \
                            screenmesg['file_saved'][self.lang])
        
    def _saveMetaAs(self):
        """
        This saves a (loaded) meta data file under a different name.
        """
        self._empty = False
        self._mdindex = self.meta.keys()
        self._mdindex.sort()
        
        for key in self._mdindex:
        
            if self.meta[key] == {}:
                self._empty = True
                
        if self._empty:
            self._info = messageWindow()
            self._info.showinfo(screenmesg['no_data_sv'][self.lang])
        else:
            self._myfile = asksaveasfilename(defaultextension = '.xml',
                                             filetypes = self.mask,
                                             initialdir = self.mypath
                                             )
            self.xmlhandle = handleXML(xmlstruct = self.meta,
                                       filename = self._myfile,
                                       linkfile = self.fn_struc,
                                       action = "w")
            self._info = messageWindow()
            self._info.showinfo(self._myfile + '\n' + \
                                screenmesg['file_saved'][self.lang])    
        
    def _refrCanvas(self):
        """
        This just refreshes the InfoCanvas widget. The object will be 
        deleted and recreated.
        """
        del(self._canvasInfo)    
        
        self._showStruc()
        self._canvasInfo = InfoCanvas(master = self.window,
                                      textvariable = self._strucMess,
                                      row = 0,
                                      column = 2,
                                      width = 250)        
                    
    def _createWinStruc(self):
        """
        This creates the internal window structure: buttons, listboxes 
        etc. 
        """
        self._strucElem = StringVar()
        self._selList = StringVar()
        self._addEntry = StringVar()
        self._strucMess = StringVar()
                
        self._frame1 = Frame(master = self.window,
                             width = 30)
        
        self._selBox = Listbox(master = self.window,
                               selectmode = EXTENDED,
                               width = 30,
                               height = 35,
                               borderwidth = 2,
                               listvariable = self._selList,
                               )


        
        self._dummy = self.struc.keys()
        self._omStruc = apply(OptionMenu,
                              (self._frame1,
                              self._strucElem) + tuple(self._dummy))
        self._strucElem.set(ommsg['sel_struc'][self.lang])
        self._crLnkBut = Button(master = self._frame1,
                                text = txtbutton['but_cre_link'][self.lang],
                                command = self._createLink
                                )
        self._rmLnkBut = Button(master = self._frame1,
                                text = txtbutton['but_rem_link'][self.lang],
                                command = self._rmLink
                                )
        self._refBut = Button(master = self._frame1,
                              text = txtbutton['but_refr'][self.lang],
                              command = self._refresh)
        
        self._newEntry = Entry(master = self._frame1,
                               textvariable = self._addEntry,
                               width = 30
                              )
        self._addMetaBut = Button(master = self._frame1,
                                  text = txtbutton['but_add_meta'][self.lang],
                                  command = self._addMeta)
        self._rmMetaBut = Button(master = self._frame1,
                                 text = txtbutton['but_rem_meta'][self.lang],
                                 command = self._rmMeta)
        self._nxtStepBut = Button(master = self._frame1,
                                  text = txtbutton['but_next'][self.lang],
                                  command = self._nextStep)
        self._prevStepBut = Button(master = self._frame1,
                                  text = txtbutton['but_prev'][self.lang],
                                  command = self._stepBack)
        self._showGraphBut = Button(master = self._frame1,
                                    text = txtbutton['but_show_graph'][self.lang],
                                    command = self._showGraph)
        
        self._frame1.grid(row = 0, column = 0, sticky = N + S)
        self._omStruc.grid(row = 0, column = 0, sticky = E + W)
        self._crLnkBut.grid(row = 1, column = 0, sticky = E + W)
        self._rmLnkBut.grid(row = 2, column = 0, sticky = E + W)
        self._refBut.grid(row = 3, column = 0, sticky = E + W)
        Label(master = self._frame1,
              height = 4
              ).grid(row = 4, column = 0, sticky = E + W)
        self._newEntry.grid(row = 5, column = 0, sticky = E + W)
        self._addMetaBut.grid(row = 6, column = 0, sticky = E + W)
        self._rmMetaBut.grid(row = 7, column = 0, sticky = E + W)
        self._nxtStepBut.grid(row = 8, column = 0, sticky = E + W)
        self._prevStepBut.grid(row = 9, column = 0, sticky = E + W)
        self._showGraphBut.grid(row = 10, column = 0, sticky = E + W)
        
        self._selBox.grid(row = 0, column = 1, sticky = "news")

        self._showStruc()

        self._canvasInfo = InfoCanvas(master = self.window,
                                      textvariable = self._strucMess,
                                      row = 0,
                                      column = 2,
                                      width = 250)        
        
    def _createLink(self):
        """
        Creates links between elements of structure and meta data 
        fields.
        """
        self.__selection = self._selBox.get(0, END)
        self.__selected = self._selBox.curselection()
        self.__selElem = self._strucElem.get()

        for key in self.__selected:
            self.meta[self.__selElem][self.__selection[int(key)]] = dict(submeta)
            
        self._showStruc()
        del(self.__selected)
        del(self.__selection)
        del(self.__selElem)
        
    def _rmLink(self):
        """
        removes links between elements of structure and meta data fields.
        """
        self.__selection = self._selBox.get(0, END)
        self.__selected = self._selBox.curselection()
        self.__selElem = self._strucElem.get()
        
        for key in self.__selected:
            del(self.meta[self.__selElem][self.__selection[int(key)]])
            
        del(self.__selected)
        del(self.__selection)
        del(self.__selElem)
        self._refresh()        
    
    def _refresh(self):
        """
        refreshes view and the listbox for the meta data fields.
        \bug if there is a no-default element things go wrong while 
             refreshing.
        """
        self._selElem = self._strucElem.get()
        
        if self._selElem in self.struc.keys(): 
            if self._selElem in meta.keys(): 
                if meta[self._selElem] != {}:
                    self._selList.set(list2str(meta[self._selElem].keys()))
            else:
                self._selList.set('')
            
        self._selBox.selection_clear(0, END)
        del(self._selElem)
        
        self._refrCanvas()
        
    def _addMeta(self):
        """
        adds a meta element to the list.
        \todo It would be a nice option to save non-default fields in 
        e.g. the config file.
        """
        self._dummy = self._addEntry.get()
        self._dummy = self._dummy.split(',')
        
        for key in self._dummy:
            if key.strip() != '':
                self._selBox.insert(END, key.strip())
                
        self._addEntry.set('')
        del(self._dummy)
        
    def _rmMeta(self):
        """
        removes a meta element from the list.
        """
        self._selected = self._selBox.curselection()
        
        for key in sorted(self._selected, reverse = True):
            self._selBox.delete(int(key))
        
        del(self._selected)
        
    def _showStruc(self):
        """
        shows the connected meta data field structure.
        \bug if files were (re-)loaded here there is a bug in 
        displaying the data stucture...
        """
        self._displStr = ""
        
        for self._struc in self.meta:
            self._displStr += self._struc + '\n'
            for self._item in self.meta[self._struc]:
                self._displStr += "'----> " + self._item + "\n"
            self._displStr += '\n'
            
        self._strucMess.set(self._displStr)

    def _showGraph(self):
        '''
        This method opens another window where the structure will be 
        displayed graphically.
        '''
        self.grapwin = drawTree(lang = self.lang, struc = self.struc,
                                storepath = self.mypath)
        
    def _nextStep(self):
        """
        opens the next window to define the attributes of the meta 
        data fields.
        """
        self.window.destroy()
        self.window = attribMetaWin(lang = self.lang,
                                    meta = self.meta,
                                    struc = self.struc,
                                    fn_meta = self.fn_meta,
                                    fn_struc = self.fn_struc,
                                    storepath = self.mypath)
    def _stepBack(self):
        """
        This method steps back to the last window. Not saved changes 
        will be lost probably.
        \todo implement this method
        """
        self.notdoneyet()
        
        
class attribMetaWin(blankWindow):
    """
    This opens a window for setting the attributes of meta data fields.
    \param lang used display language
    \param meta dictionary which holds the meta data field structure
    \param fn_meta file name of meta data field's XML file
    \param fn_struc filename of structure element's XML file   
    \param storepath path where to store the file. If not set it is the 
                     home directory of the user. 
    """
    
    def __init__(self,
                 lang = "en",
                 meta = {},
                 struc = {},
                 fn_meta = None,
                 fn_struc = None,
                 storepath = None):
        """
        Constructor
        \param lang used display language.
        \param meta dictionary which holds the meta data field 
                    structure.
        \param fn_meta file name of meta data field's XML file.
        \param fn_struc filename of structure element's XML file.
        \param storepath path where to store the file. If not set it is 
                         the home directory of the user.         
        """
        self.lang = lang
        self.meta = meta
        self.struc = struc
        self.fn_meta = fn_meta
        
        if self.fn_meta != "" and self.fn_meta != None:
            self._lastMeta = getLast(self.fn_meta)
        
        else:
            self._lastMeta = ""
            
        self.fn_struc = fn_struc
        self._lastStruc = getLast(self.fn_struc)
        
        if storepath == None:
            self.mypath = os.path.expanduser('~')
        else:
            self.mypath = storepath
        
        blankWindow.__init__(self, self.lang)
        self.window.title(wintitle['meta_2'][self.lang] + 
                          " - " + 
                          self._lastStruc + 
                          self._lastMeta)
        self._addFileMenu()
        self._addHelpMenu()
        
        self._creatWinStruc()
        
    def notdoneyet(self):
        """
        Most important dummy method!
        """
        print "attribMetaWin: this feature is not done yet!"
        self._info = messageWindow()
        self._info.showinfo("attribMetaWin: this feature is not done yet!",
                            "SOOOORRRRYYY")

    def _addFileMenu(self):
        """
        This adds a file menu to the menu bar of this window.
        """
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save_meta'],
                                  command = self._saveMeta)
        self.filemenu.add_command(label = submenu['file'][self.lang]['sv_as_meta'],
                                  command = self._saveMetaAs)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self._closeWin)
        self.filemenu.add_command(label = submenu['file'][self.lang]['quit'],
                                  command = self._exit)
        
    def _addHelpMenu(self):
        """
        This adds a help menu to the menu bar of this window
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)
        
    def _saveMeta(self):
        """
        This saves the meta data field structure
        """
        if self._attr != {}:
            self._add2Meta()
            self.mask = [txtwin['xml_files'][self.lang],
                        txtwin['all_files'][self.lang]]
            
            if self.fn_meta == None and self.fn_struc != None:
                self._myfile = asksaveasfilename(defaultextension = '.xml',
                                                 filetypes = self.mask,
                                                 initialdir = self.mypath
                                                 )
            elif self.fn_meta != None and self.fn_struc != None:
                self._myfile = self.fn_meta
            
            self.xmlhandle = handleXML(xmlstruct = self.meta,
                                       filename = self._myfile,
                                       linkfile = self.fn_struc,
                                       action = "w")

    def _saveMetaAs(self):
        """
        This saves the meta data XML under a different file name.
        """
        self.notdoneyet()
        
    def _stepBack(self):
        """
        this steps back to the last window. Unsaved changes might be 
        lost.
        """
        self.window.destroy()
        self.window = metaWin(lang = self.lang,
                              meta = self.meta,
                              struc = self.struc,
                              fn_meta = self.fn_meta,
                              fn_struc = self.fn_struc,
                              storepath = self.mypath)
        
    def _closeWin(self):
        """
        This closes the current window and goes back to the main 
        window.
        """
        self.window.destroy()
        self.window = MainWindow(lang = self.lang,
                                 storepath = self.mypath)
        
    def _exit(self):
        """
        This exits the program.
        """
        self.window.destroy()
        sys.exit(0)
        
    def _creatWinStruc(self):
        """
        Creates the internal window GUI structure.
        """
        self._attr = {}
        self._om = {}
        self._vscroll = AutoScrollbar(self.window)
        self._canvas = Canvas(master = self.window,
                              width = 300,
                              yscrollcommand = self._vscroll.set)
        self._canvas.grid(row = 0, column = 0, sticky = N + E + W + S)
        self._vscroll.grid(row = 0, column = 1, sticky = N + S)
        self._vscroll.config(command = self._canvas.yview)
        
        self.window.grid_rowconfigure(0, weight = 1)
        self.window.grid_columnconfigure(0, weight = 1)
        
        self._frame0 = Frame(self._canvas)
        self._frame0.rowconfigure(1, weight = 1)
        self._frame0.columnconfigure(1, weight = 1)
        r1 = 0
        self._lf = {}
        
        for self._stelem  in self.meta:
            self._attr[self._stelem] = {}
            self._om[self._stelem] = {}
            if self._stelem.lower() != 'name':
                self._lf[self._stelem] = LabelFrame(master = self._frame0,
                                                   text = self._stelem 
                                                   )
                self._lf[self._stelem].grid(row = r1,
                                            column = 0,
                                            ipadx = 5,
                                            ipady = 5,
                                            padx = 5,
                                            pady = 5,
                                            sticky = "news")
            r2 = 0
            
            for self._atelem in self.meta[self._stelem]:
                self._attr[self._stelem][self._atelem] = {}
                self._om[self._stelem][self._atelem] = {}
                Label(master = self._lf[self._stelem],
                      justify = LEFT,
                      text = self._atelem
                      ).grid(row = r2,
                             column = 0,
                             columnspan = 2,
                             sticky = E + W)
                
                r2 += 1
                
                for self._at in self.meta[self._stelem][self._atelem]:
                    if self._at.lower() != 'name' and self._at.lower() != 'label':
                        self._attr[self._stelem][self._atelem][self._at] = StringVar()
                        Label(master = self._lf[self._stelem],
                              text = self._at,
                              justify = LEFT
                              ).grid(row = r2,
                                     column = 0,
                                     sticky = E + W)

                    if self._at in attrib_metad.keys() and self._at.lower() != 'name' \
                    and self._at.lower() != 'label':
                        self._om[self._stelem][self._atelem][self._at] = \
                        apply(OptionMenu,
                              (self._lf[self._stelem],
                              self._attr[self._stelem][self._atelem][self._at])\
                              + tuple(attrib_metad[self._at]))
                        
                        """
                        setting default values for meta data fields
                        """ 
                        if self.meta == {} or self.meta[self._stelem][self._atelem][self._at] == '':                       
                            self._attr[self._stelem][self._atelem][self._at].set(attrib_metad[self._at][0])
                        else:
                            self._attr[self._stelem][self._atelem][self._at].set(self.meta[self._stelem][self._atelem][self._at])
                        
                        self._om[self._stelem][self._atelem][self._at]['width'] = 20
                        self._om[self._stelem][self._atelem][self._at].grid(row = r2,
                                                                            column = 1,
                                                                            sticky = 'ew')
                    elif self._at.lower() != 'name' and self._at.lower() != 'label':
                        self._om[self._stelem][self._atelem][self._at] = \
                        apply(OptionMenu,
                              (self._lf[self._stelem],
                              self._attr[self._stelem][self._atelem][self._at])\
                              + tuple("???"))
                        self._attr[self._stelem][self._atelem][self._at].set('****')
                    
                        self._om[self._stelem][self._atelem][self._at]['width'] = 20
                        self._om[self._stelem][self._atelem][self._at].grid(row = r2,
                                                                            column = 1,
                                                                            sticky = 'ew')
                    elif self._at.lower() == 'name':
                        self._attr[self._stelem][self._atelem][self._at] = StringVar()
                        Label(master = self._lf[self._stelem],
                              text = self._at,
                              justify = LEFT
                              ).grid(row = r2,
                                     column = 0,
                                     sticky = E + W)
                        self._om[self._stelem][self._atelem][self._at] = \
                        Entry(master = self._lf[self._stelem],
                              textvariable = self._attr[self._stelem][self._atelem][self._at],
                              width = 20)
                        self._om[self._stelem][self._atelem][self._at].grid(row = r2,
                                                                            column = 1,
                                                                            sticky = "ew")
                        self._attr[self._stelem][self._atelem][self._at].set(self._atelem)
                        
                    r2 += 1
                    
                r1 += 1
                
            self._canvas.create_window(0, 0, anchor = NW, window = self._frame0)
            self._frame0.update_idletasks()
            self._canvas.config(scrollregion = self._canvas.bbox("all"))
                
            self._frame2 = Frame(self.window,
                                width = 25,
                                height = 30)
            self._frame2.grid(row = 0,
                              column = 2,
                              sticky = N + E + W)
            
            self._saveBut = Button(master = self._frame2,
                                   text = txtbutton['but_sav'][self.lang],
                                   command = self._saveMeta)
            self._backBut = Button(master = self._frame2,
                                   text = txtbutton['but_prev'][self.lang],
                                   command = self._stepBack)
            self._closeBut = Button(master = self._frame2,
                                   text = txtbutton['but_clos'][self.lang],
                                   command = self._closeWin)
            self._exitBut = Button(master = self._frame2,
                                   text = txtbutton['but_quit'][self.lang],
                                   command = self._exit)
            
            self._saveBut.grid(row = 0,
                              column = 3,
                              sticky = N + E + W)
            self._backBut.grid(row = 1,
                               column = 3,
                               sticky = "news")
            self._closeBut.grid(row = 2,
                               column = 3,
                               sticky = N + E + W)
            self._exitBut.grid(row = 3,
                               column = 3,
                               sticky = N + E + W)
        
    def _add2Meta(self):
        """
        this method adds chosen values to the meta data structure 
        (dictionary).
        """
        if self._attr != {}:
            for self._stel in self._attr:
                for self._alab in self._attr[self._stel]:
                    for self._at in self._attr[self._stel][self._alab]:
                        self.meta[self._stel][self._alab][self._at] = \
                        self._attr[self._stel][self._alab][self._at].get()
                        
class drawTree(object):
    '''
    This class creates an object to draw a graph of a tree structure 
    (in a dictionary).
    \param lang contains the used language.
    \param struc contains the structure of the tree
    \param parent key for the parent index list in the dictionary
    \param child key for the child index list in the dictionary
    '''
    def __init__(self, lang = "en",
                 struc = {},
                 parent = 'parent',
                 child = 'subelem',
                 storepath = None):
        '''
        Constructor
        \param lang contains the used language.
        \param struc contains the structure of the tree
        \param parent key for the parent index list in the dictionary
        \param child key for the child index list in the dictionary
        \param storepath the path where all xml or graph files will be 
               stored in.
        '''
        self.lang = lang
        self.struc = struc
        self.storepath = storepath
        self.pic = 'tmp_graph.gif'
        self.graphfile = self.storepath + '/' + self.pic
        self.p = parent
        self.c = child 
        self.window2 = Toplevel()
        
        if self.storepath == None:
            self.storepath = os.path.expanduser('~')
            
        self.window2.title(wintitle['meta_2'][self.lang])
        self._addMenu()
        self._addFileMenu()
        self._addHelpMenu()
        self._showTree()
    
    def notdoneyet(self):
        '''
        a simple dummy method for not yet implemented methods
        '''
        self._info = messageWindow()
        self._info.showinfo("This feature is not done yet!",
                            "SOOOORRRRYYY")        
        
    def _addMenu(self):
        '''
        This addy a menu bar to the window
        '''
        self.menu = Menu(self.window2)
        self.window2.configure(menu = self.menu)
        
    def _addFileMenu(self):
        '''
        This adds a file menu to the window
        \todo has to be immplemented
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['sv_as'],
                                  command = self._saveTreeAs)
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self._closeWin)

    
    def _addHelpMenu(self):
        '''
        This adds a help menu to the winfow's menu bar.
        \todo this has to be implemented
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)      
          
    def _helpAbout(self):
        '''
        This method just opens a message window with the basic 
        information about the ADaManT XML Generator (like version and 
        copyright)
        '''
        self.about = "%s\nVersion %s\n\n%s\n%s\n%s" % (__me__,
                                                      __version__,
                                                      __copyright__,
                                                      __institute__,
                                                      __email__)
        self.msg = messageWindow()
        self.msg.showinfo(self.about)
        
    def _closeWin(self):
        """
        This closes the current window and goes back to the main window
        """
        self.window2.destroy()

        
    def _saveTreeAs(self):
        '''
        Saves the tree structure graph as gif file with a chosen file
        name.
        '''

        self._myfile = asksaveasfilename(defaultextension = '.gif',
                                 filetypes = [txtwin['gif_files'][self.lang]],
                                 initialdir = self.storepath
                                 )
        self.graphfile = self._myfile
        self._createTree()
        self._info = messageWindow()
        self._info.showinfo(self.graphfile + '\n' + \
                            screenmesg['file_saved'][self.lang],
                            "Info")          
        
            
    def _createTree(self):
        '''
        Creates a graphical tree through pydot as a gif file.
        '''
#        self.graphfile = self.storepath + '/' + self.pic
        self.graph = pydot.Dot(graph_type = 'digraph')
        
        for self.item in self.struc:
        
            for self.child in self.struc[self.item]['subelem']:
                self.edge = pydot.Edge(self.item, self.child)
                self.graph.add_edge(self.edge)

        self.graph.write_gif(self.graphfile)
        
    def _showTree(self):
        '''
        Displays the graphics of the structure tree in a window
        '''
        self._createTree()
        self.background = PhotoImage(file = self.graphfile)     

        self._picBut = Button(master = self.window2,
                              image = self.background,
                              command = self.window2.destroy)
        self._picBut.pack()
