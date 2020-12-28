#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''!
\file treasure.py
\package rpgtoolbox


\date (C) 2017-2010
\author Marcus Schwamberger, Aiko Ruprecht
\email marcus@lederzeug.de
\version 1.0
\license GNU v3
'''

import locale
from rpgtoolbox.rpgtools import dice
from rpgtoolbox.lang import *
__updated__ = "28.12.2020"



class treasure():
    '''
    Creation of a treasure using the MERP/MERS tables to create a random treasure.
    '''


    def __init__(self, lang = ''):
        """!
        Class constructor treasure
        \param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        """

        ##\var supported list of supported languages
        # Keys are determined according to lang.py
        self.supported = list(supportedrpg.keys())

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
        dummy = trhelptext['description'][self.lang]
        dummy += 'ttype: ' + trhelptext['ttype'][self.lang]
        dummy += 'output: ' + trhelptext['output'][self.lang]

        print(dummy)
        del (dummy)


    def findTreasure(self, ttype = 3, output = "screen"):
        '''!
        Determine contents of one or several treasures and create a description of the contents.
        Details are listed in function help
        \param ttype Number or keyword of the category of the treasure
        \param output Options: screen, Name of the output file
        \param lang Language of the output text
        \return Array of strings listing money and magic items in the treasures
        '''
        if self.lang not in self.supported:
            print('Error: Language not supported. Switch to default')
            self.lang = locale.getdefaultlocale()[0][:2]
            if self.lang not in self.supported:
                self.lang = 'en'

        if ttype == "precious":
            return "Ring!"

        try:
            treasuretype = trtypelist[self.lang].index(ttype) + 1
        except:
            try:
                treasuretype = trtypelist['num'].index(ttype) + 1
            except:
                print("Error: Invalid value category! Set value to default (normal)")
                treasuretype = 3

        # Generate complete text
        fcontent = ["*** %s ***\n" % (trheader[self.lang])]
        fcontent += self.findMoney(treasuretype)
        fcontent += self.findItems(treasuretype)

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
                print((screenmesg['file_saved'][self.lang][:-2] + ': ' + output))
                return(fcontent)

            except:
                print('Error: invalid file name')
                return("")


    def findMoney(self, richness = 3):
        '''!
        Function to determine amount of Money in treasure
        \param richness value category (1-5)
        \return array of strings holding the treasured Money
        '''
        if richness not in list(range(1, 6)):

            print("Error: Invalid value category! Set value to default (normal)")
            richness = 3

        if self.lang not in self.supported:

            print('Error: Language not supported. Switch to default')
            self.lang = locale.getdefaultlocale()[0][:2]

            if self.lang not in self.supported:

                self.lang = 'en'

        ##\var money list of amount and value of coins and valuables
        #total amount listed for the different values
        self.money = [[0, "ZS"], [0, "KS"], [0, "BS"], [0, "SS"], [0, "GS"], [0, "MS"], [0, "Ed"], [0, "Sch"]]

        values = {"ZS":0, "KS":1, "BS":2, "SS":3, "GS":4, "MS": 5, "Ed":6, "Sch":7}

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
        table = (((1, 10), (50, "ZS"), (500, "ZS"), (1000, "ZS"), (5000, "ZS"), (10000, "ZS")),
                 ((11, 20), (100, "ZS"), (1500, "ZS"), (3000, "ZS"), (7500, "ZS"), (5000, "KS")),
                 ((21, 30), (500, "ZS"), (2500, "ZS"), (5000, "ZS"), (1000, "KS"), (10000, "KS")),
                 ((31, 35), (1000, "ZS"), (500, "KS"), (1000, "KS"), (1750, "KS"), (1500, "BS")),
                 ((36, 40), (2000, "ZS"), (750, "KS"), (1500, "KS"), (2500, "KS"), (2000, "BS")),
                 ((41, 45), (300, "KS"), (1000, "KS"), (2000, "KS"), (400, "BS"), (250, "SS")),
                 ((46, 50), (400, "KS"), (1250, "KS"), (250, "BS"), (500, "BS"), (300, "SS")),
                 ((51, 55), (500, "KS"), (150, "BS"), (300, "BS"), (600, "BS"), (400, "SS")),
                 ((56, 60), (600, "KS"), (200, "BS"), (350, "BS"), (70, "SS"), (60, "GS")),
                 ((61, 65), (70, "BS"), (250, "BS"), (40, "SS"), (90, "SS"), (80, "GS")),
                 ((66, 70), (80, "BS"), (30, "SS"), (50, "SS"), (110, "SS"), (100, "GS")),
                 ((71, 75), (90, "BS"), (35, "SS"), (60, "SS"), (15, "GS"), (125, "GS")),
                 ((76, 80), (100, "BS"), (40, "SS"), (70, "SS"), (25, "GS"), (150, "GS")),
                 ((81, 85), (12, "SS"), (50, "SS"), (8, "GS"), (35, "GS"), (2, "MS")),
                 ((86, 90), (15, "SS"), (60, "SS"), (10, "GS"), (45, "GS"), (250, "Ed")),
                 ((91, 94), (20, "SS"), (7, "GS"), (15, "GS"), (60, "Ed"), (300, "Ed")),
                 ((95, 97), (3, "GS"), (8, "GS"), (20, "Ed"), (80, "Ed"), (400, "Sch")),
                 ((98, 99), (5, "GS"), (10, "Ed"), (50, "Ed"), (1, "MS"), (600, "Sch")),
                 ((100, 100), (10 , "Ed"), (25, "Sch"), (100, "Sch"), (500, "Sch"), (1000, "Sch")))

        # determine Money nuor times
        for i in range(1, nuor + 1):
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
        description = []

        for i in range(0, nuov - 2):

            if self.money[i][0] is not 0:
                description.append("%s %s" % (str(self.money[i][0]),
                                           valueTranslation[self.money[i][1]][self.lang]))

        for i in range(nuov - 2, nuov):

            if self.money[i][0] != 0:
                description.append("%s (%s)" % (valueTranslation[self.money[i][1]][self.lang],
                                            str(self.money[i][0])))

        return description

    # Determine magic items in treasure
    # input: richness = value category (1-5)
    # output: Text listing the magical items in the treasure


    def findItems(self, richness = 3):
        '''!
        Determine magic items in treasure.
        \param richness value category (1-5)
        \return Text listing the magical items in the treasures
        '''
        if richness not in list(range(1, 6)):

            print("Error: Invalid value category! set value to default (3)")
            richness = 3

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
                     (100, 3, 3, 4, 5, 6))

        ## \var itemit Table of items in treasure
        # table format: lower and upper limit of dice value, value category 1 to 5 result
        itemit = (((1, 10), "normal", "normal", "normal", "Gew80", "Gew60"),
                  ((11, 20), "normal", "normal", "Gew80", "Gew60", "Gew40"),
                  ((21, 30), "normal", "Gew80", "Gew60", "Gew40", "Spruch"),
                  ((31, 40), "Gew80", "Gew60", "Gew40", "Bonus5", "Spruch"),
                  ((41, 50), "Gew80", "Gew60", "Bonus5", "Bonus10", "Spruch"),
                  ((51, 55), "Gew60", "Bonus5", "Bonus5", "Bonus10", "Bonus5"),
                  ((56, 60), "Gew60", "Bonus5", "Bonus10", "Bonus15", "Bonus10"),
                  ((61, 65), "Bonus5", "Bonus5", "Bonus10", "Bonus15", "Bonus10"),
                  ((66, 70), "Bonus5", "Bonus5", "Bonus10", "Spruch", "Bonus15"),
                  ((71, 75), "Bonus5", "Bonus10", "Bonus15", "Spruch", "Bonus20"),
                  ((76, 80), "Bonus5", "Bonus10", "Spruch", "Spruch", "SV1"),
                  ((81, 85), "Bonus10", "Bonus15", "Spruch", "Spruch", "SV2"),
                  ((86, 90), "Bonus10", "Spruch", "Spruch", "SV1", "MV2"),
                  ((91, 94), "Spruch", "Spruch", "SV1", "SV2", "SV3"),
                  ((95, 97), "Spruch", "SV1", "SV2", "MV2", "MV3"),
                  ((98, 100), "SV1", "SV2", "MV2", "SV3", "bes")
                  )

        # Determine number of items
        roll = dice(100, 1)[0]

        for i in range(0, len(nuortable)):

            if roll <= nuortable[i][0]:
                nuor = nuortable[i][richness]

        # Determine items in treasure
        self.items = []

        for i in range(0, nuor):
            roll = dice(100, 1)[0]

            dummy = itemit[0][richness]

            for j in range(0, len(itemit)):

                if itemit[j][0][0] <= roll <= itemit[j][0][1]:
                    dummy = itemit[j][richness]

            if "Spruch" in dummy:
                self.items.append(self.magicItem(0))
            else:
                self.items.append(itemTranslation[dummy][self.lang])

        del(dummy)
        return self.items


    #
    # Determine kind of magic item and the embedded spell
    #
    def magicItem(self, itype = 0):
        '''!
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
        # This holds the level of the spell in an item
        spellLvl = {'1-20': {'Rune Paper':'1',
                             'Potion':'1',
                             'Daily I':'1',
                             'Daily II':'1',
                             'Daily III':'1',
                             'Daily IV':'1',
                             'Wand':'1',
                             'Rod':'1',
                             'Pole':'1'
                             },
                    '21-25': {'Rune Paper':'2',
                             'Potion':'1',
                             'Daily I':'1',
                             'Daily II':'1',
                             'Daily III':'1',
                             'Daily IV':'1',
                             'Wand':'1',
                             'Rod':'1',
                             'Pole':'2'
                             },
                    '26-30':{'Rune Paper':'2',
                             'Potion':'1',
                             'Daily I':'1',
                             'Daily II':'1',
                             'Daily III':'1',
                             'Daily IV':'1',
                             'Wand':'1',
                             'Rod':'1',
                             'Pole':'2'
                             },
                    '31-35':{ 'Rune Paper':'2',
                             'Potion':'2',
                             'Daily I':'1',
                             'Daily II':'1',
                             'Daily III':'1',
                             'Daily IV':'1',
                             'Wand':'1',
                             'Rod':'1',
                             'Pole':'3'
                             },
                    '36-40': {'Rune Paper':'2',
                             'Potion':'2',
                             'Daily I':'2',
                             'Daily II':'1',
                             'Daily III':'1',
                             'Daily IV':'1',
                             'Wand':'1',
                             'Rod':'2',
                             'Pole':'3'
                             },
                    '41-45': {'Rune Paper':'3',
                             'Potion':'2',
                             'Daily I':'2',
                             'Daily II':'2',
                             'Daily III':'1',
                             'Daily IV':'1',
                             'Wand':'1',
                             'Rod':'2',
                             'Pole':'4'
                             },
                    '46-50': {'Rune Paper':'3',
                             'Potion':'2',
                             'Daily I':'2',
                             'Daily II':'2',
                             'Daily III':'2',
                             'Daily IV':'1',
                             'Wand':'1',
                             'Rod':'2',
                             'Pole':'4'
                             },
                    '51-55': {'Rune Paper':'3',
                             'Potion':'2',
                             'Daily I':'3',
                             'Daily II':'2',
                             'Daily III':'2',
                             'Daily IV':'1',
                             'Wand':'1',
                             'Rod':'2',
                             'Pole':'5'
                             },
                    '56-60': {'Rune Paper':'4',
                             'Potion':'3',
                             'Daily I':'3',
                             'Daily II':'2',
                             'Daily III':'2',
                             'Daily IV':'2',
                             'Wand':'2',
                             'Rod':'3',
                             'Pole':'5'
                             },
                    '61-65': {'Rune Paper':'4',
                             'Potion':'3',
                             'Daily I':'3',
                             'Daily II':'3',
                             'Daily III':'2',
                             'Daily IV':'2',
                             'Wand':'2',
                             'Rod':'3',
                             'Pole':'6'
                             },
                    '66-70': {'Rune Paper':'4',
                             'Potion':'3',
                             'Daily I':'4',
                             'Daily II':'3',
                             'Daily III':'2',
                             'Daily IV':'2',
                             'Wand':'2',
                             'Rod':'3',
                             'Pole':'7'
                             },
                    '71-75': {'Rune Paper':'5',
                             'Potion':'4',
                             'Daily I':'4',
                             'Daily II':'3',
                             'Daily III':'2',
                             'Daily IV':'2',
                             'Wand':'2',
                             'Rod':'3',
                             'Pole':'7'
                             },
                    '76-80': {'Rune Paper':'5',
                             'Potion':'4',
                             'Daily I':'5',
                             'Daily II':'4',
                             'Daily III':'3',
                             'Daily IV':'2',
                             'Wand':'2',
                             'Rod':'4',
                             'Pole':'7'
                             },
                    '81-85': {'Rune Paper':'6',
                             'Potion':'5',
                             'Daily I':'5',
                             'Daily II':'4',
                             'Daily III':'3',
                             'Daily IV':'2',
                             'Wand':'2',
                             'Rod':'4',
                             'Pole':'8'
                             },
                    '86-90': {'Rune Paper':'7',
                             'Potion':'6',
                             'Daily I':'6',
                             'Daily II':'5',
                             'Daily III':'3',
                             'Daily IV':'3',
                             'Wand':'2',
                             'Rod':'4',
                             'Pole':'8'
                             },
                    '91-94': {'Rune Paper':'8',
                             'Potion':'7',
                             'Daily I':'7',
                             'Daily II':'5',
                             'Daily III':'4',
                             'Daily IV':'3',
                             'Wand':'2',
                             'Rod':'5',
                             'Pole':'9'
                             },
                    '95-97': {'Rune Paper':'9',
                             'Potion':'8',
                             'Daily I':'8',
                             'Daily II':'6',
                             'Daily III':'4',
                             'Daily IV':'3',
                             'Wand':'2',
                             'Rod':'5',
                             'Pole':'9'
                             },
                    '98-99': {'Rune Paper':'10',
                             'Potion':'9',
                             'Daily I':'9',
                             'Daily II':'7',
                             'Daily III':'5',
                             'Daily IV':'3',
                             'Wand':'2',
                             'Rod':'5',
                             'Pole':'10'
                             },
                    '100-100': { 'Rune Paper':'10',
                                 'Potion':'10',
                                 'Daily I':'10',
                                 'Daily II':'7',
                                 'Daily III':'5',
                                 'Daily IV':'3',
                                 'Wand':'2',
                                 'Rod':'5',
                                 'Pole':'10'
                               },
                    }

        # This holds the number of loaded spells in an item
        loadedSpells = {'Wand': 10,
                       'Rod': 30,
                       'Pole': 100
                       }

        # Generate content of treasure
        fcontent = ""

        if itype == 0:
            itype = dice(100, 1)[0]

        roll = dice(100, 3)

        for key1 in list(itemTypes.keys()):
            dummy = key1.split('-')

            if int(dummy[0]) <= itype <= int(dummy[1]):
                item = itemTypes[key1]['en']

                if ':' in item:
                    item = item.rpartition(': ')[2]

                fcontent += itemTypes[key1][self.lang]

                if  item in list(loadedSpells.keys()):
                    fcontent += " (" + str(dice(loadedSpells[item], 1)) + "/" + str(loadedSpells[item]) + ")"

                del(dummy)
                break

        for key2 in list(spellRealms.keys()):
            dummy = key2.split('-')

            if int(dummy[0]) <= roll[0] <= int(dummy[1]):
                realm = spellRealms[key2]['en']
                fcontent += ", (" + spellRealms[key2][self.lang] + ")"
                del(dummy)
                break

        for key3 in list(spellLists.keys()):
            dummy = key3.split('-')

            if int(dummy[0]) <= roll[1] <= int(dummy[1]):
                fcontent += ' ' + spellLists[key3][realm][self.lang]
                del(dummy)
                break

        for key4 in list(spellLvl.keys()):
            dummy = key4.split('-')

            if int(dummy[0]) <= roll[2] <= int(dummy[1]):
                fcontent += " [lvl " + spellLvl[key4][item] + "]"
                del(dummy)
                break

        fcontent = fcontent.strip()

        return fcontent
