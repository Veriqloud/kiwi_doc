# TTL gate
Purpose of this module:
- Generate gate signal for SPD, level TTL 3.3V out of FPGA (level is converted on Bread70 for SPD)
- Duty cycle > 5ns
- Delay full range 12.5ns, fine delay in 100ps step

![](pics/ttl_gate.png)

## Port descriptions

|Signals name         |Interface |Dir |Init status |Description
|---------------------|----------|----|------------|-----------
|axil signals         |s_axil    |IO  |-           |standard axilite interface for r/w registers 
|s_axil_aclk          |Clock     |I   |15MHz       |clock for axil interface 
|s_axil_aresetn       |Reset     |I   |-           |reset for axil interface, active LOW
|clk240               |Clock     |I   |240MHz      |clock to generate gate signal 
|clk80                |Clock     |I   |80MHz       |clock for fine delay this gate signal
|pps_i                |-         |I   |-           |PPS from WRS
|ttl_rst              |Reset     |I   |-           |reset for logic, active HIGH
|pulse_n/p            |-         |O   |-           |output to pins
|pulse_rep_n/p        |-         |O   |-           |output to pins, without fine delay

## User parameters

|Parameter           |Value     |Description
|--------------------|----------|------------
|C_S_Axil_Addr_Width |8         |Address width of axil interface
|C_S_Axil_Data_Width |32        |Address width of axil interface
|DELAY FORMAT        |COUNT     |Delay format for ODELAY3
|DELAY TYPE          |VARIABLE  |Delay type for ODELAY3
|DELAY VALUE         |50        |need to be between 45-65 taps for IDELAY3 calibrates correctly
|REFCLK FRE          |300       |refclk for IDELAY3 and ODELAY3, default
|UPDATE MODE         |ASYNC     |update by logic control


## Axil registers
- Base address: 0x0001_5000
- Offset address slv_reg(n) : 4*n
### slv_reg0 - R/W Access - Trigger Control
|Bits|Signal name             |HW Wire      |Action/Value|Description
|----|------------------------|-------------|------------|-----------
|31:1|-                       |-            |-           |Reserved 0
|0   |ttl_trigger_enstep_o    |en_step      |pull 0-1-0.Stay HIGH long enough<br>coresponding resolution |trigger fine delay master
 
For example: 
- Set fine delay tapes = 500 in software
- Resolution = 500*16 = 8000 (80MHz periods) = 0.1ms
- Trigger should stay HIGH longer than 0.1ms

This works the same for slave 1 and slave 2 cascaded to master
### slv_reg1 - R/W Access - Configuration
|Bits |Signal name     |HW Wire             |Action/Value|Description
|-----|----------------|--------------------|------------|-
|31:23|-               |-                   ||Reserved 0
|22:19|ttl_params_o    |duty_val            ||Set duty cycle width, 1 step is 1 period of 240MHz
|18:15|ttl_params_o    |delay_val           ||Set tune step, 1 step is 1 period of 240MHz
|14:1 |ttl_params_o    |resolution          |max is 8192|Set length of fine delay step on master ODELAY3
|0    |ttl_params_o    |increase_en         |1: increase<br>0: decrease|Set fine delay direction on master ODELAY3

The resolution is in unit of [80MHz period]
- Maximum fine delay tap: 512
- Require 16 clk cycles for each tap
- Resolution = 512*16 = 8192

### slv_reg2 - R/W Access - Trigger Control
|Bits|Signal name             |HW Wire      |Action/Value|Description
|----|------------------------|-------------|------------|-----------
|31:1|-                       |-            |-           |Reserved 0
|0   |ttl_params_en_o|ttl_params_en_o       |pull 0-1    |Enable register update

### slv_reg3 - R/W Access - Configuration
|Bits |Signal name         |HW Wire             |Action/Value |Description
|-----|--------------------|--------------------|------------|-
|31   |-                   |-                   ||Reserved 0
|30:17|ttl_params_slv_o    |resolution_slv2     |max is 8192|Set length of fine delay step on slave 2 ODELAY3
|16   |ttl_params_slv_o    |increase_en_slv2    |1: increase<br>0: decrease|Set fine delay direction on slave 2 ODELAY3
|14:1 |ttl_params_slv_o    |resolution_slv1     |max is 8192|Set length of fine delay step on slave 1 ODELAY3
|0    |ttl_params_slv_o    |increase_en_slv1    |1: increase<br>0: decrease|Set fine delay direction on slave 1 ODELAY3

### slv_reg4 - R/W Access - Trigger Control
|Bits|Signal name             |HW Wire      |Action/Value|Description
|----|------------------------|-------------|------------|-----------
|31:1|-                       |-            |-           |Reserved 0
|0   |ttl_trigger_enstep_slv1_o|en_step_slv1|pull 0-1-0.Stay HIGH long enough<br>coresponding resolution |trigger fine delay slave 1

### slv_reg5 - R/W Access - Trigger Control
|Bits|Signal name             |HW Wire      |Action/Value|Description
|----|------------------------|-------------|------------|-----------
|31:1|-                       |-            |-           |Reserved 0
|0   |ttl_trigger_enstep_slv2_o|en_step_slv2|pull 0-1-0.Stay HIGH long enough<br>coresponding resolution |trigger fine delay slave 2


<!-- |signal name    |register name                  | Axil regs     | Description
|---------------|-------------------------------|---------------|--------------
|en_step   		|ttl_trigger_enstep_o[0]		|slv_reg0[0]    |trigger fine delay master
|en_step_slv1   |ttl_trigger_enstep_slv1_o[0]	|slv_reg4[0]    |trigger fine delay slave 1
|en_step_slv2   |ttl_trigger_enstep_slv2_o[0]	|slv_reg5[0]    |trigger fine delay slave 2
|duty_val		|ttl_params_o[22:19]			|slv_reg1[22:19]|Set duty cycle width, 1 step is 1 period of 240MHz
|delay_val		|ttl_params_o[18:15]			|slv_reg1[18:15]|Set tune step, 1 step is 1 period of 240MHz
|resolution		|ttl_params_o[14:1] 			|slv_reg1[14:1] |Set length of fine delay step on master ODELAY3
|increase_en	|ttl_params_o[0]				|slv_reg1[0]    |Set fine delay increase(1)/decrease(0) on master ODELAY3
|resolution_slv2|ttl_params_slv_o[30:17] 		|slv_reg3[30:17]|Set length of fine delay step on slave 2 ODELAY3
|increase_en_slv2|ttl_params_slv_o[16]			|slv_reg3[16]   |Set fine delay increase(1)/decrease(0) on slave 2 ODELAY3
|resolution_slv1|ttl_params_slv_o[14:1] 		|slv_reg3[14:1] |Set length of fine delay step on slave 1 ODELAY3
|increase_en_slv1|ttl_params_slv_o[0]			|slv_reg3[0]    |Set fine delay increase(1)/decrease(0) on slave 1 ODELAY3
|ttl_params_en_o|ttl_params_en_o[0]				|slv_reg2[0]    |Enable register update -->

## Software control
### Generate signal
- Clock domain: 240 MHz
- Trigger PPS and align the pulse to PPS
- Change duty and tune delay the pulse with duty_val and delay_val
- Output will be fed into fine delay

These are the base functions allow to set registers, generate signal, change duty cycle and tune delay  
```python,hidelines=~
def ttl_reset():
~    Write(0x0001200c,0x01)
~    Write(0x0001200c,0x00)
~    time.sleep(2)
```
```python,hidelines=~
def calculate_delay(duty, tune, fine, inc):
~    fine_clock_num = fine*16
~    transfer = duty<<19|tune<<15|fine_clock_num<<1|inc
~    transfer_bin = bin(transfer)
~    transfer_hex = hex(transfer)
~    return transfer_hex
```
```python,hidelines=~
def write_delay_master(duty, tune, fine, inc):
~    Base_Add = 0x00015004 
~    transfer = calculate_delay(duty, tune, fine, inc)
~    Write(Base_Add,transfer)
```
```python,hidelines=~
def write_delay_slaves(fine1, inc1, fine2, inc2):
~    Base_Add = 0x0001500c
~    transfer = (fine2*16)<<17|inc2<<16|(fine1*16)<<1|inc1
~    Write(Base_Add, hex(transfer))
```
```python,hidelines=~
def params_en():
~    Base_Add = 0x0015008
~    Write(Base_Add,0x00)
~    Write(Base_Add,0x01)
```

### Fine delay
AMD support ODELAYE3 primitives to delay a signal in ps step, full range is 1,25ns. Read [UG974](https://docs.amd.com/v/u/2017.1-English/ug974-vivado-ultrascale-libraries) and [UG571](https://docs.amd.com/r/en-US/ug571-ultrascale-selectio/VAR_LOAD-Mode?tocId=6Pvw1KYIWoLfYxO5WATjSQ) for more details

Tune delay step is around 4,16ns. So, I choose Cascade configuration for ODELAYE3
- DELAY_FORMAT = COUNT
- DELAY_TYPE = VARIABLE
- UPDATE_MODE = ASYNC

Trigger the fine delay on master and 2 slaves, every trigger will shift your signal fine [taps] set in write_delay_* function
```python,hidelines=~
def trigger_fine_master():
~    Base_Add = 0x00015000
~    Write(Base_Add, 0x0)
~    Write(Base_Add, 0x1)
~    time.sleep(0.02)
~    Write(Base_Add, 0x0)
~    print("Trigger master done")
```
```python,hidelines=~
def trigger_fine_slv1():
~    Base_Add = 0x00015000
~    Write(Base_Add + 16, 0x0)
~    Write(Base_Add + 16, 0x1)
~    time.sleep(0.02)
~    Write(Base_Add + 16, 0x0)
~    print("Trigger slave1 done")
```
```python,hidelines=~
def trigger_fine_slv2():
~    Base_Add = 0x00015000
~    Write(Base_Add + 20, 0x0)
~    Write(Base_Add + 20, 0x1)
~    time.sleep(0.02)
~    Write(Base_Add + 20, 0x0)
~    print("Trigger slave2 done")
```