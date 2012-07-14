import random

def _getInnName():
    colour = random.choice(['Black', 'White', 'Red', 'Blue', 'Green', 'Golden', 'Silver', 'Sable', 'Crimson', 'Yellow', 'Purple', 'Azure', 'Grey'])
    creature = random.choice(['Pony', 'Unicorn', 'Eagle', 'Ogre', 'Hound', 'Wolf', 'Goblin', 'Hog', 'Elf'])
    job = random.choice(['Knight', 'Pirate', 'Priest', 'Minstrel', 'Prince', 'Duke', 'Earl'])
    possession = random.choice(['Treasure', 'Arm', 'Den', 'Rest', 'Drink', 'Lute', 'Tavern', 'Inn'])
    state = random.choice(['Prancing', 'Laughing', 'Sleeping', 'Flying', 'Burning', 'Drunken', 'Merry'])
    return "".join(random.choice((("The ", colour, " ", creature), ("The ", colour, " ", job), ("The ", creature, "'s ", possession), ("The ", job, "'s ", possession), ("The ", state, " ", creature), ("The ", state, " ", job))))
    
def getName(args):
    return _getInnName()