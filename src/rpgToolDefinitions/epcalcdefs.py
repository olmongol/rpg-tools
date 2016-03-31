#!/usr/bin/env python
'''
\file epcalcdefs.py
\package rpgToolDefinitions.epcalcdefs

\brief Definitions for EP-Calculator
This module contains predefined variables, lists, etc. for the EP calculator. 

\date (C) 2015-2016
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 0.1

'''
maneuvres = {'routine' : {'de' : 'Routine',
                          'en' : 'routine',
                          'ep' : 0
                          },
             'v_easy'  : {'de' : 'sehr leicht',
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
             'v_heavy' : {'de' : 'sehr schwer',
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

def getEPCrit(level = 0, crit = "T", charhit = False):
    '''
    This function returns the EP for a gained or provoked critical hit.
    \param level level of the hit monster/enemy
    \param crit class of critical hit: T, A - E
    \param charhit was the character hit (True) or not (False)
    \retval EPs for the critical hit
    '''
    selfhitcrits = {'T' : 0,
                   'A' : 100,
                   'B' : 200,
                   'C' : 300,
                   'D' : 400,
                   'E' : 500
                   }
    if charhit:
        return selfhitcrits[crit]

    hitcrits = {'A' : 5,
                'B' : 10,
                'C' : 15,
                'D' : 20,
                'E' : 25
               }    
    if level == 0:
        level = 0.5
    
    return int(round(level * hitcrits[crit], 0))

def calcEPSpell(spell = 1, caster = 1):
    '''
    This function returns the EP for a cast spell.
    \label spell level of the spell cast
    \label caster level of the caster
    \label retval EP for the spell
    '''
    return (100 - (caster - spell) * 10) 
