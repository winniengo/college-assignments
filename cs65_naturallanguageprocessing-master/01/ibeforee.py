"""
ibeforee.py
Analysis of trends of words including 'ie' and 'ei' found in various
Gutenberg corpus texts

Written By: Michael Superdock and Winnie Ngo
"""

"""
DISCUSSION QUESTIONS:

(3a)

i.

Types: 'cie' words appear 106 times. 'ie' words appear 1769 times. 
'cie' words make up 5.992% of all 'ie' word types.

Tokens: 'cie' words appear 986 times. 'ie' words apear 21520 times.
'cie' words make up 4.582% of all 'ie' word tokens.

Wehther counting types or tokens, 'cei' words consist of about 5% of the 
corpus. 

ii.

Types: 'cei' words appear 77 times. 'ei' words appear 372 times. 'cei' 
words make up 20.699% of all 'ei' word types.

Tokens: 'cei' words appear 1509 times. 'ei' words apear 16029 times. 'cei'
words make up 9.414% of all 'ei' word tokens.

When counting types, 'cei' words consist of ~20% of the corpus. However, 
when counting tokens, they consist of ~10% of the corpus.

iii.

Types: after a 'c', 'ie' is more likely. Out of the combined total of 'cie'
and 'cei' word types, 57.923% of them are 'cie'.

Tokens: after a 'c', 'ei' is more likely. Out of the combined total of 'cie'
and 'cei' word tokens, 60.481% of them are 'cei'.

(3b)

i.

Types: 'cie' = 62 times, 'ie' = 845 times, 'cie'/'ie' = 7.337%
Tokens: 'cie' = 742 times, 'ie' = 11583 times, 'cie'/'ie' = 6.406%

Removing words that contained 'eigh' or ended in 'ied', 'ies', 'ier' and 'iest'
does appear to slightly alter the results. Of the words containing 'ie', those
containing 'cie' now appear more often. This suggests that of the words that
contain the afforementioned endings, fewer of these endings are preceded by the
letter 'c'.

ii.

Types: 'cei' = 77 times, 'ei' = 303 times, 'cei'/'ei' = 25.413%
Tokens: 'cei' = 1509 times, 'ei' = 14947, 'cei'/'ei' = 10.096%

According to the numbers, there are no words in this corpus containing 'ceigh'
(or 'cei' along with the afforementioned endings). However there were words
containing 'eigh' (or 'ei' along with the afforementioned endings) which were
removed. This increased the percent of 'cei' relative to all 'ei' words from
20.699% to 25.413% when counting types and from 9.414% to 10.096% when counting
tokens.

iii.

Types: 'cei' words are now more likely. Out of the combined total of 'cie'
and 'cei' word types, 55.396% of them are 'cei'.

Tokens: 'cei' words are now more likely. Out of the combined total of 'cie'
and 'cei' word types, 67.037% of them are 'cei'.

This is simply because no 'cei' words were removed, and many 'cie' words were
removed.

(3c)

The rule 'i before e except after c' appears to be a good rule according to our
results. Considering there are more tokens and types containing 'cei' than
there are tokens and types contianing 'cie', this rule provides a decent
guideline. This result is made stronger by the large number of words with 'cie'
and 'cei' in the corpus. 

Other rules that may also be decent include substitutions of 'c' with the
letters 'b', 'e', 'h', and 'n'. These letters follow the same pattern described
above where the pattern '*ei' is more common (in either tokens or in types)
than the pattern '*ie'. However, the words including these phrases have
a lower number of total tokens and types, leading us to have less confidence in
them as possible rules.
"""


import nltk
import pylab
from warmups import wordsByFrequency 

"""
types, number of unique words
returns: a list of tuples of (word, 1)
"""
def getTypes(words):
    tuples = []
    for word in set(words):
        tuples.append([word, 1])
    return tuples

"""
tokens, each occurrence of the word
retirms: a list of tuples of (word, number of occurrences)
"""
def getTokens(wordsList):
    return wordsByFrequency(wordsList)

def question3():

    print("\n---------3a----------")
    words = nltk.corpus.gutenberg.words()
    types = getTypes(words)
    tokens = getTokens(words)
    
    print("\ntypes")
    calculateFrequencies(types, 'c')
    print("\ntokens")
    calculateFrequencies(tokens, 'c')

    print("\n---------3b------------")
    new_types = removeWords(types)
    new_tokens = removeWords(tokens)

    print("\nnew types")
    calculateFrequencies(new_types, 'c')
    print("\nnew tokens")
    calculateFrequencies(new_tokens, 'c')

    print("\n----------3c----------")
    print(' ')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        print("("+letter+")")
        print("\ntypes")
        calculateFrequencies(new_types, letter)
        print("\ntokens")
        calculateFrequencies(new_tokens, letter)
        print(' ')

"""
calculates the frequency of
i. 'cie' relative to all 'ie' words
ii. 'cei' relative to all 'ei' words 
iii. 'cei' relative to all 'cei' and 'cie' words

arguments: 
dictionary, list of tuples of [word, count]
letter, replaces 'c' with another character
"""
def calculateFrequencies(dictionary, letter):

    cie = letter + 'ie'
    cei = letter + 'ei'
    num_cie = num_ie = num_ei = num_cei = 0
    for pair in dictionary:
        if cie in pair[0]:
            num_cie += pair[1]
        if 'ie' in pair[0]:
            num_ie += pair[1]
        if 'ei' in pair[0]:
            num_ei += pair[1]
        if cei  in pair[0]:
            num_cei += pair[1]
    
    if num_ie > 0:
        print("'%sie'/'ie' = %d/%d = %.5f" \
                % (letter, num_cie, num_ie, num_cie/float(num_ie)))
    if num_ei > 0:
        print("'%sei'/'ei' = %d/%d = %.5f" \
                % (letter, num_cei, num_ei, num_cei/float(num_ei)))
    if (num_cie + num_cei) > 0:
        print("'%sei'/('%sie'+'%sei') = %d/(%d + %d) = %.5f" \
                % (letter, letter, letter, num_cei, num_cie, num_cei, \
                num_cei/float(num_cie + num_cei)))

"""
remove words ending in 'ied','ies','ier','iest' and those containing 'eigh'
return: list of tuples [word, count] 
"""
def removeWords(tuples):
    new_tuples = []
    endings = ['ied', 'ies', 'ier']
    count = 0
    for pair in tuples:
        if (pair[0][-3:]) in endings:
            continue
        elif pair[0][-4:] == 'iest':
            continue
        elif 'eigh' in pair[0]:
            continue

        new_tuples.append([pair[0], pair[1]])
    print(str(count))
    return new_tuples

def main():
    print("\nCS 65: Lab 1 Q3")
    question3()

main()
