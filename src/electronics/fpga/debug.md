# ILA debug

Vivado supports ILA core for debugging. ILA allows you to probe signals and interface in fpga directly, you can see waveform of signals but just at the trigger time because the depth of FIFO in ILA is limitted. You can have access to ILA only with JTAG cable.

It's a great support for debugging but could affect timing of the design leads to fail functions. You can add or remove signals in same clock domain with ILA for debugging purpose. 

Failed case example : Probing rd_en_4 signal in multiple ILAs in **Decoy Signal** block creates timing error, leading to signal glitching, and inconsistent fiber delay need to be set to get correlation of angles after reading from DDR4

# Bugs and issues