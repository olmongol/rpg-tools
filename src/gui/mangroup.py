#!/usr/bin/env python
'''
@file mangroup.py
@package gui
@brief Window class to handle character groups.

@date (C) 2020
@author Marcus Schwamberger
@email marcus@lederzeug.de

'''
from gui.window import *
from rpgtoolbox.lang import *
from tkinter import filedialog
import json
import os
import re



class groupWin(blankWindow):
    '''
    This window is made for managing groups of characters:
    - add/remove character from existing group
    - create new groups
    '''


    def __init__(self, lang = "en"):
        '''
        Class constructor
        '''
        self.lang = lang
        self.charlist = []
        blankWindow.__init__(self, self.lang)
#        self.window = Toplevel()
        self.window.title("Grp. Management")
        self.__addMenu()
        self.__helpMenu()
        self.__buildWin()
        self.window.mainloop()


    def __addMenu(self):
        '''
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__open)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)


    def __helpMenu(self):
        """
        This methods defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __buildWin(self):
        """
        This method builds the window content.
        """
        vcharscroll = Scrollbar(self.window, orient = VERTICAL)
        self.charbox = Listbox(self.window,
                               yscrollcommand = vcharscroll.set,
                               selectmode = EXTENDED,
                               width = 100,
                               height = 10)
        vcharscroll.config(command = self.charbox.yview)
        self.charbox.grid(row = 0, column = 0, columnspan = 2, sticky = "NEWS")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__addChar
               ).grid(row = 1, column = 0, sticky = "NSWE")

        Button(self.window,
               text = txtbutton["but_del"][self.lang],
               command = self.__remChar
               ).grid(row = 1, column = 1, sticky = "NSEw")


    def __remChar(self):
        '''
        This method removes Characters from listbox and from character list
        '''
        select = self.charbox.curselection()
        regex = re.compile(r"^([a-zA-Z ]+): ([a-zA-Z 0-9]+) \(.+\)$")
        rmlist = []

        for i in select:
            selchar = self.charbox.get(i)
            lookup = regex.match(selchar)
            if lookup:
                for c in range(0, len(self.charlist)):
                    if self.charlist[c]["player"] == lookup.group(1) and self.charlist[c]["name"] == lookup.group(2):
                        rmlist.append(c)

            for rm in rmlist:
                del(self.charlist[rm])

            for elem in select:
                self.charbox.delete(elem)


    def __addChar(self):
        '''
        This method adds characters from file to the character list and a character
        entry to the listbox.
        '''
        opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Character Files", ".json")])
        with open(opendir, "r") as fp:
            character = json.load(fp)

        self.charlist.append(character)
        lbentry = "{}: {} ({}-{}/{}/{})".format(character["player"],
                                             character['name'],
                                             character['prof'],
                                             character["lvl"],
                                             character["culture"],
                                             character['race'])
        self.charbox.insert(END, lbentry)


    def __open(self):
        '''
        This opens a file dialog window for opening a group file and put all
        characters to the listbox.
        '''
        opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])
        with open(opendir, "r") as fp:
            self.charlist = json.load(fp)

        self.charbox.delete(0, END)

        for character in self.charlist:
            lbentry = "{}: {} ({}-{}/{}/{})".format(character["player"],
                                             character['name'],
                                             character['prof'],
                                             character["lvl"],
                                             character["culture"],
                                             character['race'])
            self.charbox.insert(END, lbentry)


    def __save(self):
        '''
        This saves the character list to a JSON file
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.charlist, fp, indent = 4)


    def __quit(self):
        '''
        This method closes the window
        '''
        self.window.destroy()

#test = groupWin("en")
