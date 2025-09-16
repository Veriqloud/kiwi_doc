# Decoy signal
Purpose of this module:
- Generate signal for the second AM 
- Level is 0 or 1, apply randomly on qbit(12,5ns)
- Source of RNG is from second tRNG SwiftPro RNG

![](pics/decoy_signal.svg)

## decoy_rng_fifos.v
### Port descriptions
|Signals name         |Interface |Dir |Init status |Description
|---------------------|----------|----|------------|-----------
|s_axis_tdata[127:0]  |s_axis    |I   |-           |tRNG data come from xdma_h2c stream
|s_axis_tvalid        |s_axis    |I   |-           |data valid indication from xdma_h2c stream
|s_axis_tready        |s_axis    |O   |-           |ready signal from logic
|s_axis_clk           |Clock     |I   |250MHz      |Clock of axistream
|s_axis_tresetn       |Reset     |I   |-           |Reset of axistream, active LOW
|clk200               |Clock     |I   |200MHz      |Clock for logic
|tx_core_rst          |Reset     |I   |-           |Using same reset with rng fifos in fastdac
|rd_en_16             |-         |I   |-           |Enable signal at 10MHz, in clk200 domain
|rd_en_4              |-         |I   |-           |Enable signal at 40MHz, in clk200 domain
|de_rng_dout[3:0]     |-         |O   |-           |tRNG output at 40MHz


## decoy.v
### Port descriptions

|Signals name         |Interface |Dir |Init status |Description
|---------------------|----------|----|------------|-----------
|s_axil signals       |s_axil    |IO  |-           |standard s_axil interface 
|s_axil_aclk          |Clock     |I   |15MHz       |clock for axil interface 
|s_axil_aresetn       |Reset     |I   |-           |reset for axil interface, active LOW
|clk240               |Clock     |I   |240MHz      |clock to generate gate signal 
|clk80                |Clock     |I   |80MHz       |clock for fine delay this gate signal
|clk200               |Clock     |I   |200MHz      |clock to generate gate signal
|pps_i                |-         |I   |-           |PPS from WRS
|decoy_rst            |Reset     |I   |-           |reset for logic, active HIGH
|rd_en_4              |-         |I   |-           |Enable signal at 40MHz, in clk200 domain
|rng_value[3:0]       |-         |I   |-           |tRNG input at 40MHz
|decoy_signal_n/p     |-         |O   |-           |decoy signal output to pins
|decoy_signal         |-         |O   |-           |decoy signal output without delay
|the others signals   |-         |O   |-           |for debug on ILA


### User Parameters

|Parameter           |Value     |Description
|--------------------|----------|------------
|C_S_Axil_Addr_Width |12        |Address width of axil interface
|C_S_Axil_Data_Width |32        |Address width of axil interface
|DELAY FORMAT        |COUNT     |Delay format for ODELAY3
|DELAY TYPE          |VARIABLE  |Delay type for ODELAY3
|DELAY VALUE         |50        |need to be between 45-65 taps for IDELAY3 calibrates correctly
|REFCLK FRE          |300       |refclk for IDELAY3 and ODELAY3, default
|UPDATE MODE         |ASYNC     |update by logic control


### Axil registers
- Base address: 0x0001_6000
- Offset address slv_reg(n) : 4*n

#### slv_reg0 - R/W Access - Triiger Control
|Bits|Signal name |HW Wire      |Action/Value|Description
|----|------------|-------------|------------|-----------
|31:1|-           |-            |-           |Reserved 0
|0   |reg_enable_o|reg_enable_o |pull 0-1    |Enable register update

#### slv_reg1 - R/W Access - Configuration
|Bits|Signal name |HW Wire      |Action/Value|Description
|----|------------|-------------|------------|-----------
|31:4|-           |-            |-           |Reserved 0
|3:0 |tune_step_o |tune_step_o  |8 steps max in logic|Set tune step for decoy signal, 1 step is 1 period of 240MHz

#### slv_reg2 - R/W Access - Triiger Control
|Bits|Signal name             |HW Wire      |Action/Value|Description
|----|------------------------|-------------|------------|-----------
|31:3|-                       |-            |-           |Reserved 0
|2   |trigger_enstep_slv2_o   |trigger_enstep_slv2_o |pull 0-1-0.Stay HIGH long enough<br>coresponding resolution |trigger fine delay slave 2
|1   |trigger_enstep_slv1_o   |trigger_enstep_slv1_o |same as slave 2 |trigger fine delay slave 1
|0   |trigger_enstep_o        |trigger_enstep_o      |same as slave 2 |trigger fine delay master

#### slv_reg3 - R/W Access - Configuration
|Bits|Signal name |HW Wire      |Action/Value|Description
|----|------------|-------------|------------|-----------
|31:1|-           |-            |-           |Reserved 0
|0   |decoy_rng_mode_o |decoy_rng_mode_o  |0: from dpram<br>1: from tRNG|Choose rng source

#### slv_reg5 - R/W Access - Configuration
|Bits |Signal name     |HW Wire             |Action/Value|Description
|-----|----------------|--------------------|------------|-
|31:15|-               |-                   ||Reserved 0
|14:1 |decoy_params_80_o|resolution         |max is 8192|Set length of fine delay step on master ODELAY3
|0    |decoy_params_80_o|increase_en        |1: increase<br>0: decrease|Set fine delay direction on master ODELAY3

#### slv_reg6 - R/W Access - Configuration
|Bits |Signal name         |HW Wire         |Action/Value |Description
|-----|--------------------|----------------|------------|-
|31   |-                   |-               ||Reserved 0
|30:17|decoy_params_slv_o  |resolution_slv2 |max is 8192|Set length of fine delay step on slave 2 ODELAY3
|16   |decoy_params_slv_o  |increase_en_slv2|1: increase<br>0: decrease|Set fine delay direction on slave 2 ODELAY3
|14:1 |decoy_params_slv_o  |resolution_slv1 |max is 8192|Set length of fine delay step on slave 1 ODELAY3
|0    |decoy_params_slv_o  |increase_en_slv1|1: increase<br>0: decrease|Set fine delay direction on slave 1 ODELAY3

#### slv_reg7 - R/W Access - Configuration
|Bits|Signal name |HW Wire      |Action/Value|Description
|----|------------|-------------|------------|-----------
|31:6|-           |-            |-           |Reserved 0
|5:0 |decoy_dpram_max<br>_addr_rng_int |decoy_dpram_max<br>_addr_rng_int  |max is 64|Set max read address for rng dpram

<!-- |parameter                    |register name                | axil regs    | Description |
|-----------------------------|-----------------------------|--------------|--------------
|reg_enable_o                 |reg_enable_o                 |slv_reg0[0]   |Enable register update 
|tune_step_o                  |tune_step_o                  |slv_reg1[3:0] |Set tune step for decoy signal, 1 step is 1 period of 240MHz
|trigger_enstep_o             |trigger_enstep_o             |slv_reg2[0]   |trigger fine delay of master ODELAY3
|trigger_enstep_slv1_o        |trigger_enstep_slv1_o        |slv_reg2[1]   |trigger fine delay of slave1 ODELAY3
|trigger_enstep_slv2_o        |trigger_enstep_slv2_o        |slv_reg2[2]   |trigger fine delay of slave2 ODELAY3
|decoy_rng_mode_o             |decoy_rng_mode_o             |slv_reg3[0]   |Choose rng source. 0: from dpram, 1: from tRNG
|resolution		              |decoy_params_80_o[14:1] 		|slv_reg5[14:1]|Set length of fine delay step on master ODELAY3
|increase_en	              |decoy_params_80_o[0]			|slv_reg5[0]   |Set fine delay increase(1)/decrease(0) on master ODELAY3
|resolution_slv2              |decoy_params_slv_o[30:17] 	|slv_reg6[30:17]|Set length of fine delay step on slave 2 ODELAY3
|increase_en_slv2             |decoy_params_slv_o[16]		|slv_reg6[16]   |Set fine delay increase(1)/decrease(0) on slave 2 ODELAY3
|resolution_slv1              |decoy_params_slv_o[14:1] 	|slv_reg6[14:1] |Set length of fine delay step on slave 1 ODELAY3
|increase_en_slv1             |decoy_params_slv_o[0]		|slv_reg6[0]    |Set fine delay increase(1)/decrease(0) on slave 1 ODELAY3
|decoy_dpram_max<br>_addr_rng_int |decoy_dpram_max<br>_addr_rng_int |slv_reg7[5:0] |Set max read address for rng dpram -->

### Write to dpram from axil
Writing to dpram from axil registers.
- Base address: 0x0001_6000
- Dpram offset: 4096
- Write register(n) to dpram at: 0x0001_6000 + 4096 + 4*n
- Each register is 32 bits 

## Generate signal

These are the functions to generate the signal
```python,hidelines=~
def decoy_reset():
~    Write(0x00012000 + 20,0x01)
~    time.sleep(2)
~    Write(0x00012000 + 20,0x00)
```
Test_Decoy() function writing data for fake rng dpram and choosing rng mode.
- Max address for dpram is 64
- Rng mode : 0 for fake, 1 for tRNG
- Start decoy_rng.service to if choosing tRNG mode

```python,hidelines=~
def Test_Decoy():
~    #dpram_rng_max_addr
~    Write(0x00016000 + 28, 0x10)
~    #Write data to rng_dpram
~    Base_seq0 = 0x00016000 + 1024
~    rngseq0 = 0x00000031
~    rngseq1 = 0x00000002
~    Write(Base_seq0, rngseq0)
~    Write(Base_seq0+4, rngseq1)
~    #Write rng mode
~    Write(0x00016000 + 12, 0x0)
~    #enable regs values
~    Write(0x00016000 , 0x0)
~    Write(0x00016000 , 0x1)
```
 ![](pics/decoy_fifos.svg)

## Delays

Use these functions to add tune and fine delays for decoy signal. The principles is the same with TTL gate signal
- Tune step delay is 4.3ns, 8 steps
- Fine step delay is adjustable, maximum apro 1,4ns to 1,65ns for each master/slave 

```python,hidelines=~
def de_calculate_delay(fine, inc):
~    fine_clock_num = fine*16
~    transfer = fine_clock_num<<1|inc
~    transfer_bin = bin(transfer)
~    transfer_hex = hex(transfer)
~    return transfer_hex
```
```python,hidelines=~
def de_write_delay_master(tune, fine, inc):
~    #Write tune delay
~    Write(0x00016000 + 4, tune)
~    #Write fine delay master 
~    transfer = de_calculate_delay(fine, inc)
~    Write(0x00016000 + 20,transfer)
```
```python,hidelines=~
def de_write_delay_slaves(fine1, inc1, fine2, inc2):
~    Base_Add = 0x00016000 + 24
~    transfer = (fine2*16)<<17|inc2<<16|(fine1*16)<<1|inc1
~    Write(Base_Add, hex(transfer))
```
```python,hidelines=~
def de_params_en():
~    #enable regs values
~    Write(0x00016000 , 0x0)
~    Write(0x00016000 , 0x1)
```
```python,hidelines=~
def de_trigger_fine_master():
~    Base_Add = 0x00016000 + 8
~    Write(Base_Add, 0x0)
~    Write(Base_Add, 0x1)
~    time.sleep(0.02)
~    Write(Base_Add, 0x0)
~    print("Trigger master done")
```
```python,hidelines=~
def de_trigger_fine_slv1():
~    Base_Add = 0x00016000 + 8
~    Write(Base_Add, 0x0)
~    Write(Base_Add, 0x2)
~    time.sleep(0.02)
~    Write(Base_Add, 0x0)
~    print("Trigger slave1 done")
```
```python,hidelines=~
def de_trigger_fine_slv2():
~    Base_Add = 0x00016000 + 8
~    Write(Base_Add, 0x0)
~    Write(Base_Add, 0x4)
~    time.sleep(0.02)
~    Write(Base_Add, 0x0)
~    print("Trigger slave2 done")
```