
import os
import json

from .toggle import Toggle
from .trigger import Trigger

ROOMS_DIRECTORY = "rooms"

class Room:
	def __init__(self, name):
		filename = os.path.join(ROOMS_DIRECTORY, name + ".json")
		with open(filename) as conf_file:
                        self._conf = json.load(conf_file)
                        self._toggles = [Toggle(t['name'], t['pin'], t['default']) for t in self._conf['toggles']]
                        self._triggers = [Trigger(t['name'], t['action'], t['target']) for t in self._conf['triggers']]

	@property
	def name(self):
		return self._conf['name']

	@property
	def cameras(self):
		return self._conf['cameras']
	
	@property
	def toggles(self):
		return self._toggles

	@property
	def triggers(self):
		return self._triggers

