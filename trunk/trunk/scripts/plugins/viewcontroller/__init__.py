main = [None]

def initialize(mainwindow):
    main[0] = mainwindow
    
def title():
    return "View Controller"
    
def hajimeru():
    from viewController import *
    hajimaru(main[0])
