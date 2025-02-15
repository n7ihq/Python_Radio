from machine import Pin, PWM

def main():
  pin = Pin(18, Pin.OUT)
  pwm = PWM(pin, freq=10, duty=512)

  bands = (
    ( 1800000,  2000000), # 160 meters
    ( 3500000,  4000000), # 80 meters
    ( 7000000,  7300000), # 40 meters
    (10100000, 10150000), # 30 meters
    (14000000, 14350000), # 20 meters
    (18068888, 18168000), # 17 meters
    (21000000, 21450000), # 15 meters
    (24890000, 24990000), # 12 meters
    (28000000, 29700000)  # 10 meters
  )

  guess = 0
  for x in bands:
    f_lo, f_hi = x
    for f in range(f_lo, f_hi):
      pwm.freq(f)
      actual = pwm.freq()
      if actual != guess:
        print(str(actual) + ", ", end="")
        guess = actual
    print()

main()