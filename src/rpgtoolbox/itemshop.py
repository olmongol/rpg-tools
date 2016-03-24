#!/usr/bin/env python
'''
\package rpgtoolbox
\file itemshop.py
\brief Buying tool for characters equipment

With this tool players can buy stuff for their characters. Bought stuff may be 
saved as CSV file or can be transfered directly to SCs backpack...
 
\date (C) 2016
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''

import csv
from Tkinter import *
from tkFileDialog import *
from ImageTk import *
from gui.winhelper import AutoScrollbar, Message

