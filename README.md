# Local-Transcribe-Translate-Live-Audio
Transcribing live audio and translating into multiple languages with a handy dandy web interface

## Usage
```
pip install -r requirements.txt
python -m backend.main        # lists USB input devices, pick one; WebSocket on :8765
```
Open `frontend/index.html` in a browser. Pipeline: mic → Silero VAD → Whisper large-v3-turbo → TranslateGemma 12B (default Spanish; the page dropdown switches to Ukrainian). Results are logged to the console and broadcast as JSON over WebSocket.
