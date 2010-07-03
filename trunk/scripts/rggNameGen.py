# -*- coding: utf-8 -*-
#
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
  return _getDwarvenMaleName()

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
  if random.choice([True, False]):
    return (_getJapaneseSurname() + " " + _getJapaneseMaleName())
  return (_getJapaneseSurname() + " " + _getJapaneseFemaleName())

def _getFrenchFemaleName():
  names = [u"Adélaïde", u"Adèle", u"Adrienne", u"Agathe", u"Agnès", u"Aile", u"Aimée", u"Alaine", u"Albane", u"Alette", u"Alexandra", u"Alexanne", u"Alexis", u"Alice", u"Aline", u"Alix", u"Alizée", u"Amalie", u"Amandine", u"Ambre", u"Amée", u"Amélie", u"Anabelle", u"Anaëlle", u"Anaïs", u"Andréanne", u"Andrée", u"Andréa", u"Andrie", u"Ange", u"Angélique", u"Annabelle", u"Anne", u"Anne-Marie", u"Anne-Sophie", u"Annette", u"Annick", u"Annie", u"Antoinette", u"Appoline", u"Ariane", u"Arielle", u"Arlette", u"Armelle", u"Astérie", u"Aubine", u"Aurélie", u"Aurore", u"Avril", u"Axelle", u"Babette", u"Barbe", u"Béatrice", u"Belle", u"Bernadette", u"Bernice", u"Bertille", u"Bien", u"Aimée", u"Blaisotte", u"Blanche", u"Blanchette", u"Bluette", u"Brigitte", u"Calanthe", u"Camille", u"Capucine", u"Carolane", u"Carole", u"Caroline", u"Cassandre", u"Catherine", u"Cécilie", u"Celeste", u"Célia", u"Céline", u"Cerise", u"Chanel", u"Chantal", u"Charline", u"Charlotte", u"Charmaine", u"Cherie", u"Chloë", u"Christelle", u"Christiane", u"Christine", u"Claire", u"Claire-Marie", u"Clarisse", u"Claude", u"Claudette", u"Claudie", u"Claudine", u"Clémence", u"Clémentine", u"Clervie", u"Cloé", u"Clothilde", u"Clotilde", u"Colette", u"Coline", u"Colombe", u"Constance", u"Coralie", u"Cordélie", u"Corentine", u"Corinne", u"Cornélie", u"Cosette", u"Crescence", u"Danielle", u"Daphné", u"Daphnée", u"Delphine", u"Denise", u"Desirée", u"Dianne", u"Dionne", u"Dominique", u"Doralice", u"Doré", u"Dorette", u"Doriane", u"Dorothée", u"Drucilla", u"Égérie", u"Elaine", u"Éléanore", u"Eléna", u"Éliane", u"Élisabeth", u"Elise", u"Élizabeth", u"Élodie", u"Eloise", u"Emeline", u"Émilie", u"Émilienne", u"Emmanuelle", u"Emy", u"Ernestine", u"Esmé", u"Estée", u"Estelle", u"Eugénie", u"Eulalie", u"Evangeline", u"Eve", u"Evelyne", u"Fabienne", u"Fanette", u"Fanny", u"Fantine", u"Fernande", u"Fifi", u"Flamine", u"Fleur", u"Florence", u"Florie", u"Francine", u"Françoise", u"Frédérique", u"Gabrielle", u"Geneviève", u"Georgette", u"Georgine", u"Germaine", u"Gervaise", u"Ghislaine", u"Ginette", u"Gisèle", u"Grâce", u"Hélène", u"Héloïse", u"Henriette", u"Hermine", u"Hyacinthe", u"Inés", u"Irène", u"Iris", u"Isabeau", u"Isabelle", u"Jacqueline", u"Janine", u"Jeand'arc", u"Jeanette", u"Jeanine", u"Jeanne", u"Jeanne-Aimée", u"Jeanne-Yvette", u"Jeannine", u"Jenevieve", u"Joëlle", u"Josephine", u"Josette", u"Josiane", u"Julie", u"Juliette", u"Justine", u"Karine", u"Laetitia", u"Laure", u"Laurence", u"Lauriane", u"Laurianne", u"Laurie", u"Laurine", u"Léa", u"Léonie", u"Léonore", u"Liane", u"Lianne", u"Liliane", u"Lilianne", u"Lise", u"Lisette", u"Loraine", u"Loréline", u"Lorraine", u"Louise", u"Lucie", u"Lucienne", u"Lucile", u"Lucille", u"Lucrèce", u"Ludivine", u"Lydie", u"Mabelle", u"Madeleine", u"Maelle", u"Magalie", u"Manon", u"Marcelle", u"Margaux", u"Margot", u"Marguerite", u"Marianne", u"Marie", u"Marie-Anne", u"Marie-Claire", u"Marie-Claude", u"Marie-Ève", u"Marie-France", u"Marie-Hélène", u"Marie-Laure", u"Marielle", u"Marie-Louise", u"Marie-Noelle", u"Marie-Pier", u"Marie-Pierre", u"Marie-Sophie", u"Marie-Sylvie", u"Marie-Thérèse", u"Marine", u"Marion", u"Marjolaine", u"Marthe", u"Martine", u"Mathilde", u"Maude", u"Maxime", u"Maxine", u"Mégane", u"Mélaine", u"Mélanie", u"Mélina", u"Mélissa", u"Mélodie", u"Michèle", u"Micheline", u"Mignon", u"Mimi", u"Minerve", u"Mirabelle", u"Mireille", u"Monette", u"Monique", u"Morgane", u"Musette", u"Mylène", u"Myriam", u"Nadège", u"Nadine", u"Nanette", u"Natalie", u"Nathalie", u"Nicole", u"Nicolette", u"Noelle", u"Noemi", u"Noémie", u"Océane", u"Odette", u"Odile", u"Ombeline", u"Ondine", u"Ophélie", u"Orégane", u"Patrice", u"Paulette", u"Pauline", u"Philippine", u"Quitterie", u"Rachelle", u"Raymonde", u"Renée", u"Rochelle", u"Romaine", u"Romane", u"Rosalie", u"Rose", u"Rosine", u"Roxane", u"Sabine", u"Sabrine", u"Salome", u"Salomé", u"Sandrine", u"Sara", u"Séraphine", u"Sidonie", u"Simone", u"Simonne", u"Sixtine", u"Solange", u"Solène", u"Solenne", u"Sophie", u"Stéphanie", u"Suzanne", u"Sylvie", u"Thérèse", u"Tiphaine", u"Valentine", u"Valérie", u"Véronique", u"Victoire", u"Violette", u"Virgie", u"Virginie", u"Vivienne", u"Yannick", u"Yvette", u"Yvonne", u"Zoëu"]
  return random.choice(names)

def _getFrenchMaleName():
  names = [u"Achille", u"Adam", u"Adolphe", u"Adrien", u"Aïdan", u"Alain", u"Alain-René", u"Alban", u"Albert", u"Alexandre", u"Alexis", u"Aloïs", u"Alphonse", u"Amaury", u"Ambroise", u"Amédée", u"Anatole", u"André", u"Anicet", u"Anselme", u"Antoine", u"Aristide", u"Armand", u"Arnaud", u"Arsène", u"Arthur", u"Aubert", u"Aubin", u"Audefroy", u"Auguste", u"Augustin", u"Aurélien", u"Aymeric", u"Baptiste", u"Bardiou", u"Barthélémy", u"Basile", u"Bastien", u"Baudier", u"Baudouin", u"Beau", u"Benjamin", u"Benoît", u"Bérenger", u"Bernard", u"Bertrand", u"Blaise", u"Boudreaux", u"Brice", u"Brieux", u"Bruno", u"Cécil", u"Cédric", u"Cédrick", u"Céléstin", u"César", u"Charles", u"Charles-Antoine", u"Charles", u"Étienne", u"Chrétien", u"Christophe", u"Clair", u"Claude", u"Clément", u"Clovis", u"Côme", u"Constantin", u"Corentin", u"Cyprien", u"Cyriaque", u"Cyrille", u"Damien", u"Danick", u"Daniel", u"Dany", u"Dartagnan", u"David", u"Denis", u"Déreck", u"Didier", u"Dominique", u"Donatien", u"Edmond", u"Édouard", u"Égide", u"Élias", u"Élie", u"Éliot", u"Éloi", u"Émerick", u"Emeril", u"Émile", u"Émilien", u"Emmanuel", u"Enrick", u"Éric", u"Esmé", u"Étienne", u"Eugène", u"Evarist", u"Évrard", u"Fabien", u"Fabrice", u"Faust", u"Félix", u"Félix", u"Antoine", u"Fernand", u"Fidèle", u"Firmin", u"Flavien", u"Florent", u"Florian", u"Foudil", u"Franck", u"François", u"Frédéric", u"Frédérick", u"Gabin", u"Gabriel", u"Gaël", u"Gaétan/Gaëtan", u"Gaspard", u"Gaston", u"Gatien", u"Gauthier", u"Gautier", u"Gédéon", u"Geoffroy", u"George-Marie", u"Georges", u"Gérard", u"Germain", u"Ghislain", u"Gilbert", u"Giles", u"Gilles", u"Giraud", u"Grégoire", u"Guillaume", u"Gustave", u"Guy", u"Henri", u"Hercule", u"Hervé", u"Hilaire", u"Honoré", u"Hubert", u"Hugo", u"Hugues", u"Ignace", u"Irène", u"Isidore", u"Ismaël", u"Jacques", u"Jacquot", u"Jacques-Yves", u"Jean", u"Jean-Albert", u"Jean-André", u"Jean-Baptise", u"Jean-Christophe", u"Jean-Claude", u"Jean-Didier", u"Jean-France", u"Jean-François", u"Jean-Guy", u"Jean-Jacques", u"Jean-Jérôme", u"Jean-Lou", u"Jean-Louis", u"Jean-Luc", u"Jean-Marc", u"Jean-Marie", u"Jean-Michel", u"Jean-Paul", u"Jean-Philippe", u"Jean-Pierre", u"Jean-René", u"Jean-Sébastien", u"Jean-Simon", u"Jean-Xavier", u"Jean-Yves", u"Jérémi", u"Jérémie", u"Jérémy", u"Jermaine", u"Jérôme", u"Jessy", u"Joël", u"Joscelin", u"Joseph", u"Joseph-Benoît", u"Jourdain", u"Jules", u"Julien", u"Juste", u"Justin", u"Laurent", u"Lazare", u"Léandre", u"Léo", u"Léon", u"Léonard", u"Léopold", u"Lilian", u"Loïc", u"Lothaire", u"Lou", u"Louis", u"Louis-Charles", u"Louis-Joseph", u"Louis", u"Philippe", u"Louka", u"Luc", u"Lucas", u"Lucien", u"Ludovic", u"Macaire", u"Maël", u"Marc", u"Marc-Alexandre", u"Marc", u"André", u"Marc-André", u"Marc", u"Antoine", u"Marc-Antoine", u"Marcel", u"Marcellin", u"Marc-Henri", u"Marc", u"Olivier", u"Martial", u"Martin", u"Mathias", u"Mathieu", u"Mathis", u"Mattéo", u"Matthieu", u"Maurice", u"Maxence", u"Maxime", u"Maximilien", u"Michel", u"Mickaël", u"Mortimer", u"Narcisse", u"Nicéphore", u"Nicolas", u"Noé", u"Noël", u"Nordine", u"Octavien", u"Odilon", u"Olivier", u"Pascal", u"Patrice", u"Paul", u"Philippe", u"Pier-Olivier", u"Pierre", u"Pierrot", u"Pierre", u"Alexandre", u"Pierre-Luc", u"Pierre", u"Olivier", u"Pierrick", u"Quentin", u"Rafaël", u"Raoul", u"Raphaël", u"Rayan", u"Raymond", u"Réal", u"Régis", u"Réjean", u"Rémi", u"Rémy", u"Renald", u"Renaud", u"René", u"Richard", u"Robert", u"Rodolphe", u"Rodrigue", u"Roger", u"Roland", u"Romain", u"Romaine", u"Samuel", u"Samson", u"Samy", u"Sébastien", u"Serge", u"Séverin", u"Simeon", u"Simon", u"Olivier", u"Sofiane", u"Stanislas", u"Stefan-André", u"Stephan", u"Stéphane", u"Sulpice", u"Sylvain", u"Sylvestre", u"Tancrede", u"Terence", u"Théo", u"Théodore", u"Théophile", u"Thibaud", u"Thibault", u"Thibaut", u"Thierry", u"Thomas", u"Timothé", u"Timothée", u"Toussaint", u"Valentin", u"Valère", u"Venant", u"Victor", u"Vincent", u"Virgile", u"Voltaire", u"Xavier", u"Yan", u"Yanick", u"Yanis", u"Yoan", u"Yohan", u"Yves", u"Yvon", u"Zacharie", u"Zephrinu"] 
  return random.choice(names)

def _getFrenchRandomName():
  if random.choice([True, False]):
    return _getFrenchFemaleName()
  return _getFrenchMaleName()

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
    result = result.replace("$name", random.choice([_getDwarvenMaleName().capitalize(),
                                                   _getJapaneseRandomName().capitalize(),
                                                   _getFrenchRandomName().capitalize()]))
    return result
  return "The Great MacGuffin"
    
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
      Some generators distinguish male and female names - the input can 
      be the name of a valid style (e.g. 'dwarf' or 'French')
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
             "frenchmale":_getFrenchMaleName,
             "frenchfemale":_getFrenchFemaleName,
             "french":_getFrenchRandomName,
             "macguffin":_getMacguffinName,
             "proverb":_getProverb,
             "kaijyuu":_getKaleidoscope}
  if nametype == "keys":
    return typedic.keys()
  if nametype == 'kaikeys':
    return ['dwarfmale', 'japanesefull', 'french', 'weapon', 'eviltitle', 'macguffin']
  return typedic[nametype]()
