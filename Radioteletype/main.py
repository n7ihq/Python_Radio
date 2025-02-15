from rtty_config import RttyProcess
from machine import Pin, freq
from time import sleep
  
def main():
  rp = RttyProcess(Pin(15), 135700, "AB6NY", "CM87xe")
  rp.set_message("{} Testing from {} using a Raspberry Pi Pico RP2040")
  
  while True:
    rp.send_code()
    while rp.r.all_done == False:
      sleep(1)

main()