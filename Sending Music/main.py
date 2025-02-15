from rtttl import RTTTL
from time import sleep_ms, sleep
from machine import Pin, PWM

PIN_D4     = 2
key = PWM(Pin(PIN_D4))

def play_tone(freq, msec):
  if freq > 0:
    key.freq(int(freq/4))       # Set frequency (divide by 4 because we can't go higher than 1000 Hz)
    key.duty(512)               # 50% duty cycle
  sleep_ms(int(0.9 * msec))     # Play for a number of msec
  key.duty(0)                   # Stop playing for gap between notes
  sleep_ms(int(0.1 * msec))     # Pause for a number of msec

while(True):
  with open('tunes.txt') as f:
    for song in f:
      print(song.split(":")[0])
      tune = RTTTL(song)
      for freq, msec in tune.notes():
        play_tone(freq, msec)
      sleep(1)
