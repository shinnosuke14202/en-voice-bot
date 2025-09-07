from datetime import datetime
import subprocess
import ollama
from config import SYSTEM_PROMPT
from themes.colors import GREEN, RED, RESET


class LocalChat:
    def __init__(self, model):
        self.model = model
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.run(model=model)

    def ask(self, user_text):
        self.history.append({"role": "user", "content": user_text})
        res = ollama.chat(model=self.model, messages=self.history)
        reply = res["message"]["content"].strip()
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def run(self, model, model_name="ollama"):
        self.model = model
        proc = subprocess.Popen(
            f"{model_name} run {model}",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            _, stderr = proc.communicate(timeout=2)
            if proc.returncode != 0:
                raise RuntimeError(f"{RED}{stderr.decode('utf-8', errors='ignore')}{RESET}")
        except subprocess.TimeoutExpired:
            name, size = model.split(":") if ":" in model else (model, "unknown")
            print(f"{GREEN}✔ {model_name} is running → {name} [{size}]{RESET}")
