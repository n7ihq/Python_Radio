from machine import Timer
from fsq_varicode import fsq_varicode

class FSQ:
  def __init__(self, baud, send_tone, report_message_end=None):
    self.send_tone = send_tone
    self.report_message_end = report_message_end

    self.set_baud(baud)
    self.frequency = "7104000"
    self.call = "N0CALL"
    self.location = "CM87xe"
    self.message = "{} {}   "
    self.baud = baud
    self.bit_length = int(1000 / float(baud))
    self.timer = Timer()
    self.all_done = False

  def set_call(self, call):
    self.call = call

  def set_baud(self, baud):
    self.baud = baud
    self.bit_length = int(1000 / float(self.baud))

  def set_frequency(self, frequency):
    self.frequency = frequency

  def set_location(self, location):
    self.location = location

  def set_message(self, message):
    self.message = message.format(self.call, self.location)

  def bit(self):
    for letter in self.message:
      code = fsq_varicode.get(letter)

      if not code:
        code = fsq_varicode.get(" ")                # Make illegal characters send as spaces

      count = 0

      for tone in code:
        if tone > 0 or count == 0:
          yield tone

        count += 1

    self.all_done = True

  def stop(self):
    self.timer.deinit()
    self.all_done = True

  def send_code(self):
    self.all_done = False
    self.gen = self.bit()
    self.timer.init(period=self.bit_length, mode=Timer.PERIODIC, callback=self.bit_finished)

  def send_bit(self, unused):
    try:
      tone = next(self.gen)
    except StopIteration as tone:
      self.all_done = True
      self.stop()
      self.report_message_end()
      return

    self.send_tone(tone)

  def bit_finished(self, unused):
    self.send_bit(True)