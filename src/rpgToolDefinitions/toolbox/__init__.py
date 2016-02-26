'''
\package toolbox

\brief A toolbox for the adamant xml profile generator

This toolbox consist of functions and classes which are used by the 
main module and keep the code clean and readable. All this functions
and classes are meant as 'helper tools'.

\author  Marcus Schwamberger
\email   marcus@lederzeug.de
\date    (c) 2012
\version 0.3 alpha

\todo Create the modules for Python 3.x
'''

__author__ = "Marcus Schwamberger"
__email__ = "mongol@nld.ds.mpg.de"
__copyright__ = "(c) 2012 Marcus Schwamberger"
__date__ = "2012$"
__version__ = "0.3 alpha"


import sys

import lang
import globaltools
import xmltools
import xmlbox
import errbox
import confbox



#def checkVersion():
#    """
#    This function checks out the installed (and used) Python version. The AXG is
#    compatible to version 2.6+ or 3.2+
#    \return main version number (2/3) or error (1)
#    """
#    if sys.version_info >= (2, 6) and sys.version_info < (3, 0):
#        result = 2
#    elif sys.version_info >= (3, 2):
#        result = 3
#    else:
#        print(lang.screenmesg['wrongver'][config.lang])
#        result = 1
#    return result
#
#version = checkVersion()
#
#if version == 3:
#    from . import lang
#    from . import globaltools
#    from . import xmltools
#    from . import xmlbox
#    from . import errbox
#elif version == 2:
#    import lang
#    import globaltools
#    import xmltools
#    import xmlbox
#    import errbox
