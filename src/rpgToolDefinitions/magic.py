#!/usr/bin/env python
'''!
\file magic.py
\package rpgToolDefinitions.magic
\brief definition of data structures for spell casting and magic actions.


\date (C) 2020-2021
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "28.12.2020"

magic_range_mod = {0: 30,
                 10: 10,
                 50: 0,
                 100:-10,
                 300:-20,
                 10000000:-30
                 }

situation_mods = {"Full Cover":-20,
                 "Partial Cover":-10,
                 "Static Target":+10}



def readBasicTable(filename = "./data/default/tables/basic_spell_table.csv"):
    """!
    This reads the basic spell csv and converts it to an internal dictionary structure
    @param filename path+name of the basic spell table
    @retval table dictionary holding CSV as dictionary table
    """
    fp = open(filename, "r")
    cont = fp.read()
    fp.close()

    table = {}
    cont = cont.split("\n")
    header = cont[0].split(",")

    for key in header:
        table[key] = []

    for row in range(1, len(cont)):
        if cont[row] != "":
            for column in range(0, len(header)):
                table[header[column]].append(cont[row].split(",")[column])

    return table

