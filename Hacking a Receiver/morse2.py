from morse import Morse

def main():
  PIN_D4 = 2

  # tone = int(input(”Tone? “))
  tone = 300
  morse = Morse(PIN_D4, tone)
  print(”Morse code AM Beacon”)
  morse.speed(20)
  # str = input(”Enter the message to send: “)
  str = “Dave used to know some Morse code, but has forgotten all but a few letters.”
  while(True):
    morse.send(str)

main()
