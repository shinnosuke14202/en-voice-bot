import subprocess
import soundfile as sf
import sounddevice as sd
from config import DEFAULT_PIPER_MODEL


class PiperTTS:
    def __init__(self, piper_exe="piper", voice_model=DEFAULT_PIPER_MODEL):
        self.piper_exe = piper_exe
        self.voice_model = voice_model

    def synth(self, text, out_wav):
        if not self.voice_model:
            raise RuntimeError("No Piper voice model set. Choose a .onnx voice file.")
        cmd = [self.piper_exe, "-m", self.voice_model, "-f", out_wav]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(input=text.encode('utf-8'), timeout=90)
        if proc.returncode != 0:
            raise RuntimeError(f"Piper failed: {stderr.decode('utf-8', errors='ignore')}")
        return out_wav

    @staticmethod
    def play(wav_path):
        data, sr = sf.read(wav_path, dtype='float32')
        sd.play(data, sr)
        sd.wait()
