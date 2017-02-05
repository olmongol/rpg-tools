'''
\package rpgtoolbox
\file confbox.py

A toolbox of things to handle config files.


\author Marcus Schwamberger
\date (c) 2012-2016
\version 0.5.2 alpha
\email marcus@lederzeug.de
\license GNU V3.0
'''
import os, locale
import rpgtoolbox.globaltools as rpgtools
from rpgtoolbox.lang import *
from cairosvg.surface.path import path

defaultconfigpath = "conf/"
defaultconfigfile = "rpg-tools.cfg"
defaultlang = locale.getdefaultlocale()[0][:2]
## cfgopts
# holds allowed configuration options and their descriptions
cfgopts = {'lang' :'''
#-------------------------------------------------------------------------------
# The parameter lang describes the used language.
# Supported are: (de, en)
#-------------------------------------------------------------------------------
''',
           'datapath' : '''
#-------------------------------------------------------------------------------
# path is the default storage path for generated CSV files
#-------------------------------------------------------------------------------
''',
            'logpath' : '''
#-------------------------------------------------------------------------------
# path where the log files shall be stored
#-------------------------------------------------------------------------------
''',
            'logcount' : '''
#-------------------------------------------------------------------------------
# Number of maximum log files stored. Default: 3
#-------------------------------------------------------------------------------
''',
            'logfile' : '''
#-------------------------------------------------------------------------------
# Name of the log file. Default: rpgtools.log
#-------------------------------------------------------------------------------
''',
            'logsize' : '''
#-------------------------------------------------------------------------------
# Maximum size of a log file. Default: 1 M
#-------------------------------------------------------------------------------
''',
            'loglevel' : '''
#-------------------------------------------------------------------------------
# Loglevel. Default: error
# Available: debug, info, warning, error, critical
#-------------------------------------------------------------------------------
''',
            'db_type' : '''
#-------------------------------------------------------------------------------
# Database type: CSV, MySQL, SQLLite
# Actually only CSV is supported
#-------------------------------------------------------------------------------
''',
            'db_host' : '''
#-------------------------------------------------------------------------------
# Address of database host. Default: localhost
# The use of databases is actually not supported
#-------------------------------------------------------------------------------
''',
            'db_name' : '''
#-------------------------------------------------------------------------------
# Name of the used database. Default: rpgtools
# The use of databases is actually not supported
#-------------------------------------------------------------------------------
''',
            'db_port' : '''
#-------------------------------------------------------------------------------
# Database port. Default: 3306 (MySQL
# The use of databases is actually not supported
#-------------------------------------------------------------------------------
''',
            'db_user' : '''
#-------------------------------------------------------------------------------
# Database user. Default rpgtools
# The use of databases is actually not supported
#-------------------------------------------------------------------------------
''',
            'db_passwd' : '''
#-------------------------------------------------------------------------------
# Password of database user. Default: secred
# The use of databases is actually not supported
#-------------------------------------------------------------------------------
''',

           }

##defval
# holds default values for a configuration file.
defval = {'lang' : 'en',
          'datapath' : './data',
          'logpath'  : '/tmp/',
          'logcount' : 5,
          'logsize'  : '1M',
          'logfile'  : 'rpgtools.log',
          'loglevel' : 'error',
          'db_type'  : 'csv',
          'db_host'  : 'localhost',
          'db_port'  : 3306,
          'db_user'  : 'rpgtools',
          'db_passwd': 'secred',
          'db_name'  : 'rpgtools',
          'calc_type': 'simple',
          }

## home
# holds users home directory
home = os.path.expanduser('~')

class chkCfg(object):
    '''
    These Objects reads out a given config file and store the content of the
    configuration in a dictionary.
    \todo read default config file if it exists in the same directory
    '''


    def __init__(self, path = defaultconfigpath, filename = defaultconfigfile,
                 lang = 'en', exp = '=', comment = '#'):
        '''
        Constructor
        \param path Path to the config file
        \param filename Name of the config file
        \param lang used language for messages
        \param exp Expression used in the config file. Default is '=' for
                   expressions like \e('<cnfparam> = <value>')
        \param comment The used comment character; default is '#' for a comment
                       structure like '# this is a comment!'
        '''
        self.__cfg2dic(path, filename, lang, exp, comment)

    def __cfg2dic(self, path = defaultconfigpath, filename = defaultconfigfile, lang = 'en', \
                  exp = '=', comment = '#', logpath = None):
        '''
        This method reads out a config file and stores the data into a
        dictionary named \e cnfparam.
        \param path Path to the config file
        \param logpath path for the log files
        \param filename Name of the config file
        \param lang used language for messages
        \param exp Expression used in the config file. Default is '=' for
                   expressions like <cnfparam> = <value>
        \param comment The used comment character; default is '#' for a comment
                       structure like '# this is a comment!'

        '''
        self.lang = lang
        self.logpath = logpath
        self.path = path
        self.fn = filename
        self.exp = exp
        self.com = comment
        self._fcon = []

        if path == None:
            self.__exists = rpgtools.checkFiles('./', [self.fn])

            if self.__exists[self.fn]:
                self._fcon = rpgtools.readFile('./', self.fn, 'r')
                self.cnfparam = rpgtools.array2dict(self._fcon, self.exp, self.com)
#                logger.debug('confbox: read config file')
            else:
#                raise IOError(errmsg['no_file'][self.lang])
                self.createDefault()
                self.cnfparam = defval
        else:
            self.__exists = rpgtools.checkFiles(self.path, [self.fn])

            if self.__exists[self.fn]:

                self._fcon = rpgtools.readFile(self.path, self.fn, 'r')
                self.cnfparam = rpgtools.array2dict(self._fcon, self.exp, self.com)
            else:
#                raise IOError(errmsg['no_file'][self.lang])
                self.createDefault()
                self.cnfparam = defval


    def createDefault(self, path = defaultconfigpath, filename = defaultconfigfile,
                      logpath = "/tmp", exp = '=', comment = '#'):
        '''
        This method creates a default configuration file for the rpg-tools.

        \param path Path to the config file
        \param filname name of the config file
        \param exp expression for evaluate parameters
        \param comment comment character.
        '''
        self.path = path
        self.logpath = logpath
        self.fn = filename
        self.exp = exp
        self.com = comment
        self._content = """
################################################################################
# rpg-tools configuration file
################################################################################
\n\n"""
        for key in cfgopts:
            self._content += cfgopts[key]
            self._content += key + " = " + str(defval[key])

        self._fp = open(self.path + '/' + self.fn, 'w')
        self._fp.write(self._content)
        self._fp.close()


    def _coCfg(self, lang = 'en'):
        """
        This method checks whether all configurational parameter are set.
        \param lang contains the language that is chosen.
        """
        self.lang = lang
        self._keys_cf = self.cnfparam.keys()
        self._keys_op = cfgopts.keys()

        self._allowed = []
        self._not_allowed = []
        self._not_set = []
        self.result = ''

        if self._keys_cf != self._keys_op:

            for key in self._keys_op:

                if key in self._keys_cf:
                    self._allowed.append(key)
                else:
                    self._not_set.append(key)

            for key in self._keys_cf:

                if key not in self._keys_op:
                    self._not_allowed.append(key)

            if self._not_allowed != []:
                self.result += errmsg['wr_cfg'][self.lang] + '\n+\n'
                i = 1

                for key in self._not_allowed:
                    self.result += "%3d. %s" % (i, key) + '\n'
                    i += 1

                self.result += '\n\n'

            if self._not_set != []:
                self.result += errmsg['mis_cfg'][self.lang] + '\n\n'
                i = 1

                for key in self._not_set:
                    self.result += "%3d. %s" % (i, key) + '\n'
                    i += 1

                self.result += '\n\n'

        else:
            self.result += errmsg['fine_cfg'][self.lang]
            
    def loadCnf(self, path = defaultconfigpath, filename = defaultconfigfile):
        """
        This method loads the config data from default config file.
        \param path path of the config file
        \param filename name of config file
        \return content of the given config file
        """
        
        
        self.fp = open(path + filename, 'r')
        self.cont = self.fp.readlines()
        self.fp.close()
        
        self.content = {}
        for i in range(0, len(self.cont)):
            dummy = self.cont[i].split("=")
            dummy[0] = dummy[0].strip(' ')
            dummy[1] = dummy[1].strip(' \n')
            
            if dummy[0] != "":
                self.content[dummy[0]] = dummy[1]
                
        return self.content
        
    def saveCnf(self, path = defaultconfigpath, filename = defaultconfigfile, content = "Error 40"):
        """
        This method writes config data into a file
        \param path path to the config file
        \param filename name of the config file
        \param content holds the content which shall be written to the config
                       file. The used type for this should be a dictionary of
                       the following structure: {'config_param' : value}
        """
        self.path = path
        self.fn = filename
        self.cont = content
        self.fc = ''

        if type(content) == type({}):

            if content != {}:

                if self.path == None:
                    self.path = "."

                for param in content:
                    self.fc += param + " = " + content[param] + '\n'

                self.fp = open(self.path + '/' + self.fn, 'w')
                self.fp.write(self.fc)
                self.fp.close()

