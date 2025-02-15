from machine import Pin, freq, ADC
from time import sleep, sleep_ms
from neopixel import NeoPixel

PIN_D4 = 2

def main():
  freq(160000000)                                       # 160 MHz
  pwr = ADC(0)
  np = NeoPixel(Pin(PIN_D4), 16)

  while True:
    avg = 0
    for count in range(20):
      avg += pwr.read()
    avg /= 20
    how_many_lights = avg * 16 / 1024

    for i in range(16):
      if i < how_many_lights:
        np[i] = (0, 2, 0)
      else:
        np[i] = (0, 0, 0)
    np.write()

main()
