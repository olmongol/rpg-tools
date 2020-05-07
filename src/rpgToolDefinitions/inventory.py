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
__updated__ = "07.05.2020"

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
          "worn": False,
          "worth" : money

         }

## \var gear
# A prototype dictionary for gear/equipment.

gear = {"name": "",
         "description" : "",
         "skill" : ""
         "bonus" : 0,
         "magical" : False,
         "weight" : 0,
         "skill" : "",
         "count" : 0,
         "worth" : money
        }

## \var gems
# prototype dictionary for gems and jewelary
gems = {"name" : "",
         "description",
         "weight" : 0,
         "worth" : money
         }


## \var potions
# prototype dictionary for magical potions or rune papers

potions = {"name": "",
            "description" : ""
            "spell" : "",
            "lvl" : "",
            "skill" : "",
            "realm" : "",
            "weight" : 0,
            "worth" : money
            }

## \var herbs
# prototype dictionary for herbs/ medical potions 

herbs = {"name" : "",
         "other name" :[],
         "type" : ""
         "lvl" : 0
         "found" : [],
         "description" : "",
         "medical use" :"",
         "other use" : "",
         "weight" : 0,
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
                 "worth" : money
                }

## \var daily_item
# prototype dictionary for daily items
daily_item = {"name" : "",
              "description" : "",
              "use times" : 0
              "spell" : "",
              "realm" : "",
              "lvl" : 0,
              "bonus" : 0,
              "weight" : 0,
              "worth" : money
             }

## \var wand
# prototype dictionary for staffs, wands and rods
wand = {"name" : "",
         "description" : "",
         "loads" : "",
         "max loads":,
         "spell" : "",
         "spellist":"",
         "realm" : "",
         "weight" : 0,
         "worth" : money
        }