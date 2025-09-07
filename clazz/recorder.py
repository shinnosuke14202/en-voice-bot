import queue
import sys
import threading

import numpy as np
from config import DEFAULT_SAMPLE_RATE
import sounddevice as sd
import soundfile as sf


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

    def _collect(self):
        while self._rec:
            try:
                data = self._q.get(timeout=0.2)
                self.frames.append(data)
            except queue.Empty:
                pass

    def stop(self, wav_path):
        self._rec = False
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        if not self.frames:
            return False
        audio = np.concatenate(self.frames, axis=0)
        sf.write(wav_path, audio, self.samplerate, subtype='PCM_16')
        return True
