# SPI

To manage spi transfers between master (fpga) and slaves (devices on Bread70), use AXI Quad Spi IP. 
- Configure IP in standard mode, and choose number of slaves on the same bus
- spi_inout_mngt.v : used as a buffer between AXI Quad SPI pins and physical pins

Based on the number of devices and their digital characteristics, there are 3 spi buses:
- SPI1: jitter cleaner and tdc
- SPI2: clockchip, fast dac, slow dac
- SPI3: slow adc 
## SPI1
- Spi voltage level: 3.3V
- Serial clk: 10MHz
- Jitter cleaner reset pin: HIGH
```
Board pins | FPGA pin name     | Notes  |
---------- +------------------ +--------+
sclk1      |ext_tdc_sclk   D10 | 10MHz 
mosi1      |ext_tdc_mosi   H11 | sdi,  data from fpga to device
miso1      |ext_tdc_miso   G11 | sdo, data from device to fpga
sss        |ext_tdc_ss[1]  K10 | chip select for jitter cleaner
ssa        |ext_tdc_ss[0]  C9  | chip select for tdc
```

- Pull chip select bit to 1 to disable the device.
- 0x03: Disable both
- 0x01: Enable jitter cleaner, Disable tdc
- 0x02: Enable tdc, Disable jitter cleaner
## SPI2
- Spi voltage level: 3.3V
- Serial clk: 15MHz
```
Board pins| FPGA pin name         | Notes|
----------+---------------------- +------+
sclk2     |ext_dac_ltc_sclk   D11 | 15MHz from MMCM of DDR4
mosi2     |ext_dac_ltc_mosi   B11 | sdi,  data from fpga to device
miso2     |ext_dac_ltc_miso   C11 | sdo, data from device to fpga 
cs_l      |ext_dac_ltc_ss[2]  H9  | chip select for clock chip
cs_da     |ext_dac_ltc_ss[1]  J9  | chip select for slow dac
cs_ad     |ext_dac_ltc_ss[0]  D9  | chip select for fast dac
```
- Pull chip select bit to 1 to disable the device.
- 0x07: Disable both
- 0x03: Enable clock chip, Disable others
- 0x05: Enable slow dac, Disable others
- 0x06: Enable fast dac, Disable others
## SPI3
- Spi voltage level: 3.3V
- Serial clk: 16MHz
```
Board pins| FPGA pin name         | Notes|
----------+---------------------- +------+
a.sclk    |ext_adc_sclk   D14 | 16MHz from ?
a.mosi    |ext_adc_mosi   A13 | sdi,  data from fpga to device
a.miso    |ext_adc_miso   A12 | sdo, data from device to fpga 
a.cs      |ext_adc_ss     C13 | chip select for slow adc
```
- Pull chip select bit to 1 to disable the device.

## Scripts 
Read AMD [AXI Quad SPI](https://www.amd.com/content/dam/xilinx/support/documents/ip_documentation/axi_quad_spi/v3_2/pg153-axi-quad-spi.pdf) to understand AXI Quad SPI.

These 3 functions allow you to write and read to all devices on spi1 and spi2
1. Init_spi(base, offset, spi_mode): configure AXI quad spi 
- base and offset of axil address: defined in address table of fpga
- spi_mode: {0,1,2,3}, depends on the devices

1. Set_reg(spi_bus, device, args): write to devices
1. Get_reg(spi_bus, device, expect, args): read from devices
- spi_bus: {1,2}, corresponding to spi1 and spi2
- device: name of device in the list
- args: what you want to transmit to device (reg address and data of the device). 
- expect: correct values of register you are reading

Example: you want to write to clockchip, address 0x04, value 0x05
```
Set_reg(2, 'ltc', 0x04, 0x05)
```
You can write n bytes to devices if allowed, each value always 1 bytes (standard)
