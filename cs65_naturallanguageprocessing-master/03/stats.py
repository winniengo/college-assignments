"""
stats.py

this program analyzes the number of unigram tokens, bigram tokens, and tags
of news files in the brown corpus and then repeats this analysis for
science fiction files in the brown corpus. 

Authors: Michael Superdock, Winnie Ngo
"""


import nltk, string
from nltk.book import * #may not need this on school computers
from collections import Counter


"""
question1 - finds the number of tokens and the number of types given a list
of words

params: words - a list of words
returns: numTokens - the number of tokens in the list of words
         numTypes - the number of types in the list of words
"""
def question1(words):

    numTokens = len(words)
    print("numTokens = " + str(numTokens))
    numTypes = len(set(words))
    print("numTypes = " + str(numTypes))
    return numTokens, numTypes

"""
question2 - finds the ten most common words in a list and prints them

params: words - a list of words
returns: none
"""
def question2(words):
    
    fdist = FreqDist(words)
    lst = fdist.most_common(10)
    for item in lst:
        print(item)

"""
reviseTags - takes a list of (word, tag) tuples and removes '-TL', '-HL',
'-NC', and 'FW-' from all tags.

params: taggedWords - a list of (word, tag) tuples
returns: updatedWords - an updated list of (word, tag) tuples
"""
def reviseTags(taggedWords):

    updatedWords = []
    for word, tag in taggedWords: #removes uwanted sections from all tags
        tag = tag.replace('-TL','')
        tag = tag.replace('-HL','')
        tag = tag.replace('-NC','')
        tag = tag.replace('FW-','')
        updatedWords.append((word,tag))
    return updatedWords

"""
question3 - takes a list of (word, tag) tuples and prints the 10 most commonly
found tags

params: taggedWords - a list of (word, tag) tuples
returns: none
"""
def question3(taggedWords):
    
    fdist = mostCommonTags(taggedWords)
    lst = fdist.most_common(10) #a tuple list of 10 most common tags and freqs
    for item in lst:
        print(item)

"""
mostCommonTags - takes a list of (word, tag) tuples and returns a frequency
distribution of all of the tags

params: taggedWords - a list of (word, tag) tuples
returns: a frequency distribution of all of the tags
"""
def mostCommonTags(taggedWords):

    tagList = []
    for word, tag in taggedWords:
        tagList.append(tag)
    return FreqDist(tagList)

"""
question4 - takes a list of bigrams and prints the 5 most common ones

params: bigrams - a list of bigrams
returns:  none
"""
def question4(bigrams):
      
    fdist = FreqDist(bigrams)
    lst = fdist.most_common(5) #a tuple list of 5 most common bigrams and freqs
    for item in lst:
        print(item)

"""
question4p2 - removes all bigrams where one entry in the bigram is a
punctuation mark and then prints the 5 most common remaining bigrams

params: bigrams - a list of bigrams
returns: none
"""
def question4p2(bigrams):
    newList = []
    for bigram in bigrams:
        if bigram[0] in string.punctuation: #don't include bigrams where first
            continue                        #item is punctuation
        elif bigram[1] in string.punctuation: #don't include bigrams where
            continue                          #second item is punctuation
        else:
            newList.append(bigram) #store all other bigrams
    fdist = FreqDist(newList)
    lst = fdist.most_common(5) #tuple list of 5 most common bigrams and freqs
    for item in lst:
        print(item)

"""
createHistogram - creates a dictionary of counters (a histogram) which stores
all tags for each word type and the frequency with which these tags occur in
the taggedWords list

params: taggedWords - a list of (word, tag) tuples
returns: dictionary - a dictionary of counters storing the frequency of the
                      tags for all words
"""
def createHistogram(taggedWords):

    dictionary = {}
    for word, tag in taggedWords:
        if dictionary.get(word) == None: #if this is first time seeing word
            dictionary[word] = Counter() #make dict value a new counter
            dictionary[word][tag] += 1   #and just update counter
        else:
            dictionary[word][tag] += 1 #otherwise just update counter for entry
    return dictionary

"""
question5 - iterates through and finds the number of types and tokens for all
words with only one tag and then finds the number of types and tokens for all
words with two or more tags

params: taggedWords - a list of (word, tag) tuples
        numTokens - the total number of tokens in our list of words
        numTypes - the total number of types in our list of words
returns: none 
"""
def question5(taggedWords, numTokens, numTypes):
    
    dictionary = createHistogram(taggedWords)

    tokenCount = typeCount = tokenCount2 = typeCount2 = 0
    allCounters = list(dictionary.values())
    for counter in allCounters: #for word get set of tags and freqs
        values = list(counter.values()) #store frequencies as list
        if len(values) == 1: #if the word has only one tag
            typeCount += 1   #update type and token count
            tokenCount += values[0]
        elif len(values) > 2: #if the word has 2 or more tags
            typeCount2 += 1   #update type and token count
            for val in values:
                tokenCount2 += val
    
    #print percentages of types and tokens that meet the conditions above
    print("Types with 1 tag = %.3f%%" % (typeCount/float(numTypes)*100))
    print("Tokens with 1 tag= %.3f%%" % (tokenCount/float(numTokens)*100))
    print("Types with > 2 tags = %.3f%%" % (typeCount2/float(numTypes)*100))
    print("Tokens with > 2 tags = %.3f%%" % (tokenCount2/float(numTokens)*100))
    print("")

        
def main():

    #go through all questions 1-5 for 'news' and 'science_fiction' categories
    for category in ['news', 'science_fiction']:
        words = nltk.corpus.brown.words(categories=[category])
        print("\nquestion 1\n")
        numTokens, numTypes = question1(words)
        print("\nquestion 2\n")    
        question2(words)
        print("\nquestion 3\n") 
        taggedWords = nltk.corpus.brown.tagged_words(categories=[category])
        taggedWords = reviseTags(taggedWords)
        question3(taggedWords)
        print("\nquestion 4\n")    
        bigramList = list(bigrams(words))  
        question4(bigramList)
        print("\nquestion 4 part 2\n") 
        question4p2(bigramList)
        print("\nquestion 5\n")  
        question5(taggedWords, numTokens, numTypes)
        if category == 'news': print('\n---------question 6-------')

if __name__=='__main__':
    main()
