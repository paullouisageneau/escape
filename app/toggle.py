
import atexit

enable = True
try:
	import RPi.GPIO as GPIO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM) # Broadcom numbering
	atexit.register(GPIO.cleanup)
except ImportError:
	print("Missing RPi.GPIO, simulating pin toggles")
	enable = False

class Toggle:
	def __init__(self, conf):
		self._name = conf['name']
		self._pin = int(conf['pin'])
		self._default = bool(conf['default'])
		self._value = self._default
		if enable:
			try:
				GPIO.setup(self._pin, GPIO.OUT) # Set output
			except RuntimeError:
				print("Unable to access GPIO pin {}".format(self._pin))
		self.update()

	@property
	def name(self):
		return self._name

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, newValue):
		if self._value != newValue:
			self._value = newValue
			self.update()

	def change(self):
		self.value = not self.value

	def reset(self):
		self.value = self._default

	def update(self):
		if enable:
			try:
				GPIO.output(self._pin, GPIO.HIGH if self._value else GPIO.LOW)
			except RuntimeError:
				print("Unable to toggle GPIO pin {}".format(self._pin))
				return
		print("Pin {} toggled to {}".format(self._pin, self._value))

	def to_dict(self):
		return { "name": self._name, "value": self._value }

