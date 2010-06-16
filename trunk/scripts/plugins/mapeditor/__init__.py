main = [None]

def initialize(mainwindow):
    main[0] = mainwindow
    
def title():
    return "Map Editor"
    
def hajimeru():
    from mapEditor import *
    hajimaru(main[0])
