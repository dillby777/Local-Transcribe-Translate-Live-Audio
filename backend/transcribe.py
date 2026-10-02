"""Whisper large-v3-turbo transcription."""


class Transcriber:
    def __init__(self, model_name="large-v3-turbo"):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(model_name, device="auto", compute_type="auto")

    def transcribe(self, audio):
        segments, info = self.model.transcribe(audio, vad_filter=False)
        return " ".join(s.text.strip() for s in segments).strip(), info.language
