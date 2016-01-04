"""
zipf.py

practice using NLTK (an open-source toolkit for NLP) and answers to the related
discussion questions

Written By: Michael Superdock and Winnie Ngo 
"""


"""
DISCUSSION QUESTIONS:

(c)

'the' was the most common word in 14 out of the 18 texts. 'to' was the most
common word in 2 texts, 'I' in 1 text and 'and' in another. Noticeably, 'the' 
was second most common word in each of those texts. 

After lowercasing all of the words in each of the texts, 'the' remained the
most common word in 13 out of the 18. 'to' remained the most common word in the
same two texts. 'and' replaced 'I' in the text were 'I' was the most common
word. 'he' and 'and' replaced 'the' as the most common word in two other texts, 
respectively. Having a lot of sentences that start with 'He' and 'And' can
explain how 'the' got replaced as the most common word in these instances. 

'the', 'to', 'and', and 'of' were found in almost all of the top five lists of
most common words in the texts before and after the lowercasing. After
lowercasing the words in these texts, the order of the words in most texts
remained the same, while the count for each word went up.

(e)

Zipf's law closely approximates the empirical data in Alice in Wonderland
with only small deviations at the lowest and highest ranks. The remainder
of the empirical data is nearly consistent with Zipf's law.

Alice in Wonderland has 34110 tokens.

The Gutenberg Corpus has 2621613 tokens.

Zipf's law closely approximates the empirical data in the Gutenberg Corpus.
It appears that the Gutenberg Corpus is nearly as consistent with
Zipf's law as some of the smaller corpora. However, at very high ranks it
is clear that the frequencies of the words in Gutenberg Corpus deviate from
Zipf's law more dramatically than most of the smaller corpora. Regardless, I
would maintain that Zipf's law holds for both large and small corpora.

(f)

The plot of randomly generated strings have a trend fluctuates, due to the fact
that many words appear with similar frequencies (hence the staircase-like shape
of this plot). Nevertheless, the jagged progression of the plot still rises in
a manner similar to that of Zipf's law. This leads us to conclude that Zipf's
law is an accurate predictor of relative ranks and frequencies as a result of
both statistical probability and trends in language. Since there is a
statistical component that explains the trend of Zipf's law, I would also
conclude that there are likely other data sets that exist, which have nothing
to do with language, that follow Zipf's law as well.

"""
import nltk
import pylab
import math
import random
from warmups import wordsByFrequency, countWords

def question2c():
    print("\nQuestion 2c (Part 1):\n")
    fileids = nltk.corpus.gutenberg.fileids()
    for fileid in fileids:
        wordList = nltk.corpus.gutenberg.words(fileid)
        tupleList = wordsByFrequency(wordList)
        i = j = 0
        while i < 5:
            if tupleList[j][0].isalpha():
                print(tupleList[j], end=' ')
                i += 1
            j += 1
        print()

def question2c_part2():
    print("\nQuestion 2c (Part 2):\n")
    fileids = nltk.corpus.gutenberg.fileids()
    for fileid in fileids:
        wordList = nltk.corpus.gutenberg.words(fileid)
        lowerWordList = []
        for word in wordList:
            lowerWordList.append(word.lower())
        
        tupleList = wordsByFrequency(lowerWordList)
        i = j = 0
        while i < 5:
            if tupleList[j][0].isalpha():
                print(tupleList[j], end=' ')
                i += 1
            j += 1
        print()

def question2d():
    print("\nQuestion 2d:\n")
    words = nltk.corpus.gutenberg.words('carroll-alice.txt')

    counts = wordsByFrequency(words)
    n = len(counts)
    numTokens = len(words)
    print("Alice in Wonderland Token Count = " + str(numTokens))
    
    ranks = range(1,n+1)
    
    freqs = [freq/numTokens for (word, freq) in counts]
    pylab.loglog(ranks, freqs, label='alice')

    k = 1/H_approx(n) # where n is the number of word types
    freqs2 = [k/rank for rank in ranks]
    pylab.loglog(ranks, freqs2, label = "Zipf's law")
    
    pylab.xlabel('log(rank)')
    pylab.ylabel('log(freq)')
    pylab.legend(loc='lower left')
    print("\nAlice in Wonderland and Zipf's Law Plot Comparison:") 
    pylab.show()

def question2e(): #Repeat on the words from all the texts
    print("\nQuestion 2e:\n")
    words = nltk.corpus.gutenberg.words()
    counts = wordsByFrequency(words)
    n = len(counts)
    numTokens = len(words)
    print("Gutenberg Corpus Token Count = " + str(numTokens))
    
    ranks = range(1,n+1)
    
    freqs = [freq/numTokens for (word, freq) in counts]
    pylab.loglog(ranks, freqs, label='all words')

    k = 1/H_approx(n) # where n is the number of word types
    freqs2 = [k/rank for rank in ranks]
    pylab.loglog(ranks, freqs2, label = "zipf's law")
    
    pylab.xlabel('log(rank)')
    pylab.ylabel('log(freq)')
    pylab.legend(loc='lower left')
    print("\nGutenberg Corpus and Zipf's Law Plot Comparison:")
    pylab.show()


def question2f():
    print("\nQuestion 2f:")
    string = ""
    for i in range(2000000):
        string += random.choice("abcdefg ")
    words = string.split(' ')

    counts = wordsByFrequency(words)
    n = len(counts)
    numTokens = len(words)

    ranks = range(1,n+1)

    freqs = [freq/numTokens for (word, freq) in counts]
    pylab.loglog(ranks, freqs, label='all words')

    k = 1/H_approx(n) # where n is the number of word types
    freqs2 = [k/rank for rank in ranks]
    pylab.loglog(ranks, freqs2, label = "zipf's law")
    
    pylab.xlabel('log(rank)')
    pylab.ylabel('log(freq)')
    pylab.legend(loc='lower left')
    print("\nRandom Strings and Zipf's Law Plot Comparison:\n")
    pylab.show()


"""
calculates H(n) is the nth harmonic number where n is the number of word types 
in the corpus and 1/H(n) yields the constant k in Zipf's law
"""
def H_approx(n):
    # Euler-Mascheroni constant
    gamma = 0.57721566490153286060651209008240243104215933593992
    return gamma + math.log(n) + 0.5/n - 1./(12*n**2) + 1./(120*n**4)

def main():
    print("CS 65: Lab 1 Q2")
    question2c()
    print()
    question2c_part2()
    print()
    question2d()
    print()
    question2e()
    print()
    question2f()

main()


