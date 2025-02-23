from fsq_config import FSQConfig
from time import sleep

# FLDIGI knows these baud rates: 1.5, 2, 3, 4.5, 6

def main():
  fsq = FSQConfig(7040000, 12, "AB6NY", "CM87xe")

  while True:
    fsq.set_message("{} Testing from {} using a Raspberry Pi Pico RP2040")
    fsq.send_code()
    while fsq.all_done == False:
      sleep(5)

main()
