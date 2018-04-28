
import sys
import gevent.wsgi

from . import app

port = 8080

def main():
	try:
		# Run the webapp on specified port
		http_server = gevent.wsgi.WSGIServer(("127.0.0.1", port), app)
		http_server.serve_forever()
	except KeyboardInterrupt:
		return 0

	return 1

if __name__ == "__main__":
	sys.exit(main())
