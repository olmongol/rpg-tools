'''
\package rpgToolDefinitions
\file MERSTables.py
\brief Package for Handling MERS/MERP tables


\date 13.12.2015
\version 1.0
\author Marcus Schwamberger
\email mongol@lederzeug.de
'''

class Magic(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__prep__ = [-30, -15, 0, 10, 20]
        self.magictype = {'Essenz': {'OR':0,
                                     'LE':0,
                                     'VL':0,
                                     'KE':0,
                                     'PL':0
                                     },
                          'Leitmagie':{'OR':0,
                                       'LE':0,
                                       'VL':0,
                                       'KE':-10,
                                       'PL':-10
                                       }
                          }
        self.distmod = [[0, 0, 30],
                        [0.1, 3, 10],
                        [3, 15, 0],
                        [15, 30, -10],
                        [30, 100, -20],
                        [100, 100000, -30]
                        ]
