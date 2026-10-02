"""Silero VAD: groups audio chunks into speech utterances."""
import numpy as np

from .audio import SAMPLE_RATE


class UtteranceDetector:
    def __init__(self, threshold=0.5, max_silence_chunks=15, model=None):
        if model is None:
            from silero_vad import load_silero_vad
            model = load_silero_vad()
        self.model = model
        self.threshold = threshold
        self.max_silence = max_silence_chunks
        self.buf, self.silence = [], 0

    def _prob(self, chunk):
        import torch
        return float(self.model(torch.from_numpy(chunk), SAMPLE_RATE))

    def feed(self, chunk):
        """Return a complete utterance (np.ndarray) when speech ends, else None."""
        if self._prob(chunk) >= self.threshold:
            self.buf.append(chunk)
            self.silence = 0
        elif self.buf:
            self.buf.append(chunk)
            self.silence += 1
            if self.silence >= self.max_silence:
                audio = np.concatenate(self.buf)
                self.buf, self.silence = [], 0
                return audio
        return None
