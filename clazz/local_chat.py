import ollama
from config import DEFAULT_OLLAMA_MODEL, SYSTEM_PROMPT


class LocalChat:
    def __init__(self, model=DEFAULT_OLLAMA_MODEL):
        self.model = model
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def ask(self, user_text):
        self.history.append({"role": "user", "content": user_text})
        res = ollama.chat(model=self.model, messages=self.history)
        reply = res["message"]["content"].strip()
        self.history.append({"role": "assistant", "content": reply})
        return reply
