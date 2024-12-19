# Optics


## Alice

## Bob 

## Laser

The system runs well with a non-tunable CW laser with 100kHz bandwidth and center wavelength at around 1550nm. 

The center wavelength depends on the components chosen: the beam splitters in the interferometer, optical filter, modulators. We tested the system between 1530nm and 1570nm. The qber went up slightly from 4% at 1550nm to 6% at 1530nm and 1565nm. 

The bandwidth must be small enough to interfere with high visility on the unbalanced Mach-Zehnder interferometer. We can roughly estimate the qber contribution as $1 - \exp(-\tau/\tau_c)$, where $\tau_c$ is the coherence time and $\tau$ the delay of the Mach-Zehnder.

The stability of the laser must be good enough to allow phase stabilization of the Mach-Zehnder interferometer (which is done based on SPD counts, which is slow). As a rule of thumb, a pi phasedrift of the Mach-Zehnder interferometer should be of the order of 1s or slower. This is fine for thermal drifts. However, if the laser is tunable, it will often actively tune the center wavelength. We tested two tunable lasers. Only one of them worked in it's ultra-narrow linewidth mode: The RIO COLORADO Widely Tunable 1550nm Narrow Linewidth Laser Source.


## Detector 

The detector is a crutial component of the system. It limits the key rate on the low-loss side becaus there is a maximum count rate. It limits the maximum distance because it has dark counts. For InGaAs SPDs, the afterpulses increase the qber. 

We use the Aurea OEM module in gated mode. Additionally we apply software filters around the peaks to reduce background as much as possible. We set the dead time to around 20us. Interestingly, we noticed that changing the detection efficiency setting between 10% and 20% yield similar key rates. Even though the count rates are higher at a higher detection efficiency, the qber also goes up and/or the dead time needs to be increased. 










