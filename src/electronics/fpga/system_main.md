# System
## Description

Check again picture of electronics system in chapter **Electronics**. We design a mother board adapts to both Alice and Bob.

|Common chips | Only Alice | Only Bob
|-------------|------------|----------
|Clock buffer|slow DAC|TDC
|Clock chip  ||jitter cleaner
|Fast DAC    ||
|Slow ADC    || 
|TTL translator||

For time bin encoding scheme in our system, the arriving time of qubit matters. So the idea behind is using global counter value as a timestamp. This timestamp helps figure out the moment qubits arrive at modulators, then we can figure out the applied angles on the modulators. These angles are what we need for post-processing. 

We implement decoy state QKD scheme, so output angles includes:
| Alice | Bob
|-------|-----
|angles on AM | angles on PM
|angles on PM

Now, check interface between the ICs from FPGA to see how we drive them, what modules need to be done in FPGA

|Chips | InOut with FPGA | FPGA modules
|------|---------|------------
|Clock buffer |10MHz clock to FPGA| Clock input buffer
|Clock chip | SPI + refclk, sysrefclk, 100MHz clock | SPI + clock input buffers
|Fastdac | SPI + GTY lanes | SPI + jesd204B to transmit data to fastdac
|Slow ADC | SPI | SPI
|Slow DAC | SPI | SPI
|TTL translator | LVDS signals | There are 2 blocks: <br> - TTL gate for Bob <br> - Decoy signal for Alice
|TDC | SPI + clocks in and out + digital data | SPI + clock buffers + TDC data processing
|jitter cleaner | SPI + reset | SPI + small logic

Host computer interfaces with FPGA by PCIe for purpose of dynamic configuration, transmit and receive streams of data. Block XDMA in FPGA will be the bridge.
We can not miss source of angles which are true RNG, these sources input to FPGA through PCIe. Because they are angles on PM and AM of Alice so block Fastdac and Decoy signal contains modules incharge of tRNG.

In hardware setup, the angles are applied to qubit before we get timestamp value at detector. So to know which angles was applied we need to save them all to memory so that based on the timestamps and distance between modulators and detector, we check the corresponding address in memory. A DDR4 on board handles the storage, DDR4 block in FPGA handles state machine to write and read

There are many modules with different functions in same project, manage clocks and resets is essential.

Briefly, in FPGA should have blocks:
- XDMA, Clock and reset, SPI : global general purpose
- Fastdac, TTL gate, Decoy signal, TDC, DDR4 : local purpose.

## In this chapter
This chapter covers the RTL modules/IPs whoses functions are used for general purpose. It means that inputs could be from any part and outputs could distribute to any modules in the project. Then what are included in this chapter? (what block in block design?) And why?
- XDMA : In charge of memory access, mapping between host computer and FPGA. Communicate with host computer via AXIL and AXIS protocol.
- Clock and reset : In fact this block is a centralization of clock buffers and resets, whoses outputs distribute to coresponding modules
- SPI : In charge of interfacing with external devices using SPI protocol whoses share the same SPI bus
