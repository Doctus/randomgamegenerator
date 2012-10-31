import random

def _assembleName(ph, pa):
    name = []
    for r in pa:
        name.append(random.choice(ph[r]))
    return (''.join(name)).capitalize()

def _getDwarvenMaleName():
    phonemes = [['d', 'n', 'b', 'v', 'th', 'dv', 'l'], #Beginblends
              ['th', 'p', 'mb', 'l', 'f'], #Midblends
              ['u', 'i', 'a'], #Vowels
              ['r'], #Oddly 'r' appears where nothing else can
              ['n', 'r', 'ng', 'l'], #Endconsonants
              ['i']] #Endvowel. Again, odd.
    patterns = [[0, 2, 3, 2, 4], #Durin
                   [0, 2, 1, 5], #Nithi
                   [0, 2, 3, 1, 3, 5], #Northri
                   [0, 2, 1, 3, 5], #Suthri
                   [0, 2, 1, 2, 4], #Dvalin
                   [0, 2, 2, 4], #Dain
                   [0, 3, 2, 4], #Thror
                   [0, 2, 3, 1, 2, 4]] #Dvarfil
    return _assembleName(phonemes, random.choice(patterns))

def _getDwarvenFemaleName():
    return _getDwarvenMaleName()
  
def _getRandomDwarvenName():
    if random.choice((True, False)):
        return _getDwarvenFemaleName()
    return _getDwarvenMaleName()
  
def getName(args):
    if args == "help": return "Generates a dwarven name. Valid arguments are 'female' or 'male'."
    if "female" in args:
        return _getDwarvenFemaleName()
    elif "male" in args:
        return _getDwarvenMaleName()
    return _getRandomDwarvenName()
