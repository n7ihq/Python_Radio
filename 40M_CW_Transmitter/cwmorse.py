from machine import Pin, PWM

class CWMorse:
  character_speed = 18

  def __init__(self, pin, freq):
    self.key = PWM(Pin(pin, Pin.OUT))
    self.key.freq(freq)

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
        self.key.duty(0)
        sleep_ms(self.WORD_SPACE)
      else:
        cyphers = code[c.upper()]
        for x in cyphers:
          if x == '.':
            self.key.duty(512)
            sleep_ms(self.DOT)
          else:
            self.key.duty(512)
            sleep_ms(self.DASH)
          self.key.duty(0)
          sleep_ms(self.CYPHER_SPACE)
        self.key.duty(0)
        sleep_ms(self.LETTER_SPACE)