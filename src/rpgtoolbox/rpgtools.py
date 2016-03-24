#!/usr/bin/env python
'''
\file rpgtools.py
\package rpgtoolbox.rpgtools
\brief This module contains different functions like dices.


\date (C) 2015
\author Marcus Schwamberger
\email marcus@lederzeug.de

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
