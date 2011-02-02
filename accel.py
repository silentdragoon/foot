import serial, array, select, sys, math

def startAccessPoint():
    return array.array('B', [0xFF, 0x07, 0x03]).tostring()

def accDataRequest():
    return array.array('B', [0xFF, 0x08, 0x07, 0x00, 0x00, 0x00, 0x00]).tostring()

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return True
    return False


ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)

#Start access point
ser.write(startAccessPoint())

hx = 0
hy = 0
hz = 0

while 1:
    #Send request for acceleration data
    ser.write(accDataRequest())
    accel = ser.read(7)

    if ord(accel[0]) != 0 and ord(accel[1]) != 0 and ord(accel[2]) != 0:
	x = ord(accel[0])
	y = ord(accel[1])
	z = ord(accel[2])
        print "x: " + str(x) + " y: " + str(y) + " z: " + str(z)
	if (abs(x) > abs(hx)):
		hx = x
	if (y > hy):
		hy = y
	if (z > hz):
		hz = z

    if heardEnter():
	print "Thanks for playing! High scores:"
	print "x: " + str(hx) + " y: " + str(hy) + " z: " + str(hz)
	ser.close()
	sys.exit(0)
ser.close()
