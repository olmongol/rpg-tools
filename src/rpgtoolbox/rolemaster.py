#!/bin/env python
# -*- coding: utf-8 -*-
'''!
\package rpgtoolbox.rolemaster
\file rolemaster.py
\brief Rolemaster specific toolbox

This package holds RM specific tools like Character Skill Progression.

\license GNU v3
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
\date 2019
\copyright 2015-2019 Marcus Schwamberger
'''
__updated__ = "15.04.2022"

catnames = {'de': {'spells': "Spells",
                    'weapon': 'Weapon',
                    },
            'en': {'spells': "Spells",
                    'weapon': 'Weapon',
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
                        'Magent Basis', 'Mystiker Basis', 'Böse Mentalistmus',
                        "Taoist-Mönch Basis", "Zen-Mönch Basis"
                        ],
                 'en': ['Open Channeling', 'Closed Channeling',
                        'Animist Base', 'Cleric Base', 'Paladin Base',
                        'Ranger Base', 'Healer Base', 'Evil Channeling',
                        'Open Essence', 'Closed Essence',
                        'Illusionist Base', 'Magican Base', 'Dabbler Base',
                        'Monk Base', 'Sorcerer Base', 'Evil Essence',
                        'Open Mentalism', 'Closed Mentalism',
                        'Lay Healer', 'Bard Base', 'Mentalist Base',
                        'Magent Base', 'Mystic Base', 'Evil Mentalism',
                        "Taoist Monk Base", "Zen Monk Base"
                        ],
                 }
## @var sldirs
# name of the subdirs of specific spell list types
sldirs = ["Channeling_Open", "Channeling_Closed", "Base_List_Animist", "Base_List_Cleric",
          'Base_List_Paladin', 'Base_List_Ranger', 'Base_List_Healer', 'Channeling_Evil',
          'Essence_Open', 'Essence_Closed', 'Base_List_Illusionist', 'Base_List_Magician',
          'Base_List_Dabbler', 'Base_List_Monk', 'Base_list_Sorcerer', 'Essence_Evil',
          'Mentalism_Open', 'Mentalism_Closed', 'Base_List_Lay-Healer', 'Base_List_Bard',
          'Base_List_Bard', 'Base_List_Mentalist', 'Base_List_Magent', 'Base_List_Mystic',
          'Mentalism_Evil', "Base_List_Taoist-Monk", "Base_List_Zen-Monk"]
##\var races
# just a dictionary for translation of the races' names
races = {'de': ['normale Menschen', 'vermischte Menschen', 'Hochmenschen',
                 "Waldelben", "Grauelben", "Hochelben",
                 "Halbelben", "Zwerge", "Halblinge"],
         'en': ['Common Men', 'Mixed Men', 'High Men', 'Wood Elves', 'Grey Elves',
                 'High Elves', 'Half Elves', 'Dwarves', 'Halflings']
         }

cultures = {'de': ['Huegelmenschen', 'Corsaren', 'Nomaden', 'Landvolk', 'Stadtmenschen',
                   'Waldmenschen', 'Hochmenschen', 'Waldelben', 'Grauelben', 'Hochelben',
                   'Halbelben', 'Zwerge', 'Halblinge'],
           'en': ['Hillmen', 'Mariners', 'Nomads', 'Ruralmen', 'Urbanmen', 'Woodmen',
                   'High Men', 'Wood Elves', 'Grey Elves', 'High Elves', 'Half Elves',
                   'Dwarves', 'Halflings']

           }

##\var langpack
# starting language packs by culture
langpack = {'de': {'Huegelmenschen': {},
                    'Corsaren': {},
                    'Nomaden': {},
                    'Landvolk': {},
                    'Stadtmenschen': {},
                    'Waldmenschen': {},
                    'Hochmenschen': {},
                    'Waldelben': {},
                    'Grauelben': {},
                    'Hochelben': {},
                    'Halbelben': {},
                    'Zwerge': {},
                    'Halblinge': {}
                    },
            'en': {'Hillmen': {},
                    'Mariners': {},
                    'Nomads': {},
                    'Ruralmen': {},
                    'Urbanmen': {},
                    'Woodmen': {},
                    'High Men': {},
                    'Wood Elves': {},
                    'Grey Elves': {},
                    'High Elves': {},
                    'Half Elves': {},
                    'Dwarves': {},
                    'Halflings': {}
                    }
            }

## \var culturalDefinition
# this dictionary holds average values and starting languages based on races
# \todo this has to be filled for all races for English and German
#
culturalDefinitions = {'en': {'Hillmen':{'weight':'',
                                          'height':'',
                                          'languages':{}
                                          },
                             'Mariners': {'weight':'',
                                          'height':'',
                                          'languages':{}},
                             'Nomads':{'weight':'',
                                          'height':'',
                                          'languages':{}
                                          },
                             'Ruralmen':{'weight':'',
                                          'height':'',
                                          'languages':{}
                                          },
                             'Urbanmen':{'weight':'',
                                          'height':'',
                                          'languages':{}
                                          },
                             'Woodmen':{'weight':'',
                                          'height':'',
                                          'languages':{}
                                          },
                             'High Men': {'weight':'m 112 kg / f 75 kg',
                                          'height':'m 183 cm / f 176 cm',
                                          'languages':{'Adunaic (spoken)':{'rank':8},
                                                       'Adunaic (written)':{'rank':6},
                                                       'Westron (spoken)':{'rank':8},
                                                       'Westron (written)':{'rank':6},
                                                       'Sindarin (spoken)':{'rank':6},
                                                       'Sindarin (written)':{'rank':6},
                                                       'Quenya (spoken)':{'rank':2},
                                                       'Quenya (written)':{'rank':2},
                                                       }
                                          },
                             'Wood Elves':{'weight':'',
                                          'height':'',
                                          'languages':{}
                                          },
                             'Grey Elves':{'weight':"m 95 kg 7 f 78 kg",
                                           "height": 'm  193 cm / f 183 cm',
                                           'languages':{ "Sindarin (spoken)": {"rank": 10},
                                                         "Sindarin (written)": {'rank':10},
                                                         "Silvan (spoken)": {'rank':8},
                                                         "Silvan (written)":{'rank':6},
                                                         'Quenya (spoken)':{'rank':6},
                                                         'Quenya (written)':{'rank':4},
                                                         'Westron (spoken)':{'rank':8},
                                                         'Westron (written)':{'rank':6}
                                                        }
                                           },
                             'High Elves':{'weight':'m 108 kg / f 78 kg',
                                          'height':'m 198 cm / f 188 cm',
                                          'languages':{'Quenya (spoken)':{'rank': 10},
                                                       'Quenya (written)':{'rank':10},
                                                       'Sindarin (spoken)':{'rank':8},
                                                       'Sindarin (written)':{'rank':6},
                                                       'Westron (spoken)':{'rank':8},
                                                       'Westron (written)':{'rank':6}
                                                       }
                                          },
                             'Half Elves':{'weight':'m 95 kg / f 68 kg',
                                           'height': 'm 188 cm / f 178 cm',
                                           'languages': { 'Sindarin (spoken)': {'rank': 8},
                                                          'Sindarin (written)':{'rank': 6},
                                                          'Westron (spoken)': {'rank': 8},
                                                          'Westron (written)': {'rank':6},
                                                          'Quenya (spoken)':{'rank': 6},
                                                          'Quenya (written)':{'rank':5}
                                                         }
                                           },
                             'Dwarves':{"weight": "m 75 kg / f 68 kg",
                                         'height': 'm 145 cm / f 135 cm',
                                         'languages': { 'Khuzdul (spoken)': {"rank": 8,
                                                                              "spec bonus": 0
                                                                              },
                                                        'Khuzdul (written)': {'rank': 6,
                                                                               "spec bonus":0
                                                                               },
                                                        "Westron (spoken)": {"rank":6},
                                                        "Westron (written)": {'rank':6},
                                                        "Silvan (spoken)":{"rank":4},
                                                        "Silvan (written)":{"rank":4}
                                                      }
                                         },
                             'Halflings':{'weight':'m 27 kg / f 25 kg',
                                          'height':'m 103 cm / f 98 cm',
                                          'languages':{'Kuduk (spoken)': 8,
                                                       'Kuduk (written)':6,
                                                       'Westron (spoken)': 8,
                                                       'Westron (written)': 6
                                                       }
                                          },
                             },
                    'de': {'Huegelmenschen': {},
                           'Corsaren': {},
                           'Nomaden': {},
                           'Landvolk': {},
                           'Stadtmenschen': {},
                           'Waldmenschen': {},
                           'Hochmenschen': {},
                           'Waldelben': {},
                           'Grauelben': {},
                           'Hochelben': {},
                           'Halbelben': {},
                           'Zwerge': {},
                           'Halblinge': {}
                        }
                    }
##\var stats
# the English shortcuts/indices for stats
stats = ['Ag', 'Co', 'Me', 'Re', 'SD', 'Em', 'In', 'Pr', 'Qu', 'St']

realmstats = {'de': {'Essence': 'Em',
                      'Channeling': 'In',
                      'Mentalism': 'Pr'
                      },
              'en': {'Essence': 'Em',
                      'Channeling': 'In',
                      'Mentalism': 'Pr'
                      },
              }

exceptions = ['Costs', 'Stats', 'Progression', 'rank', 'rank bonus', 'spec bonus', \
              'item bonus']
##\var realms
# a dictionary for translating the names of magic realms
realms = {'en': ('choice', 'Essence', 'Channeling', 'Mentalism',
                 ['Channeling', 'Mentalism'], ['Channeling', 'Essence'],
                 ['Essence', 'Mentalism']),
          'de': (u'wählbar', 'Essenz', 'Leitmagie', 'Mentalismus',
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

spellists = {"Essence":["Essence_Open", "Essence_Closed", "Essence_Evil",
                         "Base_List_Monk", "Base_List_Taoist-Monk", "Base_List_Dabbler",
                         "Base_List_Magician", "Base_List_Illusionist"
                         ],
             "Channeling":["Channeling_Open", "Channeling_Closed", "Channeling_Evil",
                           "Base_List_Ranger", "Base_List_Paladin", "Base_List_Cleric",
                           "Base_List_Animist"
                           ],
             "Mentalism": ["Mentalism_Open", "Mentalism_Closed", "Mentalism_Evil",
                           "Base_List_Zen-Monk", "Base_List_Bard", "Base_List_Magend",
                           "Base_List_Lay-Healer", "Base_List_Mentalist"
                           ],
             "Channeling/Mentalism":["Base_List_Healer"],
             "Channeling/Essence":["Base_List_Sorcerer"],
             "Essence/Mentalism":["Base_List_Mystic"]}
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
#                  'Magent Base',
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
#                  'Magent Base',
#                  'Arcane'],
#           }
## \var spelltypes
# dictionary of spell types and their descriptions
# \todo add more text to the description part of the types
spelltypes = {'en': {'E': 'Elemental Spell',
                   'BE': 'Ball Elemental Spell',
                   'DE': 'Directed Elemental Spell',
                   'F': 'Force Spell',
                   'P': 'Passive Spell',
                   'U': 'Utility Spell',
                   'I': 'Informational Spell',
                   's': 'subconcious Spell',
                   'm': 'Mental Attack Spell'
                   },
              'de': {'E': 'Elementarzauber',
                   'BE': 'elementarer Ballzauber',
                   'DE': 'gezielter Elementarzauber',
                   'F': 'Kraftzauber',
                   'P': 'Passivzauber',
                   'U': 'Nützlichkeitszauber',
                   'I': 'Informationszauber',
                   's': 'unbewußter Zauber',
                   'm': 'mentaler Angriffszauber'
                   },
           }
##\var magicstats
# holds the magic attribute on the same index as the lists in realms
magicstats = ("", "Em", "In", "Pr", ['In', 'Pr'], ['In', 'Em'], ['Em', 'Pr'])
##\var labels
# a variety of labels, most of them for a character sheet
labels = {'de': {'race': 'Rasse',
                  'prof': 'Beruf',
                  'prof bonus': 'Berufsbonus',
                  'name': 'Name',
                  'realm': 'Magiebereich',
                  'stats': 'Attribute',
                  'skin': 'Hautfarbe',
                  'culture': 'Volk',
                  'gender': 'Geschlecht',
                  'player': 'Spieler',
                  'ep': 'Erfahrungspunkte',
                  'eye': 'Augenfarbe',
                  'hair': 'Haar',
                  'height': 'Größe',
                  'weight': 'Gewicht',
                  'look': 'Aussehen',
                  'ap age': 'scheinbares Alter',
                  'age': 'tatsächliches Alter',
                  'parents': 'Eltern',
                  'partner': 'Partner',
                  'siblings': 'Geschwister',
                  'kids': 'Kinder',
                  'home': 'Heimatort',
                  'god': 'Gottheit',
                  'souvereign': 'Herrscher',
                  'Ag': 'Gewandtheit',
                  'Co': 'Konstitution',
                  'Me': 'Gedächnis',
                  'Re': 'Denkvermögen',
                  'SD': 'Selbstdisziplin',
                  'Em': 'Empathie',
                  'In': 'Intuition',
                  'Pr': 'Austrahlung',
                  'Qu': 'Schnelligkeit',
                  'St': 'Stärke',
                  'RRM': 'Widerstandswurfmodifikatoren',
                  'RRChan': 'WW Leitmagie',
                  'RREss': 'WW Essenzmagie',
                  'RRMent': 'WW Mentalismus',
                  'RRArc': 'WW Arkane Magie',
                  'RRC/E': 'WW Leit/Essenz',
                  'RRC/M': 'WW Leit/Ment',
                  'RRE/M': 'WW Essenz/Ment',
                  'RRDisease':'WW Krankheiten',
                  'RRPoison': "WW Gift",
                  'RRFear': 'WW Furcht',
                  'AT': 'Rüstungsklasse',
                  'MAP': 'Fernkampfabzug',
                  'MMP': 'Bewegungseinschränkung',
                  'DB': 'Defensivbonus',
                  'shield': 'Schildbonus',
                  'total': 'Gesamt',
                  'Adrenal': "besondere Verteidigung",
                  'DP': 'Entwicklungspunkte',
                  'BGO': 'Hintergrundoptionen',
                  'short': 'Abk.',
                  'skill': 'Talent',
                  'rank': 'Stufe',
                  'lvl': 'Stufe',
                  'prio': "Priorität",
                  'costs': 'Kosten',
                  'progress': 'Steigerung',
                  'sl-type': 'Spruchlistentyp',
                  'spell': 'Zauber',
                  'aoe': "Wirkungsbereich",
                  'dura': "Dauer",
                  'range': "Reichweite",
                  'type': "Typ",
                  'spec_note': "Bes. Anmerkungen",
                  'descr': "Beschreibung",
                  },
          'en':{'race': 'Race',
                  'prof': 'Profession',
                  'prof bonus': 'Profession Bonus',
                  'name': 'Name',
                  'realm': 'Magic Realm',
                  'stats': 'Attributes',
                  'skin': 'Skin Color',
                  'culture': 'Culture',
                  'gender': 'Gender',
                  'player': 'Player',
                  'ep': 'Experience Points',
                  'eye': 'Eye Color',
                  'hair': 'Hair',
                  'height': 'Height',
                  'weight': 'Weight',
                  'look': 'Look',
                  'ap age': 'apparent Age',
                  'age': 'current Age',
                  'parents': 'Parents',
                  'partner': 'Partner',
                  'siblings': 'Siblings',
                  'kids': 'Children',
                  'home': 'Home Town',
                  'god': 'Deity',
                  'souvereign': 'Souvereign',
                  'Ag': 'Agility',
                  'Co': 'Constitution',
                  'Me': 'Memory',
                  'Re': 'Reasoning',
                  'SD': 'Self Disziplin',
                  'Em': 'Empathy',
                  'In': 'Intuition',
                  'Pr': 'Presence',
                  'Qu': 'Quickness',
                  'St': 'Strength',
                  'RRM': 'Resistance Rolls Modifiers',
                  'RRChan': 'RR Channeling',
                  'RREss': 'RR Ess',
                  'RRMent': 'RR Ment',
                  'RRArc': 'RR Arcane Magic',
                  'RRC/E': 'RR Chan/Ess',
                  'RRC/M': 'RR Chan/Ment',
                  'RRE/M': 'RR Ess/Ment',
                  'RRDisease':'RR Disease',
                  'RRPoison': "RR Poison",
                  'RRFear': 'RR Fear',
                  'AT': 'Armor Type',
                  'MAP': 'Missile Attack Penalty',
                  'MMP': 'Movement Maneuver Penalty',
                  'DB': 'Defensive Bonus',
                  'shield': 'Shield Bonus',
                  'total': 'Total',
                  'Adrenal': "Adrenal Defense",
                  'DP': 'Development Points',
                  'BGO': 'Background Options',
                  'short': 'Short',
                  'skill': 'Skill',
                  'rank': 'Rank',
                  'lvl': 'Level',
                  'prio': 'Priority',
                  'costs': 'Costs',
                  'progress': 'Progression',
                  'sl-type': 'Spell List Type',
                  'spell': 'Spell',
                  'aoe': "Area of Effect",
                  'dura': "Duration",
                  'range': "Range",
                  'type': "Type",
                  'spec_note': "Special Notes",
                  'descr': "Description",
                  },
          }
##\var progressionType
# This holds the different Cat/Skill/BD/PP development
progressionType = {'standard cat': (-15, 2, 1, 0.5, 0),
                   'standard skill': (-15, 3, 2, 1, 0.5),
                   'combined': (-30, 5, 3, 2, 0.5),
                   'BD Common Men': (0, 6, 4, 2, 1),
                   'BD Mixed Men': (0, 6, 5, 2, 1),
                   'BD High Men': (0, 7, 5, 3, 1),
                   'BD Wood Elves': (0, 6, 3, 1, 1),
                   'BD Grey Elves': (0, 6, 3, 2, 1),
                   'BD High Elves': (0, 7, 3, 2, 1),
                   'BD Half Elves': (0, 7, 5, 3, 1),
                   'BD Dwarves': (0, 7, 4, 2, 1),
                   'BD Halflings': (0, 6, 2, 2, 1),
                   'PPD Chan Common Men': (0, 6, 5, 4, 3),
                   'PPD Chan Mixed Men': (0, 6, 5, 4, 3),
                   'PPD Chan High Men': (0, 6, 5, 4, 3),
                   'PPD Chan Wood Elves': (0, 6, 5, 4, 3),
                   'PPD Chan Grey Elves': (0, 6, 5, 4, 3),
                   'PPD Chan High Elves': (0, 6, 5, 4, 3),
                   'PPD Chan Half Elves': (0, 6, 5, 4, 3),
                   'PPD Chan Dwarves': (0, 6, 5, 4, 3),
                   'PPD Chan Halflings': (0, 6, 5, 4, 3),
                   'PPD Ess Common Men': (0, 6, 5, 4, 3),
                   'PPD Ess Mixed Men': (0, 6, 5, 4, 3),
                   'PPD Ess High Men': (0, 6, 5, 4, 3),
                   'PPD Ess Wood Elves': (0, 7, 6, 5, 4),
                   'PPD Ess Grey Elves': (0, 7, 6, 5, 4),
                   'PPD Ess High Elves': (0, 7, 6, 5, 4),
                   'PPD Ess Half Elves': (0, 6, 6, 4, 3),
                   'PPD Ess Dwarves': (0, 3, 2, 1, 1),
                   'PPD Ess Halflings': (0, 2, 1, 1, 1),
                   'PPD Ment Common Men': (0, 7, 6, 5, 4),
                   'PPD Ment Mixed Men': (0, 7, 6, 5, 4),
                   'PPD Ment High Men': (0, 7, 6, 5, 4),
                   'PPD Ment Wood Elves': (0, 6, 5, 4, 3),
                   'PPD Ment Grey Elves': (0, 6, 5, 4, 3),
                   'PPD Ment High Elves': (0, 6, 5, 4, 3),
                   'PPD Ment Half Elves': (0, 7, 5, 4, 3),
                   'PPD Ment Dwarves': (0, 3, 2, 1, 1),
                   'PPD Ment Halflings': (0, 2, 1, 1, 1),
                   'skill only': (0, 1, 1, 0.5, 0),
                   'null': (0, 0, 0, 0, 0)
                   }

##\var raceAbilities
# Race bonusses for stats, RR and BGO
raceAbilities = {'Common Men': {'Ag': 0,
                                'Co': 0,
                                'Me': 0,
                                'Re': 0,
                                'SD': 2,
                                'Em': 0,
                                'In': 0,
                                'Pr': 0,
                                'Qu': 0,
                                'St': 2,
                                'RREss': 0,
                                'RRChan': 0,
                                'RRMent': 0,
                                'RRPoison': 0,
                                'RRDisease': 0,
                                'BGO': 6,
                                'Hobby Ranks': 12,
                                },
                 'Mixed Men': {'Ag': 0,
                                'Co': 2,
                                'Me': 0,
                                'Re': 0,
                                'SD': 2,
                                'Em': 0,
                                'In': 0,
                                'Pr': 2,
                                'Qu': 0,
                                'St': 2,
                                'RREss': 0,
                                'RRChan': 0,
                                'RRMent': 0,
                                'RRPoison': 0,
                                'RRDisease': 0,
                                'BGO': 5,
                                'Hobby Ranks': 12,
                                },
                 'High Men': {'Ag':-2,
                                'Co': 4,
                                'Me': 0,
                                'Re': 0,
                                'SD': 0,
                                'Em': 0,
                                'In': 0,
                                'Pr': 4,
                                'Qu':-2,
                                'St': 4,
                                'RREss':-5,
                                'RRChan':-5,
                                'RRMent':-5,
                                'RRPoison': 0,
                                'RRDisease': 0,
                                'BGO': 4,
                                'Hobby Ranks': 10,
                                },
                 'Wood Elves': {'Ag': 4,
                                'Co': 0,
                                'Me': 2,
                                'Re': 0,
                                'SD':-5,
                                'Em': 2,
                                'In': 0,
                                'Pr': 2,
                                'Qu': 2,
                                'St': 0,
                                'RREss':-5,
                                'RRChan':-5,
                                'RRMent':-5,
                                'RRPoison': 10,
                                'RRDisease': 100,
                                'BGO': 4,
                                'Hobby Ranks': 10,
                                },
                 'Grey Elves': {'Ag': 2,
                                'Co': 0,
                                'Me': 2,
                                'Re': 0,
                                'SD':-5,
                                'Em': 2,
                                'In': 0,
                                'Pr': 4,
                                'Qu': 4,
                                'St': 0,
                                'RREss':-5,
                                'RRChan':-5,
                                'RRMent':-5,
                                'RRPoison': 10,
                                'RRDisease': 100,
                                'BGO': 3,
                                'Hobby Ranks': 8,
                                },
                 'High Elves': {'Ag': 2,
                                'Co': 0,
                                'Me': 2,
                                'Re': 0,
                                'SD':-5,
                                'Em': 2,
                                'In': 0,
                                'Pr': 6,
                                'Qu': 6,
                                'St': 0,
                                'RREss':-5,
                                'RRChan':-5,
                                'RRMent':-5,
                                'RRPoison': 10,
                                'RRDisease': 100,
                                'BGO': 2,
                                'Hobby Ranks': 6,
                                },
                 'Half Elves': {'Ag': 2,
                                'Co': 2,
                                'Me': 0,
                                'Re': 0,
                                'SD':-3,
                                'Em': 0,
                                'In': 0,
                                'Pr': 4,
                                'Qu': 4,
                                'St': 2,
                                'RREss':-5,
                                'RRChan':-5,
                                'RRMent':-5,
                                'RRPoison': 0,
                                'RRDisease': 50,
                                'BGO': 4,
                                'Hobby Ranks': 10,
                                },
                 'Dwarves': {'Ag':-2,
                                'Co': 6,
                                'Me': 0,
                                'Re': 0,
                                'SD': 2,
                                'Em':-4,
                                'In': 0,
                                'Pr':-4,
                                'Qu':-2,
                                'St': 2,
                                'RREss': 40,
                                'RRChan': 0,
                                'RRMent': 40,
                                'RRPoison': 20,
                                'RRDisease': 15,
                                'BGO': 5,
                                'Hobby Ranks': 12,
                                },
                 'Halflings': {'Ag': 6,
                                'Co': 6,
                                'Me': 0,
                                'Re': 0,
                                'SD':-4,
                                'Em':-2,
                                'In': 0,
                                'Pr':-6,
                                'Qu': 4,
                                'St':-8,
                                'RREss': 50,
                                'RRChan': 0,
                                'RRMent': 40,
                                'RRPoison': 30,
                                'RRDisease': 15,
                                'BGO': 5,
                                'Hobby Ranks': 12,
                                },
                 }
##\var raceHealingFactors
# this dictionary holds race based information about Stat Loss Type, Rnds to soul
# departure and recovery multiplier.
raceHealingFactors = {"Common Men": {"soul dep": 12,
                                      "Stat Loss": 2,
                                      "Recovery": 1.0
                                      },
                      "Mixed Men": {"soul dep": 11,
                                      "Stat Loss": 2,
                                      "Recovery": 0.9
                                      },
                      "High Men": {"soul dep": 10,
                                      "Stat Loss": 2,
                                      "Recovery": 0.75
                                      },
                      "Wood Elves": {"soul dep": 3,
                                      "Stat Loss": 3,
                                      "Recovery": 1.5
                                      },
                      "Grey Elves": {"soul dep": 2,
                                      "Stat Loss": 4,
                                      "Recovery": 2.0
                                      },
                      "High Elves": {"soul dep": 1,
                                      "Stat Loss": 5,
                                      "Recovery": 3.0
                                      },
                      "Half Elves": {"soul dep": 6,
                                      "Stat Loss": 3,
                                      "Recovery": 1.5
                                      },
                      "Dwarves": {"soul dep": 21,
                                      "Stat Loss": 1,
                                      "Recovery": 0.5
                                      },
                      "Halflings": {"soul dep": 18,
                                      "Stat Loss": 1,
                                      "Recovery": 0.5
                                      }
                      }



def DPCostSpells(skill = 0, listtype = "Own Realm Own Base Lists", profession = "Magician", no = 1):
    '''
    Returns Developing Points Costs of Spell Lists. This is just needed if payed
    with variable DP costs for spell lists.
    \param skill skill rank in that Spell List
    \param listtype List type of the Spell List
    \param profession of the character.
    \param no number of Spell Lists developed this level
    \retval costs a list of the developing costs for that type of spell lists.
    \todo add "Arcane Open Lists" as well.
    '''
    costs = "N/A"
    factor = 1
    nonspellusers = ["Fighter", "Thief", "Rogue", "Warrior Monk", "Layman"]
    hybridspellusers = ["Healer", "Mystic", "Sorcerer"]
    purespellusers = ['Animist', "Cleric", "Illusionist",
                      "Magician", "Lay Healer", "Mentalist"
                      ]
    semispellusers = ["Paladin", "Ranger", "Dabbler",
                      "Monk", "Bard", "Magent", "Taoist-Monk", "Zen_Monk"
                      ]

    if 5 < no < 11:
        factor *= 2

    elif no > 10:
        factor *= 4

    if listtype == "Own Realm Own Base Lists":

        if profession in purespellusers:
            costs = [3, 3, 3]

        elif profession in hybridspellusers:
            costs = [3, 3, 3]

        elif profession in semispellusers:
            costs = [6, 6, 6]
        else:
            costs = [100000]

    elif listtype == "Own Realm Open Lists":

        if profession in purespellusers:

            if skill < 21:
                costs = [4, 4, 4]

            else:
                costs = [6, 6, 6]

        elif profession in hybridspellusers:

            if skill < 11:
                costs = [4, 4, 4]

            elif 10 < skill < 16:
                costs = [6, 6, 6]

            elif 16 < skill < 21:
                costs = [8, 8]

            else:
                costs = [12]

        elif profession in semispellusers:

            if skill < 11:
                costs = [8, 8]

            elif 10 < skill < 16:
                costs = [12]

            elif 15 < skill < 21:
                costs = [18]

            else:
                costs = [25]

        elif profession in nonspellusers:
            nsucosts = {"Fighter": 25,
                        "Thief": 18,
                        "Rogue": 15,
                        "Warrior Monk": 20,
                        "Layman": 10
                        }
            costs = [nsucosts[profession]]

            if 5 < skill < 11:
                costs[0] *= 2

            elif 10 < skill < 16:
                costs[0] *= 3

            elif 15 < skill < 21:
                costs[0] *= 4

            elif 20 < skill:
                costs[0] *= 5

    elif listtype == "Own Realm Closed Lists":

        if profession in purespellusers:

            if skill < 21:
                costs = [4, 4, 4]

            else:
                costs = [8, 8]

        elif profession in hybridspellusers:

            if skill < 11:
                costs = [4, 4, 4]

            elif 10 < skill < 16:
                costs = [6, 6, 6]

            elif 16 < skill < 21:
                costs = [10, 10]

            else:
                costs = [25]

        elif profession in semispellusers:

            if skill < 6:
                costs = [10, 10]

            elif 5 < skill < 11:
                costs = [12]

            elif 10 < skill < 16:
                costs = [25]

            elif 15 < skill < 21:
                costs = [40]

            else:
                costs = [60]

        elif profession in nonspellusers:
            nsucosts = {"Fighter": 40,
                        "Thief": 35,
                        "Rogue": 25,
                        "Warrior Monk": 30,
                        "Layman": 15
                        }
            costs = [nsucosts[profession]]

            if 5 < skill < 11:
                costs[0] *= 2

            elif 10 < skill < 16:
                costs[0] *= 3

            elif 15 < skill < 21:
                costs[0] *= 4

            elif 20 < skill:
                costs[0] *= 5

    elif listtype == "Own Realm Other Base Lists":

        if profession in purespellusers:

            if skill < 6:
                costs = [8, 8]

            elif 5 < skill < 11:
                costs = [10, 10]

            elif 10 < skill < 16:
                costs = [12]

            elif 15 < skill < 21:
                costs = [25]

            else:
                costs = [40]

        elif profession in hybridspellusers:

            if skill < 6:
                costs = [10, 10]

            elif 5 < skill < 11:
                costs = [12]

            elif 10 < skill < 16:
                costs = [25]

            elif 15 < skill < 21:
                costs = [40]

            else:
                costs = [60]

        elif profession in semispellusers:

            if skill < 6:
                costs = [25]

            elif 5 < skill < 11:
                costs = [40]

            elif 10 < skill < 16:
                costs = [60]

            elif 15 < skill < 21:
                costs = [80]

            else:
                costs = [100]

        elif profession in nonspellusers:
            nsucosts = {"Fighter": 80,
                        "Thief": 70,
                        "Rogue": 50,
                        "Warrior Monk": 60,
                        "Layman": 15
                        }
            costs = [nsucosts[profession]]

            if 5 < skill < 11:
                costs[0] *= 2

            elif 10 < skill < 16:
                costs[0] *= 3

            elif 15 < skill < 21:
                costs[0] *= 4

            elif 20 < skill:
                costs[0] *= 5

    elif listtype == "Other Realm Open Lists":

        if profession in purespellusers:
            if skill < 6:
                costs = [10, 10]

            elif 5 < skill < 11:
                costs = [12]

            elif 10 < skill < 16:
                costs = [25]

            elif 15 < skill < 21:
                costs = [40]

            else:
                costs = [60]

        elif profession in hybridspellusers:
            if skill < 6:
                costs = [12]

            elif 5 < skill < 11:
                costs = [25]

            elif 10 < skill < 16:
                costs = [40]

            elif 15 < skill < 21:
                costs = [60]

            else:
                costs = [80]

        elif profession in semispellusers:

            if skill < 6:
                costs = [30]

            elif 5 < skill < 11:
                costs = [60]

            elif 10 < skill < 16:
                costs = [80]

            elif 15 < skill < 21:
                costs = [100]

            else:
                costs = [120]

        elif profession in nonspellusers:
            nsucosts = {"Fighter": 90,
                        "Thief": 80,
                        "Rogue": 60,
                        "Warrior Monk": 70,
                        "Layman": 40
                        }
            costs = [nsucosts[profession]]

            if 5 < skill < 11:
                costs[0] *= 2

            elif 10 < skill < 16:
                costs[0] *= 3

            elif 15 < skill < 21:
                costs[0] *= 4

            elif 20 < skill:
                costs[0] *= 5

    elif listtype == "Other Realm Closed Lists":

        if profession in purespellusers:
            if skill < 6:
                costs = [20]

            elif 5 < skill < 11:
                costs = [25]

            elif 10 < skill < 16:
                costs = [40]

            elif 15 < skill < 21:
                costs = [60]

            else:
                costs = [80]

        elif profession in hybridspellusers:
            if skill < 6:
                costs = [25]

            elif 5 < skill < 11:
                costs = [40]

            elif 10 < skill < 16:
                costs = [60]

            elif 15 < skill < 21:
                costs = [80]

            else:
                costs = [100]

        elif profession in semispellusers:
            if skill < 6:
                costs = [45]

            elif 5 < skill < 11:
                costs = [60]

            elif 10 < skill < 16:
                costs = [80]

            elif 15 < skill < 21:
                costs = [100]

            else:
                costs = [120]

        elif profession in nonspellusers:
            nsucosts = {"Fighter": 105,
                        "Thief": 100,
                        "Rogue": 90,
                        "Warrior Monk": 95,
                        "Layman": 80
                        }
            costs = [nsucosts[profession]]

            if 5 < skill < 11:
                costs[0] *= 2

            elif 10 < skill < 16:
                costs[0] *= 3

            elif 15 < skill < 21:
                costs[0] *= 4

            elif 20 < skill:
                costs[0] *= 5

    elif listtype == "Other Realm Other Base Lists":

        if profession in purespellusers:

            if skill < 6:
                costs = [50]

            elif 5 < skill < 11:
                costs = [70]

            elif 10 < skill < 16:
                costs = [90]

            elif 15 < skill < 21:
                costs = [110]

            else:
                costs = [130]

        elif profession in hybridspellusers:

            if skill < 6:
                costs = [60]

            elif 5 < skill < 11:
                costs = [80]

            elif 10 < skill < 16:
                costs = [100]

            elif 15 < skill < 21:
                costs = [120]

            else:
                costs = [140]

        elif profession in semispellusers:

            if skill < 6:
                costs = [80]

            elif 5 < skill < 11:
                costs = [100]

            elif 10 < skill < 16:
                costs = [120]

            elif 15 < skill < 21:
                costs = [140]

            else:
                costs = [160]

        elif profession in nonspellusers:
            nsucosts = {"Fighter": 120,
                        "Thief": 120,
                        "Rogue": 120,
                        "Warrior Monk": 120,
                        "Layman": 100
                        }
            costs = [nsucosts[profession]]

            if 5 < skill < 11:
                costs[0] *= 2

            elif 10 < skill < 16:
                costs[0] *= 3

            elif 15 < skill < 21:
                costs[0] *= 4

            elif 20 < skill:
                costs[0] *= 5

#    elif listtype == "Arcane Open Lists":
#

    if type(costs) == type([]):

        for i in range(0, len(costs)):
            costs[i] *= factor

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

    for prof in list(professions.keys()):
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
        print("stats cannot be less then 20")
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



def refreshStatBonus(character = {}):
    '''
    This function recalculates Stat bonusses and refreshes their bunus values in
    the complete character data structure: Stat, Category
    @param character data in a dictionary/JSON
    @retval result refreshed character data
    '''
    result = character
    statlist = ["Ag", "Co", "Me", "Re", "In", "Pr", "SD", "Em", "Qu", "St"]

    for s in statlist:
        result[s]["std"] = statbonus(result[s]["temp"])
        result[s]["total"] = result[s]["std"] + result[s]["spec"] + result[s]["race"]

    for cat in list(result["cat"].keys()):
        dummy = 0

        if type(result["cat"][cat]["Stats"]) == type("") and len(result["cat"][cat]["Stats"]) == 2:
            cng = result["cat"][cat]["Stats"]
            result["cat"][cat]["Stats"] = [cng]

        for s in result["cat"][cat]["Stats"]:

            if s == "":
                pass
            elif s.strip(" ") != "SD":
                dummy += result[s.strip(" ").capitalize()]["total"]

            else:
                dummy += result[s]["total"]

        result["cat"][cat]["stat bonus"] = dummy

    return result



def bgoMoney(purse = {}):
    '''
    Extra money by BGO
    @param purse dictionary holding the character's purse
    @retval result dictionary as new purse of character
    '''
    from rpgtoolbox.rpgtools import dice
    roll = dice(100, 1)
    result = dict(purse)

    if roll < 3:
        result['GP'] += 1

    elif 2 < roll < 6:
        result['GP'] += 2

    elif 5 < roll < 16:
        result['GP'] += 5

    elif 15 < roll < 26:
        result['GP'] += 10

    elif 25 < roll < 36:
        result['GP'] += 15

    elif 35 < roll < 46:
        result['GP'] += 20

    elif 45 < roll < 56:
        result['GP'] += 30

    elif 55 < roll < 66:
        result['GP'] += 35

    elif 65 < roll < 71:
        result['GP'] += 40

    elif 70 < roll < 76:
        result['GP'] += 50

    elif 75 < roll < 81:
        result['GP'] += 60

    elif 80 < roll < 86:
        result['GP'] += 70

    elif 85 < roll < 91:
        result['GP'] += 80

    elif 90 < roll < 95:
        result['GP'] += 100

    elif 94 < roll < 98:
        result['GP'] += 125

    elif 97 < roll < 100:
        result['GP'] += 150

    elif roll == 100:
        result['GP'] += 200

    return result



def calcEncumberance(charweight = 80, maxv = 15):
    '''
    '''
    bwa = (charweight * 2) // 10
    result = {}

    for i in range(1, maxv + 1):
        result["{}x BWA"] = {"kg": bwa * i, "Enc. Pen.": 8 * (i - 1)}

    return result



def calcHitMods(char = {}):
    '''
    This calculates all data concerning hits like recovery or modifikations by injuries.
    @param char whole character dictionary/JSON
    @reval result dictionary holding all calculated data
    '''
    Co = char["Co"]['total']
    result = {"total hits": char["cat"]["Body Development"]["Skill"]["Body Development"]["total bonus"]}
    result["active"] = "1 hit/3 hours"
    result["resting"] = "{} hits/hour".format(round(Co / 2 + 0.01))
    result["sleep"] = "{} hits/sleep cycle".format(Co * 2)
    r = result['total hits'] % 4
    p = result["total hits"] // 4

    for i in range(1, 4):
        result["mod{}".format(i)] = {"hits":p * i + 1,
                                     "mod":i * -10
                                     }
        if (i == 1 and r > 2) or (i == 2 and r > 1) or (i == 3 and r > 0):
            result["mod{}".format(i)]["hits"] += 1

    return result

