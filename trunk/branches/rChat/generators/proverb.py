import random

def _getProverb():
    patterns = ["$nadj $thing draws $entities",
                "never $verb a$adj $entity",
                "a$adj $entity and a$adj $entity $frequency meet",
                "$verb $nadj $entities"]
    adjectives = [" good", "n honest", " bad", "n evil", " wasted", " wise", 
                  " ill"]
    things = ["seed", "counsel", "work", "riches", "effort", "time"]
    entities = [["thief", "thieves"], ["bird", "birds"],
                ["flatterer", "flatterers"]]
    verbs = ["trust", "kill", "harm", "be"]
    frequencies = ["often", "seldom", "never", "sometimes"]
    result = random.choice(patterns)
    while "$nadj" in result: result = result.replace("$nadj", random.choice(adjectives)[1:].strip(), 1)
    while "$adj" in result: result = result.replace("$adj", random.choice(adjectives), 1)
    while "$thing" in result: result = result.replace("$thing", random.choice(things), 1)
    while "$entity" in result: result = result.replace("$entity", random.choice(entities)[0], 1)
    while "$entities" in result: result = result.replace("$entities", random.choice(entities)[1], 1)
    while "$verb" in result: result = result.replace("$verb", random.choice(verbs), 1)
    while "$frequency" in result: result = result.replace("$frequency", random.choice(frequencies), 1)
    result = result.capitalize() + "."
    return result
    
def getName(args):
    if args == "help": return "Generates a vaguely proverb-like statement. No special arguments."
    return _getProverb()
