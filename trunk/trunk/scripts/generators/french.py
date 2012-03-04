# -*- coding: utf-8 -*-

import random

fnames = [u"Adélaïde", u"Adèle", u"Adrienne", u"Agathe", u"Agnès", u"Aile", u"Aimée", u"Alaine", 
u"Albane", u"Alette", u"Alexandra", u"Alexanne", u"Alexis", u"Alice", u"Aline", u"Alix", u"Alizée", 
u"Amalie", u"Amandine", u"Ambre", u"Amée", u"Amélie", u"Anabelle", u"Anaëlle", u"Anaïs", u"Andréanne", 
u"Andrée", u"Andréa", u"Andrie", u"Ange", u"Angélique", u"Annabelle", u"Anne", u"Anne-Marie", u"Anne-Sophie", 
u"Annette", u"Annick", u"Annie", u"Antoinette", u"Appoline", u"Ariane", u"Arielle", u"Arlette", u"Armelle", 
u"Astérie", u"Aubine", u"Aurélie", u"Aurore", u"Avril", u"Axelle", u"Babette", u"Barbe", u"Béatrice", u"Belle", 
u"Bernadette", u"Bernice", u"Bertille", u"Bien", u"Aimée", u"Blaisotte", u"Blanche", u"Blanchette", u"Bluette", 
u"Brigitte", u"Calanthe", u"Camille", u"Capucine", u"Carolane", u"Carole", u"Caroline", u"Cassandre", u"Catherine", 
u"Cécilie", u"Celeste", u"Célia", u"Céline", u"Cerise", u"Chanel", u"Chantal", u"Charline", u"Charlotte", u"Charmaine", 
u"Cherie", u"Chloë", u"Christelle", u"Christiane", u"Christine", u"Claire", u"Claire-Marie", u"Clarisse", u"Claude", 
u"Claudette", u"Claudie", u"Claudine", u"Clémence", u"Clémentine", u"Clervie", u"Cloé", u"Clothilde", 
u"Clotilde", u"Colette", u"Coline", u"Colombe", u"Constance", u"Coralie", u"Cordélie", u"Corentine", u"Corinne", 
u"Cornélie", u"Cosette", u"Crescence", u"Danielle", u"Daphné", u"Daphnée", u"Delphine", u"Denise", u"Desirée", 
u"Dianne", u"Dionne", u"Dominique", u"Doralice", u"Doré", u"Dorette", u"Doriane", u"Dorothée", u"Drucilla", u"Égérie", 
u"Elaine", u"Éléanore", u"Eléna", u"Éliane", u"Élisabeth", u"Elise", u"Élizabeth", u"Élodie", u"Eloise", u"Emeline", 
u"Émilie", u"Émilienne", u"Emmanuelle", u"Emy", u"Ernestine", u"Esmé", u"Estée", u"Estelle", u"Eugénie", 
u"Eulalie", u"Evangeline", u"Eve", u"Evelyne", u"Fabienne", u"Fanette", u"Fanny", u"Fantine", u"Fernande", u"Fifi", 
u"Flamine", u"Fleur", u"Florence", u"Florie", u"Francine", u"Françoise", u"Frédérique", u"Gabrielle", u"Geneviève", 
u"Georgette", u"Georgine", u"Germaine", u"Gervaise", u"Ghislaine", u"Ginette", u"Gisèle", u"Grâce", u"Hélène", 
u"Héloïse", u"Henriette", u"Hermine", u"Hyacinthe", u"Inés", u"Irène", u"Iris", u"Isabeau", u"Isabelle", 
u"Jacqueline", u"Janine", u"Jeand'arc", u"Jeanette", u"Jeanine", u"Jeanne", u"Jeanne-Aimée", u"Jeanne-Yvette", 
u"Jeannine", u"Jenevieve", u"Joëlle", u"Josephine", u"Josette", u"Josiane", u"Julie", u"Juliette", u"Justine", 
u"Karine", u"Laetitia", u"Laure", u"Laurence", u"Lauriane", u"Laurianne", u"Laurie", u"Laurine", u"Léa", u"Léonie", 
u"Léonore", u"Liane", u"Lianne", u"Liliane", u"Lilianne", u"Lise", u"Lisette", u"Loraine", u"Loréline", u"Lorraine", 
u"Louise", u"Lucie", u"Lucienne", u"Lucile", u"Lucille", u"Lucrèce", u"Ludivine", u"Lydie", u"Mabelle", u"Madeleine", 
u"Maelle", u"Magalie", u"Manon", u"Marcelle", u"Margaux", u"Margot", u"Marguerite", u"Marianne", u"Marie", u"Marie-Anne", 
u"Marie-Claire", u"Marie-Claude", u"Marie-Ève", u"Marie-France", u"Marie-Hélène", u"Marie-Laure", u"Marielle", u"Marie-Louise", 
u"Marie-Noelle", u"Marie-Pier", u"Marie-Pierre", u"Marie-Sophie", u"Marie-Sylvie", u"Marie-Thérèse", u"Marine", u"Marion", 
u"Marjolaine", u"Marthe", u"Martine", u"Mathilde", u"Maude", u"Maxime", u"Maxine", u"Mégane", u"Mélaine", u"Mélanie", 
u"Mélina", u"Mélissa", u"Mélodie", u"Michèle", u"Micheline", u"Mignon", u"Mimi", u"Minerve", u"Mirabelle", u"Mireille", 
u"Monette", u"Monique", u"Morgane", u"Musette", u"Mylène", u"Myriam", u"Nadège", u"Nadine", u"Nanette", u"Natalie", u"Nathalie", 
u"Nicole", u"Nicolette", u"Noelle", u"Noemi", u"Noémie", u"Océane", u"Odette", u"Odile", u"Ombeline", u"Ondine", u"Ophélie", 
u"Orégane", u"Patrice", u"Paulette", u"Pauline", u"Philippine", u"Quitterie", u"Rachelle", u"Raymonde", u"Renée", u"Rochelle", 
u"Romaine", u"Romane", u"Rosalie", u"Rose", u"Rosine", u"Roxane", u"Sabine", u"Sabrine", u"Salome", u"Salomé", u"Sandrine", 
u"Sara", u"Séraphine", u"Sidonie", u"Simone", u"Simonne", u"Sixtine", u"Solange", u"Solène", u"Solenne", u"Sophie", u"Stéphanie", 
u"Suzanne", u"Sylvie", u"Thérèse", u"Tiphaine", u"Valentine", u"Valérie", u"Véronique", u"Victoire", u"Violette", u"Virgie", 
u"Virginie", u"Vivienne", u"Yannick", u"Yvette", u"Yvonne", u"Zoëu"]
mnames = [u"Achille", u"Adam", u"Adolphe", u"Adrien", u"Aïdan", u"Alain", u"Alain-René", u"Alban", u"Albert", u"Alexandre", 
u"Alexis", u"Aloïs", u"Alphonse", u"Amaury", u"Ambroise", u"Amédée", u"Anatole", u"André", u"Anicet", u"Anselme", u"Antoine", 
u"Aristide", u"Armand", u"Arnaud", u"Arsène", u"Arthur", u"Aubert", u"Aubin", u"Audefroy", u"Auguste", u"Augustin", u"Aurélien", 
u"Aymeric", u"Baptiste", u"Bardiou", u"Barthélémy", u"Basile", u"Bastien", u"Baudier", u"Baudouin", u"Beau", u"Benjamin", 
u"Benoît", u"Bérenger", u"Bernard", u"Bertrand", u"Blaise", u"Boudreaux", u"Brice", u"Brieux", u"Bruno", u"Cécil", u"Cédric", 
u"Cédrick", u"Céléstin", u"César", u"Charles", u"Charles-Antoine", u"Charles", u"Étienne", u"Chrétien", u"Christophe", u"Clair", 
u"Claude", u"Clément", u"Clovis", u"Côme", u"Constantin", u"Corentin", u"Cyprien", u"Cyriaque", u"Cyrille", u"Damien", u"Danick", 
u"Daniel", u"Dany", u"Dartagnan", u"David", u"Denis", u"Déreck", u"Didier", u"Dominique", u"Donatien", u"Edmond", u"Édouard", 
u"Égide", u"Élias", u"Élie", u"Éliot", u"Éloi", u"Émerick", u"Emeril", u"Émile", u"Émilien", u"Emmanuel", u"Enrick", u"Éric", 
u"Esmé", u"Étienne", u"Eugène", u"Evarist", u"Évrard", u"Fabien", u"Fabrice", u"Faust", u"Félix", u"Félix", u"Antoine", u"Fernand", 
u"Fidèle", u"Firmin", u"Flavien", u"Florent", u"Florian", u"Foudil", u"Franck", u"François", u"Frédéric", u"Frédérick", u"Gabin", 
u"Gabriel", u"Gaël", u"Gaétan/Gaëtan", u"Gaspard", u"Gaston", u"Gatien", u"Gauthier", u"Gautier", u"Gédéon", u"Geoffroy", u"George-Marie", 
u"Georges", u"Gérard", u"Germain", u"Ghislain", u"Gilbert", u"Giles", u"Gilles", u"Giraud", u"Grégoire", u"Guillaume", u"Gustave", 
u"Guy", u"Henri", u"Hercule", u"Hervé", u"Hilaire", u"Honoré", u"Hubert", u"Hugo", u"Hugues", u"Ignace", u"Irène", u"Isidore", u"Ismaël", 
u"Jacques", u"Jacquot", u"Jacques-Yves", u"Jean", u"Jean-Albert", u"Jean-André", u"Jean-Baptise", u"Jean-Christophe", u"Jean-Claude", 
u"Jean-Didier", u"Jean-France", u"Jean-François", u"Jean-Guy", u"Jean-Jacques", u"Jean-Jérôme", u"Jean-Lou", u"Jean-Louis", u"Jean-Luc", 
u"Jean-Marc", u"Jean-Marie", u"Jean-Michel", u"Jean-Paul", u"Jean-Philippe", u"Jean-Pierre", u"Jean-René", u"Jean-Sébastien", u"Jean-Simon", 
u"Jean-Xavier", u"Jean-Yves", u"Jérémi", u"Jérémie", u"Jérémy", u"Jermaine", u"Jérôme", u"Jessy", u"Joël", u"Joscelin", u"Joseph", 
u"Joseph-Benoît", u"Jourdain", u"Jules", u"Julien", u"Juste", u"Justin", u"Laurent", u"Lazare", u"Léandre", u"Léo", u"Léon", u"Léonard", 
u"Léopold", u"Lilian", u"Loïc", u"Lothaire", u"Lou", u"Louis", u"Louis-Charles", u"Louis-Joseph", u"Louis", u"Philippe", u"Louka", u"Luc", 
u"Lucas", u"Lucien", u"Ludovic", u"Macaire", u"Maël", u"Marc", u"Marc-Alexandre", u"Marc", u"André", u"Marc-André", u"Marc", u"Antoine", 
u"Marc-Antoine", u"Marcel", u"Marcellin", u"Marc-Henri", u"Marc", u"Olivier", u"Martial", u"Martin", u"Mathias", u"Mathieu", u"Mathis", 
u"Mattéo", u"Matthieu", u"Maurice", u"Maxence", u"Maxime", u"Maximilien", u"Michel", u"Mickaël", u"Mortimer", u"Narcisse", u"Nicéphore", 
u"Nicolas", u"Noé", u"Noël", u"Nordine", u"Octavien", u"Odilon", u"Olivier", u"Pascal", u"Patrice", u"Paul", u"Philippe", u"Pier-Olivier", 
u"Pierre", u"Pierrot", u"Pierre", u"Alexandre", u"Pierre-Luc", u"Pierre", u"Olivier", u"Pierrick", u"Quentin", u"Rafaël", u"Raoul", u"Raphaël", 
u"Rayan", u"Raymond", u"Réal", u"Régis", u"Réjean", u"Rémi", u"Rémy", u"Renald", u"Renaud", u"René", u"Richard", u"Robert", u"Rodolphe", 
u"Rodrigue", u"Roger", u"Roland", u"Romain", u"Romaine", u"Samuel", u"Samson", u"Samy", u"Sébastien", u"Serge", u"Séverin", u"Simeon", u"Simon", 
u"Olivier", u"Sofiane", u"Stanislas", u"Stefan-André", u"Stephan", u"Stéphane", u"Sulpice", u"Sylvain", u"Sylvestre", u"Tancrede", u"Terence", 
u"Théo", u"Théodore", u"Théophile", u"Thibaud", u"Thibault", u"Thibaut", u"Thierry", u"Thomas", u"Timothé", u"Timothée", u"Toussaint", u"Valentin", 
u"Valère", u"Venant", u"Victor", u"Vincent", u"Virgile", u"Voltaire", u"Xavier", u"Yan", u"Yanick", u"Yanis", u"Yoan", u"Yohan", u"Yves", u"Yvon", 
u"Zacharie", u"Zephrinu"] 

def _getFrenchFemaleName():
  return random.choice(fnames)

def _getFrenchMaleName():
  return random.choice(mnames)

def _getFrenchRandomName():
  if random.choice([True, False]):
    return _getFrenchFemaleName()
  return _getFrenchMaleName()
  
def getName(args):
    if "female" in args:
        return _getFrenchFemaleName()
    elif "male" in args:
        return _getFrenchMaleName()
    return _getFrenchRandomName()
