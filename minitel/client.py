
import json
import requests

from .eventsource import EventSource
from .chat import Chat

EVENTS_PATH = '/api/events'
POST_PATH = '/api/messages'

class Client:
	def __init__(self, url):
		self.url = url.rstrip('/')
		self.events = EventSource(self.url + EVENTS_PATH)
		self.chat = Chat(lambda data: self.send(data))
		self.chat.start()

	def send(self, data):
		headers = { 'Content-Type': 'application/json' }
		r = requests.post(self.url + POST_PATH, data = data, headers = headers)
		return r.ok

	def run(self):
		for event in self.events:
			if event.event == 'message':
				self.chat.recv(event.data)
			elif event.event == 'reset':
				self.chat.clear()

