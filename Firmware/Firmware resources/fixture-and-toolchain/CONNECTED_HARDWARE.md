# Connected Hardware and Pin Mapping

This document summarizes the fixed four-board firmware fixture. It is a human-readable reference,
not live hardware authority. Before any board, flash, reset, or RF action, confirm the current route
through the server's `setup_overview`, the manager's assignment, and the stable electronic identity.
Do not identify boards from removable labels alone.

## Physical topology

```text
STM-A (STM32L476RG) <--- wired I2C2 bus ---> STM-B (STM32L476RG)

NRF-A (nRF52840 DK) <--- SPI/GPIO ---> Waveshare CoreSX1262-A )) RF ((
NRF-B (nRF52840 DK) <--- SPI/GPIO ---> Waveshare CoreSX1262-B )) RF ((
```

There are four independently routed development boards:

- `STM-A`
- `STM-B`
- `NRF-A`
- `NRF-B`

The STM pair communicates over the installed wired I2C connection. Each nRF board has its own
Waveshare LoRa/CoreSX1262 module. The two LoRa endpoints communicate over RF when an explicitly
authorized RF test is active; they are not a shared wired SPI bus.

## Last recorded electronic routes

These are the last retained probe/VCOM mappings, not permission to operate them and not a substitute
for live discovery:

| Logical board | Target | Last recorded probe identity | Last recorded VCOM |
|---|---|---:|---:|
| `STM-A` | STM32L476RG | `066FFF514988525067233337` | `COM12` |
| `STM-B` | STM32L476RG | `0668FF514988525067213913` | `COM17` |
| `NRF-A` | nRF52840 DK | `683710208` | `COM16` |
| `NRF-B` | nRF52840 DK | `683854191` | `COM15` |

COM numbers may change. Stable probe/USB identity plus the live server route is authoritative.

## STM-A to STM-B I2C wiring

Both STM32L476RG boards use I2C2 alternate function AF4:

| Signal | STM-A | STM-B |
|---|---|---|
| I2C2 SCL | `PB13` | `PB13` |
| I2C2 SDA | `PB14` | `PB14` |
| Common reference | `GND` | `GND` |

The fixture record declares suitable installed 3.3 V pull-ups. Do not add, remove, meter, or rewire
them during normal suite work.

For serial diagnostics, the Nucleo-64 default route connects USART2 through the ST-LINK virtual COM
port:

- USART2 TX: `PA2`
- USART2 RX: `PA3`

Use firmware counters, peripheral registers, UART output, peer behavior, and debug evidence to
troubleshoot the link rather than changing the fixture.

## nRF52840 DK to Waveshare CoreSX1262 wiring

The retained shared mapping applies to each nRF/CoreSX1262 pair:

| CoreSX1262 signal | nRF52840 DK pin |
|---|---|
| SPI MOSI | `P1.15` |
| SPI MISO | `P1.14` |
| SPI SCK / CLK | `P1.13` |
| SPI chip select / CS | `P0.04` |
| DIO1 | `P0.03` |
| RESET | `P0.28` |
| BUSY | `P0.29` |
| DIO2 reader-only input | recorded as `P.05`; see ambiguity below |

Recorded module straps/connections:

- `RXEN` is soldered to `3V3`.
- CoreSX1262 `DIO2` is soldered to `TX_EN`.
- Each module is a Waveshare LoRa module/CoreSX1262 endpoint.
- The fixed fixture contract attests that suitable antennas are already connected.

### Unresolved notation

The original pin sheet literally records the DIO2 reader pin as `P.05`, not `P0.05`. This document
does not silently normalize that ambiguity. Confirm the exact DIO2 reader GPIO from the live
manager-supplied fixture/setup record before code or hardware action that depends on it.

The shared pin sheet does not state the exact module frequency-band variant, supply-current limit,
or local RF limits. Obtain those from the authoritative fixture/setup record. Never invent them
from a similar module.

## Operating boundaries

- Do not inspect, photograph, meter, reposition, or rewire the fixed fixture during ordinary tests.
- Do not swap logical board names based on labels; use verified electronic identity.
- Flashing, resets, RF transmission, and hardware mutation still require the target project's live
  plan, lease, and authorization.
- For RF, use the legal configured frequency, lowest practical transmit power, suitable bandwidth
  and duty cycle, and the already-connected antenna.
- External instruments are outside the normal suite contract. Use UART, packet counters, target
  registers, debug state, artifact hashes, and directly observed behavior as independent evidence.

## Source records

This summary was synthesized from:

- `BYO_FIRMWARE_MCP_END_TO_END_EXPERIMENTS.md`, sections 4 and 13;
- `fresh-experiments/A24_20260726-052146/nrf-sx-pin-mappings.md`;
- retained A22 setup records for `STM-A`;
- retained D31 setup records for `STM-B`; and
- retained A24 setup records for `NRF-A` and `NRF-B`.

The copied pin sheet is beside this file as `nrf-sx-pin-mappings.md`. The master test guide is under
`../test-program/`.
