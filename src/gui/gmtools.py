#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
\file gui/gmtools.py
\package gui
\brief Window classes for GM tools gui

In this module you find the window classes for 
\li create a treasure
\li create an single magical item 

\date (C) 2017
\author Aiko Ruprecht, Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
import string

from gui.window import *
from rpgtoolbox.treasure import *

class createTreasureWin(blankWindow):
    """
    This class builds a window for treasure generation.
    \todo createTreasureWin layout could be improved
    """
    def __init__(self, lang = 'en', filename = ''):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        \param filename Path and name of a file which is displayed as default
        """
        self.lang = lang
        
        # Create window
        self.ctwin = Tk()

        title1 = Label(self.ctwin, text = txtmenu['menu_opt'][self.lang])
        title1.grid()
        
        # List of categories
        self.__trlist = Listbox(self.ctwin, height = 0)
        
        for linetext in trtypelist[self.lang]:
            self.__trlist.insert('end', linetext)
        
        self.__trlist.grid(pady = 3)
        self.__trlist.select_set(2)

        # Text output field
        self.trcontent = ''
        self.__trtext = Text(self.ctwin, height = 10, width = 47, wrap = NONE)
        self.__trtext.insert(END, submenu['items'][self.lang]['itemgen'].strip())
        self.__trtext['bg'] = '#FFFFFF'
        self.__trtext['relief'] = 'groove'
        vs = Scrollbar(self.ctwin, orient = "vertical", command = self.__trtext.yview)
        self.__trtext.config(yscrollcommand = vs.set)
        hs = Scrollbar(self.ctwin, orient = "horizontal", command = self.__trtext.xview)
        self.__trtext.config(xscrollcommand = hs.set)
        self.__trtext.grid(row = 2, sticky = E + W + N + S)
        vs.grid(row = 2, column = 1, sticky = S + N + E)
        hs.grid(sticky = W + E)
        
        # Button to create a text describing the treasure
        self.__trcreate = Button(self.ctwin, text = submenu['items'][self.lang]['treasure'],
                               command = self.__trcreate)
        self.__trcreate.grid()
        
        # Label for the saving the text
        self.__entrylabel = Label(self.ctwin, text = '\n' + txtmenu['menu_file'][self.lang])
        self.__entrylabel.grid()
        
        # Entry field to enter the file path
        self.__filename = Entry(self.ctwin)
        #self.__filename['width'] = 69
        self.__filename['borderwidth'] = 3
        self.__filename.grid(sticky = E + W)
        self.__filename.insert(1, filename)
        
        # Button to save the text
        self.__bsave = Button(self.ctwin, text = txtbutton['but_sav'][self.lang],
                              command = self.__trsave)
        self.__bsave.grid(sticky = W)
        
        # Button to close the window
        self.__bquit = Button(self.ctwin, text = txtbutton['but_quit'][self.lang],
                               command = self.__quit)
        self.__bquit.grid()

        # make the canvas expandable
        self.ctwin.grid_rowconfigure(2, weight = 1)
        self.ctwin.grid_columnconfigure(0, weight = 1)
        
    def __trcreate(self):
        '''
        This private method creates and displays the text describing the treasure
        '''
        # Create Text
        trtype = self.__trlist.curselection()[0] + 1
        items = treasure()
        self.trcontent = items.findTreasure(trtype, output = '')
        trtext = self.trcontent
        trtext = string.join(trtext, '\n')
        
        # Display text
        self.__trtext.delete('1.0', END)
        self.__trtext.insert(END, trtext + '\n')
        
        # Tidy up
        del items
        del trtext
    
    def __trsave(self):
        '''
        This private method will save the text describing the treasure
        '''
        outputfile = self.__filename.get()
        
        if outputfile != '':
            # Create text
            trtext = self.__trtext.get('1.0', END)
            trtext = trtext.encode('utf8')
            
            try:
                # Write file
                fp = open(outputfile, "w")
                fp.write(trtext)
                fp.close()
                print((screenmesg['file_saved'][self.lang][:-1] + ': ' + outputfile))
                
                # Reset output frame
                self.__trtext.delete('1.0', END)
                self.__trtext.insert (END, submenu['items'][self.lang]['itemgen'])
                self.trcontent = ''
                
            except:
                print('Error: Invalid file name')
                print(outputfile)
            
    def __quit(self):
        '''
        This private method closes the createTreasreWin window
        '''
        self.ctwin.destroy()
    
class createMagicWin(blankWindow):
    """
    This class creates a window for the generation of magical items. The output text can be edited and copied.
    \todo createMagicWin window layout could be improved
    """
    def __init__(self, lang = 'en'):
        """
        Class constructor
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        """
        self.lang = lang
        
        # Create window
        self.cmwin = Tk()
        
        # Frame for the text output
        self.__output = Entry(self.cmwin)
        self.__output['width'] = 60
        self.__output['borderwidth'] = 3
        self.__output['bg'] = '#FFFFFF'
        self.__output['relief'] = 'groove'
        self.__output.grid(sticky = W + E)
        self.__output.insert(1, submenu['items'][self.lang]['magicgen'])
        self.itemtext = ''
        hs = Scrollbar(self.cmwin, orient = "horizontal", command = self.__output.xview)
        self.__output.config(xscrollcommand = hs.set)
        hs.grid(sticky = E + W)
        
        # Button to create treasure descriptions
        self.__bcreate = Button(self.cmwin, text = submenu['items'][self.lang]['magical'],
                               command = self.__cmcreate)
        self.__bcreate.grid()
        
        # Button to close window
        self.__bquit = Button(self.cmwin, text = txtbutton['but_quit'][self.lang],
                               command = self.__quit)
        self.__bquit.grid()
 
        # make the canvas expandable
        self.cmwin.grid_rowconfigure(0, weight = 1)
        self.cmwin.grid_columnconfigure(0, weight = 1)
       
    def __cmcreate(self):
        '''
        This private method creates and displays the text describing the magical item
        '''
        # Create text
        item = treasure()
        self.itemtext = item.magicItem()
        
        # Print text into output frame
        endpos = len(self.__output.get())
        
        if endpos > 1:
            self.__output.delete(1, endpos - 1)
            
        self.__output.insert(1, self.itemtext)
        self.__output.icursor(1)
        
        # Tidy up
        del item

    def __quit(self):
        '''
        This private method closes the createTreasreWin window
        '''
        self.cmwin.destroy()

        
