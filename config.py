import os

DEFAULT_OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
DEFAULT_WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "medium")
DEFAULT_PIPER_MODEL = os.environ.get("PIPER_MODEL", "./models/en_GB-cori-high.onnx")
DEFAULT_SAMPLE_RATE = 16000

SYSTEM_PROMPT = (
    "You are a friendly, concise speaking partner for daily conversation practice. "
    "Keep replies short (1-3 sentences) and easy to understand. If asked for corrections, "
    "gently provide them and a natural alternative."
)
