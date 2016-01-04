#!/usr/bin/env python

"""
Code for supervised decision list classifier in Lab 06

Written by: Mike Superdock and Winnie Ngo
"""

import math
from operator import itemgetter

def createSenseFeatureDictionary(trainIDs, tweetData):

    dictionary = {}
    for tweetID in trainIDs: #tweetIDs for training
        words = tweetData["tweets"][tweetID]["words"]
        answers = tweetData["tweets"][tweetID]["answers"]
        
        for answer in answers:
            if dictionary.get(answer) == None:
                dictionary[answer] = dict()
            for word in words:
                if dictionary[answer].get(word) == None:
                    dictionary[answer][word] = 1
                else:
                    dictionary[answer][word] += 1
    return dictionary


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

    sentiments = sfDict.keys() # all sentiments in training data

    dictionary = {}
    for sentiment in sentiments:
        dictionary[sentiment] = dict()
        features = sfDict[sentiment].keys()
        for feature in features:
            #calculate numerator
            if sfDict[sentiment].get(feature) == None:
                numerCount = 0
            else:
                numerCount = sfDict[sentiment][feature]
            #calculate denominator
            denomCount = 0
            for sentiment2 in sentiments:
                if sentiment2 != sentiment:
                    val = sfDict[sentiment2].get(feature)
                    if val != None:
                        denomCount += val

            ratio = (float(numerCount) + a)/(denomCount + a)
            score = math.log(ratio)
            dictionary[sentiment][feature] = score
    return dictionary



"""
param: dictionaries of (sense, feature) pairs built using collocations and 
bag-of-words
    add-ons: k - None or int at which score falls below, we stop progressing 
    through the decision list 
return: dictionary of decision lists, which are sorted lists of (sense, feature)
pairs, for each word in from the training data. 
"""
def createDecisionList(scoreDict, k):
    sentiments = scoreDict.keys() 
    featureScoreList = []

    for sentiment in sentiments:
        features = scoreDict[sentiment].keys()
        for feature in features:
            featureTuple = (sentiment, feature)
            score = scoreDict[sentiment][feature]
            if k == None or score > k:
                featureScoreTuple = (featureTuple, score)
                featureScoreList.append(featureScoreTuple)

    finalScoreList = sorted(featureScoreList, key=itemgetter(1))
    finalList = [x for x, v in finalScoreList] # retreive sorted features
    return finalList[::-1]

"""
param: 
    testData - parsed testing data
    decisionTree - dictionary of decision lsits
    
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
def labelData(testIDs, tweetData, MFS, decisionList, maxRules):

    count = 0
    guessDictionary = {}

    for tweetID in testIDs: #tweet IDs for testing
        words = tweetData["tweets"][tweetID]["words"]
        answers = tweetData["tweets"][tweetID]["answers"]
        
        labelGuess = None
        rules = 1 #count of the number of rules considered
        for s, f in decisionList: #walk down the decision list
            if maxRules == None or rules <= maxRules:
                if f in words:
                    labelGuess = s
                    guessDictionary[tweetID] = labelGuess
                    break
            rules += 1

        if labelGuess == None: #no label, fall back on the MFS baseline
            guessDictionary[tweetID] = MFS
    return guessDictionary

"""
Analyze our results

param: 
    testData - parsed testing data
    guessDictionary - dictionary of sense labels using training data 
return: accuracy of supervised decision list classifier based on all of our 
guesses
"""
def examineResults(testIDs, tweetData, guessDictionary):
    totalCorrect = 0.0

    for tweetID in testIDs:
        answers = tweetData["tweets"][tweetID]["answers"]
        if guessDictionary[tweetID] in answers:
            totalCorrect += 1
    accuracy = totalCorrect/len(testIDs) * 100
    #print "%.4f" % accuracy
    return accuracy

"""
Retrieve most common words in dataset
param: data - dataset, num - number of most common words to return
return: lsit of most common words 
"""

def findMostCommonWords(trainIDs, tweetData, num):
    
    count = {}
    for tweetID in trainIDs:
        words = tweetData["tweets"][tweetID]["words"]
        for w in words: #accumulate count of words
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
def removeItemsFromDList(decisionList, removalItems):

    newDList = []
    for s, f in decisionList:
        if f not in removalItems:
            newDList.append((s,f))
    return newDList    

