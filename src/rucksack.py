#import src.gui.window
import gui.window
import Tkinter

__author__ = 'Chris'
__email__ = 'cw@almandor.de'

'''
Erst mal zum rumspielen
'''

class mywindow(gui.window.blankWindow):
    def __init__(self):
        gui.window.blankWindow.__init__(self, "de")
        self.window.mainloop()
     
#fenster = window.blankWindow()
fenster = mywindow();