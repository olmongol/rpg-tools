#!/bin/env python
'''
\package rpgtoolbox.rolemaster
\file /home/mongol/git/rpg-tools/src/rpgtoolbox/rolemaster.py
\brief Rolemaster specific toolbox

This package holds RM specific tools like Charakter Skill Progression.

\license GNU v3
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
\date 2016
\copyright 2016 Marcus Schwamberger
'''
import rpgToolDefinitions.helptools.dice as dice

##
# This holds the different Cat/Skill/BD/PP development
progressionType = {'standard_cat'   : (-15, 2, 1, 0.5, 0),
                   'standard_skill' : (-15, 3, 2, 1, 0.5),
                   'combined'       : (-30, 5, 3, 2, 0.5),
                   'BD_com_men'     : (0, 6, 4, 2, 1),
                   'BD_mix_men'     : (0, 6, 5, 2, 1),
                   'BD_high_men'    : (0, 7, 5, 3, 1),
                   'BD_wood_elves'  : (0, 6, 3, 1, 1),
                   'BD_grey_elves'  : (0, 6, 3, 2, 1),
                   'BD_high_elves'  : (0, 7, 3, 2, 1),
                   'BD_half_elves'  : (0, 7, 5, 3, 1),
                   'BD_dwarves'     : (0, 7, 4, 2, 1),
                   'BD_halflings'   : (0, 6, 2, 2, 1),
                   'PP_channeling'  : (0, 6, 5, 4, 3),
                   'PP_ess_men'     : (0, 6, 5, 4, 3),
                   'PP_ess_elves'   : (0, 7, 6, 5, 4),
                   'PP_ess_halfelves' : (0, 6, 6, 4, 3),
                   'PP_ess_dwarves' : (0, 3, 2, 1, 1),
                   'PP_ess_halflings' : (0, 2, 1, 1, 1),
                   'PP_ment_men'    : (0, 7, 6, 5, 4),
                   'PP_ment_elves'  : (0, 6, 5, 4, 3),
                   'PP_ment_halfelves' : (0, 7, 5, 4, 3),
                   'PP_ment_dwarves' : (0, 3, 2, 1, 1),
                   'PP_ment_halflings' : (0, 2, 1, 1, 1)
                   } 

##
# Race bonusses for stats, RR and BGO
raceAbilities = {'Common Men': {'Ag' : 0,
                                'Co' : 0,
                                'Me' : 0,
                                'Re' : 0,
                                'SD' : 2,
                                'Em' : 0,
                                'In' : 0,
                                'Pr' : 0,
                                'Qu' : 0,
                                'St' : 2,
                                'Ess' : 0,
                                'Chan' : 0,
                                'Ment' : 0,
                                'Pois' : 0,
                                'Dis' : 0,
                                'BGO' : 6
                                },
                 'Mixed Men' : {'Ag' : 0,
                                'Co' : 2,
                                'Me' : 0,
                                'Re' : 0,
                                'SD' : 2,
                                'Em' : 0,
                                'In' : 0,
                                'Pr' : 2,
                                'Qu' : 0,
                                'St' : 2,
                                'Ess' : 0,
                                'Chan' : 0,
                                'Ment' : 0,
                                'Pois' : 0,
                                'Dis' : 0,
                                'BGO' : 5
                                },
                 'High Men' :  {'Ag' :-2,
                                'Co' : 4,
                                'Me' : 0,
                                'Re' : 0,
                                'SD' : 0,
                                'Em' : 0,
                                'In' : 0,
                                'Pr' : 4,
                                'Qu' :-2,
                                'St' : 4,
                                'Ess' :-5,
                                'Chan' :-5,
                                'Ment' :-5,
                                'Pois' : 0,
                                'Dis' : 0,
                                'BGO' : 4
                                },
                 'Wood Elves': {'Ag' : 4,
                                'Co' : 0,
                                'Me' : 2,
                                'Re' : 0,
                                'SD' :-5,
                                'Em' : 2,
                                'In' : 0,
                                'Pr' : 2,
                                'Qu' : 2,
                                'St' : 0,
                                'Ess' :-5,
                                'Chan' :-5,
                                'Ment' :-5,
                                'Pois' : 10,
                                'Dis' : 100,
                                'BGO' : 4
                                },
                 'Grey Elves' : {'Ag' : 2,
                                'Co' : 0,
                                'Me' : 2,
                                'Re' : 0,
                                'SD' :-5,
                                'Em' : 2,
                                'In' : 0,
                                'Pr' : 4,
                                'Qu' : 4,
                                'St' : 0,
                                'Ess' :-5,
                                'Chan' :-5,
                                'Ment' :-5,
                                'Pois' : 10,
                                'Dis' : 100,
                                'BGO' : 3
                                },
                 'High Elves' : {'Ag' : 2,
                                'Co' : 0,
                                'Me' : 2,
                                'Re' : 0,
                                'SD' :-5,
                                'Em' : 2,
                                'In' : 0,
                                'Pr' : 6,
                                'Qu' : 6,
                                'St' : 0,
                                'Ess' :-5,
                                'Chan' :-5,
                                'Ment' :-5,
                                'Pois' : 10,
                                'Dis' : 100,
                                'BGO' : 2
                                },
                 'Half Elves' : {'Ag' : 2,
                                'Co' : 2,
                                'Me' : 0,
                                'Re' : 0,
                                'SD' :-3,
                                'Em' : 0,
                                'In' : 0,
                                'Pr' : 4,
                                'Qu' : 4,
                                'St' : 2,
                                'Ess' :-5,
                                'Chan' :-5,
                                'Ment' :-5,
                                'Pois' : 0,
                                'Dis' : 50,
                                'BGO' : 4
                                },
                 'Dwarves' : {'Ag' :-2,
                                'Co' : 6,
                                'Me' : 0,
                                'Re' : 0,
                                'SD' : 2,
                                'Em' :-4,
                                'In' : 0,
                                'Pr' :-4,
                                'Qu' :-2,
                                'St' : 2,
                                'Ess' : 40,
                                'Chan' : 0,
                                'Ment' : 40,
                                'Pois' : 20,
                                'Dis' : 15,
                                'BGO' : 5
                                },
                 'Haflings' : {'Ag' : 6,
                                'Co' : 6,
                                'Me' : 0,
                                'Re' : 0,
                                'SD' :-4,
                                'Em' :-2,
                                'In' : 0,
                                'Pr' :-6,
                                'Qu' : 4,
                                'St' :-8,
                                'Ess' : 50,
                                'Chan' : 0,
                                'Ment' : 40,
                                'Pois' : 30,
                                'Dis' : 15,
                                'BGO' : 5
                                },
                 }

def bonus(rank = 0, cat = 0, profession = 0, special = 0, progression = progressionType['standard_cat']):
    '''
    This function returns the cumulative Bonus of a category or skill.
    \param rank rank/level of category/skill
    \param cat category bonus if any
    \param profession profession bonus if any
    \param special special Bonus if any
    \param progression concerned progression type, e.g. Standard for categories
    '''
    
    result = cat + profession + special
    if rank == 0:
        result += progression[0]
        
    elif 0 < rank <= 10:
        result += progression[1] * rank
   
    elif 10 < rank <= 20:
        result += progression[1] * 10 + progression[2] * (rank - 10)
    
    elif 20 < rank <= 30:
        result += (progression[1] + progression[2]) * 10 + progression[3] + (rank - 20)
    
    elif 30 < rank:
        result += (progression[1] + progression[2] + progression[3]) * 10 + progression[4] * (rank - 30)

    return result    

def pointsneeded(statvalue = 20):
    '''
    This gives back the amount of ṕoints to assing for stats
    \param statvalue wanted stat value
    \return points needed to assign give stat value 
    '''
    if statvalue < 20:
        print "stats cannot be less then 20"
        result = 20
        
    elif 20 <= statvalue <= 90:
        result = statvalue
    
    else:
        result = 90 + (statvalue - 90) ** 2
        
    return result

def statbonus(statvalue = 20):
    '''
    Returns calculated bonus of stat value
    \param statvalue stat value for which the bonus should be calculated
    \return stat value's bonus
    '''
    statvalue = float(statvalue)
    
    if 0 < statvalue <= 10:
        result = int(round((statvalue - 21) / 2))
    elif 10 < statvalue < 31:
        result = int(round((statvalue - 33) / 5))
    elif 30 < statvalue < 70:
        result = 0
    elif 69 < statvalue < 90:
        result = int(round((statvalue - 67) / 5))
    elif 89 < statvalue < 101:
        result = int(round((statvalue - 81) / 2))
    else:
        result = int(round((statvalue - 95) * 2))
            
    return result
#if __name__ == '__main__':
#    pass
