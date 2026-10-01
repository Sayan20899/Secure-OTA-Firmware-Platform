from pathlib import Path
import argparse
import json

from ota.crypto import load_private_key
from ota.image import create_image

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    keys = ROOT / "runtime" / "keys"
    repo = ROOT / "runtime" / "repository"
    repo.mkdir(parents=True, exist_ok=True)

    private_key = load_private_key(keys / "private_key.pem")
    source = Path(args.input)
    image_path = repo / f"firmware-v{args.version}.bin"
    image_path.write_bytes(source.read_bytes())

    image = create_image(args.version, image_path, private_key)
    (repo / "manifest.json").write_text(json.dumps(image.to_dict(), indent=2))

    print(json.dumps(image.to_dict(), indent=2))


if __name__ == "__main__":
    main()
