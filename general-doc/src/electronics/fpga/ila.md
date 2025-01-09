# ILA debug

Vivado supports ILA core for debugging. There are 3 ILAs in this design:
- ILA for fastdac
- ILA for tdc
- ILA for ddr4

ILA allows you to probe signals and interface in fpga directly, you can see waveform of signals but just at the trigger time because the depth of FIFO in ILA is limitted. You can have access to ILA only with JTAG cable.
It's a great support for debugging but could affect timing of the design. You can add or remove signals in same clock domain with ILA for debugging purpose 