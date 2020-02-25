'''
\file latexexport.py
\package rpgtoolbox.latexexport
\brief Export class for LaTeX

This holds a class to export a character JSON to a LaTeX file from which a PDF
will be generated for printouts
.
\date (C) 2016-2020
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.1
'''

__updated__ = "22.02.2020"
__author__ = "Marcus Schwamberger"
__copyright__ = "(C) 2015-" + __updated__[-4:] + " " + __author__
__email__ = "marcus@lederzeug.de"
__version__ = "1.1"
__license__ = "GNU V3.0"
__me__ = "A RPG tool package for Python 3.6"

from gui.window import messageWindow
from rpgtoolbox import logbox as log
#from rpgtoolbox.rolemaster import stats
import json
import os
import sys
import string

logger = log.createLogger('latexreport', 'debug', '1 MB', 1, './')



def readFile(filename = ""):
    '''
    This reads a text file/LaTeX template file
    @param filename path + name of the file to read
    @retval content content of the file
    '''
    content = ""

    if type(filename) == type("") and filename != "":
        fp = open(filename, "r")
        content = fp.read()
        fp.close()
        logger.info("readFile: {} read successfully".format(filename))
        logger.debug("readFile: file content\n{}\n".format(content))

    else:
        logger.warn("readFile: wrong/missing filename '{}'".format(filename))
        print("WARN: latexreport_readFile: no filename")

    return content



def saveFile(filename = "", content = ""):
    '''
    This saves a file
    @param filename path + name of the file to store
    @param content content to store in the file
    '''
    fp = open(filename, "w")
    fp.write(content)
    fp.close()
    logger.info("saveFile: {} successfully saved.".format(filename))
    print("{} successfully saved.".format(filename))



class charsheet(object):
    '''
    This class generates LaTeX code from character's data
    '''


    def __init__(self, char = {}, storepath = "./", short = True):
        '''
        Constructor:
        @param char character data in a dictionary
        @param storepath configured store path.
        @param short a flag parameter whether the export should be short (no skills
                     with rank = 0) or long (all skills)
        '''
        from rpgtoolbox.rolemaster import stats
        self.char = char
        self.storepath = storepath
        self.short = short
        self.stats = stats
        self.createMainLatex()
        self.createGenInfo()
        self.createStats()
        self.createRRATDB()
        self.createCatSkill()
        self.execLaTeX()


    def createMainLatex(self):
        '''
        Creates the main LaTeX file from template and saves it into a sub directory
        of the characters saving path
        '''
        self.chardir = self.storepath + self.char['player']

        if not os.path.exists(self.chardir + "/latex"):
            os.makedirs(self.chardir + "/latex")
            logger.info("createMainLatex: created {}".format(self.chardir + "/latex"))

        template = readFile(self.storepath + "/default/latex/template_charsheet.tex")
        logger.info("createMainLatex: read {}".format(self.storepath + "/default/latex/template_charsheet.tex"))

        template = template.replace("name_", self.char["name"].replace(" ", "-") + "_")

        logger.info("createMainLatex: converted template")

        saveFile("{}/latex/{}.tex".format(self.chardir, self.char['name'].replace(" ", "-")), template)
        logger.info("createMainLatex: {}/latex/{}.tex saved".format(self.chardir, self.char['name'].replace(" ", "-")))


    def createGenInfo(self):
        '''
        This creates the LaTeX file with the general character information (background info)
        '''
        data = ["name", "prof", "race", "culture", "lord", "parents", "siblings", "partner",
                "children", "deity", "sex", "skin", "eyes", "hair", "height", "weight", "app_age",
                "act_age", "looking", "soul dep", "recovery", "pprecovery", "lvl", "piclink",
                "pers", "motiv", "exp", "home"]
        self.chardir += "/latex/"

        template = readFile(self.storepath + "/default/latex/template_gen_info.tex")
        logger.info("createGenInfo: read {}".format(self.storepath + "/default/latex/template_gen_info.tex"))
        template = template.replace("==>realm", str(self.char['realm']).replace(", ", "/").strip("[]"))
        for index in data:

            if index in self.char.keys():
                print(index)
                if index == "soul dep":
                    template = template.replace("==>souldeparture", str(self.char[index]).strip("[]") + " rd")
                else:
                    template = template.replace("==>" + index, str(self.char[index]).strip("[]"))

            elif index in self.char["background"].keys():
                template = template.replace("==>" + index, str(self.char['background'][index]))

            elif index == "recovery":
                rest = 1
                if round(self.char["Co"]["total"] / 2) > rest:
                    rest = round(self.char["Co"]["total"] / 2)

                sleepcycle = 1
                if self.char["Co"]["total"] * 2 > sleepcycle:
                    sleepcycle = self.char["Co"]["total"] * 2
                template = template.replace("==>recovery", "1 p. 3h/{} p. 1h pause/{} p. 3h zzZZZ".format(rest, sleepcycle))

            elif index == "pprecovery":
                sleepcycle = 1

                if round(self.char["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"] / 2) >= 1:
                    sleepcycle = round(self.char["cat"]["Power Point Development"]["Skill"]["Power Point Development"]["total bonus"] / 2)
                rest = 1

                if self.char["realm"] == "Essence" and round(self.char["Em"]["total"] / 2) > 1:
                    rest = round(self.char["Em"]["total"] / 2)

                elif self.char['realm'] == "Channeling" and round(self.char["In"]["total"] / 2) > 1:
                    rest = round(self.char["Em"]["total"] / 2)

                elif self.char['realm'] == "Mentalism" and round(self.char["Pr"]["total"] / 2) > 1:
                    rest = round(self.char["Pr"]["total"] / 2)

                elif type(self.char["realm"]) == type([]):

                    for realm in self.char["realm"]:
                        calc = 0

                        if realm == "Essence":
                            calc += self.char["Em"]["total"]

                        elif realm == "Channeling":
                            calc += self.char["In"]["total"]

                        elif realm == "Mentalism":
                            calc += self.char["Pr"]["total"]

                    calc = round(calc / 4)

                    if calc > rest:
                        rest = calc

                template = template.replace("==>pprecovery", "1 p. 3h/{} p. 1h pause/{} p. 3h zzZZZ".format(rest, sleepcycle))
            else:
                template = template.replace("==>" + index, u"\_\_\_\_\_")

        saveFile(self.chardir + "{}_gen_info.tex".format(self.char['name'].replace(" ", "-")), template)


    def createStats(self):
        '''
        This creates a LaTeX file with character stats from LaTeX template
        '''
        template = readFile(self.storepath + "/default/latex/template_stats.tex")
        vals = ["pot", "race", "spec", "std", "temp", "total"]

        for s in self.stats:
            for v in vals:
                template = template.replace("==>{}_{}".format(s, v), str(self.char[s][v]))

        saveFile(self.chardir + "{}_stats.tex".format(self.char['name'].replace(" ", "-")), template)


    def createRRATDB(self):
        '''
        This creates a LaTeX sheet with RR, DB, AT
        '''
        vals = ["RRArc", "RRC/E", "RRChan", "RRDisease", "RRE/M", "RRC/M", "RREss", "RRFear",
              "RRMent", "RRPoison"]

        template = readFile(self.storepath + "/default/latex/template_rr_at_db.tex")
        template = template.replace("==>ThreeQ", str(int(self.char["Qu"]["total"]) * 3))

        for v in vals:
            template = template.replace("==>{}".format(v), str(int(self.char[v])))

        saveFile(self.chardir + "{}_rr_at_db.tex".format(self.char['name'].replace(" ", "-")), template)


    def createCatSkill(self):
        '''
        This creates a category/skill LaTeX sheet
        '''
        self.catlist = list(self.char['cat'].keys())
        self.catlist.sort()
        catstd = u"{} & {} & {} & {} & {} & {} &{} &{} &{}&{}\\\\\n"
        skillpre = u"\hspace{4mm} "
        skillval = u"{} & {} & {} & {} & {} & {} &{} &-- &{}&{}\\\\\n"
        weapon = u"\\rowcolor{Red!30} "
        spell = u"\\rowcolor{ProcessBlue!30} "
        devel = u"\\rowcolor{Green!30} "
        datatable = ""

        for cat in self.catlist:
            datatable += u"\\hline\n"
            if "Weapon" in cat:
                datatable += weapon + catstd.format(cat,
                                                  str(self.char['cat'][cat]['Progression']).replace(", ", "/"),
                                                  str(self.char['cat'][cat]['Costs']).replace(", ", "/"),
                                                  str(self.char['cat'][cat]['rank']),
                                                  str(self.char['cat'][cat]['rank bonus']),
                                                  str(self.char['cat'][cat]['stat bonus']),
                                                  str(self.char['cat'][cat]['spec bonus']),
                                                  str(self.char['cat'][cat]['prof bonus']),
                                                  str(self.char['cat'][cat]['item bonus']),
                                                  str(self.char['cat'][cat]['total bonus'])
                                                  )
                skilllist = list(self.char['cat'][cat]['Skill'].keys())
                skilllist.sort()

                for skill in skilllist:
                    if skill not in ['Progression', 'Costs'] and "+" not in skill:

                        if self.short:

                            if self.char['cat'][cat]["Skill"][skill]["rank"] > 0:
                                datatable += weapon + skillpre + skillval.format(skill,
                                                                             str(self.char['cat'][cat]["Skill"][skill]['Progression']).replace(", ", "/"),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['Costs']).replace(", ", "/"),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['rank']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['rank bonus']),
                                                                             "--",
                                                                             str(self.char['cat'][cat]["Skill"][skill]['spec bonus']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['item bonus']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['total bonus'])
                                                                             )

                        else:
                            datatable += weapon + skillpre + skillval.format(skill,
                                                                         str(self.char['cat'][cat]["Skill"][skill]['Progression']).replace(", ", "/"),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['Costs']).replace(", ", "/"),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['rank']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['rank bonus']),
                                                                         "--",
                                                                         str(self.char['cat'][cat]["Skill"][skill]['spec bonus']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['item bonus']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['total bonus'])
                                                                         )

            elif "Development" in cat:
                datatable += devel + catstd.format(cat,
                                                  str(self.char['cat'][cat]['Progression']).replace(", ", "/"),
                                                  str(self.char['cat'][cat]['Costs']).replace(", ", "/"),
                                                  str(self.char['cat'][cat]['rank']),
                                                  str(self.char['cat'][cat]['rank bonus']),
                                                  str(self.char['cat'][cat]['stat bonus']),
                                                  str(self.char['cat'][cat]['spec bonus']),
                                                  str(self.char['cat'][cat]['prof bonus']),
                                                  str(self.char['cat'][cat]['item bonus']),
                                                  str(self.char['cat'][cat]['total bonus'])
                                                  )
                skilllist = list(self.char['cat'][cat]['Skill'].keys())
                skilllist.sort()

                for skill in skilllist:

                    if skill not in ['Progression', ['Costs']] and "+" not in skill:

                        if self.short:

                            if self.char['cat'][cat]["Skill"][skill]["rank"] > 0:
                                datatable += devel + skillpre + skillval.format(skill,
                                                                             str(self.char['cat'][cat]["Skill"][skill]['Progression']).replace(", ", "/"),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['Costs']).replace(", ", "/"),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['rank']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['rank bonus']),
                                                                             "--",
                                                                             str(self.char['cat'][cat]["Skill"][skill]['spec bonus']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['item bonus']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['total bonus'])
                                                                             )
                        else:
                            datatable += devel + skillpre + skillval.format(skill,
                                                                         str(self.char['cat'][cat]["Skill"][skill]['Progression']).replace(", ", "/"),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['Costs']).replace(", ", "/"),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['rank']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['rank bonus']),
                                                                         "--",
                                                                         str(self.char['cat'][cat]["Skill"][skill]['spec bonus']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['item bonus']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['total bonus'])
                                                                         )

            elif "Spells" in cat:
                datatable += spell + catstd.format(cat,
                                                  str(self.char['cat'][cat]['Progression']).replace(", ", "/"),
                                                  str(self.char['cat'][cat]['Costs']).replace(", ", "/"),
                                                  str(self.char['cat'][cat]['rank']),
                                                  str(self.char['cat'][cat]['rank bonus']),
                                                  str(self.char['cat'][cat]['stat bonus']),
                                                  str(self.char['cat'][cat]['spec bonus']),
                                                  str(self.char['cat'][cat]['prof bonus']),
                                                  str(self.char['cat'][cat]['item bonus']),
                                                  str(self.char['cat'][cat]['total bonus'])
                                                  )
                skilllist = list(self.char['cat'][cat]['Skill'].keys())
                skilllist.sort()

                for skill in skilllist:

                    if skill not in ['Progression', 'Costs', 'Stats'] and "+" not in skill:

                        if self.short:

                            if self.char['cat'][cat]['Skill'][skill]["rank"] > 0:
                                datatable += spell + skillpre + skillval.format(skill,
                                                                             str(self.char['cat'][cat]["Skill"][skill]['Progression']).replace(", ", "/"),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['Costs']).replace(", ", "/"),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['rank']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['rank bonus']),
                                                                             str("--"),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['spec bonus']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['item bonus']),
                                                                             str(self.char['cat'][cat]["Skill"][skill]['total bonus'])
                                                                             )
                        else:
                            datatable += spell + skillpre + skillval.format(skill,
                                                                         str(self.char['cat'][cat]["Skill"][skill]['Progression']).replace(", ", "/"),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['Costs']).replace(", ", "/"),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['rank']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['rank bonus']),
                                                                         str("--"),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['spec bonus']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['item bonus']),
                                                                         str(self.char['cat'][cat]["Skill"][skill]['total bonus'])
                                                                         )

            else:
                datatable += catstd.format(cat,
                                           str(self.char['cat'][cat]['Progression']).replace(", ", "/"),
                                           str(self.char['cat'][cat]['Costs']).replace(", ", "/"),
                                           str(self.char['cat'][cat]['rank']),
                                           str(self.char['cat'][cat]['rank bonus']),
                                           str(self.char['cat'][cat]['stat bonus']),
                                           str(self.char['cat'][cat]['spec bonus']),
                                           str(self.char['cat'][cat]['prof bonus']),
                                           str(self.char['cat'][cat]['item bonus']),
                                           str(self.char['cat'][cat]['total bonus'])
                                           )
                skilllist = list(self.char['cat'][cat]['Skill'].keys())
                skilllist.sort()

                for skill in skilllist:
                    if skill not in ['Progression', ['Costs']] and "+" not in skill:

                        if self.short:

                            if self.char['cat'][cat]['Skill'][skill]["rank"] > 0:
                                datatable += skillpre + skillval.format(skill,
                                                                        str(self.char['cat'][cat]["Skill"][skill]['Progression']).replace(", ", "/"),
                                                                        str(self.char['cat'][cat]["Skill"][skill]['Costs']).replace(", ", "/"),
                                                                        str(self.char['cat'][cat]["Skill"][skill]['rank']),
                                                                        str(self.char['cat'][cat]["Skill"][skill]['rank bonus']),
                                                                        "--",
                                                                        str(self.char['cat'][cat]["Skill"][skill]['spec bonus']),
                                                                        str(self.char['cat'][cat]["Skill"][skill]['item bonus']),
                                                                        str(self.char['cat'][cat]["Skill"][skill]['total bonus'])
                                                                        )

                        else:
                            datatable += skillpre + skillval.format(skill,
                                                                    str(self.char['cat'][cat]["Skill"][skill]['Progression']).replace(", ", "/"),
                                                                    str(self.char['cat'][cat]["Skill"][skill]['Costs']).replace(", ", "/"),
                                                                    str(self.char['cat'][cat]["Skill"][skill]['rank']),
                                                                    str(self.char['cat'][cat]["Skill"][skill]['rank bonus']),
                                                                    "--",
                                                                    str(self.char['cat'][cat]["Skill"][skill]['spec bonus']),
                                                                    str(self.char['cat'][cat]["Skill"][skill]['item bonus']),
                                                                    str(self.char['cat'][cat]["Skill"][skill]['total bonus'])
                                                                    )

        template = readFile(self.storepath + "/default/latex/template_catskill.tex")
        template = template.replace("==>fulltable", datatable)
        saveFile(self.chardir + "{}_catskill.tex".format(self.char['name'].replace(" ", "-")), template)


    def createSpells(self):
        '''
        This makes a sheet with all learned spells
        @todo this has to be fully implemented
        '''
        print("not done yet")


    def execLaTeX(self):
        '''
        This executes LaTeX to generate a PDF character sheet and tries to open it with default viewer.
        '''
        currpath = os.getcwd()
        os.chdir(self.chardir)
        try:
            # to get the right table formating LaTeX has to be run twice
            os.system("pdflatex {}.tex".format(self.char['name'].replace(" ", "-")))
            os.system("pdflatex {}.tex".format(self.char['name'].replace(" ", "-")))
            windoman = ["/usr/bin/xdg-open", "/usr/bin/gnome-open", "/usr/bin/kde-open", "/usr/bin/open"]

            for wm in windoman:
                if os.path.isfile(wm):
                    os.system("{} {}.pdf".format(wm, self.char['name'].replace(" ", "-")))

        except Exception as error:
            print("ERROR: Could not execute PDF LaTex! Please try it manually!!\n{}".format(error))
            logger.error("execLaTeX: {}".format(error))

        finally:
            os.chdir(currpath)
