import utime

class Radio:
  def __init__(self):
    from SI5351 import SI5351
    from machine import Pin, SoftI2C

    # self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)     # ESP32
    self.i2c = SoftI2C(scl=Pin(1), sda=Pin(0), freq=400000)     # RP2040

    # self.i2c = SoftI2C(scl=Pin(22), sda=Pin(21),   freq=800000)     # The ESP32 can do up to 5 MHz best case
    print( "I2C.scan():", self.i2c.scan())
    for x in range(5):
      self.clockgen = SI5351(self.i2c, 0x60 + x)
      status = 0
      if self.clockgen.read8(0, status):
        break
    self.clockgen.begin()
    self.clockgen.setClockBuilderData()
    self.key_state = False
    self.actual_freq_a = 0
    self.actual_freq_b = 0
    self.nominal_freq_a = 0
    self.nominal_freq_b = 0
    # self.last_time = utime.ticks_ms()

    self.old_mult = 0
    self.old_num = 0
    self.old_denom = 0
    self.old_src = 0

  def gcd(self, x, y):
     while(y): 
         x, y = y, x % y 
     return x 

  def send(self):
    pass

  def info(self):
    print( "I2C.scan():", self.i2c.scan())
    
  def on(self):
    if self.clockgen.enableOutputs(True):
      self.key_state = True

  def off(self):
    if self.clockgen.enableOutputs(False):
      self.key_state = False

  def key_down(self):
    if self.clockgen.enableOutputs(True):
      self.key_state = True

  def key_up(self):
    if self.clockgen.enableOutputs(False):
      self.key_state = False

  def get_freq(self, which):
    if which == 0:
      return self.nominal_freq_a
    else:
      return self.nominal_freq_b

  def set_freq(self, which, f):
    f = float(f)
    div = int(900000000.0 / f)              # Values under a megahertz need an extra divide step
    r = 1
    while div > 900:
      r *= 2
      div /= 2
   
    if div % 2:                             # Make sure it is an even number
      div -= 1
   
    pllFreq = div * r * f
   
    xtal_freq = 25000000                    # Our board uses a 25 MHz crystal
    fmult = pllFreq / xtal_freq             # The full multiplier
    mult = int(fmult)                       # The integer part of the multiplier
    frac = fmult - mult
    off = int(frac * xtal_freq)
    divisor = self.gcd(off, xtal_freq)
    num = int(off / divisor)
    denom = int(xtal_freq / divisor)
   
    if num > 0xFFFFF or denom > 0xFFFFF:
      denom = 0xFFFFF                       # Use the maximum value for the denominator
      num = int((pllFreq % xtal_freq) * denom / xtal_freq)


    # Below 18 MHz, we will never be more than half a Hertz off
    # Below 37.5 MHz, we will never be more than a Hertz off
    # Below 75 MHz, we will never be more than two Hertz off
    # Below 112.5 MHz, we will never be more than three Hertz off
    # Below 150 MHz, we will never be more than four Hertz off
    # Below 222 MHz, we will never be more than six Hertz off
    # A little over 18% of the frequencies were right on the money
    # This is better than the frequency stability of a temperature controlled crystal oscillator
    # so any failure of accuracy here will be swamped by the variability in the oscillator
    # Of course, if you have a nice OCXO crystal oscillator in an oven that has a parts-per-billion accuracy
    # then you might want to know that you will never be off by more than 4 Hz in the 200 Hz wide WSPR window
    # in the 2 meter band.

    # All that assumes that we have double precision arithmetic. Micropython on the ESP8266 only has single precision 32 bit floats.
    # So we can think we are off by as much as 5 Hz in the 40-meter band, when the Si5351 is actually much more accurate.
    # On the ESP32, I have built special micropython firmware that supports double precision artithmetic.

    # If r is 1, we will never be less than our target frequency

    if which == 0:
      self.actual_freq_a = (mult * xtal_freq + xtal_freq * num / denom) / div * r
      self.nominal_freq_a = f
      src = "A"
    else:
      self.actual_freq_b = (mult * xtal_freq + xtal_freq * num / denom) / div * r
      self.nominal_freq_b = f
      src = "B"

    # print("Mult is", mult, "Num is", num, "Denom is", denom, "Src is", src, "Div is", div)

    reset = False
    if mult != self.old_mult and num != self.old_num and denom != self.old_denom and src != self.old_src:
      reset = True

    self.clockgen.setupPLL(mult, num, denom, pllsource=src, reset=reset)
    self.old_mult = mult
    self.old_num = num
    self.old_denom = denom
    self.old_src = src

    self.clockgen.setupMultisynth(output=0, div=div, num=0, denom=1, pllsource=src)
    if r > 1:
      self.clockgen.setupRdiv(output=0, div=r)