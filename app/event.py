
import json

from gevent import spawn
from gevent.queue import Queue

class EventStream:
    def __init__(self):
        self._subscriptions = []

    def publish(self, event):
        def notify():
            for s in self._subscriptions:
                s.put(event)
        spawn(notify)
        return len(self._subscriptions)

    def subscribe(self):
        q = Queue()
        self._subscriptions.append(q)
        try:
            while True:
                event = q.get()
                yield "data: {}\n\n".format(json.dumps(event))
        except GeneratorExit:
            self._subscriptions.remove(q)

