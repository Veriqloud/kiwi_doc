import matplotlib.pylab as plt, numpy as np

def h(x):
    return -x*np.log2(x) - (1-x)*np.log2(1-x)

#qber = np.arange(0, 0.12, 0.001)



d = np.arange(0, 26, 0.01) # dB

loss_bob = 17.2 # dB

loss = 10**(-d/10 - loss_bob/10 )

discarded = 4 # basis * useless peaks
clicks = 80e6 * loss / discarded 

clicks[clicks> 25e3] = 25e3


qber = 0.04 + 100/clicks
qber[qber>0.5] = 0.5

k = (1 - 2*h(qber)) * clicks
#k_theo = 80e6 * 10**(-d/10) / 2


ex_loss = [11, 23]
ex_keyrate = [11e3, 300]


plt.figure(figsize=(5,3))
#plt.plot(d, clicks, label="clicks")
plt.plot(d, k, label="estimate")
plt.plot(ex_loss, ex_keyrate, linestyle='none', marker='x', label="deployed at DT\nBerlin Testbed")
#plt.plot(d, k_theo, linestyle="dashed", color="black", label="ideal")
plt.yscale("log")
plt.ylim((100, 20e3))
plt.xlabel("channel loss [dB]")
plt.ylabel("key rate [bit/s]")
plt.legend()
plt.savefig("key_vs_distance.png", dpi=70, bbox_inches="tight")
plt.show()

