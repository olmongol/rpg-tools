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

__updated__ = "17.06.2020"
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
from rpgToolDefinitions.inventory import *
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
        template = template.replace("==>AdrenalDef", str(self.char["cat"]["Special Defenses"]["Skill"]["Adrenal Defense"]["total bonus"]))
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



class spellbook(object):
    '''
    This class generates a LaTeX file for all learned spells of a character and
    compiles it into a PDF.
    '''


    def __init__(self, character = {}, storepath = "./data/"):
        '''
        Class constructor
        @param character dictionary which hold full character data.
        @param storepath path to the main storage directory.
        '''
        self.character = character
        self.storepath = storepath

        if self.storepath[-1] != "/" and self.storepath[-1] != "\\":
            self.storepath += "/"

        self.charpath = "{}{}/latex/".format(self.storepath, self.character["player"])
        self.fn = "{}_spellbook.tex".format(self.character["name"])

        fp = open("{}default/latex/template_spellbook.tex".format(self.storepath), "r")
        self.latex = fp.read()
        fp.close()

        self.exportSB()
        self.compilePDF()


    def exportSB(self):
        '''
        This method extracts all spell list data from character and builds the
        LaTeX spellbook
        '''
        for  cat in self.character['cat']:

            if "Spells - " in cat:

                for SL in self.character["cat"][cat]["Skill"].keys():

                    if SL not in  ["Stats", "Progression", "Spell List+"]:
                        if self.character["cat"][cat]["Skill"][SL]["rank"] > 0:
                            self.latex += "\n\\chapter*{\\yinitpar{%s}%s \\newline %s}\n" % (SL[0], SL[1:], cat[9:])
                            self.latex += r"\rowcolors{1}{}{lightgray}" + "\n" + r"\begin{longtable}{clccccp{5.5cm}}" + "\n"
                            self.latex += r"    \multicolumn{1}{c}{\textcolor{red}{Lvl}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Spell}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Area of Effect}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Duration}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Range}}&" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Type}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Description}}\\" + "\n" + \
                                          r"\endfirsthead" + "\n\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Lvl}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Spell}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Area of Effect}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Duration}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Range}}&" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Type}} &" + "\n" + \
                                          r"    \multicolumn{1}{c}{\textcolor{red}{Description}}\\" + "\n" + \
                                          r"\endhead" + "\n\n"

                            if "Spells" in self.character["cat"][cat]["Skill"][SL].keys():
                                if self.character["cat"][cat]["Skill"][SL]["Spells"] != []:
                                    for spell in self.character["cat"][cat]["Skill"][SL]["Spells"]:
                                        if self.character["cat"][cat]["Skill"][SL]["rank"] >= int(spell["Lvl"]):
                                            print("Spell: ", spell["Spell"])
                                            self.latex += "\n%s & %s & %s & %s & %s  & %s & %s\\\\\n" % (spell["Lvl"],
                                                                                                   spell["Spell"],
                                                                                                   spell["Area of Effect"],
                                                                                                   spell["Duration"],
                                                                                                   spell["Range"],
                                                                                                   spell["Type"],
                                                                                                   spell["Description"]
                                                                                                   )
                            self.latex += "\\end{longtable}\n\n"
                            if "Special Notes" in self.character["cat"][cat]["Skill"][SL].keys():
                                if len(self.character["cat"][cat]["Skill"][SL]["Special Notes"]) > 0:
                                    self.latex += "\\yinitpar{%s}%s\\\n\n" % (self.character["cat"][cat]["Skill"][SL]["Special Notes"][0][0],
                                                                      self.character["cat"][cat]["Skill"][SL]["Special Notes"][0][1:]
                                                                          )
        self.latex += "\n\\end{document}"
        if not os.path.exists(self.charpath):
            os.mkdir(self.charpath)

        fp = open(self.charpath + self.fn.replace(" ", "_"), "w")
        fp.write(self.latex)
        fp.close()


    def compilePDF(self):
        '''
        This runs the pdflatex compiler to generate the PDF
        '''
        currpath = os.getcwd()
        os.chdir(self.charpath)
        try:
            # to get the right table formating LaTeX has to be run twice
            os.system("pdflatex {}".format(self.fn.replace(" ", "_")))
            os.system("pdflatex {}".format(self.fn.replace(" ", "_")))
            windoman = ["/usr/bin/xdg-open", "/usr/bin/gnome-open", "/usr/bin/kde-open", "/usr/bin/open"]

            for wm in windoman:
                if os.path.isfile(wm):
                    os.system("{} {}.pdf".format(wm, self.fn.replace(" ", "_")[:-4]))

        except Exception as error:
            print("ERROR: Could not execute PDF LaTex! Please try it manually!!\n{}".format(error))
            logger.error("compilePDF: {}".format(error))

        finally:
            os.chdir(currpath)



class inventory(object):
    '''
    This class generates an inventory PDF from a character file if the character has an inventory.
    '''


    def __init__(self, character = {}, storepath = "./data/"):
        '''
        Class constructor
        @param character dictionary holding character's data
        @param storepath path to the main storage directory
        '''
        self.character = character
        self.storepath = storepath

        if self.storepath[-1] != "/" and self.storepath[-1] != "\\":
            self.storepath += "/"

        self.charpath = "{}{}/latex/".format(self.storepath, self.character["player"])
        self.fn = "{}_inventory.tex".format(self.character["name"])

        fp = open("{}default/latex/template_inventory.tex".format(self.storepath), "r")
        self.latex = fp.read()
        fp.close()

        self.prepTemplate()
        self.tblArmor()
        self.tblWeapon()
        self.tblGear()
        self.tblHerb()
        self.tblGems()
        self.latex += "\n\\end{document}"
        self.saveLatex()
        self.compilePDF()


    def prepTemplate(self):
        '''
        This exchanges the placeholder of the template with data from character's dictionary.
        '''
        rplmt = ["MMP", "carried", "name"]
        rpurse = ["MP", "PP", "GP", "SP", "BP", "CP", "TP", "IP"]

        for r  in rplmt:

            if r in self.character.keys():
                self.latex = self.latex.replace("==>{}".format(r), str(self.character[r]))

            else:
                self.latex = self.latex.replace("==>{}".format(r), "\_\_\_\_")

        if "purse" in self.character.keys():

            for r in rpurse:

                if r in self.character["purse"].keys():
                    self.latex = self.latex.replace("==>{}".format(r), str(self.character["purse"][r]))

                else:
                    self.latex = self.latex.replace("==>{}".format(r), "0")
        else:

            for r in rpurse:
                self.latex = self.latex.replace("==>{}".format(r), "0")


    def tblArmor(self):
        """
        this creates a table with all armor pieces.
        ----
        @todo has to be fully implemented
        """
        self.latex += "\n\\section*{\\textcolor{Maroon}{Armor}}"
        pass


    def tblWeapon(self):
        """
        this creates a table with all weapons.
        ----
        @todo has to be fully implemented
        """
        self.latex += "\n\\section*{\\textcolor{Maroon}{Weapons}}\n"
        # melee combat ---------------------
        self.latex += """
        {\\fontsize{7pt}{7pt}
            \\selectfont
        \\begin{longtable}{|p{2.5cm}|p{1.5cm}|p{1.5cm}|p{1cm}|p{0.5cm}|p{3cm}|p{7cm}|}
            \\caption*{\\textcolor{Maroon}{\\textbf{Weapons: Melee Combat}}}\\\\
            \\hline
            \\textbf{Name} & \\textbf{break\\#} & \\textbf{fumble} & \\textbf{strength} &\\textbf{bonus} &\\textbf{category/skill} &\\textbf{description}\\\\
            \\hline
            \\endfirsthead
            \\multicolumn{7}{c} {\\tablename\\ \\thetable\\ --\\textit{Continued from previous page}}\\\\
            \\hline
            \\textbf{Name} & \\textbf{break\\#} & \\textbf{fumble} & \\textbf{strenght} &\\textbf{bonus} &\\textbf{category/skill} &\\textbf{description}\\\\
            \\hline
            \\endhead
            \\hline
            \\multicolumn{7}{r}{\\textit{continued on next page..}}\\\\
            \\endfoot
            \\hline
            \\endlastfoot
        """
        for weapon in self.character["inventory"]["weapon"]:
            if weapon["breakage"] != "---" and weapon["strength"] != "---" and weapon["wtype"] not in ["th", "mis"]:
                rcolor = ""
                descadd = ""
                if weapon["magic"]:
                    rcolor = "\\rowcolor{ProcessBlue!30}"
                    descadd += ", magic weapon"
                if weapon["mithril"]:
                    rcolor = "\\rowcolor{Yellow!30}"
                    descadd += ", mithril weapon"
                if weapon["holy"]:
                    rcolor = "\\rowcolor{Green!30}"
                    descadd += ", holy weapon"
                if weapon["slaying"] != "":
                    rcolor = "\\rowcolor{Red!30}"
                    descadd += ", slaying weapon ({})".format(weapon["slaying"])
                self.latex += rcolor + " {} & {} & {} & {} & {} & {} & {}\\\\\n".format(weapon["name"],
                                                                                     weapon["breakage"] + " " + str(weapon["soft/wooden"]),
                                                                                     weapon["fumble"],
                                                                                     weapon["strength"],
                                                                                     weapon["bonus"],
                                                                                     weapon["skill"],
                                                                                     weapon["description"] + descadd
                                                                                     )

        self.latex += "\\end{longtable}\n"
        self.latex += "}\n"
        # ranged combat ----------------------
        self.latex += """
        {\\fontsize{7pt}{7pt}
            \\selectfont
        \\begin{longtable}{|p{2cm}|p{1cm}|p{0.7cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{1.2cm}|p{2.5cm}|p{3.5cm}|}
            \\caption*{\\textcolor{Maroon}{\\textbf{Weapons: Ranged Combat}}}\\\\
            \\hline
            \\textbf{Name} & \\textbf{fumble} &\\textbf{bonus}& \\textbf{near} & \\textbf{short} &\\textbf{mediumm} &\\textbf{long}& \\textbf{extreme} &\\textbf{category/skill} &\\textbf{description}\\\\
            \\hline
            \\endfirsthead
            \\multicolumn{10}{c} {\\tablename\\ \\thetable\\ --\\textit{Continued from previous page}}\\\\
            \\hline
            \\textbf{Name} & \\textbf{fumble} & \\textbf{bonus}&\\textbf{near} & \\textbf{short} &\\textbf{medium} &\\textbf{long}& \\textbf{extreme}&\\textbf{category/skill} &\\textbf{description}\\\\
            \\hline
            \\endhead
            \\hline
            \\multicolumn{10}{r}{\\textit{continued on next page..}}\\\\
            \\endfoot
            \\hline
            \\endlastfoot

        """
        for weapon in self.character["inventory"]["weapon"]:
            if weapon["near"] != "---":
                rcolor = ""
                descadd = ""
                if weapon["magic"]:
                    rcolor = "\\rowcolor{ProcessBlue!30}"
                    descadd += ", magic weapon"
                if weapon["mithril"]:
                    rcolor = "\\rowcolor{Yellow!30}"
                    descadd += ", mithril weapon"
                if weapon["holy"]:
                    rcolor = "\\rowcolor{Green!30}"
                    descadd += ", holy weapon"
                if weapon["slaying"] != "":
                    rcolor = "\\rowcolor{Red!30}"
                    descadd += ", slaying weapon ({})".format(weapon["slaying"])

                self.latex += rcolor + " {} & {} & {} & {} & {} & {} & {} & {} & {} & {}\\\\\n".format(weapon["name"],
                                                                                              weapon["fumble"],
                                                                                              weapon["bonus"],
                                                                                              weapon["near"],
                                                                                              weapon["short"],
                                                                                              weapon["medium"],
                                                                                              weapon["long"],
                                                                                              weapon["extreme"],
                                                                                              weapon["skill"],
                                                                                              weapon["description"] + descadd
                                                                                              )

        self.latex += "\\end{longtable}\n"
        self.latex += "}\n"
        # Weapon description ------------------
        self.latex += """
        {\\fontsize{7pt}{7pt}
            \\selectfont
        \\begin{longtable}{|p{2.5cm}|p{1.5cm}|p{2.5cm}|p{2.5cm}|p{3.5cm}|p{5cm}|}
            \\caption*{\\textcolor{Maroon}{\\textbf{Weapons: Further Information}}}\\\\
            \\hline
            \\textbf{Name} & \\textbf{length} & \\textbf{weight} & \\textbf{worth} &\\textbf{location} &\\textbf{description}\\\\
            \\hline
            \\endfirsthead
            \\multicolumn{6}{c} {\\tablename\\ \\thetable\\ --\\textit{Continued from previous page}}\\\\
            \\hline
            \\textbf{Name} & \\textbf{length} & \\textbf{weight} & \\textbf{worth} &\\textbf{location} &\\textbf{description}\\\\
            \\hline
            \\endhead
            \\hline
            \\multicolumn{6}{r}{\\textit{continued on next page..}}\\\\
            \\endfoot
            \\hline
            \\endlastfoot
        """
        for weapon in self.character["inventory"]["weapon"]:
            rcolor = ""
            descadd = ""
            if weapon["magic"]:
                rcolor = "\\rowcolor{ProcessBlue!30}"
                descadd += ", magic weapon"
            if weapon["mithril"]:
                rcolor = "\\rowcolor{Yellow!30}"
                descadd += ", mithril weapon"
            if weapon["holy"]:
                rcolor = "\\rowcolor{Green!30}"
                descadd += ", holy weapon"
            if weapon["slaying"] != "":
                rcolor = "\\rowcolor{Red!30}"
                descadd += ", slaying weapon ({})".format(weapon["slaying"])
            worth = ""
            for i in range(0, len(coins["long"])):
                if weapon["worth"][coins["long"][i]] > 0:
                    worth += "{}{} ".format(weapon["worth"][coins["long"][i]], coins["short"][i])
            location = weapon["location"]
            # GET LOCATION ---------
            self.latex += rcolor + " {} & {} & {} &{} &{} &{}\\\\\n".format(weapon["name"],
                                                                          weapon["length"],
                                                                          weapon["weight"],
                                                                          worth,
                                                                          location,
                                                                          weapon["description"] + descadd
                                                                          )

        self.latex += "\\end{longtable}\n"
        self.latex += "}\n"


    def tblTransport(self):
        """
        this creates a table with all transports.
        ----
        @todo has to be fully implemented
        """
        self.latex += "\n\\section{Transports}"
        pass


    def tblGear(self):
        """
        this creates a table with all gear.
        ----
        @todo has to be fully implemented
        """
        self.latex += "\n\\section{Gear}"
        pass


    def tblHerb(self):
        """
        this creates a table with all herbs.
        ----
        @todo has to be fully implemented
        """
        self.latex += "\n\\section{Herbs, Potions \& Poison}"
        pass


    def tblGems(self):
        """
        this creates a table with all gems and jewellery.
        ----
        @todo has to be fully implemented
        """
        self.latex += "\n\\section{Gems \& Jewellery}"
        pass


    def saveLatex(self):
        '''
        This saves the generated LaTeX source code
        '''
        fp = open(self.charpath + self.fn.replace(" ", "_"), "w")
        fp.write(self.latex)
        fp.close()


    def compilePDF(self):
        '''
        This runs the pdflatex compiler to generate the PDF
        '''
        currpath = os.getcwd()
        os.chdir(self.charpath)
        try:
            # to get the right table formating LaTeX has to be run twice
            os.system("pdflatex {}".format(self.fn.replace(" ", "_")))
            os.system("pdflatex {}".format(self.fn.replace(" ", "_")))
            windoman = ["/usr/bin/xdg-open", "/usr/bin/gnome-open", "/usr/bin/kde-open", "/usr/bin/open"]

            for wm in windoman:
                if os.path.isfile(wm):
                    os.system("{} {}.pdf".format(wm, self.fn.replace(" ", "_")[:-4]))

        except Exception as error:
            print("ERROR: Could not execute PDF LaTex! Please try it manually!!\n{}".format(error))
            logger.error("compilePDF: {}".format(error))

        finally:
            os.chdir(currpath)
