import requests
import time

from requests import RequestException

# Simple SSE client


class Event:
    def __init__(self, raw):
        self.event = None
        self.id = None
        self.retry = None
        self.data = None

        # Parse event line by line
        for line in raw.splitlines():
            if not line:
                continue
            [name, value] = line.split(":", 1) if ":" in line else [line, ""]
            if value.startswith(" "):
                value = value[1:]

            if name == "event":
                self.event = value
            elif name == "id":
                self.id = value
            elif name == "retry":
                self.retry = int(value)
            elif name == "data":
                if self.data:
                    self.data += "\n" + value
                else:
                    self.data = value


class EventSource:
    def __init__(self, url, *, session=None, last_id=None, retry=3000):
        self.url = url
        self.session = session
        self.last_id = None
        self.retry = retry

        self._connect()

    def _connect(self):
        headers = {"Cache-Control": "no-cache", "Accept": "text/event-stream"}  # per SSE spec

        if self.last_id:
            headers["Last-Event-ID"] = self.last_id

        # Use session if set
        requester = self.session or requests
        self.response = requester.get(self.url, stream=True, headers=headers)
        self.response.raise_for_status()
        self.response_iter = self.response.iter_lines()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            raw_event = ""
            for line in self.response_iter:
                encoding = self.response.encoding if self.response.encoding else "utf-8"
                line = line.decode(encoding, errors="ignore")
                if line:
                    raw_event += line + "\n"
                else:
                    # Dispatch event on empty line
                    event = Event(raw_event)
                    if event.id:
                        self.last_id = event.id
                    if event.retry:
                        self.retry = event.retry
                    if event.data is not None:
                        return event

            time.sleep(self.retry / 1000.0)
            self._connect()
