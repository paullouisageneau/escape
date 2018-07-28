
from gevent import sleep

from .gpio import Pin

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
			self._alt_pin = Pin(int(conf['pin_alt']))
			self._alt_pin.clear()
		else:
			self._alt_pin = None

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
		if self._alt_pin:
			self._alt_pin.value = True
			self._pin.value = True
			sleep(0.5)
			self._alt_pin.value = False
			self._pin.value = False
			success = True
		elif self._pin:
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
