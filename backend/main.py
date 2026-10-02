"""Entry point: USB mic -> Silero VAD -> Whisper -> TranslateGemma, with WebSocket output."""
import argparse
import asyncio

from . import audio
from .server import Hub


def run_pipeline(device, hub, loop):
    from .transcribe import Transcriber
    from .translate import Translator
    from .vad import UtteranceDetector
    vad, stt, mt = UtteranceDetector(), Transcriber(), Translator()
    print("Listening...")
    for chunk in audio.stream_chunks(device):
        utt = vad.feed(chunk)
        if utt is None:
            continue
        text, lang = stt.transcribe(utt)
        if not text:
            continue
        print(f"[transcript:{lang}] {text}")
        target = hub.language  # Spanish by default
        translation = mt.translate(text, lang, target)
        print(f"[translation:{target}] {translation}")
        asyncio.run_coroutine_threadsafe(hub.broadcast({
            "type": "result", "source_language": lang, "transcript": text,
            "target_language": target, "translation": translation}), loop)


async def amain(args):
    hub = Hub()
    await hub.serve(port=args.port)
    print(f"WebSocket server on ws://0.0.0.0:{args.port}")
    device = audio.select_device()
    await asyncio.get_running_loop().run_in_executor(
        None, run_pipeline, device, hub, asyncio.get_running_loop())


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    asyncio.run(amain(p.parse_args()))
