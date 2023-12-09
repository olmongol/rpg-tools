#!/usr/bin/python3
'''!
\brief This is a little tool for finding herbs in different areas of Middle-Earth

This is for foraging checks in Middle-Earth.

\date (C) 2020 - 2022
\author Marcus Schwamberger

\email marcus@lederzeug.de
\copyright GNU V3.0
\version 1.1.1

'''
from pprint import pprint
from tkinter import filedialog
import csv
import json
import os

from gui.window import *
from rpgToolDefinitions import inventory as inv
from rpgToolDefinitions.epcalcdefs import maneuvers as manmod
from rpgToolDefinitions.helptools import RMDice as Dice
from rpgToolDefinitions.middleearth import *
from rpgtoolbox.globaltools import readCSV
from rpgtoolbox.rpgtools import dice
from rpgtoolbox.rpgtools import statManeuver as statMan

__author__ = "Marcus Schwamberger"
__updated__ = "26.11.2022"
__copyright__ = "(C) 2015-{} {}".format(__updated__[-4:], __author__)
__email__ = "marcus@lederzeug.de"
__version__ = "1.1.1"
__license__ = "GNU V3.0"
__me__ = "Herb finding Tool"

logger = log.createLogger('foraging', 'info', '1 MB', 1, './log/', logfile = "findherbs.log")



def string2worth(worth = ""):
    '''!
    This converts a string like "2gp 42cp" into a worth dictionary
    @param worth string that holds the worth like "3gp 65bp". Important: space is
    delimiter and the shorts have to be lower characters.
    '''
    result = inv.money.copy()
    value = worth.split(" ")

    for v in value:
        pos = 0
        pos = inv.coins["short"].index(v[-2:])
        result[inv.coins["long"][pos]] = int(v[:-2])

    return result



def sumDices(sides = 4, number = 1):
    """!
    Rolls number D sides and returns the sum of the results
    @param sides of the dice to roll
    @param number of the dices to roll
    """
    result = 0
    for r in dice(sides, number):
        result += r

    logger.debug(f"{number}D{sides} result: {result}")
    return result



def findHerbs(herbs = [], roll = 0, skill = -15, area = ["---"], climate = [], locale = []):
        """!
        This function searches for herbs by area, climate and locale dependend on difficulty of
        finding and the success of the skill (foraging) roll.
        @param roll result of the dice roll
        @param skill total skill bonus for Foraging
        @param area local area where the herb might grow
        @param climate climate conditions
        @param locale local environment conditions like 'desert'
        @retval result list of dictionaries holding the found herbs
        """
        logger.debug(f"herbs:\n {json.dumps(herbs, indent=4)}")
        logger.info("skill: {} + roll: {} ".format(skill, roll))

        if "everywhere" not in area:
            area.append("everywhere")

        logger.info(f"area: {area}")

        if climate == ["---"]:
            climate = []

        logger.info(f"climate: {climate}")

        if locale == ["---"]:
            locale = []

        logger.info(f"locale: {locale}")
        foundherbs = []
        statman = statMan()

        for plant in herbs:
            logger.debug(f"plant: {plant['area']} - {plant['climate']} - {plant['locale']}. ")

            # print(f"current plant likes: {plant['area']} - {plant['climate']} - {plant['locale']}. ")

            if climate != [] and locale != []:
                #print("climate != [] and locale != []")

                if plant["area"] in area and plant["climate"] in climate and plant["locale"] in locale:
                    #print("1st if")
                    mod = manmod[plant["difficulty"]]["mod"]
                    logger.info(f"difficulty modificator: {mod}")

                    if roll != 100 and roll != 66:
                        check = statman.checkRoll(roll + skill + mod)
                        logger.info(f"checkresult: {check}")

                    else:
                        check = statman.checkRoll(roll)
                        logger.info("check: {}".format(check))

                    if check["success"] == "1.0":
                        no = 1
                        logger.info("success: 100%")

                    elif check["success"] == "1.25":
                        no = sumDices(8, 1)
                        logger.info("success: 125%")

                    elif check["success"] == "1.2":
                        no = sumDices(5, 1)
                        logger.info("success: 120%")

                    else:
                        no = 0
                        logger.info("no success")

                    plant["count"] = no

                    if no > 0:
                        foundherbs.append(plant)
                        logger.info(f"found {plant['count']}x {plant['name']}s")

            elif climate == []:

                if plant["area"] in area and plant["locale"] in locale:
                    mod = manmod[plant["difficulty"]]["mod"]
                    logger.info(f"difficulty modificator: {mod}")

                    if roll != 100 and roll != 66:
                        check = statman.checkRoll(roll + skill + mod)

                    else:
                        check = statman.checkRoll(roll)

                    if check["success"] == "1.0":
                        no = 1
                        logger.info("success: 100%")

                    elif check["success"] == "1.25":
                        no = sumDices(8, 1)
                        logger.info("success: 125%")

                    elif check["success"] == "1.2":
                        no = sumDices(5, 1)
                        logger.info("success: 120%")

                    else:
                        no = 0
                        logger.info("no success")

                    plant["count"] = no

                    if no > 0:
                        foundherbs.append(plant)
                        logger.info(f"found {plant['count']}x {plant['name']}s")

            elif locale == []:

                if plant["area"] in area and plant["climate"] in climate:
                    mod = manmod[plant["difficulty"]]["mod"]
                    logger.info(f"difficulty modificator: {mod}")

                    if roll != 100 and roll != 66:
                        check = statman.checkRoll(roll + skill + mod)

                    else:
                        check = statman.checkRoll(roll)

                    if check["success"] == "1.0":
                        no = 1

                    elif check["success"] == "1.25":
                        no = sumDices(8, 1)

                    elif check["success"] == "1.2":
                        no = sumDices(5, 1)

                    else:
                        no = 0

                    plant["count"] = no

                    if no > 0:
                        foundherbs.append(plant)
                        logger.info(f"found {plant['count']}x {plant['name']}s")

            else:
                if plant["area"] in area:
                    mod = manmod[plant["difficulty"]]["mod"]
                    logger.info(f"difficulty modificator: {mod}")

                    if roll != 100 and roll != 66:
                        check = statman.checkRoll(roll + skill + mod)

                    else:
                        check = statman.checkRoll(roll)

                    if check["success"] == "1.0":
                        no = 1

                    elif check["success"] == "1.25":
                        no = sumDices(5, 1)

                    elif check["success"] == "1.2":
                        no = 2

                    else:
                        no = 0

                    plant["count"] = no

                    if no > 0:
                        foundherbs.append(plant)
                        logger.info(f"found {plant['count']}x {plant['name']}s")

        logger.info(f"finished findHerbs {len(foundherbs)}")
        return foundherbs

def loadHerbs(path = "herbs.csv"):
    herbsCSV = readCSV(path)
    logger.info(f"herb table {path} read successfully")

    for plant in herbsCSV:
        if "item" in plant.keys():
            plant["name"] = plant.pop("item")

        if "comment" in plant.keys():
            plant["description"] = plant.pop("comment")

        if "effect" in plant.keys():
            plant["medical use"] = plant.pop("effect")

        if "cost" in plant.keys():
            plant["worth"] = plant.pop("cost")

        plant["worth"] = string2worth(plant["worth"])
        plant["weight"] = 0.1
        plant["location"] = "equipped"
        logger.debug(json.dumps(plant, indent = 4))

    logger.info(f'Loaded {len(herbsCSV)} herbs from {path}')
    return herbsCSV


class searchHerbsWin(blankWindow):
    """!
    This is the GUI for searching herbs in Middle-Earth.
    A list of characters can be loaded and a single character can be chosen for
    the foraging check.
    Found herbs, drugs and poisons may be added by click to the inventory of the
    selected character.

    ----
    @todo add a OptionMenu for purpose of herb for the search.
    """


    def __init__(self, lang = "en", charlist = [], storepath = "./data", herbsFileName = "herbs.csv"):
        """!
        Constructor searchHerbsWin
        @param lang chosen language for window content.
        @param charlist list of characters
        @param storepath configured storepath
        @param herbsFileName name of the CSV file containing the herbs' data
        """
        self.lang = lang
        self.charlist = charlist
        self.storepath = storepath
        # why does the window have to know the directories
        self.defaultpath = storepath + "/default/inventory/"
        self.herbsfile = herbsFileName
        self.foundherbs = []

        if "//" in self.defaultpath:
            self.defaultpath = self.defaultpath.replace("//", "/")

        self.herbsFilePath = self.defaultpath + self.herbsfile

        self.herbsCSV = loadHerbs(path=self.herbsFilePath)

        self.climate = []
        self.locale = []
        self.regions = []
        self.playerlist = ["dummy"]
        self.charlist = [{"player":"dummy",
                          "prof": "Layman",
                          "name": "Sigurt",
                          "cat": {"Outdoor - Environmental": {"Skill": {"Foraging": {"total bonus":-15}}}}
                          }]

        # get all climate/locale entries
        for h in self.herbsCSV:

            if h["climate"] not in self.climate:
                self.climate.append(h["climate"])

            if h["locale"] not in self.locale:
                self.locale.append(h["locale"])

            if h["area"] not in self.regions:
                self.regions.append(h["area"])

        self.climate.sort()
        self.locale.sort()
        self.regions.sort()
        self.searchclimate = []
        self.searchlocale = []
        #window components
        blankWindow.__init__(self, self.lang)
        self.window.title("Herb Searching window")
        self.__addMenu()
        self.__addHelpMenu()
        self.__buildWin()
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
        #----- row 0
        self.__selecPlayer = StringVar()
        self.__selecPlayer.set(self.playerlist[0])
        self.__playerOpt = OptionMenu(self.window,
                                      self.__selecPlayer,
                                      *self.playerlist,
                                      command = self.__updSelec)
        self.__playerOpt.grid(column = 0, row = 0, sticky = "W")

        self.__charname = StringVar()
        self.__charname.set(self.charlist[0]["name"])
        Label(self.window,
              width = 20,
              textvariable = self.__charname,
              ).grid(row = 0, column = 1, sticky = "W")

        self.__charprof = StringVar()
        self.__charprof.set(self.charlist[0]["prof"])
        Label(self.window,
              width = 15,
              textvariable = self.__charprof,
              ).grid(row = 0, column = 2, sticky = "W")
        Label(self.window,
              text = labels['skill'][self.lang] + ":"
              ).grid(row = 0, column = 3, sticky = "NEWS")

        self.__charskill = IntVar()
        self.__charskill.set(-15)
        Entry(self.window,
              justify = "center",
              textvariable = self.__charskill,
              width = 5
              ).grid(row = 0, column = 4, sticky = "EW")

        Label(self.window,
              text = labels['modifier'][self.lang] + ":"
              ).grid(row = 0, column = 5, sticky = "NEWS")

        self.__mod = IntVar()
        self.__mod.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__mod,
              width = 5
              ).grid(row = 0, column = 6, sticky = "EW")

        Label(self.window,
              text = labels['roll'][self.lang] + ":"
              ).grid(row = 0, column = 7, sticky = "NEWS")

        self.__roll = IntVar()
        self.__roll.set(0)
        Entry(self.window,
              justify = "center",
              textvariable = self.__roll,
              width = 5
              ).grid(row = 0, column = 8, sticky = "EW")

        Button(self.window,
               text = txtbutton["but_roll"][self.lang],
               command = self.__rollDice
               ).grid(row = 0, column = 9, sticky = "EW")

        #----- row 1
        Label(self.window,
              text = labels['region'][self.lang] + ":"
              ).grid(row = 1, column = 0, sticky = "NEWS")

        self.__region = StringVar()
        self.__region.set(self.regions[0])
        #Entry(self.window,
        #      justify = "center",
        #      textvariable = self.__region,
        #      width = 20
        #      ).grid(row = 1, column = 1, sticky = "EW")

        self.__selecRegion = StringVar()
        self.__selecRegion.set(self.regions[0])
        self.__regionOpt = OptionMenu(self.window,
                                      self.__selecRegion,
                                      *self.regions,
                                      command = self.__updRegion
                                      )
        #self.__regionOpt.config(width = 80)
        self.__regionOpt.grid(row = 1,
                              column = 1,
                              columnspan = 3,
                              sticky = "W")

        Label(self.window,
              text = labels['locale'][self.lang] + ":"
              ).grid(row = 1, column = 2, sticky = "NEWS")

        self.__selecLocale = StringVar()
        self.__selecLocale.set(self.locale[0])
        self.__localeOpt = OptionMenu(self.window,
                                      self.__selecLocale,
                                      *self.locale,
                                      command = self.__updLocale)
        self.__localeOpt.grid(row = 1, column = 3, columnspan = 2, sticky = "W")

        Label(self.window,
              text = labels['climate'][self.lang] + ":"
              ).grid(row = 1, column = 5, sticky = "NEWS")

        self.__selecClimate = StringVar()
        self.__selecClimate.set(self.climate[0])
        self.__climateOpt = OptionMenu(self.window,
                                      self.__selecClimate,
                                      *self.climate,
                                      command = self.__updClimate)
        self.__climateOpt.grid(row = 1, column = 6, sticky = "W")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self.__checkResult
               ).grid(row = 1, column = 9, sticky = "EW")

        #----- row 2
        vscroll = Scrollbar(self.window, orient = VERTICAL)
        self.displayTxt = Text(self.window,
                               yscrollcommand = vscroll.set,
                               height = 20
                               )
        vscroll.config(command = self.displayTxt.yview)
#        vscroll.grid(row = 2, colum = 10, sticky = "NSW")
        self.displayTxt.grid(row = 2,
                             column = 0,
                             columnspan = 10,
                             sticky = "NEWS")


    def __rollDice(self):
        result, self.umr = Dice(rules = "RM")
        self.__roll.set(result[0])
        logger.debug("Result roll: {}\nUMR:{}".format(result, self.umr))


    def __updClimate(self, selection):
        """!
        This gets the selected climate
        @param selction holds the selection of climate
        """
        self.searchclimate = [selection]
        logger.debug(f"selected climate. {selection}")


    def __updLocale(self, selection):
        """!
        This gets the selected locale.
        @param selection holds the selection of locale
        """
        self.searchlocale = [selection]
        logger.debug(f"selected locale: {selection}")


    def __updRegion(self, selection):
        """!
        This updates the window by the selected region
        @param selection holds the selection of  search region
        """
        self.__region.set(selection)
        self.searchregion = [selection]
        logger.debug(f"search region: {selection}")


    def __updSelec(self, selection):
        """!
        Updating window by selected Character
        @param selection holds selection o character
        """
        logger.debug(f"selected character: {selection}")
        idx = self.playerlist.index(selection)
        self.__charname.set(self.charlist[idx]["name"])
        self.__charprof.set(self.charlist[idx]["prof"])
        self.__charskill.set(self.charlist[idx]["cat"]["Outdoor - Environmental"]["Skill"]["Foraging"]["total bonus"])


    def __save(self):
        '''
        This opens a file dialog window for saving
        '''
        savedir = filedialog.asksaveasfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])

        with open(savedir, "w") as fp:
            json.dump(self.charlist, fp, indent = 4)
        logger.info(f"{savedir} saved successfully")


    def __open(self):
        '''!
        This opens a file dialog window for opening a group file.
        '''
        opendir = filedialog.askopenfilename(defaultextension = ".json", filetypes = [("Char Group Files", ".json")])

        with open(opendir, "r") as fp:
            self.charlist = json.load(fp)

        logger.info(f"{opendir} read successfully")
        self.playerlist = []

        for c in self.charlist:
            self.playerlist.append(c["player"])

        logger.debug(f"self.playerlist set")
        self.__selecPlayer.set(self.playerlist[0])
        self.__charname.set(self.charlist[0]["name"])
        self.__charprof.set(self.charlist[0]["prof"])
        self.__charskill.set(self.charlist[0]["cat"]["Outdoor - Environmental"]["Skill"]["Foraging"]["total bonus"])

        try:
            del(self.__playerOpt)

        except:
            pass

        finally:
            self.__playerOpt = OptionMenu(self.window,
                                          self.__selecPlayer,
                                          *self.playerlist,
                                          command = self.__updSelec)
            self.__playerOpt.grid(column = 0, row = 0, sticky = "W")


    def __quit(self):
        '''!
        This method closes the window
        '''
        logger.info("quit program")
        self.window.destroy()


    def __checkResult(self):
        """!
        This initiates the search for herbs by the given parameters
        """
        searchskill = self.__charskill.get()
        searchmod = self.__mod.get()
        searchroll = self.__roll.get()
        self.searchregion = [self.__region.get()]
        self.foundherbs = findHerbs(self.herbsCSV, roll = searchroll, skill = searchskill + searchmod, area = self.searchregion, \
                       climate = self.searchclimate, locale = self.searchlocale)
        logger.info(f"found {len(self.foundherbs)} herbs with {searchskill}+{searchmod}+{searchroll} in {self.searchregion}.")
        self.printFindings(self.foundherbs)


    def printFindings(self, herbs):
        """
        This function just displays the found herbs on the screen.
        @param herbs list of dictionary holding the found herbs to display
        """
        self.displayTxt.delete("1.0", "end")
        found = ""
        logger.debug(f"{len(self.foundherbs)} found herbs to display")

        for i in range(0, len(self.foundherbs)):
            found += "\n{}\n{}x {}  - {} (lvl: {}): {} - {}\n\n\t{}\n\t{}\n".format(106 * "=",
                                                                  self.foundherbs[i]["count"],
                                                                  self.foundherbs[i]["name"],
                                                                  self.foundherbs[i]["type"],
                                                                  self.foundherbs[i]["lvl"],
                                                                  self.foundherbs[i]["form"],
                                                                  self.foundherbs[i]["prep"],
                                                                  self.foundherbs[i]["medical use"],
                                                                  self.foundherbs[i]["description"],
                                                                  )

        self.displayTxt.insert(END, found)



if __name__ == '__main__':
    win = searchHerbsWin()
