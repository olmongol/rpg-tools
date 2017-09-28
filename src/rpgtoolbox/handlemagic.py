#!/usr/bin/env python
'''
\package rpgtoolbox
\file handlemagic.py
This  module holds helpers handling all spell list/magical issues

\date (C) 2015-2017
\license GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
import os
import logbox as log
from globaltools import readFile as readNotes
from globaltools import readCSV


logger = log.createLogger('magic', 'warning', '1 MB', 1, './' , 'handlemagic.log')

class getSpells(object):
    '''
    This class generates an object to get all spell lists into the right context 
    for a single character.
    \todo a method that sets the right skill category for the spell list
    '''


    def __init__(self, datadir = "./data", charprof = "", charrealm = []):
        '''
        \param datadir directory where to find the magic directory
        \param charprof profession of the character
        \param charrealm realm(s) of magic
        '''
        self.prof = charprof
        self.realm = charrealm
        self.__getAllLists(datadir + "/default/magic")
        
    def __getAllLists(self, datadir):
        '''
        Get all spell lists and spell categories from disc
        \param datadir path to the magic directory
        '''
        spellcat = os.listdir(datadir)
        spellcat.sort()
        self.spelllists = {}
        
        if datadir[-1] != "/":
            datadir += "/"
            
        for i in range(0, len(spellcat)):
            slcat = spellcat[i].replace('_', ' ')
            self.spelllists[slcat] = {}
            splst = os.listdir(datadir + spellcat[i])
            
            for j in range(0, len(splst)):
                
                if splst[j].endswith(".csv"):
                    slist = splst[j].replace('_', ' ')[:-4]
                    self.spelllists[slcat][slist] = {}
                    
                    self.spelllists[slcat][slist]["Special Notes"] = readNotes(datadir + spellcat[i], splst[j][:-4] + ".sn")
                    self.spelllists[slcat][slist]['Spells'] = readCSV(datadir + spellcat[i] + "/" + splst[j])
#                    self.spelllists[slcat][slist]['Category']
    

