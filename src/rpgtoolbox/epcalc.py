#!/usr/bin/env python
'''
\package rpgtoolbox
\file epcalc.py
This  module holds helpers for calculating the EPs

\date (C) 2015-2017
\license GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
from rpgtools import getLvl as calcLvl

class experience(object):
    '''
    This class will generate an object to handle a character's gained experience
    '''

    def __init__(self, charname = "Conan", ep = 0):
        '''
        \param charname name of the character
        \param ep experience points of the character.
        
        '''
        self.name = charname
        self.ep = ep
        self.getLvl = calcLvl
        self.lvl = self.getLvl(self.ep)
        self.gainedep = 0
        self.newlvl = self.getLvl(self.ep + self.gainedep)
        
    def spell(self, spelllevel = 1, number = 1):
        '''
        Adds EP gained by spells.
        \param spelllevel level of the casted spell
        \param number number of spells casted 
        '''
        self.gainedep += (100 - (self.lvl - spelllevel) * 10) * number
        
    def gainedCrit(self, crittype = "A", number = 0):
        '''
        Adds EPs by gained Crits
        \param crittype Level of Crit
        \param number number of gained crits of that level.
        '''
        crits = {'T' : 0,
                   'A' : 100,
                   'B' : 200,
                   'C' : 300,
                   'D' : 400,
                   'E' : 500
                   }
        
        self.gainedep += crits[crittype] * number
        
    def hitCrit(self, crittype = "A", monsterlvl = 1, number = 1):
        '''
        Adds EPs by caused Crits
        \param crittype Level of the Crit
        \param monsterlvl level of the hit monster
        \param number number of crits of that level against such a monster
        '''
        crits = {'A' : 5,
                'B' : 10,
                'C' : 15,
                'D' : 20,
                'E' : 25
               }    
        
        if monsterlvl == 0:
            monsterlvl = 0.5
        
        self.gainedep += int(round(monsterlvl * crits[crittype], 0)) * number
    
    def travelled(self, km = 0):
        '''
        Adds EPs for traveled km.
        \param km kilometers traveled
        '''
        self.gainedep += km
        
    
    def maneuver(self, manlvl = "routine", number = 0):
        '''
        Adds EPs by maneuvers.
        \param manlvl difficulty of maneuver
        \param number number of maneuvers of this level
        '''
        
        maneuvers = {'routine' : {'de' : 'Routine',
                                  'en' : 'routine',
                                  'ep' : 0
                                  },
                     'very easy'  : {'de' : 'sehr leicht',
                                     'en' : 'very easy',
                                     'ep' : 5
                                     },
                     'easy'    : {'de' : 'leicht',
                                  'en' : 'easy',
                                  'ep' : 10
                                  },
                     'medium'  : {'de' : 'mittelschwer',
                                  'en' : 'medium',
                                  'ep' : 50 
                                  },
                     'heavy'   : {'de' : 'schwer',
                                  'en' : 'heavy',
                                  'ep' : 100
                                  },
                     'very heavy' : {'de' : 'sehr schwer',
                                     'en' : 'very heavy',
                                     'ep' : 150
                                     },
                     'extreme' : {'de' : 'extrem schwer',
                                  'en' : 'extreme',
                                  'ep' : 200
                                  },
                     'folly'   : {'de' : 'Blanker Leichtsinn',
                                  'en' : 'sheer foolish',
                                  'ep' : 300
                                  },
                     'absurd'  : {'de' : 'absurd',
                                  'en' : 'absurd',
                                  'ep' : 500
                                  }
                     }
        self.gainedep += maneuvers[manlvl]['ep'] * number
        
    def killedNPC(self, monsterlvl = 1, number = 1):
        '''
        Adds EPs by killing a NPC/Monster
        \param monsterlvl level of killed monster
        \param number number of killed monsters of that level
        '''
        if monsterlvl == 0:
            self.gainedep += (50 - (monsterlvl + 1 - self.lvl) * 5) * number
            
        else:
            self.gainedep += (200 + (monsterlvl - self.lvl) * 50) * number

class NPC(object):
    '''
    '''
    def __init__(self, npcfile, beast, lvl):
        pass