from rtlsdr import RtlSdr

real_center_freq = 7.032e6
offset = 200e3

sdr = RtlSdr()
sdr.set_direct_sampling(1)
sdr.sample_rate = 225001
sdr.center_freq = real_center_freq - offset
sdr.gain = 'auto'
num_samples = 256 * int(sdr.sample_rate / 256)

print(num_samples)

print(len(sdr.read_samples(num_samples)))
sdr.close()
