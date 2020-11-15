#!/usr/bin/env python
import json
from pprint import pprint

datadir="./data/default/fight/crits/"
tempdic = {"description": "",
           "initiative": 0,
            "hits": 0,
            "hits/rnd": 0,
            "kill": -1,
            "ko": -1,
            "mod attacker": 0,
            "mod foe": 0,
            "no parry": 0,
            "parry": 0,
            "stunned": 0,
           "damaged" : ""
            }

limits = ['5', '10', '15', '20', '35', '45', '50', '55', '60', '65', '66', '70', '75', '80', '85', '90', '95', '99', '100']
crits = ["A","B","C","D","E"]

def readJSON(filename):
    with open(filename,"r") as fp:
        cont = json.load(fp)
    return cont

def writeJSON(filename, cont):
    with open(filename,"w") as fp:
        json.dump(cont,fp,indent=4)

    print("{} saved".format(filename))
    
def editCont(fcont={},filename="test"):
    cont = dict.copy(fcont)
    
    if limits != list(cont.keys()):
        #cont = dict.fromkeys(limits,dict.fromkeys(crits,{}))
        cont = {}
        for l in limits:
            cont[l]={}
            for crit in crits:
                cont[l][crit]={}

    for dice in cont.keys():
        
        for crit in cont[dice].keys():
            
            if cont[dice][crit] == {}:
                cont[dice][crit]["default"]= dict.copy(tempdic)
                cont[dice][crit]["alternate"]=None
                
            for stat in cont[dice][crit].keys():
                
                if stat == "alternate" and cont[dice][crit]["alternate"]==None:
                    altn = input("alternate (j/N): ")
                                        
                    if altn in ["j","J","y","Y"]:
                        cont[dice][crit]["alternate"]= dict.copy(tempdic)
                        
                if cont[dice][crit][stat]:
                    
                    for param in cont[dice][crit][stat].keys():
                        
                        output ="{}/{}/{}/{}: {} => ".format(dice,crit,stat,param,cont[dice][crit][stat][param])
                   
                        enter = input(output)
                        
                        if enter!="":
                            cont[dice][crit][stat][param] = "{:s}".format(enter)

                       
                        
            writeJSON(datadir+filename,cont)            

        print("\n\n")

    
    return cont

#      krush = readJSON(datadir+"Krush.json")          
#      krush=editCont(krush,"Krush.json")  
