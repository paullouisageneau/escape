
class Game:
	def __init__(self, conf):
		self._name = conf['name']
		self._address = conf['address']
		self._initial = conf['initial']
		self._final = conf['final']
		self._count = conf['initial'][0]

	@property
	def name(self):
		return self._name

	@property
	def address(self):
		return self._address

	@property
	def initial(self):
		return self._initial

	@property
	def final(self):
		return self._final

	@property
	def execute(self):
		print('execute order')
		return self._final

	@property
	def next(self):
		return self._next

	def to_dict(self):
		return { "name": self._name}

