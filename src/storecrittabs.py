#!/usr/bin/env python
import json

def readJSON(filename):
    with open(filename,"r") as fp:
        cont = json.read(fp)
    return cont

def writeJSON(filename, cont):
    with open(filename,"w") as fp:
        json.dump(cont,fp,indent=4)

    print("{} saved".format(filename))
    
datadir="./data/default/fight/crits/"
tempdic = {"description": "",
            "hits": 0,
            "hits/rnd": 0,
            "kill": -1,
            "ko": -1,
            "mod attacker": 0,
            "mod foe": 0,
            "no parry": 0,
            "parry": 0,
            "stunned": 0
            }
