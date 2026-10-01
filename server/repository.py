from __future__ import annotations

import json
from pathlib import Path

from ota.image import FirmwareImage, Version


class FirmwareRepository:
    def __init__(self, root: Path):
        self.root = root
        self.manifest = root / "manifest.json"

    def latest(self) -> FirmwareImage:
        data = json.loads(self.manifest.read_text())
        return FirmwareImage.from_dict(data)

    def file_path(self, filename: str) -> Path:
        candidate = (self.root / filename).resolve()
        if candidate.parent != self.root.resolve():
            raise ValueError("invalid firmware filename")
        if not candidate.exists():
            raise FileNotFoundError(filename)
        return candidate

    def write_release(self, image: FirmwareImage) -> None:
        (self.root / image.filename).parent.mkdir(parents=True, exist_ok=True)
        self.manifest.write_text(json.dumps(image.to_dict(), indent=2))
