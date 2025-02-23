from fsq import FSQ
from time import sleep
from radio import Radio

class FSQConfig:

  def __init__(self, frq, baud, call, location):
    self.frequency = frq
    self.baud = baud
    self.mycall = call
    self.location = location

    self.r = FSQ(self.send_tone, self.baud, self.all_done)
    self.dds = Radio()
    self.dds.send()

    self.is_beacon = False
    self.message = ""
    self.spacing = 8.7890625                 # 8.7890625 Hz
    self.usb_offset = 1350.0
    self.is_directed = False
    self.tocall = "N0CALL"
    self.beacon_interval = 60.0
    self.incremental_tone = 0.0

    self.r.set_frequency(self.frequency)
    self.r.set_call(self.mycall)
    self.r.set_location(self.location)
    self.r.set_call(self.mycall)
    self.r.set_location(self.location)

    print("Frequency:", self.frequency)
    print("Baud:", self.baud)
    print("Beacon?:", self.is_beacon)
    print("Directed?:", self.is_directed)
    print("To callsign:", self.tocall)

  def get_radio():
    return dss

  def set_message(self, msg):
    self.message = msg.format(self.mycall, self.location)

    self.all_done = False

    if self.is_beacon:
      self.r.set_message("\r\n\r\n{}:{}{}\r  \b  ".format(self.mycall, self.crc(self.mycall), self.message))
    else:
      self.r.set_message("{}:{}{}\r  \b  ".format(self.mycall, self.crc(self.mycall), self.message))

  def send_code(self):
    self.dds.on()
    sleep(.1)
    self.r.send_code()

  def send_tone(self, tone):
    self.incremental_tone = (self.incremental_tone + float(tone) + 1.0) % 33
    self.f = int(int(self.frequency) + self.usb_offset + self.incremental_tone * self.spacing)
    self.dds.set_freq(0, self.f)
    self.dds.send()

  def all_done(self):
    if self.is_beacon:
      self.r.stop()              # stop sending bits
      self.dds.off()
      sleep(float(self.beacon_interval))
      self.dds.on()
      self.r.send_code()         # Repeat for a beacon
    else:
      self.r.stop()              # stop sending bits
      self.dds.off()

    self.all_done = True

  def crc(self, text):
    self.table = []
    for x in range(256):
      byte_val = x
      for y in range(8):
        if byte_val & 0x80:
          byte_val = (byte_val * 2) ^ 7
        else:
          byte_val = (byte_val * 2) ^ 0
      self.table.append(byte_val & 0xFF)

    val = 0
    for ch in text:
      val = self.table[val ^ ord(ch)] & 0xFF

    return "%0.2X" % (val & 0xFF)