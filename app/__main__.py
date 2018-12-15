
import sys

from gevent.pywsgi import WSGIServer

from . import app

port = 8080

def main():
	try:
		# Run the webapp on specified port
		print("Listening on port {}".format(port))
		http_server = WSGIServer(("0.0.0.0", port), app)
		http_server.serve_forever()
	except KeyboardInterrupt:
		return 0

	return 1

if __name__ == "__main__":
	sys.exit(main())
