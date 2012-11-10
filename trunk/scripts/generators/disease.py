import random

def _getDiseaseName():
    first = "Gut Yellow Red Plague Black White Green Sailor's Bloody".split()
    second = 'Gut Rot Plague Death Fever Flu Flux Boils Warts'.split()
    return " ".join(("The", random.choice(first), random.choice(second)))
    
def getName(args):
    if args == "help": return "Generates a common/folk name for a disease."
    return _getDiseaseName()