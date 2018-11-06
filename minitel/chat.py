
import curses
import curses.ascii
import threading
import json

SENDER = 'Minitel'

class Message:
	def __init__(self, sender, text):
		self.sender = sender
		self.text = text
	
	def dump(self):
		m = { 'sender': self.sender, 'text': self.text }
		return json.dumps(m)
	
	@classmethod
	def parse(cls, data):
		m = json.loads(data)
		return Message(m['sender'], m['text']) if m else None

class Chat:
	def __init__(self, sendFunc):
		self.messages = []
		self._sendFunc = sendFunc
		self._condition = threading.Condition()
		self._input = ""
	
	def recv(self, data):
		message = Message.parse(data)
		if message:
			self._push(message)
	
	def send(self, text):
		message = Message(SENDER, text)
		self._sendFunc(message.dump())
	
	def clear(self):
		self.messages = []
	
	def _push(self, message):
		with self._condition:
			self.messages.append(message)
			self._condition.notify()
	
	def start(self):
		def input_loop(stdscr):
			while True:
				ch = stdscr.getch()
				with self._condition:
					if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
						if self._input:
							self.send(self._input)
							self._input = ""
					elif ch == curses.KEY_BACKSPACE or ch == curses.KEY_DC or ch == 127:
						if len(self._input) > 0:
							self._input = self._input[:-1]
					elif curses.ascii.isprint(ch):
						self._input+= chr(ch)
					self._condition.notify()
		
		def curses_main(stdscr):
			stdscr.clear()
			stdscr.refresh()
			sy, sx = stdscr.getmaxyx()
			win = curses.newwin(sy-1, sx, 0, 0)
			win.scrollok(True)
			win.idlok(True)
			input_win = curses.newwin(1, sx, sy-1, 0)
			
			input_thread = threading.Thread(target=input_loop, args=(stdscr,));
			input_thread.start()
			
			index = 0
			with self._condition:
				while True:
					changed = False
					while index < len(self.messages):
						message = self.messages[index]
						line = "{}: {}\n".format(message.sender, message.text)
						win.addstr(line)
						index+= 1
						changed = True
					if changed:
						win.refresh()
					if len(self._input) > sx-3:
						self._input = self._input[:sx-3]
						curses.beep()
					input_win.erase()
					input_win.addstr(0, 0, "> " + self._input)
					input_win.refresh()
					self._condition.wait()
		
		def curses_wrapper():
			curses.wrapper(curses_main)
		
		curses_thread = threading.Thread(target=curses_wrapper)
		curses_thread.start()

