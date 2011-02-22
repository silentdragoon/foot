import serial, array, select, sys, math, sqlite3, curses
from datetime import datetime

def startAccessPoint():
    return array.array('B', [0xFF, 0x07, 0x03]).tostring()

def accDataRequest():
    return array.array('B', [0xFF, 0x08, 0x07, 0x00, 0x00, 0x00, 0x00]).tostring()

def avg(values):
        return sum(values, 0.0) / len(values)

def startDB():
    conn = sqlite3.connect('/home/will/foot/data.db')
    c = conn.cursor()
    c.execute('''create table if not exists acceldata (sessionID text, gestureID integer, xdata real, ydata real, zdata real)''')
    conn.commit()
    c.close()
    return conn

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def main(screen):

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

    SMOOTH = 5
    STAT_SENS = 3

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
    cprint("Smoothing: " + str(SMOOTH) + " | Configuration time: " + str(abs(configcount)),5,2)
    cprint("Keys: C - Reconfigure Stationary Position | G - Set Next GestureID",5,10)
    cprint("      B - Begin Capture | S - Stop Capture | Q - Quit",5,11)

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

            # data smoothing of five values

            xlog.append(x)
            ylog.append(y)
            zlog.append(z)

            counter += 1
            configcount += 1

            # delay printing of values until config is done

            if configcount == -95:
                cprint("Configuring stationary position",15,5)

            if configcount < 0:
                cprint(str(100 - (abs(configcount))) + "%",50,5)
                counter = 0
            
            # config figures out stationary position

            if configcount == 0:
                counter = 0
                del stat[:]
                stat.extend([round(avg(xlog)),round(avg(ylog)),round(avg(zlog))])
                cprint("Stationary values: " + str(stat),15,6)
                cprint("Idling. Next gesture captured will be " + str(gestureID) + "                                     ",15,5)

            # smoothing takes place

            if counter == SMOOTH:
                counter = 0
                px = round(avg(xlog)) - stat[0]
                py = round(avg(ylog)) - stat[1] 
                pz = round(avg(zlog)) - stat[2] 

                # store captured data to sqlite database that's previously been set up

                if capturing == True:
                    c = conn.cursor()
                    c.execute('''insert into acceldata values (?,?,?,?,?)''',[rightnow,gestureID,px,py,pz])
                    conn.commit()
                    c.close()

                # print smoothed values

                cprint("                                            ",15,7)
                cprint("Current values:    " + str([px,py,pz]),15,7)

                   
            del xlog[:]
            del ylog[:]
            del zlog[:]

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
                gestureID = nextGesture
                cprint("Idling. Next gesture captured will be " + str(gestureID) + "                                     ",15,5)

        if ccc == ord('c') and capturing == False:
            configcount = -100

        if ccc == ord('b') and capturing == False:
            cprint("Capturing gesture " + str(gestureID) + "                                       ",15,5)
            capturing = True

        if ccc == ord('s') and capturing == True:
            gestureID += 1
            capturing = False
    
        if ccc == ord('q'):
            ser.close()
            sys.exit(0)

if __name__ == "__main__":
    curses.wrapper(main)
