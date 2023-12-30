import sys

from gevent.pywsgi import WSGIServer

from . import app

port = 8080


def main():
    try:
        # Run the webapp on specified port
        print("Listening on http://127.0.0.1:{}/".format(port))
        http_server = WSGIServer(("127.0.0.1", port), app)
        http_server.serve_forever()
    except KeyboardInterrupt:
        return 0

    return 1


sys.exit(main())
