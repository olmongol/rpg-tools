#!/usr/bin/env python
'''!
\file csvdef.py
\package rpgToolDefinitions.csvdef
\brief Inital definitions of needed CSV files
This module holds the inital definitions of needed CSV files and where to put
them into the directory tree.

\date (C) 2016 -2021
\author Marcus Schwamberger
\email marcus@lederzeug.de

'''
import os

__updated__ = "28.12.2020"
initialHeaders = { 'exp.csv': 'Date,Char,Exp,Lvl',
                   'count_getCrit.csv': 'Date,Char,gCritType,gCritNo',
                   'count_hit_man.csv': 'Date,Char,Hits,Travel,Routine,vEasy,Easy,Medium,Heavy,vHeavy,Foolish,Absurd,Individual',
                   'count_MKS.csv': 'Date,Char,killLvl,killNo',
                   'count_spell.csv': 'Date,Char,SpellLvl,SpellNo'
                   }



def initChar(datapath = './data/party1', charname = "Digger"):
    '''!
    This function creates the initial files for new Characters
    \param datapath Path where the adventure party is stored
    \param charname Name of the new character (same name for the directory)
    '''
    if not os.path.exists(datapath):
        os.makedirs(datapath)

    if not os.path.exists(datapath + "/" + charname):
        os.makedirs(datapath + '/' + charname)

    for key in initialHeaders:
        fp = open(datapath + '/' + charname + '/' + key, "w")
        fp.write(initialHeaders[key])
        fp.close()

