
class Game:
	def __init__(self, conf):
		self._name = conf['name']
		self._address = conf['address']
		self._nbPlayers = 5
		self._initial = conf['initial'][self._nbPlayers-3]
		self._final = self._nbPlayers
		# self._count = conf['initial'][0]
		self._casualties = -1
		self._actions = list(conf['actions'].keys())
		self._effects = conf['actions']
		self._nbActions = len(self._actions)
		self._actionIndices = dict(zip(self._actions,list(range(self._nbActions))))
		aux = self._nbActions*[False]
		self._gameState = dict(zip(self._actions,aux))
		# self._gameState = aux
		self.compute_casualties()
		self._victory = False

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

	def compute_casualties(self):
		countdown = self._initial
		for (action,state) in self._gameState.items():
			if state: countdown += self._effects[action]
		self._casualties = countdown
		self._victory = (self._casualties==self._final)
		return

	def execute(self,action):		
		if not self._gameState[action]:
			effect = self._effects[action]
			self._casualties += effect
			self._gameState[action] = True
		self._victory = (self._casualties==self._final)
		return

	def abort(self,action):
		if self._gameState[action]:
			effect = self._effects[action]
			self._casualties -= effect
			self._gameState[action] = False
		self._victory = (self._casualties==self._final)
		return

	@property
	def next(self):
		return self._next

	def to_dict(self):
		return { "name": self._name}

