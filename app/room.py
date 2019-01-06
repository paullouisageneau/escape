
import os
import json
import time

from .event import EventStream
from .toggle import Toggle
from .trigger import Trigger
from .camera import Camera
from .microphone import Microphone
from .puzzle import Puzzle

ROOMS_DIRECTORY = "rooms"

class Room:
	def __init__(self, name):
		filename = os.path.join(ROOMS_DIRECTORY, name + ".json")
		with open(filename, encoding='utf-8') as conf_file:
			conf = json.load(conf_file)
		self._conf = conf
		self.events = EventStream()
		
		self.toggles = [Toggle(c) for c in conf.get('toggles', [])]
		self.triggers = [Trigger(c, self) for c in conf.get('triggers', [])]
		self.cameras = [Camera(c) for c in conf.get('cameras', [])]
		self.microphones = [Microphone(c) for c in conf.get('microphones', [])]

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
		
		self.start_time = 0 # If chrono was started, contains the timestamp
		self.stop_time = 0  # If chrono was stopped, contains the timestamp
		
		self.clues = []        # List of sent clues
		self.current_clue = '' # Current displayed clue
		
		self.messages = []     # List of messages
		
		self._playlist_started = False

	@property
	def name(self):
		return self._conf['name']

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
	def messages_enabled(self):
		return bool(self._conf.get('messages_enabled', False))
	
	@property
	def messages_sender(self):
		return self._conf.get('messages_sender', '')
	
	@property
	def media_triggers_indexes(self):
		return [i for i in range(len(self.triggers)) if self.triggers[i].is_media]
	
	def subscribe(self):
		event_stream = self.events.subscribe()
		return event_stream
	
	def start_chrono(self):
		self.set_chrono(min(self.start_time + (time.time() - self.stop_time), time.time()), 0)
	
	def stop_chrono(self):
		self.set_chrono(self.start_time, time.time())
	
	def set_chrono(self, start_time, stop_time):
		if start_time != self.start_time or stop_time != self.stop_time:
			self.start_time = start_time
			self.stop_time = stop_time
			self.update_chrono()
			self.update_chrono_media()
	
	def update_chrono(self):
		self.events.publish('chrono', json.dumps({ 'start': self.start_time, 'stop': self.stop_time }))
		
	def update_chrono_media(self):
		if 'playlist_url' in self._conf:
			if self.start_time > 0 and self.stop_time == 0 and not self._playlist_started:
				audio_url = self._conf['playlist_url']
				self.events.publish('background_audio', audio_url)
				self._playlist_started = True
		if 'chrono_video_url' in self._conf:
			if self.stop_time > 0 or self.current_clue:
				self.events.publish('video', '')
			elif self.start_time > 0:
				video_url = self._conf['chrono_video_url']
				offset = self._conf.get('chrono_video_offset', 0)
				delta = int(max(time.time() - self.start_time, 0) + offset)
				self.events.publish('video', '{}#t={}'.format(video_url, delta))
	
	def set_clue(self, clue):
		if self.current_clue != clue:
			self.current_clue = clue
			if clue:
				self.clues.append(clue)
			self.update_clue()
			self.update_chrono_media()
	
	def update_clue(self):
		self.events.publish('clue', json.dumps({ 'text': self.current_clue }))
	
	def handle_message(self, message):
		self.messages.append(message)
		self.events.publish('message', json.dumps(message))
	
	def reset(self):
		self.set_clue('');
		self.set_chrono(0, 0);
		self.clues = []
		self.messages = []
		self._playlist_started = False
		for toggle in self.toggles:
			toggle.reset()
		for trigger in self.triggers:
			trigger.reset()
		self.reset_trigger.pull()
		# Personalized chat prompt
		self.handle_message({ 'sender': "Green", 'text': "Tenez-moi au courant de l'enquête ici." })
		self.handle_message({ 'sender': "Green", 'text': "Dites-moi si vous avez un suspect."})
		
	def notify(self):
		if self.notify_trigger:
			return self.notify_trigger.pull()
		else:
			return False

