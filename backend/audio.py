"""USB audio input device discovery and capture."""
import queue

SAMPLE_RATE = 16000
BLOCK = 512  # samples per chunk expected by Silero VAD at 16 kHz


def list_input_devices(usb_only=True):
    import sounddevice as sd
    devices = [(i, d) for i, d in enumerate(sd.query_devices()) if d["max_input_channels"] > 0]
    usb = [(i, d) for i, d in devices if "usb" in d["name"].lower()]
    return usb if usb_only and usb else devices


def select_device():
    devices = list_input_devices()
    if not devices:
        raise SystemExit("No audio input devices found")
    print("Audio input devices:")
    for n, (i, d) in enumerate(devices):
        print(f"  [{n}] {d['name']} (id {i})")
    while True:
        choice = input("Select device number: ").strip()
        if choice.isdigit() and int(choice) < len(devices):
            return devices[int(choice)][0]


def stream_chunks(device):
    """Yield float32 mono chunks of BLOCK samples from the device."""
    import sounddevice as sd
    q = queue.Queue()
    with sd.InputStream(device=device, channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK,
                        dtype="float32", callback=lambda data, *_: q.put(data[:, 0].copy())):
        while True:
            yield q.get()
