from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .crypto import sha256_bytes, sign_manifest, verify_manifest


@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> "Version":
        parts = value.lstrip("v").split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid semantic version: {value}")
        return cls(*(int(x) for x in parts))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass
class FirmwareImage:
    version: Version
    filename: str
    sha256: str
    size: int
    signature: str = ""

    def unsigned_manifest(self) -> dict:
        return {
            "version": str(self.version),
            "filename": self.filename,
            "sha256": self.sha256,
            "size": self.size,
        }

    def manifest_bytes(self) -> bytes:
        return json.dumps(
            self.unsigned_manifest(), sort_keys=True, separators=(",", ":")
        ).encode()

    def to_dict(self) -> dict:
        result = self.unsigned_manifest()
        result["signature"] = self.signature
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "FirmwareImage":
        return cls(
            Version.parse(data["version"]),
            data["filename"],
            data["sha256"],
            int(data["size"]),
            data.get("signature", ""),
        )


def create_image(
    version: str, firmware_path: Path, private_key=None
) -> FirmwareImage:
    data = firmware_path.read_bytes()
    image = FirmwareImage(
        version=Version.parse(version),
        filename=firmware_path.name,
        sha256=sha256_bytes(data),
        size=len(data),
    )
    if private_key:
        image.signature = sign_manifest(image.manifest_bytes(), private_key)
    return image


def verify_image(
    image: FirmwareImage, data: bytes, public_key
) -> tuple[bool, str]:
    if len(data) != image.size:
        return False, "size mismatch"
    if sha256_bytes(data) != image.sha256:
        return False, "sha256 mismatch"
    if not image.signature:
        return False, "missing signature"
    if not verify_manifest(image.manifest_bytes(), image.signature, public_key):
        return False, "signature verification failed"
    return True, "valid"
