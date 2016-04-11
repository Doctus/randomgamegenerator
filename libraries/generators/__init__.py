__all__ = ['advice', 'artifood', 'birthday', 'denomination', 'disease', 'dwarf', 'eviltitle', 'familyname', 'fantasyname', 'flower', 'food', 'french', 'inn', 'japanese', 'korean', 'macguffin', 'magicollect', 'manerator', 'normalname', 'personality', 'pony', 'proverb', 'relationship', 'suddenly', 'technique', 'weapon']
# Don't modify the line above, or this line!
try:
	import automodinit
	automodinit.automodinit(__name__, __file__, globals())
	del automodinit
except Exception as e:
	#print(e)
	print("Could not load automodinit. (This is usually harmless except that new name generators will not be auto-detected.)")
	from . import advice, artifood, birthday, denomination, disease, dwarf, eviltitle, familyname, fantasyname, flower, food, french, inn, japanese, korean, macguffin, magicollect, manerator, normalname, personality, pony, proverb, relationship, suddenly, technique, weapon
