# Secure OTA Firmware Update Platform

A portfolio-grade reference implementation of a secure firmware-update platform for embedded devices.

> **Important:** This repository is a complete runnable software demonstration of the architecture. The default demo runs entirely on a host computer so it can be tested without physical hardware. The embedded/Zephyr integration points are documented for later hardware deployment.

## What this project demonstrates

- Firmware version management
- Firmware image metadata
- SHA-256 integrity verification
- Ed25519 digital-signature verification
- OTA-style firmware download
- Version policy / anti-downgrade check
- Atomic update staging
- Rollback after a failed activation
- Device state machine
- REST API firmware server
- Automated unit/integration tests
- CI-ready project structure

## Architecture

```text
                    ┌─────────────────────────────┐
                    │      Firmware Builder       │
                    │  version + image + signing  │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │      OTA Firmware Server    │
                    │        FastAPI / HTTP       │
                    └──────────────┬──────────────┘
                                   │
                              GET /firmware
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Device Simulator      │
                    │                             │
                    │  Check version             │
                    │  Download                  │
                    │  SHA-256                   │
                    │  Signature verification    │
                    │  Stage image               │
                    │  Activate                  │
                    │  Rollback                  │
                    └─────────────────────────────┘
```

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the complete demo:

```bash
python scripts/demo.py
```

Run tests:

```bash
pytest -q
```

Start the OTA server:

```bash
uvicorn server.app:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Demo flow

The demo creates a signed firmware v1.0.0, starts the server, provisions the device, downloads and verifies the image, and activates it.

It then creates v1.1.0 and performs another OTA update.

Finally, it creates a deliberately corrupted firmware package. The device rejects the corrupted image and retains the previously active firmware.

Expected high-level result:

```text
Firmware v1.0.0 -> installed
Firmware v1.1.0 -> installed
Corrupted image -> rejected
Active firmware  -> v1.1.0
```

## Project structure

```text
secure-ota-firmware-platform/
├── firmware/
│   └── sample/
│       ├── v1.0.0.bin
│       └── v1.1.0.bin
├── ota/
│   ├── client.py
│   ├── crypto.py
│   ├── image.py
│   └── storage.py
├── server/
│   ├── app.py
│   └── repository.py
├── scripts/
│   ├── build_firmware.py
│   ├── generate_keys.py
│   └── demo.py
├── tests/
│   ├── test_crypto.py
│   ├── test_image.py
│   └── test_update_flow.py
├── docs/
│   ├── architecture.md
│   ├── bootloader.md
│   ├── ota.md
│   ├── secure_boot.md
│   └── validation.md
├── embedded/
│   └── README.md
├── requirements.txt
└── .github/workflows/ci.yml
```

## Security model

The demonstration uses:

1. **SHA-256** to detect image modification.
2. **Ed25519 signatures** to authenticate the firmware publisher.
3. **Monotonic firmware versions** to reject downgrades.
4. **Atomic staging** so an incomplete update is not activated.
5. **Rollback** if activation fails.

This is a learning/portfolio implementation, not production automotive security firmware. Production devices require hardware-backed keys, secure key provisioning, secure boot ROM/root-of-trust support, protected flash, anti-rollback counters and platform-specific threat modelling.

## Hardware deployment path

The software architecture is intentionally separated from the device-specific layer. The `embedded/` directory documents how the same state machine maps to a Zephyr/ARM Cortex-M implementation.

Recommended future target:

- ARM Cortex-M MCU
- Zephyr RTOS
- MCUboot or a comparable bootloader
- Device networking through Wi-Fi/Ethernet
- Protected key storage
- Hardware-backed secure boot where supported

## Interview discussion points

Be prepared to explain:

- Why a hash alone does not provide authenticity.
- Why signatures are required.
- Why an update should be staged before activation.
- How rollback protects against interrupted or bad updates.
- Why version checks prevent downgrade attacks.
- How the host simulator maps to a real MCU bootloader.
- How RTOS tasks would separate sensing, communication, update and monitoring.

## License

MIT License.
