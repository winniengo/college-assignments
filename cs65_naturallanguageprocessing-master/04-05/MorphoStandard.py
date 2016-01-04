"""
Reads in a list and creates a dictionary of 1000 words and their segmentations
released as part of the Morpho Challenge 2010 workshop. Each key is a word
and the value is a list of the its segmentations.
"""
def createStandard():
    morpho = open('/data/cs65/morphology/segments.eng', 'r')
    standard = {}

    for line in morpho.readlines():
        line = line.strip().split()
        key = line[0]
        value = line[1:]
        standard[key] = value

    morpho.close()
    return standard

def createStandard2():
    morpho = open('/data/cs65/morphology/segments.eng', 'r')
    trainingSet = {}
    testingSet = {}

    i = 0
    lines = []
    for line in morpho.readlines():
        line = line.strip().split()
        lines.append(line)
    morpho.close()

    set1 = lines[:500]
    set2 = lines[500:]

    for line in set1:
        key = line[0]
        value = line[1:]
        trainingSet[key] = value

    for line in set2:
        key = line[0]
        value = line[1:]
        testingSet[key] = value

    return trainingSet, testingSet

def createOwnStandard():
    morpho = open('eval.txt', 'r')
    standard = {}
    
    lst = []
    for line in morpho.readlines():
        line = line.strip().split()
        if line[0] in lst:
            print(line[0])
        lst.append(line[0])
        key = line[0]
        value = line[1:]
        standard[key] = value

    morpho.close()
    return standard


def main():
    standard = createOwnStandard()
    items = list(standard.items())
    """
    for i in range(len(items)):
        print(i, items[i])
    """
if __name__== '__main__':
    main()



