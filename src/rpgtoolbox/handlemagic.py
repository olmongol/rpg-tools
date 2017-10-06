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
from rolemaster import DPCostSpells

logger = log.createLogger('magic', 'warning', '1 MB', 1, './' , 'handlemagic.log')

class getSpells(object):
    '''
    This class generates an object to get all spell lists into the right context 
    for a single character.
    '''


    def __init__(self, datadir = "./data", charprof = "", charrealm = [], charlvl = 1):
        '''
        \param datadir directory where to find the magic directory
        \param charprof profession of the character
        \param charrealm realm(s) of magic
        \param charlvl character's lvl to calculate costs
        \todo  calculating development costs dependent on class and level
        '''
        self.prof = charprof
        self.realm = charrealm
        self.lvl = charlvl
        self.spelllists = {}
        self.__getAllLists(datadir + "/default/magic")
        self.__categorizeSLs()

        if type(self.realm) != type([]):
            self.realm = [self.realm]
        
    def __getAllLists(self, datadir):
        '''
        Get all spell lists and spell categories from disc
        \param datadir path to the magic directory
        '''
        spellcat = os.listdir(datadir)
        spellcat.sort()
        
        
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

    def __categorizeSLs(self):
        '''
        This private method categorizes spell lists for identifying the developing
        costs for a player character
        
        '''
        purespellusers = {"Animist": ["Channeling"],
                        "CLeric" : ["Channeling"],
                        "Illusionist" : ["Essence"],
                        "Magician" : ["Essence"],
                        "Lay Healer" : ["Mentalism"],
                        "Mentalist" : ["Mentalism"],
                        }
        hybridspellusers = {"Healer" : ["Channeling", "Mentalism"],
                            "Mystic" : ["Essence", "Mentalism"],
                            "Sorcerer": ["Channeling", "Essence"]
                            }
        semispellusers = {"Paladin" : ["Channeling"],
                         "Ranger" : ["Channeling"],
                         "Dabbler": ["Essence"],
                         "Monk": ["Essence"],
                         "Bard" : ["Mentalism"],
                         "Magent": ["Mentalism"]
                         }
        nonspellusers = {"Fighter":[],
                        "Thief":[],
                        "Rogue":[],
                        "Warrior Monk":[],
                        "Layman":[]
                        }
            
        for listcat in self.spelllists.keys():
            lcat = listcat.split(' ')
            
            if lcat[0] == "Base" and self.prof in listcat:
                self.spelllists[listcat]["Category"] = "Own Realm Own Base Lists"
            
            elif lcat[0] == "Base"  and self.prof not in listcat:
                
                if lcat[2] in purespellusers.keys():
                    
                    if purespellusers[lcat[2]] == self.realm:
                        self.spelllists[listcat]["Category"] = "Own Realm Other Base Lists"
                    
                    else:
                        self.spelllists[listcat]["Category"] = "Other Realm Base Lists"
                
                elif lcat[2] in hybridspellusers.keys():
                    
                    for item in hybridspellusers[lcat[2]]:
                    
                        if item in self.realm:
                            
                            self.spelllists[listcat]['Category'] = "Own Realm Other Base Lists"
                            break
                        
                        else:
                            self.spelllists[listcat]['Category'] = "Other Realm Base Lists"
                
                elif lcat[2] in semispellusers.keys():    
                    
                    if semispellusers[lcat[2]] == self.realm:
                        self.spelllists[listcat]["Category"] = "Own Realm Other Base Lists"
                    
                    else:    
                        self.spelllists[listcat]["Category"] = "Other Realm Base Lists"
            
            elif lcat[0] != "Base":
                
                if lcat[0] in self.realm and lcat[1] == "Open":
                    self.spelllists[listcat]["Category"] = "Own Realm Open Lists"
                
                elif lcat[0] in self.realm and lcat[1] != "Open":
                    self.spelllists[listcat]["Category"] = "Own Realm Closed Lists"         
                    
                elif lcat[0] not in self.realm and lcat[1] == "Open":
                    self.spelllists[listcat]["Category"] = "Other Realm Open Lists"
                
                elif lcat[0] not in self.realm and lcat[1] != "Open":
                    self.spelllists[listcat]["Category"] = "Other Realm Closed Lists"                        
            
            
            
