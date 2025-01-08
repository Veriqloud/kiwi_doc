# Clock and reset management

## Clock
This is an overview of the clock distribution for Kiwi device. There are 3 clock sources:
- Source 100 MHz for PCIe comes from mother board of PC
- Source 100 MHz for DDR4 comes from oscilator on XEM8310 modules
- Source 10 MHz and PPS comes from White Rabbit Switch(WRS)

WRS 10 MHz is reference for PLL LTC6951 to generate clock pairs (sysref 3.125 MHz and refclk 200 MHz) for Fast DAC AD9152 and FPGA. PLL LTC6951 requires a SYNC signal to align all outputs to input, I use WRS PPS and 10 MHz to generate this signal, then the outputs will be aligned to PPS.

reflck 200 MHz is is the source clock for all logics in fpga, PPS is reference for synchronization       

![clock system](pics/clock_tree.png)

## Reset
Use module reset_register.v to synchronise reset to clock domain and change active level