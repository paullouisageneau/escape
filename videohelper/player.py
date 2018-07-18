
import subprocess
import time

AUDIO_DEV = 'local' # hdmi/local/both

class Player:
	def __init__(self, media_path):
		self._media_path = media_path.rstrip('/')
		self._proc = None
	
	def play(self, path):
		self.stop()
		if path:
			location = path if '://' in path else self._media_path + '/' + path.lstrip('/')
			print('Playing media at location: {}'.format(location))
			self._proc = subprocess.Popen(['omxplayer', '-b', '-o', AUDIO_DEV, location])
	
	def stop(self):
		if self._proc and self._proc.poll() is None:
			self._proc.terminate()
			self._proc.wait()
			time.sleep(1)
		self._proc = None
