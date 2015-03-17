import random

def _getArtifactWeaponName():
    adj = ['black', 'white', 'great', 'dread', 'fell', 'dark', 'sacred', 'vorpal',
         'unholy', 'bursting', 'shining', 'vaulting', 'holy', 'dead', 'eternal',
         'red', 'green', 'blue', 'crimson', 'violet', 'iridescent', 'grand',
         'supreme', 'titanic', 'screaming', 'ruby', 'sapphire', 'nightmare']
    combine = ['bless', 'mourn', 'flare', 'death', 'god', 'doom', 'thorn', 'vine',
             'ice', 'flame', 'hate', 'star', 'sun', 'moon', 'stone', 'earth',
             'spark', 'poison', 'soul', 'mist']
    post = ['blessing', 'mourning', 'winter', 'heaven', 'hell', 'doom', 'destruction',
          'love', 'transcendent skill', 'might', 'cunning', 'sagacity', 'wisdom',
          'sorrow', 'dawn', 'twilight', 'sunset', 'nightmare']
    numbers = ['four', 'seven', 'nine', 'twelve', 'thirteen', 'hundred', 'thousand']
    numpost = ['blessings', 'gods', 'winters', 'hells', 'heavens', 'sages',
             'savants', 'wizards', 'archmagi', 'warlords', 'sunsets', 'dawns',
             'dreams']
    weaps = ['blade', 'cleaver', 'dagger', 'hammer', 'mace',
           'sword', 'spear', 'lance', 'dirk', 'flail',
           'axe', 'bow']
    patterns = ["the $adj $comb$weap of $post",
              "the $comb$weap",
              "the $Weap of the $numb $numpost",
              "the $adj $Weap of $post",
              "the $adj $Weap of the $numb $numpost",
              "the $comb$weap of the $numb $adj $numpost",
              "the $Weap of the $numb $adj $numpost",
              "the $adj $comb$weap",
              "the $Weap of $numpost"]
    pat = random.choice(patterns)
    pat = pat.replace("$adj", random.choice(adj).capitalize())
    pat = pat.replace("$comb", random.choice(combine).capitalize())
    pat = pat.replace("$post", random.choice(post).capitalize())
    pat = pat.replace("$numb", random.choice(numbers).capitalize())
    pat = pat.replace("$numpost", random.choice(numpost).capitalize())
    pat = pat.replace("$weap", random.choice(weaps))
    pat = pat.replace("$Weap", random.choice(weaps).capitalize())
    return pat
    
def getName(args):
    if args == "help": return "Generates the name of a magical weapon. No special arguments."
    return _getArtifactWeaponName()
