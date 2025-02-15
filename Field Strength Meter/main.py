from machine import ADC

pwr = ADC(0)

while True:
  avg = 0
  for count in range(20):
    avg += pwr.read()
  avg /= 20
  print(avg)
