#rggNameGen - for the Random Game Generator project
# v. 0.01  >> THIS IS MERELY A DEMONSTRATION INTENDED FOR
#             FUTURE REFERENCE AND IS NOT FULLY FUNCTIONAL.
#
#By Doctus (kirikayuumura.noir@gmail.com)
'''
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
'''

import random

def _assembleName(ph, pa):
  name = []
  for r in pa:
    name.append(random.choice(ph[r]))
  return (''.join(name)).capitalize()

def _getDwarvenMaleName():
  '''Data drawn from: Durin, Nithi, Northri, Suthri, Austri, Vestri,
      Dvalin, Nar, Nain, Niping, Dain, Bifur, Bofur, Bombur, Nori,
      Thorin, Thror, Vit, Lit, Dvarfil'''
  phonemes = [['d', 'n', 'b', 'v', 'th', 'dv', 'l'], #Beginblends
              ['th', 'p', 'mb', 'l', 'f'], #Midblends
              ['u', 'i', 'a'], #Vowels
              ['r'], #Oddly 'r' appears where nothing else can
              ['n', 'r', 'ng', 'l'], #Endconsonants
              ['i']] #Endvowel. Again, odd.
  patterns = [[0, 2, 3, 2, 4], #Durin
                   [0, 2, 1, 5], #Nithi
                   [0, 2, 3, 1, 3, 5], #Northri
                   [0, 2, 1, 3, 5], #Suthri
                   [0, 2, 1, 2, 4], #Dvalin
                   [0, 2, 2, 4], #Dain
                   [0, 3, 2, 4], #Thror
                   [0, 2, 3, 1, 2, 4]] #Dvarfil
  return _assembleName(phonemes, random.choice(patterns))

def _getDwarvenFemaleName():
  '''lolz, I don't know of any!'''
  return _getDwarvenMaleName()

def _getJapaneseMaleName():
  '''Data drawn from personal knowledge (special case)'''
  names = ['Risuke', 'Ichirou', 'Heisuke', 'Hajime', 'Tarou',
           'Keisuke', 'Hideki', 'Shuusuke', 'Touya', 'Minoru',
           'Mitsuo', 'Tetsuji', 'Hideo', 'Shuuji', 'Shinnosuke',
           'Mitsunori', 'Hirotaro', "Jun'ichi", 'Kazuo', 'Hiroshi',
           'Masatoshi', 'Hitoshi', 'Akira', 'Hiroto', 'Ren', 'Yuto',
           'Satoshi', 'Kei', 'Hiroki', 'Kenjirou', 'Kenshirou', 'Kenji',
           'Tatsuhiko']
  return random.choice(names)

def _getJapaneseFemaleName():
  '''Data drawn from personal knowledge (special case)'''
  names = ['Yohko', 'Megumi', 'Sakura', 'Hanako', 'Ai', 'Hirano',
           'Takako', 'Nana', 'Izumi', 'Aki', 'Yuki', 'Yoshiko',
           'Aya', 'Yuri', 'Hina', 'Rina', 'Yuuna', 'Yukiko', 'Mai',
           'Aoi', 'Nanase', 'Natsumi']
  return random.choice(names)

def _getJapaneseSurname():
  '''Data drawn from personal knowledge (special case)'''
  names = ['Yagi', 'Tanaka', 'Ueda', 'Yamagawa', 'Yamamoto',
           'Munenori', 'Satou', 'Suzuki', 'Takahashi', 'Watanabe',
           'Itou', 'Nakamura', 'Kobayashi', 'Saitou', 'Katou', 'Yoshida',
           'Yamada', 'Sasaki', 'Yamaguchi', 'Matsumoto', 'Inoue', 'Kimura',
           'Hayashi', 'Shimizu', 'Yamazaki', 'Mori', 'Abe', 'Ikeda',
           'Hashimoto', 'Yamashita', 'Ishikawa', 'Nakajima', 'Maeda',
           'Fujita', 'Ogawa', 'Okada', 'Gotou', 'Hasegawa', 'Murakami',
           'Kondou', 'Ishii', 'Sakamoto', 'Endou', 'Aoki', 'Fujii',
           'Nishimura', 'Fukuda', 'Outa', 'Miura', 'Fujiwara', 'Matsuda',
           'Nakagawa', 'Nakano', 'Tokunaga']
  return random.choice(names)

def _getJapaneseFullName(g=False):
  if g: return (_getJapaneseSurname() + " " + _getJapaneseMaleName())
  return (_getJapaneseSurname() + " " + _getJapaneseFemaleName())

def getTechniqueName(typ='rand', elemnt='rand', moral='rand',
                      complexity=-1, hotblood=False):
  if complexity == -1:
    complexity = random.randrange(2, 5)
  fireadj = [['burning', 'flaring', 'flaming'],
             ['blazing', 'purifying'],
             ['searing', 'scorching', 'consuming', 'ashmaking']]
  firenoun = [['fireball', 'nova', 'ember', 'incineration'],
              ['flame', 'flare'],
              ['blaze', 'blast']]
  iceadj = [['north', 'ice', 'freezing', 'cold', 'arctic'],
            ['boreal', 'snow'],
            ['glacial', 'shivering']]
  icenoun = [['spike', 'glacier', 'iceberg', 'freeze'],
             ['blizzard', 'snowflake'],
             ['frostbite', 'winter']]
  lightadj = [['glowing', 'flourescent', 'shimmering'],
              ['shining', 'glittering', 'iridescent'],
              ['blinding', 'erasing']]
  lightnoun = [['ray', 'beam', 'aura', 'glow'],
               ['projection', 'flash'],
               ['laser', 'emanation']]
  darkadj = [['shadow', 'shade', 'dim', 'void', 'fading'],
             ['moonlight', 'faint'],
             ['darkness', 'stygian', 'hell', 'abyssal']]
  darknoun = [['veil', 'shadow', 'murk'],
              ['nocturne', 'eclipse'],
              ['propagation', 'wave']]
  psiadj = [['mind', 'mental', 'telekinetic', 'psychic'],
            ['psionic'],
            ['brain', 'thought']]
  psinoun = [['thrust', 'force', 'blast'],
             ['mind'],
             ['probe', 'invasion']]
  violentadj = [['slashing', 'crushing', 'bursting', 'vorpal'],
                ['disintegrating', 'annihilating', 'piercing'],
                ['decapitating', 'mauling', 'slaughtering']]
  violentnoun = [['killer', 'death', 'slash', 'thrust', 'crush'],
                 ['finisher', 'pierce'],
                 ['massacre', 'slaughter', 'murder']]
  elindex = {'fire':[fireadj, firenoun],
             'darkness':[darkadj, darknoun],
             'ice':[iceadj, icenoun],
             'light':[lightadj, lightnoun],
             'psionic':[psiadj, psinoun],
             'violent':[violentadj, violentnoun],
             'rand':[random.choice([fireadj, darkadj, iceadj, lightadj, psiadj, violentadj]),
                     random.choice([firenoun, darknoun, icenoun, lightnoun, psinoun, violentnoun])]}
  if moral == 'rand':
    morality = random.choice([[0, 0, 1], [0], [0, 0, 2]])
  elif moral == 'neutral':
    morality = [0]
  elif moral == 'good':
    morality = [0, 0, 1]
  elif moral == 'evil':
    morality = [0, 0, 2]
  martialnoun = ['fist', 'kick', 'slam', 'technique', 'style', 'way', 'grasp', 'hold', 'grapple']
  magicnoun = ['ritual', 'spell', 'hex', 'curse', 'geas', 'invocation', 'evocation', 'conjuration',
               'abjuration']
  typindex = {'martial':martialnoun,
              'magic':magicnoun,
              'rand':random.choice([martialnoun, magicnoun])}
  impressiveAdjectives = ['invulnerable', 'invincible', 'forgotten', 'ancient',
                          'forbidden', 'extraordinary', 'kaleidoscopic', 'first',
                          'vaulting', 'unrivalled', 'unlimited', 'endless',
                          'cascading', 'spotless', 'secret', 'sorrowful', 'ashen',
                          'forsaken']
  impressiveAuxNouns = ['gods', 'star', 'blade', 'ultimatum', 'emperor', 'sorrow',
                        'tears', 'destiny', 'silence', 'void', 'lion']
  impressiveNouns = ['progression', 'barrage', 'works', 'cascade', 'anathema',
                     'apocalypse']
  if complexity <= 2:
    result = " ".join([random.choice(elindex[elemnt][0][random.choice(morality)]).capitalize(),
                      random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]),
                                    random.choice(typindex[typ])]).capitalize()])
  elif complexity == 3:
    if hotblood:
      if random.choice([True, False]):
        result = " ".join([random.choice(elindex[elemnt][0][random.choice(morality)]+impressiveAdjectives).capitalize(),
                           random.choice(elindex[elemnt][0][random.choice(morality)]+impressiveAdjectives+impressiveAuxNouns).capitalize(),
                            random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]+impressiveNouns),
                                      random.choice(typindex[typ])]+impressiveNouns).capitalize()])
      else:
        result = " ".join([random.choice(typindex[typ]+impressiveNouns).capitalize(), 'of the',
                           random.choice(elindex[elemnt][0][random.choice(morality)]+impressiveAdjectives).capitalize(),
                            random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]+impressiveAuxNouns),
                                      random.choice(typindex[typ])]+impressiveAuxNouns).capitalize()])
    else:
      if random.choice([True, False]):
        result = " ".join([random.choice(elindex[elemnt][0][random.choice(morality)]).capitalize(),
                           random.choice(elindex[elemnt][0][random.choice(morality)]).capitalize(),
                            random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]),
                                      random.choice(typindex[typ])]).capitalize()])
      else:
        result = " ".join([random.choice(typindex[typ]).capitalize(), 'of the',
                           random.choice(elindex[elemnt][0][random.choice(morality)]).capitalize(),
                            random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]),
                                      random.choice(typindex[typ])]).capitalize()])
  elif complexity == 4 or (complexity >= 5 and not hotblood):
    if hotblood:
      if random.choice([True, False]):
        result = " ".join([random.choice(elindex[elemnt][0][random.choice(morality)]+impressiveAdjectives).capitalize(),
                            random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]+impressiveNouns),
                                      random.choice(typindex[typ]+impressiveNouns)]).capitalize(), 'of the',
                           random.choice(elindex[elemnt][0][random.choice(morality)]+impressiveAdjectives).capitalize(),
                            random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]+impressiveAuxNouns),
                                      random.choice(typindex[typ]+impressiveAuxNouns)]).capitalize()])
      else:
        result = " ".join([random.choice(elindex[elemnt][0][random.choice(morality)]+impressiveAdjectives).capitalize(),
                           random.choice(elindex[elemnt][0][random.choice(morality)]+impressiveAdjectives).capitalize(),
                            random.choice(elindex[elemnt][1][random.choice(morality)]+impressiveAuxNouns).capitalize(),
                            random.choice(typindex[typ]+impressiveNouns).capitalize()])
    else:
      if random.choice([True, False]):
        result = " ".join([random.choice(elindex[elemnt][0][random.choice(morality)]).capitalize(),
                            random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]),
                                      random.choice(typindex[typ])]).capitalize(), 'of the',
                           random.choice(elindex[elemnt][0][random.choice(morality)]).capitalize(),
                            random.choice([random.choice(elindex[elemnt][1][random.choice(morality)]),
                                      random.choice(typindex[typ])]).capitalize()])
      else:
        result = " ".join([random.choice(elindex[elemnt][0][random.choice(morality)]).capitalize(),
                           random.choice(elindex[elemnt][0][random.choice(morality)]).capitalize(),
                            random.choice(elindex[elemnt][1][random.choice(morality)]).capitalize(),
                            random.choice(typindex[typ]).capitalize()])
  elif complexity >= 5:
    result = random.choice([", ", " - ", " of the "]).join([getTechniqueName(typ, elemnt, moral, complexity-4, True),
                                                            getTechniqueName(typ, elemnt, moral, 4, True)])
  if typ == 'magic' or (typ == 'rand' and typindex['rand'] == magicnoun):
    if random.choice([True, False, False]):
      result = (random.choice([_getJapaneseSurname(), _getDwarvenMaleName()]) + "'s ") + result
  return result

def getName(nametype):
  '''Return a random name of a type defined by the input string.
      The input can be the name of a valid style (dwarf, Japanese, or elf)
      in which case either a male or female name will be returned
      with equal probability, or it can take a form like 'dwarfmale'
      if a specific gender is desired.
  '''
  try:
    if nametype == "dwarfmale" or (nametype == "dwarf" and
                                   random.choice([True, False])):
      return (_getDwarvenMaleName())
    elif nametype == "dwarffemale" or nametype == "dwarf":
      return (_getDwarvenFemaleName())
    elif nametype == "japanesemale" or (nametype == "japanese" and
                                        random.choice([True, False])):
      return (_getJapaneseMaleName())
    elif nametype == "japanesefemale" or nametype == "japanese":
      return (_getJapaneseFemaleName())
    elif nametype == "japanesemalefull" or (nametype == "japanesefull" and
                                        random.choice([True, False])):
      return (_getJapaneseFullName(True))
    elif nametype == "japanesefemalefull" or nametype == "japanesefull":
      return (_getJapaneseFullName())
    else:
      return "Error McInvalidArgument"
  except:
    return "Error McProblem"
