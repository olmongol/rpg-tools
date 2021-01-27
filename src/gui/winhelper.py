#!/usr/bin/env python
'''!
\file winhelper.py

\brief collection of helper tools for building Tk() windows/apps


\date (C) 2012 - 2021
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0

'''

import sys

from rpgtoolbox.globaltools import *
from rpgtoolbox.lang import *

__updated__ = "28.12.2020"

if sys.version_info >= (2, 6) and sys.version_info < (3, 0):
    from tkinter import *

elif sys.version_info >= (3, 2):
    from tkinter import *



def buildWinCheck(win = None, opts = {}):
    """!
    This function is a  little helper for building windows with check buttons.

    \param win this is the Tk() main window where the frames build by this
               function will be set in.
    \param opts a dictionary with the options which can be chosen.
    """

    index = sortIndex(opts)
    li = len(index)
    b = 20
    no = li / b
    i = 0
    j = 0
    frames = []
    values = {}
    buttons = {}

    if win != None:
        if no < float(li) / b:
            no += 1

        while i < no:
            frames.append(Frame(master = win, height = 25))
            frames[i].pack(side = LEFT)

            while j < b and j < li:
                values[index[j]] = IntVar()
                buttons[index[j]] = Checkbutton(master = frames[i],
                                                text = index[j],
                                                offvalue = 0,
                                                onvalue = 1,
                                                variable = values[index[j]],
                                                anchor = NW
                                                )
                buttons[index[j]].pack(anchor = "nw")

                if opts[index[j]] == True:
                    buttons[index[j]].select()
                j += 1

            b += 20
            i += 1

    return values



def buildWinRadio(win = None, opts = {}):
    """
    This function is a little helper to build with radio buttons.

    \param win    this is the Tk() window where the herein build frames were
                  placed in.
    \param opts   This is a dictionary which holds the selectable options
    \retval value A string object with the radio button content of the (chosen)
                  language will be returned.
    """
    result = "en"

    if win != None:
        index = sortIndex(opts)
        value = StringVar()

        for key in index:
            Radiobutton(master = win,
                        text = opts[key],
                        variable = value,
                        value = key
                        ).pack(anchor = 'nw')

    return value



class AutoScrollbar(Scrollbar):
    """
    A scrollbar that hides itself if it's not needed. It only works if the grid
    geometry manager is used.
    """


    def set(self, lo, hi):
        """
        sets or hides the scrollbar
        """
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()

        Scrollbar.set(self, lo, hi)


    def pack(self, **kw):
        """
        Error handling method: This cannot be used with pack
        """
        raise TclError("cannot use pack() with this widget")


    def place(self, **kw):
        """
        Error handling method: This cannot be used with place
        """
        raise TclError("cannot use place with this widget")



class InfoCanvas(object):
    '''!
    A Canvas-widget that holds a scrollable Message-widget. This widget can only
    be used by the grid() Geometry Manager.

    \param master master Tk()-object
    \param text text string that shall be displayed
    \param width width of the canvas in pixel
    \param row row index where to put this widget in the window structure
    \param column column index where to put this widget in the window structure
    '''


    def __init__(self, master = None,
                 text = None,
                 textvariable = None,
                 width = 300,
                 row = 0,
                 column = 0,
                 relief = SUNKEN):
        """!
        Constructor InfoCanvas

        \param master master Tk()-object
        \param text text string that shall be displayed
        \param width width of the canvas in pixel
        \param row row index where to put this widget in the window structure
        \param column column index where to put this widget in the window structure
        """
        self.master = master
        self.row = row
        self.column = column
        self.width = width
        self.relief = relief

        self.message = StringVar()
        if text != None:
            self.message.set(text)
        elif textvariable != None:
            self.message = textvariable
        else:
            raise TclError("No valid text parameter")

        self.vscrollbar = AutoScrollbar(self.master)
        self.vscrollbar.grid(row = self.row,
                             column = self.column + 1,
                             sticky = N + S)

        self.hscrollbar = AutoScrollbar(self.master, orient = HORIZONTAL)
        self.hscrollbar.grid(row = self.row + 1,
                             column = self.column,
                             sticky = E + W)

        self.canvas = Canvas (master = self.master,
                              width = self.width,
                              yscrollcommand = self.vscrollbar.set,
                              xscrollcommand = self.hscrollbar.set)
        self.canvas.grid(row = self.row,
                         column = self.column,
                         sticky = "news")

        self.vscrollbar.config(command = self.canvas.yview)
        self.hscrollbar.config(command = self.canvas.xview)

        self.master.grid_rowconfigure(self.row, weight = 1)
        self.master.grid_columnconfigure(self.column, weight = 1)

        self.frame = Frame(self.canvas)
        self.frame.rowconfigure(self.row + 1, weight = 1)
        self.frame.columnconfigure(self.column, weight = 1)

        self.mbox = Message(master = self.frame,
                               justify = LEFT,
                               relief = self.relief,
                               textvariable = self.message)
        self.mbox.grid(row = 0,
                       column = 0,
                       sticky = "news")

        self.canvas.create_window(0, 0, anchor = NW, window = self.frame)
        self.frame.update_idletasks()
        self.canvas.config(scrollregion = self.canvas.bbox("all"))


    def pack(self, **kw):
        """
        Error handling method: This cannot be used with pack
        """
        raise TclError("cannot use pack() with this widget")


    def place(self, **kw):
        """
        Error handling method: This cannot be used with place
        """
        raise TclError("cannot use place with this widget")
