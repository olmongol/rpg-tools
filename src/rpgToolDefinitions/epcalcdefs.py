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
\deprecated This module is replaces by rpgtoolbox.epcalc.py
'''
maneuvers = {'routine' : {'de' : 'Routine',
                          'en' : 'routine',
                          'ep' : 0,
                          'mod': 30
                          },
             'easy'  : {'de' : 'sehr leicht',
                          'en' : 'very easy',
                          'ep' : 5,
                          'mod': 20
                          },
             'light'    : {'de' : 'leicht',
                          'en' : 'easy',
                          'ep' : 10,
                          'mod': 10
                          },
             'medium'  : {'de' : 'mittelschwer',
                          'en' : 'medium',
                          'ep' : 50,
                          'mod': 0 
                          },
             'hard'   : {'de' : 'schwer',
                          'en' : 'heavy',
                          'ep' : 100,
                          'mod':-10
                          },
             'very hard' : {'de' : 'sehr schwer',
                          'en' : 'very heavy',
                          'ep' : 150,
                          'mod':-20
                          },
             'extreme' : {'de' : 'extrem schwer',
                          'en' : 'extreme',
                          'ep' : 200,
                          'mod':-30
                          },
             'folly'   : {'de' : 'Blanker Leichtsinn',
                          'en' : 'sheer foolish',
                          'ep' : 300,
                          'mod':-50
                          },
             'absurd'  : {'de' : 'absurd',
                          'en' : 'absurd',
                          'ep' : 500,
                          'mod':-70
                          }
             
             }
param_char = {'player' : {'de' : 'Spieler',
                          'en' : 'player',
                          },
              'char' : {'de' : 'Charaktername',
                        'en' : 'Character',
                        },
              'exp' : {'de' : 'Erfahrungspunkte',
                       'en' : 'Experience Points',
                       },
              'lvl' : {'de' : 'Stufe',
                       'en' : 'Level'
                       },
              'party' : {'de' : 'Charaktergruppe',
                         'en' : 'Group of Characters'
                         }
              }
##\var epchr
# A dictionary holding the structure for tacking track of things worth EPs
epchr = {'gained hitpoints' : 0,
        'gained criticals' : {'T' : 0,
                              'A' : 0,
                              'B' : 0,
                              'C' : 0,
                              'D' : 0,
                              'E' : 0
                              },
        'criticals' : {'A' : [0, 0],
                       'B' : [0, 0],
                       'C' : [0, 0],
                       'D' : [0, 0],
                       'E' : [0, 0]
                       },
        'killed' : [[0, 0]],
        'spells' : 0,
        'maneuver' : {'routine' : 0,
                      'v_easy'  : 0,
                      'easy'    : 0,
                      'medium'  : 0,
                      'heavy'   : 0,
                      'v_heavy' : 0,
                      'extreme' : 0,
                      'folly'   : 0,
                      'absurd'  : 0
                      } ,
        'traveled km' : 0,
        'individual EP' : 0
        }


def getEPCrit(level = 0, crit = "A", charhit = False):
    '''
    This function returns the EP for a gained or provoked critical hit.
    \param level level of the hit monster/enemy
    \param crit class of critical hit: T, A - E
    \param charhit was the character hit (True) or not (False)
    \retval EPs for the critical hit
    \deprecated see epcalc.py
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
    \deprecated see epcalc.py
    '''
    return (100 - (caster - spell) * 10) 
