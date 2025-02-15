from mfsk_config import MfskProcess
from machine import Pin
from time import sleep
  
def main():
  mp = MfskProcess(15, 7040000, 4, "", "AB6NY", "CM87xe")
  mp.set_message("{} Testing from {} using a Raspberry Pi Pico RP2040")
  
  while True:
    mp.send_code()
    while mp.r.all_done == False:
      sleep(5)

main()