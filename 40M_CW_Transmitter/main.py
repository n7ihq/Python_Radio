from cwmorse import CWMorse
from machine import Pin, PWM
from time import sleep

def main():
  OUT_PIN = 18
  f = 7032966

  pin = Pin(18, Pin.OUT)
  pwm = PWM(pin, freq=f, duty=512)    # So that we can read the actual frequency
  actual = pwm.freq()
  pwm.deinit()
  pwm = None

  cw = CWMorse(OUT_PIN, f)
  cw.speed(20)
  print("CW transmitter")
  msg = "AB6NY testing ESP32 as a 40 meter transmitter sending on " + str(actual) + " Hertz."
  while True:
    print(msg)
    cw.send(msg)
    sleep(5)

main()