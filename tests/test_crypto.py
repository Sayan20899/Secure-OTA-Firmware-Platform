from pathlib import Path

from ota.crypto import generate_keypair, load_private_key, load_public_key
from ota.image import create_image, verify_image


def test_signed_image_verifies(tmp_path: Path):
    private_path = tmp_path / "private.pem"
    public_path = tmp_path / "public.pem"
    generate_keypair(private_path, public_path)

    firmware = tmp_path / "firmware.bin"
    firmware.write_bytes(b"hello firmware")

    image = create_image("1.0.0", firmware, load_private_key(private_path))
    assert verify_image(image, firmware.read_bytes(), load_public_key(public_path)) == (
        True,
        "valid",
    )


def test_tampered_image_is_rejected(tmp_path: Path):
    private_path = tmp_path / "private.pem"
    public_path = tmp_path / "public.pem"
    generate_keypair(private_path, public_path)

    firmware = tmp_path / "firmware.bin"
    firmware.write_bytes(b"hello firmware")

    image = create_image("1.0.0", firmware, load_private_key(private_path))
    assert verify_image(image, b"tampered", load_public_key(public_path))[0] is False
