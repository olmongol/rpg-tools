#!/usr/bin/env python
'''
\file errbox.py

\brief A box full of error classes


\date (C) 2012
\author Marcus Schwamberger
\email mongol@nld.ds.mpg.de
\version 0.1 alpha
'''
class adamantXML(Exception):
    """
    \class adamantXML
    Objects of this class will be raised in case of errors with XML files used 
    for ADaMant.
    \param value the value to be given to the error handler (e.g., message)
    """
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    

    
