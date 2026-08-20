# Boards

4 boards: 
- 2x nrf52840dk with Waveshare SX1262HF (915 Mhz) (Dev kit - use whatever nrf board the standard online nrf52840dk setup uses)
    - Pin mappings: `Firmware resources/fixture-and-toolchain/nrf-sx-pin-mappings.md`.
    - This talks about my connection setup to make TX/RX work on lora + pin mappings
- 2x NUCLEO-L476RG (STM32L476RGT Nucleo dev kit)
    - I2C: PB13/PB14 - use the datasheet to find out which is I2C data and I2C CLK
