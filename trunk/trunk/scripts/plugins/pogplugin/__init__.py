main = [None]

def initialize(mainwindow):
    main[0] = mainwindow
    
def title():
    return "Pog Manager"
    
def hajimeru():
    from pogPlugin import *
    hajimaru(main[0])
