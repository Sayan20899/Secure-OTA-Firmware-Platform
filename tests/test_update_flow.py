from pathlib import Path

from ota.crypto import generate_keypair, load_private_key, load_public_key
from ota.image import create_image, verify_image
from ota.storage import DeviceStorage


def test_stage_and_activate(tmp_path: Path):
    private = tmp_path / "private.pem"
    public = tmp_path / "public.pem"
    generate_keypair(private, public)

    firmware = tmp_path / "firmware.bin"
    firmware.write_bytes(b"firmware v1")

    image = create_image("1.0.0", firmware, load_private_key(private))
    valid, reason = verify_image(image, firmware.read_bytes(), load_public_key(public))

    assert valid is True
    assert reason == "valid"

    storage = DeviceStorage(tmp_path / "device")
    storage.stage(firmware.read_bytes(), "1.0.0")
    storage.activate("1.0.0")

    assert storage.state()["active_version"] == "1.0.0"
    assert storage.active.read_bytes() == b"firmware v1"


def test_rollback_removes_staged_image(tmp_path: Path):
    storage = DeviceStorage(tmp_path / "device")
    storage.stage(b"bad firmware", "2.0.0")
    storage.rollback()

    assert not storage.staged.exists()
    assert storage.state()["pending_version"] is None
