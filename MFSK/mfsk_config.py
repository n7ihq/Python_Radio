from mfsk import MFSK
from time import sleep_ms, sleep

from radio import Radio

class MfskProcess:
  def __init__(self, pin, frequency, baud, message, call, location):
    from machine import Timer
    
    self.osc = Radio()    
    self.radio_timer = Timer()
    self.old_tone = -1
    self.baud = baud
    self.usb_offset = 1133
    self.frequency = frequency
    self.message = message

    self.r = MFSK(self.radio_timer, self.send_tone)
    self.r.stop()
    self.r.set_call(call)
    self.r.set_location(location)
    self.r.set_frequency(frequency)
    self.r.set_message(message)

    if self.baud == 4:                    # 3.90625 baud
      self.r.samplerate = 8000.0
      self.r.symlen = 2048.0
      self.r.symbits = 5
      self.r.depth = 5
      self.r.basetone = 256
      self.r.numtones = 32
      self.r.preamble = 107
    elif self.baud == 8:                  # 7.8125 baud
      self.r.samplerate = 8000.0
      self.r.symlen = 1024.0
      self.r.symbits = 5
      self.r.depth = 5
      self.r.basetone = 128
      self.r.numtones = 32
      self.r.preamble = 107
    elif self.baud == 11:                 # 10.7666015625 baud
      self.r.samplerate = 11025.0
      self.r.symlen = 1024.0
      self.r.symbits = 4
      self.r.depth = 10
      self.r.basetone = 93
      self.r.numtones = 16
      self.r.preamble = 107
    elif self.baud == 16:                 # 15.625 baud
      self.r.samplerate = 8000.0
      self.r.symlen = 512.0
      self.r.symbits = 4
      self.r.depth = 10
      self.r.basetone = 64
      self.r.numtones = 16
      self.r.preamble = 107
    elif self.baud == 22:                 # 21.533203125 baud
      self.r.samplerate = 11025.0
      self.r.symlen = 512.0
      self.r.symbits = 4
      self.r.depth = 10
      self.r.basetone = 46
      self.r.numtones = 16
      self.r.preamble = 107
    elif self.baud == 31:                 # 31.25 baud
      self.r.samplerate = 8000.0
      self.r.symlen = 256.0
      self.r.symbits = 3
      self.r.depth = 10
      self.r.basetone = 32
      self.r.numtones = 8
      self.r.preamble = 107
    elif self.baud == 32:                 # 31.25 baud
      self.r.samplerate = 8000.0
      self.r.symlen = 256.0
      self.r.symbits = 4
      self.r.depth = 10
      self.r.basetone = 32
      self.r.numtones = 16
      self.r.preamble = 107
    elif self.baud == 64:                 # 62.5 baud
      self.r.samplerate = 8000.0
      self.r.symlen = 128.0
      self.r.symbits = 4
      self.r.depth = 10
      self.r.basetone = 16
      self.r.numtones = 16
      self.r.preamble = 180
    elif self.baud == 128:                # 125 baud
      self.r.samplerate = 8000.0
      self.r.symlen = 64.0
      self.r.symbits = 4
      self.r.depth = 20
      self.r.basetone = 8
      self.r.numtones = 16
      self.r.preamble = 214

    self.r.tonespacing = self.r.samplerate / self.r.symlen

    print("Frequency:", self.frequency)
    print("Message:", self.message)
 
    print("Symbits is", self.r.symbits)
    print("Depth is", self.r.depth)
    print("Bandwidth is", (self.r.numtones - 1) * self.r.tonespacing)
    print("Symbol length is", self.r.symlen)
    print("Baud is", self.r.samplerate / self.r.symlen)
    print("Tonespacing is", str(self.r.tonespacing) + ":")
    self.send_code()

  def get_radio(self):
    return self.osc

  def set_message(self, msg):
    self.message = msg
    
  def send_code(self):
    self.f = float(self.r.basetone + float(self.frequency) + self.usb_offset)
    self.osc.set_freq(0, self.f)

    start_of_transmission_length = int(8 * (1000 / (self.r.samplerate / self.r.symlen)))
    sleep_ms(start_of_transmission_length)
    self.r.send_code()

  def send_tone(self, tone):
    if tone != self.old_tone:
      f = float(float(self.frequency) + self.usb_offset + float(tone))
      self.osc.set_freq(0, f)
    self.old_tone = tone