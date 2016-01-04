"""
Implements n-fold cross validation given dataset and n to provice an 
accurate estimate of classifier error

Mike Superdock, Winnie Ngo
"""
from random import shuffle

def crossValidation(tweetData, n, randomize):
    """
    Given tweetData and n, perform n-fold cross validation. If randomize, 
    shuffle tweetIDs before splitting. Return tweetIDs in each training and
    test fold.
    """

    tweets = list(tweetData["tweets"].keys()) # retrieve all tweet IDs
    numTweets = len(tweets) # N
    indices = range(numTweets)

    # shuttle ids if specified
    if randomize:
        shuffle(indices)

    # rebuild list of tweet IDs, either shuffled or not
    tweetIDs = []
    for index in indices:
        tweetIDs.append(tweets[index])

    size = float(numTweets)/n # size of each fold

    # create training and test folds
    testFolds = []
    trainFolds = []

    for i in range(n): # for each fold, append appropriate ids
        left = int(i*size)
        right = int((i+1)*size)
        testFolds.append(tweetIDs[left:right])
        trainFolds.append(tweetIDs[0:left] + tweetIDs[right:])

    return trainFolds, testFolds
