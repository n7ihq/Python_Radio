from morse import Morse

def main():
  PIN_D4 = 2

  morse = Morse(PIN_D4)
  print("Morse code transmitter")
  while(True):
    wpm = input("How many words per minute? ")
    if int(wpm) > 0 and int(wpm) < 50:
      morse.speed(int(wpm))
      str = input("Enter the message to send: ")
      morse.send(str)
    else:
      print("Try a more reasonable speed.")

main()
