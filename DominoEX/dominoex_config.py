from dominoex import DOMINOEX
from radio import Radio
from time import sleep_ms, sleep

class DominoEXConfig:
  def __init__(self, baud, frq, call, location): 
    self.dds = Radio()

    self.is_beacon = False
    self.beacon_interval = 30.0
    self.message = ""
    self.usb_offset = 1350.0
    self.num_tones = 18
    self.incremental_tone = 0.0
    self.all_done = False

    self.r = DOMINOEX(self.send_tone, self.report_all_done)
    self.set_baud(baud)

    self.frequency = frq
    self.call = call
    self.location = location
    
    self.r.set_frequency(frq)
    self.r.set_call(call)
    self.r.set_location(location)

  def get_radio(self):
    return self.dss

  def send_code(self):
    self.dds.send()

  def send_tone(self, tone):
    self.incremental_tone = (self.incremental_tone + float(tone) + 2) % self.num_tones
    self.f = int(int(self.frequency) + self.usb_offset + (self.incremental_tone + 0.5) * self.tone_spacing - self.bandwidth / 2.0)
    self.dds.set_freq(0, self.f)
    self.dds.send()

  def report_all_done(self):
    print()
    print("All done!")
    self.all_done = True

    if self.is_beacon:
      self.r.stop()              # stop sending bits
      # self.dds.off()
      sleep(float(self.beacon_interval))
      self.dds.on()
      self.r.send_code()         # Repeat for a beacon
    else:
      self.r.stop()              # stop sending bits
      # self.dds.off()

  def set_baud(self, b):
    self.baud = b

    if self.baud == 2:
      self.spaced = 1
      self.sample_rate = 8000.0
      self.symbol_length = 4000.0
    elif self.baud == 4:
      self.spaced = 2
      self.sample_rate = 8000.0
      self.symbol_length = 2048.0
    elif self.baud == 5:
      self.spaced = 2
      self.sample_rate = 11025.0
      self.symbol_length = 2048.0
    elif self.baud == 8:
      self.spaced = 2
      self.sample_rate = 8000.0
      self.symbol_length = 1024.0
    elif self.baud == 11:
      self.spaced = 1
      self.sample_rate = 11025.0
      self.symbol_length = 1024.0
    elif self.baud == 16:
      self.spaced = 1
      self.sample_rate = 8000.0
      self.symbol_length = 512.0
    elif self.baud == 22:
      self.spaced = 1
      self.sample_rate = 11025.0
      self.symbol_length = 512.0
    elif self.baud == 44:
      self.spaced = 2
      self.sample_rate = 11025.0
      self.symbol_length = 256.0
    elif self.baud == 88:
      self.spaced = 1
      self.sample_rate = 11025.0
      self.symbol_length = 128.0

    self.r.set_baud(self.sample_rate / self.symbol_length)
    self.r.set_bit_length(1000 / (self.sample_rate / self.symbol_length))
    self.tone_spacing = self.sample_rate * self.spaced / self.symbol_length
    self.bandwidth = self.num_tones * self.tone_spacing

  def set_message(self, msg):
    self.r.set_message(chr(0) + "\r" + msg + "\r")

    self.dds.on()
    self.r.send_code()
    self.all_done = False

    print("Frequency:", self.frequency)
    print("Baud:", self.baud)
    print("Beacon?:", self.is_beacon)
    print("Message:", self.r.message)

    print()
    print("Bandwidth:", self.bandwidth)
    print("Tone spacing:", self.tone_spacing)
    print("Symbol length:", self.symbol_length)
    print("Bit length:", 1000 / (self.sample_rate / self.symbol_length))
    print("Baud:", self.sample_rate / self.symbol_length)

  def set_beacon(self, onoff, interval):
    self.is_beacon = onoff
    self.beacon_interval = interval