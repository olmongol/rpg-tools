#!/usr/bin/env python
'''!
\file /home/mongol/git/rpg-tools/src/gui/spellcasting.py
\package gui.spellcasting
\brief Spellcasting module

Herein you find classes for a window for spellcasting tests for all type of non-attack spells.

\date (c) 2022
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "19.06.2022"
__author__ = "Marcus Schwamberger"
__me__ = "spellcasting.py"

import os
import json
from tkinter import filedialog
import re
import pickle
from PIL import Image, ImageTk
 *
import rolemaster.spellcasting as sc
from rpgtoolbox.rrwindow import *
from rpgToolDefinitions.epcalcdefs import maneuvers
from rpgToolDefinitions.helptools import RMDice as dice

from gui.window import