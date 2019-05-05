#!/usr/env python
import json
from pprint import pprint
import string
fpath="../src/data/default/latex/"
fnames=['template_charsheet.tex', 'template_trainpack.tex', 'template_test.tex', 'template_cats.tex', 'template_stats.tex', 'template_spells.tex', 'template_gen_info.tex', 'template_rr_at_db.tex', 'template_skills.tex']

class myDelimiter(string.Template):
    delimiter="==>"
##    idpattern = '[a-z]+_[a-z]+'

def readJSON(filename=""):
    cont = None
    
    if type(filename)==type("") and filename!="":

        with open(filename,"r") as fp:
            cont = json.load(fp)

    return cont

def readFile(filename=""):
    cont = None
    
    if type(filename)==type("") and filename!="":
        fp = open(filename,"r")
        cont = fp.read()
        fp.close()

    return cont

def saveFile(filename="",cont=""):
    if filename!="" and type(filename)==type(""):
        fp = open(filename,"w")
        fp.write(cont)
        fp.close()
        print("{} was saved.".format(filename))
        
def buildStatsTable(char={}):
    """
    This builds a replacement table for stats from character data to use with
    the LaTeX templates
    \param char a dictionary holding all the character's data from a JSON file.
    \return a dictionary holding the replacement stats table data
    """
    rpl_table={}
    attr=["Ag","Co","Me","Re","SD","Em","In","Pr","Qu","St"]
    a_type = list(char["Ag"].keys())

    if "name" in a_type:
        a_type.remove("name")

    if type(char) == type({}) and char!={}:

        for stat in attr:

            for s_type  in a_type:
                rpl_table[stat+"_"+s_type]=char[stat][s_type]

    return rpl_table
        
def buildRRTable(char={}):
    """
    This builds a replacement table for RR from character data to use with the LaTeX
    templates.
    \param char a dictionary holding the character data
    \return a dictionary holding the replacement RR table data
    """
    
    rpl_table={'ThreeQ':3*char['Qu']['total']}
    rr = []
    for elem in list(char.keys()):
        if "RR" in elem:
            print("{} -> {}".format(elem,char[elem]))
            rpl_table[str(elem.replace("/","_"))] = char[elem]

    return rpl_table
            
def buildGenTable(char={},latexpath="./"):
    """
    """
    entries = ["prof","race","culture","hometown","lord","parents","siblings", \
               "partner","children","deity","gender","skin","eyes","hair","size",\
               "weight","apparentage","actualage","looking","souldeparture",\
               "recovery","lvl","jpg","description","motivation","realm","exp","name"]
    rpl_table = {}
    for elem in entries:
        if elem in list(char.keys()):
            rpl_table[str(elem)]=str(char[elem])
        elif elem == "jpg":
            rpl_table[str(elem)] = latexpath+"default.jpg"
        else:
            rpl_table[str(elem)] = " "

    return rpl_table

def buildCatSkill(char={}):
    """
    """
    colors = {"Weapon" : "Red",
              "Magic": "Blue",
              "Develop" : "Green",
              "Standard" : "Black"
              }
    table_line = "\textcolor{==>color}{==>cat} & \textcolor{==>color}{==>Skill} & \textcolor{==>color}{==>rank} & " + \
                 "\textcolor{==>color}{==>rank_bonus ==>prof_bonus} & \textcolor{==>color}{==>spec_bonus} & " +\
                 "\textcolor{==>color}{==>item_bonus} &\textcolor{==>color}{total_bonus}"
    tpl = myDelimiter(table_line)
    output_tbl = ""
    
    for cat in list(char["cat"].keys()):
        if "Weapon" in cat:
            color = colors["Weapon"]

        elif "Development" in cat:
            color = colors["Develop"]
            
        elif "Spell" in cat or "Power" in cat:
            color = colors["Magic"]

        else:
            color = colors["Standard"]
          
        if cat not in ["Progression"]:
           
            rplm = {"Skill": "",
                    "cat": cat,
                    "rank": char["cat"][cat]["rank"],
                    "rank_bonus" : char["cat"][cat]["rank bonus"],
                    "spec_bonus" : char["cat"][cat]["spec bonus"],
                    "item_bonus" : char["cat"][cat]["item bonus"],
                    "total_bonus": char["cat"][cat]["total bonus"],
                    "color": color
                    }
            if "prof bonus" in list(char["cat"][cat].keys()):
                rplm["prof_bonus"]=char["cat"][cat]["prof bonus"]
            else:
                rplm["prof_bonus"]= "--"
                
            output_tbl += tpl.safe_substitute(rplm)
        
        for skill in list(char["cat"][cat]["Skill"].keys()):
            print("{} : {} --> \n\t{} : {}".format(cat,skill,char["cat"][cat],char["cat"][cat]["Skill"][skill]))
            if skill not in ["Progression"]:
                rplm ={
                        "Skill": skill,
                        "cat": "--",
                        "rank": char["cat"][cat]["Skill"][skill]["rank"],
                        "rank_bonus" : char["cat"][cat]["Skill"][skill]["rank bonus"],
                        "prof_bonus" : "--",
                        "spec_bonus" : char["cat"][cat]["Skill"][skill]["spec bonus"],
                        "item_bonus" : char["cat"][cat]["Skill"][skill]["item bonus"],
                        "total_bonus": char["cat"][cat]["Skill"][skill]["total bonus"],
                        "color" : color
                    }
                output_tbl += tpl.safe_substitute(rplm)
                
    return output_tbl
        
def buildSkillTable(char={}):
    """
    """
    colors = {"Weapon" : "==>color",
              "Magic": "Blue",
              "Develop" : "Green",
              "Standard" : "Black"
              }
    table_line = "\textcolor{==>color}{==>skill} & \textcolor{==>color}{==>category} & \textcolor{==>color}{00} & \textcolor{==>color}{00} & \textcolor{==>color}{00} & \textcolor{==>color}{00} &\textcolor{==>color}{00}"
