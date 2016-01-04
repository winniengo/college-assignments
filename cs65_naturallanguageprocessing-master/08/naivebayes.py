import math
from operator import itemgetter
from collections import defaultdict


"""
counts how many time each feature occurs given a sentence sentiment

dictionary[s][fj] = count(fj, s)

returns dictionary
"""
def createSenseFeatureDictionary(trainIDs, tweetData):
    dictionary = defaultdict(lambda: defaultdict(int))
    for tweetID in trainIDs: #tweetIDs for training
        features = tweetData["tweets"][tweetID]["postFeatures"]
        answers = tweetData["tweets"][tweetID]["answers"]
        wFeatures = tweetData["tweets"][tweetID]["weightFeatures"]
        wIndices = [x[0] for x in wFeatures]
        wMultiplyers = [x[1] for x in wFeatures]
        #print wIndices
        #print wMultiplyers

        for answer in answers:
            for i in range(len(features)):
                mult = 1
                if i in wIndices:
                    pos = wIndices.index(i)
                    mult = wMultiplyers[pos]
                feature = features[i]
                dictionary[answer][feature] += 1.0 * mult

    return dictionary


"""
returns a dictionary of numerators and denomenators used to estimate P(fj|s)

denomDict[s] = sum_i( count(fi, s) )
"""
def probFeatureGivenSenseDict(sfDict):

    sentiments = sfDict.keys() # all sentiments in training data
    denomDict = {}

    for sentiment in sentiments:
        denomDict[sentiment] = sum(sfDict[sentiment].values())

    return denomDict


"""
returns a dictionary with P(s), the probability of a training instance being
labeled with sense s

probDictionary[s] = P(s)
"""
def probSenseDict(trainIDs, tweetData):

    countDictionary = defaultdict(float)
    for tweetID in trainIDs:
        sentiments = tweetData["tweets"][tweetID]["answers"]
        for sentiment in sentiments:
            countDictionary[sentiment] += 1.0
    
    probDictionary = {}
    sentiments = countDictionary.keys()
    for sentiment in sentiments:
        probDictionary[sentiment] = countDictionary[sentiment]/len(trainIDs)

    return probDictionary

"""
classify tweets using naiveBayes classifier with laplace smoothing
"""
def naiveBayesClassifier(trainIDs, testIDs, tweetData, testData, T):
    numerDict = createSenseFeatureDictionary(trainIDs, tweetData)
    denomDict = probFeatureGivenSenseDict(numerDict)
    pSenseDictionary = probSenseDict(trainIDs, tweetData)

    a = 1
    sentiments = pSenseDictionary.keys()
    correct = 0
    predictionDict = {}
    for tweetID in testIDs:

        max_bayes = None
        max_sentiment = None
        for sentiment in sentiments:
            if testData: # use first file as training, second file as testing
                features = testData["tweets"][tweetID]["postFeatures"]
                correctAnswers = testData["tweets"][tweetID]["answers"]
            else: # perform cross-validation
                features = tweetData["tweets"][tweetID]["postFeatures"]
                correctAnswers = tweetData["tweets"][tweetID]["answers"]
            
            totalPfj_s = 0
            for feature in features:
                if numerDict[sentiment].get(feature) == None:
                    numerator = a
                else:
                    numerator = numerDict[sentiment][feature] + a
                denominator = denomDict[sentiment] + T*a
                totalPfj_s += math.log(numerator/denominator)
                
            bayes = math.log(pSenseDictionary[sentiment]) + totalPfj_s

            if max_bayes == None or bayes > max_bayes:
                max_bayes = bayes
                max_sentiment = sentiment        

        predictionDict[tweetID] = max_sentiment

    return predictionDict


def calculateAccuracy(tweetData, predictionDict, stats):

    #correct = 0
    #tweetIDs = predictionDict.keys()
    #for tweetID in tweetIDs:
    #    if predictionDict[tweetID] in tweetData["tweets"][tweetID]["answers"]:
    #        correct += 1
    #accuracy = float(correct)/len(tweetIDs) * 100
    tweetIDs = predictionDict.keys()
    for tweetID in tweetIDs:
        prediction = predictionDict[tweetID]
        answer = tweetData["tweets"][tweetID]["answers"][0]
        stats[prediction][answer] += 1
    
    #return accuracy


