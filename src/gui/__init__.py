##\package gui
#
# \brief Classes and stuff for the GUI
#
# this toolbox consist of functions and classes for creating a GUI. They are 
# used by the main module.
#
# \author  Marcus Schwamberger
# \email   mongol@nld.ds mpg.de
# \date    (c) 2012
# \version 0.1 alpha

import sys
import winhelper

def checkVersion():
    """
    This function checks out the installed (and used) Python version. The AXG is
    compatible to version 2.6+ or 3.2+
    \return main version number (2/3) or error (1)
    """
    if sys.version_info >= (2, 6) and sys.version_info < (3, 0):
        result = 2        
    elif sys.version_info >= (3, 2):
        result = 3
    else:
        result = 1
        
    return result

version = checkVersion()

if version == 2:
#    import window2 as window
    import window as window
#elif version == 3:
#    from . import window3 as window
else:
    print('Version of Python interpreter not supported yet!')
    exit(1)
