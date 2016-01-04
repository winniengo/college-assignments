from random import shuffle
from parseTweet import parse_tweets

def crossValidation(tweetData, n, randomize):

  tweets = tweetData["tweets"].keys() # retrieve all tweet IDs
  numTweets = len(tweets) # N
  indices = range(numTweets)
  if randomize:
    shuffle(indices)
  # rebuild list of tweet IDs, either shuffled or not
  tweetIDs = []
  for index in indices:
    tweetIDs.append(tweets[index])

  size = float(numTweets)/n # size of each fold

  # create folds
  testFolds = []
  trainFolds = []

  for i in range(n):
    left = int(i*size)
    right = int((i+1)*size)
    testFolds.append(tweetIDs[left:right])
    trainFolds.append(tweetIDs[0:left] + tweetIDs[right:])

  return trainFolds, testFolds
