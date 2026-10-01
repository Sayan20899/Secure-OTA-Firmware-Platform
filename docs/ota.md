# OTA/FOTA Design

The host demonstration models the OTA lifecycle:

```text
Build
  ↓
Sign
  ↓
Publish
  ↓
Device checks version
  ↓
Download
  ↓
Verify
  ↓
Stage
  ↓
Activate
  ↓
Rollback on failure
```

For a real device, transport security should use TLS and device authentication. The firmware image should still be cryptographically verified after transport because TLS alone does not replace firmware authenticity controls.

A production embedded target should use a power-loss-safe update strategy such as A/B slots or a proven image-swap mechanism.
