"""
warmups.py - 
Functions for string parsing used in zipf.py and ibeforee.py and tested in the 
main function. 

Written By: Mike Superdock and Winnie Ngo
"""
from operator import itemgetter

"""
argument: s - a string
return: a list of lower-cased words in the same order as they appeared in s
"""
def getWords(s):
    return s.lower().split(' ')

"""
argument: wordList - a list of words
return: a dictionary whose keys are words in the word list and values are the
        frequencies with wich each word occurs in s
"""
def countWords(wordList):
    dictionary = {}
    for item in wordList:
        if item in dictionary:
            dictionary[item] += 1
        else:
            dictionary[item] = 1
    return dictionary

"""
argument: wordList - list of words
return: a list of (word, count) tuples sorted by count such that the first item
        in the list is the ost frequent item
"""
def wordsByFrequency(wordList):
    wordDict = countWords(wordList)
    tupleList = []
    for item in wordDict.items():
        tupleList.append(item)
    tupleList.sort(key=itemgetter(1), reverse=True)
    return tupleList

"""
tests getWords(), countWords(), wordsByFrequency() using a given string
"""
def main():
    print("\nCS 65: Lab 1 Warmup\n")
    
    string = "The cat in the hat ate the rat in the vat."
    print("string = " + string)
    
    wordList = getWords(string)
    print("\n(a) getWords(string) = ")
    print(wordList)

    wordDict = countWords(wordList)
    print("\n(b) countWords(wordList) = ")
    print(wordDict)

    tupleList = wordsByFrequency(wordList)
    print("\n(c) wordsByFrequency(wordList) = ")
    print(tupleList)

if __name__=='__main__':
    main()



