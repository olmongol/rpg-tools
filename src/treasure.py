#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
\file treasure.py
\package rpg-tools


\date (C) 2017
\author Marcus Schwamberger, Aiko Ruprecht
\email marcus@lederzeug.de
\version 1.0
\license GNU v3
'''

import locale
from rpgtoolbox.rpgtools import dice

class treasure():
    '''
    \class treasure Creation of a treasure using the MERP/MERS tables to create a random treasure. 
    '''

    def __init__(self, lang = ''):

        self.supported = ('de', 'en')

        if lang in self.supported:
            self.lang = lang
        else:
            if lang != '':
                print('Error: Language not supported. Switch to default')
            self.lang = locale.getdefaultlocale()[0][:2]
            if self.lang not in self.supported:
                self.lang = 'en'


    def help(self):
        '''
        prints helptext in the language defined in variable lang
        '''
        helptext = {'description' : {'de' : 'Schatzgenerator:\nErzeugt einen Text, der den Inhalt eines Schatzes beschreibt.\nParameter der Funktion findTreasure:\n',
                                     'en' : 'Treasure Generator:\nCreates a text describing the content of a treasure.\nParameters of the function findTreasure:\n'
                                    },
                    'ttype' : {'de': 'Nummer oder Sch�sselwort einer der folgenden Kategorien\n   1 sehr arm, 2 arm, 3 normal, 4 reich, 5 sehr reich\n',
                               'en': 'Number or keyword of one of the following categores\n   1 very poor, 2 poor, 3 normal, 4 rich, 5 very rich\n' 
                               },
                    'output' : {'de' : 'Drei Optionen\n  \"screen\" --> Ausgabe auf den Bildschirm.\n  <string> --> Name der Ausgabedatei in die ausgegeben werden soll.\n  \"\" --> Es wird keine Datei erstellt, wenn der Parameter nicht gesetzt ist.',
                                'en' : 'Three options\n  \"screen\" --> Output on the screen.\n  <string> --> Name of the file which will be used for output.\n  \"\" --> No file is created if the parameter is not set.'
                                    }
                    }
        
        dummy = helptext['description'][self.lang]
        dummy += 'ttype: ' + helptext['ttype'][self.lang]
        dummy += 'output: ' + helptext['output'][self.lang]

        print(dummy)
        del (dummy)
        

    def findTreasure(self, ttype=3, output="screen"):
        '''
        Determine contents of one or several treasures and create a description of the contents.
        Details are listed in function help
        \param ttype Number or keyword of the category of the treasure
        \param output Options: screen, Name of the output file
        \param lang Language of the output text
        \return Text listing money and magic items in the treasures
        '''
        if self.lang not in self.supported:
            print('Error: Language not supported. Switch to default')
            self.lang = locale.getdefaultlocale()[0][:2]
            if self.lang not in self.supported:
                self.lang = 'en'

        typelist = {'de': ('sehr_arm', 'arm', 'normal', 'reich', 'sehr_reich'),
                    'en': ('very_poor', 'poor', 'normal', 'rich', 'very_rich'),
                    'num': (1, 2, 3, 4, 5)
                    }

        if ttype == "precious":
            return "Ring!"
        
        try:
            treasuretype = typelist[self.lang].index(ttype) + 1
        except:
            try:
                treasuretype = typelist['num'].index(ttype) + 1
            except:
                print("Error: Invalid value category! Set value to default (normal)")
                treasuretype = 3

        finished = {'de' : 'Datei erstellt: ',
                    'en' : 'Created file: '
                    }

        header = {'de' : "Schatzinhalt",
                  'en' : "Content of Treasure"
                  }
        
        # generate complete text
        fcontent = "*** %s ***\n \n"%(header[self.lang])
        fcontent += self.findMoney(treasuretype) + self.findItems(treasuretype) + "\n\n"
        
        fcontent = fcontent.strip()
            
        if output == "screen":
            
            print(fcontent)
            return(fcontent)
            
        elif output == "":
            
            return(fcontent)
        
        else:
            
            try:
                fp = open(output, "w")
                fp.write(fcontent)
                fp.close()
                print(finished[self.lang] + output)
                return(fcontent)
            except:
                print('Error: invalid file name')
                return("")


    def findMoney(self, richness=3):
        '''
        Function to determine amount of Money in treasure
        \param richness value category (1-5)
        \return string holding the treasured Money
        '''
        if richness not in range(1, 6):
    
            print("Error: Invalid value category! Set value to default (normal)")
            richness = 3
    
        if self.lang not in self.supported:
            
            print('Error: Language not supported. Switch to default')
            self.lang = locale.getdefaultlocale()[0][:2]
            
            if self.lang not in self.supported:
                
                self.lang = 'en'


        #total amount listed for the different values
        self.money = [[0, "ZS"], [0, "KS"], [0, "BS"], [0, "SS"], [0, "GS"], [0, "MS"], [0, "Ed"], [0, "Sch"]]
    
        values = {"ZS":0, "KS":1, "BS":2, "SS":3, "GS":4, "MS": 5, "Ed":6, "Sch":7}
        
        self.valueTranslation = {"ZS": {"de": "Zinnst�cke",
                                       "en": "tin pieces"
                                       },
                                "KS": {"de": "Kupferst�cke",
                                       "en": "copper pieces"
                                       },
                                "BS": {"de": "Bronzest�cke",
                                       "en": "bronze pieces"
                                       },
                                "SS": {"de": "Silberst�cke",
                                       "en": "silver pieces"
                                       },
                                "GS": {"de": "Goldst�cke",
                                       "en": "gold pieces"
                                       },
                                "MS": {"de": "Mithrilst�cke",
                                       "en": "mithril pieces"
                                       },
                                "Ed": {"de": "Edelsteine",
                                       "en": "gems"
                                       },
                                "Sch": {"de": "Schmuckst�cke",
                                        "en": "jewelry"
                                        }
                                }
             
        # Determine number of rolls
        roll = dice(100, 1)[0] 
    
        
        if 31 <= roll <= 55:
            nuor = 2
            
        elif 56 <= roll <= 75:
            nuor = 3
            
        elif 76 <= roll <= 90:
            nuor = 4
            
        elif 90 < roll:
            nuor = 5
            
        else:
            ##\var nuor
            # number of rolls
            nuor = 1
           
        ## \var table
        # table format: lower and upper limit of dice value, value category 1 to 5 result with value and unit
        table = ((( 1, 10), (  50, "ZS"), ( 500, "ZS"), (1000, "ZS"), (5000, "ZS"), (10000,"ZS")),
                 ((11, 20), ( 100, "ZS"), (1500, "ZS"), (3000, "ZS"), (7500, "ZS"), (5000, "KS")),
                 ((21, 30), ( 500, "ZS"), (2500, "ZS"), (5000, "ZS"), (1000, "KS"), (10000,"KS")),
                 ((31, 35), (1000, "ZS"), ( 500, "KS"), (1000, "KS"), (1750, "KS"), (1500, "BS")),
                 ((36, 40), (2000, "ZS"), ( 750, "KS"), (1500, "KS"), (2500, "KS"), (2000, "BS")),
                 ((41, 45), ( 300, "KS"), (1000, "KS"), (2000, "KS"), ( 400, "BS"), ( 250, "SS")),
                 ((46, 50), ( 400, "KS"), (1250, "KS"), ( 250, "BS"), ( 500, "BS"), ( 300, "SS")),
                 ((51, 55), ( 500, "KS"), ( 150, "BS"), ( 300, "BS"), ( 600, "BS"), ( 400, "SS")),
                 ((56, 60), ( 600, "KS"), ( 200, "BS"), ( 350, "BS"), (  70, "SS"), (  60, "GS")),
                 ((61, 65), (  70, "BS"), ( 250, "BS"), (  40, "SS"), (  90, "SS"), (  80, "GS")),
                 ((66, 70), (  80, "BS"), (  30, "SS"), (  50, "SS"), ( 110, "SS"), ( 100, "GS")),
                 ((71, 75), (  90, "BS"), (  35, "SS"), (  60, "SS"), (  15, "GS"), ( 125, "GS")),
                 ((76, 80), ( 100, "BS"), (  40, "SS"), (  70, "SS"), (  25, "GS"), ( 150, "GS")),
                 ((81, 85), (  12, "SS"), (  50, "SS"), (   8, "GS"), (  35, "GS"), (   2, "MS")),
                 ((86, 90), (  15, "SS"), (  60, "SS"), (  10, "GS"), (  45, "GS"), ( 250, "Ed")),
                 ((91, 94), (  20, "SS"), (   7, "GS"), (  15, "GS"), (  60, "Ed"), ( 300, "Ed")),
                 ((95, 97), (   3, "GS"), (   8, "GS"), (  20, "Ed"), (  80, "Ed"), ( 400, "Sch")),
                 ((98, 99), (   5, "GS"), (  10, "Ed"), (  50, "Ed"), (   1, "MS"), ( 600, "Sch")),
                 ((100, 100), (10 ,"Ed"), (  25,"Sch"), ( 100,"Sch"), ( 500,"Sch"), (1000, "Sch")))
    
        # determine Money nuor times
        for i in range(1, nuor+1):
            roll = dice(100, 1)[0]
            
            # look up amount
            for j in range(0, len(table)):
                
                if table[j][0][0] <= roll <= table[j][0][1]:
                    dummy = table[j][richness]
            # sum up amounts
            self.money[values[dummy[1]]][0] += dummy[0]

        del(dummy)
        
        ## \var nuov
        # create text listing the Money
        nuov = len(self.money)
        description = ""
        
        for i in range(0, nuov-2):
            
            if self.money[i][0] is not 0:
                description += "%s %s \n"%(str(self.money[i][0]),
                                           self.valueTranslation[self.money[i][1]][self.lang])
        
        for i in range(nuov-2, nuov):
            
            if self.money[i][0] != 0:
                description += "%s (%s)\n"%(self.valueTranslation[self.money[i][1]][self.lang],
                                            str(self.money[i][0]))
        
        return description
        
        
    
    # Determine magic items in treasure
    # input: richness = value category (1-5)
    # output: Text listing the magical items in the treasure
    
    def findItems(self, richness=3):
        '''
        Determine magic items in treasure.
        \param richness value category (1-5)
        \return Text listing the magical items in the treasures
        '''
        if richness not in range(1, 6):
    
            print("Error: Invalid value category! set value to default (3)")
            richness=3
        
        if self.lang not in self.supported:
            
            print('Error: Language not supported. Switch to default')
            self.lang = locale.getdefaultlocale()[0][:2]
            
            if self.lang not in self.supported:
            
                self.lang = 'en'

        ## \var nuortable Table for number of items
        # format: upper limit of dice value, value category 1 to 5 result
        nuortable = ((20, 0, 0, 0, 0, 2),
                     (40, 0, 0, 0, 1, 2),
                     (55, 0, 0, 1, 2, 2),
                     (70, 0, 1, 1, 2, 3),
                     (80, 0, 1, 2, 2, 3),
                     (90, 1, 1, 2, 3, 4),
                     (95, 1, 2, 3, 3, 4),
                     (98, 2, 3, 4, 4, 5),
                     (100,3, 3, 4, 5, 6))
    
        ## \var itemit Table of items in treasure
        # table format: lower and upper limit of dice value, value category 1 to 5 result
        itemit = ((( 1, 10), "normal", "normal", "normal",  "Gew80",   "Gew60"),
                  ((11, 20), "normal", "normal", "Gew80",   "Gew60",   "Gew40"),
                  ((21, 30), "normal", "Gew80",  "Gew60",   "Gew40",   "Spruch"),
                  ((31, 40), "Gew80",  "Gew60",  "Gew40",   "Bonus5",  "Spruch"),
                  ((41, 50), "Gew80",  "Gew60",  "Bonus5",  "Bonus10", "Spruch"),
                  ((51, 55), "Gew60",  "Bonus5", "Bonus5",  "Bonus10", "Bonus5"),
                  ((56, 60), "Gew60",  "Bonus5", "Bonus10", "Bonus15", "Bonus10"),
                  ((61, 65), "Bonus5", "Bonus5", "Bonus10", "Bonus15", "Bonus10"),
                  ((66, 70), "Bonus5", "Bonus5", "Bonus10", "Spruch",  "Bonus15"),
                  ((71, 75), "Bonus5", "Bonus10","Bonus15", "Spruch",  "Bonus20"),
                  ((76, 80), "Bonus5", "Bonus10","Spruch",  "Spruch",  "SV1"),
                  ((81, 85), "Bonus10","Bonus15","Spruch",  "Spruch",  "SV2"),
                  ((86, 90), "Bonus10","Spruch", "Spruch",  "SV1",     "MV2"),
                  ((91, 94), "Spruch", "Spruch", "SV1",     "SV2",     "SV3"),
                  ((95, 97), "Spruch", "SV1",    "SV2",     "MV2",     "MV3"),
                  ((98,100),"SV1",    "SV2",    "MV2",     "SV3",     "bes")
                  )
        
        itemTranslation =   {"normal": {"de": "normaler Gegenstand",
                                        "en": "normal item"
                                        },
                             "Gew80": {"de": "guter Gegenstand (80% Gewicht)",
                                       "en": "high quality item (80% weight)"
                                       },
                             "Gew60": {"de": "guter Gegenstand (60% Gewicht)",
                                       "en": "high quality item (60% weight)"
                                       },
                             "Gew40": {"de": "guter Gegenstand (40% Gewicht)",
                                       "en": "high quality item (40% weight)"
                                       },
                             "Bonus5": {"de": "magisch verbesserter Gegenstand (Bonus +5)",
                                        "en": "magical enhanced item (bouns +5)"
                                        },
                             "Bonus10": {"de": "magisch verbesserter Gegenstand (Bonus +10)",
                                         "en": "magical enhanced item (bonus +10)"
                                         },
                             "Bonus15": {"de": "magisch verbesserter Gegenstand (Bonus +15)",
                                         "en": "magical enhanced item (bonus +15)"
                                         },
                             "Bonus20": {"de": "magisch verbesserter Gegenstand (Bonus +20)",
                                         "en": "magical enhanced item (bonus +20)"
                                         },
                             "Spruch": {"de": "Gegenstand mit eingebettetem Zauberspruch",
                                        "en": "item with embedded spell"
                                       },
                             "SV1": {"de": "Spruchvermehrer +1",
                                     "en": "spell adder +1"
                                     },
                             "SV2": {"de": "Spruchvermehrer +2",
                                     "en": "spell adder +2"
                                     },
                             "SV3": {"de": "Spruchvermehrer +3",
                                     "en": "spell adder +3"
                                     },
                             "MV2": {"de": "Magiepunktevermehrer x2",
                                     "en": "power point multiplier x2"
                                     },
                             "MV3": {"de": "Magiepunktevermehrer x3",
                                     "en": "power point multiplier x3"
                                     },
                             "bes": {"de": "besonderer Gegenstand",
                                     "en": "special item"
                                     }
                            }
                                
        # Determine number of items
        roll = dice(100, 1)[0]
        
        for i in range(0, len(nuortable)):
            
            if roll <= nuortable[i][0]:
                nuor = nuortable[i][richness]
        
        # Determine items in treasure
        self.items = ""
        
        for i in range(0, nuor):
            roll = dice(100, 1)[0]
            
            dummy = itemit[0][richness]
    
            for j in range(0, len(itemit)):
                
                if itemit[j][0][0] <= roll <= itemit[j][0][1]:
                    dummy = itemit[j][richness]
            
            if "Spruch" in dummy:
                self.items += self.magicItem(0) + "\n"
            else:
                self.items += itemTranslation[dummy][self.lang] + "\n"
        
        del(dummy)
        return self.items
    
    
    #
    # Determine kind of magic item and the embedded spell
    #
    def magicItem(self, itype=0):
        '''
        Determine magic item with embedded spell
        \param itype item type. Manual dice roll result can be entered or numbers according to: 
                          0 random
                          40 Rune Paper
                          65 Potion
                          70 Daily I
                          75 Daily II
                          80 Daily III
                          85 Daily IV
                          94 Wand
                          98 Rod
                          99 Pole
        \return string with item description
        '''
        
        if self.lang not in self.supported:

            print('Error: Language not supported. Switch to default')
            self.lang = locale.getdefaultlocale()[0][:2]
            
            if self.lang not in self.supported:
            
                self.lang = 'en'
    
        ##
        # This holds the type of the magical item   
        itemTypes = {'1-40': {'de': 'Runenpapier',
                              'en': 'Rune paper'
                              },
                     '41-65': {'de': 'Trank',
                               'en': 'Potion'
                               },
                     '66-70': {'de': 'Schmuckstueck: Taeglich I',
                               'en': 'jewelry: Daily I'
                               },
                     '71-75': {'de': 'Schmuckstueck: Taeglich II',
                               'en': 'jewelry: Daily II'
                               },
                     '76-80': {'de': 'Schmuckstueck: Taeglich III',
                               'en': 'jewelry: Daily III'
                               },
                     '81-85': {'de': 'Schmuckstueck: Taeglich IV',
                               'en': 'jewelry: Daily IV'
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
        
        ##
        # This holds the level of the spell in an item    
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
        
        ##
        # This holds the realm of the spells   
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
        
        ##
        # This holds the spell list
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
        
      
        fcontent = ""
            
        if itype == 0:
            itype = dice(100, 1)[0]
        
        roll = dice(100, 3)
        
        for key1 in itemTypes.keys():
            dummy = key1.split('-')
        
            if int(dummy[0]) <= itype <= int(dummy[1]):
                item = itemTypes[key1]['de']
        
                if ':' in item:
                    item = item.rpartition(': ')[2]
                
                fcontent += itemTypes[key1][self.lang]
            
                if  item in loadedSpells.keys():
                    fcontent += " (" + str(dice(loadedSpells[item], 1)) + "/" + str(loadedSpells[item]) + ")"
                
                del(dummy)    
                break
            
        for key2 in spellRealms.keys():
            dummy = key2.split('-') 
            
            if int(dummy[0]) <= roll[0] <= int(dummy[1]):
                realm = spellRealms[key2]['de']
                fcontent += ", (" + spellRealms[key2][self.lang] + ")"
                del(dummy)
                break
            
        for key3 in spellLists.keys():
            dummy = key3.split('-')
            
            if int(dummy[0]) <= roll[1] <= int(dummy[1]):
                fcontent += ' ' + spellLists[key3][realm][self.lang] 
                del(dummy)
                break
            
        for key4 in spellLvl.keys():
            dummy = key4.split('-')
            
            if int(dummy[0]) <= roll[2] <= int(dummy[1]):
                fcontent += " [lvl " + spellLvl[key4][item] + "]\n"
                del(dummy)
                break        
    
        fcontent = fcontent[:-1]
        
        return fcontent
