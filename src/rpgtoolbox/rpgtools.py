#!/usr/bin/env python
'''!
@package rpgtoolbox.rpgtools
@file rpgtools.py
@brief RPG helpful functions
This module contains some helpful functions for role-playing games like:
- dice() for dic rolling
- getLvl() for calculate actual level of char


@date (C) 2015-2021
@license GNU V3.0
@author Marcus Schwamberger
@email marcus@lederzeug.de
@version 1.0
'''
__updated__ = "28.12.2020"

import random
from rpgtoolbox.globaltools import readCSV
from rpgtoolbox.rolemaster import rankbonus
import re



def dice(sides = 6, number = 1):
    '''!
    This function delivers the result of (number of) dice roll(s) as a list.
    @param sides number of sides of the used dice
    @param number number of used dices/rolls
    @retval result list containing integer numbers of the dice rolls
    '''
    i = 0
    result = []

    while i < number:
        roll = random.randint(1, sides)
        result.append(roll)
        i += 1
    return result



def getLvl(ep = 10000):
    '''!
    This function calculates the level of a MERP/RM character.
    @param ep experience point of the character
    \return level of character as integer ValueError
    '''
    if ep <= 50000:
        lvl = int(ep / 10000)
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
    '''!
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
                if skill == "Body Development":
                    charval['cat'][cat]['Skill'][skill]['total bonus'] += 10

    return charval



def RRroll(attacklvl, targetlvl, roll):
    '''!
    This function checks out whether a RR roll has worked out.

    @param attacklvl level of the attack or attacker
    @param targetlvl level of the target
    @param roll final result of a resistance roll (all modifiers and bonusses ect)

    @retval resisted  RR was successful True/False
    @retval value the value of the RR roll table
    '''
    resisted = False
    value = 0
    if attacklvl < 6:
        value = 50 + (attacklvl - 1) * 5

    elif 5 < attacklvl < 11:
        value = 70 + (attacklvl - 5) * 3

    elif 10 < attacklvl < 15:
        value = 85 + (attacklvl - 10) * 2

    elif attacklvl >= 15:
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
    '''!
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



class equipmentPenalities(object):
    """
    This class calculates MMP and armor penalties.
    ----
    @bug sometimes armor penalties are not correctly calculated
    """


    def __init__(self, character = {}):
        """
        Constructor equipmentPenalties
        @param character JSON structure with all character data
        """
        self.character = character
        if "inventory" not in character.keys():
            exit()

        self.weightpenalty = 0

        self.AT = 1

        self.calcWeightPen()
        self.getAT()
        self.calcArmorPen()


    def calcWeightPen(self):
        """
        This calculates the weight penalty
        """
        rex = r"^([0-9]{1,6}[\.]{0,1}[0-9]{0,2})( +|)(lbs.|lbs|kg|)$"
        checker = re.compile(rex)
        chk = checker.match(self.character["background"]["weight"])
        if chk:
            if chk.group(3) in ["", "kg"]:
                BWA = round(float(chk.group(1)) * 2.2 / 10.0, 2)
            else:
                BWA = round(float(chk.group(1)) / 10.0, 2)
        limitfactor = 1
        while self.character["carried"] > BWA * limitfactor:
            self.weightpenalty -= 8
            limitfactor += 1


    def getAT(self):
        """
        This gets the armor type of equipped armor.
        """
        greaves = 0
        for armor in self.character["inventory"]["armor"]:
            if armor["location"] == "equipped":

                if type(armor["AT"]) == type(2):
                    if armor["AT"] > self.AT:
                        self.AT = armor["AT"]

                if "greaves" in armor["name"].lower():
                    greaves += 0.5
        if greaves > 1:
            greaves = 1

        self.AT += int(greaves)


    def calcArmorPen(self):
        """
        This calculates all armor penalties.
        """
        ## @var self.minmanmod
        # minimum maneuver modification
        self.minmanmod = 0
        ## @var self.maxmanmod
        # maximum maneuver modification
        self.maxmanmod = 0
        ## @var self.msatpen
        # missile attack penalty
        self.misatpen = 0
        ## @var self.armqupen
        # armor quickness penalty
        self.armqupen = 0

        if self.AT == 6:
            self.maxmanmod = -20 + self.character["cat"]["Armor - Light"]["Skill"]["Soft Leather"]["total bonus"]
            self.misatpen = -5
        elif self.AT == 7:
            self.minmanmod = -10
            self.maxmanmod = -40 + self.character["cat"]["Armor - Light"]["Skill"]["Soft Leather"]["total bonus"]
            self.misatpen = -15
            self.armqupen = -10
        elif self.AT == 8:
            self.minmanmod = -15
            self.maxmanmod = -50 + self.character["cat"]["Armor - Light"]["Skill"]["Soft Leather"]["total bonus"]
            self.misatpen = -15
            self.armqupen = -15
        elif self.AT == 9:
            self.minmanmod = -5
            self.maxmanmod = -50 + self.character["cat"]["Armor - Light"]["Skill"]["Rigid Leather"]["total bonus"]
        elif self.AT == 10:
            self.minmanmod = -10
            self.maxmanmod = -70 + self.character["cat"]["Armor - Light"]["Skill"]["Rigid Leather"]["total bonus"]
            self.misatpen = -10
            self.armqupen = -5
        elif self.AT == 11:
            self.minmanmod = -15
            self.maxmanmod = -90 + self.character["cat"]["Armor - Light"]["Skill"]["Rigid Leather"]["total bonus"]
            self.misatpen = -20
            self.armqupen = -15
        elif self.AT == 12:
            self.minmanmod = -15
            self.maxmanmod = -110 + self.character["cat"]["Armor - Light"]["Skill"]["Rigid Leather"]["total bonus"]
            self.misatpen = -30
            self.armqupen = -15
        elif self.AT == 13:
            self.minmanmod = -10
            self.maxmanmod = -70 + self.character["cat"]["Armor - Medium"]["Skill"]["Chain"]["total bonus"]
            self.armqupen = -5
        elif self.AT == 14:
            self.minmanmod = -15
            self.maxmanmod = -90 + self.character["cat"]["Armor - Medium"]["Skill"]["Chain"]["total bonus"]
            self.misatpen = -10
            self.armqupen = -10
        elif self.AT == 15:
            self.minmanmod = -25
            self.maxmanmod = -120 + self.character["cat"]["Armor - Medium"]["Skill"]["Chain"]["total bonus"]
            self.misatpen = -20
            self.armqupen = -20
        elif self.AT == 16:
            self.minmanmod = -25
            self.maxmanmod = -130 + self.character["cat"]["Armor - Medium"]["Skill"]["Chain"]["total bonus"]
            self.misatpen = -20
            self.armqupen = -20
        elif self.AT == 17:
            self.minmanmod = -15
            self.maxmanmod = -90 + self.character["cat"]["Armor - Heavy"]["Skill"]["Plate"]["total bonus"]
            self.armqupen = -10
        elif self.AT == 18:
            self.minmanmod = -20
            self.maxmanmod = -110 + self.character["cat"]["Armor - Heavy"]["Skill"]["Plate"]["total bonus"]
            self.misatpen = -10
            self.armqupen = -20
        elif self.AT == 19:
            self.minmanmod = -35
            self.maxmanmod = -150 + self.character["cat"]["Armor - Heavy"]["Skill"]["Plate"]["total bonus"]
            self.misatpen = -30
            self.armqupen = -30
        elif self.AT == 20:
            self.minmanmod = -45
            self.maxmanmod = -165 + self.character["cat"]["Armor - Heavy"]["Skill"]["Plate"]["total bonus"]
            self.misatpen = -40
            self.armqupen = -40

        if self.maxmanmod > self.minmanmod:
            self.maxmanmod = self.minmanmod



class statManeuver(object):
    '''
    This class handles static maneuver roll results. An object of it operates as single static maneuver table where a
    given roll (already modified by severity and other modifiers) is checked and the result returned.

    '''


    def __init__(self, tablefile = "./data/default/tables/general_smt.csv"):
        '''!
        Constructor statManeuver
        @param tablefile CSV containing the table which shall be used for static maneuver rolls.
        '''
        self.table = readCSV(tablefile)


    def checkRoll(self, roll):
        '''!
        Checks the rolled number + bonusses for success.
        @param roll the modified roll result (number)
        @retval result table row as dictionary.
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

