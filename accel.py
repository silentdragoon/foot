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

def avg(values):
	return sum(values, 0.0) / len(values)


ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)

#Start access point
ser.write(startAccessPoint())

counter = 0
configcount = 0
normal = []
xlog = []
ylog = []
zlog = []

while 1:
    #Send request for acceleration data
    ser.write(accDataRequest())
    accel = ser.read(7)

    if ord(accel[0]) != 0 and ord(accel[1]) != 0 and ord(accel[2]) != 0:
	x = ord(accel[0])
	y = ord(accel[1])
	z = ord(accel[2])

	x -= 128
	y -= 128
	z -= 128

	xlog.append(x)
	ylog.append(y)
	zlog.append(z)

	counter += 1
	configcount += 1

	# average last five movements	


	if configcount < 100:
		counter = 0
	
	if configcount == 100:
		counter = 0
		normal.extend([round(avg(xlog)),round(avg(ylog)),round(avg(zlog))])
		print "Stationary position: " + str(normal)
		

	if counter == 5:
		counter = 0
		px = round(avg(xlog)) - normal[0]
		py = round(avg(ylog)) - normal[1] 
		pz = round(avg(zlog)) - normal[2] 

		if (abs(px) + abs(py) + abs(pz)) < 20:
			print "Stationary."
		else:
			print "x: " + str(px) + " y: " + str(py) + " z: " + str(pz)


		del xlog[:]
		del ylog[:]
		del zlog[:]

	# if motion is detected, print motion
	# if not much motion is detection, print stationary

    if heardEnter():
	print "Thanks for playing!"
	ser.close()
	sys.exit(0)
ser.close()
