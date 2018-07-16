
import os
import subprocess

class Player:
	def __init__(self, media_path):
		self._media_path = media_path
	
	def play(self, path):
		location = path if '://' in path else os.path.join(self._media_path, path)
		
		print('Playing media at location: {}'.format(location))
		self._run(['omxplayer', '-b', '-o', 'hdmi', location])
		self._run(['xrefresh', '-display', ':0'])
	
	def _run(self, args):
		proc = subprocess.Popen(args)
		proc.wait()