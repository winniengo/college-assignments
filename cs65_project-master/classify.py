from commandline import handleCommandLineArgs

from writeJazzy import clean_tweets
from operator import itemgetter
import string, re
from sklearn import svm
from svm import *

import string

import sys
sys.path = [x for x in sys.path if '2.7' not in x]
import sklearn

from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

# open-source tokenization
sys.path.append('/data/cs65/semeval-2015/arktweet/')
from arktweet import tokenize, dict_tagger, dict_tokenizer
sys.path.append('/data/cs65/semeval-2015/scripts/')
from scorer import scorer

############ Functions for Features Before Preprocessing #############

def preFeatures(tweetData, upper, repitition):
    """
    identifies features prior to preprocessing. These are saved in the
    dictionary under the tag 'weightFeatures', as they were weighted
    features when this was implemented for Niave Bayes. This returns the
    tweet dictionary with the features.
    """

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

        # construct dictionary of tweet data after preprocessing
        newData['tweets'][tweetID] = {}
        newData['tweets'][tweetID]['weightFeatures'] = weightFeatures
        newData['tweets'][tweetID]['answers'] = answers
        newData['tweets'][tweetID]['words'] = words
        newData['tweets'][tweetID]['tags'] = tags

    return newData

def isUpper(words):
    """
    identifies words that are completely uppercase and are greater than 3
    characters in length. It returns the feature 'UPPER', giving us a count
    of all uppercase words
    """

    wFeatures = []
    for i in range(len(words)):
        if words[i].isupper() and len(words[i]) > 3:
            wFeatures += "UPPER"
    return wFeatures


def repeatedChars(words):
    """
    identifies words that have 2 or more repeated characters (such as the word
    greeeeat). It returns the feature 'REPEATED', giving us a count of all
    words with repeated characters
    """

    wFeatures = []
    for i in range(len(words)):
        rgx = re.compile(r"(\w)\1{2,}") #matches same char, of same case
        if rgx.search(words[i]):
            m  = rgx.search(words[i]).group()[1:]
            feat = re.sub(m, '', words[i])
            while rgx.search(feat):
                m = rgx.search(feat).group()[1:]
                feat = re.sub(m, '', feat)
            wFeatures += (feat.lower().strip(string.punctuation)+"_REPEATED")
    return wFeatures


################# Functions for Preprocessing Modifications ###################

def preProcessing(tweetData, conflate, lower, negate, hashtag):
    """
    preproccess tweetData by modifing both 'words' and 'answers'
    
    conflate - objective-OR-neutral becomes neutral
    lower - case-folding words
    negate - negates words occuring after negative word and before punctuation
    hashtag - removes '#' in hastags
    """

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

def conflateAnswers(answers):
    """
    conflates answer set, such that objective-OR-neutral becomes neutral.
    returns the conflated answers
    """

    if 'objective' in answers or 'neutral' in answers:
        answers = ['neutral']
    return answers


def lowerWords(wordList):
    """
    lowers words in our word list. returns word list in all lowercase
    """

    newWords = []
    for i in range(len(wordList)):
        newWords.append(wordList[i].lower())
    return newWords


def negateWords(words, negateWordList):
    """
    negates words found between a negative word in our negateWordList (or words
    ending in n't) and a punctuation mark
    """
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


def hashtagWords(wordList):
    """
    removes hastags from our sentence. returns words without the hashtags
    """

    newWords = [] 
    for word in wordList:
        if '#' in word:
            word = word.replace('#', '')
        newWords.append(word)

    return newWords

def removeStopWords(tweetData, num):
    """
    removes the most common words in all tweets. It removes up to num words.
    It returns the dictionary with the common words
    """

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


def findMostCommonWords(tweetData, num):
    """
    finds the most common words in all tweets and returns them. this is used
    as a helper function for removeStopWords
    """
    
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


def removeOtherWords(tweetData, url, tweetHandle):
    """
    removes other words. Specifically, if url is true, it removes urls. If
    tweetHandle is true, it removes twitter handles (tag '@')
    """

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


############### Functions for Features After Preprocessing ####################

def postFeatures(tweetData, biGrams, triGrams, fourGrams, fiveGrams, \
        dTriGrams, dFourGrams, adjective, emoticon, punctuation):
    """
    identifies features after preprocessing. These are saved in the dictionary
    under the tag 'features'. This returns dictionary with the features

    n-grams - all different types of tag n-grams (word n-grams not useful)
    adjective - determines a count of adjectives
    emoticon - produces multiple emoticons for each emoticon in tweet
    puntuation - determines a count of punctuations

    this also includes all words as features
    """

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
        features += tags
        if biGrams:
            features += ngrams(tags, 2) #tag n-grams
        if triGrams:
            features += ngrams(tags, 3)
        if fourGrams:
            features += ngrams(tags, 4)
        if fiveGrams:
            features += ngrams(tags, 5)
        if dTriGrams: #discontiguous triGrams
            features += discontiguousNgrams(ngrams(tags,3),3)
        if dFourGrams: #discontiguous fourGrams
            features += discontiguousNgrams(ngrams(tags,4),4)
        if adjective:
            wfeatures += isAdjective(tags)
        if emoticon:
            wfeatures += isEmoticon(words, tags)
        if punctuation:
            wfeatures += isPunctuation(tags)

        # construct dictionary of tweet data after preprocessing
        newData['tweets'][tweetID] = {}
        newData['tweets'][tweetID]['postFeatures'] = features
        newData['tweets'][tweetID]['weightFeatures'] = wfeatures
        newData['tweets'][tweetID]['answers'] = answers
        newData['tweets'][tweetID]['words'] = words
        newData['tweets'][tweetID]['tags'] = tags

    return newData

def isAdjective(tags):
    """
    counts the number of adjectives seen and returns them as features
    """

    wFeatures = []
    for i in range(len(tags)):
        if tags[i] == 'A':
            wFeatures += "ADJECTIVE"
    return wFeatures

def isEmoticon(words, tags):
    """
    adds more emoticons for each one seen and returns them as features
    """

    wFeatures = []
    for i in range(len(words)):
        if tags[i] == 'E':
            if words[i] in [':)','(:',':-)',':))',';)',';-)','=)',\
                    '=))',';]','<3','^_^', '^.^',':)))', '(;', '<33',
                    '<333', '<3333']:
                feat = 'POSITIVE'
                wFeatures += feat
            elif words[i] in [':(',':/',':-(',':\\', '>:(',':\'(',':((']:
                feat = 'NEGATIVE'
                wFeatures += feat
    return wFeatures

def isPunctuation(tags):
    """
    counts the number of punctuation marks seen and returns them as features
    """

    wFeatures = []
    for i in range(len(tags)):
        if tags[i] == ',':
            wFeatures += "PUNCTUATION"
    return wFeatures

def ngrams(words, n):
    """
    n-gram helper functions - takes a list of words and segments into n grams
    """

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

def discontiguousNgrams(ngramList, n):
    """
    takes a list of words and segments into discontiguous ngrams
    """
    
    newGrams = []
    for ngram in ngramList:
        for i in range(1, (n-1)):
            temp = ngram.split()
            temp[i] = '*'
            temp = ' '.join(temp)
            newGrams.append(temp)
    return newGrams     


def main():

    crossVal, tweetData, testData, trainFolds, testFolds = \
            handleCommandLineArgs()

    #tweetData = parse_tweets('jazzyTokenizeHandleConflateHashtag.twv', 'B')
    #tweetData = parse_tweets('jazzyTokenizeUrlConflateHashtag.twv', 'B')

    ################  1. Feature and Preprocessing Flags ##################

    #1.1 features to check prior to any preprocessing

    upper = True            #features for words in all CAPS
    repitition = True       #features for words with repeating characters
    
    #1.2 preprocessing of words within the tweets

    tokenize = False        #splits the tweets into tokens
    tokenizeAndTag = True   #splits the tweets into tokens and tags
    stopWords = False       #removes stop words
    removeWords = True      #remove certain words from text
    if removeWords:         
        url = True          #removes urls
        tweetHandle = True  #removes tweet handles
    conflate = True         #used to conflate answers
    lower = True            #sets all words to lower case
    negateWords = ['not', 'no', 'never'] #negate words in negative contexts
    hashtag = True          #removes hashtags

    #1.3 features identified after preprocessing (ngrams are of tags)

    biGrams = True
    triGrams = False
    fourGrams = False
    fiveGrams = False
    dTriGrams = False
    dFourGrams = False
    adjective = False       #counts the number of adjectives
    emoticons = True        #weights emoticons
    punctuation = False      #counts the number of punctuation

    ############## 2. Feature and Preproccessing Implementation #############

    #2.1 update dictionary with features before preprocessing
    tweetData = preFeatures(tweetData, upper, repitition)

    #2.2 preprocessing
    if tokenize:
        dict_tokenizer(tweetData)
    if tokenizeAndTag:
        dict_tagger(tweetData)
    if stopWords:
        removeStopWords(tweetData, 50)
    if removeWords: 
        removeOtherWords(tweetData, url, tweetHandle)
    preProcessedData = preProcessing(tweetData, conflate, lower, \
            negateWords, hashtag)

    #2.3 update dictionary with features after preprocessing
    postFeaturesData = postFeatures(preProcessedData, biGrams, triGrams, \
            fourGrams, fiveGrams, dTriGrams, dFourGrams, adjective, emoticons, \
            punctuation)


    #feature extraction and preprocessing if we are testing on a sepearate set
    if testData:

        #2.1 update dictionary with features before preprocessing
        testData = preFeatures(testData, upper, repitition)
        
        #2.2 preprocessing
        if tokenize:
            dict_tokenizer(testData)
        if tokenizeAndTag:
            dict_tagger(testData)
        if stopWords:
            removeStopWords(testData, 50)
        if removeWords: 
            removeOtherWords(testData, url, tweetHandle)

        #2.3 update dictionary with features after preprocessing
        preProcessedTestData = preProcessing(testData, conflate, lower,\
                negateWords, hashtag)

        postFeaturesTestData = postFeatures(preProcessedTestData, biGrams, \
                triGrams, fourGrams, fiveGrams, dTriGrams, dFourGrams, \
                adjective, emoticons, punctuation)

    print("\n*****Preprocessing complete*****")

    ########################## 3. Classification ############################
    
    print("\n****Implementing classifier*****")
    if testData: # classifying on unlabeled test data
        svmClassifier(trainFolds[0], testFolds[0], \
                postFeaturesData, postFeaturesTestData, None, crossVal)
    else: # cross validation
        svmScorer(trainFolds, testFolds, postFeaturesData, postFeaturesData)

main()
