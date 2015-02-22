import random, re

double_letters = []
double = re.compile(r"(.)\1")
with open("2of12inf.txt", "r") as f:
    words = f.readlines()
for word in words:
    if double.search(word) and len(word) < 9 and "lly" not in word[-4:] and "ed" not in word[-3:] and "ing" not in word[-4:]:
        double_letters.append(word)

beginning = list(set('''jac mas will jayd n mich eth al aid dan anth matt josh andr jam dav log gabr sam nat luc land cal gav tyl luk jord brand jul aar jerem ang conn henr just aust rob soph isab emm oliv av emil abig madis m chl ell addis natal lil aver sof vic evel alex l amel z layl kat kayl alys alic sar ashl audr'''.split()))

end = list(set('''ob on am en oah ael an er en el ew ah ua am ew es id in an er eph on iel uel ohn as ian an eb on aac in en er e an er as ah en att ert in i ia a y ail oe eth ie ey yn'''.split()))
        
def singlify(matchobj):
    return matchobj.group(0)[0]

def _getParts():
    return (random.choice(beginning) + random.choice(end)).title()
        
def _getDouble():
    word = random.choice(double_letters)
    return double.sub(singlify, word[:-2]).title()
    
def getName(args):
    if args == "help": return "Generates a fantasy-ish name by: combining parts of two real names ('parts') or removing a double letter from an actual word ('double')."
    elif args == "double":
        return _getDouble()
    elif args == "parts":
        return _getParts()
    return _getParts()