#!/usr/bin/env python

"""
Code for supervised decision list classifier in Lab 06

Written by: Mike Superdock and Winnie Ngo
"""

from parse import getData
import math
from operator import itemgetter
from warmup import retrieveMostCommonSenses

"""
param: dictionary of parsed training data
    add-on: lower - True for implementating case-folding (makes all words
    lower-case)
return: dictionary of (sense, feature) pair and the number of times the 
feature is present in the sense per lexelt found in training data using
collocations
"""
def createSenseFeatureDictionary_C(trainData, lower):
    lexelts = trainData.keys() # all lexelts in training data

    lexeltDictionary = {} # dictionary of (sense, feature) pair
    # where lexeltDicationary[lexelt][sense][feature] = # of feature in sense  
    
    for lexelt in lexelts: 
        dictionary = {} 
        instances = trainData[lexelt].keys() # fetch all instances per lexelt
        for instance in instances:
            # fetch words, answers, heads per instance
            words = trainData[lexelt][instance]["words"]
            answers = trainData[lexelt][instance]["answers"] #or 'senses'
            heads = trainData[lexelt][instance]["heads"]

            wordRange = range(len(words))
            if lower: # convert all words to lower-case
                for i in wordRange:
                    words[i] = words[i].lower()

            for head in heads: 
                # build respective features per head
                feature1 = words[head-1] + " " + words[head]
                feature2 = words[head] + " " + words[head+1]
                for answer in answers: 
                    if dictionary.get(answer) == None:
                        dictionary[answer] = dict()
                    
                    for feature in [feature1, feature2]:
                        # accumulate count(feature is present in sense)
                        if dictionary[answer].get(feature) == None:
                            dictionary[answer][feature] = 1
                        else:
                            dictionary[answer][feature] += 1

        lexeltDictionary[lexelt] = dictionary 

    return lexeltDictionary

"""
param: 
    trainData - parsed training data
    k - bag-of-words constant

    add-on: lower - True for implementing case-folding
return: dictionary of (sense, feature) pair and the respective counts using
words in a bag-of-words
"""
def createSenseFeatureDictionary_B(trainData, k, lower):
    lexelts = trainData.keys()

    lexeltDictionary = {}
    
    for lexelt in lexelts: 
        dictionary = {} 
        instances = trainData[lexelt].keys() # fetch all instances per lexelt
        for instance in instances:
            # fetch words, answers, heads per instance
            words = trainData[lexelt][instance]["words"]
            answers = trainData[lexelt][instance]["answers"]
            heads = trainData[lexelt][instance]["heads"]

            wordRange = range(len(words))
            if lower: # convert all words to lower-case
                for i in wordRange:
                    words[i] = words[i].lower()

            for head in heads: 
                for answer in answers:
                    if dictionary.get(answer) == None:
                        dictionary[answer] = dict()
                    # accumulate count using words in bag-of-words
                    for i in range(head-k,head+k+1): 
                        if i == head:
                            continue
                        else:
                            if i in wordRange: # prevent out-of-bound index
                                w = words[i]
                                if dictionary[answer].get(w) == None:
                                    dictionary[answer][w] = 1
                                else:
                                    dictionary[answer][w] += 1

        lexeltDictionary[lexelt] = dictionary

    return lexeltDictionary

"""
param: dictionary of (sense, feature) pair per lexelt in training data
return: dictionary of score per (sense, feature) pair using the below equation,
which scores how good a feature is in distinguishing two senses using a ratio
of probabilities which is approximated by using maximum likelihood estimation

            ( count(f is present in sense(i))                        )
score = log (------------------------------------------------------- )
            ( count(f is present in all other senses except sense(i)))

we also use Laplace smoothing, adding alpha = 0.1 instead of +1 to both the
numerator and denominator
"""
def createScoreDictionary(sfDict):
    a = 0.1 # Laplace smoothing

    lexelts = sfDict.keys() # all lexelts in training data
    
    lexeltDictionary = {} # dictionary of score per (sense, feature) pair 
    # where lexeltDictionary[lexelt][sense][feature] = score 

    for lexelt in lexelts:
        dictionary = {}
        answers = sfDict[lexelt].keys()
        for answer1 in answers: # where answer1 = sense(i)
            dictionary[answer1] = dict()
            features = sfDict[lexelt][answer1].keys()
            for feature in features:
                # count(feature in sense) 
                numerCount = sfDict[lexelt][answer1][feature] 
                # count(feature in all other senses)
                denomCount = 0
                
                for answer2 in answers: # for all other senses 
                    if answer2 != answer1: # except sense(i)
                        val = sfDict[lexelt][answer2].get(feature) 
                        if val != None: 
                            denomCount += val # accumulate denominator 
                
                # calculate score
                ratio = (float(numerCount) + a)/(denomCount + a)
                score = math.log10(ratio)
                dictionary[answer1][feature] = score
        lexeltDictionary[lexelt] = dictionary
    
    return lexeltDictionary

"""
param: dictionaries of (sense, feature) pairs built using collocations and 
bag-of-words
    add-ons: k - None or int at which score falls below, we stop progressing 
    through the decision list 
return: dictionary of decision lists, which are sorted lists of (sense, feature)
pairs, for each word in from the training data. 
"""
def createDecisionDict(scoreDict1, scoreDict2, k):
    lexeltDictionary = {}

    lexelts = scoreDict1.keys() # all lexelts from training data
    for lexelt in lexelts:
        featureScoreList = []
        for scoreDict in [scoreDict1, scoreDict2]: # [collocation, bag-of-words]
            answers = scoreDict[lexelt].keys() # all senses
            for answer in answers:
                features = scoreDict[lexelt][answer].keys()
                for feature in features:
                    featureTuple = (answer, feature)
                    score = scoreDict[lexelt][answer][feature]
                    if k == None or score > k: # add-on 
                        featureScoreTuple = (featureTuple, score)
                        featureScoreList.append(featureScoreTuple)

        # sort features by max score
        finalScoreList = sorted(featureScoreList, key=itemgetter(1))
        finalList = [x for x, v in finalScoreList] # retreive sorted features
        lexeltDictionary[lexelt] = finalList[::-1] # append to decision dict

    return lexeltDictionary

"""
param: 
    testData - parsed testing data
    decisionTree - dictionary of decision lsits
    k - bag-of-words constant
    
    add-on: maxRules - None or int of rules at which we stop progressing through
    the decision list
return: dictionary[lexelt][instance[ = sense label using training data

Use the decision list on the test data, beginning with an instance (the 
item in the test data that includes the text and the identified head word) of a
word. Walk down the decision list and if the instance contains the 1st 
feature, label the instance as that sense. If not, proceed to the next 
feature and continue this process until all features in the deccision list 
have been exhausted. If this occurs, label the instance with the MFS from the 
training data
"""
def labelData(testData, decisionTree, k, maxRules):
    count = 0
    mostCommonTrainSenses = retrieveMostCommonSenses(trainData) # MSF baseline
    lexelts = testData.keys() # all lexelts in test data

    guessDictionary = {}
    for lexelt in lexelts:
        instances = testData[lexelt].keys()
        dTree = decisionTree[lexelt]
        guessDictionary[lexelt] = dict()

        for instance in instances:
            words = testData[lexelt][instance]["words"]
            heads = testData[lexelt][instance]["heads"]
            wordRange = range(len(words))
            featureList = []
            for head in heads: # build features
                feature1 = words[head-1] + " " + words[head]
                feature2 = words[head] + " " + words[head+1]
                featureList.append(feature1)
                featureList.append(feature2)
                for i in range(head-k,head+k+1):
                    if i != head and i in wordRange:
                        featureList.append(words[i])

            labelGuess = None
            # walk down the decision list
            rules = 1 # count of rules considered
            for s, f in dTree:
                if maxRules == None or rules <= maxRules: # add-on
                    if f in featureList:
                        labelGuess = s
                        guessDictionary[lexelt][instance] = labelGuess
                        break
                rules += 1

            if labelGuess == None: # no label, fall back on the MFS baseline
                guessDictionary[lexelt][instance] = \
                        mostCommonTrainSenses[lexelt][0]
    return guessDictionary

"""
Analyze our results

param: 
    testData - parsed testing data
    guessDictionary - dictionary of sense labels using training data 
return: accuracy of supervised decision list classifier based on all of our 
guesses
"""
def examineResults(testData, guessDictionary):
    totalCorrect = 0
    totalGuesses = 0

    lexelts = testData.keys()
    for lexelt in lexelts:
        instances = testData[lexelt].keys()
        for instance in instances:
            answers = testData[lexelt][instance]["answers"]
            if guessDictionary[lexelt][instance] in answers:
                totalCorrect += 1
        totalGuesses += len(instances)
    accuracy = float(totalCorrect)/totalGuesses * 100
    print "%.1f" % accuracy

"""
Retrieve most common words in dataset
param: data - dataset, num - number of most common words to return
return: lsit of most common words 
"""

def findMostCommonWords(data, num):
    words = []
    lexelts = data.keys()
    for lexelt in lexelts:
        instances = data[lexelt].keys()
        for instance in instances:
            words += data[lexelt][instance]["words"]

    count = {}
    for w in words: # accumulate count of words
        if count.get(w) == None:
            count[w] = 1
        else:
            count[w] += 1

    wordCountPairs = count.items()
    # sort list to retrieve words with the highest counts
    sortedWordCountPairs = sorted(wordCountPairs, key=itemgetter(1))
    sortedWordCountPairs = sortedWordCountPairs[::-1]
    commonWords = [x for x, v in sortedWordCountPairs]

    if num < len(sortedWordCountPairs):
        return commonWords[:num]
    else:
        return commonWords

"""
Exclude "stopwords", very common words, from being used as part of features
param: list of stopwords to remove
return: dictionary of updated decision trees 
"""
def removeItemsFromDTree(decisionDict, removalItems):
    lexelts = decisionDict.keys()
    for lexelt in lexelts:
        dTree = decisionDict[lexelt]
        newDTree = [] # revised dictionary list 
        for sense, feature in dTree:
            keepFeature = True
            featureElements = feature.split()
            for element in featureElements:
                if element in removalItems: # don't append words in list 
                    keepFeature = False
                    continue
            if keepFeature:
                newDTree.append((sense,feature))
        decisionDict[lexelt] = newDTree

    return decisionDict

# ****************************************************************************
# LAB QUESTIONS
# ****************************************************************************
"""
Apply decision lists to the test data; display results.
"""
def question12(trainData, testData):
    # build (sense, feature) dictionary and score dictionary for collocations
    sfDict_C = createSenseFeatureDictionary_C(trainData, False)
    scoreDict_C = createScoreDictionary(sfDict_C)

    # build sense feature dictionary and score dictionary for bag of words
    for k in range(10):
        sfDict_B = createSenseFeatureDictionary_B(trainData, k, False)
        scoreDict_B = createScoreDictionary(sfDict_B)
    
        #create decision tree
        decisionDict = createDecisionDict(scoreDict_C, scoreDict_B, None)

        # use decision lists on the testing data and analyze results
        guessDictionary = labelData(testData, decisionDict, k, None)
        # calculate and displace accuracy 
        print k, ':',
        examineResults(testData, guessDictionary)
    print

"""
Change decision lists so that a given number i of very common words are 
excluded from being used as part of features. Apply to the test data; display 
results. "Very common" words are those that appear most frequently in the 
training data, which we calculate 
for.
"""
def question13a(trainData, testData, i):
    print "exclude", i, "most common 'stopwords' from features:"

    sfDict_C = createSenseFeatureDictionary_C(trainData, False)
    scoreDict_C = createScoreDictionary(sfDict_C)

    for k in range(10):
        sfDict_B = createSenseFeatureDictionary_B(trainData, k, False)
        scoreDict_B = createScoreDictionary(sfDict_B)
        decisionDict = createDecisionDict(scoreDict_C, scoreDict_B, None)
    
        # find k most common words in training set
        mostCommonWords = findMostCommonWords(trainData, i)
        # exclude these words from being used as part of features
        decisionDict = removeItemsFromDTree(decisionDict, mostCommonWords)

        # use decision lists on the testing data and analyze results
        guessDictionary = labelData(testData, decisionDict, k, None)
        print k, ':',
        examineResults(testData, guessDictionary)
    print 

"""
Implement 'case-folding'. In other words, all words and thus features are made
lower-case and apply resulting decision lists to test data. Display results.
""" 
def question13b(trainData, testData):
    print "implement case-folding:"

    # build (sense, feature) dictionary and score dictionary for collocations
    # where everything is lower-case
    sfDict_C = createSenseFeatureDictionary_C(trainData, True)
    scoreDict_C = createScoreDictionary(sfDict_C)

    for k in range(10):
        # build dictionaries for bag-of-words where everything is lower-case
        sfDict_B = createSenseFeatureDictionary_B(trainData, k, True)
        scoreDict_B = createScoreDictionary(sfDict_B)
        decisionDict = createDecisionDict(scoreDict_C, scoreDict_B, None)
    
        # use decision lists on the testing data and analyze results
        guessDictionary = labelData(testData, decisionDict, k, None)
        print k, ':',
        examineResults(testData, guessDictionary)
    print 

"""
Apply decision lists to the test data, however when walking down decision lists
stop when score falls below a given threshold i. Display results.
"""
def question14a(trainData, testData, i):
    print "end decision list when score <", i, ":"

    sfDict_C = createSenseFeatureDictionary_C(trainData, False)
    scoreDict_C = createScoreDictionary(sfDict_C)
    
    for k in range(10):
        sfDict_B = createSenseFeatureDictionary_B(trainData, k, False)
        scoreDict_B = createScoreDictionary(sfDict_B)
        decisionDict = createDecisionDict(scoreDict_C, scoreDict_B, i)
    
        # use decision lists on the testing data and analyze results
        guessDictionary = labelData(testData, decisionDict, k, None)
        print k, ':',
        examineResults(testData, guessDictionary)
    print

""" 
Apply decision lists to the test data, however when walking down decision lists
stop after seeing i, a given number of, rules. Display results.
"""
def question14b(trainData, testData, i):
    print "stop after seeing", i, "rules:"

    sfDict_C = createSenseFeatureDictionary_C(trainData, False)
    scoreDict_C = createScoreDictionary(sfDict_C)
    
    for k in range(10):
        sfDict_B = createSenseFeatureDictionary_B(trainData, k, False)
        scoreDict_B = createScoreDictionary(sfDict_B)
        decisionDict = createDecisionDict(scoreDict_C, scoreDict_B, None)
    
        # use decision lists on the testing data and analyze results
        # stop after seeing i rules
        guessDictionary = labelData(testData, decisionDict, k, i)
        print k, ':',
        examineResults(testData, guessDictionary)
    print


###############################################################################
if __name__=='__main__':

    #retreive and parse training and testing data
    trainingFile = '/data/cs65/senseval3/train/EnglishLS.train'
    trainData = getData(trainingFile)

    testingFile = '/data/cs65/senseval3/test/EnglishLS.test'
    testData = getData(testingFile)

    print "Training File Load Complete"
    
    # apply supervised decision list classifier built using training data 
    # on test data; display results
    print "\nQuestion 12:\n"
    question12(trainData, testData)

    print "\nQuestion 13:\n"
    question13a(trainData, testData, 10) 
    question13a(trainData, testData, 20) 
    question13a(trainData, testData, 30) 
    
    question13b(trainData, testData)
    
    print "\nQuestion 14:\n"
    question14a(trainData, testData, -1)
    question14a(trainData, testData, -0.5)
    question14a(trainData, testData, 0)
    question14a(trainData, testData, 0.5)
    question14a(trainData, testData, 1.0)

    question14b(trainData, testData, 0)
    question14b(trainData, testData, 25)
    question14b(trainData, testData, 50)
    question14b(trainData, testData, 100)
    question14b(trainData, testData, 150)
    

