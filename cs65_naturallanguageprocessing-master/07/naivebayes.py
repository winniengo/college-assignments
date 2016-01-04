import math
from operator import itemgetter

def createSenseFeatureDictionary(trainIDs, tweetData):
    #print 'createSenseFeatureDictionary'
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

def probFeatureGivenSenseDict(sfDict, D):

    sentiments = sfDict.keys() # all sentiments in training data

    dictionary = {}
    denomsDict = {}
    for sentiment in sentiments:

        dictionary[sentiment] = {}
        features = sfDict[sentiment].keys()
        denomCount = 0
        for feature in features:
            #calculate denominator
            denomCount += sfDict[sentiment][feature]
        denomsDict[sentiment] = denomCount

        for feature in features:
            #calculate numerator
            numerCount = sfDict[sentiment][feature]
            dictionary[sentiment][feature] = float(numerCount-D)

    return dictionary, denomsDict


def probSenseDict(trainIDs, tweetData):

    countDictionary = {}
    for tweetID in trainIDs:
        sentiments = tweetData["tweets"][tweetID]["answers"]
        for sentiment in sentiments:
            if countDictionary.get(sentiment) == None:
                countDictionary[sentiment] = 1
            else:
                countDictionary[sentiment] += 1
    
    probDictionary = {}
    
    sentiments = countDictionary.keys()
    for sentiment in sentiments:
        probDictionary[sentiment] = \
                float(countDictionary[sentiment])/len(trainIDs)

    return probDictionary


def naiveBayesClassifier(trainIDs, testIDs, tweetData, D, T, U, num):

    sfDictionary = createSenseFeatureDictionary(trainIDs, tweetData)
    pFeatureSenseDictionary, denoms = probFeatureGivenSenseDict(sfDictionary, D)
    pSenseDictionary = probSenseDict(trainIDs, tweetData)
    stopWords = findMostCommonWords(trainIDs, tweetData, num)

    sentiments = pSenseDictionary.keys()
    
    correct = 0
    for tweetID in testIDs:

        max_bayes = float("-inf")
        max_sentiment = None
        for sentiment in sentiments:
            features = tweetData["tweets"][tweetID]["words"]
            correctAnswers = tweetData["tweets"][tweetID]["answers"]
            totalPfj_s = 0
            for feature in features:
                if feature in stopWords: # ignore any 'stopwords'
                    totalPfj_s += 0.0
                elif pFeatureSenseDictionary[sentiment].get(feature) == None:
                    totalPfj_s += math.log((D*T/U)/denoms[sentiment])
                else:
                    totalPfj_s += math.log(pFeatureSenseDictionary[sentiment][feature])
                
            bayes = math.log(pSenseDictionary[sentiment]) + totalPfj_s

            if bayes > max_bayes:
                max_bayes = bayes
                max_sentiment = sentiment

        if max_sentiment in correctAnswers:
            correct += 1

    accuracy = float(correct)/len(testIDs) * 100
    return accuracy

"""
Retrieve most common words in dataset
param: data - dataset, num - number of most common words to return
return: lsit of most common words 
"""

def findMostCommonWords(tweetData, num):
    
    count = defaultdict(int)
    for tweetID in trainIDs:
        words = tweetData["tweets"][tweetID]["words"]
        for w in words: #accumulate count of words
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

