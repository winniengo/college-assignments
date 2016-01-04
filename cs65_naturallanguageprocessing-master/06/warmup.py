#!/usr/bin/env python
""" 
Code and answers to discussion questions 1-11 to Lab 6

Written by: Mike Superdock and Winnie Ngo
"""

"""
Exploring the training data ---------------------------------------------------
Question 1:

    There are 57 different lexelts.

Question 2:

    There are 20 nouns, 32 verbs, and 5 adjectives.

Question 3:

    There are 112 training examples for the noun "organization".

Question 4:

    There are 4 senses of organization.n represented in the training data.

Question 5:

    If you just guessed randomly, you would label about 21% of the words in
    the training data correctly.

Question 6:

    The most frequent sense for organization.n is organization%1:14:00::

Question 7:

    You label about 57% of the words correctly using the most frequent tag
    from the training data to label the training data. This is lower than
    expected, in our opinion. We assume that a particular word would have
    primarily one sense the majority of the times it appears.

    Note: the calculations for question 7 were done using the same scoring
    method proposed for question 11.

Exploring the test data -------------------------------------------------------
Question 8:

    There are 56 examples of organization.n in the test data

Question 9:

    (a) The following sense was found in the training set for organization.n
    but not in the testing set: 'organization%1:04:00::'. This is generally
    not a problem. All this suggests is that our training set contains extra
    information that is not necessary to label our testing set.

    (b) The following senses were found in the testing set for organizaiton.n
    but not in the training set: 'organization%1:07:00::' and
    'organization%1:04:01::'. This presents a problem because we have no way 
    of accurately predicting senses such as these two in the testing set if 
    we never actually encouter them in the training set.

Question 10:

    77% of the words have the same most frequent sense in the training data and
    the test data. 

    This suggests that it is not uncommon for the most common sense to
    differ between the training set and the testing set--it happens about
    23% of the time. This trend indicates that the most common sense from the
    training set will not always be the most accurate predictor in the testing
    set.

    Note: To handle most frequent sense ties , we considered any and all
    them in our final matching. If any of the most frequent senses in the
    training set matched any of the most frequent senses in the testing set
    for a single lexelt, we counted that as a match.

Question 11:

    This method predicted about 55% percent of words correctly in the
    testing set. This is exactly the result we expected. It performed
    better than our random predictor (21%) and slightly worse than the MFS
    baseline (57%).

    We know that the most common sense is identical between lexelts in the
    training set and the testing set a majority of the time (77%). For these
    words we expect this MFS labeler to perform about as well on the testing
    set as it did on the training set. For the other words we expect that it
    will only perform slightly worse for the testing set. These expectations
    were met by our results, which showed that of all senses in the testing
    set only 2% less were predicted accurately relative to the MFS baseline.
"""

from parse import getData
from collections import Counter
import numpy

def question1(trainData):

    print len(trainData.keys())
    return

def question2(trainData):
    
    keys = trainData.keys()
    vCount = 0
    aCount = 0
    nCount = 0
    for k in keys:
        if ('n' == k[-1]):
            nCount += 1
        elif ('a' == k[-1]):
            aCount += 1
        else:
            vCount += 1
    print "aCount: %d" % (aCount)
    print "nCount: %d" % (nCount)
    print "vCount: %d" % (vCount)
    return

def question3(trainData):

    print len(trainData[u'organization.n'].keys())
    return

def question4(trainData):

    keys = trainData[u'organization.n'].keys()
    senseList = []
    for k in keys:
        senseList += trainData[u'organization.n'][k]["answers"]
    senseList = set(senseList)
    if 'U' in senseList:
        senseList.remove('U')

    print len(senseList)
    return

def question5(trainData):
    
    instanceTotal = 0
    correctGuessTotal = 0
    lexelts = trainData.keys()
    for lexelt in lexelts:
        instances = trainData[lexelt].keys() #retrieve all instances
        senseList = []
        for instance in instances: #retrieve all senses of the lexelt
            senseList += trainData[lexelt][instance]["answers"]
        senseList = set(senseList) #find the set of senses of lexelt
        if 'U' in senseList:       #remove 'U' from senses
            senseList.remove('U')
        instanceTotal += len(instances)
        correctGuessTotal += float(len(instances))/len(senseList)
   
    print correctGuessTotal/instanceTotal * 100

def question6(trainData):
    
    counter = {}
    instances = trainData[u'organization.n'].keys()
    senses = []
    for instance in instances:
        senses = trainData[u'organization.n'][instance]["answers"]
        for sense in senses:
            val = counter.get(sense)
            if val == None:
                counter[sense] = 1
            else:
                counter[sense] += 1
    items = counter.items()
    keys = []
    vals = []
    for key, val in items:
        keys.append(key)
        vals.append(val)
    maxKey = keys[numpy.argmax(vals)]
    print maxKey

def question8(testData):

    print len(testData[u'organization.n'].keys())

def question9(trainData, testData):

    trainSenses = []
    testSenses = []
    instances = trainData[u'organization.n'].keys()
    for instance in instances:
        trainSenses += trainData[u'organization.n'][instance]["answers"]
    instances = testData[u'organization.n'].keys()
    for instance in instances:
        testSenses += testData[u'organization.n'][instance]["answers"]

    trainSensesSet = set(trainSenses)
    testSensesSet = set(testSenses)
    unsharedSenses1 = []
    for sense in trainSenses:
        if not sense in testSenses:
            unsharedSenses1.append(sense)
    unsharedSenses2 = []
    for sense in testSenses:
        if not sense in trainSenses:
            unsharedSenses2.append(sense)

    print "Senses found in training set but not in testing set:",unsharedSenses1
    print "Senses found in testing set but not in training set:",unsharedSenses2

    """
    the senses found in training set but not in the testing set don't matter!
    they won't causes us any problems. They just give us extra information
    
    the senses found in the testing set but not in the training set will cause
    problems. When we are testing, we will have to find ways to handle senses
    that we have not encountered in our training set
    """

def retrieveMostCommonSenses(data):

    lexelts = data.keys()
    mostCommonSenses = {}
    for lexelt in lexelts:
        counter = {}
        instances = data[lexelt].keys()
        for instance in instances:
            senses = data[lexelt][instance]["answers"]
            for sense in senses:
                if counter.get(sense) == None:
                    counter[sense] = 1
                else:
                    counter[sense] += 1
        items = counter.items()
        senseList = []
        countList = []
        for k, v in items:
            senseList.append(k)
            countList.append(v)
        maxCount = max(countList)
        for i in range(len(countList)):
            if countList[i] == maxCount:
                if mostCommonSenses.get(lexelt) == None:
                    mostCommonSenses[lexelt] = [senseList[i]]
                else:
                    mostCommonSenses[lexelt] += senseList[i]
    return mostCommonSenses

def question10(trainData, testData):

    trainSenses = retrieveMostCommonSenses(trainData)
    testSenses = retrieveMostCommonSenses(testData)
    
    matchCount = 0
    trainKeys = trainSenses.keys()
    for key in trainKeys:
        commonTrainSenses = trainSenses[key]
        commonTestSenses = testSenses[key]
        match = False
        for sense in commonTrainSenses:
            if sense in commonTestSenses:
                match = True
        if match == True:
            matchCount += 1

    print float(matchCount)/len(trainKeys) * 100

    """
    it is not uncommon for the most common sense to differ between sets.
    This happens about 23% of the time. This trend indicates that using
    our most common sense in the training set will not always be the
    most accurate predictor of the accurate sense for a word in the
    testing set
    """ 

def question11(trainData, testData):
    
    totalCorrect = 0
    totalGuesses = 0

    trainSenses = retrieveMostCommonSenses(trainData)
    lexelts = testData.keys()
    for lexelt in lexelts:
        instances = testData[lexelt].keys()
        for instance in instances:
            senses = testData[lexelt][instance]["answers"]
            if trainSenses[lexelt][0] in senses:
                totalCorrect += 1
            totalGuesses += 1

    print float(totalCorrect)/totalGuesses * 100
        

if __name__=='__main__':
    trainingFile = '/data/cs65/senseval3/train/EnglishLS.train'
    trainData = getData(trainingFile)
    testingFile = '/data/cs65/senseval3/test/EnglishLS.test'
    testData = getData(testingFile)
    
    # questions on training data
    print "\nQuestion 1:\n"
    question1(trainData)
    print "\nQuestion 2:\n"
    question2(trainData)
    print "\nQuestion 3:\n"
    question3(trainData)
    print "\nQuestion 4:\n"
    question4(trainData)
    print "\nQuestion 5:\n"
    question5(trainData)
    print "\nQuestion 6:\n"
    question6(trainData)
    print "\nQuestion 7:\n"          #we used the same methodology employed
    question11(trainData, trainData) #in question 11 to answer question 7

    # questions on testing data
    print "\nQuestion 8:\n"
    question8(testData)
    print "\nQuestion 9:\n"
    question9(trainData, testData)
    print "\nQuestion 10:\n"
    question10(trainData, testData)
    print "\nQuestion 11:\n"
    question11(trainData, testData)


