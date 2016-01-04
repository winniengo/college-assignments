"""
CS65: Lab 7 - Mike Superdock, Winnie Ngo

Exploring the training data:

1. There are 8036 training examples.

2. Using the sentiment labels as given, we found 2437 instances labeled 
'objective', 2994 labeled 'positive', 2835 labeled 'neutral' and 1170 
labeled 'negative. That is 30%, 37%, 35% and 17%, respectively. 

After conflating neutral of objective into neutral, we found 2994 instances
labeled positive, 3872 labeled neutral and 1170 labeled negative. That is
37%, 48%, and 15%, respectively.

3. The random baseline is 29.36%.

4. The MFS is 'positive' and using the baseline we accurately label 37.26% of 
the training data correctly. After labels are conflated, the MFS is 'neutral'
and using it we accuraltely label 48.18%.

"""
from parseTweet import parse_tweets
import operator

"""
outputs the number of training examples
"""
def question1(tweetData):

    print len(tweetData["tweets"].keys())

"""
given dataset, outputs how often each sentiment label appears in raw numbers
and percentages

params: conflate - True, conflates neutral or objective labels into a neutral
return: dictionary of sentiment and the number of times it appears in dataset
"""
def question2(tweetData, conflate):

    total = float(len(tweetData['tweets'].keys()))

    tweets = tweetData["tweets"].keys()
    sentDictionary = {}
    for tweetID in tweets:
        sentiments = tweetData["tweets"][tweetID]["answers"]
        if conflate:
            if 'objective' in sentiments or 'neutral' in sentiments:
                sentiments = ['neutral']
        for sentiment in sentiments:
            if sentDictionary.get(sentiment) == None:
                sentDictionary[sentiment] = 1
            else:
                sentDictionary[sentiment] += 1

    for sentiment, count in sentDictionary.items(): # raw numbers and %'s
        print "%s %d %.2f" % (sentiment, count, count/total)

    return sentDictionary

def question3(tweetData):

    tweets = tweetData["tweets"].keys()
    sentiments = []
    s_sentiments = 0 #single sentiments
    d_sentiments = 0 #double sentiments
    for tweetID in tweets:
        answers = tweetData["tweets"][tweetID]["answers"]
        sentiments += answers # to obtain n
        if len(answers) == 1:
            s_sentiments += 1
        else: 
            d_sentiments += 1
            
    n = float(len(set(sentiments)))
    print ((s_sentiments * 1/n) + (d_sentiments * 2/n)) / len(tweets) * 100

def question4(sentDictionary, testData, conflate):

    sortSents = sorted(sentDictionary.items(), key=operator.itemgetter(1))
    MFS = sortSents[-1][0]
    
    correctCount = 0
    tweets = tweetData["tweets"].keys()
    for tweetID in tweets:
        sentiments = tweetData["tweets"][tweetID]["answers"]
        if conflate:
            if 'objective' in sentiments or 'neutral' in sentiments:
                sentiments = ['neutral']
        if MFS in sentiments:
            correctCount += 1

    print float(correctCount)/len(tweets) * 100


if __name__=='__main__':
    filename = '/data/cs65/semeval-2015/B/train/twitter-train-full-B.tsv'
    tweetData = parse_tweets(filename, 'B')

    print "\nQuestion 1:\n"
    question1(tweetData)
    print "\nQuestion 2:\n"
    sentDictionary1 = question2(tweetData, False)
    print "\nQuestion 2 (with conflation to neutral):\n"
    sentDictionary2 = question2(tweetData, True)
    print "\nQuestion 3:\n"
    question3(tweetData)
    print "\nQuestion 4:\n"
    question4(sentDictionary1, tweetData, False)
    question4(sentDictionary2, tweetData, True)
    
