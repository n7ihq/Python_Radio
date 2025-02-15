from machine import PWM, Pin

def main():
  PIN_D4 = 2
  MIN = 40
  MAX = 135

  servo = PWM(Pin(PIN_D4, Pin.OUT), freq=50)
  servo.duty(int(MIN))

  while(True):
    degrees = float(input("How many degrees of rotation (0 to 180)? "))
    if degrees >= 0 and degrees <= 180:
      d = int(degrees / 180 * (MAX-MIN) + MIN)
      print(d, "duty cycle")
      servo.duty(d)

main()
