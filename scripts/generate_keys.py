from pathlib import Path

from ota.crypto import generate_keypair

ROOT = Path(__file__).resolve().parents[1]
KEYS = ROOT / "runtime" / "keys"
KEYS.mkdir(parents=True, exist_ok=True)

generate_keypair(KEYS / "private_key.pem", KEYS / "public_key.pem")
print(f"Generated keys in {KEYS}")
