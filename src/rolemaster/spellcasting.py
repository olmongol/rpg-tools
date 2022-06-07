#!/usr/bin/env python
'''!
\file /home/mongol/git/rpg-tools/src/rolemaster/spellcasting.py
\package rolemaster.spellcasting
\brief This holds definitions and functions to handle spell casting tests and
calculating spell casting modifications

lorem ipsum

\date (c) 2022
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "07.06.2022"
__author__ = "Marcus Schwamberger"
__me__ = "spellcasting.py"

import json
import csv
import sys
from rpgtoolbox.logbox import *

logger = createLogger(logger = "spellcasting logger", logpath = "../log/", logfile = "spellcasting.log")



class castingmod(object):
    """!
    This class calculates the spell casting modification for a single character
    """


    def __init__(self, rpc):
        """!
        Constructor
        @param rpc filename (JSON) or data (dictionary) of role playing character (PC or NPC)

        @var self.chardata: the attribute holding the character data dictionary.
        """

        if type(rpc) == type(""):

            self.readCharacter(rpc)

        else:
            self.chardata = rpc
            logger.debug("character data taken.")

        ##@var self.mod
        #  modification for spell casting roll
        self.mod = 0
        self.readModTables()


    def readModTables(self, datapath = "data/default/tables/"):
        '''!
        This method reads the default spell casting modification tables.
        '''
        ##
        self.rndPrepTable = []

        with open(f"{datapath}spell_casting_mods.csv", "r") as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                self.rndPrepTable.append(row)


    def readCharacter(self, filename):
        """!
        This reads a character file (JSON)
        @param filenam file name of the character file to be read
        """

        if filename and type(filename) == type(""):
            logger.debug(f"open character file: {filename}")

            with open("filename", "r") as fp:
                self.chardata = json.load(fp)

            logger.info(f"file {filename} read.")



def modBySpellLvlAndPrep(casterslvl = 1, spelllvl = 1, preprnds = 0, instspell = False):
    """!
    This function delivers
    @param spelllvl level of the spell
    @param casterslvl level of the spell caster
    @param preprnds number of preparation
    @param instspell boolean which is only true if an instantaneous spell is cast

    @retval instant modification for instantaneous spells (if \e instspell is true)
    @retval noninstant modification for non-instantaneous spells (if \e instspell is false)
    """
    chspdiff = casterslvl - spelllvl
    logger.debug(f"spell diff: {chspdiff} \t prep rnds: {preprnds} \t instantaneous: {instspell}")

    if  8 < chspdiff:
        instant = 15

        if instspell:

            if  preprnds == 0:
                noninstant = 5

            elif preprnds == 1:
                noninstant = 10

            elif preprnds == 2:
                noninstant = 15

            elif 2 < preprnds < 5:
                noninstant = 20

            elif 4 < preprnds < 7:
                noninstant = 25

            elif 6 < preprnds < 9:
                noninstant = 30

            elif 8 < preprnds:
                noninstant = 35

    elif 5 < chspdiff < 9:
        instant = 10

        if instspell:

            if  preprnds == 0:
                noninstant = 0

            elif preprnds == 1:
                noninstant = 5

            elif preprnds == 2:
                noninstant = 10

            elif 2 < preprnds < 5:
                noninstant = 15

            elif 4 < preprnds < 7:
                noninstant = 20

            elif 6 < preprnds < 9:
                noninstant = 25

            elif 8 < preprnds:
                noninstant = 30

    elif chspdiff == 5:
        instant = 5

        if instspell:

            if  preprnds == 0:
                noninstant = -10

            elif preprnds == 1:
                noninstant = 0

            elif preprnds == 2:
                noninstant = 5

            elif 2 < preprnds < 5:
                noninstant = 10

            elif 4 < preprnds < 7:
                noninstant = 15

            elif 6 < preprnds < 9:
                noninstant = 20

            elif 8 < preprnds:
                noninstant = 25

    elif chspdiff == 4:
        instant = 5

        if instspell:

            if  preprnds == 0:
                noninstant = -20

            elif preprnds == 1:
                noninstant = 0

            elif preprnds == 2:
                noninstant = 5

            elif 2 < preprnds < 5:
                noninstant = 10

            elif 4 < preprnds < 7:
                noninstant = 15

            elif 6 < preprnds < 9:
                noninstant = 20

            elif 8 < preprnds:
                noninstant = 25

    elif chspdiff == 3:
        instant = 5

        if instspell:

            if  preprnds == 0:
                noninstant = -30

            elif preprnds == 1:
                noninstant = 0

            elif preprnds == 2:
                noninstant = 5

            elif 2 < preprnds < 5:
                noninstant = 10

            elif 4 < preprnds < 7:
                noninstant = 15

            elif 6 < preprnds < 9:
                noninstant = 20

            elif 8 < preprnds:
                noninstant = 25

    elif chspdiff == 2:
        instant = 0

        if instspell:

            if  preprnds == 0:
                noninstant = -35

            elif preprnds == 1:
                noninstant = -10

            elif preprnds == 2:
                noninstant = 0

            elif 2 < preprnds < 5:
                noninstant = 5

            elif 4 < preprnds < 7:
                noninstant = 10

            elif 6 < preprnds < 9:
                noninstant = 15

            elif 8 < preprnds:
                noninstant = 20

    elif chspdiff == 1:
        instant = 0

        if instspell:

            if  preprnds == 0:
                noninstant = -45

            elif preprnds == 1:
                noninstant = -20

            elif preprnds == 2:
                noninstant = 0

            elif 2 < preprnds < 5:
                noninstant = 5

            elif 4 < preprnds < 7:
                noninstant = 10

            elif 6 < preprnds < 9:
                noninstant = 15

            elif 8 < preprnds:
                noninstant = 20

    elif chspdiff == 0:
        instant = 0

        if instspell:

            if  preprnds == 0:
                noninstant = -55

            elif preprnds == 1:
                noninstant = -30

            elif preprnds == 2:
                noninstant = 0

            elif 2 < preprnds < 5:
                noninstant = 5

            elif 4 < preprnds < 7:
                noninstant = 10

            elif 6 < preprnds < 9:
                noninstant = 15

            elif 8 < preprnds:
                noninstant = 20

    elif chspdiff == -1:
        instant = -30

        if instspell:

            if  preprnds == 0:
                noninstant = -85

            elif preprnds == 1:
                noninstant = -60

            elif preprnds == 2:
                noninstant = -30

            elif 2 < preprnds < 5:
                noninstant = -25

            elif 4 < preprnds < 7:
                noninstant = -20

            elif 6 < preprnds < 9:
                noninstant = -15

            elif 8 < preprnds:
                noninstant = -10

    elif chspdiff == -2:
        instant = -35

        if instspell:

            if  preprnds == 0:
                noninstant = -90

            elif preprnds == 1:
                noninstant = -65

            elif preprnds == 2:
                noninstant = -35

            elif 2 < preprnds < 5:
                noninstant = -30

            elif 4 < preprnds < 7:
                noninstant = -25

            elif 6 < preprnds < 9:
                noninstant = -20

            elif 8 < preprnds:
                noninstant = -15

    elif chspdiff == -3:
        instant = -40

        if instspell:

            if  preprnds == 0:
                noninstant = -95

            elif preprnds == 1:
                noninstant = -70

            elif preprnds == 2:
                noninstant = -40

            elif 2 < preprnds < 5:
                noninstant = -35

            elif 4 < preprnds < 7:
                noninstant = -30

            elif 6 < preprnds < 9:
                noninstant = -25

            elif 8 < preprnds:
                noninstant = -20

    elif chspdiff == -4:
        instant = -45

        if instspell:

            if  preprnds == 0:
                noninstant = -100

            elif preprnds == 1:
                noninstant = -75

            elif preprnds == 2:
                noninstant = -45

            elif 2 < preprnds < 5:
                noninstant = -40

            elif 4 < preprnds < 7:
                noninstant = -35

            elif 6 < preprnds < 9:
                noninstant = -30

            elif 8 < preprnds:
                noninstant = -25

    elif chspdiff == -5:
        instant = -50

        if instspell:

            if  preprnds == 0:
                noninstant = -105

            elif preprnds == 1:
                noninstant = -80

            elif preprnds == 2:
                noninstant = -50

            elif 2 < preprnds < 5:
                noninstant = -45

            elif 4 < preprnds < 7:
                noninstant = -40

            elif 6 < preprnds < 9:
                noninstant = -35

            elif 8 < preprnds:
                noninstant = -30

    elif -8 < chspdiff < -5:
        instant = -70

        if instspell:

            if  preprnds == 0:
                noninstant = -125

            elif preprnds == 1:
                noninstant = -100

            elif preprnds == 2:
                noninstant = -70

            elif 2 < preprnds < 5:
                noninstant = -65

            elif 4 < preprnds < 7:
                noninstant = -60

            elif 6 < preprnds < 9:
                noninstant = -55

            elif 8 < preprnds:
                noninstant = -40

    elif -11 < chspdiff < -7:
        instant = -95

        if instspell:

            if  preprnds == 0:
                noninstant = -150

            elif preprnds == 1:
                noninstant = -125

            elif preprnds == 2:
                noninstant = -95

            elif 2 < preprnds < 5:
                noninstant = -90

            elif 4 < preprnds < 7:
                noninstant = -85

            elif 6 < preprnds < 9:
                noninstant = -80

            elif 8 < preprnds:
                noninstant = -75

    elif -16 < chspdiff < -10:
        instant = -120

        if instspell:

            if  preprnds == 0:
                noninstant = -175

            elif preprnds == 1:
                noninstant = -150

            elif preprnds == 2:
                noninstant = -120

            elif 2 < preprnds < 5:
                noninstant = -115

            elif 4 < preprnds < 7:
                noninstant = -110

            elif 6 < preprnds < 9:
                noninstant = -105

            elif 8 < preprnds:
                noninstant = -100

    elif -21 < chspdiff < -15:
        instant = -170

        if instspell:

            if  preprnds == 0:
                noninstant = -225

            elif preprnds == 1:
                noninstant = -200

            elif preprnds == 2:
                noninstant = -170

            elif 2 < preprnds < 5:
                noninstant = -165

            elif 4 < preprnds < 7:
                noninstant = -160

            elif 6 < preprnds < 9:
                noninstant = -155

            elif 8 < preprnds:
                noninstant = -140

    elif chspdiff < -20:
        instant = -220

        if instspell:

            if  preprnds == 0:
                noninstant = -275

            elif preprnds == 1:
                noninstant = -250

            elif preprnds == 2:
                noninstant = -220

            elif 2 < preprnds < 5:
                noninstant = -215

            elif 4 < preprnds < 7:
                noninstant = -210

            elif 6 < preprnds < 9:
                noninstant = -205

            elif 8 < preprnds:
                noninstant = -200
    if instspell:
        logger.debug(f"instant mod: {instant}")
        return instant

    else:
        logger.debug(f"non-instant mod: {noninstant}")
        return noninstant



def modByOtherCond(**kwargs):
    """!
    This function  delivers spell casting modification by realm, spell type, outer
    conditions like use of voice or equipment
    @param kwargs this dictionary of free key/value pairs  may contain the following
    parameters:
    - \b realm  allowed values: channeling, essence, mentalism
    - snap (boolean) if a non-instantaneous spell is cast in a snap action
    - \b pptotal number of total/max powerpoints (int);  \e optional
    - \b ppremain number of remaining powerpoints (int); \e optional
    - \b sltype  spell list type; allowed values (str):
        - 'own realm own base'
        - 'own realm other base'
        - 'own realm open'
        - 'own realm closed'
        - 'arcane open'
        - 'other realm other base'
        - 'other realm open'
        - 'other realm closed'
    - \b freehands number of free hands while casting: 0,1,2
    - \b voice the use of voice; the allowed values (str) are:
        - 'none'
        - 'whisper'
        - 'normal'
        - 'shout'
    - \b helmet type of worn helmet; allowed values (str):
        - 'none'
        - 'leather'
        - 'leather and metal'
        - 'metal'
    - \b equipment type and mass of worn/carried equipment as a dict:
        - {'organic living': number of lbs, \n 'organic non-living': number of lbs, \n 'inorganic": number of libs}
    - \b at armor type (int); range 1-20

    @retval result spell casting modification (int)

    """
    #----- setting default values
    realm = "channeling"
    snap = False
    pptotal = 1
    ppremain = 1
    sltype = "own realm own base"
    freehands = 1
    voice = "normal"
    helmet = "none"
    equipment = {"organic living":0,
                "organic non-living":0,
                "inorganic":0}
    at = 1
    allowed = {"realm": ["channeling", "essence", "mentalism"],
              "sltype": ['own realm own base', 'own realm other base', 'own realm open',
                          'arcane open', 'other realm other base', 'other realm open', 'other realm closed'],
              "voice": ["none", "whisper", "normal", "shout"],
              "helmet": ["none", "leather", "leather and metal", "metal"],

              }
    result = 0

    if "realm" in kwargs.keys():

        if kwargs["realm"] in  allowed["realm"]:
            realm = kwargs["realm"]
            logger.debug(f"realm set to {realm}")

        else:
            logger.error(f"wrong realm set: {kwargs['realm']}")
            print(f"wrong realm set: {kwargs['realm']}")
            sys.exit(1)

    if "snap" in kwargs.keys():

        if type(kwargs["snap"]) == bool:
            snap = kwargs["snap"]
            logger.debug(f"snap set to {snap}")

        else:
            logger.error(f"wrong type for snap: {type(kwargs['snap'])}")
            print(f"wrong type for snap: {type(kwargs['snap'])}")
            sys.exit(1)

    #----- mod by snap action
    if snap:
        result -= 20

    if "pptotal" in kwargs.keys():

        if type(kwargs["pptotal"]) == int:
            pptotal = kwargs["pptotal"]
            logger.debug(f"pptotal set to {pptotal}")

        else:
            logger.error(f"wrong type for pptotal: {type(kwargs['pptotal'])}")
            print(f"wrong type for pptotal: {type(kwargs['pptotal'])}")
            sys.exit(1)

    if "ppremain" in kwargs.keys():

        if type(kwargs["ppremain"]) == int:
            ppremain = kwargs["ppremain"]
            logger.debug(f"ppremain set to {ppremain}")

        else:
            logger.error(f"wrong type for ppremain: {type(kwargs['ppremain'])}")
            print(f"wrong type for ppremain: {type(kwargs['ppremain'])}")
            sys.exit(1)

    ppercent = round(ppremain / pptotal)

    #----- mod by remaining pp
    if 0.25 < ppercent < 0.51:
        result -= 10

    elif 0.50 < ppercent < 0.76:
        result -= 20

    elif 0.75 < ppercent:
        result -= 30

    if "sltype" in kwargs.keys():

        if kwargs["sltype"] in allowed["sltype"]:
            sltype = kwargs["sltype"]
            logger.debug(f"sltype set to  {sltype}")

        else:
            logger.error(f"wrong sltype set: {sltype}")
            print(f"wrong sltype set: {sltype}")
            sys.exit(1)

    if "freehands" in kwargs.keys():

        if type(kwargs["freehands"]) == int:

            if -1 < kwargs["freehands"] < 3:
                freehands = kwargs["freehands"]
                logger.debug(f"frehands set to {freehands}")

        else:
            logger.error(f"wrong type for freehands: {type(freehands)}")
            print(f"wrong type for freehands: {type(freehands)}")
            sys.exit(1)

    #----- mods by freehand
    if freehands == 0:

        if realm == "channeling":
            result -= 20

        elif realm == "essence":
            result -= 30

    elif freehands == 2:

        if realm == "channeling":
            result += 5

        elif realm == "essence":
            result += 10

    if "voice" in kwargs.keys():

        if kwargs["voice"] in allowed["voice"]:
            voice = kwargs["voice"]
            logger.debug(f"voice set to {voice}")

        else:
            logger.error(f"wrong value set for vorce: {kwargs['voice']}")
            print(f"wrong value set for vorce: {kwargs['voice']}")
            sys.exit(1)

    #----- mod by voice
    if voice == "none":

        if  realm == "channeling":
            result -= 10

        elif realm == "essence":
            result -= 5

    elif voice == "normal":

        if  realm == "channeling":
            result += 5

    elif voice == "shout":

        if  realm == "channeling":
            result += 10

        elif realm == "essence":
            result += 5

    if "helmet" in kwargs.keys():

        if kwargs["helmet"] in allowed["helmet"]:
            helmet = kwargs["helmet"]
            logger.debug(f"helmet set to {helmet}")

        else:
            logger.error(f"wrong value for helmet: {helmet}")
            print(f"wrong value for helmet: {helmet}")
            sys.exit(1)

    #----- mods by helmet
    if helmet == "leather":

        if realm == "essence":
            result -= 20

        elif realm == "mentalism":
            result -= 30

    elif helmet == "leather and metal":

        if realm == "channeling":
            result -= 10

        elif realm == "essence":
            result -= 30

        else:
            result -= 40

    else:

        if realm == "channeling":
            result -= 20

        elif realm == "essence":
            result -= 40

        else:
            result -= 60

    if "equipment" in  kwargs.keys():
        if type(kwargs["equipment"]) == dict:

            for key in kwargs["equipment"].keys():
                if  key in equipment.keys() and type(kwargs["equipment"][key]) == int:
                    equipment[key] = kwargs["equipment"][key]
                    logger.debug(f"equipment[{key}] set to {equipment[key]}")
                else:
                    logger.error(f"equipment[{key}] cannot set to {kwargs['equipment'][key]}")
                    print(f"ERROR: equipment[{key}] cannot set to {kwargs['equipment'][key]}")

    #----- mod by equipment
    if realm == "channeling":

        if equipment["inorganic"] - 10 > 0:
            result -= equipment["inorganic"] - 10

    elif realm == "essence":
        eqmod = 0

        if (equipment["organic living"] - 50) // 5 > eqmod:
            eqmod = (equipment["organic living"] - 50) // 5

        if equipment["organic non-living"] - 10 > eqmod:
            eqmod = equipment["organic non-living"] - 10

        if (equipment["inorganic"] - 5) * 2 > eqmod:
            eqmod = (equipment["inorganic"] - 5) * 2

        result -= eqmod

    if  "at" in kwargs.keys():

        if type(kwargs["at"]) == int:

            if 0 < kwargs["at"] < 21:
                at = kwargs["at"]
                logger.debug(f"AT set to {at}")

        else:
            logger.error(f"wrong type for AT: {type(kwargs['at'])}")
            print(f"wrong type for AT: {type(kwargs['at'])}")
            sys.exit(1)

    #----- mod by AT
    if realm == "channeling":

        if 12 < at < 15:
            result -= 30

        elif 14 < at < 17:
            result -= -60

        elif 16 < at < 19:
            result -= -35

        elif at == 19:
            result -= 60

        elif at == 20:
            result -= 75

    elif realm == "essence":

        if 4 < at < 7:
            result -= 10

        elif 6 < at < 9:
            result -= 20

        elif 8 < at < 11:
            result -= 25

        elif at == 11:
            result -= 40

        elif at == 12:
            result -= 50

        elif at in [13, 14]:
            result -= 40

        elif at in [15, 16]:
            result -= 70

        elif at in [17, 18]:
            result -= 45

        elif at == 19:
            result -= 75

        elif at == 20:
            result -= 90

    return result

