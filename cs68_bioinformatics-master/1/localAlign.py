"""
localAlign.py - uses dynamic programming to compute a local alignment using a
linear gap penalty function for protein and DNA strands

Eric Oh and Winnie Ngo
"""
import sys, os
import numpy as py
import matplotlib.pyplot as plt
#############################################

"""
usage() - prints out information for how program should be used on the command
line.  Call this method if the user gives improper arguments
"""
def usage():
    print >> sys.stderr, "Usage: python localAlign.py <seq1> <seq2> <matrixFile> <g> <output>"
    print >> sys.stderr, "  seq1, seq2 - fasta files containing two sequences to align (1 per file)"
    print >> sys.stderr, "  matrixFile - file containing substitution matrix"
    print >> sys.stderr, "  g - integer specifying penalty for a gap"
    print >> sys.stderr, "  output - name of output file for raw alignment"


"""
checks that file exists, exits program if it doesn't
param: arg - command-line argument
"""
def check_argv(arg):
    valid = False
    while not valid:
        if os.path.exists(arg):
            valid = True 
        else:
            print >> sys.stderr, arg, "does not exist."
            sys.exit(1)


"""
checks that g is a negative integer, exits program if it isn't
param: arg - command-line argument
return: integer specifying gap penalty
"""
def check_g(arg):
    try:
        g = int(arg) 
    except ValueError:
        print >> sys.stderr, "<g> must be an integer"
        sys.exit(1)
    
    if g >= 0:
        print >> sys.stderr, "<g> gap penalty must be negative"
        sys.exit(1)
    
    return g


"""
reads in fasta files
param: filename - fasta file
return: a string containing sequence from file
"""
def load_sequence(filename):
    fasta = open(filename, 'r')
    fasta.readline() # do not care about the first line

    sequence = ''
    for line in fasta.readlines():
        sequence += line.strip() 

    fasta.close()
    return sequence


"""
reads in matrix file into a dictionary where the key is the character at the 
beginning of the line. The value it maps to is a dictionary containing all the 
(column, value) pairs for that row
param: filename - matrix file
return: a two-dimensional dictionary 
"""
def load_matrix(filename):
    matrix = open(filename, 'r')
    column_header =  matrix.readline().split()
    
    subMatrix = {}
    for line in matrix.readlines():
        row = line.split() 
        rowMatrix = {} # dict containing all (column,value) pairs for that row
        for i in range(1, len(row)):
            rowMatrix[column_header[i-1]] = int(row[i])
        subMatrix[row[0]] = rowMatrix # key = character at the beginning of row

    matrix.close()
    return subMatrix


"""
returns optimal score using 'highroad' for equally optimal alignments
param: up, match, left - three possible scores for F[i,j]
       x, y -  F[i, j] where x = i and y = j
return: opt_scr, opt_arw - highest integer score and corresponding pointer
"""
def max_score(up, match, left, x, y):
    opt_scr = up
    opt_arw = 'up'

    if opt_scr < match:
        opt_scr = match
        opt_arw = 'match'
    if opt_scr < left:
        opt_scr = left
        opt_arw = 'left'
    if opt_scr <= 0:
        opt_scr = 0
        opt_arw = ''

    return opt_scr, opt_arw


"""    
writes aligned sequences to file
param: filename - output file
        aSequences - list of possible aligned sequences from sequence 1 and 2
"""
def write_file(filename, aSequences):
    output = open(filename, 'w')
    for i in range(0, len(aSequences), 3):
        output.write(aSequences[i] + '\n')
        output.write(aSequences[i + 2] + '\n\n')
    output.close()


"""
returns optimal alignment score F(n, m) for the entire sequence
param: scoreMatrix - 2D matrix containing optimal score for all F(i,j)
       xRange, yRange - F(n, m) where n = xRange - 1, m = yRange - 1
return: optimal_score, optimal_index - max value and and list of corresponding 
indices (i,j)
"""
def find_optimal_score(scoreMatrix, xRange, yRange):
    allScores = []
    for row in scoreMatrix:
        allScores += row

    optimal_score = max(allScores) # find the largest score across the matrix
    
    optimal_index = []
    for y in range(1, yRange): # find all possible indices containing score
        for x in range(1, xRange):
            if optimal_score == scoreMatrix[y][x]:
                optimal_index.append([y, x]) # append to list
    
    return optimal_score, optimal_index


"""
constructs aligned sequence 1 and 2 using local alignment
param: x, y - (i, j) of the optimal score for the entire sequence 
        arrowMatrix - 2D matrix containing pointers to optimal score
        seq1, seq2 - the read-in sequences
return: aSeq1, aSeq2 - the read-in sequences after being aligned
        marker - string indicating a gap, perfect identity or substition
        startIndex - start index of aligned sequence as found in seq1 and seq2
        identity - no. of perfect alignments in aligned sequences
        gap - no. of total gaps in aligned sequences
        length - size of aligned sequence
"""
def construct_alignment(x, y, arrowMatrix, seq1, seq2):
    end = False
    aSeq1 = aSeq2 = marker = '' # construct aligned sequences + marker
    identity = gap = length = 0
    i = j = 1 # used to obtain the next amino acid to be added to the aligned
              # sequences from the read-in sequence 2 and 1 respectively 
    while not end:
        length += 1
        ptr = arrowMatrix[y][x]
        if ptr == "up": # insert gap in seq2, add next amino acid from seq1
            aSeq1 += seq1[-j]
            aSeq2 += '-'
            marker += ' '
            y -= 1
            j += 1
            gap += 1
        elif ptr == "left": # insert gap in seq1, add next amino acid from seq2
            aSeq2 += seq2[-i]
            aSeq1 += '-'
            marker += ' '
            x -= 1
            i += 1
            gap += 1
        elif ptr == 'match':
            aSeq1 += seq1[-j]
            aSeq2 += seq2[-i]
            if seq1[-j] == seq2[-i]: # check whether it's a perfect alignment
                identity += 1
                marker += '|'
            else:
                marker += '.' # or subsituation
            y -= 1
            x -= 1
            j += 1
            i += 1
        elif ptr == '': # score is 0, end of alignment
            end = True
    
    aSeq1 = ''.join(reversed(aSeq1))
    aSeq2 = ''.join(reversed(aSeq2))
    marker = ''.join(reversed(marker))
    startIndex = [y + 1, x + 1] # y, x indicate where in the read-in sequence 1
                                # and 2, respectively, that the alignment starts
    return aSeq1, aSeq2, marker, startIndex, identity, gap, length - 1


"""
standard output of the alignment: optimal score, 50 characters per line for 
each sequence, with the start and ending character indices, and markes to 
indicate type of alignment, number of identity and gaps
param: seq1, marker, seq2 - aligned sequences and corresponding char indicating
type of alignment
        startIndex - start index of aligned sequence as found in seq1 and seq2
"""
def print_alignment(seq1, marker, seq2, startIndex):
    rows = len(seq1)/50 # no. of 50 char rows
    start1 = startIndex[0]
    start2 = startIndex[1]

    print "Alignment:"
    for i in range(rows):
        # print a row of sequence 1
        printStr = "%5d " % start1
        for k in range(50):
            #print 50 * i + k
            printStr += seq1[50 * i + k]
            if seq1[50 * i + k] != '-':
                start1 += 1
        printStr += "%5d" % (start1 - 1)
        print printStr
        
        # print corresponding row of markers
        print "      %s" % marker[50 * i: 50 * i + 50]

        # print corresponding row of sequence 2
        printStr = "%5d " % start2
        for k in range(50):
            printStr += seq2[50 * i + k]
            if seq2[k] != '-':
                start2 += 1
        printStr += "%5d " % (start2 - 1)   
        print printStr, '\n'
  
    # print remainder, if any left
    if len(seq1) % 50: 
        printStr = "%5d " % start1
        for char in seq1[rows * 50:]:
            printStr += char
            if char != '-':
                start1 += 1
        printStr += "%5d" % (start1 - 1)
        print printStr

        print "      %s" % marker[rows * 50:]

        printStr = "%5d " % start2
        for char in seq2[rows * 50:]:
            printStr += char
            if char != '-':
                start2 += 1
        printStr += "%5d " % (start2 - 1)   
        print printStr, '\n'


"""
use matplotlib library to visualize the scoring matrix
param: scoreMatrix, 2D matrix containing optimal scores
"""
def plot_visual(scoreMatrix):
    data = py.array(scoreMatrix, py.int32)
    plt.imshow(data, interpolation = 'none')
    plt.xlabel('Sequence 2')
    plt.ylabel('Sequence 1')
    plt.title('Local Alignment Score F')
    plt.jet()
    plt.colorbar()

    plt.show()

########################################################

def main():
    if len(sys.argv) != 6:
        print "Error, incorrect number of arguments"
        usage()
        sys.exit(1)

    # error check command-line args
    check_argv(sys.argv[1])
    check_argv(sys.argv[2])
    check_argv(sys.argv[3])
    g = check_g(sys.argv[4])
    
    # load args 
    seq1 = load_sequence(sys.argv[1])
    seq2 = load_sequence(sys.argv[2])
    subMatrix = load_matrix(sys.argv[3])
    output_file = sys.argv[5]

    xRange = len(seq2) + 1
    yRange = len(seq1) + 1
    scoreMatrix = [[0 for x in range(xRange)] for y in range(yRange)]
    ptrMatrix = [['' for x in range(xRange)] for y in range(yRange)]
    
    # iterate using Smith-Waterman algorithem
    for y in range (1, yRange):
        for x in range(1, xRange):
            subScore = subMatrix[seq1[y - 1]][seq2[x - 1]] #substitution matrix
            up = scoreMatrix[y - 1][x] + g
            match = scoreMatrix[y - 1][x - 1] + subScore
            left = scoreMatrix[y][x - 1] + g
            scoreMatrix[y][x], ptrMatrix[y][x]  = max_score(up, match, left,x,y)

    # determine optimal score and resulting sequences
    algnSequences = [] 
    algnScore, algnIndices = find_optimal_score(scoreMatrix, xRange, yRange)
    print "\nAlignment Score: %d\n" % algnScore

    # for each possible alignment, construct aligned sequences and output
    for [y, x] in algnIndices:
        aSeq1, aSeq2, marker, startIndex, identity, gap, length = \
            construct_alignment(x, y, ptrMatrix, seq1[:y], seq2[:x])
        algnSequences.append(aSeq1)
        algnSequences.append(marker)
        algnSequences.append(aSeq2)

        # print each alignment to screen
        print_alignment(aSeq1, marker, aSeq2, startIndex)
        print "Identity %d/%d Gaps %d/%d\n" % (identity, length, gap, length)
        
    # output aligned sequences to file
    write_file(output_file, algnSequences)

    # display score matrix via heatmap
    plot_visual(scoreMatrix)    
    



main()
