#!/usr/bin/env python
'''
\file calc_ep.py
\package calc_ep
\brief This is a little tool for calculating EPs for MERS/RM


\date (C) 2015-2016
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 0.3
'''
#import ConfigParser as CP
import Tkinter
from gui.window import *
from rpgtoolbox.lang import *
__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015 " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "0.5.5 alpha"
__me__ = "A MERS/RM EP Calculator for Python 2.x"

class MainWindow(blankWindow):
    """
    This is the class for the main window object.
    \param lang The chosen language for window's and button's texts. At 
                the moment, only English (en, default value) and German 
                (de) are supported. 
    \param title title of the window
    \param storepath path where things like options have to be stored    
    """
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
        Label(self.window, width = 60).pack()
        self.__addFileMenu()
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

        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['quit'],
                                  command = self.window.destroy)
    def __newFile(self):
        """
        This method opens a new window for generation of a new 
        functional structure.
        """
        self.window.destroy()
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
        self.notdoneyet()
#        self.window = confWindow(self.lang)        
        
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
        This method will show the ADaManT Handbook
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
                                                      __email__)
        self.msg = messageWindow()
        self.msg.showinfo(self.about)
    
class confWindow(blankWindow):
    """
    This class builds a window for selecting and saving options of 
    ADaManT. For now it is just choosing the language for menus and 
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
     
mywindow = MainWindow(lang = "de", title = "EP Calculator")
