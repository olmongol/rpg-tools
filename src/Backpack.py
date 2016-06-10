#!/usr/bin/env python
'''
\file Backpack.py
\brief This is a simple tool to keep track of a character's backpack

With this tool you are able to keep track of all the items and the money a 
pen & paper RPG character is carrying. To make it work as an "Online Shop" you 
need to set up a MySQL data base.

\date (C) 2015
\author Marcus Schwamberger
\email marcus@lederzeug.de

\todo Modul: reading and interpreting mysql configuration
\todo Modul: create intial mysql db
\todo Modul: insert, update and read data from db
\todo Modul: saves extracted data as PDF
'''
__author__ = "Marcus Schwambgerger"
__copyright__ = "(C) 2015 Marcus Schwamberger"
__date__ = "2015"
__version__ = "1.0"
__me__ = "RPG Backpack"

__osnames = {'posix' : 'Linux/Unix',
#             'nt'    : 'Windows',
             'mac'   : 'Mac OS',
#             'os2'   : 'OS/2',
#             'ce'    : 'Windows CE',
#             'Java'  : 'Java'
             }

import sys
import gui
import toolbox.lang as lang

# check Python version
if sys.version_info >= (2, 6) and sys.version_info < (3, 0):
    result = 2
    # Python 2 detected
    from Tkinter import *
    from gui.window2 import *

elif sys.version_info >= (3, 2):
    result = 3
    # Python 3 detected
    from tkinter import *
    from gui.window3 import *
else:
    print(lang.screenmesg['wrongver']["en"])
    result = 1