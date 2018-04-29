
class Toggle:
	def __init__(self, name, pin, value):
		self.__name = name
		self.__pin = int(pin)
		self.__value = bool(value)
		self.update()

	@property
	def name(self):
		return self.__name

	@property
	def value(self):
		return self.__value

	@value.setter
	def value(self, newValue):
		self.__value = newValue
		self.update()

	def update(self):
		# TODO: Here, set the pin to high or low on RPi
		print("Pin {} toggled to {}".format(self.__pin, self.__value))

	def to_dict(self):
		return { "name": self.__name, "value": self.__value }
