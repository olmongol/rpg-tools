#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
\package rpgtoolbox.chartotext
\file chartotext.py

\brief  brief description
Detailed description

\author Marcus Schwamberger
\email marcus@lederzeug.de
\date 22.09.2018
\copyright 2018
\version 0.1
\license GNU V3.0
'''
__updated__ = "01.01.2000"
__me__ = "/home/mongol/git/rpg-tools/src/rpgtoolbox/chartotext.py"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__copyright__ = "2018 - %s" % __updated__[-4:]
__version__ = "0.1"

import sys
import os
import json
from rpgtoolbox.globaltools import readJSON as readChar
from string import Template



class template(Template):
    '''
    Template class with delimiter '==>' instead '$'.
    '''
    delimiter = "==>"
    idpattern = r'[a-z][_a-z0-9]*'



class latexsheets(object):
    '''
    This Class transforms the JSON data of a character into a LaTeX file to generate a printable character sheet.
    '''


    def __init__(self, charfile = None, defaultpath = "./data/default"):
        '''
        Constructor of a chartolatex object.

        @param charfile path and name of the character file to transform into a latex document.
        '''
        self.charfile = charfile
        self.__tmplfiles = ['template_charsheet.tex', '']
        if defaultpath[-1] != "/":
            self.latextmplpath = defaultpath + "/latex/"

        else:
            self.latextmplpath = defaultpath + "latex/"

        if not charfile:
            print("ERROR: No character file given. Exiting...")
            sys.exit(1)

        else:
            self.character = readChar(self.charfile)

            if "/" in charfile:
                self.latexoutpath = charfile[:charfile.rfind("/") + 1] + "output/"

            else:
                self.latexoutpath = "./output/"

            if not os.path.exists(self.latexoutpath):
                os.makedirs(self.latexoutpath)


    def createMainPage(self):
        '''
        This creates the main page of the character sheet.
        '''
