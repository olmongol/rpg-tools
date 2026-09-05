#!/usr/bin/python3
'''!
\file epcalcwin_gui.py
\package gui.epcalcwin
\brief GUI for the EP calculator: experience points, maneuvers, spells and basic spell casting
This module provides the main EP calculation window (\c EPCalcWin) incl. a basic
spell-casting window driven by the basic spell table (magic.readBasicTable) and
resistance rolls (rpgtools.RRroll), plus the maneuver window (\c manWin) and the
group-EP display/helper class (\c showGrpEP).

\date (C) 2015-2026
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 1.3.0
----
\todo
- adding a cat/skill checker window for the whole group (select skill once and check for all)
'''
import os
import json
from gui.window import *
from rpgtoolbox import epcalc, rpgtools as rpg
from rpgtoolbox.rrwindow import *
from rpgToolDefinitions.epcalcdefs import maneuvers
from rpgtoolbox.rpgtools import  getLvl
from rpgToolDefinitions.helptools import RMDice as dice
from copy import deepcopy
from pprint import pprint
from tkinter import filedialog
import re
import pickle
from PIL import Image as _pilimg, ImageTk
from rpgtoolbox import logbox as log

logger = log.createLogger('global', 'debug', '1 MB', 1, './log' , 'epcalcwin.log')


class EPCalcWin(blankWindow):
    """!
    This is a GUI for EP calculation for your character party.
    """


    def __init__(self, lang = "en", charlist = None, storepath = "./data"):
        """!
        Class constructor
        @param lang The chosen language for window's and button's
                    texts. At the moment, only English (en, default
                    value) and German (de) are supported.
        @param charlist list of dictionaries holding: player, charname, EPs
        @param storepath path for storing the data into the character files.
        """

        self.lang = lang
        # BUG-FIX: charlist could be None instead of [], causing TypeError on iteration.
        # Guard against None to prevent crash at L114 (__buildWin).
        self.charlist = charlist if charlist is not None else []
        if self.charlist == []:
            self.charlist.append({  "player": "Marcus",
                                    "exp": 10000,
                                    "prof": "Ranger",
                                    "name": "Player1"
                                })
        self.storepath = storepath
        blankWindow.__init__(self, self.lang)
        self.window.title("EP Calculator")
        self.__addMenu()
        self.__addHelpMenu()
        self.__buildWin()
        self.__loadAutosave()
        self.window.mainloop()


    def __addMenu(self):
        '''!
        This methods adds the menu bar to the window
        '''
        self.filemenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['menu_file'][self.lang],
                              menu = self.filemenu)
        self.filemenu.add_command(label = submenu['file'][self.lang]['open'],
                                  command = self.__open)
        self.filemenu.add_command(label = submenu['file'][self.lang]['save'],
                                  command = self.__save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = submenu['file'][self.lang]['close'],
                                  command = self.__quit)


    def __addHelpMenu(self):
        """!
        This methods defines a help menu.
        """
        self.helpmenu = Menu(master = self.menu)
        self.menu.add_cascade(label = txtmenu['help'][self.lang],
                              menu = self.helpmenu)

        self.helpmenu.add_separator()
        self.helpmenu.add_command(label = submenu['help'][self.lang]['about'],
                                  command = self._helpAbout)


    def __buildWin(self):
        """!
        This method builds the window content.
        """
        # # \var self.players
        # list of given player names
        self.players = []
        # # \var self.group
        # dictionary of EP objects per player
        self.group = {}

        for elem in self.charlist:
            self.players.append(elem["player"])
            self.group[elem["player"]] = epcalc.experience(elem["player"], elem["exp"])
            self.group[elem["player"]].updateInfo()

        self.__selecPlayer = StringVar(self.window)
        self.__selecPlayer.set(self.players[0])

        self.__playerOpt = OptionMenu(self.window,
                                      self.__selecPlayer,
                                      *self.players,
                                      command = self.__updSelec)
        self.__playerOpt.grid(column = 0, row = 0, sticky = "W")

        self.__charname = StringVar()
        self.__charname.set(self.charlist[0]["name"])
        Label(self.window,
              width = 20,
              textvariable = self.__charname,
              ).grid(row = 0, column = 1, sticky = "W")

        self.__charprof = StringVar()
        self.__charprof.set("{} ({})".format(self.charlist[0]["prof"], self.group[self.charlist[0]["player"]].lvl))
        Label(self.window,
              width = 15,
              textvariable = self.__charprof,
              ).grid(row = 0, column = 2, sticky = "W")

        self.__charexp = StringVar()
        self.__charexp.set(str(self.charlist[0]["exp"]))
        Label(self.window,
              width = 15,
              textvariable = self.__charexp,
              ).grid(row = 0, column = 3, sticky = "W")

        self.__gained = StringVar()
        self.__gained.set("+{}".format(self.group[self.charlist[0]["player"]].gainedep))
        Label(self.window,
              width = 10,
              textvariable = self.__gained,
              ).grid(row = 0, column = 4, sticky = "W")

        self.__newep = StringVar()
        self.__newep.set("<{}>".format(self.group[self.charlist[0]["player"]].gainedep + self.group[self.charlist[0]["player"]].ep))
        Label(self.window,
              width = 10,
              textvariable = self.__newep,
              ).grid(row = 0, column = 5, sticky = "W")

        self.__newlvl = IntVar()
        self.__newlvl.set(self.group[self.charlist[0]["player"]].lvl)
        Label(self.window,
              width = 10,
              textvariable = self.__newlvl,
              ).grid(row = 0, column = 6, sticky = "EW")

        # row 1
        Label(self.window,
              text = s_elem_def['MANEUVER'][self.lang] + ":",
              ).grid(row = 1, column = 0, sticky = "EW")

        self.manlist = list(maneuvers.keys())
        if not self.manlist:
            logger.warning("No maneuvers available; using 'unavailable' as default!")
            self.manlist = ["unavailable"]
        self.__selecman = StringVar()
        self.__selecman.set(self.manlist[0])

        self.__manOpt = OptionMenu(self.window,
                                   self.__selecman,
                                   *self.manlist
                                   )
        self.__manOpt.grid(row = 1, column = 1, sticky = "EW")

        Label(self.window,
              text = s_elem_def["COUNT"][self.lang] + ":"
              ).grid(row = 1, column = 2, sticky = "EW")

        self.__cMan = IntVar()
        self.__cMan.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__cMan,
              ).grid(row = 1, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcMan
               ).grid(row = 1, column = 4, sticky = "EW")

        Button(self.window,
               text = labels["win_man"][self.lang],
               command = self.__callManWin
               ).grid(row = 1, column = 6, sticky = "EW")

        # row 2
        Label(self.window,
              text = s_elem_def["SPELL"][self.lang] + ":",
              ).grid(row = 2, column = 0, sticky = "W")

        self.__lvlSpell = IntVar()
        self.__lvlSpell.set(1)
        Entry(self.window,
              justify = "center",
              textvariable = self.__lvlSpell
              ).grid(row = 2, column = 1, sticky = "EW")

        Label(self.window,
              text = s_elem_def["COUNT"][self.lang] + ":"
              ).grid(row = 2, column = 2, sticky = "EW")

        self.__cSpell = IntVar()
        self.__cSpell.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__cSpell,
              ).grid(row = 2, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcSpell
               ).grid(row = 2, column = 4, sticky = "EW")

        Button(self.window,
               text = labels["win_casting"][self.lang],
               command = self.__winCasting
               ).grid(row = 2, column = 6, sticky = "EW")
        # row 3
        self.critlist = ['T', 'A', 'B', 'C', 'D', 'E', "KILL"]
        Label(self.window,
              text = s_elem_def["H_CRITS"][self.lang] + ":",
              ).grid(row = 3, column = 0, sticky = "W")

        self.__gcrit = StringVar()
        self.__gcrit.set("T")
        OptionMenu(self.window,
                    self.__gcrit,
                    *self.critlist
                   ).grid(row = 3, column = 1, sticky = "EW")

        Label(self.window,
              text = s_elem_def["HITS"][self.lang] + ":",
              ).grid(row = 3, column = 2, sticky = "W")

        self.__hits = IntVar()
        self.__hits.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__hits,
              ).grid(row = 3, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcGCrit
               ).grid(row = 3, column = 4, sticky = "EW")

        Button(self.window,
               text = labels["win_fight"][self.lang],
               command = self.notdoneyet
               ).grid(row = 3, column = 6, sticky = "NEWS")

        # row 4
        Label(self.window,
              text = s_elem_def["CRITICAL"][self.lang] + ":",
              ).grid(row = 4, column = 0, sticky = "W")

        self.__crit = StringVar()
        self.__crit.set("T")
        OptionMenu(self.window,
                    self.__crit,
                    *self.critlist
                   ).grid(row = 4, column = 1, sticky = "EW")
        Label(self.window,
              text = labels["lvl_enemy"][self.lang] + ":",
              ).grid(row = 4, column = 2, sticky = "WE")

        self.__lvlenem = IntVar()
        self.__lvlenem.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__lvlenem,
              ).grid(row = 4, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcCrit
               ).grid(row = 4, column = 4, sticky = "EW")
        Button(self.window,
               text = txtbutton["but_rr"][self.lang],
               command = self.__rrroll
               ).grid(row = 4, column = 6, sticky = "EW")

        # row 5
        Label(self.window,
              text = s_elem_def["TRAVEL"][self.lang] + ":",
              ).grid(row = 5, column = 0, sticky = "W")

        self.__travel = IntVar()
        self.__travel.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__travel,
              ).grid(row = 5, column = 1, sticky = "EW")
        Label(self.window,
              text = labels["comment"][self.lang] + ":",
              ).grid(row = 5, column = 2, sticky = "EW")

        self.__comtravel = StringVar()
        self.__comtravel.set("")
        Entry(self.window,
              justify = "center",
              textvariable = self.__comtravel,
              ).grid(row = 5, column = 3, sticky = "EW")
        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcTravel
               ).grid(row = 5, column = 4, sticky = "EW")

        Button(self.window,
               text = labels["diary"][self.lang],
               command = self.notdoneyet
               ).grid(row = 5, column = 6, sticky = "EW")
        # row 6
        Label(self.window,
              text = s_elem_def["IDEAS"][self.lang] + ":",
              ).grid(row = 6, column = 0, sticky = "W")

        self.__ideas = IntVar()
        self.__ideas.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__ideas,
              ).grid(row = 6, column = 1, sticky = "EW")
        Label(self.window,
              text = labels["comment"][self.lang] + ":",
              ).grid(row = 6, column = 2, sticky = "EW")
        self.__comideas = StringVar()
        self.__comideas.set("")
        Entry(self.window,
              justify = "center",
              textvariable = self.__comideas,
              ).grid(row = 6, column = 3, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_add"][self.lang],
               command = self.__calcIdeas
               ).grid(row = 6, column = 4, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_fin"][self.lang],
               command = self.__finalize,
               bg = "grey",
               fg = "white"
               ).grid(row = 6, column = 6, sticky = "EW")


    def __updDispay(self, curPlayer = ""):
        '''!
        Updates display of current player
        @param curPlayer name of selected player
        '''
        self.group[curPlayer].updateInfo()
        self.__gained.set("+{}".format(self.group[curPlayer].gainedep))
        self.__newep.set("<{}>".format(self.group[curPlayer].newep))
        self.__newlvl.set(self.group[curPlayer].newlvl)


    def __updSelec(self, event):
        """!
        Update selected Player data
        """
        selected = self.__selecPlayer.get()
        ind = self.players.index(selected)
        self.__charname.set(self.charlist[ind]["name"])
        self.__charprof.set("{} ({})".format(self.charlist[ind]["prof"], self.group[selected].lvl))
        self.__charexp.set(str(self.charlist[ind]["exp"]))
        self.__gained.set("+{}".format(self.group[self.charlist[ind]["player"]].gainedep))
        self.__newep.set("<{}>".format(self.group[self.charlist[ind]["player"]].gainedep + self.group[self.charlist[ind]["player"]].newep))
        self.__newlvl.set(self.group[self.charlist[ind]["player"]].newlvl)


    def __autoSave(self):
        """!
        This function is for aut saving the group object in case of a program / computer crash
        """
        with open("autosave.pkl", "wb") as fp:
            pickle.dump(self.group, fp)


    def __loadAutosave(self):
        """!
        This loads an autosave file if there is any
        """
        if os.path.exists("autosave.pkl"):
            with open("autosave.pkl", "rb") as fp:
                self.group = pickle.load(fp)

            os.remove("autosave.pkl")


    def __grpBonus(self):
        '''!
        This methods calculates the group bonus while finalize process.
        '''
        grpbonus = 0

        for name in self.group.keys():
            grpbonus += self.group[name].gainedep

        grpbonus = int(round(grpbonus / len(self.group.keys())))

        for name in self.group.keys():
            self.group[name].gainedep += grpbonus
            self.group[name].updateInfo()

        self.__autoSave()


    def __calcMan(self):
        '''!
        This computes EPs for each successful maneuver and add them to character's
        gained EPs
        '''
        curPlayer = self.__selecPlayer.get()
        curManLvl = self.__selecman.get()
        number = self.__cMan.get()

        self.group[curPlayer].maneuver(curManLvl, number)
        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcSpell(self):
        '''!
        This computes EPs for a given number aof spells aof the same level
        '''
        curPlayer = self.__selecPlayer.get()
        spellLvl = self.__lvlSpell.get()
        spellNo = self.__cSpell.get()
        self.group[curPlayer].spell(spellLvl, spellNo)
        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcGCrit(self):
        '''!
        This calculates EP for gained criticals and hits
        '''
        curPlayer = self.__selecPlayer.get()
        gCrit = self.__gcrit.get()
        hits = self.__hits.get()

        if gCrit in ["T", "KILL"]:
            self.group[curPlayer].gainedHits(hits)

        else:
            self.group[curPlayer].gainedHits(hits)
            self.group[curPlayer].gainedCrit(gCrit, 1)

        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcCrit(self):
        '''!
        This calculates EP for caused criticals against an enemy of a certain level
        '''
        curPlayer = self.__selecPlayer.get()
        crit = self.__crit.get()
        lvlEnem = self.__lvlenem.get()

        if crit not in ["T", "KILL"]:
            self.group[curPlayer].hitCrit(crit, lvlEnem, 1)
        elif crit == "KILL":
            self.group[curPlayer].killedNPC(lvlEnem, 1)

        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcTravel(self):
        '''!
        Travelled EPs
        ----
        @todo The comments have to be added to the  character's diary
        '''
        curPlayer = self.__selecPlayer.get()
        travel = self.__travel.get()
        comm = self.__comtravel.get()
        self.group[curPlayer].travelled(travel)

        self.__autoSave()
        self.__updDispay(curPlayer)


    def __calcIdeas(self):
        '''!
        EPs for ideas and role-playing
        ----
        @todo The comments have to be added to the character's diary
        '''
        curPlayer = self.__selecPlayer.get()
        ideas = self.__ideas.get()
        comm = self.__comideas.get()
        self.group[curPlayer].ideas(ideas)

        self.__autoSave()
        self.__updDispay(curPlayer)


    def __finalize(self):
        '''!
        Do all finalizing steps:
        -# adding new EPs to characters
        -# open display window for whole group EPs
        -# store new levels
         - in character's files
         - in group file
        '''
        self.__grpBonus()

        for i in range(0, len(self.charlist)):
            name = self.charlist[i]['player']
            self.charlist[i]["exp"] = self.group[name].newep
            newlvl = getLvl(self.group[name].newep)

            if self.charlist[i]["lvl"] < newlvl:
                self.charlist[i]["lvl"] = deepcopy(newlvl)
                self.charlist[i]["lvlup"] += 1

            self.charlist[i]['old_exp'] = self.group[name].ep

        self.__autoSave()
        gw = showGrpEP(self.charlist, self.storepath, self.lang)


    def __callManWin(self):
        '''!
        Opens Maneuver Window for maneuver rolls
        '''
        who = self.__selecPlayer.get()
        for elem in self.charlist:
            if elem['player'] == who:
                manWin(elem, self.lang)


    def __rrroll(self):
        '''!
        This opens a resistance roll window
        ----
        @todo has to be implemented fully
        '''
        who = self.__selecPlayer.get()
        RRWin(self.lang, who, self.charlist, self.storepath)


    def __targetArmor(self, char):
        '''!
        Resolve the target-armor class for castBaseSpell from the character's
        equipped armor inventory.  castBaseSpell expects the keys
        'metal armor', 'leather armor', 'other', 'metal shield',
        'metal helmet', 'leather helmet'.

        Heuristic (the RM character JSON does not carry an explicit armor
        class, only name / material / covers):
          * metal armor   - metal material (or name contains 'plate' / 'mail')
          * leather armor - leather / hide material
          * metal shield  - name contains 'shield' AND metal material
          * 'other'       - fallback for any non-metal, non-leather item
                            (arm greaves, bucklers, etc.)
        The first matching class wins; if nothing matches, 'other' is True.

        @param char character dict (expects 'inventory.armor' to be a list)
        @return tuple (targetarmor_dict, human_readable_label)
        '''
        target = {"metal armor": False,
                  "leather armor": False,
                  "other": False,
                  "metal shield": False,
                  "metal helmet": False,
                  "leather helmet": False}

        label = "no armor"
        armor = char.get("inventory", {})
        lst = armor.get("armor") if isinstance(armor, dict) else None

        if isinstance(lst, list):
            for item in lst:
                if not isinstance(item, dict):
                    continue
                if item.get("location") == "none":
                    continue
                name = (item.get("name") or "").lower()
                mat = (item.get("material") or "").lower()
                is_metal = (mat == "metal") or ("plate" in name) or ("mail" in name)
                is_leather = (mat == "leather") or ("hide" in mat)

                if is_metal and ("shield" in name):
                    target["metal shield"] = True
                    label = "metal shield"
                elif is_leather and ("helmet" in name):
                    target["leather helmet"] = True
                    label = "leather helmet"
                elif is_metal and ("helmet" in name):
                    target["metal helmet"] = True
                    label = "metal helmet"
                elif is_metal:
                    target["metal armor"] = True
                    label = "metal armor"
                elif is_leather:
                    target["leather armor"] = True
                    label = "leather armor"
                else:
                    target["other"] = True
                    label = item.get("name") or "other armor"

        if not any(target.values()):
            target["other"] = True

        return target, label

    def __winCasting(self):
        '''!
        Opens a Toplevel window for basic spell-casting via the basic spell table
        (magic.readBasicTable), followed by a resistance roll (rpgtools.RRroll).
        Flow:
          1. pick character (or 'universell' = no character filter), spell list, spell
          2. roll d100 (button) or enter a value manually
          3. Zaubern: probe = list total bonus + d100  ->  basic table cell
                      cell 'F'  -> Fumble;  cell int  -> RR-Modifikator
          4. RRroll(stufe zauberer, stufe ziel, rrmod + RR-Ziel-Modifikator)
             resisted=True  -> Ziel widersteht (Zauber schlaegt FEHL)
        '''
        from rpgToolDefinitions import magic as _magic
        from rpgtoolbox.rpgtools import RRroll as _RRroll

        top = Toplevel(self.window)
        top.transient(self.window)
        try:
            top.title(labels["win_casting"][self.lang])
        except (KeyError, IndexError):
            top.title("Zauber wirken")
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(2, weight=1)
        L = self.lang

        def _t(key, fallback):
            """!
            Localized label lookup in the langpack labels dict.

            @param key      label key in gui.window.labels
            @param fallback text to return if the key or language is missing
            @return localized string or fallback
            """
            d = labels.get(key) or {}
            return d.get(L) or d.get("de") or fallback

        # --- helper: collect learned spell-list blocks for a character ----------
        def _spell_blocks(char):
            """!
            Collects all spell-list blocks of one character from its 'Spells - *'
            categories (cat -> Skill -> list -> Spells).

            @param char character dict (or None for no list at all)
            @return list of dicts with keys 'cat', 'name', 'rank', 'total bonus',
                    'cat total bonus', 'Spells'
            """
            out = []
            if char is None:
                return out
            cat = char.get('cat') or {}
            if not isinstance(cat, dict):
                return out
            for cname, blk in sorted(cat.items()):
                if not str(cname).startswith('Spells - '):
                    continue
                if not isinstance(blk, dict):
                    continue
                cat_total = blk.get('total bonus', 0)
                skill = blk.get('Skill')
                if isinstance(skill, dict):
                    for lname, lblk in sorted(skill.items()):
                        if not isinstance(lblk, dict):
                            continue
                        spells = lblk.get('Spells') or []
                        if not spells:
                            continue
                        out.append({
                            'cat': cname,
                            'name': lname,
                            'rank': lblk.get('rank', 0),
                            'total bonus': lblk.get('total bonus', 0),
                            'cat total bonus': cat_total,
                            'Spells': spells,
                        })
                else:
                    # fallback: no 'Skill' sub-dict -> spells directly on the block
                    spells = blk.get('Spells') or []
                    if spells:
                        out.append({
                            'cat': cname,
                            'name': cname.split(' - ', 1)[-1],
                            'rank': blk.get('rank', 0),
                            'total bonus': blk.get('total bonus', 0),
                            'cat total bonus': cat_total,
                            'Spells': spells,
                        })
            return out

        def _learned_blocks(char):
            """
            Collects only the spell-list blocks the character actually learned
            (list rank > 0).

            A character may know a list (rank > 0) without having trained any
            bonus into it yet; a list with a positive bonus but rank 0 is an
            item/gear source, not a learned list, and is excluded here.

            @param char character dict (or None for no list at all)
            @return learned spell-list blocks as produced by _spell_blocks
            @bug BUG-2254
            """
            res = []
            for b in _spell_blocks(char):
                try:
                    r = int(b.get("rank", 0))
                except (TypeError, ValueError):
                    r = 0
                if r > 0:
                    res.append(b)
            return res

        # --- collect all spell lists (all characters) for 'universell' -----------
        all_blocks = []
        for c in self.charlist:
            for b in _spell_blocks(c):
                b.setdefault('realm', c.get('realm') or 'Essence')
                all_blocks.append(b)

        def _char_entry(sel):
            """resolve the charlist dict behind a selected display name"""
            for c in self.charlist:
                if (c.get('player') or c.get('name') or '?') == sel:
                    return c
            return None

        def _current_blocks():
            """(blocks, realm) for the current character selection"""
            sel = char_var.get()
            if sel == 'universell':
                blocks = all_blocks
                realm = 'Essence'
                caster = self.charlist[0] if self.charlist else None
                if caster and isinstance(caster.get('realm'), str):
                    realm = caster['realm']
                return blocks, realm, caster
            caster = _char_entry(sel)
            blocks = _learned_blocks(caster) if caster else []
            realm = 'Essence'
            if caster and isinstance(caster.get('realm'), str):
                realm = caster['realm']
            return blocks, realm, caster

        # --- dropdowns: character / spell list / spell ----------------------------
        char_names = ['universell'] + [c.get('player') or c.get('name') or '?'
                                       for c in self.charlist]
        char_names_uniq = []
        for n in char_names:
            if n not in char_names_uniq:
                char_names_uniq.append(n)
        char_names = char_names_uniq if char_names_uniq else ['universell']

        char_var = StringVar(top)
        char_var.set('universell')  # BUG-2257: window must open with a valid selection
        list_var = StringVar(top)
        spell_var = StringVar(top)

        def _set_options(menu, var, options, on_change=None):
            """
            Replaces the OptionMenu options dynamically and re-selects the first
            (or the still valid old) entry.

            Every new menu entry gets the same command callback as the original
            OptionMenu construction, so selecting an entry after a rebuild still
            fires on_change as before.

            @param menu OptionMenu whose internal menu is refilled
            @param var StringVar bound to the OptionMenu
            @param options new option labels (may be empty)
            @param on_change Optional callback invoked after a selection change
            @bug BUG-2255
            """
            old = var.get()
            menu['menu'].delete(0, 'end')
            for o in options:
                def _pick(o=o):
                    """!\
                    Menu entry action: stores the selection in the bound
                    StringVar and then notifies the change callback, so the
                    spell dropdown / info text are rebuilt on every selection.

                    @bug BUG-2255
                    """
                    var.set(o)
                    if on_change is not None:
                        on_change()
                menu['menu'].add_command(label=o, command=_pick)
            if options:
                var.set(old if old in options else options[0])
            else:
                var.set('-')

        # --- spell info output ----------------------------------------------------
        info = Text(top, height=6, width=56, wrap='word')
        info.grid(row=6, column=0, columnspan=4, sticky='WE', padx=2, pady=2)
        info.config(state='disabled')

        def _show_spell_info():
            """show the fields of the currently selected spell"""
            info.config(state='normal')
            info.delete('1.0', 'end')
            blocks, _realm, _caster = _current_blocks()
            blk = next((b for b in blocks if b['name'] == list_var.get()), None)
            s = None
            if blk is not None:
                s = next((x for x in (blk.get('Spells') or [])
                          if str(x.get('Spell')) == str(spell_var.get())), None)
            if s is None:
                info.insert('end', '(kein Zauber gewaehlt)\n')
            else:
                info.insert('end', 'Zauber      : %s\n' % s.get('Spell', '-'))
                info.insert('end', 'Stufe       : %s\n' % s.get('Lvl', '-'))
                info.insert('end', 'Dauer       : %s\n' % s.get('Duration', '-'))
                info.insert('end', 'Reichweite  : %s\n' % s.get('Range', '-'))
                info.insert('end', 'Ziel        : %s\n' % s.get('Area of Effect', '-'))
                info.insert('end', 'Typ         : %s\n' % s.get('Type', '-'))
                info.insert('end', 'Beschreibung: %s\n' % (s.get('Description') or '-'))
                if blk is not None:
                    info.insert('end', '\nListe : %s  (Rank %s, Bonus %s)\n' % (
                        blk['name'], blk.get('rank', '-'), blk.get('total bonus', '-')))
            info.config(state='disabled')

        def _rebuild_spells():
            """!
            Refills the spell dropdown with the spells of the currently selected
            list; only spells with Lvl <= list rank are offered. Afterwards the
            spell-info output is updated.
            """
            blocks, _realm, _caster = _current_blocks()
            blk = next((b for b in blocks if b['name'] == list_var.get()), None)
            names = []
            if blk is not None:
                try:
                    lvl_ok = int(blk.get('rank', 0))
                except (TypeError, ValueError):
                    lvl_ok = 0
                for s in (blk.get('Spells') or []):
                    if not isinstance(s, dict):
                        continue
                    try:
                        if int(s.get('Lvl', 0)) > lvl_ok and lvl_ok > 0:
                            continue
                    except (TypeError, ValueError):
                        pass
                    names.append(str(s.get('Spell', '?')))
            _set_options(spell_menu, spell_var, names, _show_spell_info)
            _show_spell_info()

        def _rebuild_lists():
            """!
            Refills the spell-list dropdown from the currently selected character
            (or all lists for 'universell') and triggers _rebuild_spells().
            """
            blocks, _realm, _caster = _current_blocks()
            list_opts = [b['name'] for b in blocks]
            _set_options(list_menu, list_var, list_opts, _rebuild_spells)
            _rebuild_spells()

        # --- input fields -------------------------------------------------------
        st_z_var = IntVar(top);    st_z_var.set(1)
        st_t_var = IntVar(top);    st_t_var.set(1)
        name_t_var = StringVar(top)
        rr_mod_var = IntVar(top);  rr_mod_var.set(0)
        d100_var = IntVar(top)

        def _lbl(text):
            """!\
            Builds a readable label: light text (fg) on the standard
            dark window background, otherwise it renders black-on-dark.

            @param text label text
            @return configured tk.Label widget
            @bug BUG-2256
            """
            return Label(top, text=text, bg='#333333', fg='#e8e8e8')

        _lbl('Stufe Zaub.:').grid(row=3, column=0, sticky='E', padx=1, pady=1)
        Entry(top, width=5, textvariable=st_z_var).grid(row=3, column=1, sticky='W', padx=1, pady=1)
        _lbl('Stufe Ziel:').grid(row=3, column=2, sticky='E', padx=1, pady=1)
        Entry(top, width=5, textvariable=st_t_var).grid(row=3, column=3, sticky='W', padx=1, pady=1)

        _lbl('Name Ziel:').grid(row=4, column=0, sticky='E', padx=1, pady=1)
        Entry(top, width=14, textvariable=name_t_var).grid(row=4, column=1, sticky='W', padx=1, pady=1)
        _lbl('RR-Ziel-Mod.:').grid(row=4, column=2, sticky='E', padx=1, pady=1)
        Entry(top, width=5, textvariable=rr_mod_var).grid(row=4, column=3, sticky='W', padx=1, pady=1)

        _lbl('Wuerfel:').grid(row=5, column=0, sticky='E', padx=1, pady=1)
        Entry(top, width=5, textvariable=d100_var).grid(row=5, column=1, sticky='W', padx=1, pady=1)

        # --- result output -------------------------------------------------------
        res = Text(top, height=8, width=56, wrap='word')
        res.grid(row=7, column=0, columnspan=4, sticky='WE', padx=2, pady=2)
        res.config(state='disabled')

        def _emit(text=''):
            """!
            Appends one line to the cast-result text widget and scrolls to the end.

            @param text line to append (newline is added automatically)
            """
            res.config(state='normal')
            res.insert('end', text + '\n')
            res.see('end')
            res.config(state='disabled')

        # --- actions -------------------------------------------------------------
        def _do_roll():
            """!
            Rolls a d100 via the helptools RMDice function (rules="RM") and stores
            the result in the 'Wuerfel' entry field. Falls back to a plain random
            d100 if the dice function fails.
            """
            try:
                roll_res = dice(rules="RM")
                v = int(roll_res[0][0])
            except Exception:
                import random as _r
                v = _r.randint(1, 100)
            d100_var.set(v)

        def _do_cast():
            """!
            Casts the currently selected spell: takes the list bonus plus the
            d100 value as probe, resolves the result cell from the basic spell
            table (magic.readBasicTable) for the target realm and armor class,
            then applies the cell modifier to a resistance roll
            (rpgtools.RRroll(caster level, target level, roll)).
            All steps are printed to the result output; 'F' in the table is a
            Fumble, a resisted target means the spell fails.
            """
            sel_char = char_var.get()
            sel_list = list_var.get()
            sel_spell = spell_var.get()

            blocks, realm, caster = _current_blocks()
            blk = next((b for b in blocks if b['name'] == sel_list), None)
            if blk is None:
                _emit('FEHLER: keine Spruchliste gewaehlt.')
                return

            # cast bonus: list bonus, fallback: cat bonus
            total = blk.get('total bonus', 0)
            if not isinstance(total, (int, float)):
                total = blk.get('cat total bonus', 0)
            try:
                total = int(total)
            except (TypeError, ValueError):
                total = 0

            try:
                d100      = int(d100_var.get())
                st_z      = int(st_z_var.get() or 1)
                st_t      = int(st_t_var.get() or 1)
                rr_target = int(rr_mod_var.get() or 0)
            except (TypeError, ValueError):
                _emit('FEHLER: unguelle Zahleneingabe.')
                return

            # realm: realm of the character who learned this list (if any)
            if blk.get('realm'):
                realm = blk['realm']

            # resolve target character by name (exact match on player/name)
            target_char = None
            tname = name_t_var.get().strip()
            if tname:
                for c in self.charlist:
                    cand = [(c.get('player') or '').strip(),
                            (c.get('name') or '').strip()]
                    if tname in cand or tname.lower() in [x.lower() for x in cand]:
                        target_char = c
                        break

            # armor class of the TARGET (no target -> unarmored 'Other')
            armor_dict, armor_lbl = self.__targetArmor(
                target_char if target_char is not None else {'inventory': {}})
            armor_token = 'Other'
            if armor_dict.get('metal armor'):
                armor_token = 'Metal Armor'
            elif armor_dict.get('leather armor'):
                armor_token = 'Leather Armor'
            elif armor_dict.get('metal shield'):
                armor_token = 'Metal Shield'
            elif armor_dict.get('metal helmet'):
                armor_token = 'Metal Helmet'
            elif armor_dict.get('leather helmet'):
                armor_token = 'Leather Helmet'

            col = '%s_%s' % (realm, armor_token)

            probe = total + d100
            _emit('=' * 52)
            _emit('Zauber wirken : %s  /  %s  /  %s' % (sel_char, sel_list, sel_spell))
            _emit('  Stufe Zauberer : %d    Stufe Ziel : %d' % (st_z, st_t))
            _emit('  Ziel          : %s   (Ruestung: %s)' % (name_t_var.get() or '-', armor_lbl))
            _emit('  Realm         : %s    Spalte: %s' % (realm, col))
            _emit('  Listenbonus   : %d    d100: %d' % (total, d100))
            _emit('  Probe (= bonus + d100) : %d' % probe)

            try:
                table = _magic.readBasicTable()
            except Exception as e:
                _emit('  FEHLER: Grundtabelle nicht lesbar: %s' % e)
                return
            ladder = table.get('roll') or []
            if col not in table or not ladder:
                _emit('  FEHLER: Spalte "%s" nicht in der Grundtabelle.' % col)
                return

            # last table row whose ladder value is <= probe (worst row if probe < first)
            idx, found = 0, False
            for i, v in enumerate(ladder):
                try:
                    if int(v) <= probe:
                        idx, found = i, True
                    else:
                        break
                except (TypeError, ValueError):
                    break
            if not found:
                try:
                    if probe < int(ladder[0]):
                        idx, found = 0, True
                except (TypeError, ValueError):
                    pass
            if not found:
                _emit('  FEHLER: Probe %d nicht in der Tabelle.' % probe)
                return

            cell = table[col][idx]
            _emit('  Tabelle       : Zeile <= %s    Zelle = %s' % (ladder[idx], cell))

            if str(cell).strip().upper() == 'F':
                _emit('  ERGEBNIS       : FUMBLE  -  der Zauber FEHLSCHLAGT.')
                return

            try:
                rrmod = int(str(cell).strip())
            except (TypeError, ValueError):
                _emit('  ERGEBNIS       : ungueltiger Tabellenwert (%s)' % cell)
                return
            _emit('  RR-Modifikator : %d' % rrmod)

            final_roll = rrmod + rr_target
            _emit('  RR-Schlusswert : %d + %d (Ziel-Mod) = %d' % (rrmod, rr_target, final_roll))

            try:
                resisted, value = _RRroll(st_z, st_t, final_roll)
            except Exception as e:
                _emit('  FEHLER bei RR-Wurf: %s' % e)
                return
            _emit('  RR-Wert Ziel   : %s' % value)
            if resisted:
                _emit('  ERGEBNIS       : ZIEL WIDERSTEHT  -  Zauber FEHLSCHLAGT.')
            else:
                _emit('  ERGEBNIS       : ZIEL WIDERSTEHT NICHT  -  Zaubern GELINGT.')

        # --- menus + buttons -------------------------------------------------------
        _lbl('Charakter:').grid(row=0, column=0, sticky='E', padx=1, pady=1)
        char_menu = OptionMenu(top, char_var, *char_names, command=lambda x: _rebuild_lists())
        char_menu.grid(row=0, column=1, columnspan=3, sticky='WE', padx=1, pady=1)

        _lbl('Spruchliste:').grid(row=1, column=0, sticky='E', padx=1, pady=1)
        list_menu = OptionMenu(top, list_var, '-', command=lambda x: _rebuild_spells())
        list_menu.grid(row=1, column=1, columnspan=3, sticky='WE', padx=1, pady=1)

        _lbl('Zauber:').grid(row=2, column=0, sticky='E', padx=1, pady=1)
        spell_menu = OptionMenu(top, spell_var, '-', command=lambda x: _show_spell_info())
        spell_menu.grid(row=2, column=1, columnspan=3, sticky='WE', padx=1, pady=1)

        btn_roll = Button(top, text=_t('but_roll', 'Wuerfeln'), command=_do_roll,
                          bg='#2a5d8a', fg='white', padx=6, pady=2)
        btn_cast = Button(top, text=_t('but_cast', 'Zaubern'), command=_do_cast,
                          bg='#3a7d3a', fg='white', padx=6, pady=2)
        btn_close = Button(top, text=_t('but_clos', 'schliessen'), command=top.destroy,
                           bg='#555555', fg='white', padx=6, pady=2)
        btn_roll.grid(row=8, column=0, sticky='WE', padx=2, pady=2)
        btn_cast.grid(row=8, column=1, sticky='WE', padx=2, pady=2)
        btn_close.grid(row=8, column=2, columnspan=2, sticky='E', padx=2, pady=2)

        # initial population + focus
        _rebuild_lists()
        btn_roll.focus_set()
        top.protocol('WM_DELETE_WINDOW', top.destroy)
        self.win_casting = top

    def __winSpellLists(self, char):
        '''!
        Collects all ranked (or listed) spell lists of a character.
        @param char character dict from self.charlist
        @retval list of tuples (listname, totalbonus)
        '''
        out = []
        cat = char.get("cat", {})
        if not isinstance(cat, dict):
            return out

        for key in sorted(cat.keys()):
            if key.startswith("Spells - "):
                blk = cat[key]

                if not isinstance(blk, dict):
                    continue

                out.append((key, int(blk.get("total bonus", 0))))

        return out


    def __save(self):
        '''!
        This opens a file dialog window for saving
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.charlist, fp, indent = 4)


    def __open(self):
        '''!
        This opens a file dialog window for opening a group file.
        '''
        opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])
        with open(opendir, "r") as fp:
            self.charlist = json.load(fp)
        # set up new player group list
        self.players = []
        self.group = {}
        for elem in self.charlist:
            self.players.append(elem["player"])
            self.group[elem["player"]] = epcalc.experience(elem["player"], elem["exp"])
            self.group[elem["player"]].updateInfo()

        self.__selecPlayer.set(self.players[0])
        self.__playerOpt = OptionMenu(self.window,
                                      self.__selecPlayer,
                                      *self.players,
                                      command = self.__updSelec)
        self.__playerOpt.grid(column = 0, row = 0, sticky = "W")


    def __quit(self):
        '''!
        This method closes the window
        '''
        self.window.destroy()




class showGrpEP(object):
    '''!
    Display and save window for group EPs
    '''


    def __init__(self, charlist = None, storepath = "./data", lang = 'en'):
        """!
        Class constructor

        @param charlist   list of dictionaries holding: player, charname, EPs
        @param storepath  path for storing the data into the character files
        @param lang       interface language ("en" default, "de")
        """
        self.lang = lang
        self.storepath = storepath
        self.charlist = charlist
        self.window = Toplevel()
        self.title = wintitle["rm_groupEP"][self.lang]

        self.window.title(self.title)
        for i in range(0, len(self.charlist)):
            Label(self.window,
                  text = "{} ({}):".format(self.charlist[i]["player"],
                                         self.charlist[i]["name"])
                  ).grid(row = i, column = 0, sticky = "EW")
            Label(self.window,
                  text = "+{} -> {}".format(self.charlist[i]["exp"] - self.charlist[i]["old_exp"],
                                            self.charlist[i]['exp'])
                  ).grid(row = i, column = 1, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_save_char"][self.lang],
               command = self.saveChars,
               bg = "grey",
               fg = "white"
               ).grid(row = i + 1, column = 0, sticky = "NEWS")
        Button(self.window,
               text = txtbutton["but_save_grp"][self.lang],
               command = self.saveGroup
               ).grid(row = i + 1, column = 1, sticky = "NEWS")

        self.window.mainloop()


    def saveChars(self):
        '''!
        This saves all single characters separated from group
        '''
        if self.storepath[-1] != "/":
            self.storepath += "/"
        if os.path.exists(self.storepath):

            for char in self.charlist:
                charpath = self.storepath + "/" + char["player"] + "/"

                if os.path.exists(charpath):
                    with open(charpath + char['name'] + ".json", "w") as fp:
                        json.dump(char, fp, indent = 4)
                    print("data saved to {}".format(charpath + char['name'] + ".json"))
                else:
                    print("{} not found -> {}".format(charpath, os.getcwd()))

#        if os.path.exists("autosave.pkl"):
#            os.remove("autosave.pkl")


    def saveGroup(self):
        '''!
        Saves all data in a groupfile
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])
        with open(savedir, "w") as fp:
            json.dump(self.charlist, fp, indent = 4)

        if os.path.exists("autosave.pkl"):
            os.remove("autosave.pkl")




class manWin(object):
    '''
    Maneuver Window
    '''


    def __init__(self, character = None, lang = "en"):
        '''!
        Constructor
        @param character whole character daa
        @param lang interface language; default: English
        '''
        self.character = character
        self.lang = lang
        self.man_ep = 0
        # # @var self.total
        # total result of skill check
        self.total = 0
        self.category = "Armor - Heavy"
        self.skill = ""
        self.man = "routine"
        self.maneuver = maneuvers
        self.mantab = rpg.statManeuver()
        self.spelltab = rpg.statManeuver("./data/default/tables/spell_casting_smt.csv")
        self.dice = dice
        self.window = Toplevel()
        self.title = "{}: {} - {}".format(wintitle['rm_maneuver'][self.lang], self.character['player'], self.character['name'])
        self.window.title(self.title)
        self._buildwin()
        self.window.mainloop()


    def _buildwin(self):
        '''
        This defines the different element in the window layout
        '''
        # row 0
        Label(self.window,
              text = self.character["player"]
              ).grid(row = 0, column = 0, sticky = "NEWS")
        Label(self.window,
              text = self.character["name"]
              ).grid(row = 0, column = 2, sticky = "NEWS")
        Label(self.window,
              text = "{}/{} ({})".format(self.character["race"],
                                         self.character["prof"],
                                         self.character["lvl"])
              ).grid(row = 0, column = 4, sticky = "NEWS")
        from PIL import Image as _pilimg, ImageTk
        self.cpic = ImageTk.PhotoImage(_pilimg.open(self.character["piclink"]).resize((210, 210), _pilimg.Resampling.LANCZOS))
        self.picLabel = Label(master = self.window,
                              image = self.cpic
                              )

        self.picLabel.grid(column = 5,
                           row = 0,
                           columnspan = 2,
                           rowspan = 8,
                           sticky = "NEWS",
                           padx = 5,
                           pady = 5)
        # row 1
        vcscroll = Scrollbar(self.window, orient = VERTICAL)
        self.catlb = Listbox(self.window,
                             yscrollcommand = vcscroll.set,
                              width = 30,
                              height = 5)
        vcscroll.config(command = self.catlb.yview)
        vcscroll.grid(row = 1, column = 1, sticky = "WNS")
        self.catlb.grid(row = 1, column = 0, sticky = "NEW")
        for cat in  self.character["cat"].keys():
            self.catlb.insert(END, cat)
        self.catlb.bind("<Button-1>", self._fillSkill)

        vsscroll = Scrollbar(self.window, orient = VERTICAL)
        self.skilllb = Listbox(self.window,
                               yscrollcommand = vsscroll.set,
                              width = 30,
                              height = 5)
        vsscroll.config(command = self.skilllb.yview)
        vsscroll.grid(row = 1, column = 3, sticky = "WNS")
        self.skilllb.grid(row = 1, column = 2, sticky = "NEW")
        for skill in self.character["cat"]["Armor - Heavy"]["Skill"].keys():
            if skill not in ["Progression", "Stats"] and skill[-1] != "+":
                self.skilllb.insert(END, skill)
        self.skilllb.bind("<Button-1>", self._getSkill)

        vmscroll = Scrollbar(self.window, orient = VERTICAL)
        self.manlb = Listbox(self.window,
                             yscrollcommand = vmscroll.set,
                             height = 5)
        vmscroll.config(command = self.manlb.yview)
        vmscroll.grid(row = 1, column = 5, sticky = "WNS")
        self.manlb.grid(row = 1, column = 4, sticky = "NEW")

        for skill in self.maneuver.keys():
            self.manlb.insert(END, skill)
        self.manlb.bind("<Button-1>", self._getMan)
        # row 2
        self.catlabel = Label(self.window,
                              text = self.category)
        self.catlabel.grid(row = 2, column = 0, sticky = "EWS")

        self.skilllabel = Label(self.window,
                                text = self.skill)
        self.skilllabel.grid(row = 2, column = 2, sticky = "EWS")

        self.manlabel = Label(self.window,
                              text = self.man)
        self.manlabel.grid(row = 2, column = 4, sticky = "EWS")
        # row 3
        Label(self.window,
              text = "+ {}:".format(labels['modifier'][self.lang])
              ).grid(row = 3, column = 0, sticky = "NEWS")

        Button(self.window,
               text = txtbutton["but_roll"][self.lang],
               command = self._rollDice,
               bg = "grey",
               fg = "white",
#               image = "./data/default/pics/d10.png"
               ).grid(row = 3, column = 2, sticky = "NEWS")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self._chkResult
               ).grid(row = 3, column = 4, sticky = "NEWS")
        # row 4
        self.mod = IntVar()
        self.mod.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.mod
              ).grid(row = 4, column = 0, sticky = "EW")
        self.diceroll = StringVar()
        self.diceroll.set("0")
        Entry(self.window,
              justify = "center",
              textvariable = self.diceroll,
              ).grid(row = 4, column = 2, sticky = "EW")

        self.totallabel = StringVar()
        self.totallabel.set("--")
        Label(self.window,
              textvariable = self.totallabel,
              justify = "center"
              ).grid(row = 4, column = 4, sticky = "NEWS")
        # row 5
        Label(self.window,
              text = labels['class'][self.lang] + ":"
              ).grid(row = 5, column = 0, sticky = "NEWS")

        Label(self.window,
              text = labels['perc'][self.lang] + ":"
              ).grid(row = 5, column = 2, sticky = "NEWS")

        Label(self.window,
              text = labels['time'][self.lang] + ":"
              ).grid(row = 5, column = 4, sticky = "NEWS")
        # row 6
        self.classif = StringVar()
        self.classif.set("--")
        Label(self.window,
              textvariable = self.classif,
              ).grid(row = 6, column = 0, sticky = "NEWS")

        self.perc = StringVar()
        self.perc.set("--")
        Label(self.window,
              textvariable = self.perc,
              ).grid(row = 6, column = 2, sticky = "NEWS")

        self.timef = StringVar()
        self.timef.set("--")
        Label(self.window,
              textvariable = self.timef,
              ).grid(row = 6, column = 4, sticky = "NEWS")
        # row 7
        Label(self.window,
              text = labels['modifier'][self.lang] + ":"
              ).grid(row = 7, column = 0, sticky = "NEWS")

        self.modif = StringVar()
        self.modif.set("--")
        Label(self.window,
              textvariable = self.modif
              ).grid(row = 7, column = 2, sticky = "NEWS")
        # row 8
        self.desc = StringVar()
        self.desc.set("")
        Label(self.window,
              wraplength = 700,
              textvariable = self.desc
              ).grid(row = 8,
                     rowspan = 2,
                     column = 0,
                     columnspan = 5,
                     sticky = "NEWS")


    def _fillSkill(self, event):
        '''
        Depending on the selected category fill the skill listbox
        '''

        self.skilllb.delete(0, END)
        selcat = self.catlb.curselection()
        self.catlabel.config(text = "")

        if selcat != ():
            self.category = self.catlb.get(selcat[0])
            self.catlabel.config(text = self.category)
            self.skilllabel.config(text = "")

            for skill in self.character["cat"][self.category]["Skill"].keys():

                if skill not in ["Progression", "Stats"] and skill[-1] != "+":
                    self.skilllb.insert(END, skill)

                else:
                    print("-->".format(skill))


    def _getSkill(self, event):
        '''
        Getting selected Skill
        '''
        selskill = self.skilllb.curselection()

        if selskill != ():
            self.skill = self.skilllb.get(selskill[0])
            self.skilllabel.config(text = self.skill)

        logger.debug(f"selelcted skill {self.skill}")


    def _getMan(self, event):
        '''
        Get maneuver level
        '''

        selman = self.manlb.curselection()

        if selman != ():
            self.man = self.manlb.get(selman[0])
            self.manlabel.configure(text = self.man)

        logger.debug(f"maneuver: {self.category} - {self.skill} - {self.man}")


    def _rollDice(self):
        '''!
        This trows a d100. Result ist ([dice result], [unmodified])
        ----
        @todo set dice(rules="RM")
        '''
        self.result = self.dice()

        if self.result[1] == []:
            self.diceroll.set(str(self.result[0][0]))

        else:
            self.diceroll.set("um {}".format(self.result[1][0]))


    def _chkResult(self):
        '''
        '''
        dummy = self.diceroll.get()
        um = re.compile(r"(um|Um|UM) ([0-9]{1,3})")
        sr = re.compile(r"[-]*[0-9]+")

        if um.match(dummy):
            self.total = int(um.match(dummy).group(2))

        elif sr.match(dummy):
            self.total = int(sr.match(dummy).group())

        else:
            self.total = 0

        if self.category:
            skilladd = self.character["cat"][self.category]["total bonus"]
            logger.info("total category bonus added")
            logger.debug(f"{self.category}: {skilladd}")

            if self.skill:
                skilladd = self.character["cat"][self.category]["Skill"][self.skill]["total bonus"]
                logger.info("total skill bonus added")
                logger.debug(f"{self.skill}:{skilladd}")

        mod = self.mod.get()
        man = maneuvers[self.man]["mod"]
        self.total += skilladd + mod + man

        if "Spell" not in self.category or "Runes" in self.skill:
            self.probe = self.mantab.checkRoll(self.total)
            logger.debug(f"non-spell result: {self.probe} ")

        else:
            self.probe = self.spelltab.checkRoll(self.total)
            logger.debug(f"spell result: {self.probe} ")

        self._updTotal()


    def _updTotal(self):
        """!
        Refreshes the displayed total bonus from self.total and the
        classification fields (classification, success percent, timef,
        modificator, description) from the last checkRoll probe.
        """
        self.totallabel.set(str(self.total))
        self.classif.set(self.probe["classification"])
        self.perc.set(self.probe['success'])
        self.timef.set(self.probe['time'])
        self.modif.set(self.probe['mod'])
        self.desc.set(self.probe['description'])
#    def maneuver_ep(self, manlvl = "routine", number = 0):
#        '''
#        Adds EPs by maneuvers.
#        @param manlvl difficulty of maneuver
#        @param number number of maneuvers of this level
#        '''
#        from rpgToolDefinitions.epcalcdefs import maneuvers
#
#        self.man_ep += maneuvers[manlvl]['ep'] * number


if __name__ == '__main__':
    with open("/home/mongol/git/rpg-tools/src/data/groups/charparty.json", "r") as fp:
        cl = json.load(fp)

    mantan = rpg.statManeuver
    rrtab = rpg.RRroll

    win = EPCalcWin()
