
class Microphone:
	def __init__(self, conf):
		self._name = conf['name']
		
		if 'stream' not in conf:
			raise ValueError('Missing microphone stream')
		self._stream = conf['stream']
	
	@property
	def name(self):
		return self._name

	@property
	def stream(self):
		return self._stream
