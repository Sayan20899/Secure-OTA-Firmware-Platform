# Secure Boot and Firmware Security

## Integrity

SHA-256 provides a deterministic digest of the firmware image. If the image changes, the digest changes.

## Authenticity

Ed25519 signing allows the device to verify that the release was signed by the trusted firmware publisher.

```text
Firmware -> SHA-256 -> Digest
                                           -> Signed manifest
                             |
Device -> verify signature --+
```

A hash by itself does not prove who produced an image.

## Production hardening

A production implementation should additionally consider:

- immutable root of trust
- hardware-backed key storage
- protected bootloader
- anti-rollback counters
- secure key provisioning
- debug-port protection
- secure random number generation
- threat modelling
- certificate/key rotation
