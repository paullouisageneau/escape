
from .controller import Controller

class Camera:
	def __init__(self, conf):
		self._name = conf['name']
		
		if not 'stream' in conf:
			raise ValueError('Missing camera stream')
		self._stream = conf['stream']
		
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
