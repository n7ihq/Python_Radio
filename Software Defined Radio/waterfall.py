import matplotlib.animation as animation
from matplotlib.mlab import psd
import pylab as pyl
import numpy as np
import sys
from rtlsdr import RtlSdr

NFFT = 1024*4
NUM_SAMPLES_PER_SCAN = NFFT*4
NUM_BUFFERED_SWEEPS = 100

class Waterfall(object):
    keyboard_buffer = []
    shift_key_down = False
    image_buffer = -100*np.ones((NUM_BUFFERED_SWEEPS, NFFT))

    def __init__(self, sdr):
        self.fig = pyl.figure()
        self.sdr = sdr
        self.init_plot()

    def init_plot(self):
        self.ax = self.fig.add_subplot(1,1,1)
        self.image = self.ax.imshow(self.image_buffer,
          aspect='auto', interpolation='nearest', vmin=-50, vmax=10)
        self.ax.set_xlabel('Current frequency (MHz)')
        self.ax.get_yaxis().set_visible(False)

    def update_plot_labels(self):
        fc = self.sdr.fc
        rs = self.sdr.rs

        freq_range = (fc - rs/2)/1e6, (fc + rs*(0.5))/1e6

        self.image.set_extent(freq_range + (0, 1))
        self.fig.canvas.draw_idle()

    def update(self, *args):
        start_fc = self.sdr.fc

        self.image_buffer = np.roll(self.image_buffer, 1, axis=0)

        for scan_num, start_ind in enumerate(range(0, NFFT, NFFT)):
            self.sdr.fc += self.sdr.rs*scan_num
            samples = self.sdr.read_samples(NUM_SAMPLES_PER_SCAN)
            psd_scan, f = psd(samples, NFFT=NFFT)
            pwr = 10 * (np.log2(psd_scan)/np.log2(8))
            self.image_buffer[0, start_ind: start_ind+NFFT] = pwr

        self.image.set_array(self.image_buffer)
        self.sdr.fc = start_fc

        return self.image,

    def start(self):
        self.update_plot_labels()
        ani = animation.FuncAnimation(self.fig, self.update, interval=50, save_count=64*1024, blit=True)
        pyl.show()
        return

def main():
    sdr = RtlSdr()
    wf = Waterfall(sdr)

    sdr.rs = 1.0e6
    sdr.fc = 28000000
    sdr.gain = 'auto'

    wf.start()

    sdr.close()

if __name__ == '__main__':
    main()
