
class Trigger:
	def __init__(self, name, action, target):
		self._name = name
		self._action = action
		self._target = target

	@property
	def name(self):
		return self._name

	def to_dict(self):
		return { "name": self._name }

	def event(self):
		return { "action": self._action, "target": self._target }
