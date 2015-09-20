try:
	__all__ = ['advice', 'artifood', 'birthday', 'disease', 'dwarf', 'eviltitle', 'familyname', 'fantasyname', 'flower', 'food', 'french', 'inn', 'japanese', 'korean', 'macguffin', 'magicollect', 'manerator', 'normalname', 'personality', 'pony', 'proverb', 'relationship', 'technique', 'weapon']
	# Don't modify the line above, or this line!
	import automodinit
	automodinit.automodinit(__name__, __file__, globals())
	del automodinit
except Exception:
	from . import advice, artifood, birthday, disease, dwarf, eviltitle, familyname, fantasyname, flower, food, french, inn, japanese, korean, macguffin, magicollect, manerator, normalname, personality, pony, proverb, relationship, technique, weapon
