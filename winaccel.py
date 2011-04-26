import serial, array, select, sys, math, sqlite3, curses, struct
from datetime import datetime
from classifier import *

def startAccessPoint():
    return array.array('B', [0xFF, 0x07, 0x03]).tostring()

def accDataRequest():
    return array.array('B', [0xFF, 0x08, 0x07, 0x00, 0x00, 0x00, 0x00]).tostring()

def avg(values):
        return sum(values, 0.0) / len(values)

def startDB():
    conn = sqlite3.connect('testData.db')
    c = conn.cursor()
    c.execute('''create table if not exists acceldata (sessionID text, gestureID integer, xdata text, ydata text, zdata text)''')
    conn.commit()
    c.execute('''create table if not exists capData (gestureID integer, cap text)''')
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
    
    r = Recognizer()
    gestureName = "Stomp"
    
    blank = [[0,0,0,0],[0,5,5,5],[0,0,0,0]]
    r.addTemplate("blank",blank)
     
    def cprint(message,x,y):
        if y == 5 and x == 15:
            screen.addstr(5,5,"STATUS:                                 ")
        screen.addstr(y,x,message)
        screen.refresh()

    rightnow = datetime.now()

    ser = serial.Serial(2,115200,timeout=1)

    # start access point
    ser.write(startAccessPoint())

    # initialise counters and such

    capturing = False
    gestureID = 1
    
    screen.nodelay(1)

    cprint("Welcome to the gesture capture app.",5,0)
    cprint("SessionID: " + str(rightnow),5,1)
    cprint("Keys: G - Set Next GestureID | N - Set next GestureName",5,11)
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
            x = struct.unpack('b', accel[0])
            y = struct.unpack('b', accel[1])
            z = struct.unpack('b', accel[2])

            
            cprint("Next gesture captured will be " + str(gestureID) + "                                     ",15,5)

                # store captured data to sqlite database that's previously been set up

            if capturing == True:
            
                cprint("Capturing gesture " + str(gestureID) + "                                       ",15,5)
                c = conn.cursor()
                c.execute('''insert into acceldata values (?,?,?,?,?)''',[rightnow,gestureID,str(x),str(y),str(z)])
                conn.commit()
                c.close()
                
                # capture data for recognition later
                capData.append([0,int(x[0]),int(y[0]),int(z[0])])

            # print smoothed values

            cprint("                                            ",15,7)
            cprint("Current values:    " + str([x,y,z]),15,7)
            cprint("                                            ",15,6)
            cprint("Next gesture's name is: " + gestureName,15,6)

                   

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

        if ccc == ord('n') and capturing == False:
            screen.nodelay(0)
            curses.echo()
            cprint("Please input next gesture's name: ",5,9)
            screen.addstr(9,55, " "*10, curses.A_UNDERLINE)
            gestureName = screen.getstr(9,55)
            curses.noecho()
            screen.nodelay(1)
            cprint("                                                       ",5,9)

        if ccc == ord('c') and capturing == False:
            configcount = -100

        if ccc == ord('b') and capturing == False:
            capturing = True

        if ccc == ord('s') and capturing == True:
            gestureID += 1
            capturing = False
            cprint("Idling. Next gesture captured will be " + str(gestureID) + "                                     ",15,5)
            
            c = conn.cursor()
            c.execute('''insert into capData values (?,?)''',[(gestureID-1),str(capData)])
            conn.commit()
            c.close()
           
            # do classification
            cprint("                                                                                                          ",15,20)
            cprint("Gesture name and score: " + str(r.recognize(capData)),15,20)
           
            # add as a trace
            r.addTemplate(gestureName,capData)
           
            capData = []
    
        if ccc == ord('q'):
            ser.close()
            sys.exit(0)

if __name__ == "__main__":
    curses.wrapper(main)
