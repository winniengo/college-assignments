"""
pos.py

Using two texts (a training text consisting of the first 33 files in the
news category and a test text consisting of the last 11 files in the news
category), this program tags the test text using the statistics gathered
from the training text. We then do a series of analyses on our results
and introduce new training sets.

Authors: Michael Superdock, Winnie Ngo
"""
from nltk.corpus import brown
from stats import *
import random


"""
finds the maximum likelihood estimation of P(T = t|W = w) which represents
the probability that the tag t is the correct tag for the word w

params: tag - tag t
        word - word w
return: P calculated by dividing the number of times word w is used as tag t by 
the number of times word w occurs
"""
def probability(histogram, word, tag):
    counter = histogram[word] #find the tags for a given word
    tagCount = 0
    for val in list(counter.values()): #for each tag find the value
        tagCount += val #find the total number of tags
    return (histogram[word][tag])/float(tagCount) #return the number of tags
                            #for a given word divided by the total tag count


"""
for each word token in the test text, assign the most likely part of speech tag
using P(T=t|W=w). For words that occur in the test text but not in the training
text, can use several different methods (ie. assign most common tag in training
corpus, assign random tag, etc.)

params: histogram - a dictionary of counters that maps a word to its tags
                    (with frequencies)
        testTokens - a list of (word, tag) tuples
        defaultTag - a list of default tags we choose randomly to assign to new
                     words
return: taggedTokens - a list of tuples (token, maxTag) where token is a
                       word in the test text and maxTag is the most likely tag
        unknownTokens - a list of tuples (token, defaultTag, index) where token
                        is a word that didn't occure in the training set,
                        defaultTag is the tag we assigned it randomly, and
                        index is the words position in the original text
"""
def assignTags(histogram, testTokens, defaultTags):

    taggedTokens = [] #tokens with the tags that we assigned them
    unknownTokens =  [] #tokens that were not found in histogram
    index = 0
    for token, tag in testTokens: #for each token
        if histogram.get(token) == None: #if we don't find it in our histogram
            defaultTag = random.choice(defaultTags) #assign tag randomly
            taggedTokens.append((token, defaultTag))
            unknownTokens.append((token, defaultTag, index))
            index += 1
            continue
        
        #retrieve counter of all tags for a given word token
        counter = list(histogram[token].keys())
        maxTag = "" #tag with the highest likelihood of being assigned to word
        maxProb = 0 #probability of a tag being assigned to word
        for i in range(len(counter)): 
            prob = probability(histogram, token, counter[i])
            if prob > maxProb: #update probability and tag if a more likely
                maxProb = prob                                #tag is found
                maxTag = counter[i]
        
        taggedTokens.append((token, maxTag))
        index += 1
    return taggedTokens, unknownTokens


"""
prints each word token in the test text, our guess of the part of speech, the
actual part of speech (provided by the corpus), and either a 1 of 0 depending
on whether our guess was correct or not (1 is correct).

params: tagGuesses - list of tulpes (word, our guess of tag)
        tagTruth - list of tuples (word, actual tag)
return: incorrect - list of tuples (word, our tag guess, actual tag) for all
                    cases where the guess and actual tag are not equal

"""
def analyzeAssignedTags(tagGuesses, tagTruth):
    print("%20s  %8s  %8s  %6s" % ('word', 'guess', 'truth', 'result')) 
    print('%20s  %8s  %8s  %6s' % ('----', '-----', '-----', '------'))
    correct = 0 #number of correct guesses
    incorrect = [] #list of tuples with incorrect guesses
    for i in range(len(tagTruth)):
        word = tagTruth[i][0] 
        if not word == tagGuesses[i][0]: #assert that we are comparing the same
            raise AssertionError()       #word in each of our lists
        if tagTruth[i][1] == tagGuesses[i][1]: #if guess is correct update vars
            result =  1
            correct += 1
        else:                   #if guess is incorrect append to incorrect list
            result = 0
            incorrect.append((word, tagGuesses[i][1], tagTruth[i][1]))
        print("%20s  %8s  %8s  %6d" % (word, tagGuesses[i][1], \
                tagTruth[i][1], result))
    print("\nPercentage of words tagged correctly: %.3f%%" \
            % (correct/float(len(tagTruth)) * 100))

    return incorrect


"""
this function takes all incorrectly guessed tags and outputs the corresponding
word, our guess, the actual tag, and the number of times this mistake was made

param: incorrectTags - a list of (word, guess, and truth) tuples where word is
                       a word we incorrectly tagged, guess is our tag attempt
                       and truth is the actual tag provided by the corpus
returns: none
"""
def analyzeIncorrectTags(incorrectTags):

    fdist = FreqDist(incorrectTags)
    print("\nTop 10 Most Common Incorrect Tags\n")
    print("%20s  %8s  %8s  %6s" % ('word', 'guess', 'truth', 'count'))
    print('%20s  %8s  %8s  %6s' % ('----', '-----', '-----', '-----'))
    topTen = fdist.most_common(10)
    
    for tup, count in topTen: #print out data for most common incorrect tags
        word = tup[0]
        guessTags = tup[1]
        truthTags = tup[2]
        print("%20s  %8s  %8s  %6d" % (word, guessTags, truthTags, count))


"""
this function takes the our tag guesses for tokens which we had not seen
in our training set and finds what percent of the time we accurately
guessed the right tag

params: tagGuesses - a list of (word, tag, index) where word is the word in
                     the corpus, tag is our guess, and index is its index in
                     the original text
        tagTruth - a list of (word, tag) tuples where the tag is the actual
                   tag provided by the corpus
returns: incorrect - a list of (word, guess, and truth) tuples where word is
                     a word we incorrectly tagged, guess is our tag attempt
                     and truth is the actual tag provided by the corpus
"""
def analyzeAssignedTagsUnknownTokens(tagGuesses, tagTruth):
    print("%20s  %8s  %8s  %6s" % ('word', 'guess', 'truth', 'result')) 
    print('%20s  %8s  %8s  %6s' % ('----', '-----', '-----', '------'))
    correct = 0
    incorrect = []
    for i in range(len(tagGuesses)): #look at each of the tags we have guessed
        word = tagGuesses[i][0]                    #because not in histogram
        index = tagGuesses[i][2]
        if tagGuesses[i][1] == tagTruth[index][1]: #guessed tag is correct
            result =  1                            
            correct += 1
        else: #guessed tag is incorrect
            result = 0
            incorrect.append((word, tagGuesses[i][1], tagTruth[index][1]))
        print("%20s  %8s  %8s  %6d" % (word, tagGuesses[i][1], \
                tagTruth[index][1], result))
    print("\n\nPercentage of words tagged correctly out of unknowns: %.3f%%" \
            % (correct/float(len(tagGuesses)) * 100))

    return incorrect


"""
answers Lab 03 Questions 7 - 11
"""
def main():

    #create our training set and testing set from the news category in the
    #brown corpus
    fileids = brown.fileids(categories = 'news')
    training_ids = fileids[:33]
    test_ids = fileids[33:]
    training = brown.tagged_words(fileids=training_ids)
    test = brown.tagged_words(fileids=test_ids)
    
    trainingTokens = reviseTags(training) #revise tags in our training set
    hist = createHistogram(trainingTokens) #used revised tags to make histogram
    fdist = mostCommonTags(trainingTokens)
    mostCommonTag = fdist.most_common(1)[0][0] #retrieve most common tag

    print("\nQuestion 8\n")
    tagGuesses, unknownTokens = assignTags(hist, test, [mostCommonTag])
    tagTruth = reviseTags(test)
    incorrectTags = analyzeAssignedTags(tagGuesses, tagTruth)
    
    print("\nQuestion 9\n")
    analyzeIncorrectTags(incorrectTags)

    print("\nQuestion 10\n")
    incorrectTags = analyzeAssignedTagsUnknownTokens(unknownTokens, tagTruth)
    analyzeIncorrectTags(incorrectTags)
    
    print("\nQuestion 10 part 2\n")
    # repeat test, but randomly assign the 10 most frequently found tags
    top5Tags = fdist.most_common(10)
    defaultTags = [tag for tag, count in top5Tags]
    tagGuesses, unknownTokens = assignTags(hist, test, defaultTags)
    incorrectTags = analyzeAssignedTagsUnknownTokens(unknownTokens, tagTruth)
    analyzeIncorrectTags(incorrectTags)

    print("\nQuestion 11\n")
    testids = brown.fileids(categories = 'romance')
    test = brown.tagged_words(fileids=testids)
    tagGuesses, unknowTokens = assignTags(hist, test, [mostCommonTag])
    tagTruth = reviseTags(test)
    incorrectTags = analyzeAssignedTags(tagGuesses, tagTruth)
    analyzeIncorrectTags(incorrectTags)

main()
