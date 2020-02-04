import sys

from .chat import Chat
from .client import Client


def main():
    try:
        if len(sys.argv) < 2 or len(sys.argv) > 3:
            print("Usage: {} URL [username]".format(sys.argv[0]))
            return 1
        url = sys.argv[1]
        username = sys.argv[2] if len(sys.argv) >= 3 else "Minitel"
        client = Client(url, username)
        client.run()
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(e)

    return 1


if __name__ == "__main__":
    sys.exit(main())
