import serial, array, select, sys, math, sqlite3, curses
from datetime import datetime

def startAccessPoint():
    return array.array('B', [0xFF, 0x07, 0x03]).tostring()

def accDataRequest():
    return array.array('B', [0xFF, 0x08, 0x07, 0x00, 0x00, 0x00, 0x00]).tostring()

def avg(values):
        return sum(values, 0.0) / len(values)

def startDB():
    conn = sqlite3.connect('/home/will/foot/testData.db')
    c = conn.cursor()
    c.execute('''create table if not exists acceldata (sessionID text, gestureID integer, xdata real, ydata real, zdata real)''')
    conn.commit()
    c.execute('''create table if not exists capData (gestureID integer, cap test)''')
    conn.commit()
    c.close()
    return conn

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main(screen):

    capData = []

    def cprint(message,x,y):
        if y == 5 and x == 15:
            screen.addstr(5,5,"STATUS:                                 ")
        screen.addstr(y,x,message)
        screen.refresh()

    rightnow = datetime.now()

    ser = serial.Serial('/dev/ttyACM0',115200,timeout=1)

    # start access point
    ser.write(startAccessPoint())

    # initialise counters and such

    configcount = -100
    counter = 0
    stat = []
    xlog = []
    ylog = []
    zlog = []
    capturing = False
    gestureID = 1
    
    screen.nodelay(1)

    cprint("Welcome to the gesture capture app.",5,0)
    cprint("SessionID: " + str(rightnow),5,1)
    cprint("Keys: C - Reconfigure Stationary Position | G - Set Next GestureID",5,11)
    cprint("      B - Begin Capture | S - Stop Capture | Q - Quit",5,12)

    cprint("Waiting for accelerometer data.", 15,5)

    # set up sqlite3 database
    conn = startDB()

    while 1:

        ccc = screen.getch()
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
            
            cprint("Next gesture captured will be " + str(gestureID) + "                                     ",15,5)

                # store captured data to sqlite database that's previously been set up

            if capturing == True:
                c = conn.cursor()
                c.execute('''insert into acceldata values (?,?,?,?,?)''',[rightnow,gestureID,x,y,z])
                conn.commit()
                c.close()
                
                # capture data for recognition later
                
                capData.append([0,x,y,z])

            # print smoothed values

            cprint("                                            ",15,7)
            cprint("Current values:    " + str([x,y,z]),15,7)

                   

        if ccc == ord('g') and capturing == False:
            screen.nodelay(0)
            curses.echo()
            cprint("Please input next gesture ID to be captured: ",5,9)
            screen.addstr(9,55, " "*3, curses.A_UNDERLINE)
            nextGesture = screen.getstr(9,55)
            curses.noecho()
            screen.nodelay(1)
            cprint("                                                       ",5,9)
            if is_number(nextGesture):
		gestureID = int(nextGesture)
        	cprint("Idling. Next gesture captured will be " + str(gestureID) + "                                     ",15,5)

        if ccc == ord('c') and capturing == False:
            configcount = -100

        if ccc == ord('b') and capturing == False:
            cprint("Capturing gesture " + str(gestureID) + "                                       ",15,5)
            capturing = True

        if ccc == ord('s') and capturing == True:
            gestureID += 1
            capturing = False
            cprint("Idling. Next gesture captured will be " + str(gestureID) + "                                     ",15,5)
            
            c = conn.cursor()
            c.execute('''insert into capData values (?,?)''',[(gestureID-1),str(capData)])
            conn.commit()
            c.close()
           
            capData = []
    
        if ccc == ord('q'):
            ser.close()
            sys.exit(0)

if __name__ == "__main__":
    curses.wrapper(main)
