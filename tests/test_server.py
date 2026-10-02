import asyncio
import json

import pytest

websockets = pytest.importorskip("websockets")
from backend.server import Hub


def test_set_language_and_broadcast():
    async def run():
        hub = Hub()
        server = await hub.serve("127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        async with websockets.connect(f"ws://127.0.0.1:{port}") as ws:
            assert json.loads(await ws.recv())["language"] == "es"
            await ws.send(json.dumps({"type": "set_language", "language": "uk"}))
            assert json.loads(await ws.recv())["language"] == "uk"
            await hub.broadcast({"type": "result", "translation": "Привіт"})
            assert json.loads(await ws.recv())["translation"] == "Привіт"
        server.close()
    asyncio.run(run())
