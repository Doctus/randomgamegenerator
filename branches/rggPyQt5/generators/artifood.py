import random
from . import food

def getArtifood():
    adj = ['black', 'white', 'great', 'dread', 'fell', 'dark', 'sacred', 'vorpal',
           'unholy', 'bursting', 'shining', 'vaulting', 'holy', 'dead', 'eternal',
           'red', 'green', 'blue', 'crimson', 'violet', 'iridescent', 'grand',
           'supreme', 'titanic', 'screaming', 'ruby', 'sapphire', 'nightmare',
           "ultimate", "endless", "lost",
                    "forgotten", "ancient", "mystical", "arcane", "divine",
                    "forbidden", "perfect", "brilliant"]
    post = ['blessing', 'mourning', 'winter', 'heaven', 'hell', 'doom', 'destruction',
            'love', 'transcendent skill', 'might', 'cunning', 'sagacity', 'wisdom',
            'sorrow', 'dawn', 'twilight', 'sunset', 'nightmare',
            "power", "wisdom", "undeath", "destruction", "life", "holiness",
               "ice", "flames", "death", "silence", "immortality"]
    numbers = ['four', 'seven', 'nine', 'twelve', 'thirteen', 'hundred', 'thousand']
    numpost = ['blessings', 'gods', 'winters', 'hells', 'heavens', 'sages',
               'savants', 'wizards', 'archmagi', 'warlords', 'sunsets', 'dawns',
               'dreams']
    patterns = ["the $adj $item of $post",
                "the $item of the $numb $numpost",
                "the $item of $post",
                "the $adj $item of the $numb $numpost",
                "the $item of the $numb $adj $numpost",
                "the $item of the $numb $adj $numpost",
                "the $adj $item",
                "the $item of $numpost"]
    pat = random.choice(patterns)
    pat = pat.replace("$adj", random.choice(adj).capitalize())
    pat = pat.replace("$post", random.choice(post).capitalize())
    pat = pat.replace("$numb", random.choice(numbers).capitalize())
    pat = pat.replace("$numpost", random.choice(numpost).capitalize())
    pat = pat.replace("$item", food.getFood().capitalize())
    return pat
    
def getName(args):
    if args == "help": return "Generates an artifact food name. No special arguments."
    return getArtifood()
