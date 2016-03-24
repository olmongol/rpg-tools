#!/usr/bin/env python
'''
\file /home/mongol/workspace/bpcheck/src/gui/window2.py
\package gui.window2
\brief All classes for building the GUI with Tk.


\date (C) 2012
\author Marcus Schwamberger
\email marcus@lederzeug.de

'''
__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2012 " + __author__
__license__ = "GPL V3 "
__email__ = "marcus@lederzeug.de"
__version__ = "0.1 alpha"
__me__ = "Blood Pressure Checker"

import os

from Tkinter import *
from tkFileDialog import *
from gui.language import *

class messageWindow(object):
    """
    A class to build a message window containing version, author and email on
    default. 
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

        \param message contains a message to be displayed in the message window.
                       It may be an array, a string or a number (integer/float).
        \param title   sets the title of the message window. The default is 
                       'Info'.
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
            exit(1)

        label = Label(self.window,
                      text = message,
                      wraplength = 300,
                      padx = 10,
                      pady = 10,
                      font = ('Arial', 10))

        button = Button(self.window,
                        text = buttons['ok'][self.lang],
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
        self.mask = [txtwin['bpc'][self.lang],
                    txtwin['all_files'][self.lang]
                    ]
        
    def __addMenu(self):
        '''
        This private method just adds the menu bar into the window's layout
        '''
        self.menu = Menu(self.window)
        self.window.configure(menu = self.menu)
 
    def _addHelpMenu(self):
        '''
        This adds the help menu to the menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help']['about'][self.lang],
                                  command = self._helpAbout) 
    
    def _helpAbout(self):
        '''
        This method just opens a message window with the basic information about
        the ADaManT XML Generator (like version and copyright)
        '''
        self.about = "%s\nVersion %s\n\n%s\n%s\n%s" % (__me__,
                                                      __version__,
                                                      __copyright__,
                                                      __license__,
                                                      __email__)
        self.msg = messageWindow()
        self.msg.showinfo(self.about)
        
    def _notdoneyet(self):
        """
        The most important dummy function of the whole coding process!
        """
        self.ndy = messageWindow()
        self.ndy.showinfo(screenmsg['notdoneyet'][self.lang])

class mainWindow(blankWindow):
    """
    This class generates the main window of the program.
    """
    def __init__(self, lang = 'de', storepath = None):
        '''
        Constructor
        '''
        self._myfile = ""
        
        if storepath == None:
            self.storepath = os.path.expanduser('~')
        else:
            self.storepath = storepath
                
        blankWindow.__init__(self, lang)
        self.lang = lang      
        self._readCfg()  
        self.window.title(wintitle['main'][self.lang])
        
        self._addFileMenu()
        self._addEditMenu()
        self._addOptMenu()
        self._addHelpMenu()
        self.window.mainloop()
        
    def _addFileMenu(self):
        """
        This method adds a File menu to the windows menu bar.
        """
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file']['new'][self.lang],
                                  command = self._newFile)
        self.filemenu.add_command(label = submenu['file']['open'][self.lang],
                                  command = self._openFile)
        self.filemenu.add_command(label = submenu['file']['save'][self.lang],
                                  command = self._saveFile)
        self.filemenu.add_command(label = submenu['file']['save_as'][self.lang],
                                  command = self._saveFileAs)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file']['quit'][self.lang],
                                  command = self.window.destroy) 
        
    def _newFile(self):
        '''
        This generates a new file.
        \todo this method has to be implemented 
        '''
        self._notdoneyet()

    def _openFile(self):
        '''
        This opens a file.
        \todo this method has to be implemented fully
        '''
        self._myfile = askopenfilename(filetypes = self.mask,
                                       initialdir = self.storepath)
        self.fp = open(self._myfile, 'r')
        self._fcontent = self.fp.readlines()
        self.fp.close()
                
    def _saveFile(self):
        '''
        This saves the data into a file.
        \todo this method has to be implemented for new files.
        '''
        if self._myfile == "":
            self._notdoneyet()
        else:
            self.fp = open(self._myfile, 'w')
            self.fp.write(self._fcontent)
            self.fp.close()
            self._info = messageWindow(self.lang)
            self._info.showinfo(message = self._myfile + '\n'\
                                + screenmsg['saved'][self.lang])
        
    def _saveFileAs(self):
        '''
        Save data in another file.
        \todo this method has to be implemented 
        '''
        self._notdoneyet()

    def _addEditMenu(self):
        '''
        This adds the edit menu to the menu bar.
        \todo this method has to be implemented
        '''
        self.editmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_edit'][self.lang],
                              menu = self.editmenu)
        self.editmenu.add_command(label = submenu['edit']['add'][self.lang],
                                 command = self._addData)
        self.editmenu.add_command(label = submenu['edit']['remove'][self.lang],
                                 command = self._removeData)
        self.editmenu.add_command(label = submenu['edit']['edit'][self.lang],
                                 command = self._editData)
        self.editmenu.add_separator()
        self.editmenu.add_command(label = submenu['edit']['graph'][self.lang],
                                  command = self._plotGraph)
        
    def _addData(self):
        '''
        This adds data to an existing data set.
        \todo this method has to be implemented
        '''
        self._notdoneyet()
        
    def _removeData(self):
        '''
        This removes data from the data set
        \todo this method has to be implemented
        '''
        self._notdoneyet()
        
    def _editData(self):
        '''
        This edits data of an opened data set
        \todo this method has to be implemented
        '''
        self._notdoneyet()
            
    def _addOptMenu(self):
        '''
        This adds an Options menu
        '''
        self.optmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_opt'][self.lang],
                              menu = self.optmenu)
        self.optmenu.add_command(label = submenu['opts']['basic'][self.lang],
                                 command = self._basicOpts)
        self.optmenu.add_command(label = submenu['opts']['graph'][self.lang],
                                 command = self._graphOpts)
        self.optmenu.add_command(label = submenu['opts']['output'][self.lang],
                                 command = self._outputOpts)
            
    def _basicOpts(self):
        '''
        This opens a window for basic options
        \todo has to be implemented
        ''' 
        self.window.destroy()
        self.window = optWindow(self.lang, 'basic', self.cnf)
        
    def _graphOpts(self):
        '''
        This opens a window for graphical options
        \todo has to be implemented
        ''' 
        self.window.destroy()
        self.window = optWindow(self.lang, 'graph', self.cnf)         
        
    def _outputOpts(self):
        '''
        This opens a window for output options
        \todo has to be implemented
        ''' 
        self.window.destroy()
        self.window = optWindow(self.lang, 'output', self.cnf)
        
    def _addHelpMenu(self):
        '''
        This adds the help menu to the menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help']['context'][self.lang],
                                  command = self._helpContext)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help']['about'][self.lang],
                                  command = self._helpAbout)
        
    def _helpContext(self):
        '''
        This adds a context menu to the help menu.
        \todo this method has to be implemented
        '''
        self._notdoneyet()
    
    def _readCfg(self):
        '''
        This reads the config file (if any) automatically.
        \todo has to be implemented fully
        '''        
        self.cnf = {'lang' : 'de',
                    'profile' : 'default.bpc',
                    }
#        self._notdoneyet()
    
    def _plotGraph(self):
        '''
        Plotting graphs from selected data set
        \todo has to be implemented fully
        '''
        self._notdoneyet()
        

class optWindow(blankWindow):
    '''
    This opens an option window where all configurations can be done.
    \param lang supported language which shall be used for the GUI
    \param opts type of options that shall be set: basic, graph, output
    \param cfg  this is a dictionary that holds existing configuration 
                parameters.
    '''
    
    def __init__(self, lang = 'de', opts = 'basic', cfg = {}):
        '''
        Constructor
        '''
        self.lang = lang
        self.opts = opts
        self.cfg = cfg
        self._cfgfile = ".bpchecker"
        self.storepath = os.path.expanduser('~')
                
        blankWindow.__init__(self, lang)
        self.lang = lang        
        self.opts = opts
        self.cfg = cfg
        self.window.title(wintitle['options'][self.lang])
        self._checkOpts()
        self._addFileMenu()
        self._addHelpMenu()
#        self.window.mainloop()

    def _addFileMenu(self):
        """
        This adds a file menu to the window's menu bar
        \todo has to be implemented
        """
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file']['save'][self.lang],
                                  command = self._saveOpts)     
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file']['quit'][self.lang],
                                  command = self._closeWindow)  
        
    def _addHelpMenu(self):
        '''
        This adds the help menu to the menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_help'][self.lang],
                              menu = self.helpmenu)
        self.helpmenu.add_command(label = submenu['help']['context'][self.lang],
                                  command = self._helpContext)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help']['about'][self.lang],
                                  command = self._helpAbout)
    
    def _checkOpts(self):
        '''
        This checks which kind of options shal be set and modifies the 
        options window in that way.
        \todo has to be implemented fully
        '''
        if self.opts == "basic":
            self._notdoneyet()
            print("Basic Options")
        elif self.opts == "graph":
            self._notdoneyet()
            print("Graph Options")
        elif self.opts == "output":
            self._notdoneyet()
            print("Output Options")
        
   
    def _saveOpts(self):
        """ 
        This saves options into a config file.
        \todo has to be implemented fully    
        """
        self._notdoneyet()
        
    def _closeWindow(self):
        '''
        This closes the options' window and reopens the main window 
        again.
        '''
        self._saveOpts()
        self.window.destroy()
        self.window = mainWindow(lang = self.lang, storepath = self.storepath)
        
