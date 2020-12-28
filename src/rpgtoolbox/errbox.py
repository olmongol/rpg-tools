#!/usr/bin/env python
'''!
\package rpgtoolbox.errbox
\file errbox.py

\brief A box full of error classes


\date (C) 2012-2021
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 0.1 alpha
'''



class raisedError(Exception):
    """!
    \class raisedError
    Objects of this class will be raised in case of errors with files used
    for rpg-tools.
    \param value the value to be given to the error handler (e.g., message)
    """


    def __init__(self, value):
        self.value = value


    def __str__(self):
        return repr(self.value)

