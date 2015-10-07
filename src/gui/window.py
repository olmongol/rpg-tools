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

__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015 " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "0.5.5 alpha"
__me__ = "A Tkinter window tool package for Python 2"

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
