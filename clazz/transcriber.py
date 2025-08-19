from faster_whisper import WhisperModel
from config import DEFAULT_WHISPER_MODEL


class Transcriber:
    def __init__(self, model_name=DEFAULT_WHISPER_MODEL, compute_type="auto"):
        self.model_name = model_name
        self.compute_type = compute_type
        self.model = WhisperModel(model_name, compute_type=compute_type)

    def reload(self, model_name):
        self.model_name = model_name
        self.model = WhisperModel(model_name, compute_type=self.compute_type)

    def transcribe(self, wav_path, language=None):
        segments, info = self.model.transcribe(wav_path, language=language)
        text_parts = []
        for seg in segments:
            text_parts.append(seg.text)
        return info.language, (" ".join(t.strip() for t in text_parts)).strip()
