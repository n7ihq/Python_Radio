from mfsk_varicode import mfsk_varicode
from machine import Timer

class MFSK:

  NASA_K = 7
  POLY1 = 0x6D
  POLY2 = 0x4F

  def __init__(self, timr, send_tone):
    self.timer = timr
    self.send_tone = send_tone

    #
    # Default is MFSK4
    #
    self.symbits = 5
    self.symlen = 2048
    self.samplerate = 8000
    self.depth = 5
    self.basetone = 256
    self.numtones = 32
    self.preamble = 107
    self.timer_running = False

    self.frequency = 7104000.0
    self.call = ""
    self.location = ""
    self.message = "{} {}   "
    self.count_tabs = 0
    self.has_bits = False
    self.sym_queue = []

    # Initialization for the forward error correction
    self.encoder_output = [0] * (1 << self.NASA_K)
    self.mask = (1 << self.NASA_K) - 1
    self.encode_state = 0
    self.bit_count = 0
    self.bit_state = 0

  # Code for the forward error correction
  def init_encoder(self):
    self.interleave_table = [8] * (self.symbits * self.symbits * self.depth)
    for x in range(1 << self.NASA_K):
      self.encoder_output[x] = (self.parity(self.POLY1 & x) | (self.parity(self.POLY2 &x) << 1))
    self.flush_interleave_table()

  # Hamming weight (the number of bits that are ones)
  def hamming_weight(self, w):
    w = (w & 0x55555555) + ((w >>  1) & 0x55555555)
    w = (w & 0x33333333) + ((w >>  2) & 0x33333333)
    w = (w & 0x0F0F0F0F) + ((w >>  4) & 0x0F0F0F0F)
    w = (w & 0x00FF00FF) + ((w >>  8) & 0x00FF00FF)
    w = (w & 0x0000FFFF) + ((w >> 16) & 0x0000FFFF)
    return w

  def parity(self, w):
    return self.hamming_weight(w) & 1

  def encode(self, bit):
    self.encode_state <<= 1
    if bit == "1":
      self.encode_state |= 1

    return self.encoder_output[self.encode_state & self.mask]

  def set_call(self, call):
    self.call = call

  def set_baud(self, baud):
    self.baud = float(baud)

  def set_bit_length(self, len):
    self.bit_length = 1000000.0 / float(self.baud)

  def set_frequency(self, frequency):
    self.frequency = float(frequency)

  def set_location(self, location):
    self.location = location

  def set_message(self, message):
    self.message = message.format(self.call, self.location)
    self.message = "\r" + chr(2) + "\r" + self.message + "\r" + chr(0) + "\r"
    self.has_bits = True

  def bit(self):
    global mfsk_varicode

    for letter in self.message:
      code = mfsk_varicode[ord(letter) & 255]
      for bit in bin(code)[2:]:
        yield bit

  def stop(self):
    self.timer.deinit()
    self.timer_running = False
    self.all_done = True

  def send_code(self):
    self.set_baud(self.samplerate / self.symlen)
    self.bit_length = 1000000.0 / float(self.baud)
    self.tonespacing = self.samplerate / self.symlen
    self.bandwidth = (self.numtones - 1) * self.tonespacing
    self.init_encoder()

    self.all_done = False
    self.clearbits()
    self.gen = self.bit()
    if self.timer_running == False:
      self.timer.init(period=int(self.bit_length/1000), mode=Timer.PERIODIC, callback=self.next_tone)
      self.timer_running = True
    self.reported_end = False
    self.has_bits = True
    while self.has_bits:
      bit = self.get_bit()
      self.send_bit(bit)

    self.flush_tx(self.preamble)
    self.reported_end = True

  def get_bit(self):
    try:
      bit = next(self.gen)
    except StopIteration as e:
      self.has_bits = False
      return None
    return bit

  def send_bit(self, bit):
    try:
      data = self.encode(bit)
      for x in range(2):
        self.bit_state = (self.bit_state << 1) | ((data >> x) & 1)
        self.bit_count += 1

        if self.bit_count == self.symbits:
          self.interleave()
          self.send_symbol()
          self.bit_count = 0
          self.bit_state = 0
    except Exception as e:
      print("Error:", e)

  def clearbits(self):
    data = self.encode(0)
    for x in range(self.preamble):
      for y in range(2):
        self.bit_state = (self.bit_state << 1) | ((data >> x) & 1)
        self.bit_count += 1
        if self.bit_count == self.symbits:
          self.interleave()
          self.bit_count = 0
          self.bit_state = 0

  def interleave_get(self, x, y, z):
    index = self.symbits * self.symbits * x + self.symbits * y + z
    return self.interleave_table[index]

  def interleave_put(self, x, y, z, val):
    index = self.symbits * self.symbits * x + self.symbits * y + z
    self.interleave_table[index] = val

  def symbols(self):
    for x in range(self.depth):
      for y in range(self.symbits):
        for z in range(self.symbits - 1):
          self.interleave_put(x, y, z, self.interleave_get(x, y, z + 1))

      for y in range(self.symbits):
        self.interleave_put(x, y, self.symbits-1, self.syms[y])

      for y in range(self.symbits):
        self.syms[y] = self.interleave_get(x, y, self.symbits - y - 1)

  def interleave(self):
    self.syms = []
    for x in range(self.symbits):
      self.syms.append(self.bit_state >> ((self.symbits - x - 1)) & 1)

    self.symbols()

    self.bit_state = 0
    for x in range(self.symbits):
      self.bit_state = (self.bit_state << 1) | self.syms[x]

  def flush_interleave_table(self):
    for x in range(len(self.interleave_table)):
      self.interleave_table[x] = 0

  def flush_tx(self, preamble):
    self.send_bit(chr(1));
    for x in range(preamble):
      self.send_bit(chr(0));
    self.bit_state = 0
    self.all_done = True

  #
  # In order to reduce the number of bit errors in a digital modem,
  # all symbols are automatically Gray encoded such that adjacent
  # symbols in a constellation differ by only one bit.
  #
  def gray_encode(self, data):
    bits = data;
    bits ^= data >> 1;
    bits ^= data >> 2;
    bits ^= data >> 3;
    bits ^= data >> 4;
    bits ^= data >> 5;
    bits ^= data >> 6;
    bits ^= data >> 7;
    return bits;

  def send_symbol(self):
    from uasyncio import sleep_ms
    import utime
    sym = self.bit_state & (self.numtones - 1)
    sym = self.gray_encode(sym)
    while len(self.sym_queue) > 10:
      # 256000 / 500 is 512 milliseconds (2 symbols at 3.90625 baud)
      sleep_ms(int(self.bit_length / 500))           # Needed so the web server gets some time
      utime.sleep_ms(int(self.bit_length / 500))     # Needed so ^C works
    self.sym_queue.append(sym)

  def sendchar(self, ch):
    code = mfsk_varicode[ord(ch) & 255]
    for bit in bin(code)[2:]:
      self.send_bit(bit);

  def sendidle(self):
    self.sendchar(chr(0));

  def next_tone(self, unused):
    if self.sym_queue:
      sym = self.sym_queue.pop(0)
      self.send_tone(self.basetone + sym * self.tonespacing)