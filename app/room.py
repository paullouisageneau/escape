
import os
import json

from .event import EventStream
from .toggle import Toggle
from .trigger import Trigger
from .puzzle import Puzzle

ROOMS_DIRECTORY = "rooms"

class Room:
	def __init__(self, name):
		filename = os.path.join(ROOMS_DIRECTORY, name + ".json")
		with open(filename, encoding='utf-8') as conf_file:
			conf = json.load(conf_file)
		self._conf = conf
		self.events = EventStream()
		
		self.toggles = [Toggle(c) for c in conf['toggles']] if 'toggles' in conf else []
		self.triggers = [Trigger(c, self.events) for c in conf['triggers']] if 'triggers' in conf else []
		self.puzzles = [Puzzle(c) for c in conf['puzzles']] if 'puzzles' in conf else []
		
		reset_conf = { 'name': 'reset', 'event': 'reset', 'data': '' }
		if 'reset_pin' in conf:
			reset_conf['pin'] = int(conf['reset_pin'])
		self.reset_trigger = Trigger(reset_conf, self.events)

	@property
	def name(self):
		return self._conf['name']

	@property
	def cameras(self):
		return self._conf['cameras'] if 'cameras' in self._conf else []
	
	@property
	def microphones(self):
		return self._conf['microphones'] if 'microphones' in self._conf else []

	@property
	def css_url(self):
		return self._conf.get('css_url', '')

	@property
	def chrono_offset(self):
		return int(self._conf.get('chrono_offset', 0))

	@property
	def chrono_reversed(self):
		return bool(self._conf.get('chrono_reversed', False))
	
	def reset(self):
		for toggle in self.toggles:
			toggle.reset()
		self.reset_trigger.pull()
