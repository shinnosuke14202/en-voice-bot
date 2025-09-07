import subprocess
import time
import soundfile as sf
import sounddevice as sd



class PiperTTS:
    def __init__(self, piper_exe="piper", voice_model="./models/en_GB-cori-high.onnx"):
        self.piper_exe = piper_exe
        self.voice_model = voice_model

    def synth(self, text, out_wav):
        if not self.voice_model:
            raise RuntimeError("No Piper voice model set. Choose a .onnx voice file.")

        cmd = [self.piper_exe, "-m", self.voice_model, "-f", out_wav, "--sentence-silence", "0.5"]

        # Launch the external CLI program as a subprocess
        # By default, stdout and stderr are not captured, and those attributes
        # will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,  
            stderr=subprocess.PIPE
        )

        # Send the text to Piper via STDIN, wait for it to finish (max 90s)
        stdout, stderr = proc.communicate(input=text.encode('utf-8'), timeout=90)

        # If Piper failed, raise with the error message
        if proc.returncode != 0:
            raise RuntimeError(f"Piper failed: {stderr.decode('utf-8', errors='ignore')}")

        # Return the path of the WAV Piper just wrote
        return out_wav

    @staticmethod
    def play(wav_path):
        data, sr = sf.read(wav_path, dtype='float32')
        duration = len(data) / sr 
        sd.play(data, sr)
        time.sleep(duration + 1) 
