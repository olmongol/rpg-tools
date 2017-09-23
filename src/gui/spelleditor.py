#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
\file spelleditor.py
\package gui
\brief Editor for creating/editing spell lists


\date (C) 2017
\author mongol
\email marcus@lederzeug.de

'''
from window import *
from rpgtoolbox.lang import *
from rpgtoolbox import rolemaster as rm
import json
import os
import csv

def readCSV(filename):
    '''
    This function reads CSV files and builds a dictionary/JSON of its content.
    \param filename name (and path) of the CSV
    \return dictionary with the computed CSV table (keys = header)
    '''
    cont = []
    
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
    
        for line in csvreader:
            cont.append(line)
            
    cdic = {}
    
    for i in range(0, len(cont)):
        for j in range(0, len(cont[0])):
            if i == 0:
                cdic[cont[0][j]] = []
            else:
                cdic[cont[0][j]].append(cont[i][j])
                
    return cdic
        
    

class editSpellList(blankWindow):
    '''
    Class for Spell List Editor Window
    '''
    def __init__(self, lang = 'en', datapath = "./data/default/"):
        '''
        Class constructor
        \param lang display language. Default is English
        \param datapath main path for spell list structure
        '''
        self.lang = lang
        self.datapath = datapath
        self.filename = "spellist.json"
        blankWindow.__init__(self, self.lang)
        self.window.title(wintitle['rm_spells'][self.lang])
        self.filemenu = Menu(master = self.menu)
        self.__addFileMenu()
#        self.__addEditMenu()
        self.__addHelpMenu()
#        self.__buildWin()
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
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['quit'],
                                  command = self.__closewin)
    def __newFile(self):
        """
        This method initializes a new spell list.
        """
        self.notdoneyet("newFile")


    def __openFile(self):
        """
        This method opens a dialogue window (Tk) for opening files.
        The content of the opened file will be saved in \e file
        \e content as an array.
        """
        self.__filein = askopenfilename(filetypes = self.mask,
                                        initialdir = self.datapath)
   
        if self.__filein != "" and self.__filein != ():
            with open(self.__filein, 'r') as filecontent:
                if self.__filein[-4:].lower() == "json":
                    self.spellist = json.load(filecontent)
                elif self.__filein[-4:].lower == "spell":
                    self.spellist = json.load(filecontent)
                else:
                    msg = messageWindow()
                    msg.showinfo(errmsg['wrong_type'][self.lang])
                    pass

    def __saveFile(self):
        '''
        This method opens a file dialogue window (Tk) for saving the results
        of the EP calculation into an .json or .grp file.
        \todo has to be implemented
        '''
        filename = self.datapath + "magic/" + self.spellist['en']['type'].replace(' ', '_') + ".json"       

        if os.path.exists(filename):
            os.rename(filename, "BACKUP-" + filename)
        
        with open(filename, "w") as outfile:
            json.dump(self.character, outfile, sort_keys = True, indent = 4, ensure_ascii = False)          
        
        msg = messageWindow()
        msg.showinfo(processing['saved'][self.lang], 'Info')
        
    def __closewin(self):
        '''
        A method to destroy the current window and go back to MainWindow.
        '''
        self.window.destroy()
#        self.window = MainWindow(lang = self.lang, char = self.character)  

    def __addHelpMenu(self):
        '''
        Adds a help menu entry to menu bar.
        '''
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)
#        self.helpmenu.add_command(label = submenu['help'][self.lang]['win'],
#                              command = self.__helpAWin)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)   
        
    def __buildWin(self):
        '''
        A method to build the window elements and widgets.
        '''
        self.__sltypes = rm.spellisttypes
        self.__sptypes = rm.spelltypes
        ##\var self.__optWdg
        # contains all needed OptionWidgets
        self.__optWdg = {}
        ##\var self.__enryWdg
        # contains EntryWidgets
        self.__entryWdg = {}
        ##\var self.__slData
        # contains data of all spell list widgets StringVar() IntVar()
        self.__slData = {'spells': []}
        Label(master = self.window,
              width = 10,
              text = rm.labels[self.lang]['sl-type']
              ).grid(column = 0, row = 0)
        self.__slData['sl-type'] = StringVar()      
        self.__optWdg['sl-type'] = OptionMenu(self.window,
                                              self.__sltypes,
                                                self.__slData['sl-type'],
                                                command = self.__updSLData
                                              ).grid(column = 1, row = 0, sticky = EW)
        Label(master = self.window,
              width = 15,
              text = rm.labels[self.lang]['name']
              ).grid(column = 3, row = 0)
              
        self.__slData['sl_name'] = StringVar()
        
        Entry(master = self.window,
              width = 35,
              textvariable = self.__slData['sl_name'],
              ).grid(column = 4, row = 0)
        Label(master = self.window,
              width = 10,
              text = rm.labels[self.lang]['spec_note']
              ).grid(column = 0, columnspan = 4, row = 1)
              
        self.__slData['spec_notes'] = StringVar()
        Entry(master = self.window,
              width = 200,
              height = 60,
              textvariable = self.__slData['spec_notes'],
              ).grid(column = 0, columnspan = 4, row = 2)
        
        listbox = Listbox(master = self.window,
                  listvariable = self.__slData['spells'],
                  width = 200,
                  height = 120,
                  ).grid(column = 0, columnspan = 4, row = 3)
                  
        Label(master = self.window,
              width = 10,
              text = rm.labels[self.lang]['spell']
              ).grid(column = 0, row = 4)
              
        self.__slData['spell'] = StringVar()
        Entry(master = self.window,
              width = 10,
              textvariable = self.__slData['spell']
              ).grid(column = 0, row = 5)
              
        Label(master = self.window,
              width = 10,
              text = rm.labels[self.lang]['lvl']
              ).grid(column = 1, row = 4)
              
        self.__slData['lvl'] = IntVar()
        Entry(master = self.window,
              width = 10,
              textvariable = self.__slData['lvl']
              ).grid(column = 1, row = 5)
        
        Label(master = self.window,
              width = 10,
              text = rm.labels[self.lang]['aoe']
              ).grid(column = 2, row = 4)
        self.__slData['aoe'] = StringVar()
        Entry(master = self.window,
              width = 10,
              textvariable = self.__slData['aoe']
              ).grid(column = 2, row = 5)
              
        Label(master = self.window,
              width = 10,
              text = rm.labels[self.lang]['dura']
              ).grid(column = 3, row = 4)
        self.__slData['dura'] = StringVar()
        Entry(master = self.window,
              width = 10,
              textvariable = self.__slData['dura']
              ).grid(column = 3, row = 5)
        
        Label(master = self.window,
              width = 10,
              text = rm.labels[self.lang]['range']
              ).grid(column = 4, row = 4)
        self.__slData['range'] = StringVar()
        Entry(master = self.window,
              width = 10,
              textvariable = self.__slData['range']
              ).grid(column = 4, row = 5)
              
        Label(master = self.window,
              width = 10,
              text = rm.labels[self.lang]['type']
              ).grid(column = 5, row = 4)
        self.__slData['type'] = StringVar()
        OptionMenu(self.window,
                   rm.spellisttypes[self.lang].keys(),
                   *self.__slData['type'],
                   command = self.__updSLData
                   ).grid(column = 5, row = 5)
                   
        Label(master = self.window,
              width = 50,
              text = rm.labels[self.lang]['descr']
              ).grid(column = 0, columnspan = 4, row = 6)
        
        self.__slData['descr'] = StringVar()      
        Entry(master = self.window,
              width = 200,
              height = 100,
              textvariable = self.__slData['descr']
              ).grid(column = 0, columnspan = 4, row = 7)
              
        # \todo text has to be replaced by lang.labels['update']      
        Button(master = self.window,
               text = 'update',
               width = 15,
               command = self.__updSLData
               ).grid(column = 5, row = 7)
        
              
#        self.__optWdg[str(i)] = OptionMenu(self.window,
#                               self.__prio["%s - %d" % (self.__catnames[self.lang]['weapon'], i)],
#                               *self.weaponcats,
#                               command = self.__getPrio)
#        self.__optWdg[str(i)].config(width = 50)
#        self.__optWdg[str(i)].grid(column = 0, row = i, sticky = "W")
        print "not done yet"
        
    def __updSLData(self):
        '''
        This updates new/modified Spell List Data
        \todo has to be implemented
        '''
        self.notdoneyet('updSLData')
        
if __name__ == '__main__':
    win = editSpellList()
