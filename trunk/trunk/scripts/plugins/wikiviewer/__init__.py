main = [None]

def initialize(mainwindow):
    main[0] = mainwindow
    
def title():
    return "MoMMWiki Viewer"
    
def hajimeru():
    from wikiViewer import *
    hajimaru(main[0])
