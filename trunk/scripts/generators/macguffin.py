import random, dwarf, japanese, french

def _getMacguffinName(genre="fantasy"):
    if genre == "fantasy":
      patterns = ["the $item of $name",
                  "the $item of $thing",
                  "the $adj $item of $name",
                  "the $adj $item of $thing",
                  "the $item of $adj $thing",
                  "$name's $item of $thing"]
      itemTypes = ["eye", "scepter", "staff", "shield", "blade", "orb",
                   "sphere", "wand", "helm", "hand", "amulet", "ring"]
      stuff = ["power", "wisdom", "undeath", "destruction", "life", "holiness",
               "ice", "flames", "death", "silence", "immortality"]
      adjectives = ["freezing", "unlimited", "ultimate", "endless", "lost",
                    "forgotten", "ancient", "mystical", "arcane", "divine",
                    "forbidden", "perfect", "brilliant"]
      result = random.choice(patterns)
      result = result.replace("$item", random.choice(itemTypes).capitalize())
      result = result.replace("$thing", random.choice(stuff).capitalize())
      result = result.replace("$adj", random.choice(adjectives).capitalize())
      result = result.replace("$name", random.choice([dwarf._getDwarvenMaleName().capitalize(),
                                                     japanese._getJapaneseRandomName().capitalize(),
                                                     french._getFrenchRandomName().capitalize()]))
      return result
    else:
        return _getMacguffinName("fantasy")
    
def getName(args):
    return _getMacguffinName(args)
