RPG Tools
---------
A usefull toolbox of scripts for pen & paper role playing.

# Needed Packages:

## Python 3:
This project supports since Jan 2025 no Python versions below 3.12
- tkinter
- pillow/PIL

## LaTeX:
- pdflatex with German & English language support (e.g., MIkTeX for Windows or texlive for Linux)

# Supported RPGs:
- Role Master (RM)
- Middle-Earth Role Playing (MERP)

#  Supported languages
- English
- Deutsch (partially, have to be improved)

#  Supported OSs:
- Linux/Unix
- Windows 10 (still buggy but becomes better)

# General Infomation
This uses Python v3.x with Tkinter. Some of the Scripts may be run on the command shell.
For generating a handy code documentation you can use doxygen with the concerned doxyfile in the main directory.

This project is running for a while but not finished yet. I am about to finish the character generation/bookkeeping but other planed features are:
- doing test for
  1. spell casting
     - functions for calculating enviromental and situational modifiers are finished.
     - function for base spell usage against a target is finished.
     - function for static casting maneuver is finished.
     - GUI has to be implemted.
     - connection to the EP module has to be implemented.
     - connection to the fight module has to be implemented.
  2. movement maneuvers
- fight simulation of NPCs/PCs (mainly done for prepared lists of PCs/NPCs)
  1. connect to EP module for hits & crits (calculation of EPs)
  2. connect to a (future) logging/diary tool
- half automated party/character history/log/diary


# Finished tools
- Generator for random magic items following the MERS (German) tables (linked to the character generator: ./src/rm_char_tools.py)
- RM Character Generator tool (./src/rm_char_tools.py) (even for level-up of PCs)
- attack results / combat module (./src/attackcheck.py)
- generator for a NPC / Beast database and create such lists for the combat module.(./src/monstercreator.py)
- calculating Experience Points for a party of characters (./src/test_epcalcwin.py)
- static manuevers for characters (linked to the EP module) / creating a party overview for GM
- RR for characters (linked to the EP module)
- multiple printout templates for character sheets (PDF, generated with pdflatex)
- herb module for the healing herb hunt in Middle Earth (./src/findherbs.py)
- inventory module for keeping track of the character's items and equipment; it may be used as a store tool as well. (./src/rm-inventory)
- Treasure generator (V 1.0 alpha, MERS - that means German language)
