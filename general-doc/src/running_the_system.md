# Running the System

## Basic admin controlling a configured system (no ssh to the system requred)

Clone repo `git@github.com:Veriqloud/kiwi_hw_control.git`

Power on the system

- power on the White Rabbit Switches, wait about 20sec for lights to flash 
- power on the VQ box, this will power on the FPGA board 
- power on the computer by pressing the button on the back of the box (or wakeonlan over the netowk)


Point the scripts to the appropriate `network.json`

```.bash
export QLINE_CONFIG_DIR=path_to/kiwi_hw_control/config/qline1
```

Go to `kiwi_hw_control/qline_clean/local`. This is the folder from which you can initialize and calibrate the system. There are three programs:
- `hw_alice.py` / `hw_bob.py` to change and get the current hardware parameters (check their help messages)
- `hws.py` to calibrate the system, i.e. Alice and Bob at the same time. 
- `mon.py` to get the status and plot counts or gates

Run 

```.bash
mon.py --status
``` 

to get basic info on the system

If you are lucky,

```.bash
hws.py --full_init  
```

is all you need. This might take up to two minutes. If you get a fail message, try again. 





## ssh setup (required for development, deployment and debugging)

Put something like this into your `~/.ssh/config`:

```
Host Alice
    HostName ql001.home
    User vq-user
    IdentityFile ~/.ssh/your_ssh_key
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 1h

Host Bob
    HostName ql002.home
    User vq-user
    IdentityFile ~/.ssh/your_ssh_key
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 1h

Host vq
    HostName veriqloud.pro.dns-orange.fr
    User vq-user
    IdentityFile ~/.ssh/your_ssh_key
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
        ControlMaster auto
        ControlPersist 1h

Host RemoteAlice
    ProxyCommand ssh vq nc ql001 22
    User vq-user
    IdentityFile ~/.ssh/your_ssh_key
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
        ControlMaster auto
        ControlPersist 1h

Host RemoteBob
    ProxyCommand ssh vq nc ql002 22
    User vq-user
    IdentityFile ~/.ssh/your_ssh_key
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
        ControlMaster auto
        ControlPersist 1h

```

The last three entries are for connecting from the internet through port forwarding on the VQ server.

Make sure your public key is on the machines, e.g. `ssh-copy-id vq-user@ql001.home`


## Manually optimizing the qber

ssh on the systems

You can check with `qber` that the system is running fine:

On Bob
```.bash
cd servers
qber 
```

On Alice
```.bash
qber 6400
```

This will print the correlation matrix of the relative count rates for all the 4x4 possible angle choices.

On your local machine run `hw_alice.py` and `hw_bob.py` to change parameters.

## Misc


```.bash
hw_alice.py set --fake_rng_seq [off, random]
hw_bob.py set --fake_rng_seq [off, random]
hw_alice.py set --insert_zeros on
hw_alice.py set --zero_pos 14
```







