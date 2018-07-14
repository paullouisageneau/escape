
from .gpio import Pin

class Trigger:
	def __init__(self, conf, events):
		self._name = conf['name']
		self._events = events
		
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
			self._input_pin = Pin(int(conf['input_pin']))
			self._input_pin.listen(self.pull)
		else:
			self._input_pin = None

	@property
	def name(self):
		return self._name

	def pull(self):
		success = False
		if self._pin:
			self._pin.pulse()
			success = True
		if self._event:
			success|= self._events.publish(self._event, self._data) > 0
		return success

	def to_dict(self):
		return { "name": self._name }
