# FPGA module introduction
The FPGA integration module XEM8310-AU25P is a product of opalkelly, using ADM Artix UltraScale+ FPGA. All information about XEM8310 is available on [Documentation portal](https://docs.opalkelly.com/xem8310/introduction/) of opalkelly. From website you can also download:
- FrontPanel to setting devices, loading bitstream, flash,...
- Vivado board file
- Pins list

This FPGA module will be plugged to the "Bread70" PCB to communicate with all ICs on board. 
# Vivado project
The RTL source code and Vivado block design is available on GitHub [kiwi_fpga](https://github.com/Veriqloud/kiwi_fpga.git). Follow the instructions in README to rebuild Vivado project and block design from Tcl script. Then you have fully access to the project and can generate the bitstream for FPGA from your local machine.

The main blocks in project:
- XDMA
- Clock and reset management
- Fastdac
- TDC 
- DDR4
- TTL gate
- SPI
- ILA debug

Reading the detail of each block in sub-chapters
# Prepare FPGA board
Configuration VIO voltage for XEM8310 is the first step to do after getting FPGA. Simply download the FrontPanel API from opalkelly website to your local machine, connect the USB-C and change these VIO settings:
- VIO1 = 1.8V
- VIO2 = 2.5V
- VIO3 = 3.3V

Restart the FPGA module and verify the VIOs. Then you can plug FPGA module to power verified Bread70.
# Loading bitstream
There are 2 ways to load bitstream to FPGA
- USB and FrontPanel API
- JTAG

You can only have access to ILA debug windows in Vivado by JTAG. With this solution, you also can check the Calibration Process of DDR4. I tested severals FPGA modules, some of them pass the Calibration Process smoothly, some doesn't.

