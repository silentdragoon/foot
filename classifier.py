from Protractor3D import *

def main():

    p = Protractor3D()

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

    templates = {}
    templates["tap foot"] = p.generate_template(sampleStomp)
    templates["flick left"] = p.generate_template(sampleFlickLeft)    


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

    currentTest = p.generate_template(testFlickLeft)

    # go through dict of templates
    # doing classification of current test against each item

    result1 = p.protractor3D_classify(currentTest,templates["tap foot"])
    result2 = p.protractor3D_classify(currentTest,templates["flick left"])

    if result1[2] < result2[2]:
        print "gesture is tap foot"
    else:
        print "gesture is flick left"


if __name__ == "__main__":
    main()
