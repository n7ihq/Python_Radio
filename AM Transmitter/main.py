from cwmorse import CWMorse
from time import sleep

frequency = 540000
tone = 14
carrier = 15

def main():
  cw = CWMorse(carrier, tone, frequency)
  cw.speed(10)
  print("CW transmitter")
  msg = "AB6NY testing RP2040 as an AM transmitter sending on " + str(frequency) + " Hertz."
  cw.tune(True)
  sleep(30)
  cw.tune(False)
  
  while True:
    print(msg)
    cw.send(msg)
    sleep(5)

main()