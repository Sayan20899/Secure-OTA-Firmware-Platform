from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .repository import FirmwareRepository

ROOT = Path(__file__).resolve().parents[1] / "runtime" / "repository"
repository = FirmwareRepository(ROOT)

app = FastAPI(
    title="Secure OTA Firmware Server",
    version="1.0.0",
    description="Reference OTA firmware repository for the portfolio project.",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/firmware/latest")
def latest():
    try:
        return repository.latest().to_dict()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No firmware release available")


@app.get("/firmware/{filename}")
def download(filename: str):
    try:
        path = repository.file_path(filename)
    except (ValueError, FileNotFoundError):
        raise HTTPException(status_code=404, detail="Firmware image not found")
    return FileResponse(path, media_type="application/octet-stream", filename=path.name)
