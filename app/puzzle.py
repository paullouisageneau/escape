
class Puzzle:
	def __init__(self, conf):
		self._name = conf['name']
		self._id = int(conf['id'])
		self._next = int(conf['next'])

	@property
	def name(self):
		return self._name

	@property
	def id(self):
		return self._id

	@property
	def next(self):
		return self._next

	def to_dict(self):
		return { "name": self._name, "id": self._id, "next": self._next }

