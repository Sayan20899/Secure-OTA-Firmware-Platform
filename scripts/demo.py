from pathlib import Path
import json
import shutil
import subprocess
import sys
import time

import httpx
import uvicorn
from threading import Thread

from ota.client import OTAClient
from ota.crypto import load_private_key
from ota.image import create_image
from server.repository import FirmwareRepository

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
REPO = RUNTIME / "repository"
KEYS = RUNTIME / "keys"
DEVICE = RUNTIME / "device"


def build_release(version: str, content: bytes):
    source = RUNTIME / f"source-{version}.bin"
    source.write_bytes(content)
    private = load_private_key(KEYS / "private_key.pem")

    image_path = REPO / f"firmware-v{version}.bin"
    image_path.write_bytes(content)
    image = create_image(version, image_path, private)
    (REPO / "manifest.json").write_text(json.dumps(image.to_dict(), indent=2))
    return image


def main():
    if RUNTIME.exists():
        shutil.rmtree(RUNTIME)
    KEYS.mkdir(parents=True)
    REPO.mkdir(parents=True)

    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_keys.py")],
        check=True,
    )

    print("\n[1] Creating firmware v1.0.0")
    build_release("1.0.0", b"DEMO FIRMWARE VERSION 1.0.0\n")

    config = uvicorn.Config(
        "server.app:app", host="127.0.0.1", port=8765, log_level="warning"
    )
    server = uvicorn.Server(config)
    thread = Thread(target=server.run, daemon=True)
    thread.start()

    for _ in range(30):
        try:
            if httpx.get("http://127.0.0.1:8765/health").status_code == 200:
                break
        except Exception:
            time.sleep(0.1)

    from ota.storage import DeviceStorage

    client = OTAClient(
        "http://127.0.0.1:8765",
        DeviceStorage(DEVICE),
        KEYS / "public_key.pem",
    )

    print("[2] Installing v1.0.0")
    print("    ", client.update()[1])

    print("\n[3] Creating firmware v1.1.0")
    build_release("1.1.0", b"DEMO FIRMWARE VERSION 1.1.0\n")
    print("[4] Installing v1.1.0")
    print("    ", client.update()[1])

    print("\n[5] Corrupting the latest image")
    latest = REPO / "firmware-v1.1.0.bin"
    latest.write_bytes(b"TAMPERED FIRMWARE")

    # Restore the manifest so the device expects the original SHA-256/signature.
    # The image remains corrupted, therefore verification must fail.
    print("[6] Verifying corrupted firmware")
    result = client.update()
    print("    ", result[1])

    print("\n[7] Device state")
    print(json.dumps(client.storage.state(), indent=2))
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
