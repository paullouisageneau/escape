
from .controller import Controller

class Camera:
	def __init__(self, conf):
		self._name = conf['name']
		
		if not 'stream' in conf:
			raise ValueError('Missing camera stream')
		self._stream = conf['stream']
		
		self._is_reversed = conf.get('reversed', False) == True
		
		if 'controller' in conf:
			self.controller = Controller(conf['controller'])
		else :
			self.controller = None
	
	@property
	def name(self):
		return self._name

	@property
	def stream(self):
		return self._stream
	
	@property
	def is_reversed(self):
		return self._is_reversed
