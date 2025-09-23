# FPGA module introduction
The FPGA integration module XEM8310-AU25P is a product of opalkelly, using AMD Artix UltraScale+ FPGA. All information about XEM8310 is available on [Documentation portal](https://docs.opalkelly.com/xem8310/introduction/) of opalkelly. From website you can also download:
- FrontPanel to setting devices, loading bitstream, flash,...
- Vivado board file
- Pins list

This FPGA module will be plugged to the "Bread70" PCB to communicate with all ICs on board. 
# Vivado project
The RTL source code and Vivado block design is available on GitHub [kiwi_fpga](https://github.com/Veriqloud/kiwi_fpga.git). Follow the instructions in README to rebuild Vivado project and block design from Tcl script. Then you have fully access to the project and can generate the bitstream for FPGA on your local machine.

The main blocks in project:
- XDMA
- Clock and reset
- Fastdac
- TDC 
- DDR4
- TTL gate
- Decoy signal
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
- USB and FrontPanel API: Install FrontPanel API and Configure Device with your bitstream
- JTAG: Simply Open Vivado Hardware manager, Open target and Program device

You can only have access to ILA debug windows in Vivado by JTAG. With this solution, you also can check the Calibration Process of DDR4. I tested severals FPGA modules with the same bitstream, some of them pass the Calibration Process smoothly, some don't. 

# Flashing bitstream
## Using JTAG
### Specification
There are 2 non-volatile memory to flash board XEM8310. Read Specification of the board
- System Flash
- FPGA Flash

We are going to choose FPGA Flash mode, using 32MiB QSPI non-volatile memory
[Opalkelly Flash Memory](https://docs.opalkelly.com/xem8310/flash-memory/)
### Generate specific bitstream
Usually, you generate bitstream in vivado -> top.bit configuration file
To be able to load .bit configuration to Flash Memory. Add these to .xdc constraint
```
set_property BITSTREAM.CONFIG.EXTMASTERCCLK_EN disable [current_design] 
set_property CONFIG_MODE SPIx4 [current_design] 
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design] 
set_property BITSTREAM.CONFIG.SPI_FALL_EDGE YES [current_design] 
set_property BITSTREAM.CONFIG.CONFIGRATE 85.0 [current_design]
```
Generate bitstream with these added constraints -> top.bit. This bit file only can be used by load it to FPGA Flash 
### Create the memory configuration .mcs file
In vivado:
Tools -> Generate Memory Configuration File -> Choose...
- Format: MCS
- Memory Part: IS25WP256D-x1x2x4
- Filename:/PATH_TO/top.mcs
- Interface:SPIx4
- Load bitstream files: /PATH_TO/top.bit
- Start Add at 0, direction up

Click OK to generate top.mcs
### Load the memory configuration file
In vivado:
- Open Hardware Manager
- Right click on Target -> configuration Memory Device
- choose the Memory part, top.mcs
- Choose: Erase, Program, Verify
- Program -> Wait it to finish
### Power cycle
Turn off and turn on FPGA.  The bitstream should be loaded after 2-3s. Ready to check
## Using FrontPanel
Generate the specific bitstream as Using JTAG method
### Download and install FrontPanel
run:
```
sudo ./install
```
build flashloader
```
cd Samples/FlashLoader/Cxx/
sudo make
```
### Download the Samples for XEM8310
- Download from opakelly Files Download
- copy the flashloader.bit to ../Samples/Flashloader/Cxx/
### Load bitstream
Create a bash script to flash your specific bitstream in /PATH_TO_BIT/
```
#!/bin/bash
pushd FrontPanel-Ubuntu22.04LTS-x64-5.3.6/Samples/FlashLoader/Cxx/ || exit 1
flashloader w /PATH_TO_BIT/Bob_top_wrapper.bit
popd
```
Power cycle the board and check


