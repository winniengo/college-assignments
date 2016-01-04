""" 
ngrams.py
Analysis of unigram, bigram, and trigram models of three categories of texts: 
editorial, adventure, romance

Written By: Mike Superdock and Winnie Ngo
"""
#!/usr/bin/python

import re, string, os

"""
DISCUSSION QUESTIONS:
(2a)
11.907% of romance unigrams and 14.032% of adventure unigrams don't appear in
editorial, respectively. 

(2b)
56.973% of romance bigrams and 59.51% of adventure bigrams don't appear in
editorial, respectively. 

89.689% of romance trigrams and 80.854% of adventure trigrams don't appear in
editorial, respectively. 

(2c) We were not surprised that the percent of n-grams increased as n
increased. Although two documents may contain many of the same unigrams,
it is unlikely that any combination of two adjacent unigrams (bigrams)
in one text will also appear in the other text. The odds are even less
likely when combining three adjacent unigrams to form a trigram.

If anything, we were surprised by how many of the trigrams and bigrams were
shared between two separate texts. We did not expect for 10-20% of the
trigrams that appeared in romance and adventure texts to also appear in the
editorial text.

(2d)(i)

If we trained our language model on two categories rather than one, it
improves our results. Using two categories provides for a greater variety
of types in our training set, because different categories often use
different language.

Of the three combinations that we tried for unigrams, our best result was
found when determining the number of romance tokens that did not appear
in either the editorial or adventure categories (7.327%). The best result
for bigram tokens was also found when determining the number of romance
tokens that did not appear in either the editorial or adventure categories
(43.265%). We suspect that this occured because the combination of editorial
and adventure texts contains more variety in vocabulary than any of the other
combinations of 2 categories.

(2d)(ii)

Using chunk D as our test data does change our results because it is
composed of all three categories. We compared these against the remaining
three chunks (A,B, and C) which also were composed of sections from all
three categories. We know that each category uses different word types more
commonly than others. By adding all three of these categories together in both
the training set and the testing set, we expect to find lower percentages
than we did in the earlier questions. This is because the same variety in
vocabulary that exists in chunk D is also reflected in chunks A, B, and C.
We found that this expectation was confirmed by our results. 

We repeated the experiment 4 times, each time using a different chunk as
our test data and the remaining three as our training set. For unigrams
they consistently yielded percentages around 7% and for bigrams they
consistently yielded percentages around 45%. These results were lower,
but not that much lower, than our results from earlier questions.
"""


"""
converts a text file into a list of tokens found in file
params: category, the name of the .txt file
returns: a list of file's tokens - unigram model
"""
def read_file(category):
    infile = open('/data/cs65/lab02/' + category + '.txt', 'r')
    lines = infile.read().splitlines()
    infile.close()
    
    return lines

"""
compares the ngrams of one text (text1) to another's (text2)
params: tokenList, a list of text file's ngrams (tokens, not types) 
        refList, a list of text file's types
returns: percentage of ngrams that appear in text1 and not in text2
"""
def compare(tokenList, refList):
    counter = 0
    refTypes = set(refList)
    for token in tokenList:
        if token not in refTypes:
            counter += 1

    return counter/float(len(tokenList)) * 100

"""
creates a list of trigrams froms a list of unigrams (tokens, not types) where
one trigram is constructed of three consecutive unigrams separated by a space
params: list, list of text file's unigrams 
returns: trigrams, list of textfile's trigrams 
"""
def create_trigrams_list(lst):
    trigrams = []
    for index in range(len(lst)-2):
        trigrams.append(lst[index] + ' ' +  lst[index+1] + ' ' + lst[index+2])
    
    return trigrams

"""
creates a list of bigrams froms a list of unigrams (tokens, not types) where
one bigram is constructed of two consecutive unigrams separated by a space
params: list, list of text file's unigrams 
returns: trigrams, list of textfile's bigrams 
"""
def create_bigrams_list(lst):
    bigrams = []
    for index in range(len(lst)-1):
        bigrams.append(lst[index] + ' ' + lst[index+1])
    
    return bigrams
"""
creates a 'chunk', a combination of a quarter of each categories' ngram. 
param: list1, list2, list3, the ngram list of each category
       val, the number of chunk where 1 = first 25%, 2 = second 25%, etc.
returns: a list of ngrams across all three categories
"""
def create_chunk(list1, list2, list3, val):

    chunk = []
    for lst in [list1, list2, list3]:
        length = len(lst)
        startIdx = int(length*(val*0.25))
        endIdx = int(length*((val+1)*0.25))
        chunk += lst[startIdx:endIdx]
    return chunk

"""
calculates the percentage of one category's unigrams to editorial's 
params: lists of romance, editorial, adventure unigrams
"""
def question2a(rTokens, eTokens, aTokens):
    print "-----2(a)-----"
    percent_r_not_in_e = compare(rTokens, eTokens)
    percent_a_not_in_e = compare(aTokens, eTokens)
    
    print "%.3f%% of romance tokens don't appear in editorial" \
            % percent_r_not_in_e    
    print "%.3f%% of adventure tokens don't appear in editorial" \
            % percent_a_not_in_e

"""
calculates the percentage of one category's bigrams to editorial's 
params: lists of romance, editorial, adventure bigrams
"""
def question2b_1(rBigrams, eBigrams, aBigrams):
    print "\n-----2(b)-----"
    print "%.3f%% of romance bigrams don't appear in editorial" \
            % compare(rBigrams, eBigrams)    
    print "%.3f%% of adventure bigrams don't appear in editorial" \
            % compare(aBigrams, eBigrams)

"""
calculates the percentage of one category's trigrams to editorial's 
params: lists of romance, editorial, adventure trigrams
"""
def question2b_2(rTrigrams, eTrigrams, aTrigrams):
    print "\n%.3f%% of romance trgrams don't appear in editorial" \
            % compare(rTrigrams, eTrigrams)
    print "%.3f%% of adventure trigrams don't appear in editorial" \
            % compare(aTrigrams, eTrigrams)

"""
calculates percentage of one category's unigrams and bigrams  to those of  two
categories
params: lists of romance, editorial, adventure unigrams and bigrams
"""
def question2d_1(rTokens, aTokens, eTokens, rBigrams, aBigrams, eBigrams):
    print "\n-----2(d)(i)-----"
    print "%.3f%% of romance tokens don't appear in editorial + adventure" \
            % compare(rTokens, aTokens + eTokens)
    print "%.3f%% of adventure tokens don't appear in editorial + romance" \
            % compare(aTokens, eTokens + rTokens)
    print "%.3f%% of editorial tokens don't appear in romance + adventure" \
            % compare(eTokens, rTokens + aTokens)

    print "\n%.3f%% of romance bigrams don't appear in editorial + adventure" \
            % compare(rBigrams,aBigrams + eBigrams)  
    print "%.3f%% of adventure bigrams don't appear in editorial + romance" \
            % compare(aBigrams, rBigrams + eBigrams)
    print "%.3f%% of editorial bigrams don't appear in romance + adventure" \
            % compare(eBigrams, rBigrams + aBigrams)

"""
params: lists of romance, editorial, adventure unigrams and bigrams
"""
def question2d_2(rTokens, aTokens, eTokens, rBigrams, aBigrams, eBigrams):
    print"\n-----2(d)(ii)-----"    
    chunkA = create_chunk(rTokens, aTokens, eTokens, 0)
    chunkB = create_chunk(rTokens, aTokens, eTokens, 1)
    chunkC = create_chunk(rTokens, aTokens, eTokens, 2)
    chunkD = create_chunk(rTokens, aTokens, eTokens, 3)

    print "%.3f of chunk D unigrams don't appear in chunks A, B, C" \
            % compare(chunkD, chunkA + chunkB + chunkC)
    print "%.3f of chunk A unigrams don't appear in chunks D, B, C" \
            % compare(chunkA, chunkD + chunkB + chunkC)
    print "%.3f of chunk B unigrams don't appear in chunks A, D, C" \
            % compare(chunkB, chunkA + chunkD + chunkC)
    print "%.3f of chunk C unigrams don't appear in chunks A, B, D" \
            % compare(chunkC, chunkA + chunkB + chunkD)

    b_chunkA = create_chunk(rBigrams, aBigrams, eBigrams, 0)
    b_chunkB = create_chunk(rBigrams, aBigrams, eBigrams, 1)
    b_chunkC = create_chunk(rBigrams, aBigrams, eBigrams, 2)
    b_chunkD = create_chunk(rBigrams, aBigrams, eBigrams, 3)
    print "\n%.3f of chunk D bigrams don't appear in chunks A, B, C" \
            % compare(b_chunkD, b_chunkA + b_chunkB + b_chunkC)
    print "%.3f of chunk A bigrams don't appear in chunks D, B, C" \
            % compare(b_chunkA, b_chunkD + b_chunkB + b_chunkC)
    print "%.3f of chunk B bigrams don't appear in chunks A, D, C" \
            % compare(b_chunkB, b_chunkA + b_chunkD + b_chunkC)
    print "%.3f of chunk C bigrams don't appear in chunks A, B, D" \
            % compare(b_chunkC, b_chunkA + b_chunkB + b_chunkD)

def main():
    print "\nCS 65: Lab 2 Q2"

    #load text files
    rTokens = read_file('romance')
    eTokens = read_file('editorial')
    aTokens = read_file('adventure')
    
    #question 2a
    question2a(rTokens, eTokens, aTokens)

    #question 2b
    rBigrams = create_bigrams_list(rTokens)
    eBigrams = create_bigrams_list(eTokens)
    aBigrams = create_bigrams_list(aTokens)
    question2b_1(rBigrams, eBigrams, aBigrams)

    rTrigrams = create_trigrams_list(rTokens)
    eTrigrams = create_trigrams_list(eTokens)
    aTrigrams = create_trigrams_list(aTokens)
    question2b_2(rTrigrams, eTrigrams, aTrigrams)

    #question 2d
    question2d_1(rTokens, aTokens, eTokens, rBigrams, aBigrams, eBigrams)
    question2d_2(rTokens, aTokens, eTokens, rBigrams, aBigrams, eBigrams)

main()
