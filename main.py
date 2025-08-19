import os
import threading
import tempfile
from datetime import datetime

import customtkinter as ctk
from tkinter import filedialog, messagebox

from config import DEFAULT_OLLAMA_MODEL, DEFAULT_PIPER_MODEL, DEFAULT_WHISPER_MODEL
from clazz import LocalChat, PiperTTS, Recorder, Transcriber


# ------------------------ GUI App ------------------------ #
class SpeakingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")  # or "dark"/"light"
        ctk.set_default_color_theme("blue")

        self.title("Local Speaking Chat (Ollama + Whisper + Piper)")
        self.geometry("900x650")

        # State
        self.recorder = Recorder()
        self.transcriber = Transcriber(DEFAULT_WHISPER_MODEL)
        self.tts = PiperTTS(voice_model=DEFAULT_PIPER_MODEL)
        self.chat = LocalChat(DEFAULT_OLLAMA_MODEL)
        self.last_reply_text = ""
        self.recording = False

        # Layout grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Settings frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(
            row=0, column=0, sticky="ew", padx=10, pady=10)
        self.settings_frame.grid_columnconfigure((1, 3, 5), weight=1)

        ctk.CTkLabel(self.settings_frame, text="Ollama model").grid(
            row=0, column=0, padx=6, pady=6)
        self.ollama_entry = ctk.CTkEntry(self.settings_frame)
        self.ollama_entry.insert(0, DEFAULT_OLLAMA_MODEL)
        self.ollama_entry.grid(row=0, column=1, sticky="ew", padx=6, pady=6)
        self.test_llm_btn = ctk.CTkButton(
            self.settings_frame, text="Test LLM", command=self.on_test_llm)
        self.test_llm_btn.grid(row=0, column=2, padx=6, pady=6)

        ctk.CTkLabel(self.settings_frame, text="Whisper model").grid(
            row=0, column=3, padx=6, pady=6)
        self.whisper_entry = ctk.CTkEntry(self.settings_frame)
        self.whisper_entry.insert(0, DEFAULT_WHISPER_MODEL)
        self.whisper_entry.grid(row=0, column=4, sticky="ew", padx=6, pady=6)
        self.reload_whisper_btn = ctk.CTkButton(
            self.settings_frame, text="Reload Whisper", command=self.on_reload_whisper)
        self.reload_whisper_btn.grid(row=0, column=5, padx=6, pady=6)

        ctk.CTkLabel(self.settings_frame, text="Piper voice .onnx").grid(
            row=1, column=0, padx=6, pady=6)
        self.piper_entry = ctk.CTkEntry(self.settings_frame)
        self.piper_entry.insert(0, DEFAULT_PIPER_MODEL)
        self.piper_entry.grid(row=1, column=1, columnspan=4,
                              sticky="ew", padx=6, pady=6)
        self.piper_browse_btn = ctk.CTkButton(
            self.settings_frame, text="Browse", command=self.on_browse_voice)
        self.piper_browse_btn.grid(row=1, column=5, padx=6, pady=6)

        # Controls frame
        self.ctrl_frame = ctk.CTkFrame(self)
        self.ctrl_frame.grid(row=1, column=0, sticky="ew",
                             padx=10, pady=(0, 10))
        self.ctrl_frame.grid_columnconfigure(3, weight=1)

        self.rec_btn = ctk.CTkButton(
            self.ctrl_frame, text="Start Recording", fg_color="#2e7d32", command=self.on_start_record)
        self.rec_btn.grid(row=0, column=0, padx=6, pady=8)
        self.stop_btn = ctk.CTkButton(self.ctrl_frame, text="Stop Recording",
                                      fg_color="#c62828", command=self.on_stop_record, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=6, pady=8)
        self.repeat_btn = ctk.CTkButton(
            self.ctrl_frame, text="Speak Last Reply", command=self.on_repeat, state="disabled")
        self.repeat_btn.grid(row=0, column=2, padx=6, pady=8)

        # Chat frame
        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.grid(
            row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1)

        self.chat_box = ctk.CTkTextbox(
            self.chat_frame, width=840, height=380, wrap="word")
        self.chat_box.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.chat_box.configure(state="disabled")

        # Manual input
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(
            row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.input_frame)
        self.entry.grid(row=0, column=0, sticky="ew", padx=6, pady=6)
        self.send_btn = ctk.CTkButton(
            self.input_frame, text="Send", command=self.on_send)
        self.send_btn.grid(row=0, column=1, padx=6, pady=6)

        # Status bar
        self.status_var = ctk.StringVar(value="Ready")
        self.status = ctk.CTkLabel(
            self, textvariable=self.status_var, anchor="w")
        self.status.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))

    # ---------- Helpers ---------- #
    def append_chat(self, role, text):
        ts = datetime.now().strftime("%H:%M")
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"[{ts}] {role}: {text}\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def set_status(self, text):
        self.status_var.set(text)
        self.update_idletasks()

    # ---------- Event Handlers ---------- #
    def on_browse_voice(self):
        path = filedialog.askopenfilename(title="Select Piper .onnx voice", filetypes=[
                                          ("Piper voice", ".onnx"), ("All files", "*.*")])
        if path:
            self.piper_entry.delete(0, "end")
            self.piper_entry.insert(0, path)

    def on_test_llm(self):
        try:
            self.chat.model = self.ollama_entry.get().strip() or DEFAULT_OLLAMA_MODEL
            reply = self.chat.ask(
                "Say 'Ready to chat.' in one short sentence.")
            self.append_chat("Assistant", reply)
            self.last_reply_text = reply
            self.repeat_btn.configure(state="normal")
            self.set_status("LLM OK")
        except Exception as e:
            messagebox.showerror("LLM error", str(e))
            self.set_status("LLM failed")

    def on_reload_whisper(self):
        try:
            m = self.whisper_entry.get().strip() or DEFAULT_WHISPER_MODEL
            self.transcriber.reload(m)
            self.set_status(f"Whisper loaded: {m}")
        except Exception as e:
            messagebox.showerror("Whisper error", str(e))

    def on_start_record(self):
        try:
            self.recorder.start()
            self.recording = True
            self.rec_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.set_status("Recording…")
        except Exception as e:
            messagebox.showerror("Audio error", str(e))

    def on_stop_record(self):
        if not self.recording:
            return
        self.recording = False
        self.rec_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.set_status("Processing…")

        threading.Thread(target=self._process_audio_flow, daemon=True).start()

    def _process_audio_flow(self):
        try:
            with tempfile.TemporaryDirectory() as td:
                wav_in = os.path.join(td, "input.wav")
                ok = self.recorder.stop(wav_in)
                if not ok:
                    self.set_status("No audio captured")
                    return
                self.set_status("Transcribing…")
                lang, text = self.transcriber.transcribe(wav_in)
                self.append_chat("You", text)

                self.set_status("Thinking…")
                self.chat.model = self.ollama_entry.get().strip() or DEFAULT_OLLAMA_MODEL
                reply = self.chat.ask(text)
                self.append_chat("Assistant", reply)
                self.last_reply_text = reply
                self.repeat_btn.configure(state="normal")

                self.set_status("Speaking…")
                self.tts.voice_model = self.piper_entry.get().strip() or DEFAULT_PIPER_MODEL
                wav_out = os.path.join(td, "reply.wav")
                self.tts.synth(reply, wav_out)
                PiperTTS.play(wav_out)
                self.set_status("Ready")
        except Exception as e:
            messagebox.showerror("Flow error", str(e))
            self.set_status("Error")

    def on_repeat(self):
        if not self.last_reply_text:
            return

        def _speak():
            try:
                self.set_status("Speaking…")
                with tempfile.TemporaryDirectory() as td:
                    wav_out = os.path.join(td, "repeat.wav")
                    self.tts.voice_model = self.piper_entry.get().strip() or DEFAULT_PIPER_MODEL
                    self.tts.synth(self.last_reply_text, wav_out)
                    PiperTTS.play(wav_out)
                self.set_status("Ready")
            except Exception as e:
                messagebox.showerror("TTS error", str(e))
                self.set_status("Error")
        threading.Thread(target=_speak, daemon=True).start()

    def on_send(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.append_chat("You", text)
        self.entry.delete(0, "end")

        def _chat_and_speak():
            try:
                self.set_status("Thinking…")
                self.chat.model = self.ollama_entry.get().strip() or DEFAULT_OLLAMA_MODEL
                reply = self.chat.ask(text)
                self.append_chat("Assistant", reply)
                self.last_reply_text = reply
                self.repeat_btn.configure(state="normal")
                self.set_status("Speaking…")
                with tempfile.TemporaryDirectory() as td:
                    wav_out = os.path.join(td, "reply.wav")
                    self.tts.voice_model = self.piper_entry.get().strip() or DEFAULT_PIPER_MODEL
                    self.tts.synth(reply, wav_out)
                    PiperTTS.play(wav_out)
                self.set_status("Ready")
            except Exception as e:
                messagebox.showerror("Chat error", str(e))
                self.set_status("Error")
        threading.Thread(target=_chat_and_speak, daemon=True).start()


if __name__ == "__main__":
    app = SpeakingApp()
    app.mainloop()
