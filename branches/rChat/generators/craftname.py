import random

def _getCraftName():
    parts = 'Wolf Raven Silver Moon Star Water Snow Sea Tree Wind Cloud Witch Thorn Leaf White Black Green Fire Rowan Swan Night Red Mist Hawk Feather Eagle Song Sky Storm Sun Wood'.split()
    return random.choice((" ".join(random.sample(parts, 2)), " ".join(random.sample(parts, 2))+random.choice(parts).lower()))
    
def getName(args):
    if args == "help": return "Generates a craft name in the style of Lady Pixie Moondrip."
    return _getCraftName()