
class Toggle:
	def __init__(self, name, pin, value):
		self._name = name
		self._pin = int(pin)
		self._value = bool(value)
		self.update()

	@property
	def name(self):
		return self._name

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, newValue):
		self._value = newValue
		self.update()

	def update(self):
		# TODO: Here, set the pin to high or low on RPi
		print("Pin {} toggled to {}".format(self._pin, self._value))

	def to_dict(self):
		return { "name": self._name, "value": self._value }

