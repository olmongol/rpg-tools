#!/usr/bin/env python
'''!
\file window.py
\package gui.window
\brief Some classes for GUI


\date (C) 2015 - 2022
\author Marcus Schwambeger
\email marcus@lederzeug.de
\version 1.1.1
'''
from tkinter import *
from tkinter.filedialog import *

from rpgToolDefinitions.helptools import RMDice
from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import *
from rpgtoolbox.lang import *

__author__ = "Marcus Schwamberger"
__updated__ = "06.12.2023"
__copyright__ = "(C) 2015-{} {}".format(__updated__[-4:], __author__)
__email__ = "marcus@lederzeug.de"
__version__ = "1.1.1"
__license__ = "GNU V3.0"
__me__ = "A RPG tool package for Python 3"

mycnf = chkCfg()
logger = log.createLogger('window', 'warning', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = "window.log")



class testRollWindow(object):
    """
    A class to build a window for test rolls like fumbles, resistance rolls etc.
    It holds a message, an Entry widged for the roll result, a button for computer
    based roll, and finally a button to display the result.
    """


    def __init__(self, rootwin = None, lang = 'en', resultwidget = None):
        """!
        Constructor \ref testRollWindow

        @param rootwin a reference to the root window calling this one
        @param lang contains the chosen display language.
        @param resultwidget reference to the widget to compute the result of the
               test roll
        """

        self.lang = lang
        self.rootwin = rootwin
        self.resultwidget = resultwidget
        self.window = Toplevel()
        self.showinfo("Fumble!!!")


    def showinfo(self, message = '', title = 'Info'):
        """!
        This method adds and displays content to the message window.

        @param message contains a message to be displayed in the
                       message window. It may be an array, a string or
                       a number (integer/float).
        @param title   sets the title of the message window. The
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
            self.logger.error('Message Window gets the wrong data type for message! Exiting...')
            exit(1)

        self.message = IntVar()
        self.message.set(message)

        label = Label(self.window,
                      textvariable = self.message,
                      wraplength = 300,
                      padx = 10,
                      pady = 10,
                      font = ('Arial', 10))
        #label.grid(row = 0, column = 0, rowspan = 4, columnspan = 3, sticky = "NEWS")

        self.rollresult = StringVar()
        self.rollresult.set("0")
        entry = Entry(self.window,
                      justify = "center",
                      textvariable = self.rollresult
                      )
        #entry.grid(row = 4, column = 0, sticky = "WE")

        button1 = Button(self.window,
                text = labels["roll"][self.lang],
                command = self.rollDice)
        #button1.grid(row = 4, column = 1, sticky = "WE")

        button2 = Button(self.window,
                        text = txtmenu['but_ok'][self.lang],
                        command = self.putFumbleResult)
        #button2.grid(row4, column = 2, sticky = "WE")
        label.pack()
        Label(self.window, width = 35).pack()
        entry.pack()
        button1.pack()
        button2.pack()
        self.window.mainloop()


    def rollDice(self, event = None):
        """!
        This method just rolls virtual RM dices

        @retval result total result of the dice roll
        """
        self.result, self.unmodified = RMDice(rules = "RM")
        self.rollresult.set(self.result)


    def putFumbleResult(self, event = None):
        """!
        This connects to rhe root window responsive widget and transfers the roll
        result
        """
        self.result = self.rollresult.get().strip("(,)")
        self.resultwidget(self.result)
        self.window.destroy()



class messageWindow(object):
    """
    A class to build a message window containing version, author and
    email on default.
    \param lang contains the chosen display language.
    """


    def __init__(self, lang = 'en'):
        """!
        Constructor messageWindow
        \param lang contains the chosen display language.
        """

        self.lang = lang
        self.window = Toplevel()


    def showinfo(self, message = '', title = 'Info'):
        """!
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
    '''!
    A simple window class with  a not filled menu bar.
    \param lang  chosen language for the menu.
    '''


    def __init__(self, lang = 'en'):
        '''!
        Class constructor blankWindow
        \param lang  chosen language for the menu.
        '''
        self.lang = lang
        self.window = Tk()
        #self.window = window
        self.__addMenu()

        ##\var self.mask
        # This is the file extension filter for the file I/O window
        self.mask = [txtwin['json_files'][self.lang],
                     txtwin['spell_files'][self.lang],
                     txtwin['all_files'][self.lang]
                     ]


    def __addMenu(self):
        '''
        This private method just adds the menu bar into the window's
        layout
        '''
        ##\var self.menu
        # the root object for the menu bar
        self.menu = Menu(self.window)
        self.window.configure(menu = self.menu)


    def _helpAbout(self):
        '''
        This method just opens a message window with the basic
        information about the rpg-tools XML Generator (like version and
        copyright)
        '''
        ## \var self.about
        # info parameters of the program like version, license etc.
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
