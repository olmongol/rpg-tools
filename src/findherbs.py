#!/usr/bin/python3
'''!
\file find_herbs.py
\package  find_herbs.py
\brief This is a little tool for finding herbs in different areas of Middle-Earth



\date (C) 2020
\author Marcus Schwamberger
\email marcus@lederzeug.de
\license GNU V3.0
\version 1.1.0

'''
import os
import json
import csv
from pprint import pprint
from rpgtoolbox.globaltools import readCSV
from rpgtoolbox.rpgtools import statManeuver as statMan
from rpgtoolbox.rpgtools import dice
from rpgToolDefinitions import inventory as inv
from rpgToolDefinitions.epcalcdefs import maneuvers as manmod
from rpgToolDefinitions.middleearth import *
from gui.window import *
from rpgToolDefinitions.helptools import RMDice as Dice
from tkinter import filedialog
logger = log.createLogger('AT-Window', 'info', '1 MB', 1, './', logfile = "findherbs.log")


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

    return result

def findHerbs(herbs=[], roll = 0, skill = -15, area = ["---"], climate = [], locale = []):
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

        print("findHerbs: skill: {} + roll: {} ".format(skill, roll))
       
        if "everywhere" not in area:
            area.append("everywhere")

        if climate == ["---"]:
            climate = []

        if locale == ["---"]:
            locale = []

        foundherbs = []
        statman = statMan()

        for plant in herbs:

            if climate != [] and locale != []:
                print("climate != [] and locale != []") 

                if plant["area"] in area and plant["climate"] == climate and plant["locale"] == locale:
                    print("1st if") 
                    mod = manmod[plant["difficulty"]]["mod"]

                    if roll != 100 and roll != 66:
                        check = statman.checkRoll(roll + skill + mod)
                    else:
                        check = statman.checkRoll(roll)
                        print("check: {}".format(check))

                    if check["success"] == "1.0":
                        no = 1
                    elif check["success"] == "1.25":
                        no = sumDices(5, 1)
                    elif check["success"] == "1.2":
                        no = 2
                    else:
                        no = 0
                    print("success all")
                    for i in range(0, no):
                        foundherbs.append(plant)

            elif climate == []:
                print("1st elif") 

                if plant["area"] in area and plant["locale"] in locale:
                    mod = manmod[plant["difficulty"]]["mod"]

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

                    for i in range(0, no):
                        foundherbs.append(plant)

            elif locale == []:
                print("2st elif") 

                if plant["area"] in area and plant["climate"] in climate:
                    mod = manmod[plant["difficulty"]]["mod"]

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

                    for i in range(0, no):
                        foundherbs.append(plant)

        print("finished findHerbs ", len(foundherbs))
        print("finished findHerbs ", foundherbs)
        return foundherbs

class searchHerbsWin(blankWindow):
    """!
    This is the GUI for searching herbs in Middle-Earth.
    A list of characters can be loaded and a single character can be chosen for
    the foraging check.
    Found herbs, drugs and poisons may be added by click to the inventory of the
    selected character.
    """


    def __init__(self, lang = "en", charlist = [], storepath = "./data", herbsfile = "herbs.csv"):
        """!
        Constructor searchHerbsWin
        @param lang chosen language for window content.
        @param charlist list of characters
        @param storepath configured storepath
        @param herbsfile name of the CSV file containing the herbs' data
        """
        self.lang = lang
        self.charlist = charlist
        self.storepath = storepath
        self.defaultpath = storepath + "/default/inventory/"
        self.herbsfile = herbsfile

        if "//" in self.defaultpath:
            self.defaultpath = self.defaultpath.replace("//", "/")

        self.herbs = readCSV(self.defaultpath + self.herbsfile)
        for plant in self.herbs:
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

        logger.info(f'Loaded {len(self.herbs)} herbs from {herbsfile}')

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
        for h in self.herbs:

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
        # row 0
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
        # row 1
        Label(self.window,
              text = labels['region'][self.lang] + ":"
              ).grid(row = 1, column = 0, sticky = "NEWS")

        self.__region = StringVar()
        self.__region.set(self.regions[0])
        Entry(self.window,
              justify = "center",
              textvariable = self.__region,
              width = 20
              ).grid(row = 1, column = 1, sticky = "EW")

        self.__selecRegion = StringVar()
        self.__selecRegion.set(self.regions[0])
        self.__regionOpt = OptionMenu(self.window,
                                      self.__selecRegion,
                                      *self.regions,
                                      command = self.__updRegion)
        self.__regionOpt.grid(row = 1,
                              column = 2,
                              columnspan = 3,
                              sticky = "W")

        Label(self.window,
              text = labels['locale'][self.lang] + ":"
              ).grid(row = 1, column = 4, sticky = "NEWS")

        self.__selecLocale = StringVar()
        self.__selecLocale.set(self.locale[0])
        self.__localeOpt = OptionMenu(self.window,
                                      self.__selecLocale,
                                      *self.locale,
                                      command = self.__updLocale)
        self.__localeOpt.grid(row = 1, column = 5, sticky = "W")

        Label(self.window,
              text = labels['climate'][self.lang] + ":"
              ).grid(row = 1, column = 6, sticky = "NEWS")

        self.__selecClimate = StringVar()
        self.__selecClimate.set(self.climate[0])
        self.__climateOpt = OptionMenu(self.window,
                                      self.__selecClimate,
                                      *self.climate,
                                      command = self.__updClimate)
        self.__climateOpt.grid(row = 1, column = 7, sticky = "W")

        Button(self.window,
               text = txtbutton["but_result"][self.lang],
               command = self.__checkResult
               ).grid(row = 1, column = 9, sticky = "EW")

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
        print("Result: {}\nUMR:{}".format(result, self.umr))


    def __updClimate(self, selection):
        """!
        This gets the selected climate
        """
        self.searchclimate = [selection]
        print(selection)


    def __updLocale(self, selection):
        """!
        This gets the selected locale
        """
        self.searchlocale = [selection]
        print(selection)


    def __updRegion(self, selection):
        """!
        This updates the window by the selected region
        """
        self.__region.set(selection)
        self.searchregion = [selection]
        print(selection)


    def __updSelec(self, selection):
        """!
        Updating window by selected Character
        """
        print(selection)
        idx = self.playerlist.index(selection)
        self.__charname.set(self.charlist[idx]["name"])
        self.__charprof.set(self.charlist[idx]["prof"])
        self.__charskill.set(self.charlist[idx]["cat"]["Outdoor - Environmental"]["Skill"]["Foraging"]["total bonus"])
        pass


    def __save(self):
        '''
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

        self.playerlist = []

        for c in self.charlist:
            self.playerlist.append(c["player"])

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
        self.window.destroy()


    def __checkResult(self):
        """!
        This initiates the search for herbs by the given parameters
        """
        searchskill = self.__charskill.get()
        searchmod = self.__mod.get()
        searchroll = self.__roll.get()
        self.searchregion = [self.__region.get()]
        self.foundherbs = findHerbs(self.herbs, roll = searchroll, skill = searchskill + searchmod, area = self.searchregion, \
                       climate = self.searchclimate, locale = self.searchlocale)
        self.printFindings(self.foundherbs)


    def printFindings(self, herbs):
        print(herbs)
        print(self.foundherbs)
        """
        This function just displays the found herbs on the screen.
        """
        count = 1
        self.displayTxt.delete("1.0", "end")
        found = ""
        for i in range(0, len(self.foundHerbs)):

            if i < len(self.foundHerbs) - 1:

                if self.foundHerbs[i] == self.foundHerbs[i + 1]:
                    count += 1

                else:
                    found += "\n{}\n{}x {}  - {}: {} - {}\n\t{}\n".format(80 * "=",
                                                                          count,
                                                                          self.foundHerbs[i]["name"],
                                                                          self.foundHerbs[i]["type"],
                                                                          self.foundHerbs[i]["form"],
                                                                          self.foundHerbs[i]["prep"],
                                                                          self.foundHerbs[i]["medical use"] + " " + self.foundHerbs[i]["description"]
                                                                          )
                    count = 1

        self.displayTxt.insert(END, found)



if __name__ == '__main__':
    win = searchHerbsWin()
