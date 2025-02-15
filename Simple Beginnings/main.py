from machine import Pin, PWM
from time import sleep

ANY_CHANGE = Pin.IRQ_RISING | Pin.IRQ_FALLING
PIN_D4     = 2
PIN_D8     = 15

xmit_pin = PWM(Pin(PIN_D4, Pin.OUT), 1000)
xmit_pin.duty(0)

def key_changed(pin):
  global xmit_pin

  if pin.value():
    xmit_pin.duty(512)
  else:
    xmit_pin.duty(0)

key = Pin(PIN_D8, Pin.IN)
key.irq(trigger=ANY_CHANGE, handler=key_changed)

while(True):
  sleep(1)
