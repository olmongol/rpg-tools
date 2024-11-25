#!/usr/bin/env python
'''!
\file /home/mongol/git/rpg-tools/src/rpgtoolbox/charactertools.py
\package rpgtoolbox.charactertools
\brief Toolbox for handing data of (non-)player characters

lorem ipsum

\date (c) 2023
\copyright GNU V3.0
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1
'''
__version__ = "0.1"
__updated__ = "18.08.2023"
__author__ = "Marcus Schwamberger"
__email__ = "marcus@lederzeug.de"
__license__ = "GNU V3"
__copyright__ = "2022 - 2023"

import json
from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import *

mycnf = chkCfg()
logger = log.createLogger('chartools', 'debug', '1 MB', 1, logpath = mycnf.cnfparam["logpath"], logfile = "chartools.log")



class playerCharacter(object):
    '''!This class handles the JSON data of a player character'''


    def __init__(self, **kwargs):
        '''! Class constructor
        The constructor may be executed with some parameters.
        @param kwargs The following parameter may be given:
               - filename: name (and path) of the JSON file containing the character data
               - chardata: a dictionary holding the character data
        '''
        self.filename = ""
        self.chardata = {}

        try:
            for elem in kwargs.keys():

                if elem in self.__dict__.keys():
                    self.__dict__[elem] = kwargs[elem]
                    logger.debug(f"setting {elem} to {kwargs[elem]}")

        except Exception as error:
            logger.error(f"Could not set up Character obj because of:\n\n{error}")
            exit()

        if self.filename:

            with open(self.filename, "r", encode = "utf-8") as fp:
                self.chardata = json.load(fp)

            logger.info(f"{self.filename} successfully read.")


    def checkStructure(self):
        '''!
        This method checks whether the datastructure of a character's dictionary is correct.
        '''
        lv1 = [['AT', 'Ag', 'BGO', 'Co', 'DP', 'Em', 'Hobby Ranks', 'In', 'MMP', 'Me', 'Pr', 'Qu',
              'RRArc', 'RRC/E', 'RRC/M', 'RRChan', 'RRDisease', 'RRE/M', 'RREss', 'RRFear', 'RRMent',
              'RRPoison', 'Re', 'Recovery', 'SD', 'St', 'Stat Loss', 'armmanmod', 'armquickpen',
              'background', 'carried', 'cat', 'culture', 'exp', 'history', 'idxcontainer',
              'idxtransport', 'inventory', 'lvl', 'lvlup', 'misslepen', 'motivation', 'name',
              'old_exp', 'piclink', 'player', 'prof', 'purse', 'race', 'realm', 'soul dep', 'statgain'],

            ]
