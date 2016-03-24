#!/usr/bin/env python
'''
\file logtools.py
\package ostools.logtools
\brief This module contains all tools needed for logging purposes. 


\date (C) 2012
\author Marcus Schwamberger
\email marcus@lederzeug.de

'''
import logging
import logging.handlers

##
# possible log levels

LEVEL = {'debug'    : logging.DEBUG,
         'info'     : logging.INFO,
         'warning'  : logging.WARNING,
         'error'    : logging.ERROR,
         'critical' : logging.CRITICAL
         }

def mkLogger(logger = 'adlogger',
              loglvl = 'debug',
              logsize = '1 MB',
              count = 5,
              logpath = './',
              logfile = 'ad-threaded.log'):
    """
    \brief This function builds a full usable logging object with handler.
    mkLogger builds a logging object and a logging handler which will be linked
    to the object. Futher, it sets the logging formatter: \em time: \em level:
    \em message
    @param logger  Name of logger object; default 'GSMlogger'
    @param loglvl  Logging level, may be (debug, info, warning, error, critical);
                   default: debug
    @param logsize default: 1 MB, may be KB or MB (max 100 MB)
    @param count   number of logfiles to be stored
    @param logpath path to logfiles; default /var/log/
    @param logfile name of the logfile

    @retval result complete logger object with handler
    """

    logger = logging.getLogger(logger)
    logfile = logpath + logfile
    logger.setLevel(LEVEL[loglvl.lower()])
    formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
    logsize = logsize.split()

    if 'GB' in logsize[1].upper():
        logsize[0] = int(logsize[0]) * 1024 * 1024 * 1024
    elif 'MB' in logsize[1].upper():
        logsize[0] = int(logsize[0]) * 1024 * 1024
    elif 'KB' in logsize[1].upper():
        logsize[0] = int(logsize[0]) * 1024
    else:
        logsize[0] = 102400
        
    if logsize[0] < 1024 * 1024:
        count = 10
    elif (1024 * 1024) <= logsize[0] < (1024 * 1024 * 100):
        count = 3
    else:
        count = 10
        logsize[0] = 204800

    handler = logging.handlers.RotatingFileHandler(logfile, maxBytes = logsize[0],
                                                   backupCount = count)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
    
    
def createLogger(**args):
    '''
    This function gets the external information of the configuration
    file to create the logger of it.
    The created logger object is global not local!
    \param args the allowed entries here are:  
                \arg \b logger - logger name
                \arg \b loglvl - debug, info, warning, error, critial
                \arg \b logsize - number and unit (GB, MB, KB)
                \arg \b logpath - path where the logfile shall be written to
                \arg \b logfile - name of the logfile
                \arg \b count - number of logfiles to be stored 
    '''
    global logger
    
    default = {'logger' : 'adlogger',
               'loglvl' : 'warning',
               'logsize' : '1 MB',
               'count' : 5,
               'logpath' : './',
               'logfile' : 'ad-tread.log'
              }
    kl = default.keys()
    ak = args.keys()

    for key in kl:
        if key not in ak:
            args[key] = default[key]  
    
    logger = mkLogger(logger = args['logger'],
                      loglvl = args['loglvl'],
                      logsize = args['logsize'],
                      count = int(args['count']),
                      logpath = args['logpath'],
                      logfile = args['logfile']
                      )
    
