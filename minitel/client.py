import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .eventsource import EventSource
from .chat import Chat

EVENTS_PATH = "/api/events"
MESSAGES_PATH = "/api/messages"
RETRY_DELAY = 1
MAX_BACKLOG = 22
MSG_CONNECTING = "Connexion..."
MSG_CLOSING = "Fin."


class ClientRetry(Retry):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def sleep(response=None):
        time.sleep(RETRY_DELAY)


class Client:
    def __init__(self, url, username):
        self.url = url.rstrip("/")
        self.chat = Chat(username, lambda data: self.send(data))

    def send(self, data):
        headers = {"Content-Type": "application/json"}
        r = requests.post(self.url + MESSAGES_PATH, data=data, headers=headers)
        return r.ok

    def _populate(self):
        with requests.Session() as session:
            retries = ClientRetry(total=3600, status_forcelist=(500, 502, 503, 504))
            session.mount("http://", HTTPAdapter(max_retries=retries))
            session.mount("https://", HTTPAdapter(max_retries=retries))
            r = session.get(self.url + MESSAGES_PATH)
            r.raise_for_status()
            messages = r.json()
            for m in messages[-MAX_BACKLOG:]:
                self.chat.recv(m)

    def run(self):
        print(MSG_CONNECTING)
        self._populate()
        events = EventSource(self.url + EVENTS_PATH)
        self.chat.start()
        try:
            for event in events:
                if event.event == "message":
                    self.chat.recv(event.data)
                elif event.event == "reset":
                    self.chat.clear()
        finally:
            self.chat.stop()
            print(MSG_CLOSING)
