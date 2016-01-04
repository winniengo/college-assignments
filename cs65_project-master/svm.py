"""
Implement scikit-learn SVM for machine learning classifiction

Winnie Ngo, Michael Superdock
"""
import nltk
from collections import defaultdict

import sys
sys.path = [x for x in sys.path if '2.7' not in x]
import sklearn

from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from nltk.classify.scikitlearn import SklearnClassifier

sys.path.append('/data/cs65/semeval-2015/scripts/')
from scorer import scorer

def svmScorer(trainFolds, testFolds, tweetData, testData):
    """
    Uses n-fold cross validation to evaluate the predictions of the
    SVM classifier on our set of data. Accumulates stats based on our
    predictions and calculates a score based on these stats
    """

    stats = defaultdict(lambda: defaultdict(int))
    for i in range(len(testFolds)):
        trainIDs = trainFolds[i]
        testIDs = testFolds[i]
        svmClassifier(trainIDs, testIDs, tweetData, testData, stats, True)

    scorer(stats)

def svmClassifier(trainIDs, testIDs, tweetData, testData, stats, crossVal):
    """
    Train classifier model on training data and predict on test data. Increment
    stats dictionary if using n-fold cross validation, otherwise write to file
    tweet id and label from model. 
    """

    # train classifier on training data
    classifier = svmTrain(trainIDs, tweetData)
    # label test data
    predictions, answers = svmPredict(testIDs, testData, classifier, crossVal)

    if crossVal: # validate classifier on known test data labels
        for i in range(len(predictions)):
            stats[predictions[i]][answers[i]] += 1
    else: # output classifier predictions on unknown test data labels
        filename = "test_labels.txt"
        writePredictions(testIDs, predictions, filename)


def svmTrain(tids, tweetData):
    """
    Creates and trains Logistic Regression classification model using training
    data. Returns model
    """

    trainData = []
    for tweetID in tids:
        answer = tweetData["tweets"][tweetID]["answers"][0]
        features = tweetData["tweets"][tweetID]["postFeatures"]
        features += tweetData["tweets"][tweetID]["weightFeatures"]
        fdist = nltk.FreqDist(features)
        tup = tuple((fdist, answer))
        trainData.append(tup)

    classifier = LogisticRegression(C=1.0, penalty='l1')
    classif = SklearnClassifier(classifier)
    classif.train(trainData)
    
    return classif


def svmPredict(tids, testData, classifier, crossVal):
    """
    Use given classifier to predict labels on test data and return labels. 
    If cross validation is implemented, also return list of know labels.
    """
    
    testDataFeatures = []
    testDataAnswers = []
    
    for tweetID in tids:
        features = testData["tweets"][tweetID]["postFeatures"]
        features += testData["tweets"][tweetID]["weightFeatures"]
        fdist = nltk.FreqDist(features)
        testDataFeatures.append(fdist)

        if crossVal:
            answer = testData["tweets"][tweetID]["answers"][0]
            testDataAnswers.append(answer)
    
    predictionList = classifier.classify_many(testDataFeatures)

    return predictionList, testDataAnswers


def writePredictions(tids, predictions, filename):
    """
    Write to file tweet ids and corresponding answers to classifier
    """
    output = open(filename, 'w')

    for i, tid in enumerate(tids):
        line = '%s\t%s\n'% (tid, predictions[i])
        print(line)
        output.write(line)

    output.close()
