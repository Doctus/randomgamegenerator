import random

def _generateGoodMG():
    goodAdj = ["Aqua","Beat","Beauty","Blizzard","Blue","Burst","Circle","Clear","Clover","Crystal","Diamond","Dream","Emerald","Espoir","Eternal","Fantastic","Finale","Fire","Five","Flash","Floral","Galaxy","Gold","Golden","Grand","Happiness","Happy","Harmony","Healing","Heart","Heartful","Holy","Infinity","Jewel","Light","Love","Loving","Lucky","Luminous","Marble","Millennium","Mint","Miracle","Musical","Passionate","Piacere","Pink","Prayer","Pretty","Prism","Protection","Rainbow","Rose","Rouge","Ruby","Saint","Sapphire","Shining","Silver","Solar","Sonic","Sparkling","Spiral","Splash","Star","Starlight","Storm","Sunny","Sunshine","Super","Therapy","Thunder","True","Wave","White","Smile","Prismatic"]
    someNouns = ["Crystal","Scepter","Staff","Chalice","Mirror","Crystals","Pendule","Bell","Stones","Lights"]
    goodMac = str("The %s %s" % (random.choice(goodAdj),random.choice(someNouns)))
    return goodMac
    
def getName(args):
    return _generateGoodMG()