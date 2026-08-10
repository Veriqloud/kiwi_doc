# True RNG
## tRNG
To generate random number for QKD, we use SwiftRNG Pro from TectroLabs. [Documentation](https://tectrolabs.com/swiftrng-pro/) for device is available on website of TectroLabs.

Picture below show you the path of random bytes. We have a small API sends "x" command to SwiftRNG Pro, the device returns 16000 bytes of random data. Then data is sent through PCIe to FPGA using axistream protocol.

There are 2 channels using true RNG data. One channel is for PM angles encoding in fastdac_transport.v and one channel is for AM angle encoding decoy state in decoy_rng_fifos.v 

## 
![rng data flow](pics/rng_flow.svg)

