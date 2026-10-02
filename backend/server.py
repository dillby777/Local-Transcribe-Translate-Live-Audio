"""WebSocket server: broadcasts JSON results, receives language selection."""
import asyncio
import json

LANGUAGES = {"es": "Spanish", "uk": "Ukrainian"}


class Hub:
    def __init__(self, default_language="es"):
        self.clients = set()
        self.language = default_language

    async def handler(self, ws):
        self.clients.add(ws)
        try:
            await ws.send(json.dumps({"type": "config", "language": self.language,
                                      "languages": LANGUAGES}))
            async for raw in ws:
                try:
                    msg = json.loads(raw)
                except ValueError:
                    continue
                if (isinstance(msg, dict) and msg.get("type") == "set_language"
                        and msg.get("language") in LANGUAGES):
                    self.language = msg["language"]
                    await self.broadcast({"type": "config", "language": self.language,
                                          "languages": LANGUAGES})
        finally:
            self.clients.discard(ws)

    async def broadcast(self, message):
        data = json.dumps(message, ensure_ascii=False)
        await asyncio.gather(*(c.send(data) for c in list(self.clients)), return_exceptions=True)

    async def serve(self, host="0.0.0.0", port=8765):
        import websockets
        return await websockets.serve(self.handler, host, port)
