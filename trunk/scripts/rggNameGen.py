#rggNameGen - for the Random Game Generator project
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

def _getEvilTitle():
  eps = ['Baron', 'Bringer', 'Champion', 'Demon', 'Duke', 'Emperor',
         'Empress', 'Harbinger', 'Heart', 'Herald', 'Lady', 'Lord',
         'Master', 'Mother', 'Overlord', 'Queen', 'Servant', 'Spawn']
  evilstuff = ['Annihilation', 'Conquest', 'Darkness', 'Decay', 'Despair',
               'Destruction', 'Doom', 'Dread', 'Famine', 'Fear', 'Fury',
               'Greed', 'Hate', 'Horror', 'Madness', 'Malice', 'Pestilence',
               'Ruin', 'Sorrow', 'Terror']
  return random.choice(eps) + " of " + random.choice(evilstuff)

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

def _getJapaneseRandomName():
  if random.choice([True, False]):
    return _getJapaneseMaleName()
  return _getJapaneseFemaleName()

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

def _getJapaneseMaleFullName():
  return (_getJapaneseSurname() + " " + _getJapaneseMaleName())

def _getJapaneseFemaleFullName():
  return (_getJapaneseSurname() + " " + _getJapaneseFemaleName())

def _getJapaneseRandomFullName():
  if random.choice([True, False]):
    return (_getJapaneseSurname() + " " + _getJapaneseMaleName())
  return (_getJapaneseSurname() + " " + _getJapaneseFemaleName())

def _getArtifactWeaponName():
  adj = ['black', 'white', 'great', 'dread', 'fell', 'dark', 'sacred', 'vorpal',
         'unholy', 'bursting', 'shining', 'vaulting', 'holy', 'dead', 'eternal',
         'red', 'green', 'blue', 'crimson', 'violet', 'iridescent', 'grand',
         'supreme', 'titanic', 'screaming', 'ruby', 'sapphire', 'nightmare']
  combine = ['bless', 'mourn', 'flare', 'death', 'god', 'doom', 'thorn', 'vine',
             'ice', 'flame', 'hate', 'star', 'sun', 'moon', 'stone', 'earth',
             'spark', 'poison', 'soul', 'mist']
  post = ['blessing', 'mourning', 'winter', 'heaven', 'hell', 'doom', 'destruction',
          'love', 'transcendent skill', 'might', 'cunning', 'sagacity', 'wisdom',
          'sorrow', 'dawn', 'twilight', 'sunset', 'nightmare']
  numbers = ['four', 'seven', 'nine', 'twelve', 'thirteen', 'hundred', 'thousand']
  numpost = ['blessings', 'gods', 'winters', 'hells', 'heavens', 'sages',
             'savants', 'wizards', 'archmagi', 'warlords', 'sunsets', 'dawns',
             'dreams']
  weaps = ['blade', 'cleaver', 'dagger', 'hammer', 'mace',
           'sword', 'spear', 'lance', 'dirk', 'flail',
           'axe', 'bow']
  patterns = ["the $adj $comb$weap of $post",
              "the $comb$weap",
              "the $Weap of the $numb $numpost",
              "the $adj $Weap of $post",
              "the $adj $Weap of the $numb $numpost",
              "the $comb$weap of the $numb $adj $numpost",
              "the $Weap of the $numb $adj $numpost",
              "the $adj $comb$weap",
              "the $Weap of $numpost"]
  pat = random.choice(patterns)
  pat = pat.replace("$adj", random.choice(adj).capitalize())
  pat = pat.replace("$comb", random.choice(combine).capitalize())
  pat = pat.replace("$post", random.choice(post).capitalize())
  pat = pat.replace("$numb", random.choice(numbers).capitalize())
  pat = pat.replace("$numpost", random.choice(numpost).capitalize())
  pat = pat.replace("$weap", random.choice(weaps))
  pat = pat.replace("$Weap", random.choice(weaps).capitalize())
  return pat

def _generateAdvice():
  anto = [['+cold', '+heat'], ['wisdom', '+fool'], ['+light', '+darkness'],
        ['victory', 'defeat'], ['evil', 'good'], ['sound', 'silence']]
  phrases = ["To find +~#, you must look within +@%.",
           "The greatest ~# is in the middle of +@%.",
           "The path of ~# leads to @%.",
           "Be wary of the ~# that cloaks itself as @%.",
           "When you see ~#, @% lies just above."]
  advice = random.choice(phrases)
  subject = random.choice(anto)
  if random.choice([True, False]): subject.reverse()
  advice = advice.replace("~#", subject[0])
  advice = advice.replace("@%", subject[1])
  advice = advice.replace('++', 'the ')
  advice = advice.replace('+', '')
  advice = advice.capitalize()
  return advice

def _generateTechniqueName(typ='rand', elemnt='rand', moral='rand',
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
                          'forsaken', 'flawless', 'cacophonic', 'overwhelming',
                          'ferocious', 'unstoppable', 'lunar', 'solar']
  impressiveAuxNouns = ['gods', 'star', 'blade', 'ultimatum', 'emperor', 'sorrow',
                        'tears', 'destiny', 'silence', 'void', 'lion', 'master',
                        'brilliance', 'wheel', 'oblivion']
  impressiveNouns = ['progression', 'barrage', 'works', 'cascade', 'anathema',
                     'apocalypse', 'prana', 'kata', 'technology', 'method',
                     'perfection', 'excellency']
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
    result = random.choice([", ", " - ", " of the "]).join([_generateTechniqueName(typ, elemnt, moral, complexity-4, True),
                                                            _generateTechniqueName(typ, elemnt, moral, 4, True)])
  if typ == 'magic' or (typ == 'rand' and typindex['rand'] == magicnoun):
    if random.choice([True, False, False]):
      result = (random.choice([_getJapaneseSurname(), _getDwarvenMaleName()]) + "'s ") + result
  return result

def getTechniqueName(st):
  if len(st) <= 0:
    return _generateTechniqueName()
  argCompilation = ['rand', 'rand', 'rand', -1, False]
  if st.find("martial") != -1:
      argCompilation[0] = 'martial'
  elif st.find("magic") != -1:
      argCompilation[0] = 'magic'
  if st.find("fire") != -1:
      argCompilation[1] = 'fire'
  elif st.find("ice") != -1:
      argCompilation[1] = 'ice'
  elif st.find("darkness") != -1:
      argCompilation[1] = 'darkness'
  elif st.find("light") != -1:
      argCompilation[1] = 'light'
  elif st.find("psionic") != -1:
      argCompilation[1] = 'psionic'
  elif st.find("violent") != -1:
      argCompilation[1] = 'violent'
  if st.find("good") != -1:
      argCompilation[2] = 'good'
  elif st.find("neutral") != -1:
      argCompilation[2] = 'neutral'
  elif st.find("evil") != -1:
      argCompilation[2] = 'evil'
  if st.find("simple") != -1:
      argCompilation[3] = 2
  elif st.find("moderate") != -1:
      argCompilation[3] = 3
  elif st.find("complex") != -1:
      argCompilation[3] = 4
  if st.find("awesome") != -1 or st.find("hotblood") != -1 or st.find("cool") != -1:
      argCompilation[4] = True
  if st.find("exalted") != -1:
      argCompilation[3] = random.choice([4, 7, 8, 10, 11, 12, 15])
  return _generateTechniqueName(argCompilation[0], argCompilation[1], argCompilation[2],
                                                  argCompilation[3], argCompilation[4])

def getAdvice():
  #We might want to do more here at some point, hence breaking it up.
  return _generateAdvice()

def _getKaleidoscope():
  blegh = random.choice([getName(random.choice(getName('kaikeys'))),
                         getName(random.choice(getName('kaikeys'))),
                         getName(random.choice(getName('kaikeys'))),
                         getTechniqueName('cool exalted')])
  blegh = blegh.split()
  if len(blegh) > 1:
    blegh[1] = random.choice([getName(random.choice(getName('kaikeys'))),
                              getName(random.choice(getName('kaikeys'))),
                              getName(random.choice(getName('kaikeys'))),
                              getTechniqueName('cool exalted')])
  else:
    blegh = blegh + random.choice([getName(random.choice(getName('kaikeys'))),
                                   getName(random.choice(getName('kaikeys'))),
                                   getName(random.choice(getName('kaikeys'))),
                                   getTechniqueName('cool exalted')]).split()
  blegh = " ".join(blegh)
  return blegh

def getName(nametype):
  '''Return a random name of a type defined by the input string.
      The input can be the name of a valid style (dwarf, Japanese, or elf)
      in which case either a male or female name will be returned
      with equal probability, or it can take a form like 'dwarfmale'
      if a specific gender is desired.
  '''
  typedic = {"dwarfmale":_getDwarvenMaleName,
             "dwarf":_getDwarvenMaleName,
             "dwarffemale":_getDwarvenFemaleName,
             "japanesemale":_getJapaneseMaleName,
             "japanese":_getJapaneseRandomName,
             "japanesefemale":_getJapaneseFemaleName,
             "japanesemalefull":_getJapaneseMaleFullName,
             "japanesefemalefull":_getJapaneseFemaleFullName,
             "japanesefull":_getJapaneseRandomFullName,
             "weapon":_getArtifactWeaponName,
             "eviltitle":_getEvilTitle,
             "kaijyuu":_getKaleidoscope}
  if nametype == "keys":
    return typedic.keys()
  if nametype == 'kaikeys':
    return ['dwarfmale', 'japanesefull', 'weapon', 'eviltitle']
  return typedic[nametype]()
