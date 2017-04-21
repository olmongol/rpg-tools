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
catnames = {'de' : {'spells' : "Spells",
                    'weapon' : 'Weapon',
                    },
            'en' : {'spells' : "Spells",
                    'weapon' : 'Weapon',
                    },
            }
##\var spellisttypes
# dictionary of spell list type lists
spellisttypes = {'de': ['Offene Leitmagie', 'Geschlossene Leitmagie',
                        'Animist Basis', 'Kleriker Basis', 'Paladin Basis',
                        'Waldläufer Basis', 'Heiler Basis', 'Böse Leitmagie',
                        'Offene Essenz', 'Geschlossene Essenz',
                        'Illusionist Basis', 'Magier Basis', 'Dilletant Basis',
                        'Mönch Basis', 'Hexer Basis', 'Böse Essenz',
                        'Offene Mentalismus', 'Geschlossene Mentalismus',
                        'Laienheiler Basis', 'Barden Basis', 'Mentalist Basis',
                        'Magent Basis', 'Mystiker Basis', 'Böse Mentalistmus'
                        ],
                 'en': ['Open Channeling', 'Closed Channeling',
                        'Animist Base', 'Cleric Base', 'Paladin Base',
                        'Ranger Basis', 'Healer Basis', 'Evil Channeling',
                        'Open Essence', 'Closed Essence',
                        'Illusionist Base', 'Magican Base', 'Dabbler Base',
                        'Monk Base', 'Sorcerer Base', 'Evil Essence',
                        'Open Mentalism', 'Closed Mentalism',
                        'Lay Healer', 'Bard Base', 'Mentalist Base',
                        'Magent Base', 'Mystic Base', 'Evil Mentalism'
                        ],
                 }
##\var races
# just a dictionary for translation of the races' names
races = {'de' : ['normale Menschen', 'vermischte Menschen', 'Hochmenschen',
                 "Waldelben", "Grauelben", "Hochelben",
                 "Halbelben", "Zwerge", "Halblinge"],
         'en' : ['Common Men', 'Mixed Men', 'High Men', 'Wood Elves', 'Grey Elves',
                 'High Elves', 'Half Elves', 'Dwarves', 'Halflings']
         }

cultures = {'de' : ['Huegelmenschen', 'Corsaren', 'Nomaden', 'Landvolk', 'Stadtmenschen',
                   'Waldmenschen', 'Hochmenschen', 'Waldelben', 'Grauelben', 'Hochelben',
                   'Halbelben', 'Zwerge', 'Halblinge'],
           'en' : ['Hillmen', 'Mariners', 'Nomads', 'Ruralmen', 'Urbanmen', 'Woodmen',
                   'High Men', 'Wood Elves', 'Grey Elves', 'High Elves', 'Half Elves',
                   'Dwarves', 'Halflings'] 
           
           }
##\var stats
# the English shortcuts/indices for stats
stats = ['Ag', 'Co', 'Me', 'Re', 'SD', 'Em', 'In', 'Pr', 'Qu', 'St']

realmstats = {'de' : {'Essence' : 'Em',
                      'Channeling' : 'In',
                      'Mentalism' : 'Pr'
                      },
              'en' : {'Essence' : 'Em',
                      'Channeling' : 'In',
                      'Mentalism' : 'Pr'
                      },
              }

exceptions = ['Costs', 'Stats', 'Progression', 'rank', 'rank bonus', 'spec bonus', \
              'item bonus']
##\var realms
# a dictionary for translating the names of magic realms
realms = {'en': ('choice', 'Essence', 'Channeling', 'Mentalism',
                 ['Channeling', 'Mentalism'], ['Channeling', 'Essence'],
                 ['Essence', 'Mentalism']),
          'de': ('wählbar', 'Essenz', 'Leitmagie', 'Mentalismus',
                 ['Leitmagie', 'Mentalismus'], ['Leitmagie', 'Essenz'],
                 ['Essenz', 'Mentalismus']),
          }
##\var ppds
# a lists that helps to set the right PPD progression
ppds = ("", "PPD Ess ", "PPD Chan ", "PPD Ment ",
        ["PPD Chan ", "PPD Ment "], ["PPD Chan ", "PPD Ess "], ["PPD Ess ", "PPD Ment "])

##\var speccat
# a dirtionary of lists of special categories: BD, PPD
speccat = {'en': ['Body Development', 'Power Point Development'],
           'de': ['Body Development', 'Power Point Development'],
           }
###\var sltype
## dictionary of lists of spell list types
##\todo translate German part
#sltype = {'en': ['Open Channeling',
#                  'Closed Channeling',
#                  'Evil Channeling',
#                  'Open Essence',
#                  'Closed Essence',
#                  'Evil Essence',
#                  'Open Mentalism',
#                  'Closed Mentalism',
#                  'Evil Mentalism',
#                  'Magician Base',
#                  'Illusionist Base',
#                  'Cleric Base',
#                  'Animist Base',
#                  'Mentalist Base',
#                  'Lay Healer Base',
#                  'Healer Base',
#                  'Mystic Base',
#                  'Sorcerer Base',
#                  'Ranger Base',
#                  'Monk Base',
#                  'Dabbler Base',
#                  'Bard Base',
#                  'Magend Base',
#                  'Arcane'],
#           'de': ['Open Channeling',
#                  'Closed Channeling',
#                  'Evil Channeling',
#                  'Open Essence',
#                  'Closed Essence',
#                  'Evil Essence',
#                  'Open Mentalism',
#                  'Closed Mentalism',
#                  'Evil Mentalism',
#                  'Magician Base',
#                  'Illusionist Base',
#                  'Cleric Base',
#                  'Animist Base',
#                  'Mentalist Base',
#                  'Lay Healer Base',
#                  'Healer Base',
#                  'Mystic Base',
#                  'Sorcerer Base',
#                  'Ranger Base',
#                  'Monk Base',
#                  'Dabbler Base',
#                  'Bard Base',
#                  'Magend Base',
#                  'Arcane'],
#           }
## \var spelltypes
# dictionary of spell types and their descriptions
# \todo add more text to the description part of the types
spelltypes = {'en' : {'E' : 'Elemental Spell',
                   'BE' : 'Ball Elemental Spell',
                   'DE' : 'Directed Elemenal Spell',
                   'F' : 'Force Spell',
                   'P' : 'Passive Spell',
                   'U' : 'Utility Spell',
                   'I' : 'Informational Spell',
                   's' : 'subconcious Spell',
                   'm' : 'Mental Attack Spell'
                   },
              'de' : {'E' : 'Elementarzauber',
                   'BE' : 'elementarer Ballzauber',
                   'DE' : 'gezielter Elemenarzauber',
                   'F' : 'Kraftzauber',
                   'P' : 'Passivzauber',
                   'U' : 'Nützlichkeitszauber',
                   'I' : 'Informationszauber',
                   's' : 'unbewußter Zauber',
                   'm' : 'mentaler Angriffszauber'
                   },
           }
##\var magicstats
# holds the magic attribute on the same index as the lists in realms
magicstats = ("", "Em", "In", "Pr", ['In', 'Pr'], ['In', 'Em'], ['Em', 'Pr'])
##\var labels
# a variety of labels, most of them for a character sheet
labels = {'de' : {'race' : 'Rasse',
                  'prof' : 'Beruf',
                  'prof bonus' : 'Berufsbonus',
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
                  'short' : 'Abk.',
                  'skill' : 'Talent',
                  'rank' : 'Stufe',
                  'lvl' : 'Stufe',
                  'prio' : "Priorität",
                  'costs' : 'Kosten',
                  'progress': 'Steigerung',
                  'sl-type': 'Spruchlistentyp',
                  'spell': 'Zauber',
                  'aoe' : "Wirkungsbereich",
                  'dura': "Dauer",
                  'range': "Reichweite",
                  'type' : "Typ",
                  'spec_note': "Bes. Anmerkungen",
                  'descr': "Beschreibung",
                  },
          'en' :{'race' : 'Race',
                  'prof' : 'Profession',
                  'prof bonus' : 'Profession Bonus',
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
                  'RREss' : 'RR Ess',
                  'RRMent' : 'RR Ment',
                  'RRArc' : 'RR Arcane Magic',
                  'RRC/E' : 'RR Chan/Ess',
                  'RRC/M' : 'RR Chan/Ment',
                  'RRE/M' : 'RR Ess/Ment',
                  'RRDisease' :'RR Disease',
                  'RRPoison' : "RR Poison",
                  'RRFear' : 'RR Fear',
                  'AT' : 'Armor Type',
                  'MAP' : 'Missile Attack Penalty',
                  'MMP' : 'Movement Maneuver Penalty',
                  'DB' : 'Defensive Bonus',
                  'shield' : 'Shield Bonus',
                  'total' : 'Total',
                  'Adrenal': "Adrenal Defense",
                  'DP' : 'Development Points',
                  'BGO' : 'Background Options',
                  'short' : 'Short',
                  'skill' : 'Skill',
                  'rank' : 'Rank',
                  'lvl' : 'Level',
                  'prio' : 'Priority',
                  'costs' : 'Costs',
                  'progress' : 'Progression',
                  'sl-type': 'Spell List Type',
                  'spell': 'Spell',
                  'aoe' : "Area of Effect",
                  'dura': "Duration",
                  'range': "Range",
                  'type' : "Type",
                  'spec_note': "Special Notes",
                  'descr': "Description",
                  },
          }
##\var progressionType
# This holds the different Cat/Skill/BD/PP development
progressionType = {'standard cat'   : (-15, 2, 1, 0.5, 0),
                   'standard skill' : (-15, 3, 2, 1, 0.5),
                   'combined'       : (-30, 5, 3, 2, 0.5),
                   'BD Common Men'     : (0, 6, 4, 2, 1),
                   'BD Mixed Men'     : (0, 6, 5, 2, 1),
                   'BD High Men'    : (0, 7, 5, 3, 1),
                   'BD Wood Elves'  : (0, 6, 3, 1, 1),
                   'BD Grey Elves'  : (0, 6, 3, 2, 1),
                   'BD High Elves'  : (0, 7, 3, 2, 1),
                   'BD Half Elves'  : (0, 7, 5, 3, 1),
                   'BD Dwarves' : (0, 7, 4, 2, 1),
                   'BD Halflings'   : (0, 6, 2, 2, 1),
                   'PPD Chan Common Men' : (0, 6, 5, 4, 3),
                   'PPD Chan Mixed Men' : (0, 6, 5, 4, 3),
                   'PPD Chan High Men'  : (0, 6, 5, 4, 3),
                   'PPD Chan Wood Elves'  : (0, 6, 5, 4, 3),
                   'PPD Chan Grey Elves'  : (0, 6, 5, 4, 3),
                   'PPD Chan High Elves'  : (0, 6, 5, 4, 3),
                   'PPD Chan Half Elves'  : (0, 6, 5, 4, 3),
                   'PPD Chan Dwarves'  : (0, 6, 5, 4, 3),
                   'PPD Chan Halflings'  : (0, 6, 5, 4, 3),
                   'PPD Ess Common Men' : (0, 6, 5, 4, 3),
                   'PPD Ess Mixed Men' : (0, 6, 5, 4, 3),
                   'PPD Ess High Men' : (0, 6, 5, 4, 3),
                   'PPD Ess Wood Elves'   : (0, 7, 6, 5, 4),
                   'PPD Ess Grey Elves'   : (0, 7, 6, 5, 4),
                   'PPD Ess High Elves'   : (0, 7, 6, 5, 4),
                   'PPD Ess Half Elves' : (0, 6, 6, 4, 3),
                   'PPD Ess Dwarves' : (0, 3, 2, 1, 1),
                   'PPD Ess Halflings' : (0, 2, 1, 1, 1),
                   'PPD Ment Common Men' : (0, 7, 6, 5, 4),
                   'PPD Ment Mixed Men' : (0, 7, 6, 5, 4),
                   'PPD Ment High Men' : (0, 7, 6, 5, 4),
                   'PPD Ment Wood Elves' : (0, 6, 5, 4, 3),
                   'PPD Ment Grey Elves' : (0, 6, 5, 4, 3),
                   'PPD Ment High Elves' : (0, 6, 5, 4, 3),
                   'PPD Ment Half Elves' : (0, 7, 5, 4, 3),
                   'PPD Ment Dwarves' : (0, 3, 2, 1, 1),
                   'PPD Ment Halflings' : (0, 2, 1, 1, 1),
                   'skill only' : (0, 1, 1, 0.5, 0),
                   'null' : (0, 0, 0, 0, 0)
                   } 

##\var raceAbilities
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
                 'Halflings' : {'Ag' : 6,
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
    Returns Developing Points Costs of Spell Lists. This is just needed if payed 
    with variable DP costs for spell lists.
    \param skill skill rank in that Spell List
    \param listtype List type of the Spell List
    \param sutype Spell User Type (pure, hybrid, semi, non).
    \param no number of Spell Lists developed this level
    \todo this function has to be implemented fully but it is not urgent.
    \deprecated this function may be deprecated because this is solved by CSV
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
    \todo implement German language support - will be handled by imported CSV files
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
        
    
    
        
def rankbonus(rank = 0, cat = 0, profession = 0, special = 0, progression = progressionType['standard cat']):
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

