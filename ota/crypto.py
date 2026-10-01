from __future__ import annotations

import base64
import hashlib
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def generate_keypair(private_path: Path, public_path: Path) -> None:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_path.write_bytes(
        private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    public_path.write_bytes(
        public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )


def load_private_key(path: Path) -> Ed25519PrivateKey:
    return serialization.load_pem_private_key(path.read_bytes(), password=None)


def load_public_key(path: Path) -> Ed25519PublicKey:
    return serialization.load_pem_public_key(path.read_bytes())


def sign_manifest(manifest_bytes: bytes, private_key: Ed25519PrivateKey) -> str:
    return base64.b64encode(private_key.sign(manifest_bytes)).decode("ascii")


def verify_manifest(
    manifest_bytes: bytes, signature_b64: str, public_key: Ed25519PublicKey
) -> bool:
    try:
        public_key.verify(base64.b64decode(signature_b64), manifest_bytes)
        return True
    except (InvalidSignature, ValueError):
        return False
