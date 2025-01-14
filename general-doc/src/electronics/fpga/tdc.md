# TDC

We use AS6501 TDC(Time to Digital Converter) chip to convert arriving time of q-bit to digital data. All modules and IP manage in/out signals from TDC are grouped under block tdc:

![overview](pics/tdc.png)	
## clk_rst_buffer
- OLVDS_TDC.v, ILVDS_TDC.v: buffer for differential output and input signals,clocks
- tdc_clk_rst_mngt.v : generate refclk 5MHz, rstindex for TDC; generate simulated STOPA signal for TDC
## time_spi
- Quad AXI spi: IP of AMD, manage to transfer data from AXI bus to spi bus
- spi_inout_mngt.v: mananage inout pins from quad AXI spi to physical spi pins
## system_ila_tdc 
ILA debug core, probes signals under tdc blocks
## tdc_mngt
- AS6501_IF.v: manages digital data from TDC, output tdc time/global counter/click result depends on axil commands
- TDC_REG_MNGT_v1_0.v: manages axilite registers
- fifo_gc_tdc_rtl.v: instantiates fifo_gc_tdc, this fifo is axistream fifo. Instantiate axistream fifo in an RTL module allows to modify FREQ_HZ parameter of axistream interface when rebuild the block design

### Axil registers
|signals in modules		    			|signals		            |Dir|axil registers	| offset address (dec) |
|---------------------------------------|---------------------------|---|---------------|----------------------|
|AS6501_IF_0/enable 		 			|tdc_enable					|O	|slv_reg0[0]	|0
|AS6501_IF_0/index_stop_bitwise_i		|tdc_index_stop_bitwise_o	|O	|slv_reg1[15:0]	|4
|AS6501_IF_0/start_gc_i					|start_gc_sim				|O	|slv_reg2[0]	|8
|tdc_clk_rst_mngt_0/stopa_sim_limit_i	|stopa_sim_limit			|O	|slv_reg3[31:0]	|12
|AS6501_IF_0/gate0_i					|gate0_o					|O	|slv_reg4[31:0]	|16
|AS6501_IF_0/gate1_i					|gate1_o 					|O	|slv_reg5[31:0]	|20
|AS6501_IF_0/shift_tdc_time_i			|shift_tdc_time_o			|O	|slv_reg6[15:0]	|24
|AS6501_IF_0/start_gc_i					|shift_gc_back_o			|O	|slv_reg7[15:0]	|28
|AS6501_IF_0/command_i					|tdc_command_o				|O	|slv_reg8[2:0]	|32
|AS6501_IF_0/reg_enable_tdc_i			|tdc_reg_enable_o			|O	|slv_reg9[0]	|36
|AS6501_IF_0/reg_enable200_i			|tdc_reg_enable200_o		|O	|slv_reg9[1]	|36
|tdc_clk_rst_mngt_0/stopa_sim_enable_i	|stopa_sim_enable_o			|O	|slv_reg9[2]	|36
|AS6501_IF_0/command_enable				|tdc_command_enable_o		|O	|slv_reg10[0]	|40
|unused									|tdc_command_get_gc_o		|O	|slv_reg11[0]	|44
|AS6501_IF_0/total_count_o				|total_count_i				|I	|slv_reg16[31:0]|64
|AS6501_IF_0/click0_count_o				|click0_count_i				|I	|slv_reg15[31:0]|60
|AS6501_IF_0/click1_count_o				|click1_count_i				|I	|slv_reg14[31:0]|56

### Data flow
Picture below shows an overview how data flows through modules and xdma channels. Responses to commands are written in modules AS6501_IF.v

![tdc data flow](pics/tdc_data_flow.png)
### Software control functions
Setting registers used in state machine under clk200
```python,hidelines=~
def Time_Calib_Reg(command,t0, gc_back, gate0, width0, gate1, width1):
~    BaseAddr = 0x00000000
~    Write(BaseAddr + 16,hex(int(width0<<24 | gate0))) #gate0
~    Write(BaseAddr + 20,hex(int(width1<<24 | gate1))) #gate1
~    Write(BaseAddr + 24,hex(int(t0))) #shift tdc time = 0
~    Write(BaseAddr + 28,hex(int(gc_back))) #shift gc back = 0
~    Write(BaseAddr + 32,hex(int(command))) #command = 1: raw | =2: with gate
~    Write(BaseAddr + 36,0x0)
~    Write(BaseAddr + 36,0x2)# turn bit[1] to high to enable register setting
```
Initialize tdc module, global counter in tdc module is local, it means it's available in Bob only for calibration purpose. There are 2 state machines in tdc module:

- state machine under lclk_i: Config_Tdc() sets registers and enable this state machine, output digital data in FPGA 
- state machine under clk200: Reset_gc() and Start_gc() send command to reset and start global counter

```python,hidelines=~
def Time_Calib_Init():
~    Config_Tdc() #Get digital data from TDC chip
~    Reset_gc() #Reset global counter
~    Start_gc() #Global counter start counting at the next PPS
```
Get detection result, function Get_Stream() includes reset fifo_gc_tdc and read data from xdma0_c2h_*.
```python,hidelines=~
def Cont_Det(): 
~    num_data = 2000
~    Get_Stream(0x00000000+40,'/dev/xdma0_c2h_2','data/tdc/output_dp.bin',num_data)
~    command ="test_tdc/tdc_bin2txt data/tdc/output_dp.bin data/tdc/histogram_dp.txt"
~    s = subprocess.check_call(command, shell = True)
~
~    time_gc = np.loadtxt("data/tdc/histogram_dp.txt",usecols=(1,2),unpack=True)
~    int_time_gc = time_gc.astype(np.int64)
~    duration = (max(int_time_gc[1])-min(int_time_gc[1]))*25
~    click_rate = np.around(num_data/(duration*0.000000001),decimals=4)
~    print("Number of count: ", str(len(int_time_gc[1])))
~    print("Appro click rate: ", str(click_rate), "click/s")

```