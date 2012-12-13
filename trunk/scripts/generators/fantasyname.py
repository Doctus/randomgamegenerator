import random, re

double_letters = []
double = re.compile(r"(.)\1")
with open("2of12inf.txt", "r") as f:
    words = f.readlines()
for word in words:
    if double.search(word) and len(word) < 9 and "lly" not in word[-4:] and "ed" not in word[-3:] and "ing" not in word[-4:]:
        double_letters.append(word)

def singlify(matchobj):
    return matchobj.group(0)[0]
        
def _getFantasy():
    word = random.choice(double_letters)
    return double.sub(singlify, word[:-1])
    
def getName(args):
    if args == "help": return "Generates a fantasy-ish name by removing a double letter from an actual word."
    return _getFantasy()