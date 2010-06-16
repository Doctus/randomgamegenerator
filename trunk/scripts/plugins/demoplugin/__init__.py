main = [None]

def initialize(mainwindow):
    main[0] = mainwindow
    
def title():
    return "Demo Plugin"
    
def hajimeru():
    from demoplugin import *
    hajimaru(main[0])