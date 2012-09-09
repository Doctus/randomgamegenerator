import random, japanese, dwarf

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
  dancenoun = ['step', 'spin', 'walk', 'waltz', 'shuffle', 'drop', 'flare', 'spin']
  typindex = {'martial':martialnoun,
              'magic':magicnoun,
              'dance':dancenoun,
              'rand':random.choice([martialnoun, magicnoun, dancenoun])}
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
      result = (random.choice([japanese._getJapaneseSurname(), dwarf._getDwarvenMaleName()]) + "'s ") + result
  return result

def getTechniqueName(st):
  if len(st) <= 0:
    return _generateTechniqueName()
  argCompilation = ['rand', 'rand', 'rand', -1, False]
  if st.find("martial") != -1:
      argCompilation[0] = 'martial'
  elif st.find("magic") != -1:
      argCompilation[0] = 'magic'
  elif st.find("dance") != -1:
      argCompilation[0] = 'dance'
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

def getName(args):
    if args == "help": return "Generates a special technique name. Valid arguments are any one of 'martial' 'magic' 'dance' and/or any one of 'fire' 'ice' 'darkness' 'light' 'psionic' 'violent' and/or any one of 'good' 'neutral' 'evil' and/or any one of 'simple' 'moderate' 'complex' 'exalted' and/or 'awesome'."
    return getTechniqueName(args)
