
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
		
		if 'input_pin' in conf:
			def callback():
				self.pull()
			self._input_pin = Pin(int(conf['input_pin']))
			self._input_pin.listen(callback)
		else:
			self._input_pin = None
		
		self._notify = 'notify' in conf and conf['notify']

	@property
	def name(self):
		return self._name

	@property
	def is_media(self):
		# return true if media only
		return self._pin is None

	def pull(self):
		success = False
		if self._pin:
			self._pin.pulse()
			success = True
		if self._event:
			success|= self._room.events.publish(self._event, self._data) > 0
		if self._notify:
			self._room.notify()
		return success

	def to_dict(self):
		return { "name": self._name }
