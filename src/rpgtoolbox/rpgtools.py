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
import random

def dice(sides = 6, number = 1):
    '''
    This function delivers the result of a dice roll as a list.
    \param sides number of sides of the used dice
    \param number number of used dices/rolls
    \retval result list containing int numbers of the dice rolls
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
