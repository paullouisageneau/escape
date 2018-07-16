
from .eventsource import EventSource
from .player import Player

EVENTS_PATH = '/api/events'

class Client:
	def __init__(self, url, media_path):
		self.url = url.rstrip('/')
		self.events = EventSource(self.url + EVENTS_PATH)
		self.player = Player(media_path)

	def run(self):
		for event in self.events:
			if event.event == 'video' or event.event == 'audio':
				self.player.play(event.data)
