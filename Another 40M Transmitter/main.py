from machine import Pin, PWM
from rp2 import PIO, StateMachine, asm_pio

class RP_CW:
  def __init__(self, pin):
    from machine import Pin
    from rp2 import PIO, StateMachine, asm_pio

    @asm_pio(set_init=PIO.OUT_LOW)
    def square():
      wrap_target()
      set(pins, 1)
      set(pins, 0)
      wrap()

    self.pin = Pin(pin, Pin.OUT)
    self.f = 7030000
    self.sm = rp2.StateMachine(0, square, freq=2*self.f, set_base=self.pin)

  def on(self):
    self.sm.active(1)

  def off(self):
    self.sm.active(0)
  
  def frequency(self, frq):
    self.f = frq

class CWMorse:
  character_speed = 18

  def __init__(self, pin, freq):
    self.cw = RP_CW(pin)
    self.cw.frequency(freq)
    
  def speed(self, overall_speed):
    if overall_speed >= 18:
      self.character_speed = overall_speed
    units_per_minute = int(self.character_speed * 50)        # The word PARIS is 50 units of time
    OVERHEAD = 2
    self.DOT = int(60000 / units_per_minute) - OVERHEAD
    self.DASH = 3 * self.DOT
    self.CYPHER_SPACE = self.DOT

    if overall_speed >= 18:
      self.LETTER_SPACE = int(3 * self.DOT) - self.CYPHER_SPACE
      self.WORD_SPACE = int(7 * self.DOT) - self.CYPHER_SPACE
    else:
      # Farnsworth timing from “https://www.arrl.org/files/file/Technology/x9004008.pdf”
      farnsworth_spacing = (60000 * self.character_speed - 37200 * overall_speed) / (overall_speed * self.character_speed)
      farnsworth_spacing *= 60000/68500    # A fudge factor to get the ESP8266 timing closer to correct
      self.LETTER_SPACE = int((3 * farnsworth_spacing) / 19) - self.CYPHER_SPACE
      self.WORD_SPACE = int((7 * farnsworth_spacing) / 19) - self.CYPHER_SPACE

  def send(self, str):
    from the_code import code
    from time import sleep_ms
    for c in str:
      if c == ' ':
        self.cw.off()
        sleep_ms(self.WORD_SPACE)
      else:
        cyphers = code[c.upper()]
        for x in cyphers:
          if x == '.':
            self.cw.on()
            sleep_ms(self.DOT)
          else:
            self.cw.on()
            sleep_ms(self.DASH)
          self.cw.off()
          sleep_ms(self.CYPHER_SPACE)
        self.cw.off()
        sleep_ms(self.LETTER_SPACE)

from time import sleep

frequency = 7030000

def main():
  cw = CWMorse(15, frequency)
  cw.speed(5)
  print("CW transmitter")
  msg = "AB6NY testing RP2040 as a 40 meter transmitter sending on " + str(frequency) + " Hertz."
  while True:
    print(msg)
    cw.send(msg)
    sleep(5)

main()