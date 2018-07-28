
from gevent import sleep

from .gpio import Pin

ALT_PULSE_DURATION = 500

class Trigger:
	def __init__(self, conf, room):
		self._name = conf['name']
		self._room = room
		
		if 'event' in conf:
			self._event = conf['event']
			self._data = conf['data']
		else:
			self._event = None
			self._data = None

		if 'pin' in conf:
			self._pin = Pin(int(conf['pin']))
			self._pin.clear()
		else:
			self._pin = None
	
		if 'pin_alt' in conf:
			self._pin_alt = Pin(int(conf['pin_alt']))
			self._pin_alt.clear()
		else:
			self._pin_alt = None

		if 'input_pin' in conf:
			def callback():
				self.pull()
			self._input_pin = Pin(int(conf['input_pin']))
			self._input_pin.listen(callback)
		else:
			self._input_pin = None
		
		self._notify = 'notify' in conf and conf['notify']
		self._togglable = 'togglable' in conf and conf['togglable']
		self._toggle = False

	@property
	def name(self):
		return self._name

	@property
	def is_media(self):
		# return true if media only
		return self._pin is None

	def reset(self):
		self._toggle = False

	def pull(self):
		success = False
		if self._pin:
			if self._pin_alt:
				self._pin_alt.value = True
				self._pin.value = True
				sleep(ALT_PULSE_DURATION/1000.)
				self._pin_alt.value = False
				self._pin.value = False
			else:
				self._pin.pulse()
			success = True

		if self._event:
			success|= self._room.events.publish(self._event, self._data if not self._toggle else '') > 0
		if self._notify:
			self._room.notify()
		if self._togglable:
			self._toggle = not self._toggle
		return success

	def to_dict(self):
		return { "name": self._name }
