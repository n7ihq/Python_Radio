from machine import Timer
from dominoex_varicode import dominoex_varicode

class DOMINOEX:
  def __init__(self, send_tone, report_message_end=None):
    self.send_tone = send_tone
    self.report_message_end = report_message_end

    # self.set_baud(10.766)     # DOMINOEX 11
    self.set_baud(2)     # DOMINOEX MICRO

    self.frequency = "7104000"
    self.call = "N0CALL"
    self.location = "CM87xe"
    self.message = "{} {}   "
    self.bit_length = int(1000 / float(self.baud))
    self.timer = Timer()

  def set_call(self, call):
    self.call = call

  def set_baud(self, baud):
    self.baud = float(baud)

  def set_bit_length(self, len):
    self.bit_length = int(len)

  def set_frequency(self, frequency):
    self.frequency = frequency

  def set_location(self, location):
    self.location = location

  def set_message(self, message):
    self.message = message.format(self.call, self.location)

  def bit(self):
    for letter in self.message:
      code = dominoex_varicode[ord(letter)]
      count = 0
      for tone in code:
        if tone & 0x8 or count == 0:
          yield tone
        count += 1
    self.report_message_end()

  def stop(self):
    self.timer.deinit()

  def send_code(self):
    self.gen = self.bit()
    self.timer.init(period=self.bit_length, mode=Timer.PERIODIC, callback=self.bit_finished)

  def send_bit(self, unused):
    try:
      tone = next(self.gen)
    except StopIteration as tone:
      return self.report_message_end()
    self.send_tone(tone)

  def bit_finished(self, unused):
    self.send_bit(True)