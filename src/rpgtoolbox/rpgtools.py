#!/usr/bin/env python
'''
\package rpgtoolbox
\file rpgtools.py
\package rpgtoolbox.rpgtools
\brief RPG helpful functions
This module contains some helpful functions for role-playing games like:
\li dice


\date (C) 2015-2016
\license GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__updated__ = "27.05.2018"

import random
from rpgtoolbox.globaltools import readCSV
from rpgtoolbox.rolemaster import rankbonus

def dice(sides = 6, number = 1):
    '''
    This function delivers the result of (number of) dice roll(s) as a list.
    \param sides number of sides of the used dice
    \param number number of used dices/rolls
    \retval result list containing integer numbers of the dice rolls
    '''
    i = 0
    result = []
    
    while i < number:
        roll = random.randint(1, sides)
        result.append(roll)
        i += 1
    return result

def getLvl(ep = 10000):
    '''
    This function calculates the level of a MERP/RM character.
    \param ep experience point of the character
    \return level of character as integer ValueError
    '''
    if ep <= 50000:
        lvl = ep / 10000
    elif ep > 50000 and ep <= 150000:
        lvl = (ep - 50000) / 20000 + 5  
    elif ep > 150000 and ep <= 300000:
        lvl = (ep - 150000) / 30000 + 10
    elif ep > 300000 and ep <= 500000:
        lvl = (ep - 300000) / 40000 + 15
    else:
        lvl = (ep - 500000) / 50000 + 20
    return lvl


def calcTotals(charval = {}):
    '''
     This function calculates total bonusses for all categories and skills of a
     character.
     It saves rank bonusses and totals in the character's data dictionary
     \param charval the character's (whole) data in JSON format
     \retval result updated character's data concerning the total bonusses.
    '''


    for cat in charval['cat']:
        progression = charval['cat'][cat]['Progression']
        rank = charval['cat'][cat]['rank']
        catrankbonus = rankbonus(rank = rank, progression = progression)
        charval['cat'][cat]['rank bonus'] = catrankbonus
        statbonus = 0
        itembonus = charval['cat'][cat]['item bonus']

        if 'prof bonus' in charval['cat'][cat]:
            profbonus = charval['cat'][cat]['prof bonus']

        else:
            profbonus = 0
        specbonus = charval['cat'][cat]['spec bonus']

        if charval['cat'][cat]['Stats'] == [""] or charval['cat'][cat]['Stats'] == u'':
            pass

        elif type(charval['cat'][cat]['Stats']) != type([]):
            statbonus += charval[charval['cat'][cat]['Stats']]['total']

        else:

            for s in charval['cat'][cat]['Stats']:

                if s != "SD":
                    statbonus += charval[s.strip(" ").capitalize()]['total']

                else:
                    statbonus += charval[s]['total']
            
        charval['cat'][cat]['stat bonus'] = statbonus
        charval['cat'][cat]['total bonus'] = rankbonus(rank = rank,
                                                       profession = profbonus,
                                                       special = specbonus,
                                                       progression = progression
                                                       ) + statbonus + itembonus

        for skill in charval['cat'][cat]['Skill']:
            
            if (skill != "Progression" and "Spell" not in cat) or ("Spell" in cat and skill not in ['Stats', 'Progression']):
                progression = charval['cat'][cat]['Skill'][skill]['Progression']

                if type(progression) == type(2):
                    progression = [progression]
            
                rank = charval['cat'][cat]['Skill'][skill]['rank']
                bonus = rankbonus(rank = rank, progression = progression)
                charval['cat'][cat]['Skill'][skill]['rank bonus'] = bonus
                total = bonus + charval['cat'][cat]['total bonus'] + charval['cat'][cat]['Skill'][skill]['item bonus'] + charval['cat'][cat]['Skill'][skill]['spec bonus']
                charval['cat'][cat]['Skill'][skill]['total bonus'] = total
                
    return charval


class statManeuver(object):
    '''
    This class handles static maneuver roll results.
    '''
    
    def __init__(self, tablefile = "./data/default/tables/general_smt.csv"):
        self.table = readCSV(tablefile)
        
    def checkRoll(self, roll):
        '''
        Checks the rolled number + bonusses for success.
        \param roll the modified roll result (number)
        \retval result table row as dictionary.
        '''
        result = {}

        for row in range(0, len(self.table)):
            lower, upper = self.table[row]['roll'].split(" < ")
            
            if lower == "UM" and roll == int(upper):
                result = dict(self.table[row])
                break

            elif lower == "" and roll <= int(upper):
                result = dict(self.table[row])
            
            elif upper == "" and int(lower) <= roll: 
                result = dict(self.table[row])
                
            elif lower != "UM" and lower != "" and upper != "":
                
                if int(lower) <= roll <= int(upper):
                    result = dict(self.table[row])
            
        if "roll" in result.keys():
            del(result['roll'])
                        
        return result
                 
        
