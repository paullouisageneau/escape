
import curses
import curses.ascii
import threading
import _thread
import json

class Message:
	def __init__(self, sender, text):
		self.sender = sender
		self.text = text
	
	def dump(self):
		m = { 'sender': self.sender, 'text': self.text }
		return json.dumps(m)
	
	@classmethod
	def parse(cls, data):
		m = json.loads(data) if isinstance(data, str) else data
		return Message(m['sender'], m['text']) if m else None

class Chat:
	def __init__(self, username, send_func):
		self.messages = []
		self._username = username
		self._send_func = send_func
		self._condition = threading.Condition()
		self._curses_thread = None
		self._stopped = False
		self._input = ""
	
	def recv(self, data):
		message = Message.parse(data)
		if message:
			self._push(message)
			return True
		return False
	
	def send(self, text):
		message = Message(self._username, text)
		return self._send_func(message.dump())
	
	def clear(self):
		with self._condition:
			self.messages = []
			self._input = ""
			self._condition.notify()
	
	def _push(self, message):
		with self._condition:
			self.messages.append(message)
			self._condition.notify()
	
	def start(self):
		def input_loop(stdscr):
			try:
				while True:
					ch = stdscr.getch()
					with self._condition:
						if ch in (curses.KEY_ENTER, 10, 13):
							if self._input:
								if not self.send(self._input):
									curses.beep()
								self._input = ""
						elif ch in (curses.KEY_BACKSPACE, curses.KEY_DC, 127):
							if len(self._input) > 0:
								self._input = self._input[:-1]
						elif curses.ascii.isprint(ch):
							self._input+= chr(ch)
						self._condition.notify()
			except KeyboardInterrupt:
				_thread.interrupt_main()
			except Exception as e:
				print(e)
				_thread.interrupt_main()
		
		def curses_main(stdscr):
			stdscr.clear()
			stdscr.refresh()
			sy, sx = stdscr.getmaxyx()
			win = curses.newwin(sy-1, sx, 0, 0)
			win.scrollok(True)
			win.idlok(True)
			input_win = curses.newwin(1, sx, sy-1, 0)
			
			input_thread = threading.Thread(target=input_loop, args=(stdscr,));
			input_thread.daemon = True
			input_thread.start()
			
			index = 0
			with self._condition:
				while not self._stopped:
					if index > len(self.messages):
						win.clear()
						index = 0
					has_new = False
					while index < len(self.messages):
						message = self.messages[index]
						line = "{}: {}\n".format(message.sender, message.text)
						win.addstr(line)
						if message.sender != self._username:
							has_new = True
						index+= 1
					if has_new:
						curses.beep()
					win.refresh()
					if len(self._input) > sx-3:
						self._input = self._input[:sx-3]
						curses.beep()
					input_win.erase()
					input_win.addstr(0, 0, "> " + self._input)
					input_win.refresh()
					self._condition.wait()
		
		def curses_wrapper():
			try:
				curses.wrapper(curses_main)
			except KeyboardInterrupt:
				_thread.interrupt_main()
			except Exception as e:
				print(e)
				_thread.interrupt_main()
		
		self._stopped = False
		self._curses_thread = threading.Thread(target=curses_wrapper)
		self._curses_thread.start()
		
	def stop(self):
		if self._curses_thread:
			with self._condition:
				self._stopped = True
				self._condition.notifyAll()
			self._curses_thread.join()
			self._curses_thread = None
		
