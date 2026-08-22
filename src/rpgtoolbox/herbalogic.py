#!/usr/bin/env python3
r'''!
\package herbalogic
\brief Herbalogik: findHerbs(), string2worth(), sumDices()

Extrahiert aus findherbs.py als Teil der Modularisierung.
Alle Kräuter-Such-Funktionen hier zentralisiert.
'''
__version__ = "0.1"
__updated__ = "Marcus Schwamberger"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__license__ = "GNU V3.0"

from rpgtoolbox import logbox as log

logger = log.createLogger('foraging', 'info', '1 MB', 1, './log/', logfile="findherbs.log")

import csv
import json
from rpgToolDefinitions import inventory as inv
from rpgToolDefinitions.epcalcdefs import maneuvers as manmod
from rpgtoolbox.rpgtools import dice, statManeuver as statMan

def string2worth(worth = ""):
    r'''!
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
    r'''!
    Rolls number D sides and returns the sum of the results
    @param sides of the dice to roll
    @param number of the dces to roll
    r'''
    result = 0
    for r in dice(sides, number):
        result += r

    logger.debug(f"{number}D{sides} result: {result}")
    return result


def findHerbs(herbs=None, roll=0, skill=-15, area=None, climate=None, locale=None):
    r'''!
    This function searches for herbs by area, climate and locale dependend on difficulty of
    finding and the success of the skill (foraging) roll.
    @param herbs list of available herbs (optional)
    @param roll result of the dice roll
    @param skill total skill bonus for Foraging
    @param area local area where the herb might grow (optional)
    @param climate climate conditions (optional)
    @param locale local environment conditions like 'desert' (optional)
    @retval result list of dictionaries holding the found herbs
    r'''
    if herbs is None:
        herbs = []
    if area is None:
        area = ["---"]
    if climate is None:
        climate = []
    if locale is None:
        locale = []

    logger.debug(f"herbs:\n {json.dumps(herbs, indent=4)}")
    logger.info("skill: {} + roll: {}".format(skill, roll))

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

        if climate != [] and locale != []:

            if plant["area"] in area and plant["climate"] in climate and plant["locale"] in locale:
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
