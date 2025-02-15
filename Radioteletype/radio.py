from rp2 import PIO, StateMachine, asm_pio

class Radio:
  def set_osc(self, carrier_pin, frq, mark, space):
    from machine import Pin, freq
    
    @asm_pio(set_init=PIO.OUT_LOW)
    def square():
      wrap_target()
      set(pins, 1)
      set(pins, 0)
      wrap()

    self.carrier_pin = Pin(carrier_pin, Pin.OUT)
    self.sm_mark.init(square, freq=2*(self.f+mark), set_base=self.carrier_pin)
    self.sm_space.init(square, freq=2*(self.f+space), set_base=self.carrier_pin)
    self.sm_mark.active(0)
    self.sm_space.active(0)

  def __init__(self, carrier_pin, frq, mark, space):
    self.f = frq
    self.sm_mark = StateMachine(0)
    self.sm_space = StateMachine(1)
    self.set_osc(carrier_pin, frq, mark, space)
            
  def set_mark(self):
    self.sm_mark.active(1)
    self.sm_space.active(0)

  def set_space(self):
    self.sm_space.active(1)
    self.sm_mark.active(0)

  def get_freq(self):
    return self.f

  def off(self):
    self.sm_space.active(0)
    self.sm_mark.active(0)