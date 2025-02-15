from machine import Timer

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ \r\n"

rtty_letters = {
  "a" : "11000",
  "b" : "10011",
  "c" : "01110",
  "d" : "10010",
  "e" : "10000",
  "f" : "10110",
  "g" : "01011",
  "h" : "00101",
  "i" : "01100",
  "j" : "11010",
  "k" : "11110",
  "l" : "01001",
  "m" : "00111",
  "n" : "00110",
  "o" : "00011",
  "p" : "01101",
  "q" : "11101",
  "r" : "01010",
  "s" : "10100",
  "t" : "00001",
  "u" : "11100",
  "v" : "01111",
  "w" : "11001",
  "x" : "10111",
  "y" : "10101",
  "z" : "10001",
  " " : "00100",
  "\r": "00010",
  "\n": "01000",
  "+" : "11011",     # shift to figures
  "-" : "11111",     # shift to letters
}

rtty_figures = {
  "0" : "01101",    # same as p
  "1" : "11101",    # same as q
  "2" : "11001",    # same as w
  "3" : "10000",    # same as e
  "4" : "01010",    # same as r
  "5" : "00001",    # same as t
  "6" : "10101",    # same as y
  "7" : "11100",    # same as u
  "8" : "01100",    # same as i
  "9" : "00011",    # same as o
  "-" : "11000",    # same as a
  "*" : "10100",    # BELL: same as s
  "$" : "10010",    # same as d
  "'" : "11010",    # same as j
  "," : "00110",    # same as n
  "!" : "10110",    # same as f
  ":" : "01110",    # same as c
  "(" : "11110",    # same as k
  "\"": "10001",    # same as z
  ")" : "01001",    # same as l
  "#" : "00101",    # same as h
  "?" : "10011",    # same as b
  "&" : "01011",    # same as g
  "." : "00111",    # same as m
  "/" : "10111",    # same as x
  ";" : "01111",    # same as v
  " " : "00100",    # unique (same in both lists)
  "\r": "00010",    # unique (same in both lists)
  "\n": "01000",    # unique (same in both lists)
  "+" : "11011",    # shift to figures
  "-" : "11111",    # shift to letters
}

start_bit = "B"
stop_bit = "E"

class RTTY:
  def __init__(self, space, mark):
    self.xmit_space = space
    self.xmit_mark = mark
    self.all_done = False

    self.set_baud(45.45)

    self.frequency = "7035000"
    self.call = "N0CALL"
    self.location = "CM87xe"
    self.message = "{} {}   "
    self.baud = 45.45
    self.bit_length = int(1000 / float(self.baud))
    self.timer = Timer()

  def set_call(self, call):
    self.call = call

  def set_baud(self, baud):
    self.baud = float(baud)
    self.bit_length = int(1000.0 / self.baud)

  def set_frequency(self, frequency):
    self.frequency = frequency

  def set_location(self, location):
    self.location = location

  def fix_message(self, msg):
    mode = True                       # True means we are in letter mode
    str = "----------\r\n"            # Start each message with 10 diddles and a CRLF
    for c in msg:
      c = c.upper()
      if c in letters:
        if not mode:                  # We were in figures mode -- shift back to letters
          str += "-"
          mode = True
      else:                           # It was not a letter
        if mode:                      # We were in letters mode -- shift to figures
          str += "+"
          mode = False
      str += c
    if not mode:                      # If we were in figures mode, shift back to letters
      str += "-"

    str += "\r\n"                     # End each message with a CRLF
    return str

  # set_call() and set_location() must be called first
  def set_message(self, message):
    self.message = self.fix_message(message.format(self.call, self.location))
    print(self.message)

  def bit(self):
    for letter in self.message:
      letter = letter.lower()
      code = rtty_letters.get(letter)

      if not code:                                  # It wasn’t a letter
        code = rtty_figures.get(letter)             # So see if it was a number

      if not code:
        code = rtty_figures.get(" ")                # Make illegal characters send as spaces

      yield start_bit

      for b in code:
        yield b

      yield stop_bit

  def stop(self):
    self.timer.deinit()

  def send_code(self):
    self.all_done = False
    self.gen = self.bit()
    self.send_start_of_message()
    self.timer.init(period=self.bit_length, mode=Timer.PERIODIC, callback=self.bit_finished)

  def send_bit(self, unused):
    try:
      b = next(self.gen)
    except StopIteration as b:
      self.all_done = True
      return

    if b == "0":
      self.send_space()
    elif b == "1":
      self.send_mark()
    elif b == start_bit:
      self.send_start_bit()
    elif b == stop_bit:
      self.send_stop_bit()

  def bit_finished(self, unused):
    self.send_bit(True)

  def send_space(self):
    self.xmit_space()

  def send_mark(self):
    self.xmit_mark()

  def send_start_bit(self):
    self.xmit_space()

  def send_stop_bit(self):
    self.xmit_mark()

  # Lead-in: Hold MARK for 1.5 bits
  def send_start_of_message(self):
    self.xmit_mark()