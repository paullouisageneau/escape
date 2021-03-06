import subprocess
from urllib.parse import parse_qs

AUDIO_DEV = "local"  # hdmi/local/both
MEDIA_PREFIX = "media/"


class Player:
    def __init__(self, media_path):
        self._media_path = media_path.rstrip("/")
        self._proc = None

    def play(self, path):
        self.stop()
        if "://" not in path:
            path = path.lstrip("/")
            path = path[len(MEDIA_PREFIX) :] if path.startswith(MEDIA_PREFIX) else path
            path = self._media_path + "/" + path

        startTime = 0
        if "#" in path:
            path, hashString = path.split("#", 1)
            hashParams = parse_qs(hashString)
            if "t" in hashParams:
                startTime = int(hashParams["t"][0].split(",", 1)[0])

        print("Playing media: {}".format(path))
        self._proc = subprocess.Popen(
            ["omxplayer", "-b", "-o", AUDIO_DEV, "-l", str(startTime), path],
            stdin=subprocess.PIPE,
            close_fds=True,
        )

    def stop(self):
        if self._proc and self._proc.poll() is None:
            try:
                self._proc.stdin.write("q".encode())
                self._proc.stdin.flush()
            except IOError:
                pass
            self._proc.wait()
        self._proc = None
