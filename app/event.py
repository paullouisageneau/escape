
import json

from gevent import spawn
from gevent.queue import Queue

class EventStream:
    def __init__(self):
        self._subscriptions = []

    def publish(self, event, data):
        def notify():
            for s in self._subscriptions:
                s.put((event, data))
        spawn(notify)
        return len(self._subscriptions)

    def subscribe(self):
        q = Queue()
        self._subscriptions.append(q)
        try:
            while True:
                event, data = q.get()
                yield "event: {}\ndata: {}\n\n".format(event, data)
        except GeneratorExit:
            self._subscriptions.remove(q)

