
from .eventsource import EventSource
from .player import Player

EVENTS_PATH = '/api/events'

class Client:
	def __init__(self, url, media_path):
		self.url = url.rstrip('/')
		self.events = EventSource(self.url + EVENTS_PATH)
		self.player = Player(media_path)

	def run(self):
		print("Listening for video events...")
		for event in self.events:
			if event.event == 'video':
				if event.data:
					self.player.play(event.data)
				else:
					self.player.stop()
			elif event.event == 'reset':
				self.player.stop()

