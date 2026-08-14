This note includes the tests of added fucntions after releases. 

# Realease 25th Mars 2026

- Using register to reset fifo_128x16,fifo_16x4 and fifo_decoy_rng_128x16,fifo_decoy_rng_16x2
- Monitoring almost_full and empty flags of only fifo_128x16 and fifo_decoy_rng_128x16

## Reset
- Reset HIGH
- Baseaddr = 0x00012000
- Module: clk_rst_axil_mngt.v
- Enable by pull high slv_reg7[0]  

### Software control
```python,hidelines=~
def rng_reset():                    
~   Write(0x00012000 + 28, 0x1)      
~   Write(0x00012000 + 28, 0x0)    
~   print("Reset rng stream fifos")  
```
## Monitor
- Baseaddr : 0x00030000
- Module : fastdac_axil_mngt.v
- Command request : pull high slv_reg0[1]
- Read back flags values : slv_reg9[3:0]

### slv_reg9 - R Access - Monitoring
|Bits|Signal name        |HW Wire          |Action/Value|Description
|----|-------------------|-----------------|------------|-----------
|31:4|-                 |-                 |-           |Reserved 0
|3|rng_fifos_status_i   |almost_full_16    |-           |almost_full of fifo_128x16
|2|rng_fifos_status_i   |empty_16          |-           |empty of fifo_128x16
|1|rng_fifos_status_i   |de_almost_full_16 |-           |almost_full of fifo_decoy_rng_128x16
|0|rng_fifos_status_i   |de_empty          |-           |empty of fifo_decoy_rng_128x16

### Software control
```python,hidelines=~
def rng_fifos_mon():
~   while(True):
~       #Write command
~       Write(0x00030000, 0x0)
~       Write(0x00030000, 0x2)
~       time.sleep(0.01)
~       #Read reg
~       mon_rng = Read(0x00030000 + 36)
~       hex_mon_rng = mon_rng.decode('utf-8').strip()
~       rng_almost_full = (int(hex_mon_rng, 16) & 0x8)>>3
~       rng_empty = (int(hex_mon_rng, 16) & 0x4)>>2
~       de_rng_almost_full = (int(hex_mon_rng, 16) & 0x2)>>1
~       de_rng_empty = int(hex_mon_rng, 16) & 0x1
~       print(f"rng_af,e: {rng_almost_full},{rng_empty} | de_rng_af,e: {de_rng_almost_full},{de_rng_empty}", flush=True)

```

