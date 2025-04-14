# Calibration


When the system is turned on, we start with some default parameters (from config/defaults.txt). Some of them will be fine straight away but some might need to be updated. Generally, we are going to run some scripts controlled by `client_ctl.py` on Alice to find correct parameters. The general steps are the following:

## Init

Initialize devices controlled by the FPGA (clock chip, DAC, TDC, etc...) and modules in the FPGA.

## Am bias

Determine the bias voltage value for the amplitude modulator to be in blocking mode. This a simple algorith looking at SPD counts and changing the voltage.


## Polarization 

Use the polarization controller to maximize counts

## Find single peak

Alice sends a single pulse every n cycles. Bob measures the timestamps, makes an arrival-time histogram and calculates the delay between him and Alice modulo the time difference between the single pulses. This allows Bob to switch to gated mode and interpret arrival times as measurement results 0 or 1.

## Find shift 

The phase modulator needs to produce a signal that is fine aligned in time to the qubit double pulse. To find that fine delay, we put a sequence on the phase modulator and take data for a range of fine shifts. We then make histograms and look for the fine shift where the modulation of the qubit was the strongest. 

## Find delay

The coarse delay between Alice and Bob (in units of qubit distance) is found using the phase modulator. We do this in two steps. First we put a sequce of periodicity 80, where one qubit is different from the rest. We find that particular qubit to get the distance modulo 80. We then put a sequence of 80*400, where 80 consecutive qubits are different from the rest, find those 80 qubits and have thus determined the absolute distance between Alice and Bob.

## Find zeros

Every 16 pulses zero-angle states are send and used to feedback the offset value for the Bob's phase modulator. To find the proper position to insert these states, we run the following routine: we send a state that yields unbalanced clicks everywhere and change the insert_zeros_position parameter. When we hit the right value, we see the expected unbalanced. 







