#!/usr/bin/env python

'''
\file window3.py
\brief All classes and functions for Tk used for Python 3.x

This module contains all needed classes/functions to build up a GUI with Tk and 
Python 3.x 

\author Marcus Schwamberger
\email marcus@lederzeug.de
\date (c) 2012
\version 0.1 alpha
'''

__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2012 " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "0.1 alpha"
__me__ = "Tkinter package box for Python 3"

from toolbox.lang import *
from tkinter.filedialog import *
from tkinter import *

class messageWindow(object):
    """
    A class to build a message window containing version, author and email on
    default. 
    """
    def __init__(self, lang = 'en'):
        self.lang = lang
        self.window = Tk()


    def showinfo(self, message = '', title = 'Info'):
        """
        This method adds content to the message window.

        @param message contains a message to be displayed in the message window.
                       It may be an array, a string or a number (integer/float).
        @param title sets the title of the message window. The default is 'Info'.
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
            print "Wrong Data Format"
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
        
        
class MenuWin(object):
    '''
    Master class for all windows using menus. It just contains a basic window 
    layout with a menu bar. There is a method for a help menu, but it is not 
    linked to the menu bar yet.
    @param lang This parameter holds the language that should be used for the 
                GUI's texts. At the moment, German (de) and English (en) are 
                supported. Default language is English. 
    '''


    def __init__(self, lang = 'en'):
        '''
        Constructor
        '''
        self.lang = lang
        self.window = Tk()
        self.__addMenu()
        
    def __addMenu(self):
        '''
        This private method just adds the menu bar into the window's layout
        '''
        self.menu = Menu(self.window)
        self.window.configure(menu = self.menu)
    
    def addHelp(self, context = 'hlp_about'):
        '''
        This method adds a help menu to the menu bar.
        @param context defines the context of the needed help menu: e.g., an
                       \e about \e information  (which is the default)
                       
        @todo: add additional help contexts - maybe even a real \e context 
            \e help 
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu[self.lang]['help'],
                              menu = self.helpmenu
                             )
        
        if context != 'hlp_about':
            if context == 'hlp_first':
                self.helpmenu.add_command(label = txtmenu[self.lang][context],
                                          command = self.firstSteps
                                          )
            elif context == 'hlp_context':
                self.helpmenu.add_command(label = txtmenu[self.lang][context],
                                          command = self.contextHelp
                                          )
        else:
            self.helpmenu.add_command(label = txtmenu[self.lang][context],
                                      command = self.helpAbout)

    def helpAbout(self):
        '''
        This method just opens a message window with the basic information about
        the ADaManT XML Generator (like version and copyright)
        '''
        self.about = "%s\nVersion %s\n\n%s\n%s\n%s" % (__me__,
                                                      __version__,
                                                      __copyright__,
                                                      __institute__,
                                                      __email__)
        self.msg = messageWindow()
        self.msg.showinfo(self.about)
        
    def firstSteps(self):
        '''
        This method opens a help window with the first steps howtos.
        @todo: implement this help method
        @todo: write the first step howtos...
        '''
        
        
    def contextHelp(self):
        '''
        This method opens a context help window where the user may get more 
        detailed help information about the task he is doing.
        @todo: Implement a context help method
        '''
        
