import time
import atexit

PULSE_DURATION = 200
RECV_PULSE_DURATION = 200

enable = True
try:
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Broadcom numbering
    atexit.register(GPIO.cleanup)
except ImportError:
    print("Missing RPi.GPIO, simulating pin toggles")
    enable = False

# Wrapper for an individial GPIO pin (in or out)
class Pin:
    def __init__(self, number):
        self._number = number
        self._mode = None

    @property
    def number(self):
        return self._number

    @property
    def value(self):
        val = False
        if enable:
            try:
                if self._mode != GPIO.IN:
                    GPIO.setup(self._number, GPIO.IN)
                    self._mode == GPIO.IN
                val = GPIO.input(self._number)
            except RuntimeError:
                print("Unable to read GPIO pin {}".format(self._number))
        print("Pin {} has value {}".format(self._number, val))

    @value.setter
    def value(self, val):
        if enable:
            try:
                if self._mode != GPIO.OUT:
                    GPIO.setup(self._number, GPIO.OUT)
                    self._mode = GPIO.OUT
                GPIO.output(self._number, GPIO.HIGH if val else GPIO.LOW)
            except RuntimeError:
                print("Unable to set GPIO pin {}".format(self._number))
                return
        print("Pin {} set to {}".format(self._number, val))

    def clear(self):
        self.value = False

    def pulse(self):
        print("Sending pulse on pin {}".format(self._number))
        self.value = True
        time.sleep(PULSE_DURATION / 1000.0)
        self.value = False

    def listen(self, callback):
        def wrapped_callback(number):
            print("Detected a pulse on pin {}".format(number))
            callback()

        if enable:
            try:
                if self._mode != GPIO.IN:
                    GPIO.setup(self._number, GPIO.IN)
                GPIO.add_event_detect(
                    self._number,
                    GPIO.RISING,
                    callback=wrapped_callback,
                    bouncetime=int(RECV_PULSE_DURATION * 1.5),
                )
            except RuntimeError:
                print("Unable to read GPIO pin {}".format(self._number))
        print("Waiting for a pulse on pin {}".format(self._number))
