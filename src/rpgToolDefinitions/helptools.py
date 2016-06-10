#!/usr/bin/env python
'''
\file helptools.py
\package rpgToolDefinitions
\brief help functions for rpg  


\date (C) 2015
\author Marcus Schwamberger
\email marcus@lederzeug.de

'''
from random import randrange as rrange

def dice(sides = 100, nod = 1, rules = "MERS", low = 4, high = 96):
    '''
    This functions simulates the sides and number of dices thrown at RPG
    \param sides number of sides of the dice(s)
    \param nod number of dices
    \rules MERS/MERP/RM rules activated
    \param low value to roll again and subtract second value
    \param high value to roll again and add second value
    \return result list of result(s) of thrown dices
    '''
    result = []
    umr = []
    
    if sides < 2:
        sides = 2
    
    if nod < 1:
        nod = 1
        
    for d in range(nod):
        throw = rrange(1, sides)
        if rules == "RM " or rules == "MERS":
            if throw <= low:
                throw2 = rrange(1, sides)
                dummy = throw2
                
                while throw2 >= high:
                    throw2 = rrange(1, sides)
                    dummy += throw2
                
                throw -= dummy
            
            elif throw == 66 and rules == "RM":
                umr.append ([d, 66])
                
            elif throw >= high:
                
                if throw == 100 and rules == "RM":
                    umr.append([d, 100])
                
                throw2 = rrange(1, sides)
                dummy = throw2
                
                while throw2 >= high:
                    throw2 = rrange(1, sides)
                    dummy += throw2
                    
                throw += dummy
        
        result.append(throw)
    
    return result, umr
        
        
