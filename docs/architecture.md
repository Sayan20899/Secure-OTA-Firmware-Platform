# Architecture

## Layers

### Firmware layer
The real embedded implementation is expected to run on an ARM Cortex-M target under Zephyr RTOS.

### Boot layer
The bootloader validates the candidate image before handing control to the application.

### Update layer
The OTA client downloads a release manifest and firmware image from the server.

### Security layer
The release manifest is signed with Ed25519. The device verifies the signature and independently checks the SHA-256 digest of the image.

### Reliability layer
The image is staged before activation. A production implementation would use a power-loss-safe A/B or swap strategy.

## State machine

```text
IDLE
 |
 | update available
 v
DOWNLOADING
 |
 v
VERIFYING
 |          \
 | valid     \ invalid
 v            v
STAGED      REJECTED
 |
 v
ACTIVATING
 |
 +---- success ----> ACTIVE
 |
 +---- failure -----> ROLLBACK
```
