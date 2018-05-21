
import os
import json

from .event import EventStream
from .toggle import Toggle
from .trigger import Trigger
from .puzzle import Puzzle
from .game import Game

ROOMS_DIRECTORY = "rooms"

class Room:
	def __init__(self, name):
		filename = os.path.join(ROOMS_DIRECTORY, name + ".json")
		with open(filename) as conf_file:
			self._conf = json.load(conf_file)
		self.events = EventStream()
		self.toggles = [Toggle(c) for c in self._conf['toggles']]
		self.triggers = [Trigger(c, self.events) for c in self._conf['triggers']]
		self.puzzles = [Puzzle(c) for c in self._conf['puzzles']]
		if 'game' in self._conf.keys():		
			self.game = Game(self._conf['game'])

	@property
	def name(self):
		return self._conf['name']

	@property
	def cameras(self):
		return self._conf['cameras']

	@property
	def css_url(self):
		return self._conf.get('css_url', '')

	@property
	def chrono_offset(self):
		return int(self._conf.get('chrono_offset', 0))

	@property
	def chrono_reversed(self):
		return bool(self._conf.get('chrono_reversed', False))
