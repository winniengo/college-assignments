from __future__ import print_function
import sys
sys.path.append('/data/cs65/semeval-2015/jazzy')
from jazzy import spell

"""
takes tweet dictionary, spell checks 'words' and writes results into oringial
.tsv file format
"""
def clean_tweets(tweetDictionary, filename):
   cleanFile = open(filename, 'w')
   tweetIDs = sorted(tweetDictionary['tweets'].keys())  #python3 compatible
   size = 20
   length = len(tweetIDs)
   for left in range(0,length,size):
      sys.stderr.write('Spellcheck: %d/%d\r' % (left, length))
      twids = []
      senses = []
      tweets = []

      right = left+size
      if right >= len(tweetIDs):
         piece = tweetIDs[left:]
      else:
         piece = tweetIDs[left:right]

      for tweetID in piece:
         twids.append(tweetID.split('_'))
         senses.append(''.join(tweetDictionary['tweets'][tweetID]['answers']))
         tweets.append(' '.join(tweetDictionary['tweets'][tweetID]['words']))

      cleanTweets = spell(tweets)
      for j in range(len(tweets)):
         line = '%s\t%s\t%s\t%s\n' % (twids[j][0], twids[j][1], senses[j], 
                                      cleanTweets[j])
         cleanFile.write(line.encode('utf-8'))
         cleanFile.flush()

   sys.stderr.write('Spellcheck complete           \n')
   cleanFile.close()


if __name__=='__main__':
   clean_tweet(tweetData, filename)
