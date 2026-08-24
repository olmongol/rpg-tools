#!/usr/bin/env python
"""!
\file magic.py
\package rpgToolDefinitions.magic
\brief definition of data structures for spell casting and magic actions.

\date (C) 2020-2021
@author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.5s

----
@todo - add magicpath to configuration
- add tablepath to configuration
"""
import os
import csv

__version__ = "0.5s"
__updated__ = "21.09.2021"

##@var magic_range_mod
# range motdication for spell casting
magic_range_mod = {0: 30,
                 10: 10,
                 50: 0,
                 100:-10,
                 300:-20,
                 10000000:-30
                 }
##@var situational_mods
# attack spell modification based on the situation
situation_mods = {"Full Cover":-20,
                 "Partial Cover":-10,
                 "Static Target":+10}
##@var magicpath
# the path from src directory where all the spell lists are saved as csv
magicpath = "data/default/magic/"



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


#---- spell list reader ----------------------------------------------------


def readMagicList(listname, spellname, datapath=None):
    """!
    Reads one profession spell-list CSV and returns all spells contained in
    it, plus the file name actually read.

    @param listname   name of the list sub-directory under data/default/magic,
                      e.g. 'Channeling_Open' or 'Base_List_Healer'
    @param spellname  spell file name, e.g. 'Barrier_Law' or 'Barrier_Law.csv'
    @param datapath   base character data directory (e.g. './data'); when
                      None, './data' is assumed.  The list CSV is expected at
                      <datapath>/default/magic/<listname>/<spellname>.csv
                      with fallbacks to <datapath>/magic and <datapath>
                      directly.
    @retval spells    list of dicts per spell with the file's columns
                      (Lvl as int, plus e.g. Spell, Area of Effect, Duration,
                      Range, Type, Description)
    @retval filename  absolute path of the CSV read ("" when not found)
    """
    if datapath is None:
        datapath = "./data"
    datapath = datapath.rstrip("/")

    spellfile = spellname if spellname.endswith(".csv") else spellname + ".csv"

    candidates = [
        os.path.join(datapath, "default", "magic", listname, spellfile),
        os.path.join(datapath, "magic", listname, spellfile),
        os.path.join(datapath, listname, spellfile),
    ]

    filename = ""
    for cand in candidates:
        if os.path.exists(cand):
            filename = os.path.abspath(cand)
            break

    spells = []
    if not filename:
        return spells, ""

    with open(filename, "r", newline="") as fp:
        reader = csv.reader(fp)
        rows = [row for row in reader if row and row[0].strip()]

    if len(rows) < 2:
        return spells, filename

    header = [h.strip() for h in rows[0]]

    for row in rows[1:]:
        record = {}
        for idx, key in enumerate(header):
            record[key] = row[idx].strip() if idx < len(row) else ""
        try:
            record["Lvl"] = int(record.get("Lvl", "0"))
        except ValueError:
            record["Lvl"] = 0
        spells.append(record)

    return spells, filename

