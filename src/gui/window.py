#!/usr/bin/env python
'''
\file window.py
\package gui.window
\brief 


\date (C) 2015
\author mongol
\email marcus@lederzeug.de

'''
import os
import sys
from Tkinter import *
from ImageTk import *
from tkFileDialog import *
from rpgtoolbox.lang import *
from rpgtoolbox.globaltools import *
#from rpgtoolbox.logbox import *
from rpgtoolbox import logbox as log
from rpgtoolbox.errbox import *
from rpgtoolbox.confbox import *
from gui.winhelper import AutoScrollbar
from gui.winhelper import InfoCanvas

__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015 " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "0.5.5 alpha"
__me__ = "A RPG tool package for Python 2.x"

logger = log.createLogger('window', 'debug', '1 MB', 1, './')

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
#        self.logger = log.createLogger(logpath = '/tmp/')

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
        self.mask = [txtwin['csv_files'][self.lang],
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
        information about the rpg-tools XML Generator (like version and 
        copyright)
        '''
        self.about = "%s\nVersion %s\n\n%s\n%s\n%s" % (__me__,
                                                      __version__,
                                                      __copyright__,
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
    def __init__(self, lang = 'en', title = "Main Window", storepath = None):
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
        else:
            self.mypath = storepath

        self.picpath = "./gui/pic/"
        self.lang = lang
        blankWindow.__init__(self, self.lang)
        self.window.title(title)
        Label(self.window, width = 40).pack()
        self.__addFileMenu()
        self.__addOptionMenu()
        self.__addHelpMenu()
        
        """
        \todo self.mask has to be checked and modified
        """
        self.mask = [txtwin['csv_files'][self.lang],
                     txtwin['exp_files'][self.lang],
                     txtwin['xml_files'][self.lang],
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
        \todo adapt this to csv/text files
        """
        self.__filein = askopenfilename(filetypes = self.mask,
                                        initialdir = self.mypath)
        if self.__filein != "":
            fp = open(self.__filein, 'r')
            self.fcont = fp.readlines()
            
        self.window.destroy()
        
    def __saveFile(self):
        """
        This method will save a file.
        \todo mainWindow.__saveFile has to be implemented 
        """
        self.notdoneyet()
        
        
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
        information about the rpg-tools (like version and 
        copyright)
        '''
        self.about = "%s\nVersion %s\n\n%s\n%s" % (__me__,
                                                      __version__,
                                                      __copyright__,
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
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__openFile)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__saveFile)
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
        This method will show the rpgbox Handbook
        \todo helpHandbook needs to be implemented
        """
        self.notdoneyet()
    

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
        self._cnf = chkCfg(path = "./")
        
        if 'path' in self._cnf.cnfparam.keys():
            self.sto_path.set(self._cnf.cnfparam['path'])
        else:
            self.sto_path.set("./data")
            
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
        logger.debug("window.__save: saved conf to %s" % (self.path))
        self.msg = messageWindow()
        self.msg.showinfo(processing['saved'][self.lang] + '\n' + shortcut[self.lang])
        
    def __closewin(self):
        """
        A method for closing the window and opening the main window.
        """
        self.path = self.sto_path.get()
        self.window.destroy()
        logger.debug('window.py: lang-%s path-%s' % (self.lang, self.path))
        self.window = MainWindow(lang = self.lang, storepath = self.path)
        
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
        
        
        
 
class metaWin(blankWindow):
    """
    Creates a window for generating meta data fields
    \param lang this holds the chosen display language.
    \param storepath path of the default storage location of the XML 
                     files. 
    """
    
    def __init__(self,
                 lang = "en",
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
        
        if storepath == None:
            self.mypath = os.path.expanduser('~')
        else: 
            self.mypath = storepath

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
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self._openStruc)
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
                    
    def _stepBack(self):
        """
        This method steps back to the last window. Not saved changes 
        will be lost probably.
        \todo implement this method
        """
        self.notdoneyet()
