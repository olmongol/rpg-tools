#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
\package rpgtoolbox.chartotext
\file chartotext.py

\brief  brief description
Detailed description

\author Marcus Schwamberger
\email marcus@lederzeug.de
\date 22.09.2018
\copyright 2018
\version 0.1
\license GNU V3.0
'''
__updated__ = "01.01.2000"
__me__ = "/home/mongol/git/rpg-tools/src/rpgtoolbox/chartotext.py"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__copyright__ = "2018 - %s" % __updated__[-4:]
__version__ = "0.1"

import sys
import os
import json
from rpgtoolbox.globaltools import readJSON as readChar
from rpgtoolbox.globaltools import readFile, writeFile
from string import Template



class template(Template):
    '''
    Template class with delimiter '==>' instead '$'.
    '''
    delimiter = "==>"
    idpattern = r'[a-z][_a-z0-9]*'



class latexsheets(object):
    '''
    This Class transforms the JSON data of a character into a LaTeX file to generate a printable character sheet.
    '''


    def __init__(self, charfile = None, defaultpath = "./data/default"):
        '''
        Constructor of a chartolatex object.

        @param charfile path and name of the character file to transform into a latex document.
        '''
        self.charfile = charfile
        self.__tmplfiles = {'main':'template_charsheet.tex',
                            'general' : 'template_gen_info.tex',
                            'categories':'template_cats.tex',
                            'skills': 'template_skills.tex',
                            'rr_at_db': 'template_rr_at_db.tex',
                            'stats': 'template_stats.tex',
                            'spells' : 'template_spells.tex',
                            'training': 'template_trainpack.tex'
                            }

        if defaultpath[-1] != "/":
            self.latextmplpath = defaultpath + "/latex/"

        else:
            self.latextmplpath = defaultpath + "latex/"

        if not charfile:
            print("ERROR: No character file given. Exiting...")
            sys.exit(1)

        else:
            self.character = readChar(self.charfile)

            if "/" in charfile:
                self.latexoutpath = charfile[:charfile.rfind("/") + 1] + "output/"

            else:
                self.latexoutpath = "./output/"

            if not os.path.exists(self.latexoutpath):
                os.makedirs(self.latexoutpath)


    def createLatexFile(self, page = "main", data = {}):
        '''
        Creates given Latex file.
        '''
        content = readFile(self.latextmplpath + self.__tmplfiles[page])
        content = template(content)
        output = content.safe_substitute(data)
        writeFile(self.latexoutpath, self.__tmplfiles[page].replace('template', self.character['name']), output)


    def selectData(self, page = 'main'):
        '''
        This constructs a data set for each LaTeX file
        '''
        if page == "main":
            data = {}
            elements = self.__tmplfiles.values()

            for i in range(0, len(elements)):
                elements[i] = elements[i].replace("template", "")[:-4]

            data['name' + elements[i]] = self.character['name'] + elements[i]

        elif page == "general":
            data = {}
            elements = ['name', 'profession', 'race', 'culture', 'hometown', 'lord', 'parents', 'siblings', 'partner', 'children', 'deity',
                      'gender', 'skin', 'eyes', 'hair', 'size', 'weight', 'apparentage', 'actualage', 'looking', 'souldepature', 'recovery', 'lvl',
                      'jpg', 'description', 'motivation', 'realm', 'exp']

            for item in elements:

                if item in self.character.keys():
                    data[item] = self.character[item]

                else:
                    data[item] = " --"

        elif page == "categories":
            data = {}
            pass

        elif page == "skills":
            data = {}
            pass

        elif page == "rr_at_db":
            data = {}
            elements = ["RRChan", "RRFear", "RRDisease", "RREss", "RRMent", "RRArc", "RRPoison", "RRC/M", "RRE/M", "RRC/E"]
            for item in elements:

                if item in self.character.keys():
                    data[item] = self.character[item]

                else:
                    data[item] = " --"

        elif page == "stats":
            data = {}
            elements = ["Pr_temp", "Pr_pot", "Pr_std", "Pr_race", "Pr_spec", "Pr_total",
                        "Me_temp", "Me_pot", "Me_std", "Me_race", "Me_spec", "Me_total",
                        "Qu_temp", "Qu_pot", "Qu_std", "Qu_race", "Qu_spec", "Qu_total",
                        "St_temp", "St_pot", "St_std", "St_race", "St_spec", "St_total",
                        "Em_temp", "Em_pot", "Em_std", "Em_race", "Em_spec", "Em_total",
                        "Ag_temp", "Ag_pot", "Ag_std", "Ag_race", "Ag_spec", "Ag_total",
                        "Re_temp", "Re_pot", "Re_std", "Re_race", "Re_spec", "Re_total",
                        "Co_temp", "Co_pot", "Co_std", "Co_race", "Co_spec", "Co_total",
                        "In_temp", "In_pot", "In_std", "In_race", "In_spec", "In_total",
                        "SD_temp", "SD_pot", "SD_std", "SD_race", "SD_spec", "SD_total"
                        ]

            for elem in elements:
                stat, stattype = elem.split('_')
                data[elem] = self.character[stat][stattype]

        elif page == "spells":
            data = {}
            pass

        elif page == "training":
            data = {}
            pass

        return data
