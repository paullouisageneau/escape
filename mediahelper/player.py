
import subprocess

class Player:
	def __init__(self, baseUrl):
		self._baseUrl = baseUrl
	
	def play(self, url):
		if not url:
			return
		if not '://' in url:
			url = self._baseUrl + (url if url[0] == '/' else '/' + url);
		
		print('Playing media at URL: {}'.format(url))
		self._run(['omxplayer', '-b', '-o', 'hdmi', url])
		self._run(['xrefresh', '-display', ':0'])
	
	def _run(self, args):
		proc = subprocess.Popen(args)
		proc.wait()
