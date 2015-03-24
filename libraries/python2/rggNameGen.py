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

import random, os

GENERATOR_DIR = "generators"
KAIJYUUKEYS = ("technique", "dwarf", "japanese", "food", "weapon", "artifood", "french", "macguffin")

generators = {}
try:
	for file in os.listdir(GENERATOR_DIR):
		if ".py" in file and "__init__" not in file and ".pyc" not in file:
			#This is kind of bad, but since we have to use the "from generators"
			#syntax I don't know a cleaner way to do this.
			exec("from generators import "+file[:-3])
			exec("generators[file[:-3]] = "+file[:-3]+".getName")
except Exception as e:
	pass

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
		for x in range(0, random.choice((3, 4, 5))):
			result.append(getName(random.choice(KAIJYUUKEYS), "exalted full"))
		return " ".join(result)
	try:
		return generators[generator](args)
	except KeyError:
		return "Key Error: no generator named " + str(generator) + ". For a list of available generators, see /generate keys."
