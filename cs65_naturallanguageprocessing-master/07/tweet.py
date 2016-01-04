from parseTweet import parse_tweets
from crossVal import crossValidation
from operator import itemgetter
from declist import *
from naivebayes import *
import string

# open-source tokenization
import sys
sys.path.append('/data/cs65/semeval-2015/arktweet/')
from arktweet import tokenize

"""
conflate neutral sentiments into a single sentiment as in Q2 for dataset
"""
def tokenizeData(tweetData):
    newData = {}
    newData['tweets'] = {}

    tweetIDs = tweetData['tweets'].keys()
    listTweets = []
    for tweetID in tweetIDs:
        listTweets.append(' '.join(tweetData['tweets'][tweetID]['words']))

    tokenizedTweets = tokenize(listTweets)
    for i in range(len(tweetIDs)):
        tweetID = tweetIDs[i]
        words = tokenizedTweets[i].split()
        sentiments = tweetData['tweets'][tweetID]['answers']

        newData['tweets'][tweetID] = {}
        newData['tweets'][tweetID]['answers'] = sentiments
        newData['tweets'][tweetID]['words'] = words

    return newData
    

def conflateData(tweetData):
    newData = {}
    newData['tweets'] = {}

    tweetIDList = tweetData['tweets'].keys()
    for tweetID in tweetIDList:
        sentiments = tweetData['tweets'][tweetID]['answers']
        words = tweetData['tweets'][tweetID]['words']

        newData['tweets'][tweetID] = {}
        newData['tweets'][tweetID]['words'] = words

        # conflate neutral sentiments into a single sentimentas in Q2
        if 'objective' in sentiments or 'neutral' in sentiments:
            newData['tweets'][tweetID]['answers'] = ['neutral']
        else:
            newData['tweets'][tweetID]['answers'] = sentiments


    return newData

def lowerData(tweetData):
    newData = {}
    newData['tweets'] = {}

    tweetIDs = tweetData['tweets'].keys()
    for tweetID in tweetIDs:
        sentiments = tweetData['tweets'][tweetID]['answers']
        words = tweetData['tweets'][tweetID]['words']

        newData['tweets'][tweetID] = {}
        newData['tweets'][tweetID]['answers'] = sentiments

        newWords = []
        for i in range(len(words)):
            newWords.append(words[i].lower())
        newData['tweets'][tweetID]['words'] = newWords
    return newData


def negateData(tweetData, negateWordsList):
    newData = {}
    newData['tweets']= {}

    tweetIDs = tweetData['tweets'].keys()
    for tweetID in tweetIDs:
        sentiments = tweetData['tweets'][tweetID]['answers']
        words = tweetData['tweets'][tweetID]['words']

        newWords = []
        negation = False
        for w in words:

            #append words
            if negation:
                newWords.append('NOT_' + w)
            else:
                newWords.append(w)
            
            #set negation to True or False
            if w.lower() in negateWordsList or w.lower()[-3:] == "n't":
                negation = True
            elif w[-1] in string.punctuation:
                negation = False

        newData['tweets'][tweetID] = {}
        newData['tweets'][tweetID]['answers'] = sentiments
        newData['tweets'][tweetID]['words'] = newWords
    return newData


def mostFrequentSent(tweetIDList, tweetData):
    sentDictionary = {}
    for tweetID in tweetIDList: 
        sentiments = tweetData['tweets'][tweetID]['answers']
            
        # count sentiments
        for sentiment in sentiments:
            if sentDictionary.get(sentiment) == None:
                sentDictionary[sentiment] = 1
            else:
                sentDictionary[sentiment] += 1

    # sort sentiments by count, add most frequent to dictionary
    sentList = sorted(sentDictionary.items(), key=itemgetter(1))
    return sentList[-1] #returns most frequent sentiment

def calculateDiscount(trainFolds, testFolds, tweetData):

    DTotal = 0
    TTotal = 0
    UTotal = 0
    for i in range(len(trainFolds)):
        trainFold = trainFolds[i]
        testFold = testFolds[i]
        trainFeatures = []
        testFeatures = []
        for trainID in trainFold:
            trainFeatures += tweetData['tweets'][trainID]['words']
        for testID in testFold:
            testFeatures += tweetData['tweets'][testID]['words']
        #print trainFeatures
        #print testFeatures
        trainSet = set(trainFeatures)
        testSet = set(testFeatures)
        T = float(len(trainSet))
        U = 0.0
        for item in testSet:
            #print item
            if not item in trainSet:
                U += 1.0
        D = (1/((10*T/U) + 1))
        DTotal += D
        TTotal += T
        UTotal += U
    D_average = DTotal/len(trainFolds)
    T_average = TTotal/len(trainFolds)
    U_average = UTotal/len(trainFolds)
    return D_average, T_average, U_average


"""
for each chunk of the cross-validation, find the most frequent sentiment
"""
def question5(testFolds, tweetData):
    MFSList = []
    for chunk in testFolds:
        mfs = mostFrequentSent(chunk, tweetData)
        MFSList.append(mfs)

    # display results
    print 'Chunk |   MFS\n---------------'
    for i in range(len(MFSList)):
        print '  %-3d | %s (%d)' % (i, MFSList[i][0], MFSList[i][1])

    return MFSList

"""
use the MFS from the training data to label the test data"
"""
def question6(trainFolds, testFolds, tweetData):
    trainMFSList = []
    for chunk in trainFolds:
        mfs = mostFrequentSent(chunk, tweetData)
        trainMFSList.append(mfs)

    percentCorrectList = []
    for i in range(len(testFolds)):
        mfs = trainMFSList[i][0]
        correctCount = 0
        for tweetID in testFolds[i]:
            answers = tweetData['tweets'][tweetID]['answers']

            if mfs in answers:
                correctCount += 1
        percentCorrectList.append(float(correctCount)/len(testFolds[i]) * 100)

    totalPercent = 0
    for i in range(len(testFolds)):
        totalPercent += percentCorrectList[i]

    print '%.3f' % (totalPercent/len(testFolds))

def question7(trainFolds, testFolds, tweetData, stopWords):

    totalAccuracy = 0.0
    for i in range(len(testFolds)):
        trainIDs = trainFolds[i]
        testIDs = testFolds[i]
        MFS = mostFrequentSent(trainIDs, tweetData)

        sfDict = createSenseFeatureDictionary(trainIDs, tweetData)
        scoreDict = createScoreDictionary(sfDict)
        decisionList = createDecisionList(scoreDict, None)

        if stopWords > 0:
            removeItemsList = findMostCommonWords(trainIDs,tweetData,stopWords)
            decisionList = removeItemsFromDList(decisionList, removeItemsList)
        
        guessDict = labelData(testIDs, tweetData, MFS, decisionList, None)
        totalAccuracy += examineResults(testIDs, tweetData, guessDict)

    print "%.3f" % (totalAccuracy/len(testFolds))

"""
implements naive bayes classifier using 5-fold cross validation to train
and test
"""
def question9(trainFolds, testFolds, tweetData, n):

    D, T, U = calculateDiscount(trainFolds, testFolds, tweetData) #NEW

    totalAccuracy = 0
    for i in range(len(testFolds)):
        trainIDs = trainFolds[i]
        testIDs = testFolds[i]
        totalAccuracy += naiveBayesClassifier(trainIDs,testIDs,tweetData,D,T,U,n)

    print "%.3f" % (totalAccuracy/len(testFolds))


def main():
    filename = '/data/cs65/semeval-2015/B/train/twitter-train-full-B.tsv'
    tweetData = parse_tweets(filename, 'B')

    # use 5-fold cross-validation
    trainFolds, testFolds = crossValidation(tweetData, 5, False)

    standardTweetData = conflateData(tweetData)
    lowerTweetData = lowerData(standardTweetData)
    negatedTweetData = negateData(standardTweetData, ['not'])
    lowerNegatedTweetData = negateData(lowerTweetData, ['not'])
    tokenizedTweetData = tokenizeData(standardTweetData) 

    #extras: 
    negateWords = ['not', 'no', 'never']
    negatedTweetData2 = negateData(standardTweetData, negateWords) 
    lowerNegatedTweetData2 = negateData(lowerTweetData, negateWords)

    print "\nQuestion 5: Most Frequent Sentiments in %d Chunks:\n" % (len(testFolds))
    testMFSList = question5(testFolds, standardTweetData)

    print "\nQuestion 6: Accuracy of MFS on Test Data (with cross-validation):"
    question6(trainFolds, testFolds, standardTweetData)
    
    print "\nQuestion 7: Accuracy of Decision List Classifier:\n"
    print "Standard Conditions:"
    question7(trainFolds, testFolds, standardTweetData, 0)
    # test stopwords

    print "\nWith Stopwords Removed:"
    for i in range(25, 151, 25):
        print i, "-",
        question7(trainFolds, testFolds, standardTweetData, i)

    print "\nWith Case-Folding:"
    question7(trainFolds, testFolds, lowerTweetData, 0)

    print "\nQuestion 8: Accuracy of Decision List with Negations after 'not':"
    question7(trainFolds, testFolds, negatedTweetData, 0)

    print "\nApply negation after 'not','no','never':"
    question7(trainFolds, testFolds, negatedTweetData2, 0)
    
    print "\nQuestion 9: Accuracy of Naive Bayes Classifier:"
    question9(trainFolds, testFolds, standardTweetData, 0)

    
    print "\nQuestion 10: Naive Bayes Classifier:"
    
    print "\n1. With StopWords Removed:"
    for i in range(25, 151, 25):
        print i, '-',
        question9(trainFolds, testFolds, standardTweetData, i)

    print "\n2. With Case-Folding:"
    question9(trainFolds, testFolds, lowerTweetData, 0)
    

    print "\n3. With Negations after 'not':"
    question9(trainFolds, testFolds, negatedTweetData, 0)
    print "\n4. With Case-Folding and Negations after 'not':"
    question9(trainFolds, testFolds, lowerNegatedTweetData, 0)
    
    print "\n5. With StopWords Removed, Case-Folding, and Negations after 'not':"
    for i in range(25, 151, 25):
        print i, '-', 
        question9(trainFolds, testFolds, lowerNegatedTweetData, i)
    
    print '\nUsing 2nd Negation Strategy...'    
    print "\n1. With Negations after 'not', 'never', 'no':"
    question9(trainFolds, testFolds, negatedTweetData2, 0)
    print "\n2. With Case-Folding and Negations after 'not':"
    question9(trainFolds, testFolds, lowerNegatedTweetData2, 0)
    
    print "\n3. With StopWords Removed, Case-Folding, and Negations after 'not', \
            'never', 'no':"
    for i in range(25, 151, 25):
        print i, '-', 
        question9(trainFolds, testFolds, lowerNegatedTweetData2, i)
    print

    print "\nQuestion 11: Accuracy of Decision List and Naive Bayes with Tokenization\n"
    print 'Decision List:'
    question7(trainFolds, testFolds, tokenizedTweetData, 0)
    print 'Naive Bayes:'
    question9(trainFolds, testFolds, tokenizedTweetData, 0)

    print "\nQuestion 11: Extras\n"
    tokenedLowerTweetData = lowerData(tokenizedTweetData)
    tokenedLowerNegatedTweetData = negateData(tokenedLowerTweetData, negateWords)
    print 'Decision List:'
    question7(trainFolds, testFolds, tokenedLowerNegatedTweetData, 0)
    print 'Naive Bayes:'
    question9(trainFolds, testFolds, tokenedLowerNegatedTweetData, 30)
    

main()
