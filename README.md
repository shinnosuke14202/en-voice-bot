# Speaking/Chat App (Ollama + Whisper + Piper)

A local **AI speaking app** for daily conversations, powered by:
- [Ollama](https://ollama.com) — Large Language Models (chatting, conversation)
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) — Speech-to-Text (transcribe your voice)
- [Piper](https://github.com/rhasspy/piper) — Text-to-Speech (natural voices)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern Python GUI  

No internet required after setup. Everything runs **fully local** on your computer.

## Features
- 🎙️ Record your voice → transcribed with Whisper  
- 💬 AI replies with natural conversation using Ollama  
- 🔊 Text-to-Speech playback via Piper (choose your voice)  
- ⌨️ Manual text input also supported  
- ⚡ Works fully offline after downloading models

## Installation and Setup

1) Install deps (Windows)
```
   pip install customtkinter sounddevice soundfile numpy faster-whisper ollama
```


2) Install & run Ollama:
   
[Download Ollama](https://ollama.com/download)  
[Ollama API Docs](https://github.com/ollama/ollama/blob/main/docs/api.md)  
```
   ollama serve
   ollama pull llama3.1:8b
```


3) Install Piper & voice:
   
[Piper (OHF-Voice)](https://github.com/OHF-Voice/piper1-gpl)  
[Piper Python API Docs](https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_PYTHON.md)  
[Piper Sample Voices](https://rhasspy.github.io/piper-samples/) 

Download a voice .onnx file 
```
python -m piper.download_voices en_GB-cori-high
```


5) Run app:
```
python main.py
```

## UI

<img width="892" height="672" alt="image" src="https://github.com/user-attachments/assets/fabc4ea8-e51d-445f-9118-50db2f1eca6d" />

