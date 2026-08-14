# Reports
From Vivado project, you can generate reports of design in detail. This text shows a summary of resource utilization and power consumption and CDC

- Not using ILAs, the design saves a lot of resources(LUT, LUTRAM, FF and BRAM). So, the bitstream running on device will not include ILAs. For developper want to debug, keep it is useful.

- Update reports pictures

## Resource utilization
- Note on resource utilization : The BRAM utilization is mostly full after using more FIFOs for true RNG data path. There are 2 cases could be optimized:
    - Could reduces size of FIFOs in this data paths but have to be careful to avoid underfow of data. 
    - Second option is reduce size of gc_fifo_in , this FIFO was upsized for debuging DDR4 Virtual FIFO empty, error was fixed by writing data in BURST to Virtual FIFO to regulate the traffic, the size of fifo_gc_in is not criminal because this fifo is read very fast, level of fifo should be close to empty. Care should be consider with the data written in BURST to fifo_gc_in, avoid making fifo_gc_in full because losed data could make mismatch angles between Alice and Bob

## CDC

There are some CDC critial warnings need to explain why could be ignored

## Constraints

Explain the constraints in XDC

