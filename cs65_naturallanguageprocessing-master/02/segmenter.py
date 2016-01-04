#!/usr/bin/python
"""
segmenter.py
A simple sentence segmenter which takes a text file containing one word (or 
punctuation) per line as a command-line argument. Any time program comes 
across an end-of-sentence marker (period, colon, semi-colon, exclamation point.
or question mark) it decides if that really ends the sentence of not. Outputs
a file myguesses.txt where each line contains the line number of an end of 
sentence

Written By: Mike Superdock and Winnie Ngo
"""
import sys, re, os

def usage():
    print >> sys.stderr, 'Usage: ./segmenter.py <category>\n' 

"""
confirms that commandline arguments match usage, exits if it doesn't
"""
def check_args():
    if len(sys.argv) == 2:
        path = "/data/cs65/lab02/" + sys.argv[1] + ".txt"
        if os.path.exists(path):
            return path
        else:
            print(' ')
            print >> sys.stderr, "file \"", sys.argv[1], "\" does not exist.\n"
    
    usage()
    sys.exit(1)


"""
returns a list of all the words/punctution in a given .txt file
params: fname, file path
returns: list of lines
"""
def read_text_lines(fname):
    infile = open(fname, 'r')
    lines = infile.read().splitlines()
    infile.close()

    return lines
"""
outputs results to file
param: lst, list of end of sentence indices
        fname, name of output file
"""
def write_results_to_file(lst, fname):
    f = open(fname, 'w')
    for item in lst:
        f.write(str(item))
        f.write('\n')
    f.close

"""
converts list of words and punctuation to list of trigrams were each trigram is
constructed by concatenating three consecuting words/punctuation separated by
spaces
params: lst, list of words/punctutaion from file
returns: list of trigrams
"""
def list_to_trigrams_list(lst):
    trigrams = []
    for index in range(len(lst)-2):
        trigram = lst[index] + lst[index+1]  + lst[index+2]
        trigrams.append(trigram)
    return trigrams

"""
constructs a list of indices where '.' follows 3 patterns we decided were most
common for indicating the end of sentence. Removes from the list where 
abbreviations such as 'Mr.', 'Dr.', 'Sen.' occur.
params: trigramsList, list of trigrams
returns: list of indices where a period marks the end of sentence
"""
def find_eos_periods(trigramsList):
    perIndices = []
    patterns0 = [r"['`]\.[A-Z]", r"[a-z]\.[A-Z]", r".\.`"]
    for pattern in patterns0:
        rgx0 = re.compile(pattern)
        indices = [idx + 1 for idx in range(len(trigramsList)) \
                if rgx0.search(trigramsList[idx])]
        perIndices += indices
        
    patterns = ['Mr', 'Mrs', 'Ms', 'St', 'Dr', 'Gen', 'Rep', 'Sen']
    notIndices = []
    for pattern in patterns:
        rgx = re.compile(pattern+'\..')
        indices = [idx + 1 for idx in range(len(trigramsList)) \
                if rgx.search(trigramsList[idx])]
        notIndices += indices
    
    return [item for item in perIndices if item not in notIndices]

def main():
    print "\nCS 65: Lab 2 Q1"
    textFile = check_args()
    textList = read_text_lines(textFile)
    trigramsList = list_to_trigrams_list(textList)

    rgxSemi = re.compile(';')
    rgxExc = re.compile('!')
    rgxQMark = re.compile('\?')
    ExcIndices = [idx for idx in range(len(textList)) \
            if rgxExc.search(textList[idx])]
    QMarkIndices = [idx for idx in range(len(textList)) \
            if rgxQMark.search(textList[idx])]
    SemiIndices = [idx for idx in range(len(textList)) \
            if rgxSemi.search(textList[idx])]

    # special cases
    PerIndices = find_eos_periods(trigramsList)
    ColIndices = [] # much more frequently than not, colons do not indicate an
                    # end of sentence thus it is better overall to ignore it as
                    # an end of sentence marker

    results = ColIndices + ExcIndices + QMarkIndices + PerIndices + SemiIndices
    results.sort()

    write_results_to_file(results, "myguesses.txt")

main()

