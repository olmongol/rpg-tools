'''
\file confbox.py

A toolbox of things to handle config files. 


\author Marcus Schwamberger
\date (c) 2012
\version 0.5.2 alpha
\email marcus@lederzeug.de
'''
import os
import toolbox.globaltools as tools
from toolbox.lang import *

## cfgopts
# holds allowed configuration options and their descriptions
cfgopts = {'lang' :'''
#-------------------------------------------------------------------------------
# The parameter lang describes the used language. 
# Supported are: (de, en)
#-------------------------------------------------------------------------------
''',
           'path' : '''
#-------------------------------------------------------------------------------
# path is the default storage path for generated XML files
#-------------------------------------------------------------------------------
''',
            'log' : '''
#-------------------------------------------------------------------------------
# path where the log files shall be stored
#-------------------------------------------------------------------------------
'''            
           }

##defval
# holds default values for a configuration file.
defval = {'lang' : 'en',
          'path' : '~',
          'log'  : '/tmp/'
          }

## home
# holds users home directory
home = os.path.expanduser('~')

class chkCfg(object):
    '''
    These Objects reads out a given config file and store the content of the
    configuration in a dictionary.
    '''


    def __init__(self, path = None, filename = ".axgk",
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

    def __cfg2dic(self, path = None, filename = '.axgk', lang = 'en', \
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
            self.__exists = tools.checkFiles(home, [self.fn])
            
            if self.__exists[self.fn]:
                self._fcon = tools.readFile(home, self.fn, 'r')
            else:
#                raise IOError(errmsg['no_file'][self.lang])
                self.createDefault(path = home, logpath = home)
        else:
            self.__exists = tools.checkFiles(self.path, self.fn)
            
            if self._exists[self.fn]:
                self._fcon = tools.readFile(self.path, self.fn, 'r')
            else:
#                raise IOError(errmsg['no_file'][self.lang])
                self.createDefault(path = home, logpath = home)
                
        self.cnfparam = tools.array2dict(self._fcon, self.exp, self.com)
        
        
    def createDefault(self, path = None, filename = ".axgk",
                      logpath = None, exp = '=', comment = '#'):
        '''
        This method creates a default configuration file for the ADaManT XML
        Generator Kit.
        
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
        
        if self.path == None:
            self.path = home
            
        if self.logpath == None:
            self.logpath = home    
            
        self._content = """
################################################################################
# ADaManT configuration file
################################################################################
\n\n"""
        for key in cfgopts:
            self._content += cfgopts[key]
            self._content += key + " = " + defval[key]
            
        self._fp = open(home + '/' + self.fn, 'w')
        self._fp.write(self._content)
        self._fp.close()
        
    def _coCfg(self, lang):
        """
        This method checks whether all configurational parameter are set.
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
           
    def saveCnf(self, path = None, filename = '.axgk', content = None):
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
                    self.path = home
                
                for param in content:
                    self.fc += param + " = " + content[param] + '\n'
                    
                self.fp = open(home + '/' + self.fn, 'w')
                self.fp.write(self.fc)
                self.fp.close()
                    
