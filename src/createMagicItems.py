#!/usr/bin/env python
'''
\file /home/mongol/git/rpg-tools/src/createMagicItems.py
\package createMagicItems
\brief This little program creates a random list of magical items 
Base of this are the MERS/MERP rules to create a random list of magic items. It 
It is possible to fixate the type item of by command line option. 
Language support exists for:
\li German (default)
\li English

\date (C) 2016
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
import argparse
from rpgToolDefinitions.helptools import dice

itemTypes = {'1-40': {'de': 'Runenpapier',
                      'en': 'Rune paper'
                      },
             '41-65': {'de': 'Trank',
                       'en': 'Potion'
                       },
             '66-70': {'de': 'Taeglich I',
                       'en': 'Daily I'
                       },
             '71-75': {'de': 'Taeglich II',
                       'en': 'Daily II'
                       },
             '76-80': {'de': 'Taeglich III',
                       'en': 'Daily III'
                       },
             '81-85': {'de': 'Taeglich IV',
                       'en': 'Daily IV'
                       },
             '86-94': {'de': 'Stab',
                       'en': 'Wand'
                       },
             '95-98': {'de': 'Rute',
                       'en': 'Rod'
                       },
             '99-100': {'de': 'Stecken',
                        'en': 'Pole'
                        } 
             }

spellLvl = {'1-20': {'Runenpapier':'1',
                     'Trank':'1',
                     'Taeglich I': '1',
                     'Taeglich II': '1',
                     'Taeglich III': '1',
                     'Taeglich IV': '1',
                     'Stab': '1',
                     'Rute': '1',
                     'Stecken':'1'
                     },
            '21-25': {'Runenpapier':'2',
                     'Trank'       :'1',
                     'Taeglich I'  :'1',
                     'Taeglich II' :'1',
                     'Taeglich III':'1',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'1',
                     'Stecken'     :'2'
                     },
            '26-30':{'Runenpapier':'2',
                     'Trank'       :'1',
                     'Taeglich I'  :'1',
                     'Taeglich II' :'1',
                     'Taeglich III':'1',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'1',
                     'Stecken'     :'2'
                     },
            '31-35':{'Runenpapier':'2',
                     'Trank'       :'2',
                     'Taeglich I'  :'1',
                     'Taeglich II' :'1',
                     'Taeglich III':'1',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'1',
                     'Stecken'     :'2'
                     },
            },

spellRealms = {'1-30': {'de': 'Offene Essenz',
                         'en': 'Open Essence'
                         },
               '31-60': {'de': 'Magier',
                         'en': 'Magician'
                         },
               '61-75': {'de': 'Leitmagie',
                         'en': 'Channeling',
                         },
               '76-90': {'de': 'Animisten',
                         'en': 'Animist'
                         },
               '91-100': {'de': 'Barde/Waldlaeufer',
                          'en': 'Bard/Hunter'
                          },
               }
spellLists = {'1-2' : {'Offene Essenz': {'de': 'Fluch',
                                         'en': 'Curse'
                                         },
                       'Magier': {'de': 'Fluch',
                                  'en': 'Curse'
                                 },
                       'Leitmagie': {'de': 'Fluch',
                                     'en': 'Curse'
                                    },
                       'Animisten': {'de': 'Fluch',
                                     'en': 'Curse'
                                    },
                       'Barde/Waldlaeufer': {'de': 'Fluch',
                                             'en': 'Curse'
                                             },
                       },
              '3-14': {'Offene Essenz': {'de': 'Herrschaft ueber den Koerper',
                                         'en': 'Reign over the body'
                                         },
                       'Magier': {'de': 'Gesetz des Feuers',
                                  'en': 'Fire Law'
                                  },
                       'Leitmagie': {'de': 'Naturkunde',
                                     'en': 'Nature´s law'
                                     },
                       'Animisten': {'de': 'Seelenkunde',
                                     'en': 'Soul´s law'
                                     },
                       'Barde/Waldlaeufer' : {'de': 'Wege des Lernens',
                                              'en': 'Ways of learning'
                                              },
                       },
              '15-26': {'Offene Essenz': {'de': 'Verborgenes Verstehen',
                                          'en': 'Hiden understanding'
                                          },
                        'Magier': {'de': 'Gesetz des Eises',
                                   'en': 'Ice law'
                                   },
                        'Leitmagie': {'de': 'Wege des Wandelns',
                                      'en': 'Ways of changing'
                                      },
                        'Animisten': {'de': 'Wesen des Blutes',
                                      'en': 'Nature of blood'
                                      },
                        'Barde/Waldlaeufer': {'de': 'Lieder der Macht',
                                              'en': 'Songs of power'
                                              },
                        },
              '27-38': {'Offene Essenz': {'de': 'Wege des Oeffnens',
                                          'en': 'Ways of Opening'
                                          },
                        'Magier': {'de': 'Gesetz der Erde',
                                   'en': 'Earth law'
                                   },
                        'Leitmagie': {'de': 'Abwehr von Zaubern',
                                      'en': 'Defense of Spells'
                                      },
                        'Animisten': {'de': 'Wesen der Knochen und Muskeln',
                                      'en': 'Nature of bones and muscles'
                                      },
                        'Barde/Waldlaeufer': {'de': 'Geraeuschkontrolle',
                                              'en': 'Sound control'
                                              },
                        },
              '39-50': {'Offene Essenz': {'de': 'Hand der Essenz',
                                          'en': 'Hand of essence'
                                          },
                        'Magier': {'de': 'Gesetz des Lichts',
                                   'en': 'Light law'
                                   },
                        'Leitmagie': {'de': 'Wege der Heilung',
                                      'en': 'Ways of healing'
                                      },
                        'Animisten': {'de': 'Wesen der Organe',
                                      'en': 'Nature of organs'
                                      },
                        'Barde/Waldlaeufer': {'de': 'Gegenstandskunde',
                                              'en': 'Item lore'
                                              },
                        },
              '51-62': {'Offene Essenz': {'de': 'Spruchkunde',
                                          'en': 'Spell lore'
                                          },
                        'Magier': {'de': 'Gesetz des Windes',
                                   'en': 'Wind law'
                                   },
                        'Leitmagie': {'de': 'Schutz',
                                      'en': 'Protection'
                                      },
                        'Animisten': {'de': 'Beherrschung der Tiere',
                                      'en': 'Animal control'
                                      },
                        'Barde/Waldlaeufer': {'de':'Wesen der Wege',
                                              'en': 'Nature of paths'
                                              },
                        },
              '63-74': {'Offene Essenz': {'de': 'Wege der Wahrnehmung',
                                          'en': 'Ways of perception'
                                          },
                        'Magier': {'de': 'Gesetz des Wassers',
                                   'en': 'Water law'
                                   },
                        'Leitmagie': {'de': 'Verborgenes Entdecken',
                                      'en': 'Discover hidden'
                                      },
                        'Animisten': {'de': 'Beherrschung der Pflanzen',
                                      'en': 'Plant control'
                                      },
                        'Barde/Waldlaeufer': {'de': 'Wege des Wanderns',
                                              'en': 'Ways of wandering'
                                              },
                        },
              '75-86': {'Offene Essenz': {'de': 'Illusionen',
                                          'en': 'Illusions'
                                          },
                        'Magier': {'de': 'Entfernungen Ueberbruecken',
                                   'en': 'Distance law'
                                   },
                        'Leitmagie': {'de': 'Wege von Geraeusch und Licht',
                                      'en': 'Ways of sound and light'
                                      },
                        'Animisten': {'de': 'Heilkunde',
                                      'en': 'Healing'
                                      },
                        'Barde/Waldlaeufer': {'de': 'Wege der Tarnung',
                                              'en': 'Ways of Camouflage'
                                              },
                        },
              '87-98': {'Offene Essenz': {'de': 'Herrschaft ueber den Geist',
                                          'en': 'Reign over the mind',
                                          },
                        'Magier': {'de': 'Koerperkontrolle',
                                   'en': 'Body control'
                                   },
                        'Leitmagie': {'de':'Wege der Beruhigung',
                                      'en': 'Ways of sedation',
                                      },
                        'Animisten': {'de': 'Nahrung und Schutz',
                                      'en': 'Food and Protection'
                                      },
                        'Barde/Waldlaeufer': {'de': 'Wesen der Natur',
                                              'en': 'Ways of Nature'
                                              },
                        },
              '99-100': {'Offene Essenz': {'de':'Besonderheit',
                                           'en':'Special'
                                           },
                         'Magier': {'de': 'Besonderheit',
                                    'en': 'Special'
                                    },
                         'Leitmagie': {'de': 'Besonderheit',
                                       'en': 'Special'
                                       },
                         'Animisten': {'de': 'Besonderheit',
                                       'en': 'Special'
                                       },
                         'Barde/Waldlaeufer': {'de': 'Besonderheit',
                                               'en': 'Special' 
                                               },
                         },
              
              }



parser = argparse.ArgumentParser(description = "Magical Items Creator")
parser.add_argument('-n', '--number', action = 'store', type = int, default = 1,
                    help = 'Anzahl der zu erzeugenden Gegenstaende')
parser.add_argument('-t', '--type', type = int, default = 0,
                    help = 'bestimmter Typ: \n40 Runenpapier \n65 Trank\n70 Taegl. I\n' + 
                    '75 Taegl. II\n80 Taegl. III\n85 Taegl. IV\n94 Stab\n98 Rute\n99 Stecken')
parser.add_argument('-o', '--out', default = "magicItems.txt", help = "Name der Ausgabedatei")
parser.add_argument('-l', '--language', default = "de", help = "zu verwendende Sprache")

args = parser.parse_args()
n = args.number
t = args.type
fn = args.out

for i in range(1, n):
    
    if t == 0:
        print "o"
    
