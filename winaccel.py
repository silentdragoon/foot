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
    c.execute('''create table if not exists capData (gestureID integer, traceID integer, cap text)''')
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

    # initialise counters and such

    capturing = False
    gestureID = 0
    capData = []
    r = Recognizer()

    PhoneList = "Double tap", "Shake", "Clockwise Circle", "Counterclockwise Circle", "Swing Left", "Swing Right"
    MediaList = "Double tap", "Swing Right", "Swing Left", "Shake", "Swing Forward", "Swing Backward"
    MapList = "Swing Left", "Swing Right", "Swing Forward", "Swing Backward", "Arc Left", "Arc Right"
    BrowserList = "Double tap toe forward", "Double tap left front", "Double tap left right"
    WholeList = ("Double tap", "Shake", "Clockwise Circle", "Counterclockwise Circle", "Swing Left", "Swing Right",
                "Swing Forward", "Swing Backward", "Arc Left", "Arc Right")
    ShortList = "Double tap", "Shake"

    gestureList = ShortList
    gestureName = gestureList[0]
    traces = 5
    traceID = 0
    classifying = False
    testing = False

    score = 0.0
    total = 0.0
    badClass = []

    blank = [[0,0,0,0],[0,5,5,5],[0,0,0,0]]
    r.addTemplate("blank",blank)

    def cprint(message,x,y):
        screen.addstr(y,0," "*100)
        screen.addstr(y,x,message)
        screen.refresh()

    rightnow = datetime.now()

    ser = serial.Serial(3,115200,timeout=1)

    # start access point
    ser.write(startAccessPoint())

    screen.nodelay(1)

    cprint("Welcome to the gesture capture app.",5,0)
    cprint("SessionID: " + str(rightnow),5,1)
    cprint("Keys: G - Set Next GestureID | N - Set next GestureName | C - Toggle Classify Mode",5,11)
    cprint("      B - Begin Capture | S - Stop Capture | Q - Quit",5,12)
    cprint("Waiting for accelerometer data.", 15,5)
    cprint("Classify Mode: " + str(classifying) + " Testing mode: " + str(testing),5,2)

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


            if classifying == False:
                cprint("Next gesture captured will be ID " + str(gestureID),15,5)

            if classifying == True:
                cprint("We have entered classification mode.",15,5)
                cprint(" "*100,15,6)

                # store captured data to sqlite database that's previously been set up

            if capturing == True:

                cprint("Capturing gesture " + str(gestureID),15,5)
                # c = conn.cursor()
                # c.execute('''insert into acceldata values (?,?,?,?,?)''',[rightnow,gestureID,str(x),str(y),str(z)])
                # conn.commit()
                # c.close()

                # capture data for recognition later
                capData.append([0,int(x[0]),int(y[0]),int(z[0])])

            # print current values

            if classifying == False:
                cprint("Next gesture: " + gestureName + ", trace " + str(traceID),15,6)

            cprint("Current values:    " + str([x,y,z]),15,7)

        if ccc == ord('g') and capturing == False and classifying == False:
            screen.nodelay(0)
            curses.echo()
            cprint("Please input next gesture ID to be captured: ",5,9)
            screen.addstr(9,55, " "*3, curses.A_UNDERLINE)
            nextGesture = screen.getstr(9,55)
            curses.noecho()
            screen.nodelay(1)
            cprint(" "*100,5,9)
            if is_number(nextGesture):
                gestureID = int(nextGesture)
                gestureName = gestureList[gestureID]
                cprint("Idling. Next gesture captured will be ID " + str(gestureID),15,5)
                cprint("Next gesture: " + gestureName + ", trace " + str(traceID),15,6)

        if ccc == ord('n') and capturing == False and classifying == False:
            screen.nodelay(0)
            curses.echo()
            cprint("Please input next gesture's name: ",5,9)
            screen.addstr(9,55, " "*10, curses.A_UNDERLINE)
            gestureName = screen.getstr(9,55)
            curses.noecho()
            screen.nodelay(1)
            cprint("                                                       ",5,9)

        if ccc == ord('c') and capturing == False and classifying == False:
            classifying = True
            cprint("Classify Mode: " + str(classifying) + " Testing mode: " + str(testing),5,2)

        elif ccc == ord('c') and capturing == False and classifying == True:
            classifying = False
            cprint("Classify Mode: " + str(classifying) + " Testing mode: " + str(testing),5,2)

        if ccc == ord('t') and capturing == False and testing == True:
            testing = False
            cprint("Classify Mode: " + str(classifying) + " Testing mode: " + str(testing),5,2)

        elif ccc == ord('t') and capturing == False and testing == False:
            testing = True
            classifying = False
            gestureID = 0
            traceID = 0
            gestureName = gestureList[gestureID]
            cprint("Classify Mode: " + str(classifying) + " Testing mode: " + str(testing),5,2)

        if ccc == ord('b') and capturing == False and classifying == False:
            capturing = True

        if ccc == ord('s') and capturing == True and classifying == False:
            traceID += 1
            capturing = False
            cprint("Idling. Next gesture captured will be " + str(gestureID),15,5)

            c = conn.cursor()
            c.execute('''insert into capData values (?,?,?)''',[(gestureID-1),traceID,str(capData)])
            conn.commit()
            c.close()

            # do classification
            cresult = r.recognize(capData)
            cprint("Classification Result: " + str(cresult),15,9)

            # add as a trace
            if testing == False:
                r.addTemplate(gestureName,capData)

            capData = []

            if testing == True:
                if  gestureName in cresult:
                    score += 1.0
                else:
                    badClass.append("gID: " + str(gestureID) + " tID: " + str(traceID) +  " gName: " + gestureName)
                total += 1.0
                cprint(str(score) + "/" + str(total) + ", " + str(score/total*100) + "% accuracy",15,11)
                cprint("Bad Classifications: " + str(badClass),15,15)

        elif ccc == ord('s') and capturing == True and classifying == True:
            cresult = r.recognize(capData)
            cprint("Classification Result: " + str(cresult),15,9)
            capData = []

        # check to see if we're done with this gesture yet
        if (traceID == traces):
        # move onto the next gesture
            traceID = 0
            gestureID += 1
            # check to see if we're done capturing
            if (gestureID + 1) > len(gestureList):
                classifying = True
                cprint("Classify Mode: " + str(classifying),5,2)
            else:
                gestureName = gestureList[gestureID]

        elif ccc == ord('q'):
            ser.close()
            sys.exit(0)

if __name__ == "__main__":
    curses.wrapper(main)
