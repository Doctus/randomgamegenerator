# -*- coding: utf-8 -*-
#
#rggNameGen - for the Random Game Generator project
#
#By Doctus (kirikayuumura.noir@gmail.com)
'''
    This file is part of RandomGameGenerator.

    RandomGameGenerator is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RandomGameGenerator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with RandomGameGenerator.  If not, see <http://www.gnu.org/licenses/>.
'''
from random import choice

GENERATOR_DIR = "generators"
KAIJYUUKEYS = ("technique", "dwarf", "japanese", "food", "weapon", "artifood", "french", "macguffin")

from . import generators

def getName(generator, args):
	'''Return a random name by passing generator args.'''
	if generator == "keys":
		return ", ".join(list(generators.keys()))
	elif generator == "help":
		if not args:
			return "Type '/generate help NAMETYPE' for more information on a specific generator. Available generators: " + ", ".join(list(generators.keys()))
		try:
			return generators[args]("help")
		except KeyError:
			return "Key Error: no generator named " + str(args) + ". For a list of available generators, see /generate keys."
	elif generator == "kaijyuu":
		result = []
		for x in range(0, choice((3, 4, 5))):
			result.append(getName(choice(KAIJYUUKEYS), "exalted full"))
		return " ".join(result)
	try:
		return getattr(generators, generator).getName(args)
	except KeyError:
		return "Key Error: no generator named " + str(generator) + ". For a list of available generators, see /generate keys."
