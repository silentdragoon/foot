import serial, array, select, sys, math, sqlite3, curses
from datetime import datetime
from classifier import *

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
    
    r = Recognizer()
    gestureName = "Stomp"
    
    blank = [[0,0,0,0],[0,5,5,5],[0,0,0,0]]
    r.addTemplate("blank",blank)
    
    # Add some default templates :)
    '''
    sampleStomp=[[0,0,0,0],[0,-5,10,9],[0,-21,-6,-29],[0,-23,-3,-39],[0,-253,12,-211],[0,-12,-3,-32],[0,0,0,0]]
    sampleFlickLeft=[[0,0,0,0],[0,21,-3,-16],[0,253,-8,-21],[0,186,24,-35],[0,13,-8,-12],[0,5,2,-6],[0,1,0,-13],[0,250,-2,-11],[0,3,1,-12],[0,0,0,0]]
    sampleFlickRight=[[0,0,0,0],[0,249,4,-6],[0,239,-18,-4],[0,7,-1,5],[0,8,-2,-3],[0,11,2,-8],[0,0,0,0]]
    sampleDoubleTap=[[0,0,0,0],[0,1,16,-20],[0,248,199,11],[0,222,56,-40],[0,241,207,-218],[0,248,-11,-4],[0,253,-1,-4],[0,254,0,-5],[0,0,0,0]]
    sampleShake=[[0,0,0,0],[0,0,-1,-9],[0,252,6,-3],[0,221,32,-6],[0,126.0,-9,-10],[0,193,2,-199],[0,54,61,-104],[0,28,-3,-234],[0,13,69,-66],[0,7,18,8],[0,0,0,0]]

    testFlickLeft =     [[0,0,0,0],[0,21,-3,-16],[0,255,-8,-21],[0,195,25,-38],[0,14,-8,-12],[0,5,3,-6],[0,1,1,-16],[0,256,-1,-5],[0,3,2,-12],[0,0,1,0]]
    testFlickRight =    [[0,0,0,0],[0,250,4,-6],[0,239,-18,-4],[0,7,-1,5],[0,8,-2,-3],[0,14,2,-8],[0,0,0,0]]
    testDoubleTap =     [[0,0,0,0],[0,1,16,-20],[0,250,199,11],[0,222,56,-40],[0,241,207,-218],[0,250,-14,-4],[0,253,-1,-4],[0,244,5,-5],[0,0,0,0]]
    testShake =         [[0,0,0,0],[0,0,-1,-9],[0,260,6,-3],[0,230,32,-6],[0,140.0,-9,-10],[0,193,2,-199],[0,54,50,-104],[0,28,-3,-234],[0,13,78,-66],[0,7,18,8],[0,0,0,0]]
                    
    tr1 = [[0, 0.0, 0.0, -1.0], [0, 1.0, 0.0, -2.0], [0, 1.0, 0.0, -2.0], [0, 1.0, 1.0, -4.0], [0, 1.0, 2.0, -5.0], [0, 6.0, 10.0, -5.0], [0, -241.0, 32.0, 15.0], [0, -223.0, -23.0, -216.0], [0, -222.0, 13.0, -196.0], [0, -21.0, 16.0, 12.0], [0, -23.0, -1.0, -12.0], [0, -50.0, 2.0, -34.0], [0, -40.0, -18.0, -39.0], [0, 4.0, -11.0, 4.0], [0, -194.0, -12.0, -210.0], [0, -217.0, 4.0, -224.0], [0, -37.0, 36.0, 8.0], [0, -164.0, 49.0, -20.0], [0, -10.0, -2.0, 9.0], [0, 3.0, 6.0, 4.0], [0, 2.0, 0.0, 0.0], [0, 1.0, 1.0, -1.0], [0, 1.0, 0.0, -5.0], [0, 5.0, 1.0, -2.0], [0, 1.0, 0.0, -2.0], [0, 2.0, 0.0, -2.0]]
    tr2 = [[0, 1.0, 0.0, -2.0], [0, 3.0, 1.0, -5.0], [0, 6.0, 2.0, -9.0], [0, 9.0, 19.0, -33.0], [0, -65.0, 16.0, -40.0], [0, -12.0, 207.0, -44.0], [0, -1.0, -10.0, 19.0], [0, -2.0, 20.0, -209.0], [0, -9.0, 20.0, -212.0], [0, 0.0, 17.0, -213.0], [0, -29.0, 12.0, 18.0], [0, -13.0, -2.0, -3.0], [0, 7.0, -33.0, -31.0]]
    tr3 = [[0, 2.0, 0.0, -2.0], [0, 5.0, 0.0, 0.0], [0, 2.0, 3.0, -7.0], [0, -3.0, 8.0, 1.0], [0, -170.0, 17.0, 26.0], [0, -204.0, 39.0, -210.0], [0, -11.0, 15.0, -2.0], [0, -33.0, 9.0, -16.0], [0, -52.0, -20.0, -37.0], [0, -9.0, -34.0, -28.0], [0, 5.0, -26.0, -14.0], [0, 5.0, 18.0, 18.0], [0, -215.0, 20.0, -183.0]]
    tr4 = [[0, 1.0, 1.0, 1.0], [0, 2.0, 4.0, -13.0], [0, 0.0, 19.0, -13.0], [0, -25.0, 1.0, -44.0], [0, -4.0, -16.0, 3.0], [0, -234.0, -6.0, -193.0], [0, -24.0, -10.0, -213.0], [0, -13.0, -3.0, -219.0], [0, 0.0, -15.0, 17.0], [0, 3.0, -14.0, 1.0], [0, -85.0, 21.0, -51.0], [0, -3.0, -16.0, 14.0]]
    tr5 = [[0, -2.0, 0.0, -3.0], [0, 1.0, 1.0, -6.0], [0, 3.0, 5.0, 1.0], [0, -231.0, 22.0, -202.0], [0, 7.0, 0.0, 7.0], [0, 8.0, 19.0, -216.0], [0, -51.0, 26.0, -2.0], [0, -37.0, 1.0, -25.0], [0, 7.0, -38.0, -27.0], [0, 1.0, -38.0, -31.0], [0, 5.0, -11.0, -11.0], [0, -5.0, 12.0, -13.0], [0, -242.0, 58.0, -170.0], [0, -215.0, -13.0, -212.0], [0, -45.0, -21.0, -30.0], [0, -243.0, 6.0, 13.0]]
    tr6 = [[0, 0.0, 1.0, 3.0], [0, 4.0, 3.0, -1.0], [0, 4.0, 7.0, -5.0], [0, -4.0, 21.0, -32.0], [0, -15.0, 5.0, -6.0], [0, -2.0, -28.0, -23.0], [0, -241.0, -7.0, -219.0], [0, -25.0, 3.0, -213.0], [0, -27.0, 7.0, -204.0], [0, -13.0, 3.0, -222.0], [0, -15.0, -3.0, 9.0], [0, -2.0, -11.0, -8.0], [0, -244.0, -18.0, -9.0]]
    tr7 = [[0, 0.0, 0.0, -2.0], [0, 3.0, 0.0, -1.0], [0, 1.0, 1.0, -5.0], [0, -7.0, 4.0, -4.0], [0, 1.0, 16.0, 10.0], [0, -187.0, 18.0, 28.0], [0, -221.0, 20.0, -218.0], [0, -10.0, 8.0, 24.0], [0, -11.0, -1.0, 5.0], [0, -35.0, -22.0, -69.0], [0, -28.0, -21.0, -40.0], [0, -11.0, -12.0, -16.0], [0, 9.0, 9.0, 26.0], [0, -223.0, 20.0, -215.0], [0, -11.0, 76.0, -186.0]]

    
    # add these to a dict of templates

    r.addTemplate("tap foot", sampleStomp)
    r.addTemplate("flick left", sampleFlickLeft)
    r.addTemplate("flick right", sampleFlickRight)
    r.addTemplate("double tap", sampleDoubleTap)
    r.addTemplate("shake", sampleShake)
    
    r.addTemplate("flick left",testFlickLeft)
    r.addTemplate("flick right",testFlickRight)
    r.addTemplate("double tap",testDoubleTap)
    r.addTemplate("shake",testShake)
    
    r.addTemplate("flick left", tr1)
    r.addTemplate("flick right", tr2)
    r.addTemplate("flick left", tr3)
    r.addTemplate("flick right", tr4)
    r.addTemplate("flick left", tr5)
    r.addTemplate("flick right", tr6)
    r.addTemplate("flick left", tr7)
    '''
    
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
            
                cprint("Capturing gesture " + str(gestureID) + "                                       ",15,5)
                c = conn.cursor()
                c.execute('''insert into acceldata values (?,?,?,?,?)''',[rightnow,gestureID,x,y,z])
                conn.commit()
                c.close()
                
                # capture data for recognition later
                
                capData.append([0,x,y,z])

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
