import queue
import sys
import threading
from config import DEFAULT_SAMPLE_RATE
import sounddevice as sd


class Recorder:
    def __init__(self, samplerate=DEFAULT_SAMPLE_RATE, channels=1, device=None):
        self.samplerate = samplerate
        self.channels = channels
        self.device = device
        self._q = queue.Queue()
        self._rec = False
        self._stream = None
        self.frames = []

    def _callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if self._rec:
            self._q.put(indata.copy())

    def start(self):
        self.frames = []
        self._q = queue.Queue()
        self._rec = True
        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._callback,
            device=self.device,
            dtype='float32'
        )
        self._stream.start()
        self._collector = threading.Thread(target=self._collect, daemon=True)
        self._collector.start()
