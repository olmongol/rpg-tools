#!/usr/bin/env python
'''
\package rpgtoolbox.rpgtools
\file rpgtools.py
\brief RPG helpful functions
This module contains some helpful functions for role-playing games like:
- dice() for dic rolling
- getLvl() for calculate actual level of char


\date (C) 2015-2020
\license GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
__updated__ = "22.02.2020"

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
        lvl = round((ep - 50000) / 20000) + 5
    elif ep > 150000 and ep <= 300000:
        lvl = round((ep - 150000) / 30000) + 10
    elif ep > 300000 and ep <= 500000:
        lvl = round((ep - 300000) / 40000) + 15
    else:
        lvl = round((ep - 500000) / 50000) + 20
    return round(lvl)



def calcTotals(charval = {}):
    '''
     This function calculates total bonusses for all categories and skills of a
     character.
     It saves rank bonusses and totals in the character's data dictionary
     @param charval the character's (whole) data in JSON format
     @retval result updated character's data concerning the total bonusses.
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

        if charval['cat'][cat]['Stats'] == [""] or charval['cat'][cat]['Stats'] == '':
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
            #DEBUG
            print("calc total: {} - {}".format(cat, skill))
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



def RRroll(attacklvl, targetlvl, roll):
    '''
    This function checks out whether a RR roll has worked out.

    @param attacklvl level of the attack or attacker
    @param targetlvl level of the target
    @param roll final result of a resistance roll (all modifiers and bonusses ect)

    @retval resisted  RR was successful True/False
    @retval value the value of the RR roll table
    '''
    resisted = False

    if attacklvl < 6:
        value = 50 + (attacklvl - 1) * 5

    elif 5 < attacklvl < 11:
        value = 70 + (attacklvl - 5) * 3

    elif 10 < attacklvl < 15:
        value = 85 + (attacklvl - 10) * 2

    elif attacklvl > 15:
        value = 90 + (attacklvl - 15)

    if targetlvl < 6:
        value -= (targetlvl - 1) * 5

    elif 5 < targetlvl < 11:
        value -= (20 + (targetlvl - 5) * 3)

    elif 10 < targetlvl < 16:
        value -= (32 + (targetlvl - 10) * 2)

    elif targetlvl > 15:
        value -= (39 + (targetlvl - 15))

    if value <= roll:
        resisted = True

    return resisted, value



def statGain(dicelow = 1, dicehigh = 1, temp = 50, pot = 75):
    '''
    This function calculates the stat gain roll: a temporary steat could raise ore fall.
    @param dicelow result of the lower result of the  d10 roll
    @param dicehight result of the higher result of the d10 roll
    @param temp temp value of stat
    @param pot pot value of stat
    @retval result new temp value of stat
    '''
    result = temp
    statdif = pot - temp

    if dicelow >= dicehigh:
        dummy = int(dicehigh)
        dicehigh = int(dicelow)
        dicelow = int(dummy)

    if statdif <= 10:

        if dicelow < 6:
            result -= dicelow

        else:
            result += 2 * dicelow

    elif 10 < statdif <= 20:

        if dicehigh < 6:
            result -= dicehigh

        else:
            result += 2 * dicehigh

    else:

        if (dicehigh + dicelow) < 6:
            result -= dicehigh + dicelow

        else:
            result += dicehigh + dicelow

    if result > pot:
        result = pot
    return result



class statManeuver(object):
    '''
    This class handles static maneuver roll results. An object of it operates as single static maneuver table where a
    given roll (allready modified by severity and other modifiers) is checked and the result returned.

    '''


    def __init__(self, tablefile = "./data/default/tables/general_smt.csv"):
        '''
        Constructor which needs the table to use.
        @param tablefile CSV containing the table which shall be used for static maneuver rolls.
        '''
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

        if "roll" in list(result.keys()):
            del(result['roll'])

        return result

