from .gpio import Pin


class Toggle:
    def __init__(self, conf):
        if "name" not in conf:
            raise KeyError("No name specified for toggle")

        self._name = conf["name"]
        if type(self._name) != str or len(self._name) == 0:
            raise TypeError("Invalid name for toggle")

        self._hidden = "hidden" in conf and conf["hidden"]

        if "pin" not in conf:
            raise KeyError('No pin specified for toggle "{}"'.format(self._name))

        self._pin = Pin(int(conf["pin"]))
        self._default = bool(conf["default"] if "default" in conf else False)
        self._value = self._default
        self.update()

    @property
    def name(self):
        return self._name

    @property
    def hidden(self):
        return self._hidden

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
        self._pin.value = self._value

    def to_dict(self):
        return {"name": self.name, "value": self.value}
