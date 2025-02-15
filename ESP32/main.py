from machine import UART
from name import name

TX = 21
RX = 37

def main():

  uart = UART(1, baudrate=2400, tx=TX, rx=RX)

  if name == "Ichabod":
    count = 0
    while True:
      msg = "UUU " + str(count) + ": Hello, world!\r\n"
      print("Sending", msg, end="")
      uart.write(msg)
      count += 1

  while True:
    try:
      m = uart.read()
      if m:
        print(m.decode('utf-8'), end="")
    except UnicodeError:
      pass

main()
