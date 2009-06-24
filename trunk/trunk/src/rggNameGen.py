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
  '''Data drawn from:'''
  return 'NYI'
  phonemes = []
  patterns = []
  return _assembleName(phonemes, random.choice(patterns))

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
           'Aoi']
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
