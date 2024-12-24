# Hardware Testing


Just some guidelines for hardware testing. 

## Labequipment you might need

- Oscilloscope with sufficient bandwidth (e.g. Siglent SDS5034X 4Ch 350MHz 5GSa/s; or better)
- Voltmeter
- Optical powermeter
- analogue and logical probes for the oscilloscope
- fast photodiode
- soldering lab
- optical fibers and attenuators

## Electronics testing
This procedure is for individual test, on single node
1. Prepare XEM8310 (written in FPGA programming Chapter)
1. Prepare Computer (written in Computer Chapter)
1. Set up the hardware: XEM8310, Bread70, WRS, Computer
- Plug XEM8310 to Bread70
- Connect clocks from WRS to Bread70
- Connect Computer and Bread70 with PCIe
- 12V-5A Power Supply for Bread70 and XEM8310. Choose either Banana Jack on XEM8310 or on Bread70 to power, not using both at the same time
1. Turn on WRS, wait for the Sync Status is green
1. Power on the boards
1. Load bitstream to FPGA
1. Turn on computer and log in
1. Check if PCIe device is available. Device ID should return 9034
1. Using scripts in /qline/hw_control/ to test ICs   

If you want to test new bitstream, it's enough to just reload bitstream, then reboot computer
### Clockchip
### Fast DAC
### Slow DAC
### TDC and Jitter cleaner
### TTL gate
### DDR4	




