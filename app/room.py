
import os
import json

from .toggle import Toggle

ROOMS_DIRECTORY = "rooms"

class Room:
	def __init__(self, name):
		filename = os.path.join(ROOMS_DIRECTORY, name + ".json")
		with open(filename) as conf_file:
			self.__conf = json.load(conf_file)
			self.__toggles = [Toggle(t['name'], t['pin'], t['default']) for t in self.__conf['toggles']]

	@property
	def name(self):
		return self.__conf['name']

	@property
	def cameras(self):
		return self.__conf['cameras']
	
	@property
	def toggles(self):
		return self.__toggles

