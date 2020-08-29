import json
import csv
from pprint import pprint
from rpgtoolbox.globaltools import readCSV
#from gui.spelleditor import readCSV
from rpgtoolbox.rpgtools import statManeuver as statMan
from rpgtoolbox.rpgtools import dice
from rpgToolDefinitions import inventory as inv
from rpgToolDefinitions.epcalcdefs import maneuvers as manmod
#from rpgToolDefinitions.inventory import coins

defaultpath="data/default/inventory/"
herbsfile = "herbs.csv"

herbs = readCSV(defaultpath+herbsfile)

def string2worth(worth = ""):
    '''
    This converts a string like "2gp 42cp" into a worth dictionary
    @param worth string that holds the worth like "3gp 65bp". Important: space is
    delimiter and the shorts have to be lower characters.
    '''
##    print(worth)
    result = inv.money.copy()
    value = worth.split(" ")
    
    for v in value:
        pos = 0
        pos = inv.coins["short"].index(v[-2:])
        result[inv.coins["long"][pos]] = int(v[:-2])

    return result

def sumDices(sides=4,number=1):
    """
    Rolls number D sides and returns the sum of the results
    @param sides of the dice to roll
    @param number of the dices to roll
    """
    result=0
    for r in dice(sides,number):
        result +=r

    return result


def findHerbs(roll=0,skill=-15,area="---",climate="mild temperate",locale=["---"]):
    """
    This function searches for herbs by area, climate and locale dependend on difficulty of
    finding and the success of the skill (foraging) roll.
    @param roll result of the dice roll
    @param skill total skill bonus for Foraging
    @param area local area where the herb might grow
    @param climate climate conditions
    @param locale local environment conditions like 'desert'
    @retval result list of dictionaries holding the found herbs
    """
    herbs = readCSV(defaultpath+herbsfile)
    result = []
    protoherb ={"name":"",
                "AF" : 0,
                "climate":"",
                "description":"",
                "worth":{},
                "difficulty":"",
                "medical use":"",
                "form":"",
                "locale":"",
                "lvl":0,
                "type":"",
                "area":"",
                "weight":0.1,
                "other use":"",
                "location": "equipped",
                "other name":[],
                "found":[]
            }
    
    statman = statMan()
    for plant in herbs:
        plant["name"]=plant.pop("item")
        plant["description"]=plant.pop("comment")
        plant["medical use"]=plant.pop("effect")
        plant["worth"]=plant.pop("cost")
        plant["worth"]=string2worth(plant["worth"])
        plant["weight"]=0.1
        plant["location"]="equipped"
        plant["other use"]=""
        plant["other name"]=[]
        
        
        if plant["area"] in [area,"everywhere"] and plant["climate"]==climate and plant["locale"]==locale:
            mod = manmod[plant["difficulty"]]["mod"]
            if roll != 100 and roll != 66:
                check = statman.checkRoll(roll+skill+mod)
            else:
                check = statman.checkRoll(roll)
##            pprint(check)
            
            if check["success"] == "1.0":
                no = 1
            elif check["success"] == "1.25":
                no = sumDices(5,1)
            elif check["success"] == "1.2":
                no = 2
            else:
                no=0

            for i in range(0,no):
                result.append(plant)

    return result
            
                
            

