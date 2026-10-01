from __future__ import annotations

from pathlib import Path

import httpx

from .crypto import load_public_key
from .image import FirmwareImage, Version, verify_image
from .storage import DeviceStorage


class OTAClient:
    def __init__(self, base_url: str, storage: DeviceStorage, public_key_path: Path):
        self.base_url = base_url.rstrip("/")
        self.storage = storage
        self.public_key = load_public_key(public_key_path)

    def current_version(self) -> Version | None:
        value = self.storage.state().get("active_version")
        return Version.parse(value) if value else None

    def check(self) -> FirmwareImage:
        response = httpx.get(f"{self.base_url}/firmware/latest", timeout=10)
        response.raise_for_status()
        return FirmwareImage.from_dict(response.json())

    def update(self) -> tuple[bool, str]:
        image = self.check()
        current = self.current_version()

        if current and image.version <= current:
            return False, f"update rejected: {image.version} is not newer than {current}"

        response = httpx.get(
            f"{self.base_url}/firmware/{image.filename}", timeout=30
        )
        response.raise_for_status()
        data = response.content

        valid, reason = verify_image(image, data, self.public_key)
        if not valid:
            return False, f"update rejected: {reason}"

        self.storage.stage(data, str(image.version))

        # Activation is deliberately isolated from staging so a future
        # hardware implementation can perform a power-loss-safe commit.
        try:
            self.storage.activate(str(image.version))
        except Exception as exc:
            self.storage.rollback()
            return False, f"activation failed; rollback performed: {exc}"

        return True, f"firmware {image.version} installed successfully"
