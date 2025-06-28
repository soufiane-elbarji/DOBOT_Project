from serial.tools import list_ports

import pydobot

port = "COM5"
device = pydobot.Dobot(port=port, verbose=False)

print("Dobot connected")

(x, y, z, r, j1, j2, j3, j4) = device.pose()


print(f"dobot position:  x:{x} y:{y} z:{z} r:{r}")


device.close()