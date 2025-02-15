from machine import Timer, Pin, PWM

def main():
  from time import sleep_us

  freqs = [433.98, 315]

  speaker_pin = Pin(19, Pin.OUT)
  speaker_pin.value(0)
  in_pin = Pin(36, Pin.IN)

  while True:
    speaker_pin.value(0)
    for x in freqs:
      f = int(((x + (0.86 * x/315))/64.5) * 1000000)
      print(x, f)
      tune = PWM(Pin(18), freq=int(f), duty=512)
      for count in range(1000000):
        speaker_pin.value(in_pin.value())
        sleep_us(10)

main()
