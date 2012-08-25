import random

def _getEvilTitle():
  eps = ['Baron', 'Bringer', 'Champion', 'Demon', 'Duke', 'Emperor',
         'Empress', 'Harbinger', 'Heart', 'Herald', 'Lady', 'Lord',
         'Master', 'Mother', 'Overlord', 'Queen', 'Servant', 'Spawn']
  evilstuff = ['Annihilation', 'Conquest', 'Darkness', 'Decay', 'Despair',
               'Destruction', 'Doom', 'Dread', 'Famine', 'Fear', 'Fury',
               'Greed', 'Hate', 'Horror', 'Madness', 'Malice', 'Pestilence',
               'Ruin', 'Sorrow', 'Terror']
  return random.choice(eps) + " of " + random.choice(evilstuff)
  
def getName(args):
    return _getEvilTitle()
