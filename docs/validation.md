# Validation Plan

| ID | Test | Expected result |
|---|---|---|
| T01 | Valid signed firmware | Install |
| T02 | Modified firmware | Reject |
| T03 | Invalid signature | Reject |
| T04 | Older firmware | Reject |
| T05 | Wrong image size | Reject |
| T06 | Interrupted staging | Do not activate |
| T07 | Activation failure | Rollback |
| T08 | Newer valid firmware | Install |

The automated tests cover the cryptographic verification, versioning and staging/rollback primitives. Additional hardware-in-the-loop tests should be added when a Zephyr/ARM target is selected.
