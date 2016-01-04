"""
Allows classify.py to be run in each of the following two ways:
a. python3 classify.py training_file n
    n-fold cross validation is performed on the training_file and the scorer is
    called at the end showing the performance under cross_validation

b. python3 clasify.py training_file test_file
    Output consists of two columns separated by a space: <instance id> <label>

Mike Superdock, Winnie Ngo
"""

from parsetweets import parse_tweets
from crossval import crossValidation
import sys, os

def usage():
    """
    Display usage information about program's command line agruments
    """
    
    print ("Usage:") 
    print ("1. python3 classifier.py <trainingFile> <n>")
    print ("2. python3 classifier.py <trainingfile> <testFile>")


def check_argv(arg):
    """
    Check that file exists, exits program if it doesn't
    """
    
    if os.path.exists(arg):
        return arg
    else: 
        print (arg, "does not exist")
        sys.exit(1)


def check_n(arg):
    """
    Check that n is a positive integer, exits program if not
    """
    
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
    """ 
    User must run classify.py in one of the two following ways:
        a. python3 classify.py training_file n
        b. python3 classify.py training_file test_file
    Return resulting training set, test set, and training and test folds
    """
    
    # retrieve and check command-line arguments
    if len(sys.argv) != 3:
        print ("Error, incorrect number of arguments")
        usage()
        sys.exit(1)

    # input training data file
    trainingFile = check_argv(sys.argv[1])
    
    # check which way to run the code
    if os.path.exists(sys.argv[2]):
        testFile = check_argv(sys.argv[2])
        crossVal = False
    else:
        n = check_n(sys.argv[2])
        crossVal = True

    # build training dataset
    tweetData = parse_tweets(trainingFile, 'B')

    # implement n-fold cross validation
    if crossVal == True: 
        testData = None
        trainFolds, testFolds = crossValidation(tweetData, n, False)
    else: # ir vyukd test dataset
        testData = parse_tweets(testFile, 'B')
        trainFolds = [list(tweetData["tweets"].keys())]
        testFolds = [list(testData["tweets"].keys())]

    return crossVal, tweetData, testData, trainFolds, testFolds
