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

## Build the hardware boxes

Some pictures for instructions

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
- Register values are generated from Analog Devices Software 
- When SPI works, configure clockchip with generated registers. If configure properly, pll is locked, you will get output clocks at expected frequency

Config_Ltc() function will write configuration and read back registers to verify. Run this command to execute this function:
```
python main.py party_name --ltc_init
```
- Align all outputs by provide a pulse to sync pin 
Sync_Ltc() function sends a trigger signal to FPGA, FPGA generates the sync pulse for clockchip 
```
python main.py party_name --sync_ltc
```
After this process, clock outputs are aligned. Check with oscilloscope. 
Clockchip is always the first device to configure
### Fast DAC
- Register values are calculated based on datasheet
- Generate double pulse on alice

```
python main.py alice --sequence dp
python main.py alice --shift 2 0 0 0 0 0
python main.py alice --fda_init

```
- If you want to generate single pulse, just need to update --sequence command. It depends what you wrote to dpram_seq
```
python main.py alice --sequence sp
```
- Similarly, change the mode, amplitude, shift in --shift command. It depends what you wrote to dpram_rng and rng fifo
### Slow DAC
- Register values are calculated based on datasheet
- When SPI works, the chip works directly

Config_Sda(): include Soft reset, set configuration registers and read back registers to verify
```
python main.py party_name --sda_init
```
Set_vol(channel, voltage): This function defines output value on which channel. 
- Bias for Voltage Control Attenuator(VCA): channel 7, vol_value from 0V to 5V
- Bias for Amplitude modulator(AM): channel 4, vol_value from -10V to 10V
- Bias for Polarization Controller(PolC): from channel 0 to 3, vol_value from 0V to 5V
```
python main.py party_name --am_bias 4 vol_value
python main.py party_name --vca_bias 7 vol_value
python main.py party_name --pol_bias chan vol_value
```
You should connect output load before setting voltage on DAC output, setting voltage back to 0 before disconnect the load. Otherwise, you have to reset the device (reload bitstream and reboot). Use volmeter to verify output voltages
### TDC and Jitter cleaner
#### Jitter cleaner
Jitter cleaner Si5319 clean the jitter of 5MHz generated from FPGA. 5MHz is reference clock for tdc.
The device works when SPI works, reset pin is HIGH generated from FPGA

Config_Jic(): Set cofiguration registers and read back to verify. Run command to init jitter cleaner:
```
python main.py bob --jic_init
```
#### TDC
To test TDC, you can generate a simualted STOPA signal from FPGA or take diretly output signal from APD
- Generate a signal 50kHz, duty cycle 65ns, simulate signal from APD
```
python main.py bob --sim_stop_pulse 5 21
```
- APD can be set in continuous mode or gated mode (with gate signal). 

Module tdc also have continuous mode and gated mode:
- continuous mode: detects all clicks whether APD in continuous mode or gated mode
- gated mode: detects only clicks inside the software filter. Software filter is defined by 4 parameters: gate0, width0, gate1, width1

Set parameters for tdc depends on which mode
```
python main.py bob --time_calib_reg command t0 gc_back gate0 width0 gate1 width1
```
Enable tdc module, start state machine with start_gc, this start_gc is aligned to the next pps edge
```
python main.py bob --time_calib_init
```
Get detection result
```
python main.py bob --gated_det
```
you should get data in histogram_gated.txt. Start with simple test:
- Generate single pulse from Pulse Generator
- Set APD in continuous mode
- Set module tdc in continuous mode
- Start state machine
- Get detection result
- Draw the histogram

After going through these steps, you can advance in double pulse, changing APD mode, changing tdc module mode, changing click rate,... 
### TTL gate
The purpose is to generate the gate signal for APD. Duty cycle is large enough to fit 2 peaks (click 0 and click 1). This signal can be delayed (tune+fine) 12,5ns. Run these command to apply settings and generate signal with duty and tune parameters
```
python main.py debug --ttl_rst
python main.py debug --para_master duty tune fine inc
python main.py debug --para_slaves fine1 inc1 fine2 inc2
python main.py debug --regs_en
```
Run these command to trigger fine delays. There are 3 fine delay modules cacasded in FPGA, so you have to trigger 3 modules: master, slave1 and slave2. Depends on the fine value, number of trigger command changes. Trigger signal on oscilloscope with PPS to figure out your settings
```
python main.py debug --add_delay_m
python main.py debug --add_delay_s1
python main.py debug --add_delay_s2
```

### DDR4	

## Physics experiments
After passing the electronics tests, you can connect electrical signals to optical components and do some experiments



