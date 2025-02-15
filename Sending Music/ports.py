# pip install serial

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

print([ port for port, desc, hwid in sorted(ports) if port != ""])

# for port, desc, hwid in sorted(ports):
#   print("{}: {}".format(port, desc))
