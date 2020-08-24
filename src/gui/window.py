#!/usr/bin/env python
'''
\file window.py
\package gui.window
\brief Some classes for GUI


\date (C) 2015 - 2018
\author Marcus Schwambeger
\email marcus@lederzeug.de
\version 1.0
'''
from tkinter import *
from tkinter.filedialog import *
from rpgtoolbox.lang import *
from rpgtoolbox import logbox as log

__author__ = "Marcus Schwamberger"
__updated__ = "31.01.2020"
__copyright__ = "(C) 2015-{} {}".format(__updated__[-4:], __author__)
__email__ = "marcus@lederzeug.de"
__version__ = "1.0"
__license__ = "GNU V3.0"
__me__ = "A RPG tool package for Python 3"

logger = log.createLogger('window', 'warning', '1 MB', 1, './')



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
        self.mask = [txtwin['json_files'][self.lang],
                     txtwin['spell_files'][self.lang],
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
                                                      __license__,
                                                      __copyright__,
                                                      __email__)
        self.msg = messageWindow()
        self.msg.showinfo(self.about)


    def handbook(self, chapter = "handbook"):
        '''
        This method will call call a specific chapter from the handbook of
        rm_char_tools.
        \todo handbook has to be implemented
        '''
        self.notdoneyet("handbook chapter %s" % (chapter))


    def __closewin(self):
        """
        Method for closing the window and opening the main window.
        """
        self.window.destroy()


    def notdoneyet(self, txt = "feature"):
        '''
        a simple dummy method for not yet implemented methods
        '''
        self._info = messageWindow()
        self._info.showinfo("This %s is not done yet!" % (txt),
                            "SOOOORRRRYYY")
