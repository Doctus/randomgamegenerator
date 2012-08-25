import random

def getRelationship():
    things = ["siblings", "parent and child", "married", "lovers", "members of the same clan", 
              "members of the same guild or organization", "followers of the same god or philosophy",
              "old friends", "old rivals", "unrequited love", "arranged betrothal",
              "master and servant", "henchman and employer", "master and apprentice", "false identities of the same person",
              "old grudge", "leader and follower", "fought against each other in a war", "drinking buddies",
              "business partners", "old companions", "erstwhile allies", "ideological enemies",
              "allies for political convenience", "mentor and pupil", "teacher and student", "colleagues",
              "healer and patient", "bound by life debt", "childhood friends", "con artist and mark",
              "distant relatives", "like family", "competitors", "both swore the same oath",
              "fellow cultists", "inseparable partners", "pen pals", "benefactor and beneficiary",
              "members of the same secret society", "former lovers", "bitter foes",
              "avenger and target", "keepers of the same secret", "part of a love triangle",
              "last survivors of some group", "no one else knows about the crime they committed",
              "writer/artist/musician and fan", "co-conspirators", "enemies of the same enemy",
              "friends of the same friend", "servants of the same master", "grew up in the same town"]
    stuff = random.choice(things)
    stuff2 = "".join((stuff, random.choice(["", "", "", "", "", "", "", "".join((", and ", random.choice(things))), "".join((", and ", random.choice(things))), "... or so they think", "... until recently"])))
    return stuff2
    
def getName(args):
    return getRelationship()
