#!/bin/env python
# -*- coding: utf-8 -*-
'''
\package rpgtoolbox.rolemaster
\file /home/mongol/git/rpg-tools/src/rpgtoolbox/rolemaster.py
\brief Rolemaster specific toolbox

This package holds RM specific tools like Charakter Skill Progression.

\license GNU v3
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
\date 2017
\copyright 2017 Marcus Schwamberger
'''
#import rpgToolDefinitions.helptools.dice as dice

races = {'de' : ['gewöhnliche Menschen', 'vermischte Menschen', 'Hochmenschen',
                 "Waldelben", "Grauelben", "Hochelben",
                 "Halbelben", "Zwerge (Kuduk)", "Halblinge (Hobbits)"],
         'en' : ['Common Men', 'Mixed Men', 'High Men', 'Wood Elves', 'Gray Elves',
                 'High Elves', 'Half Elves', 'Dwarves', 'Halflings']
         }

stats = ['Ag', 'Co', 'Me', 'Re', 'SD', 'Em', 'In', 'Pr', 'Qu', 'St']

realms = {'en': ('choice', 'Essence', 'Channeling', 'Mentalism',
                 'Channeling;Mentalism', 'Channeling;Essence',
                 'Essence;Mentalism'),
          'de': ('wählbar', 'Essenz', 'Leitmagie', 'Mentalismus',
                 'Leitmagie;Mentalismus', 'Leitmagie;Essenz',
                 'Essenz;Mentalismus'),
          }
labels = {'de' : {'race' : 'Rasse',
                  'prof' : 'Beruf',
                  'name' : 'Name',
                  'realm' : 'Magiebereich',
                  'stats' : 'Attribute',
                  'skin' : 'Hautfarbe',
                  'culture' : 'Volk',
                  'gender' : 'Geschlecht',
                  'player' : 'Spieler',
                  'ep' : 'Erfahrungspunkte',
                  'eye' : 'Augenfarbe',
                  'hair' : 'Haar',
                  'height' : 'Größe',
                  'weight' : 'Gewicht',
                  'look' : 'Aussehen',
                  'ap age' : 'scheinbares Alter',
                  'age' : 'tatsächliches Alter',
                  'parents' : 'Eltern',
                  'partner' : 'Partner',
                  'siblings' : 'Geschwister',
                  'kids' : 'Kinder',
                  'home' : 'Heimatort',
                  'god' : 'Gottheit',
                  'souvereign' : 'Herrscher',
                  'Ag' : 'Gewandtheit',
                  'Co' : 'Konstitution',
                  'Me' : 'Gedächnis',
                  'Re' : 'Denkvermögen',
                  'SD' : 'Selbstdisziplin',
                  'Em' : 'Empathie',
                  'In' : 'Intuition',
                  'Pr' : 'Austrahlung',
                  'Qu' : 'Schnelligkeit',
                  'St' : 'Stärke',
                  'RRM' : 'Widerstandswurfmodifikatoren',
                  'RRChan' : 'WW Leitmagie',
                  'RREss' : 'WW Essenzmagie',
                  'RRMent' : 'WW Mentalismus',
                  'RRArc' : 'WW Arkane Magie',
                  'RRC/E' : 'WW Leit/Essenz',
                  'RRC/M' : 'WW Leit/Ment',
                  'RRE/M' : 'WW Essenz/Ment',
                  'RRDisease' :'WW Krankheiten',
                  'RRPoison' : "WW Gift",
                  'RRFear' : 'WW Furcht',
                  'AT' : 'Rüstungsklasse',
                  'MAP' : 'Fernkampfabzug',
                  'MMP' : 'Bewegungseinschränkung',
                  'DB' : 'Defensivbonus',
                  'shield' : 'Schildbonus',
                  'total' : 'Gesamt',
                  'Adrenal': "besondere Verteidigung",
                  'DP' : 'Entwicklungspunkte',
                  'BGO': 'Hintergrundoptionen',
                  },
          'en' :{'race' : 'Race',
                  'prof' : 'Profession',
                  'name' : 'Name',
                  'realm' : 'Magic Raalm',
                  'stats' : 'Attributes',
                  'skin' : 'Skin Color',
                  'culture' : 'Culture',
                  'gender' : 'Gender',
                  'player' : 'Player',
                  'ep' : 'Experience Points',
                  'eye' : 'Eye Color',
                  'hair' : 'Hair',
                  'height' : 'Height',
                  'weight' : 'Weight',
                  'look' : 'Look',
                  'ap age' : 'apparent Age',
                  'age' : 'current Age',
                  'parents' : 'Parents',
                  'partner' : 'Partner',
                  'siblings' : 'Siblings',
                  'kids' : 'Children',
                  'home' : 'Home Town',
                  'god' : 'Deity',
                  'souvereign' : 'Souvereign',
                  'Ag' : 'Agility',
                  'Co' : 'Constitution',
                  'Me' : 'Memory',
                  'Re' : 'REasoning',
                  'SD' : 'Self Disziplin',
                  'Em' : 'Empathy',
                  'In' : 'Intuition',
                  'Pr' : 'Presence',
                  'Qu' : 'Quickness',
                  'St' : 'Strength',
                  'RRM' : 'Resistance Rolls Modifiers',
                  'RRChan' : 'RR Channeling',
                  'RREss' : 'RR Essence',
                  'RRMent' : 'RR Mentalism',
                  'RRArc' : 'RR Arcane Magic',
                  'RRC/E' : 'RR Chan/Ess',
                  'RRC/M' : 'RR Chan/Ment',
                  'RRE/M' : 'RR Ess/Ment',
                  'RRDisease' :'RR Disease',
                  'RRPoison' : "RR Poison",
                  'RRFear' : 'RR Fear',
                  'AT' : 'Armor Type',
                  'MAP' : 'Missle Attack Penalty',
                  'MMP' : 'Movement Maneuver Penalty',
                  'DB' : 'Defensive Bonus',
                  'shield' : 'Shield Bonus',
                  'total' : 'Total',
                  'Adrenal': "Adrenal Defense",
                  'DP' : 'Development Points',
                  'BGO' : 'Background Options',
                  },
          }
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
                   'PP_ment_halflings' : (0, 2, 1, 1, 1),
                   'skill_only' : (0, 1, 1, 0.5, 0),
                   'null' : (0, 0, 0, 0, 0)
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
                                'RREss' : 0,
                                'RRChan' : 0,
                                'RRMent' : 0,
                                'RRPoison' : 0,
                                'RRDisease' : 0,
                                'BGO' : 6,
                                'Hobby Ranks': 12,
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
                                'RREss' : 0,
                                'RRChan' : 0,
                                'RRMent' : 0,
                                'RRPoison' : 0,
                                'RRDisease' : 0,
                                'BGO' : 5,
                                'Hobby Ranks': 12,
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
                                'RREss' :-5,
                                'RRChan' :-5,
                                'RRMent' :-5,
                                'RRPoison' : 0,
                                'RRDisease' : 0,
                                'BGO' : 4,
                                'Hobby Ranks': 10,
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
                                'RREss' :-5,
                                'RRChan' :-5,
                                'RRMent' :-5,
                                'RRPoison' : 10,
                                'RRDisease' : 100,
                                'BGO' : 4,
                                'Hobby Ranks': 10,
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
                                'RREss' :-5,
                                'RRChan' :-5,
                                'RRMent' :-5,
                                'RRPoison' : 10,
                                'RRDisease' : 100,
                                'BGO' : 3,
                                'Hobby Ranks': 8,
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
                                'RREss' :-5,
                                'RRChan' :-5,
                                'RRMent' :-5,
                                'RRPoison' : 10,
                                'RRDisease' : 100,
                                'BGO' : 2,
                                'Hobby Ranks': 6,
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
                                'RREss' :-5,
                                'RRChan' :-5,
                                'RRMent' :-5,
                                'RRPoison' : 0,
                                'RRDisease' : 50,
                                'BGO' : 4,
                                'Hobby Ranks': 10,
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
                                'RREss' : 40,
                                'RRChan' : 0,
                                'RRMent' : 40,
                                'RRPoison' : 20,
                                'RRDisease' : 15,
                                'BGO' : 5,
                                'Hobby Ranks': 12,
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
                                'RREss' : 50,
                                'RRChan' : 0,
                                'RRMent' : 40,
                                'RRPoison' : 30,
                                'RRDisease' : 15,
                                'BGO' : 5,
                                'Hobby Ranks': 12,
                                },
                 }

def DPCostSpells(skill = 0, listtype = "Own Realm Own Base List", sutype = "pure", no = 1):
    '''
    Returns Developing Points Costs of Spell Lists. This is just needed if payed with variable DP costs for spell lists.
    \param skill skill rank in that Spell List
    \param listtype List type of the Spell List
    \param sutype Spell User Type (pure, hybrid, semi, non).
    \param no number of Spell Lists developed this level
    \todo this function has to be implemented fully but it is not urgent.
    '''
    costs = "N/A"
    factor = 1
    
    if 5 < no < 11:
        factor *= 2
    
    elif no > 10:
        factor *= 4
        
    if listtype == "Own Realm Own Base List":
    
        if sutype == "pure":
            costs = [3, 3, 3]
        
        elif sutype == "hybrid":
            costs = [3, 3, 3]
        
        elif sutype == "semi":
            costs = [6, 6, 6]
    
    elif listtype == "Own Realm Open List":
    
        if sutype == "pure":
        
            if skill < 21:
                costs = [4, 4, 4]
            
            else:
                costs = [6, 6, 6]
        
        elif sutype == "hybrid":
        
            if skill < 11:   
                costs = [4, 4, 4]
            
            elif 10 < skill < 16:
                costs = [6, 6, 6]
            
            elif 16 < skill < 21:
                costs = [8, 8]
            
            else:
                costs = (12)
        
        elif sutype == "semi":
        
            if skill < 11:
                costs = [8, 8]
            elif 10 < skill < 16:
                costs = [12]
            elif 15 < skill < 21:
                costs = [18] 
            else:
                costs = [25]
                    
    return costs
    
def choseProfession(lang = 'en'):
    '''
    This function reads the ProfBonus.csv and delivers a structured dictionary 
    for further computation.
    \param lang chosen language - at the moment there is just English supported
    \retval professions  a dictionary: 
    \li 1 lvl <professions> 
    \li 2.lvl: Prime Stats (list), Profession Bonusses (dict, 3. lvl), 
          Realm (string)
    \li 3. (Profession Bonusses) \<Skill Category\> : int
    \todo implement German language support 
    \bug doesn't work correctly. It has to be checked separately!!
    '''
    
    # Just until German Language Support is implemented 
    if lang != "en":
        lang = "en"
        
    filename = "./data/default/ProfBonus_%s.csv" % (lang)
    fp = open(filename, "r")
    content = fp.readlines()
    fp.close()
    professions = {}
    key = content[0].strip('\n').split(',')
    
    for i in range(1, len(content)):
        dummy = content[i].strip('\n').split(',')
        professions[dummy[0]] = {}
        
        for j in range(1, len(key)):
            
            if ';' in dummy[j]:
                professions[dummy[0]][key[j]] = dummy[j].split(';')
            
            else:
                professions[dummy[0]][key[j]] = dummy[j]
    
    for prof in professions.keys():
        dummy = {}
    
        for bonus in professions[prof]['Profession Bonusses']:
            dummy2 = bonus.split(':')
            dummy[dummy2[0]] = int(dummy2[1])
            
        professions[prof]['Profession Bonusses'] = dict(dummy)
        
    return professions
        
    
    
        
def bonus(rank = 0, cat = 0, profession = 0, special = 0, progression = progressionType['standard_cat']):
    '''
    This function returns the cumulative Bonus of a category or skill.
    \param rank rank/level of category/skill
    \param cat category bonus if any
    \param profession profession bonus if any
    \param special special Bonus if any
    \param progression concerned progression type, e.g. Standard for categories
    \return the skill rank bonus
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

