from parseTweet import parse_tweets
from writeJazzy import clean_tweets
from crossVal import crossValidation
from operator import itemgetter
from classifier import handleCommandLineArgs
import string, re
from sklearn import svm

#import sys
#sys.path = [x for x in sys.path if '3.4' not in x]   
#import sklearn

import sys
sys.path = [x for x in sys.path if '2.7' not in x]
import sklearn

# open-source tokenization
sys.path.append('/data/cs65/semeval-2015/arktweet/')
from arktweet import tokenize, dict_tagger, dict_tokenizer
sys.path.append('/data/cs65/semeval-2015/scripts/')
from scorer import scorer



"""
feature weighting - all features receive weight 1 if present, 0 otherwise
    upper - if original token is all uppercased and more than 3 letters (+1)
    repitition - if original token has >3 adjacent repititions of 1 letter (+3)
    adjective - if token is an adjective accoding to its POS tag (+3)
"""
def preFeatures(tweetData, upper, repitition, adjective):

    newData = {}
    newData['tweets'] = {}
    tweetIDs = tweetData['tweets'].keys()
    for tweetID in tweetIDs:
        weightFeatures = []
        answers = tweetData['tweets'][tweetID]['answers']
        words = tweetData['tweets'][tweetID]['words']
        tags = tweetData['tweets'][tweetID].get('tags')

        if upper:
            weightFeatures += isUpper(words)
        if repitition:
            weightFeatures += repeatedChars(words)
        if adjective:
            weightFeatures += isAdjective(words, tags)

        weightFeatures = set(weightFeatures)

        # construct dictionary of tweet data after preprocessing
        newData['tweets'][tweetID] = {}
        newData['tweets'][tweetID]['weightFeatures'] = weightFeatures
        newData['tweets'][tweetID]['answers'] = answers
        newData['tweets'][tweetID]['words'] = words
        newData['tweets'][tweetID]['tags'] = tags

    return newData

""" feature weighting helper function """
def isUpper(words):
    wFeatures = []
    for i in range(len(words)):
        if words[i].isupper() and len(words[i]) > 3:
            wFeatures.append((i,2))
    return wFeatures

""" feature weighting helper function """
def repeatedChars(words):
    wFeatures = []
    for i in range(len(words)):
        rgx = re.compile(r"(\w)\1{2,}") #matches same char, of same case
        if rgx.search(words[i]):
            wFeatures.append((i,4))
    return wFeatures

""" feature weighting helper function """
def isAdjective(words, tags):
    wFeatures = []
    for i in range(len(words)):
        if tags[i] == 'A':
            wFeatures.append((i,4))
    return wFeatures

###############################################################################
"""
implements word n-grams and discontinuous n-grams
"""
def postFeatures(tweetData, biGrams, triGrams, fourGrams, fiveGrams, \
        dTriGrams, dFourGrams):

    newData = {}
    newData['tweets'] = {}
    tweetIDs = tweetData['tweets'].keys()
    for tweetID in tweetIDs:
        features = []
        wfeatures = tweetData['tweets'][tweetID].get('weightFeatures')
        answers = tweetData['tweets'][tweetID]['answers']
        words = tweetData['tweets'][tweetID]['words']
        tags = tweetData['tweets'][tweetID].get('tags')

        features += words
        if biGrams:
            features += ngrams(words, 2)
        if triGrams:
            features += ngrams(words, 3)
        if fourGrams:
            features += ngrams(words, 4)
        if fiveGrams:
            features += ngrams(words, 5)
        if dTriGrams: #discontiguous triGrams
            features += discontiguousNgrams(ngrams(words,3),3)
        if dFourGrams: #discontiguous fourGrams
            features += discontiguousNgrams(ngrams(words,4),4)

        # construct dictionary of tweet data after preprocessing
        newData['tweets'][tweetID] = {}
        newData['tweets'][tweetID]['postFeatures'] = features
        newData['tweets'][tweetID]['weightFeatures'] = wfeatures
        newData['tweets'][tweetID]['answers'] = answers
        newData['tweets'][tweetID]['words'] = words
        newData['tweets'][tweetID]['tags'] = tags

    return newData

""" n-gram helper function - takes list of words and segments in n grams"""
def ngrams(words, n):
    ngramsList = []
    for i in range(len(words)-n+1):
        ngram = ""
        for j in range(i,(i+n)):
            if j == (i+n-1):
                ngram += words[j]
            else:
                ngram += (words[j] + " ")
        ngramsList.append(ngram)
    return ngramsList

""" n-gram helper function - takes list of ngrams and returns discontinuous list"""
def discontiguousNgrams(ngramList, n):
    
    newGrams = []
    for ngram in ngramList:
        for i in range(1, (n-1)):
            temp = ngram.split()
            temp[i] = '*'
            temp = ' '.join(temp)
            newGrams.append(temp)
    return newGrams     

###############################################################################
"""
normalization - modifies 'words' and 'answers'
    conflate - objective-OR-neutral beceoms neutral
    lower - case-folds words
    negate - negates words that occur after list and before punctuation
    hashtag - remove '#' in hashtags
"""
def preProcessing(tweetData, conflate, lower, negate, hashtag):

    newData = {}
    newData['tweets'] = {}
    tweetIDs = tweetData['tweets'].keys()
    for tweetID in tweetIDs:
        wfeatures = tweetData['tweets'][tweetID].get('weightFeatures')
        answers = tweetData['tweets'][tweetID]['answers']
        words = tweetData['tweets'][tweetID]['words']
        tags = tweetData['tweets'][tweetID].get('tags') # None otherwise

        # construct dictionary of tweet data after preprocessing
        newData['tweets'][tweetID] = {}
        if conflate:
            answers = conflateAnswers(answers)
        if lower:
            words = lowerWords(words)
        if negate:
            words = negateWords(words, negate)
        if hashtag:
            words = hashtagWords(words)

        newData['tweets'][tweetID]['words'] = words
        newData['tweets'][tweetID]['answers'] = answers
        newData['tweets'][tweetID]['tags'] = tags
        newData['tweets'][tweetID]['weightFeatures'] = wfeatures

    return newData

""" conflate words, preprocessing helper function """
def conflateAnswers(answers):
    # conflate neutral sentiments into a single sentimentas in Q2
    if 'objective' in answers or 'neutral' in answers:
        answers = ['neutral']
    return answers

""" lower words, preprocessing helper function """ 
def lowerWords(wordList):
    newWords = []
    for i in range(len(wordList)):
        newWords.append(wordList[i].lower())
    return newWords

""" negate words, preprocessing helper function """
def negateWords(words, negateWordList):
    newWords = []
    negation = False
    for word in words:

        #append words
        if negation:
            newWords.append('NOT_' + word)
        else:
            newWords.append(word)
            
        #set negation to True or False
        if word.lower() in negateWordList or word.lower()[-3:] == "n't":
            negation = True
        elif word[-1] in string.punctuation:
            negation = False

    return newWords

""" remove # from hashtags, preprocessing helper function """
def hashtagWords(wordList):
    newWords = [] 
    for word in wordList:
        if '#' in word:
            word = word.replace('#', '')
        newWords.append(word)

    return newWords

###############################################################################
""" calculate discounts used for smoothing """
def calculateTValue(trainFolds, testFolds, tweetData):

    TTotal = []
    for i in range(len(trainFolds)):
        trainFold = trainFolds[i]
        trainFeatures = set()
        for trainID in trainFold:
            trainFeatures.update(tweetData['tweets'][trainID]['postFeatures'])
        T = float(len(trainFeatures))
        TTotal.append(T)
    return TTotal

""" finds the most common words in all tweets """
def findMostCommonWords(tweetData, num):
    
    count = defaultdict(int)
    tweetIDs = tweetData["tweets"].keys()
    for tweetID in tweetIDs:
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

""" removes the most common words in all tweets """
def removeStopWords(tweetData, num):

    commonWords = findMostCommonWords(tweetData, num)
    tweetIDs = tweetData["tweets"].keys()
    for tweetID in tweetIDs:
        words = tweetData["tweets"][tweetID]["words"]
        newWords = []
        newTags = []
        for word in words:
            if not word in commonWords:
                newWords.append(word)
        tweetData["tweets"][tweetID]["words"] = newWords

"""
removes specific words in the tweet
    url - remove word if it is a url
    tweetHandle - remove word if it a twitter Handle (starts with @)
"""
def removeOtherWords(tweetData, url, tweetHandle):

    tweetIDs = tweetData["tweets"].keys()
    for tweetID in tweetIDs:
        words = tweetData["tweets"][tweetID]["words"]
        tags = tweetData["tweets"][tweetID].get("tags")
        removeIndices = []
        for i in range(len(words)):
            word = words[i]
            tag = tags[i]
            if url:
                if 'http://' in word: # remove URLs
                    removeIndices.append(i)
            if tweetHandle:
                if tag == '@':
                    if not i in removeIndices:
                        removeIndices.append(i)
        removeIndices = removeIndices[::-1]
        for indx in removeIndices:
            del words[indx]
            del tags[indx]
        
        tweetData["tweets"][tweetID]["words"] = words
        tweetData["tweets"][tweetID]["tags"] = tags

"""
classify words using naive bayes and cross-validation
"""
def naiveBayes(trainFolds, testFolds, tweetData, testData):

    T = calculateTValue(trainFolds, testFolds, tweetData) #NEW

    totalAccuracy = 0

    stats = defaultdict(lambda: defaultdict(int))
    for i in range(len(testFolds)):
        trainIDs = trainFolds[i]
        testIDs = testFolds[i]
        predictionDict = naiveBayesClassifier(trainIDs, testIDs, tweetData, testData, T[i])
        #totalAccuracy += calculateAccuracy(tweetData, predictionDict)
        calculateAccuracy(tweetData, predictionDict, stats)
    
    scorer(stats)

    #print "%.2f" % (totalAccuracy/len(testFolds))

###############################################################################
def main():
    #use 5-fold cross-validation
    tweetData, testData, trainFolds, testFolds = handleCommandLineArgs()

    #filename = '/data/cs65/semeval-2015/B/train/twitter-train-full-B.tsv'
    #tweetData = parse_tweets(filename, 'B')

    #tweetData = parse_tweets('jazzyTokenizeHandleConflateHashtag.twv', 'B')
    #tweetData = parse_tweets('jazzyTokenizeUrlConflateHashtag.twv', 'B')

    #mandatory tweetData modifications (as specified by us)
    tokenize = False
    tokenizeAndTag = True
    stopWords = False
    removeWords = True
    if removeWords:
        url = True
        tweetHandle = True

    if tokenize:
        dict_tokenizer(tweetData)
    if tokenizeAndTag:
        dict_tagger(tweetData)
    if stopWords:
        removeStopWords(tweetData, 50)
    if removeWords: 
        removeOtherWords(tweetData, url, tweetHandle)

    if testData: # repeat on testData
        if tokenize:
            dict_tokenizer(testData)
        if tokenizeAndTag:
            dict_tagger(testData)
        if stopWords:
            removeStopWords(testData, 50)
        if removeWords: 
            removeOtherWords(testData, url, tweetHandle)

        
    # features identified before processing (weighted features)
    upper = True
    repitition = True
    adjective = True

    preFeaturesTweetData = preFeatures(tweetData, upper, repitition, adjective)
    if testData:
        preFeaturesTestData = preFeatures(testData, upper, repitition, adjective)

    # pre processing tweetData modifications
    conflate = True
    lower = True
    negateWords = ['not', 'no', 'never']
    hashtag = True

    preProcessedData = preProcessing(preFeaturesTweetData, conflate, lower, \
            negateWords, hashtag)
    if testData:
        preProcessedTestData = preProcessing(preFeaturesTestData, conflate, lower,\
                negateWords, hashtag)

    #features identified after processing (ngrams)
    biGrams = False
    triGrams = False
    fourGrams = False
    fiveGrams = False
    dTriGrams = False
    dFourGrams = False

    postFeaturesData = postFeatures(preProcessedData, biGrams, triGrams, \
            fourGrams, fiveGrams, dTriGrams, dFourGrams)
    if testData:
        postFeaturesTestData = postFeatures(preProcessedTestData, biGrams, triGrams, \
            fourGrams, fiveGrams, dTriGrams, dFourGrams)
    else:
        postFeaturesTestData = None

    print "*****preProcessing complete*****"
    #featuresList = extractFeatures(postFeaturesData)
    X, Y = constructXY(postFeaturesData)
    #print X[:5]
    #print Y[:5]
    clf = svm.SVC()
    clf.fit(X,Y)
    SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3, gamma=0, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False)


    """
    for i in range(len(X)):
        Xfile.write(X[i])
        Yfile.write(Y[i])

    Xfile.close()
    Yfile.close()
    """
    print "HERE"
    #
    #print "\nNaive Bayes Classifier:"
    #naiveBayes(trainFolds, testFolds, postFeaturesData, postFeaturesTestData)

main()
