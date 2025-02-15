from matplotlib.pyplot import *
from rtlsdr import RtlSdr
import numpy as np
import scipy.signal as signal
import peakdetect

real_center_freq = 7.032e6
offset = 200e3
margin = 10e3

sdr = RtlSdr()
sdr.set_direct_sampling(1)
sdr.sample_rate = 225001
sdr.center_freq = real_center_freq - offset
sdr.gain = 'auto'
num_samples = 256 * int(sdr.sample_rate / 256)

# samples = sdr.read_samples(num_samples)
samples = sdr.read_samples(num_samples)

power, psd_freq = psd(samples, NFFT=1024, Fs=sdr.sample_rate, Fc=real_center_freq)

power_db = 10*np.log10(power)
maxima, minima = peakdetect.peakdetect(power_db, psd_freq, delta=1)
for mx in maxima:
  f = mx[0]
  dBm = mx[1]
  print("Peak at", f, "of", dBm, "dB")
  # Was this peak anywhere near our target frequency?
  if f > real_center_freq-margin and f < real_center_freq+margin:
    print("We see a peak at", str(f))

sdr.close()
show()
