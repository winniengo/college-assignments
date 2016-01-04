from parseTweet import parse_tweets
from crossVal import crossValidation
from operator import itemgetter
import string, sys, os

# open-source tokenization
sys.path.append('/data/cs65/semeval-2015/arktweet/')
from arktweet import tokenize

"""
prints out information about program's command line agruments
"""
def usage():
    print ("Usage:") 
    print ("1. python3 classifier.py <trainingFile> <n>")
    print ("2. python3 classifier.py <trainingfile> <testFile>")

"""
checks that file exists, exits program if it doesn't
"""
def check_argv(arg):
    if os.path.exists(arg):
        return arg
    else: 
        print (arg, "does not exist")
        sys.exit(1)

"""
check that n is a positive integer, exits program if not
"""
def check_n(arg):
    try:
        n = int(arg)
    except ValueError:
        print ("n must be an integer")
        sys.exit(1)

    if n <= 0:
        print ("n must be a positive integer")
        sys.exit(1)

    return n

def handleCommandLineArgs():
    # retrieve and check command-line arguments
    #print sys.argv
    if len(sys.argv) != 3:
        print ("Error, incorrect number of arguments")
        usage()
        sys.exit(1)

    trainingFile = check_argv(sys.argv[1])
    
    if os.path.exists(sys.argv[2]):
        testFile = check_argv(sys.argv[2])
        crossVal = False
    else:
        n = check_n(sys.argv[2])
        crossVal = True

    # build Tweet dataset
    #trainingFile = '/data/cs65/semeval-2015/B/train/twitter-train-full-B.tsv'
    tweetData = parse_tweets(trainingFile, 'B')

    if crossVal: 
        # do n-fold cross validation on training set specified
        trainFolds, testFolds = crossValidation(tweetData, n, False)
        testData = None
    else:
        testData = parse_tweets(testFile, 'B')
        trainFolds = [list(tweetData["tweets"].keys())]
        testFolds = [list(testData["tweets"].keys())]

    return tweetData, testData, trainFolds, testFolds
        

