# Bootloader Design

A production ARM implementation separates the bootloader from the application in flash.

```text
Flash
+------------------------+
| Bootloader             |
+------------------------+
| Image metadata         |
+------------------------+
| Active application     |
+------------------------+
| Candidate/update image |
+------------------------+
```

At reset the bootloader:

1. Reads image metadata.
2. Checks image size and integrity.
3. Verifies authenticity.
4. Applies version policy.
5. Selects a valid image.
6. Transfers control to the application.

The current repository implements this decision logic at the host level. A hardware deployment should use a mature MCU bootloader such as MCUboot where appropriate rather than replacing a silicon/platform root of trust with application code.
