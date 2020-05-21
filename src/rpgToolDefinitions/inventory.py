#!/usr/bin/env python
'''
\file inventory.py
\package rpgToolDefinitions.inventory
\brief definition of data structures for character inventories.


\date (C) 2020
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "21.05.2020"

## \var geartypes
# (dictionary) list of different type of equippment like armor, weapon, tool...
geartypes = {"en": ["clothes", "tool", "container", "food", "equippment"],
            "de" :["Kleidung", "Werkzeug", u"Behälter", "Nahrung", u"Ausrüstung"]
            }
##\var treeformat
# width of treeview columns
treeformat = {"item" : 200,
             "name" : 200,
             "comment" : 450,
             "description":450,
             "AT" :50,
             "prod. time":90,
             "weight":70,
             "cost" : 70,
             "worth": 70,
             "short":50,
             "type":80,
             "breakage":100,
             "strength":100,
             "fumble": 100,
             "ID" : 40,
             "magic" : 40,
             "mithril": 40,
             "slaying" : 100,
             "holy" : 40,
             "OB" :50,
             "man bonus" :60,
             "height/weight" : 100,
             "capacity":100,
             "mi/hr":50,
             "ft/rnd":50
             }
##\var char_inv_tv
# header for character's armor for treeview display
# @todo has to be fully filled
char_inv_tv = {"armor" : ["name", "description", "AT", "weight", "worth"],
               "weapon" : ["name", "description", "bonus", "breakage", "weight", "magic", "mithril", 'slaying', "holy", "worth"],
               "services" :["name", "description", "weight", "worth"],
               "gems" : ["name", "description", "weight", "worth"],
               "gear" : ["name", "description", "weight", "worth"],
               "transport" :["name", "description", "weight", "worth"],
               "herbs" :[],
               "runes" :[],
               "constant item" :[],
               "daily item" :[],
               }

## \var money
# This dictionary holds the different coins available

money = {"mithril" : 0,
         "platinium" : 0,
         "gold": 0,
         "silver" : 0,
         "bronze" : 0,
         "copper" : 0,
         "tin" : 0,
         "iron" : 0
        }

## \var weapon
# A dictonary holding all information that are needed for a single weapon.
weapon = {"name" : "",
          "description" : "",
          "bonus" : 0,
          "magic" : False,
          "mithril" : False,
          "slaying" : "",
          "holy" : False,
          "skill" : "",
          "table" : "",
          "crit" : [],
          "weight" : 0,
          "breakage": 0,
          "fumble" : 4,
          "strength" : 0,
          "soft/wooden" : 0,
          "location" : "",
          "range mod" :[],
          "worth" : money
         }

## \var amor
# A dictonary holding all information about a a piece of armor

armor = {"name": "",
          "description" : "",
          "material" : "",
          "AT" : 1,
          "covers" : [],
          "weight" : 0,
          "bonus" : 0,
          "skill" : "",
          "bonus DB" :0,
          "bonus man": 0,
          "bonus OB": 0,
          "location" : "",
          "worth" : money

         }

## \var gear
# A prototype dictionary for gear/equipment.

gear = {"name": "",
         "description" : "",
         "skill" : "",
         "bonus" : 0,
         "magical" : False,
         "weight" : 0,
         "skill" : "",
         "count" : 0,
         "type" : "",
         "worth" : money
        }

## \var gems
# prototype dictionary for gems and jewelery
gems = {"name" : "",
         "description":"",
         "weight" : 0,
         "location" : "",
         "worth" : money
         }

## \var runes
# prototype dictionary for magical potions or rune papers

runes = {"name": "",
            "description" : "",
            "type" : "",  #potion,rune paper, rod, wand,staff
            "spell" : "",
            "lvl" : "",
            "loads":1,
            "max loads":1,
            "skill" : "",
            "realm" : "",
            "weight" : 0,
            "location" : "",
            "worth" : money
            }

## \var herbs
# prototype dictionary for herbs/ medical potions

herbs = {"name" : "",
         "other name" :[],
         "type" : "",
         "lvl" : 0,
         "found" : [],
         "description" : "",
         "medical use" :"",
         "other use" : "",
         "weight" : 0,
         "location" : "",
         "worth": money
         }

## \var constant_item
# prototype dictionary for constant magic items like PP Muliplier, spell adder

constant_item = {"name" : "",
                 "description" : "",
                 "spell" : "",
                 "realm" : "",
                 "lvl" : 0,
                 "weight" : 0,
                 "add spell" : 0,
                 "mult PP" : 0,
                 "location" : "",
                 "worth" : money
                }

## \var daily_item
# prototype dictionary for daily items
daily_item = {"name" : "",
              "description" : "",
              "use times" : 0,
              "spell" : "",
              "realm" : "",
              "lvl" : 0,
              "bonus" : 0,
              "weight" : 0,
              "location" : "",
              "worth" : money
             }

transport = {"name" :"",
            "description":"",
            "worth": money}

services = {"name" : "",
            "description":""}
