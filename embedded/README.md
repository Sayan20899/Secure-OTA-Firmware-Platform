# Embedded / Zephyr Integration

This directory is reserved for the hardware-specific implementation.

Recommended target architecture:

- ARM Cortex-M MCU
- Zephyr RTOS
- MCUboot
- Device networking
- Secure storage where available

The host implementation deliberately keeps the OTA state machine independent from hardware-specific APIs. This makes it possible to validate the protocol and security decisions before integrating them with a physical target.

Next hardware milestone:

1. Select a Zephyr-supported ARM Cortex-M board.
2. Create a Zephyr application with sensor, update and monitoring threads.
3. Integrate MCUboot.
4. Map image metadata to flash partitions.
5. Connect the device to the OTA server.
6. Perform hardware-in-the-loop update and rollback tests.
