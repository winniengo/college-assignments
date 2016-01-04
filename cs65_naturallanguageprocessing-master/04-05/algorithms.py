"""
Algorithms used in paper. 13 correspond to algorithms used in Hafer and Weiss. 5 are
algorithms we wrote that improved upon the results found in the first 13.

Michael Superdock and Winnie Ngo
"""
def peakAndPlateau(word, freqCount):
    j = 0 #stores the index of the current char in the word
    i = 0 #stores the index of the beggining of the next segment
    segment = []
    while i < len(word)-1:              #if we reach a peak or plateu
        if i == 0:
            if freqCount[i] >= freqCount[i+1]:
                segment.append(word[j:i+1])
                j = i+1
        else:
            if freqCount[i]>= freqCount[i-1] and freqCount[i] >= freqCount[i+1]:
                segment.append(word[j:i+1]) #append word segment to list
                j = i+1
        i += 1
    segment.append(word[j:]) #append final segment to list

    return segment

def cutoff(word, svCount, k):
    i = 0 #stores the index of the current char in the word
    j = 0 #stores the index of the beggining of the next segment
    segment = []
    while i < len(word)-1: 
        if svCount[i] >= k: #if successor variety is greater than cutoff k
            segment.append(word[j:i+1]) #append word segment to list
            j = i+1
        i += 1
    segment.append(word[j:]) #append final segment to list

    return segment

def cutoffSplusP(word, svCount, pvCount, k):
    aligned_pvCount = pvCount[::-1] + [0]
    aligned_svCount = [0] + svCount

    i = 1 #stores the index of the current char in the word
    j = 0 #stores the index of the beggining of the next segment
    segment = []
    while i < len(word): 
        if aligned_svCount[i] + aligned_pvCount[i] >= k:
        # if the sum of the two counts reach the cutoff
            segment.append(word[j:i])
            j = i
        i += 1
    segment.append(word[j:]) #append final segment to list

    return segment

def cutoffSandP(word, svCount, pvCount, k1, k2):
    aligned_pvCount = pvCount[::-1] + [0]
    aligned_svCount = [0] + svCount

    i = 1 #stores the index of the current char in the word
    j = 0 #stores the index of the beggining of the next segment
    segment = []
    while i < len(word):
        if aligned_svCount[i] >= k1 and aligned_pvCount[i] >= k2: 
        # if successor and predecessor counts reach cutoff k
            segment.append(word[j:i]) #append word segment to list
            j = i
        i += 1
    segment.append(word[j:])

    return segment

def completeWord(word, endOfWordList):
    i = 0
    j = 0
    segment = []
    while i < len(word) - 1:
        if endOfWordList[i]:
            segment.append(word[j:i+1])
            j = i+1
        i += 1
    segment.append(word[j:])

    return segment

def completeWordRevised(word, endOfWordList):

    k = 0
    newList = []
    while k <  len(endOfWordList)-1:
        if k != len(endOfWordList)-2:
            if endOfWordList[k] == True and endOfWordList[k+1] == True:
                newList.append(False)
            elif endOfWordList[k] == True and endOfWordList[k+1] == False:
                newList.append(True)
            else:
                newList.append(False)
        else:
            newList.append(endOfWordList[k])
        k += 1
    newList.append(endOfWordList[k])
    
    i = 0
    j = 0
    segment = []
    while i < len(word) - 1:
        if newList[i]:
            segment.append(word[j:i+1])
            j = i+1
        i += 1
    segment.append(word[j:])

    return segment

def completeWordRevised2(word, endOfWordList):
    
    k = 0
    newList = []
    while k <  len(endOfWordList)-1:
        if k != len(endOfWordList)-2:
            if endOfWordList[k] == True and endOfWordList[k+1] == True:
                newList.append(False)
            elif endOfWordList[k] == True and endOfWordList[k+1] == False:
                newList.append(True)
            else:
                newList.append(False)
        else:
            if word[-1] == 's' or word[-1] == 'y':
                newList.append(endOfWordList[k])
            else:
                if endOfWordList[k] == True and endOfWordList[k+1] == True:
                    newList.append(False)
                elif endOfWordList[k] == True and endOfWordList[k+1] == False:
                    newList.append(True)
                else:
                    newList.append(False)
        k += 1
    newList.append(endOfWordList[k])
    
    i = 0
    j = 0
    segment = []
    while i < len(word) - 1:
        if newList[i]:
            segment.append(word[j:i+1])
            j = i+1
        i += 1
    segment.append(word[j:])

    return segment


"""
a cut is made if either the predecessor frequency exceeds a cutoff 
or the prefix is a complete word
"""
def unionCutoffs(word, pvCutoffSegments, svCompleteWords):
    i = j = 0
    pvCutIndices = []
    svCutIndices = []
    for segment in pvCutoffSegments:
        i += len(segment)
        pvCutIndices.append(i)
    for segment in svCompleteWords:
        j += len(segment)
        svCutIndices.append(j)

    cutIndices = list(set(pvCutIndices + svCutIndices))
    cutIndices = sorted(cutIndices)
    
    i = j = 0
    segment = []
    while i < len(word):
        if i in cutIndices:
            segment.append(word[j:i])
            j = i
        i += 1
    segment.append(word[j:])
    
    return segment

"""
a cut is made where both successor and predecessor counts are at a peak
or plateau
"""
def intersectCutoffs(word, svPeakSegments, pvPeakSegments):
    i = j = 0
    pvCutIndices = []
    svCutIndices = []
    for segment in pvPeakSegments:
        i += len(segment)
        pvCutIndices.append(i)
    for segment in svPeakSegments:
        j += len(segment)
        svCutIndices.append(j)

    cutIndices = []
    for i in range(1,len(word)+1):
        if i in pvCutIndices and i in svCutIndices:
            cutIndices.append(i)

    i = j = 0
    segment = []
    while i < len(word):
        if i in cutIndices:
            segment.append(word[j:i])
            j = i
        i += 1
    segment.append(word[j:])

    return segment

"""
a cut is made where the sum of predecessor and successor frequency counts 
reaches a peak or plateau
"""
def spSumPeakPlateau(word, svCount, pvCount):

    aligned_pvCount = pvCount[::-1] + [0]
    aligned_svCount = [0] + svCount
    sumCount = [0]*len(aligned_svCount)

    for i in range(len(aligned_svCount)):
        sumCount[i] = aligned_svCount[i] + aligned_pvCount[i]
    
    j = 0 # counts segment indices in word
    i = 1 # index of character where summation occurs + segmentation is possible
    segment = []
    while i < len(word):              
        if sumCount[i] >= sumCount[i-1] and sumCount[i] >= sumCount[i+1]:
            segment.append(word[j:i]) # append word segment to list
            j = i
        i += 1
    segment.append(word[j:]) #append final segment to list
    
    return segment

"""
a cut is made wherever one is strongly indicated by one of the counts and
confirmed by a moderate value for the other count. Specifically, a cut is made
when the successor is a complete word and the predecessor is at least 5, or
where the predecessor count is at least 17 and the sucessor is at least 2.
"""
def hybrid26(word, sCompleteSegments, svCount, pvCount):
    scCutIndices = [] # cuts indicating successor(i,j) is a complete word
    i = 0
    for segment in sCompleteSegments:
        i += len(segment)         
        scCutIndices.append(i)

    reversed_pvCount = pvCount[::-1] + [0]

    i = 0
    j = 0
    segment = []
    while i < len(word)-1:  
        if (i+1) in scCutIndices and reversed_pvCount[i+1] >= 5:
            # index of cut corresponds to index-1 in word
            segment.append(word[j:i+1])
            j = i+1
        elif reversed_pvCount[i+1] >= 17 and svCount[i] >= 2:
            segment.append(word[j:i+1])
            j = i+1
        i += 1
    segment.append(word[j:])

    return segment

"""
extensions
"""
def hyphenationImprovement(segmentations):

    lst = []
    for seg in segmentations:
        newSplit = seg.rpartition("-")
        for item in newSplit:
            if item != '':
                lst.append(item)
    return lst

