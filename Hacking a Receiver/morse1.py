from morse import Morse

def main():
  PIN_D4 = 2

  # tone = int(input(”Tone? “))
  tone = 800
  morse = Morse(PIN_D4, tone)
  print(”Morse code AM Beacon”)
  morse.speed(20)
  # str = input(”Enter the message to send: “)
  str = “Patrizia knows two or three letters of morse code, but she won’t admit to it.”
  while(True):
    morse.send(str)

main()
