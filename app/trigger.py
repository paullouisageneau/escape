
class Trigger:
	def __init__(self, conf, events):
		self._name = conf['name']
		self._type = conf['type']
		self._data = conf['data']
		self._events = events

	@property
	def name(self):
		return self._name

	def pull(self):
		count = self._events.publish(self._type, self._data)
		return count > 0

	def to_dict(self):
		return { "name": self._name }
