#!/usr/bin/env python
'''
\package rpgtoolbox
\file logbox.py

\brief a module with logging tools

This module consists of functions to handle a logging.

\date (C) 2012-2016
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.4
'''

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
"""size of GB"""
GB = MB ** 2

def createLogger(logger = 'rpg-Logger', loglvl = 'debug', logsize = '2 MB',
                 count = 5, logpath = '/var/log/', logfile = 'rpg-tools.log'):
    """
    \brief this function builds a full usable logging object with handler.
    This builds a logging object and a logging handler which will be 
    linked to the object. Further, it sets the logging formatter: 
    \em time: \em level: \em message
    
    @param logger  Name of logger object; default 'ADaManT-Logger'
    @param loglvl  Logging level, may be (debug, info, warning, error, critical);
                   default: debug
    @param logsize default: 2 MB, may be KB, MB or GB. The max. size is 10 GB. If 
                   set on a higher value the log size will be set to 10 GB 
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
    elif 'GB' in logsize[1].upper():
        logsize[0] = int(logsize[0]) * GB
    else:
        logsize[0] = 100 * KB
    
    if logsize[0] > 10 * GB:
        logsize[0] = 10 * GB
    
    handler = logging.handlers.RotatingFileHandler(logfile,
                                                   maxBytes = logsize[0],
                                                   backupCount = count)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

    
