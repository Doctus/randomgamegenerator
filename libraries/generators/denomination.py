from random import choice

def first():
	return choice(["New", "Life", "Christ", "Renewed", "First", "Holy"])

def second():
	return choice(["Life", "Faith", "Grace", "Gospel"])

def third():
	return choice(["Community", "Baptist", "Bible", "Reformed"])

def final():
	return choice(["Assembly", "Church", "Assembly of God", "Church of God", "Center", "Chapel", "Pentecostal"])
	
def pattern():
	return choice(([first, final], [first, second, final], [first, second, third, final], [first, third, final], [second, third, final]))
	
def getName(args):
    if args == "help": return "Generates a name in the style of typical American Protestant church names. No special arguments."
    return " ".join([func() for func in pattern()])