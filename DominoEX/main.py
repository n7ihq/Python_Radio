from dominoex_config import DominoEXConfig
from time import sleep

def main():
  dex = DominoEXConfig(4, 7040000, "AB6NY", "CM87xe")

  while True:
    dex.set_message("          {} Testing from {} using a Raspberry Pi Pico RP2040")
    dex.send_code()
    while dex.all_done == False:
      sleep(5)

main()
