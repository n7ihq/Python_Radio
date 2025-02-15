from cwmorse import CWMorse
from time import sleep

frequency = 28050000

def main():
  cw = CWMorse(15, frequency)
  cw.farnsworth(False)
  cw.speed(0.1)

  print("CW transmitter")
  msg = "This is AB6NY testing RP2040 as a 40 meter transmitter sending on " + str(frequency) + " Hertz."
  while True:
    print(msg)
    cw.send(msg)
    sleep(5)

main()
