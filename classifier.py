from Protractor3D import *

class Recognizer:

    templates = []
 
    def recognize(self, points):

        p = Protractor3D()
        topMatches = []

        currentTest = p.generate_template(points)
        '''bestDistance = float("infinity")
        bestTemplate = None'''
        for template in self.templates:
            distance = p.protractor3D_classify(currentTest,template.points)
            rotation = int(abs(distance[0]))
            '''print "Rotation " + str(rotation);'''
            if rotation < 30:
                # it's likely to be our gesture! 
                topMatches.append([int(distance[2]),template.name,rotation])
                topMatches.sort()
                if len(topMatches) > 5:
                    topMatches.pop()
            '''if distance < bestDistance:
                bestDistance = distance
                bestTemplate = template'''

        '''score = 1.0 - (bestDistance / (0.5 * math.sqrt(250.0 * 250.0 + 250.0 * 250.0)))
        if (score > 1) or (score < 0):
            bestTemplate.name = "None, MSE2:"
            score = bestDistance;
            '''
        return topMatches

    def addTemplate(self,name,points):
        self.templates.append(Template(name,points))
        return len([t for t in self.templates if t.name == name])

    def deleteTemplates(self,name):
        self.templates = [t for t in self.templates if t.name != name]
        return len(self.templates)

class Template:
    def __init__(self,name,points):
        self.name = name
        self.points = Protractor3D().generate_template(points)


def main():

    r = Recognizer()
    
    # hard coded templates

    sampleStomp =  [[0, 0,       0,    0],
                    [0, -5,      10,   9],
                    [0, -21,     -6,   -29],
                    [0, -23,     -3,   -39],
                    [0, -253,    12,   -211],
                    [0, -12,     -3,   -32],
                    [0, 0,       0,    0]]


    sampleFlickLeft =  [[0, 0,      0,      0],
                        [0, 21,     -3,     -16],
                        [0, 253,    -8,     -21],
                        [0, 186,    24,     -35],
                        [0, 13,     -8,     -12],
                        [0, 5,      2,      -6],
                        [0, 1,      0,      -13],
                        [0, 250,    -2,     -11],
                        [0, 3,      1,      -12],
                        [0, 0,      0,      0]]

    sampleFlickRight = [[0,0,0,0],
                        [0,249,4,-6],
                        [0,239,-18,-4],
                        [0,7,-1,5],
                        [0,8,-2,-3],
                        [0,11,2,-8],
                        [0,0,0,0]]

    sampleDoubleTap =  [[0,0,0,0],
                        [0,1,16,-20],
                        [0,248,199,11],
                        [0,222,56,-40],
                        [0,241,207,-218],
                        [0,248,-11,-4],
                        [0,253,-1,-4],
                        [0,254,0,-5],
                        [0,0,0,0]]

    sampleShake =  [[0,0,0,0],
                    [0,0,-1,-9],
                    [0,252,6,-3],
                    [0,221,32,-6],
                    [0,126.0,-9,-10],
                    [0,193,2,-199],
                    [0,54,61,-104],
                    [0,28,-3,-234],
                    [0,13,69,-66],
                    [0,7,18,8],
                    [0,0,0,0]]

    # hard coded test data

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
    '''
    r.addTemplate("tap foot", sampleStomp)
    r.addTemplate("flick left", sampleFlickLeft)
    r.addTemplate("flick right", sampleFlickRight)
    r.addTemplate("double tap", sampleDoubleTap)
    r.addTemplate("shake", sampleShake)
    '''
    r.addTemplate("fl", tr1)
    r.addTemplate("fr", tr2)
    r.addTemplate("fl2", tr3)
    r.addTemplate("fr2", tr4)

    # perform recognition on each test item    
    '''
    print r.recognize(testFlickLeft)
    print r.recognize(testFlickRight)
    print r.recognize(testDoubleTap)
    print r.recognize(testShake)
    '''
    print "should be fl" + str(r.recognize(tr5))
    print "should be fr" + str(r.recognize(tr6))
    print "should be fl" + str(r.recognize(tr7))


if __name__ == "__main__":
    main()
