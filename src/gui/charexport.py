#!/usr/bin/env python
'''
\file charexport.py
\package gui.charexport
\brief Module for export RPG Characters to LaTeX/PDF.


\date (C) 2015 - 2018
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
from tkinter import *
from tkinter.filedialog import *
from rpgtoolbox.lang import *
from rpgtoolbox import logbox as log
from rpgtoolbox.globaltools import *
from string import Template
from gui.window import *
import json
import sys
import os

__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__version__ = "1.0"
__license__ = "GNU V3.0"
__me__ = "A RPG tool package for Python 2.7"
__updated__ = "30.04.2018"
__copyright__ = "(C) 2015-%s %s" % (__updated__[-4:], __author__)

Template.delimiter = "=>"



class exportWindow(blankWindow):
    '''
    This window class will display a character sheet on the screen
    '''


    def __init__(self, lang = 'en', storepath = "./data/",
                 title = "Export Character", char = None):

        self._character = char
        self._tmplpath = storepath + "default/latex/"


    def createLaTeX(self):
        '''
        This method builds LaTeX source files for the character sheet
        '''
