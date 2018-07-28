
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
		self.triggers = [Trigger(c, self) for c in conf['triggers']] if 'triggers' in conf else []
		self.puzzles = [Puzzle(c) for c in conf['puzzles']] if 'puzzles' in conf else []
		
		reset_conf = { 'name': 'reset', 'event': 'reset', 'data': '' }
		if 'reset_pin' in conf:
			reset_conf['pin'] = int(conf['reset_pin'])
			if 'reset_pin_alt' in conf:
				reset_conf['pin_alt'] = int(conf['reset_pin_alt'])
		self.reset_trigger = Trigger(reset_conf, self)
		
		if 'notification_audio_url' in conf:
			notify_conf = { 'name': 'notify', 'event': 'audio', 'data': conf['notification_audio_url'] }
			self.notify_trigger = Trigger(notify_conf, self)
		else:
			self.notify_trigger = None

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
	def style_url(self):
		return self._conf.get('style_url', '')

	@property
	def chrono_offset(self):
		return int(self._conf.get('chrono_offset', 0))

	@property
	def chrono_reversed(self):
		return bool(self._conf.get('chrono_reversed', False))
	
	@property
	def media_triggers_indexes(self):
		return [i for i in range(len(self.triggers)) if self.triggers[i].is_media]
	
	def reset(self):
		for toggle in self.toggles:
			toggle.reset()
		for trigger in self.triggers:
			trigger.reset()
		self.reset_trigger.pull()
		
	def notify(self):
		if self.notify_trigger:
			self.notify_trigger.pull()

