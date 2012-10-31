import random

def _getJapaneseMaleName():
  names = ['Risuke', 'Ichirou', 'Heisuke', 'Hajime', 'Tarou',
           'Keisuke', 'Hideki', 'Shuusuke', 'Touya', 'Minoru',
           'Mitsuo', 'Tetsuji', 'Hideo', 'Shuuji', 'Shinnosuke',
           'Mitsunori', 'Hirotaro', "Jun'ichi", 'Kazuo', 'Hiroshi',
           'Masatoshi', 'Hitoshi', 'Akira', 'Hiroto', 'Ren', 'Yuto',
           'Satoshi', 'Kei', 'Hiroki', 'Kenjirou', 'Kenshirou', 'Kenji',
           'Tatsuhiko']
  return random.choice(names)

def _getJapaneseFemaleName():
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
  return (_getJapaneseSurname() + " " + _getJapaneseRandomName())

def getName(args):
    if args == "help": return "Generates a Japanese name. Valid arguments are 'full' or 'surname' (given-only will be assumed if neither is passed) and 'male' or 'female'."
    if "female" in args and "full" in args:
        return _getJapaneseFemaleFullName()
    elif "male" in args and "full" in args:
        return _getJapaneseMaleFullName()
    elif "male" in args:
        return _getJapaneseMaleName()
    elif "female" in args:
        return _getJapaneseFemaleName()
    elif "surname" in args:
        return _getJapaneseSurname()
    elif "full" in args:
        return _getJapaneseRandomFullName()
    else:
        return _getJapaneseRandomName()
