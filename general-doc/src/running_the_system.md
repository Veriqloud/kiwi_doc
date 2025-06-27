# Running the System

## ssh setup

You need ssh access to Alice and Bob. 

Put this into your `~/.ssh/config`:

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
    ProxyCommand ssh vq nc ql001 22
    User vq-user
    IdentityFile ~/.ssh/your_ssh_key
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
        ControlMaster auto
        ControlPersist 1h

```

The last three entries are for connecting from the internet through the VQ server.

Ask someone to copy your ssh public key onto the machines. 


## Control the hardware


clone repo `git@github.com:Veriqloud/kiwi_hw_control.git`

ssh onto Alice and Bob and run the servers

```bash
cd ~/qline/server
hw.py &
hws.py & # first on Bob then on Alice
gc -c ../config/gc.json & # first on Bob then on Alice
```

on your personal computer go the the `kiwi_hw_control/qline_clean/local`. This is the folder from which you can initialize and calibrate the system. There are two programs:
- `hw_alice.py` / `hw_bob.py` to change and get the current hardware parameters (check their help messages)
- `hws.py` to calibrate the system, i.e. Alice and Bob at the same time. 

If you are lucky,

```.bash
hws.py --full_init  
```

is all you need. This might take up to two minutes. If you get a fail message, try again. If you get a fail message again, contact the admin:)

You can check with `qber` that the system is running fine:

On Bob
```.bash
qber -f ../config/qber.json 
```

On Alice
```.bash
qber -f ../config/qber_fifo_alice.json -n ../config/qber_net_alice.json 6400
```

This will print the correlation matrix and the qber. Some final commands:

```.bash
hw_alice.py set --fake_rng_seq [off, random]
hw_bob.py set --fake_rng_seq [off, random]
hw_alice.py set --insert_zeros on
hw_alice.py set --zero_pos 14
```







