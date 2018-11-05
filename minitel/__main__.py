
import sys

from .chat import Chat
from .client import Client

def main():
	try:
		if len(sys.argv) < 2:
			print("Usage: {} URL".format(sys.argv[0]))
			return 1
		
		url = sys.argv[1]
		client = Client(url)
		client.run()
		
	except KeyboardInterrupt:
		return 0

	return 1

if __name__ == "__main__":
	sys.exit(main())
