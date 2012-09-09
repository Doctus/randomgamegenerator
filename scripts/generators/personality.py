import random

personalitytraits = [["Argumentative","Garrulous","Hot-tempered","Overbearing","Articulate","Antagonistic","Quiet","Laconic","Soft-spoken","Secretive","Retiring","Mousy"],
          ["Arrogant","Haughty","Elitist","Proud","Rude","Aloof"],
          ["Capricious","Mischievous","Impulsive","Irreverent","Madcap"],
          ["Careless","Thoughtless","Absent-minded","Dreamy","Insensitive"],
          ["Courageous","Brave","Craven","Shy","Fearless","Obsequious"],
          ["Curious","Inquisitive","Prying","Intellectual","Perceptive","Keen"],
          ["Exacting","Perfectionist","Stern","Harsh","Punctual","Driven"],
          ["Friendly","Trusting","Kind-hearted","Forgiving","Easy-going","Compassionate","Moody","Gloomy","Morose","Irritable","Vengeful"],
          ["Greedy","Miserly","Hard-headed","Covetous","Avaricious","Thrifty","Generous","Wastrel","Spendthrift","Extravagant","Charitable"],
          ["Naive","Honest","Truthful","Innocent","Gullible","Foolhardy"],
          ["Opinionated","Bigoted","Biased","Narrow-minded","Blustering","Hide-bound"],
          ["Optimistic","Cheerful","Happy","Diplomatic","Pleasant","Pessimistic","Fatalistic","Cynical","Sarcastic"],
          ["Sober","Practical","Level-headed","Realistic","Dull","Reverent","Ponderous"],
          ["Suspicious","Scheming","Paranoid","Cautious","Deceitful","Nervous"],
          ["Uncivilized","Uncultured","Boorish","Barbaric","Graceless","Crude"],
          ["Violent","Cruel","Sadistic","Immoral","Jealous"]]

def _getPersonality():
    types = random.sample(personalitytraits, 2)
    trait1 = random.choice(types[0])
    trait2 = random.choice(types[1])
    pattern = random.choice(["and", "and", "and sometimes", "and slightly", "and rather"])
    return " ".join((trait1, pattern, trait2))
    
def getName(args):
    if args == "help": return "Generates a brief personality description. No special arguments."
    return _getPersonality()
