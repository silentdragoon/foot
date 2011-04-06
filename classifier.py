from Protractor3D import *

class Recognizer:

    templates = []
 
    def recognize(self, points):

        p = Protractor3D()

        currentTest = p.generate_template(points)
        bestDistance = float("infinity")
        bestTemplate = None
        for template in self.templates:
            distance = p.protractor3D_classify(currentTest,template.points)[2]
            if distance < bestDistance:
                bestDistance = distance
                bestTemplate = template

        score = 1.0 - (bestDistance / (0.5 * math.sqrt(250.0 * 250.0 + 250.0 * 250.0)))

        return bestTemplate.name, score

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

    # add these to a dict of templates

    r.addTemplate("tap foot", sampleStomp)
    r.addTemplate("flick left", sampleFlickLeft)

    # hard coded test data

    testStomp    = [[0, 0,       0,    0],
                    [0, -6,      10,   3],
                    [0, -21,     -8,   -30],
                    [0, -25,     -3,   -42],
                    [0, -250,    14,   -212],
                    [0, -14,     -4,   -32],
                    [0, 0,       0,    0]]

    testFlickLeft =    [[0, 0,      0,      0],
                        [0, 21,     -3,     -16],
                        [0, 255,    -8,     -21],
                        [0, 195,    25,     -38],
                        [0, 14,     -8,     -12],
                        [0, 5,      3,      -6],
                        [0, 1,      1,      -16],
                        [0, 256,    -1,     -5],
                        [0, 3,      2,      -12],
                        [0, 0,      1,      0]]

    # generate template for current test
    # go through dict of templates
    # doing classification of current test against each item

    print r.recognize(testStomp)
    print r.recognize(testFlickLeft)


if __name__ == "__main__":
    main()
