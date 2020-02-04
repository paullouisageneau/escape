import sys

from .client import Client


def main():
    try:
        if len(sys.argv) < 3:
            print("Usage: {} URL MEDIA_PATH".format(sys.argv[0]))
            return 1

        url = sys.argv[1]
        media_path = sys.argv[2]
        client = Client(url, media_path)
        client.run()

    except KeyboardInterrupt:
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
