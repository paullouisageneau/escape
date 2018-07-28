
from gevent import spawn, sleep
from gevent.queue import Queue

RETRY = 1000
KEEPALIVE_INTERVAL = 10000

class EventStream:
	def __init__(self):
		self._subscriptions = []
		def keepalive():
			while True:
				sleep(KEEPALIVE_INTERVAL/1000.)
				self.publish('keepalive', '')
		spawn(keepalive)

	def publish(self, event, data):
		if self._subscriptions:
			def notify():
				for s in self._subscriptions:
					s.put((event, data))
			spawn(notify)
			sleep(0) # yield
		return len(self._subscriptions)

	def subscribe(self):
		q = Queue()
		self._subscriptions.append(q)
		try:
			yield "retry: {}\n\n".format(RETRY)
			while True:
				event, data = q.get()
				yield "event: {}\ndata: {}\n\n".format(event, data)
		except GeneratorExit:
			self._subscriptions.remove(q)
