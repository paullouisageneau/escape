
import os
import json

from .event import EventStream
from .toggle import Toggle
from .trigger import Trigger

ROOMS_DIRECTORY = "rooms"

class Room:
	def __init__(self, name):
		filename = os.path.join(ROOMS_DIRECTORY, name + ".json")
		with open(filename) as conf_file:
			self._conf = json.load(conf_file)

		self.event_stream = EventStream()
		self.toggles = [Toggle(c) for c in self._conf['toggles']]
		self.triggers = [Trigger(c, self.event_stream) for c in self._conf['triggers']]

	@property
	def name(self):
		return self._conf['name']

	@property
	def cameras(self):
		return self._conf['cameras']


