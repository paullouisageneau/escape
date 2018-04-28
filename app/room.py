
import os
import json

ROOMS_DIRECTORY = "rooms"

class Toggle:
	def __init__(self, name, value):
		self.name = name
		self.value = value

class Room:
	def __init__(self, name):
		filename = os.path.join(ROOMS_DIRECTORY, name + ".json")
		with open(filename) as conf_file:
			self.__conf = json.load(conf_file)
			self.__toggles = list(map(lambda t: Toggle(t['name'], t['default']), self.__conf['toggles']))

	@property
	def name(self):
		return self.__conf['name']

	@property
	def cameras(self):
		return self.__conf['cameras']
	
	@property
	def toggles(self):
		return self.__toggles
