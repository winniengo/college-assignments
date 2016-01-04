import nltk, string, math
from MorphoStandard import *
from algorithms import *

##### Methods for setting up analysis #######
def createCharDictionary():

    dictionary = {}
    charList = "abcdefghijklmnopqrstuvwxyz-'"
    for index in range(len(charList)):
        dictionary[charList[index]] = index+1
    return dictionary

def corpus_menu():
    print ("\n(1)Brown (2)Reuters (3)Scrabble (4)Google (0)Quit")
    return input('Pick your corpus: ')

def createWordList(corpus_number):
    
    types = None
    if corpus_number == 1:
        brownWords = nltk.corpus.brown.words()
        types = set(word.lower() for word in brownWords)
    elif corpus_number == 2:
        reutersWords = nltk.corpus.reuters.words()
        types = set(word.lower() for word in reutersWords)
    elif corpus_number == 3:
        scrabbleWordList = open('/data/cs65/corpora/Scrabble/all.txt')
        scrabbleWords = [x.rstrip() for x in scrabbleWordList]
        types = set(word.lower() for word in scrabbleWords)
        scrabbleWordList.close()
    elif corpus_number == 4:
        wordcts = [x.split() for x in \
                open('/data/google/1gms/word_only_sorted')]
        words = [word.lower() for word, freq in wordcts]
        types = set(words)

    punctuation = [p for p in string.punctuation if p != "-" and p != "'"]
    lst = []
    for word in types:
        badWord = False
        for char in word:
            if char.isdigit() or char in punctuation or char in ["ü"]:
                badWord = True
                break
        if not badWord:
            lst.append(word)

    return lst

def createEmptyTrieList():

    lst = [None]*29
    lst[0] = [0, 0, False] # lst[0][0] = S, lst[0][1] = D lst[0][2] = bool
                           # S = successor variety count
                           # D = total successor count
                           # bool = true if end of word
    return lst

def createTrie(dictionary, wordList, forward):
    trie = createEmptyTrieList()
    for word in wordList:
        sublist = trie
        if not forward:
            word = word[::-1]
        for char in word:
            sublist[0][1] += 1          # update count of sublist
            index = dictionary[char]    # find index in list
            if sublist[index] == None:  # if sublist doesnt exist
                sublist[0][0] += 1
                sublist[index] = createEmptyTrieList()
            sublist = sublist[index]
        sublist[0][2] = True
    return trie

##### Methods for analyzing data #####
def accumulateWordData(word, trie, charDict): 
    
    successorVarietyList = []
    successorTotalList = []
    endOfWordList = []

    subList = trie
    for char in word:
        index = charDict[char]
        if subList != None:
            subList = subList[index]
        
        if subList == None:
            svCount = 0
            sCount = 0
            endOfWord = False
        else:
            svCount = subList[0][0]
            sCount = subList[0][1]
            endOfWord = subList[0][2]

        successorVarietyList.append(svCount)
        successorTotalList.append(sCount)
        endOfWordList.append(endOfWord)

    return successorVarietyList, successorTotalList, endOfWordList


def accumulateWordEntropyData(word, trie, charDict):

    subList = trie
    charList = "abcdefghijklmnopqrstuvwxyz-'"
    entropyList = []
    for char in word:
        #print("char: " + char)
        H_ai = 0
        D_ai = 0
        index = charDict[char]

        if subList != None:
            subList = subList[index]

        if subList == None:
            D_ai = 0
        else:
            D_ai = subList[0][1]
            if (subList[0][2]):
                D_ai += 1
            for c in charList:
                #print("c: " + c)
                D_aij = 0
                index2 = charDict[c]
                successorSubList = subList[index2]
                if successorSubList == None:
                    D_aij = 0
                else:
                    D_aij = successorSubList[0][1]
                    if successorSubList[0][2]:
                        D_aij += 1
                #print(D_ai)
                #print(D_aij)
                p = 0
                if D_aij != 0:
                    p = float(D_aij)/D_ai
                    H_ai += (-1*p*math.log(p)/math.log(2))
        entropyList.append(H_ai)
    return entropyList


def reverseSegment(segments):

    segments = segments[::-1]
    i = 0
    for s in segments:
        segments[i] = s[::-1]
        i += 1

    return segments

def analyzeResults(testDict, trueDict, countEndCuts):
    tp = 0 # no. of true positives
    fp = 0 # no. of false positives
    tb = 0 # total no. of true boundaries (tp + false negatives)
    for word, segments in testDict.items():
        trueSegments = trueDict[word]
        
        i = j = 0
        cutIndices = [0]
        trueCutIndices = [0] # count beginning of word as a cut
        for segment in segments: # count end of word as a cut
            i += len(segment)
            cutIndices.append(i)
        for segment in trueSegments:
            j += len(segment)
            trueCutIndices.append(j)

        if not countEndCuts:
            cutIndices = cutIndices[1:-1]
            trueCutIndices = trueCutIndices[1:-1]

        #print word, cutIndices, trueCutIndices
        for index in cutIndices:
            if index in trueCutIndices:
                tp += 1
            else:
                fp += 1
            
        tb += len(trueCutIndices)

    if (tp+fp == 0):
        precision = 0
    else:    
        precision = float(tp) / (tp + fp) * 100

    if tb == 0:
        recall = 0
    else:
        recall = float(tp)/ tb * 100

    F = 2 * precision * recall / (precision + recall)
    return tp, fp, tb, precision, recall, F

def printSegmentationInfo(dictionary, morphoStandard, val):

    lst = list(dictionary.items())[:50]
    print("\n\n-----Segmentation Info-----  %d" % (val))
    for key, value in lst:
        print(" ")
        print("word: ", key)
        print("correct segmentation: ", morphoStandard[key])
        print("our segmentation: ", value)
    
    return
    

def main():
    
    print("\nCreating morphology segment standard...")
    #morphoStandard = createStandard()
    morphoStandard = createStandard2()[1] #testing set
    #morphoStandard = createOwnStandard()
    testWords = list(morphoStandard.keys())
    #testSegmentations = list(morphoStandard.values())[:10]
    print("Morphology standard complete.")

    #choice = int(corpus_menu())
    choice = 3
    loop = False
    while choice != 0:

        if loop == False:

            print("\nReading in words for trie...")
            wordList = createWordList(choice)
            print("Read complete.")
    
            print("\nBuilding tries....")
            charDict = createCharDictionary() 
            forwardTrie = createTrie(charDict, wordList, True)
            backwardTrie = createTrie(charDict, wordList, False)
            print("Trie build Complete.\n")

            loop = True
        #"""
        dict1 = {}
        dict1a = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        dict5 = {}
        dict6 = {}
        dict7 = {}
        dict7a = {}
        dict8 = {}
        dict9 = {}
        dict10 = {}
        dict11 = {}
        dict12 = {}
        dict12a = {}
        dict13 = {}
        dict13a = {}
        dict13b = {}
        dict14 = {}
        dict15 = {}
        dict16 = {}
        dict17 = {}
        dict18 = {}
        """
        dict0 = {}
        dict1 = {}
        dict1a = {}
        dict2 = {}
        dict2a = {}
        dict3 = {}
        dict3a = {}
        dict4 = {}
        dict4a = {}
        dict5 = {}
        dict5a = {}
        dict6 = {}
        dict6a = {}
        dict7 = {}
        dict7a = {}
        dict8 = {}
        dict8a = {}
        dict9 = {}
        dict9a = {}
        dict10 = {}
        dict10a = {}
        dict11 = {}
        dict11a = {}
        dict12 = {}
        dict12a = {}
        dict13 = {}
        dict13a = {}
        dict14 = {}
        dict14a = {}
        dict15 = {}
        dict15a = {}
        dict16 = {}
        dict16a = {}
        dict17 = {}
        dict17a = {}
        dict18 = {}
        dict18a = {}
        dict19 = {}
        dict19a = {}
        dict20 = {}
        dict20a = {}
        dict21 = {}
        dict21a = {}
        dict22 = {}
        dict22a = {}
        dict23 = {}
        dict23a = {}
        dict24 = {}
        dict24a = {}
        dict25 = {}
        dict25a = {}
        dict26 = {}
        dict26a = {}
        dict27 = {}
        dict27a = {}
        dict28 = {}
        dict28a = {}
        dict29 = {}
        dict30 = {}
        """

        k = input("\nenter number to continue: ")
        print(" ")

        for word in testWords: #testWords[6:12]

            svList, sList, sEndList = \
                    accumulateWordData(word, forwardTrie, charDict)
            pvList, pList, pEndList = \
                    accumulateWordData(word[::-1], backwardTrie, charDict)
            sEntropyList = accumulateWordEntropyData(word, forwardTrie, \
                    charDict)
            pEntropyList = accumulateWordEntropyData(word[::-1], \
                    backwardTrie, charDict)
            
            
            """
            dict1[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 2.5)
            dict2[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 2.6)
            dict3[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 2.7)
            dict4[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 2.8)
            dict5[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 2.9)
            dict6[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3)
            dict7[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.1)
            dict8[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.2)
            dict9[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.3)
            dict10[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.4)
            dict11[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.5)
            dict12[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.6)
            dict13[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.7)
            dict14[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.8)
            dict15[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.9)
            dict16[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 4)
            dict17[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 4.1)
            dict18[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 4.2)
            dict19[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 4.3)
            dict20[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 4.4)
            dict21[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 4.5)
            dict22[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.1)
            dict23[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.2)
            dict24[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.3)
            dict25[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.4)
            dict26[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.5)
            dict27[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.6)
            dict28[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.7)
            dict29[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.8)
            dict30[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 7.9)
            """
            
            
            """
            dict1a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.0))
            dict1[word] = unionCutoffs(word, dict0[word], dict1a[word])
            dict2a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.1))
            dict2[word] = unionCutoffs(word, dict0[word], dict2a[word])
            dict3a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.2))
            dict3[word] = unionCutoffs(word, dict0[word], dict3a[word])
            dict4a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.3))
            dict4[word] = unionCutoffs(word, dict0[word], dict4a[word])
            dict5a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.4))
            dict5[word] = unionCutoffs(word, dict0[word], dict5a[word])
            dict6a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.5))
            dict6[word] = unionCutoffs(word, dict0[word], dict6a[word])
            dict7a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.6))
            dict7[word] = unionCutoffs(word, dict0[word], dict7a[word])
            dict8a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.7))
            dict8[word] = unionCutoffs(word, dict0[word], dict8a[word])
            dict9a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.8))
            dict9[word] = unionCutoffs(word, dict0[word], dict9a[word])
            dict10a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.9))
            dict10[word] = unionCutoffs(word, dict0[word], dict10a[word])

            dict11a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 4.0))
            dict11[word] = unionCutoffs(word, dict0[word], dict11a[word])
            dict12a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 4.1))
            dict12[word] = unionCutoffs(word, dict0[word], dict12a[word])
            dict13a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 13))
            dict13[word] = unionCutoffs(word, dict0[word], dict13a[word])
            dict14a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 14))
            dict14[word] = unionCutoffs(word, dict0[word], dict14a[word])
            dict15a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 15))
            dict15[word] = unionCutoffs(word, dict0[word], dict15a[word])
            dict16a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 16))
            dict16[word] = unionCutoffs(word, dict0[word], dict16a[word])
            dict17a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 17))
            dict17[word] = unionCutoffs(word, dict0[word], dict17a[word])
            dict18a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 18))
            dict18[word] = unionCutoffs(word, dict0[word], dict18a[word])
            dict19a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 19))
            dict19[word] = unionCutoffs(word, dict0[word], dict19a[word])
            dict20a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 20))
            dict20[word] = unionCutoffs(word, dict0[word], dict20a[word])

            dict21a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 21))
            dict21[word] = unionCutoffs(word, dict0[word], dict21a[word])
            dict22a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 22))
            dict22[word] = unionCutoffs(word, dict0[word], dict22a[word])
            dict23a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 23))
            dict23[word] = unionCutoffs(word, dict0[word], dict23a[word])
            dict24a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 24))
            dict24[word] = unionCutoffs(word, dict0[word], dict24a[word])
            dict25a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 25))
            dict25[word] = unionCutoffs(word, dict0[word], dict25a[word])
            dict26a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 26))
            dict26[word] = unionCutoffs(word, dict0[word], dict26a[word])
            dict27a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 27))
            dict27[word] = unionCutoffs(word, dict0[word], dict27a[word])
            dict28a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 28))
            dict28[word] = unionCutoffs(word, dict0[word], dict28a[word])
            """

            #for testing purposes
            #"""
            dict1[word] = cutoff(word, svList, 2)
            dict1a[word] = reverseSegment(cutoff(word[::-1], pvList, 17))

            dict2[word] = cutoffSandP(word, svList, pvList, 2, 16)
            dict3[word] = cutoffSplusP(word, svList, pvList, 25)

            dict4[word] = completeWord(word, sEndList)
            dict5[word] = reverseSegment(completeWord(word[::-1], pEndList))

            dict6[word] = unionCutoffs(word, dict1a[word], dict4[word])

            dict7[word] = peakAndPlateau(word, svList)
            dict7a[word] = reverseSegment(peakAndPlateau(word[::-1], pvList))
            
            dict8[word] = intersectCutoffs(word, dict7[word], dict7a[word])
            dict9[word] = spSumPeakPlateau(word, svList, pvList)

            dict10[word] = unionCutoffs(word, dict4[word], dict7a[word])

            dict11[word] = hybrid26(word, dict4[word], svList, pvList)

            dict12a[word] = reverseSegment(cutoff(word[::-1], pEntropyList, 3.9))
            dict12[word] = unionCutoffs(word, dict4[word], dict12a[word])

            dict13[word] = cutoffSplusP(word, sEntropyList, pEntropyList, 3.8)
            dict14[word] = completeWordRevised(word, sEndList)
            dict15[word] = unionCutoffs(word, dict14[word], dict12a[word])
            dict16[word] = completeWordRevised2(word, sEndList)
            dict17[word] = unionCutoffs(word, dict16[word], dict12a[word])
            dict18[word] = hyphenationImprovement(dict17[word])
            #"""
            
 
        TF = False #true if we count boundaries, false otherwise

        # print results and analysis
        
        print ("%-59s  %10s  %10s %10s" % ('Method', 'Precision', 'Recall', 'F-measure'))
        print ('-' * 95)
        #"""
        tp, fp, tb, precision, recall, F = analyzeResults(dict1, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
                ("1 successor >= cutoff*", precision, recall, F))
 
        #"""
        """
        tp, fp, tb, precision, recall = analyzeResults(dict1a, morphoStandard)
        print ("%-59s %10.3f%% %10.3f%%" % \
                ("1a predecessor >= cutoff", precision, recall))
        """
        #"""
        tp, fp, tb, precision, recall, F = analyzeResults(dict2, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
                ("2 successor >= cutoff and  predecessor >= cutoff*", \
                precision, recall, F))

   
        tp, fp, tb, precision, recall, F = analyzeResults(dict3, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
                ("3 successor + predecessor >= cutoff", precision, recall, F))


        tp, fp, tb, precision, recall, F = analyzeResults(dict4, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
                ("4 successor is complete word*", precision, recall, F))


        tp, fp, tb, precision, recall, F = analyzeResults(dict5, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
                ("5 predecessor is complete word", precision, recall, F))


        tp, fp, tb, precision, recall, F = analyzeResults(dict6, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
                ("6 successor is complete word or predecessor >= cutoff", \
                precision, recall, F))


        tp, fp, tb, precision, recall, F = analyzeResults(dict7, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
                ("7 successor at peak/plateau*", precision, recall, F))

        #"""
        """
        tp, fp, tb, precision, recall = analyzeResults(dict7a, morphoStandard)
        print ("%-59s %10.3f%% %10.3f%%" % \
                ("7a predecessor at peak/plateau", precision, recall))
        """
        #"""
        tp, fp, tb, precision, recall, F = analyzeResults(dict8, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
                ("8 successor and predecessor at peak/plateau", \
                precision, recall, F))


        tp, fp, tb, precision, recall, F = analyzeResults(dict9, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % ("9 successor + predecessor at \
                peak/plateau", precision, recall, F))


        tp, fp, tb, precision, recall, F = analyzeResults(dict10, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
              ("10 successor is complete word or predecessor @ peak/plateau", \
              precision, recall, F))


        tp, fp, tb, precision, recall, F = analyzeResults(dict11, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % ("11 hybrid of experiments 2 and 6", \
              precision, recall, F))

        
        tp, fp, tb, precision, recall, F = analyzeResults(dict12, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
              ("12 successor is complete word or predecessor entropy @ p/p", \
              precision, recall, F))

        tp, fp, tb, precision, recall, F = analyzeResults(dict13, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
              ("13 successor + predecessor entropies >= cutoff", \
              precision, recall, F))

        tp, fp, tb, precision, recall, F = analyzeResults(dict14, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % ("Complete Word Revised", \
              precision, recall, F))

        tp, fp, tb, precision, recall, F = analyzeResults(dict15, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
              ("Complete Word Revised and Predecessor Entropy @ p/p", \
              precision, recall, F))

        tp, fp, tb, precision, recall, F = analyzeResults(dict16, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % ("Complete Word Revised 2", \
              precision, recall, F))

        tp, fp, tb, precision, recall, F = analyzeResults(dict17, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % \
              ("Complete Word Revised and Predecessor Entropy @ p/p", \
              precision, recall, F))

        tp, fp, tb, precision, recall, F = analyzeResults(dict18, morphoStandard, TF)
        print ("%-59s %10.1f%% %10.1f%% %10.1f" % ("Hyphenation Improvement", \
              precision, recall, F))

        
        
        printSegmentationInfo(dict1, morphoStandard, 1)
        printSegmentationInfo(dict2, morphoStandard, 2)
        printSegmentationInfo(dict3, morphoStandard, 3)
        printSegmentationInfo(dict4, morphoStandard, 4)
        printSegmentationInfo(dict5, morphoStandard, 5)
        printSegmentationInfo(dict6, morphoStandard, 6)
        printSegmentationInfo(dict7, morphoStandard, 7)
        printSegmentationInfo(dict8, morphoStandard, 8)
        printSegmentationInfo(dict9, morphoStandard, 9)
        printSegmentationInfo(dict10, morphoStandard, 10)
        printSegmentationInfo(dict11, morphoStandard, 11)
        printSegmentationInfo(dict12, morphoStandard, 12)
        printSegmentationInfo(dict13, morphoStandard, 13)
        printSegmentationInfo(dict14, morphoStandard, 14)
        printSegmentationInfo(dict15, morphoStandard, 15)
        printSegmentationInfo(dict16, morphoStandard, 16)
        printSegmentationInfo(dict16, morphoStandard, 16)
        

        
        
        """
        tp, fp, tb, precision, recall = analyzeResults(dict1, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("1", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict2, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("2", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict3, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("3", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict4, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("4", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict5, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("5", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict6, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("6", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict7, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("7", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict8, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("8", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict9, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("9", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict10, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("10", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict11, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("11", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict12, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("12", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict13, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("13", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict14, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("14", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict15, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("15", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict16, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("16", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict17, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("17", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict18, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("18", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict19, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("19", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict20, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("20", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict21, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("21", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict22, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("22", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict23, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("23", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict24, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("24", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict25, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("25", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict26, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("26", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict27, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("27", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict28, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("28", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict29, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("29", \
              precision, recall))
        tp, fp, tb, precision, recall = analyzeResults(dict30, morphoStandard, TF)
        print ("%-59s %10.3f%% %10.3f%%" % \
              ("30", \
              precision, recall))
        
        """       
        
        choice = 3


main()
