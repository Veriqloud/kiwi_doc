# Clock and reset management

## Clock tree
This is an overview of the clock distribution for Kiwi device. There are 3 clock sources:
- Source 100 MHz for PCIe comes from mother board of PC
- Source 100 MHz for DDR4 comes from oscilator on XEM8310 modules
- Source 10 MHz and PPS comes from White Rabbit Switch(WRS)

WRS 10 MHz is reference for PLL LTC6951 to generate clock pairs (sysref 3.125 MHz and refclk 200 MHz) for Fast DAC AD9152 and FPGA. PLL LTC6951 requires a SYNC signal to align all outputs to input, I use WRS PPS and 10 MHz to generate this signal, then the outputs will be aligned to PPS.

reflck 200 MHz is is the source clock for all logics in fpga, PPS is reference for synchronization       

![clock system](pics/clock_tree.svg)

## Module RTL
Purpose of this module:
- Manage the input clocks
- Generate the resets for other RTL modules
- Generate SYNC signal for clockchip on board Bread70

![module overview](pics/clk_rst_rtl.svg)

### Port descriptions
|Signals name         |Interface |Dir |Init status |Description
|---------------------|----------|----|------------|-----------
|fastdac_refclki_p/n  |cr_ext_cr |I   |200MHz      |input of jesd refclk from clockchip 
|fastdac_sysref_p/n   |cr_ext_cr |I   |3.125MHz    |input of jesd sysref from clockchip
|fastdac_syncout_p/n  |cr_ext_cr |I   |-           |input of jesd syncout from receiver 
|ext_clk10_p/n        |cr_ext_cr |I   |10MHz       |input of 10MHz from WRS
|ext_clk100_p/n       |cr_ext_cr |I   |100MHz      |input of 100MHz from clockchip 
|axil signals         |s_axil    |IO  |-           |standard axilite interface for r/w registers 
|s_axil_aclk          |Clock     |I   |15MHz       |clock for axil interface 
|sys_reset_n          |Reset     |I   |-           |system reset, active LOW
|clk_ddr_axi_i        |Clock     |I   |300MHz      |clock to generated from MMCM of DDR4 
|rst_ddr_axi_i        |Reset     |I   |-           |reset synced to clk_ddr_axi_i
|fastdac_gt_powergood_i|-        |I   |-           |powergood indicator of jesd204B core
|pps_i                |-         |I   |-           |PPS from WRS
|lclk_i               |Clock     |I   |-           |lclk domain of tdc module
|rstn_axil_o          |Reset     |O   |-           |Reset axil interface in others modules
|rstn_ddr_axi_o       |Reset     |O   |-           |Reset AXI interface of DDR4
|fastdac_refclk_o     |Clock     |O   |200MHz      |Refclk for QPLL in JESD204_PHY IP 
|fastdac_coreclk_o    |Clock     |O   |200MHz      |Clock for logic in 200MHz domain
|fastdac_corerst_o    |Reset     |O   |-           |Reset for fastdac core
|fastdac_sysref_o     |Clock     |O   |3.125MHz    |Sysref for jesd204b core 
|fastdac_syncout_o    |-         |O   |-           |syncout for jesd204b core
|clk10_o              |Clock     |O   |10MHz       |clk10 SE (single-ended)
|clk100_o             |Clock     |O   |100MHz      |clk100 SE
|sync_ltc_o           |Clock     |O   |2ms HIGH    |SYNC signal for clockchip output alignment  
|tdc_rst_o            |Reset     |O   |-           |Reset for tdc clock reset module
|lrst_o               |Reset     |O   |-           |Reset for tdc module in lclk domain
|ttl_rst              |Reset     |O   |-           |Reset for ttl_gate module
|decoy_rst            |Reset     |O   |-           |Reset for decoy module
|gc_rst_o             |Reset     |O   |-           |Reset for tdc module in clk200 domain
|ddr_data_rstn_o      |Reset     |O   |-           |Reset for ddr_data module

### User parameters
|Parameter           |Value     |Description
|--------------------|----------|------------
|C_S_Axil_Addr_Width |10        |Address width of axil interface
|C_S_Axil_Data_Width |32        |Address width of axil interface

### Axilite registers:
- Base Address: 0x0001_2000
- Offset address slv_reg(n) : 4*n
#### slv_reg0 - R/W Access - Trigger Control
|Bits|Signal name             |HW Wire       |Action/Value|Description
|----|------------------------|--------------|------------|-----------
|31:2|-                       |-             |-           |Reserved 0
|1   |clockchip_sync_o        |clockchip_sync|Pull LOW to HIGH|Send trigger to generate SYNC signal for external clockchip
|0   |fpga_turnkey_fastdac_rst_o|fpga_turnkey_fastdac_rst|Pull HIGH to LOW|Reset fastdac core, active HIGH

#### slv_reg1 - R/W Access - Trigger Control
|Bits|Signal name |HW Wire       |Action/Value|Description
|----|------------|--------------|------------|-----------
|31:2|-           |-             |-           |Reserved 0
|1   |tdc_rst_o   |tdc_rst       |Pull HIGH to LOW|Reset tdc clock management, active HIGH
|0   |lrst_o      |lrst_i        |Pull HIGH to LOW|Reset tdc module in lclk domain, active HIGH

#### slv_reg2 - R/W Access - Trigger Control
|Bits|Signal name |HW Wire       |Action/Value|Description
|----|------------|--------------|------------|-----------
|31:1|-           |-             |-           |Reserved 0
|0   |gc_rst_o    |gc_rst        |Pull HIGH to LOW|Reset tdc module in clk200 domain, active HIGH

#### slv_reg3 - R/W Access - Trigger Control
|Bits|Signal name |HW Wire       |Action/Value|Description
|----|------------|--------------|------------|-----------
|31:1|-           |-             |-           |Reserved 0
|0   |ttl_rst_o   |ttl_rst       |Pull HIGH to LOW|Reset ttl module, active HIGH

#### slv_reg4 - R/W Access - Trigger Control
|Bits|Signal name |HW Wire       |Action/Value|Description
|----|------------|--------------|------------|-----------
|31:1|-           |-             |-           |Reserved 0
|0   |ddr_data_rst|ddr_data_rst  |Pull HIGH to LOW|Reset ddr_data module, active HIGH

#### slv_reg5 - R/W Access - Trigger Control
|Bits|Signal name |HW Wire       |Action/Value|Description
|----|------------|--------------|------------|-----------
|31:1|-           |-             |-           |Reserved 0
|0   |decoy_rst_o	|decoy_rst     |Pull HIGH to LOW|Reset decoy module, active HIGH

#### slv_reg6 - R/W Access - Trigger Control
|Bits|Signal name    |HW Wire          |Action/Value|Description
|----|---------------|-----------------|------------|-----------
|31:1|-              |-                |-           |Reserved 0
|0   |ltc_sync_rst_o	|ltc_sync_rst     |Pull HIGH to LOW|Reset decoy module, active HIGH

### Generate SYNC signal for clockchip
After receiving sync trigger command from OS, FPGA detects rising edge of PPS and start counting to generate a 2ms pulse for clockchip (minimum is 1ms). Order of commands:
- Initialize clock chip : writing configuration registers
- Reset the sync counter
- Send the sync trigger
- FGPA should return the SYNC pulse for clock chip, the outputs of clock chip should be aligned to reference clock
- Each time there'a any change in configuration registers, new parameters is applied after SYNC

Note: This SYNC is different with SYNC on DDR
