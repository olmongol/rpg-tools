#!/usr/bin/env python
'''!
\file inventory.py
\package rpgToolDefinitions.inventory
\brief definition of data structures for character inventories.


\date (C) 2020-2021
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
__version__ = "1.0"
__updated__ = "28.12.2020"

## \var geartypes
# (dictionary) list of different type of equipment like armor, weapon, tool...
geartypes = {"en": ["clothes", "tool", "container", "food", "gear", "ammo", "outdoor", "light", "write", "trap", "rope", "magic", "service", "transport"],
            "de":["Kleidung", "Werkzeug", u"Behälter", "Nahrung", u"Ausrüstung", "Munition", "Outdoor", "Licht", "Schreibzeug", "Falle", "Seil", "magisch", "Dienst", "Transport" ]

            }
charged_item = {"de":["Runenpapier", "Zaubertrank", "Zauberstab (30 cm)", "Zauberstab (75 cm)", "Zauberstab (150 cm)"],
               "en": ["Rune Paper", "Potion", "Wand (1')", "Rod (2.5')", "Staff (5')"]}
## \var info_charged
# holds max number of loads  (idx 0) and cost(=value) per level of spell(=idx)
info_charged = {"rune": [1, 2, 10, 20, 30, 40, 60, 80, 100, 125, 150],
               "potion":[1, 5, 15, 30, 45, 60, 90, 120, 150, 200, 225],
               "wand":[10, 10, 30],
               "rod":[30, 40, 80, 120, 150, 200],
               "staff":[100, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800]
               }
charge_action = {"de": ["neu verzaubern", "aufladen"],
                 "en": ["newly enchant", "recharge"]}
##\var treeformat
# width of treeview columns
treeformat = {"item": 200,
             "name": 200,
             "comment": 450,
             "description":450,
             "AT":50,
             "prod. time":90,
             "height":70,
             "weight":70,
             "length":70,
             "cost": 70,
             "worth": 90,
             "near":50,
             "shortc":40,
             "short":60,
             "medium":60,
             "long":60,
             "extreme":60,
             "type":100,
             "wtype":100,
             "mtype":100,
             "breakage":100,
             "strength":100,
             "fumble": 100,
             "ID": 40,
             "magic": 40,
             "mithril": 40,
             "slaying": 100,
             "holy": 40,
             "OB":50,
             "man bonus":60,
             "capacity":100,
             "mi/hr":50,
             "ft/rnd":50,
             "AF":30,
             "climate":70,
             "difficulty":80,
             "form":80,
             "prep":70,
             "lvl":30,
             "effect":300,
             "medical use":400,
             "other use": 200,
             "capacity": 40,
             "volume": 40,
             "bonus":50,
             "skill":300,
             "area":70,
             }
##\var char_inv_tv
# header for character's armor for treeview display
# @todo has to be fully filled
char_inv_tv = {"armor": ["name", "description", "AT", "weight", "worth"],
               "weapon": ["name", "description", "bonus", "breakage", "weight", "magic", "mithril", 'slaying', "holy", "worth"],
               "services":["name", "description", "weight", "worth"],
               "gems": ["name", "description", "weight", "worth"],
               "gear": ["name", "description", "weight", "capacity", "volume", "bonus", "skill", "worth"],
               "transport":["name", "description", "height", "weight", "capacity", "OB", "worth"],
               "herbs":["name", "type", "lvl", "description", "medical use", "other use", "worth"],
#               "runes" :[],
#               "constant item" :[],
#               "daily item" :[],
               }

perm_item = {"spell adder":{"+0":0,
                             "+1":50,
                             "+2": 100,
                             "+3": 200,
                             "+4": 400
                             },
             "pp mult":{"x1":0,
                         "x2": 200,
                         "x3": 400,
                         }
            }

## \var money
# This dictionary holds the different coins available

money = {"mithril": 0,
         "platinium": 0,
         "gold": 0,
         "silver": 0,
         "bronze": 0,
         "copper": 0,
         "tin": 0,
         "iron": 0
        }

coins = {'long': ["mithril", "platinium", "gold", "silver", "bronze", "copper", "tin", "iron"],
         'short': ["mp", "pp", "gp", "sp", "bp", "cp", "tp", "ip"]}

## \var weapon
# A dictonary holding all information that are needed for a single weapon.
weapon = {"name": "",
          "description": "",
          "bonus": 0,
          "magic": False,
          "mithril": False,
          "slaying": "",
          "holy": False,
          "skill": "",
          "table": "",
          "crit": [],
          "weight": 0,
          "length": "",
          "breakage": "",
          "fumble": "",
          "strength": "",
          "soft/wooden": "",
          "near": "---",
          "short": "---",
          "medium": "---",
          "long": "---",
          "extreme": "---",
          "location": "equipped",
          "worth": money.copy()
         }

## \var amor
# A dictonary holding all information about a a piece of armor

armor = {"name": "",
          "description": "",
          "material": "",
          "AT": 1,
          "covers": [],
          "weight": 0,
          "bonus": 0,
          "magic": False,
          "skill": "",
          "bonus DB":0,
          "bonus man": 0,
          "bonus OB": 0,
          "location": "equipped",
          "worth": money.copy()

         }

## \var gear
# A prototype dictionary for gear/equipment.

gear = {"name": "",
         "description": "",
         "skill": "",
         "bonus": 0,
         "magic": False,
         "weight": 0,
         "skill": "",
         "count": 0,
         "type": "",
         "capacity":"",
         "volume":"",
         "type":"",
         "location": "equipped",
         "worth": money.copy()
        }

## \var gems
# prototype dictionary for gems and jewelery
gems = {"name": "",
         "description":"",
         "weight": 0,
         "location": "equipped",
         "magic":False,
#         "realm":"",
#         "spell": "",
#         "lvl":0,
#         "spell list":"",
#         "loads":0,
#         "max loads":0,
#         "bonus":0,
         "worth": money.copy()
         }

## \var runes
# prototype dictionary for magical potions or rune papers

runes = {"name": "",
        "description": "",
        "type": "",  #potion,rune paper, rod, wand,staff
        "spell": "",
        "lvl": "",
        "loads":1,
        "max loads":1,
        "skill": "",
        "realm": "",
        "weight": 0,
        "location": "",
        "worth": money.copy()
        }

## \var herbs
# prototype dictionary for herbs/ medical potions

herbs = {"name": "",
         "other name":[],
         "type": "",
         "lvl": 0,
         "found": [],
         "description": "",
         "medical use":"",
         "other use": "",
         "weight": 0.1,
         "location": "equipped",
         "worth": money.copy()
         }

## \var constant_item
# prototype dictionary for constant magic items like PP Muliplier, spell adder

constant_item = {"name": "",
                 "description": "",
                 "spell": "",
                 "realm": "",
                 "lvl": 0,
                 "weight": 0,
                 "add spell": 0,
                 "pp mult": 0,
                 "location": "equipped",
                 "worth": money.copy()
                }

## \var daily_item
# prototype dictionary for daily items
daily_item = {"name": "",
              "description": "",
              "daily": 0,
              "spell list":"",
              "spell": "",
              "realm": "",
              "lvl": 0,
              "bonus": 0,
              "weight": 0,
              "location": "",
              "worth": money.copy()
             }

transport = {"name":"",
            "description":"",
            "magic":False,
            "bonus": 0,
            "skill":"",
            "worth": money.copy()}

services = {"name": "",
            "description":"",
            "location":"equipped"}
