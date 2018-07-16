
from .eventsource import EventSource
from .player import Player

EVENTS_PATH = '/api/events'

class Client:
	def __init__(self, url):
		self.url = url.rstrip('/')
		self.events = EventSource(self.url + EVENTS_PATH)
		self.player = Player(self.url)

	def run(self):
		for event in self.events:
			if event.event == 'video' or event.event == 'audio':
				url = event.data
				self.player.play(url)
