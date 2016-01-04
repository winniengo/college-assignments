"""
star.py - uses the star algorithm to identity a MSA.

Picks a string that has the maximal avergae alignment score to select 
the center. Uses a global alignment algorithm with linear gap penalty. 
Matches should have a score of +1, substitutions -1 and gaps -3. 

Winnie Ngo
"""

#############################################
"""
returns optimal score using 'highroad' for equally optimal alignments
param: up, match, left - three possible scores for F[i,j]
return: opt_scr, opt_arw - highest integer score and corresponding pointer
"""
def max_score(up, match, left):
    opt_scr = up
    opt_arw = 'up'

    if opt_scr < match:
        opt_scr = match
        opt_arw = 'match'

    if opt_scr < left:
        opt_scr = left
        opt_arw = 'left'

    return opt_scr, opt_arw

"""
constructs aligned sequence 1 and 2 using local alignment
param: x, y - (i, j) of the optimal score for the entire sequence 
        arrowMatrix - 2D matrix containing pointers to optimal score
        seq1, seq2 - the read-in sequences
return: aSeq1, aSeq2 - the read-in sequences after being aligned
        marker - string indicating a gap, perfect identity or substition
"""
def construct_alignment(arrowMatrix, seq1, seq2):
    aSeq1 = aSeq2 = '' # construct newly aligned sequences
    lenSeq1 = x = len(arrowMatrix[0])-1
    lenSeq2 = y = len(arrowMatrix)-1

    j = i = 1 # used to obtain the next amino acid to be added to the aligned
              # sequences from the read-in sequence 2 and 1 respectively 

    while i < lenSeq1 and j < lenSeq2:
        ptr = arrowMatrix[y][x]
        if ptr == "up": # insert gap in seq2, add next amino acid from seq1
            aSeq1 += seq1[-i]
            aSeq2 += '-'
            y -= 1
            i += 1
        elif ptr == "left": # insert gap in seq1, add next amino acid from seq2
            aSeq2 += seq2[-j]
            aSeq1 += '-'
            x -= 1
            j += 1
        elif ptr == 'match':
            aSeq1 += seq1[-i]
            aSeq2 += seq2[-j]
            y -= 1
            x -= 1
            j += 1
            i += 1

    aSeq1 = ''.join(reversed(aSeq1))
    aSeq2 = ''.join(reversed(aSeq2))

    # account for leftover char
    aSeq1 = seq1[:x] + aSeq1
    aSeq2 = seq2[:y] + aSeq2

    # account for gaps that occur before the sequence
    if len(aSeq1) > len(aSeq2):
        aSeq2 = '-'*(len(aSeq1) - len(aSeq2)) + aSeq2
    elif len(aSeq2) > len(aSeq1):
        aSeq1 = '-'*(len(aSeq2) - len(aSeq1)) + aSeq1
    
    return [aSeq1, aSeq2] # center, sequence

def globalAlgorithm(seq, center, scrMatrix, ptrMatrix, g):
    # initialize matrices
    scrMatrix[0][0] = 0
    for i in range(1, len(scrMatrix)):
        scrMatrix[i][0] = i * g
        ptrMatrix[i][0] = 'up'

    for j in range(1, len(scrMatrix[0])):
        scrMatrix[0][j] = j * g
        ptrMatrix[0][j] = 'left'

    # iterate through matrix solving for optimal score using F(i,j)
    for i in range(1,len(scrMatrix)):
        for j in range(1, len(scrMatrix[i])):
            left = scrMatrix[i][j-1] + g
            up = scrMatrix[i-1][j] + g
            if seq[i-1] == center[j-1]:
                match = scrMatrix[i-1][j-1] + 1
            else:
                match = scrMatrix[i-1][j-1] - 1

            #print up, match, left
            scrMatrix[i][j], ptrMatrix[i][j] = max_score(up, match, left)

    return scrMatrix, ptrMatrix

def calculateAvgScr(optScrAlign):
    total = 0
    for scr, alignments in optScrAlign:
            total += scr
    
    optAvgScr = float(total)/len(optScrAlign)
    return total, optAvgScr

########################################################

def main():
    # given the following sequences
    s0 = 'CTATTAATAC'
    s1 = 'TATTAATAC'
    s2 = 'CTATTAT'
    s3 = 'CTATTAATC'
    s4 = 'ATTAATAC'

    # use a global alignment algorithm with linear gap penaly to find the string with the
    # maximal average alignment score
    print '%-12s %s' % ('Sequence', 'Avg. Score')
    center = s0
    optScrAlign0 = [] # where each item is [optimal score, [aligned seq1, aligned seq2]]
    for seq in [s1, s2, s3, s4]:
        scrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]
        ptrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]

        scrMatrix, ptrMatrix = globalAlgorithm(seq, center, scrMatrix, ptrMatrix, -3)
        alignment = construct_alignment(ptrMatrix, center, seq)
        optScrAlign0.append([scrMatrix[len(seq)][len(center)], alignment])

    sumScr, avgScr = calculateAvgScr(optScrAlign0)
    print optScrAlign0
    print '%-12s %d/%d = %3.2f' % (center, sumScr, len(optScrAlign0), avgScr)
    
    center = s1
    optScrAlign1 = []
    for seq in [s0, s2, s3, s4]:
        scrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]
        ptrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]

        scrMatrix, ptrMatrix = globalAlgorithm(seq, center, scrMatrix, ptrMatrix, -3)
        alignment = construct_alignment(ptrMatrix, center, seq)
        optScrAlign1.append([scrMatrix[len(seq)][len(center)], alignment])
    
    sumScr, avgScr = calculateAvgScr(optScrAlign1)
    print optScrAlign1
    print '%-12s %d/%d = %3.2f' % (center, sumScr, len(optScrAlign1), avgScr)

    center = s2
    optScrAlign2 = []
    for seq in [s0, s1, s3, s4]:
        scrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]
        ptrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]

        scrMatrix, ptrMatrix = globalAlgorithm(seq, center, scrMatrix, ptrMatrix, -3)
        alignment = construct_alignment(ptrMatrix, center, seq)
        optScrAlign2.append([scrMatrix[len(seq)][len(center)], alignment])

    sumScr, avgScr = calculateAvgScr(optScrAlign2)
    print optScrAlign2
    print '%-12s %d/%d = %3.2f' % (center, sumScr, len(optScrAlign2), avgScr)

    center = s3
    optScrAlign3 = []
    for seq in [s0, s1, s2, s4]:
        scrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]
        ptrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]

        scrMatrix, ptrMatrix = globalAlgorithm(seq, center, scrMatrix, ptrMatrix, -3)
        alignment = construct_alignment(ptrMatrix, center, seq)
        optScrAlign3.append([scrMatrix[len(seq)][len(center)], alignment])
    sumScr, avgScr = calculateAvgScr(optScrAlign3)
    print optScrAlign3
    print '%-12s %d/%d = %3.2f' % (center, sumScr, len(optScrAlign3), avgScr)

    center = s4
    optScrAlign4 = []
    for seq in [s0, s1, s2, s3]:
        scrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]
        ptrMatrix = [[0]*(len(center)+1) for i in range(len(seq)+1)]

        scrMatrix, ptrMatrix = globalAlgorithm(seq, center, scrMatrix, ptrMatrix, -3)
        alignment = construct_alignment(ptrMatrix, center, seq)
        optScrAlign4.append([scrMatrix[len(seq)][len(center)], alignment])    
    sumScr, avgScr = calculateAvgScr(optScrAlign4)
    print optScrAlign4
    print '%-12s %d/%d = %3.2f' % (center, sumScr, len(optScrAlign4), avgScr)


    print "\nCenter: %s" % s0

    print "\nPairwise Sequence Alignments:\n(center sequence always on bottom)"
    MSA = [s0]
    for i in range(len(optScrAlign0)):
        MSA.append(optScrAlign0[i][1][1])
        print optScrAlign0[i][1][1]
        print optScrAlign0[i][1][0]
        print

    print "Merge:"
    for alignment in MSA:
        print alignment
    print
    


main()
