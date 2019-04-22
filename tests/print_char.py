#!/usr/env python
import json
from pprint import pprint
import string

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
            
