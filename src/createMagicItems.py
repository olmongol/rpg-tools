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
import argparse, locale
from rpgtoolbox.rpgtools import dice

lang = locale.getdefaultlocale()[0][:2]
supported = ('de', 'en')

if lang not in supported:
    lang = 'en'

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

spellLvl = {'1-20': {'Runenpapier' :'1',
                     'Trank'       :'1',
                     'Taeglich I'  :'1',
                     'Taeglich II' :'1',
                     'Taeglich III':'1',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'1',
                     'Stecken'     :'1'
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
            '26-30':{'Runenpapier' :'2',
                     'Trank'       :'1',
                     'Taeglich I'  :'1',
                     'Taeglich II' :'1',
                     'Taeglich III':'1',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'1',
                     'Stecken'     :'2'
                     },
            '31-35':{ 'Runenpapier':'2',
                     'Trank'       :'2',
                     'Taeglich I'  :'1',
                     'Taeglich II' :'1',
                     'Taeglich III':'1',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'1',
                     'Stecken'     :'3'
                     },
            '36-40': {'Runenpapier':'2',
                     'Trank'       :'2',
                     'Taeglich I'  :'2',
                     'Taeglich II' :'1',
                     'Taeglich III':'1',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'2',
                     'Stecken'     :'3'
                     },
            '41-45': {'Runenpapier':'3',
                     'Trank'       :'2',
                     'Taeglich I'  :'2',
                     'Taeglich II' :'2',
                     'Taeglich III':'1',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'2',
                     'Stecken'     :'4'
                     },
            '46-50': {'Runenpapier':'3',
                     'Trank'       :'2',
                     'Taeglich I'  :'2',
                     'Taeglich II' :'2',
                     'Taeglich III':'2',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'2',
                     'Stecken'     :'4'
                     },
            '51-55': {'Runenpapier':'3',
                     'Trank'       :'2',
                     'Taeglich I'  :'3',
                     'Taeglich II' :'2',
                     'Taeglich III':'2',
                     'Taeglich IV' :'1',
                     'Stab'        :'1',
                     'Rute'        :'2',
                     'Stecken'     :'5'
                     },
            '56-60': {'Runenpapier':'4',
                     'Trank'       :'3',
                     'Taeglich I'  :'3',
                     'Taeglich II' :'2',
                     'Taeglich III':'2',
                     'Taeglich IV' :'2',
                     'Stab'        :'2',
                     'Rute'        :'3',
                     'Stecken'     :'5'
                     },
            '61-65': {'Runenpapier':'4',
                     'Trank'       :'3',
                     'Taeglich I'  :'3',
                     'Taeglich II' :'3',
                     'Taeglich III':'2',
                     'Taeglich IV' :'2',
                     'Stab'        :'2',
                     'Rute'        :'3',
                     'Stecken'     :'6'
                     },
            '66-70': {'Runenpapier':'4',
                     'Trank'       :'3',
                     'Taeglich I'  :'4',
                     'Taeglich II' :'3',
                     'Taeglich III':'2',
                     'Taeglich IV' :'2',
                     'Stab'        :'2',
                     'Rute'        :'3',
                     'Stecken'     :'7'
                     },
            '71-75': {'Runenpapier':'5',
                     'Trank'       :'4',
                     'Taeglich I'  :'4',
                     'Taeglich II' :'3',
                     'Taeglich III':'2',
                     'Taeglich IV' :'2',
                     'Stab'        :'2',
                     'Rute'        :'3',
                     'Stecken'     :'7'
                     },
            '76-80': {'Runenpapier':'5',
                     'Trank'       :'4',
                     'Taeglich I'  :'5',
                     'Taeglich II' :'4',
                     'Taeglich III':'3',
                     'Taeglich IV' :'2',
                     'Stab'        :'2',
                     'Rute'        :'4',
                     'Stecken'     :'7'
                     },
            '81-85': {'Runenpapier':'6',
                     'Trank'       :'5',
                     'Taeglich I'  :'5',
                     'Taeglich II' :'4',
                     'Taeglich III':'3',
                     'Taeglich IV' :'2',
                     'Stab'        :'2',
                     'Rute'        :'4',
                     'Stecken'     :'8'
                     },
            '86-90': {'Runenpapier':'7',
                     'Trank'       :'6',
                     'Taeglich I'  :'6',
                     'Taeglich II' :'5',
                     'Taeglich III':'3',
                     'Taeglich IV' :'3',
                     'Stab'        :'2',
                     'Rute'        :'4',
                     'Stecken'     :'8'
                     },
            '91-94': {'Runenpapier':'8',
                     'Trank'       :'7',
                     'Taeglich I'  :'7',
                     'Taeglich II' :'5',
                     'Taeglich III':'4',
                     'Taeglich IV' :'3',
                     'Stab'        :'2',
                     'Rute'        :'5',
                     'Stecken'     :'9'
                     },
            '95-97': {'Runenpapier':'9',
                     'Trank'       :'8',
                     'Taeglich I'  :'8',
                     'Taeglich II' :'6',
                     'Taeglich III':'4',
                     'Taeglich IV' :'3',
                     'Stab'        :'2',
                     'Rute'        :'5',
                     'Stecken'     :'9'
                     },
            '98-99': {'Runenpapier':'10',
                     'Trank'       :'9',
                     'Taeglich I'  :'9',
                     'Taeglich II' :'7',
                     'Taeglich III':'5',
                     'Taeglich IV' :'3',
                     'Stab'        :'2',
                     'Rute'        :'5',
                     'Stecken'     :'10'
                     },
            '100-100': { 'Runenpapier' :'10',
                         'Trank'       :'10',
                         'Taeglich I'  :'10',
                         'Taeglich II' :'7',
                         'Taeglich III':'5',
                         'Taeglich IV' :'3',
                         'Stab'        :'2',
                         'Rute'        :'5',
                         'Stecken'     :'10'
                       },
            }

##
# This holds the number of loaded spells in an item            
loadedSpells = {'Stab' : 10,
               'Rute' : 30,
               'Stecken' : 100
               }

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
                                     'en': 'Natures law'
                                     },
                       'Animisten': {'de': 'Seelenkunde',
                                     'en': 'Souls law'
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

header = {'de' : "Magische Gegenstaende:\n----------------------\n\n",
          'en' : "Magical Items:\n--------------\n\n"}


helptext = {'number' : {'de' : 'Anzahl der zu erzeugenden Gegenstaende',
                        'en' : 'Number of items to generate'
                        },
            'type' : {'de' : 'bestimmter Typ: \n40 Runenpapier \n65 Trank\n70 Taegl. I\n' + 
                      '75 Taegl. II\n80 Taegl. III\n85 Taegl. IV\n94 Stab\n98 Rute\n99 Stecken',
                      'en' : 'specific type: \n40 Rune Paper \n65 Trank \n70 Daily I \n' + 
                      '75 Daily II \n80 Daily III \n85 Daily IV \n 94 Wand \n98 Rod \n99 Pole'
                      },
            'out' : {'de' : "Name der Ausgabedatei",
                     'en' : 'Name of the output file'},
            'language' : {'de' : "zu verwendende Sprache",
                          'en' : 'used output language'},
            'finished' : {'de' : 'Datei erstellt: ',
                          'en' : 'Created file: '
                          }
            }
parser = argparse.ArgumentParser(description = "Magical Items Creator")
parser.add_argument('-n', '--number', action = 'store', type = int, default = 1,
                    help = helptext['number'][lang])
parser.add_argument('-t', '--type', type = int, default = 0,
                    help = helptext['type'][lang])
parser.add_argument('-o', '--out', default = "magicItems.txt", help = helptext['out'][lang])
parser.add_argument('-l', '--language', default = "de", help = helptext['language'][lang])

args = parser.parse_args()
n = args.number + 1
t = args.type
fn = args.out
lang = args.language

fcontent = header[lang]

for i in range(1, n):
    
    if t == 0:
        roll = dice(100, 4)
        
        for key1 in itemTypes.keys():
            dummy = key1.split('-')
 
            if int(dummy[0]) <= roll[0] <= int(dummy[1]):
                item = itemTypes[key1]['de']
                fcontent += "- " + itemTypes[key1][lang]
            
                if  item in loadedSpells.keys():
                    fcontent += " (" + str(dice(loadedSpells[item], 1)) + "/" + str(loadedSpells[item]) + ")"
                
                del(dummy)    
                break
            
        for key2 in spellRealms.keys():
            dummy = key2.split('-') 
            
            if int(dummy[0]) <= roll[1] <= int(dummy[1]):
                realm = spellRealms[key2]['de']
                fcontent += " " + spellRealms[key2][lang] + ":"
                del(dummy)
                break
            
        for key3 in spellLists.keys():
            dummy = key3.split('-')
            
            if int(dummy[0]) <= roll[2] <= int(dummy[1]):
                fcontent += ' ' + spellLists[key3][realm][lang] 
                del(dummy)
                break
            
        for key4 in spellLvl.keys():
            dummy = key4.split('-')
            
            if int(dummy[0]) <= roll[3] <= int(dummy[1]):
                fcontent += " [lvl " + spellLvl[key4][item] + "]\n"
                del(dummy)
                break
    
    else:
        roll = dice(100, 3)

        for key1 in itemTypes.keys():
            dummy = key1.split('-')
 
            if int(dummy[0]) <= t <= int(dummy[1]):
                item = itemTypes[key1]['de']
                fcontent += "- " + itemTypes[key1][lang]
            
                if  item in loadedSpells.keys():
                    fcontent += " (" + str(dice(loadedSpells[item], 1)) + "/" + str(loadedSpells[item]) + ")"
                
                del(dummy)    
                break
            
        for key2 in spellRealms.keys():
            dummy = key2.split('-') 
            
            if int(dummy[0]) <= roll[0] <= int(dummy[1]):
                realm = spellRealms[key2]['de']
                fcontent += " " + spellRealms[key2][lang] + ":"
                del(dummy)
                break
            
        for key3 in spellLists.keys():
            dummy = key3.split('-')
            
            if int(dummy[0]) <= roll[1] <= int(dummy[1]):
                fcontent += ' ' + spellLists[key3][realm][lang] 
                del(dummy)
                break
            
        for key4 in spellLvl.keys():
            dummy = key4.split('-')
            
            if int(dummy[0]) <= roll[2] <= int(dummy[1]):
                fcontent += " [lvl " + spellLvl[key4][item] + "]\n"
                del(dummy)
                break        
        
                
fp = open(fn, "w")
fp.write(fcontent)
fp.close()

print helptext['finished'][lang] + fn              
    
