from __future__ import annotations

import json
from pathlib import Path


class DeviceStorage:
    """Small filesystem-backed device state used by the host demonstration."""

    def __init__(self, root: Path):
        self.root = root
        self.active = root / "active.bin"
        self.staged = root / "staged.bin"
        self.state_file = root / "state.json"
        self.root.mkdir(parents=True, exist_ok=True)

    def state(self) -> dict:
        if not self.state_file.exists():
            return {"active_version": None, "pending_version": None}
        return json.loads(self.state_file.read_text())

    def save_state(self, state: dict) -> None:
        self.state_file.write_text(json.dumps(state, indent=2))

    def stage(self, data: bytes, version: str) -> None:
        self.staged.write_bytes(data)
        state = self.state()
        state["pending_version"] = version
        self.save_state(state)

    def activate(self, version: str) -> None:
        self.staged.replace(self.active)
        state = self.state()
        state["active_version"] = version
        state["pending_version"] = None
        self.save_state(state)

    def rollback(self) -> None:
        if self.staged.exists():
            self.staged.unlink()
        state = self.state()
        state["pending_version"] = None
        self.save_state(state)
