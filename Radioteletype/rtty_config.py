from rtty import RTTY
from machine import Pin

class RttyProcess:
  def __init__(self, pin, freq, call, location):
    from radio import Radio

    self.mark = 2195
    self.diff_freq = 170
    self.space = self.mark - self.diff_freq
    self.osc = Radio(pin, freq, self.mark, self.space)
    self.r = RTTY(self.send_space, self.send_mark)
    self.r.set_call(call)
    self.r.set_location(location)

  def set_message(self, msg):
    self.r.set_message(msg)

  def send_space(self):
    self.osc.set_space()

  def send_mark(self):
    self.osc.set_mark()

  def send_code(self):
    self.r.send_code()