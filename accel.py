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


def performGesture(gestureID):
	print "Now perform your gesture. Return to the stationary position when you are done."
	print "If you'd like to perform a gesture again, just press enter."

	while 1:
		if heardEnter():
			return False	
		return True

ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)

# start access point
ser.write(startAccessPoint())

# initialise counters and such

SMOOTH = 5
STAT_SENS = 3

configcount = -100
counter = 0
statcount = 0
stat = []
xlog = []
ylog = []
zlog = []

while 1:
    	# send request for acceleration data
    	ser.write(accDataRequest())
    	accel = ser.read(7)

    	if ord(accel[0]) != 0 and ord(accel[1]) != 0 and ord(accel[2]) != 0:
		x = ord(accel[0])
		y = ord(accel[1])
		z = ord(accel[2])

	# set 0 as midpoint

	x -= 128
	y -= 128
	z -= 128

	# data smoothing of five values

	xlog.append(x)
	ylog.append(y)
	zlog.append(z)

	counter += 1
	configcount += 1

	# delay printing of values until config is done

	if configcount < 0:
		counter = 0
	
	# config figures out stationary position

	if configcount == 0:
		counter = 0
		stat.extend([round(avg(xlog)),round(avg(ylog)),round(avg(zlog))])
		print str(configcount) + " Stationary values: " + str(stat)
		

	# print smoothed values

	if counter == SMOOTH:
		counter = 0
		px = round(avg(xlog)) - stat[0]
		py = round(avg(ylog)) - stat[1] 
		pz = round(avg(zlog)) - stat[2] 

		# if not much change, probably stationary

		if (abs(px) or abs(py) or abs(pz)) < STAT_SENS:
			print str(configcount) + " Stationary."
			statcount += 1

		# user is waiting to perform gesture

		if statcount == 5:
			statcount = 0
			if performGesture(gestureID) == True:
				gestureID += 1
			if performGesture(gestureID) == False:
				performGesture(gestureID)

		# otherwise, print accel values

		else:

			print str(configcount) + " " + str([px,py,pz])


		del xlog[:]
		del ylog[:]
		del zlog[:]

    if heardEnter():
	print "Thanks for playing!"
	ser.close()
	sys.exit(0)

ser.close()
