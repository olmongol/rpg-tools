#!/usr/bin/env python3
r'''!
\package rpgtoolbox.combatcore
\brief Monster/NPC combat data preparation and table management

Extracted from monstercreatorWin for separation of concerns.
Pure logic, no Tkinter dependencies.

@version 1.0
@date 2026-08-15
'''
__version__ = "1.0"
__updated__ = "2026-08-15"


import csv
import os
import shutil


def prepare_attack_data(weapon_list):
    """
    Prepares attack data from a weapon list into structured form
    for display and NPC handling.
    @param weapon_list: Raw weapon/attack data entries (list)
    @return (meleelist, missilelist, attacks)
    """
    meleelist = []
    missilelist = []
    attacks = {}
    magiclist = [
        "Fire Bolt", "Ice Bolt", "Lightning Bolt",
        "Shock Bolt", "Water Bolt", "Fire Ball", "Cold Ball"
    ]
    magicsc = ["Fb", "Ib", "Lb", "Sb", "Wb", "FB", "CB"]

    for w in weapon_list:
        if "wtype" not in w:
            continue

        if w["wtype"] not in ["th", "mis"]:
            meleelist.append(w.get("item", ""))

        if w["wtype"] in ["th", "mis"] or "th" in w.get("wtype", ""):
            missilelist.append(w.get("item", ""))

        item = w.get("item", "")
        shortc = w.get("shortc", "")
        attacks[item] = shortc

    for i, spell in enumerate(magiclist):
        attacks[spell] = magicsc[i]

    return meleelist, missilelist, attacks


def saveGMTable(gmtable_path, gmcontent, header=None):
    """
    Saves all data from the GM table to CSV.
    @param gmtable_path: Path to CSV file
    @param gmcontent: List of dict entries for NPCs/monsters
    @param header: Optional CSV fieldnames for DictWriter
    """
    oldpath = gmtable_path[:-4] + ".old" if gmtable_path.endswith(".csv") else gmtable_path + ".old"

    try:
        if os.path.exists(gmtable_path):
            shutil.copyfile(src=gmtable_path, dst=oldpath)
    except (IOError, OSError):
        pass

    # Remove doublets from content
    seen = set()
    unique_content = []
    for entry in gmcontent:
        name = entry.get("name", "")
        if name and name not in seen:
            seen.add(name)
            unique_content.append(entry)

    with open(gmtable_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header or list(gmcontent[0].keys()) if gmcontent else ["name"])
        writer.writeheader()
        writer.writerows(unique_content)


def loadGMTable(gmtablepath="/home/mongol/git/rpg-tools/data/nscs/default/gmtable.csv"):
    r"""!
    Loads the GM table from CSV.

    @param gmtablepath: Path to CSV file (default: gmtable.csv)
    @return (content, headers): List of dicts and field names
    """
    content = []
    if not gmtablepath or not os.path.isfile(gmtablepath):
        return content
    
    with open(gmtablepath, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames or []
        
        for row in reader:
            for field in headers:
                if not row[field]:
                    row[field] = 0
            content.append(row)
    
    return content, headers
