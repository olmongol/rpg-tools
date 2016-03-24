#!/usr/bin/env python
'''
\file logbox.py

\brief a module with logging tools

This module consists of functions to handle a logging.

\date (C) 2012
\author Marcus Schwamberger
\email mongol@nld.ds.mpg.de
\version 0.4.1 alpha
'''

#import logging
import logging.handlers

"""Debugging level"""
LEVEL = {'debug'    : logging.DEBUG,
         'info'     : logging.INFO,
         'warning'  : logging.WARNING,
         'error'    : logging.ERROR,
         'critical' : logging.CRITICAL}

"""size of KB"""
KB = 1024
"""size of MB"""
MB = KB ** 2

def createLogger(logger = 'ADaManT-Logger', loglvl = 'debug', logsize = '2 MB',
                 count = 5, logpath = '/var/log/', logfile = 'adamant-xml.log'):
    """
    \brief this function builds a full usable logging object with handler.
    This builds a logging object and a logging handler which will be 
    linked to the object. Further, it sets the logging formatter: 
    \em time: \em level: \em message
    
    @param logger  Name of logger object; default 'ADaManT-Logger'
    @param loglvl  Logging level, may be (debug, info, warning, error, critical);
                   default: debug
    @param logsize default: 2 MB, may be KB or MB. The max. size is 100 MB. If 
                   set on a higher value the log size will be set to 100 MB 
                   automatically.
    @param count   number of log files to be stored
    @param logpath path to log files; default is  '/var/log/'
    @param logfile name of the log file; default KMT.log

    @retval result complete logger object with handler
    """
 
    logger = logging.getLogger(logger)
    logfile = logpath + logfile
    logger.setLevel(LEVEL[loglvl.lower()])
    
    """defining the logging format"""
    formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
    logsize = logsize.split()
    
    if 'MB' in logsize[1].upper():
        logsize[0] = int(logsize[0]) * MB
    elif 'KB' in logsize[1].upper():
        logsize[0] = int(logsize[0]) * KB
    else:
        logsize[0] = 100 * KB
    
    if logsize[0] > 100 * MB:
        logsize[0] = 100 * MB
    
    handler = logging.handlers.RotatingFileHandler(logfile,
                                                   maxBytes = logsize[0],
                                                   backupCount = count)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

    
