from bs4 import BeautifulSoup as bs
import os

def getData(inFile):
    """
    Input: inFile is the path of the file (training or testing)

    Return: a dictionary mapping "lexelts" to dictionaries mapping
    "instances" to words and heads.

    Example usage for return data:

    A list of the polysemous words to be disambiguated
    >>> data.keys()
    [u'begin.v', u'rule.v', u'play.v', u'argument.n', ...]

    A list of the IDs of the instances
    >>> data['play.v'].keys()
    [u'play.v.bnc.00018254', u'play.v.bnc.00026527', ...]

    A dictionary representing the instance
    >>> data['play.v']['play.v.bnc.00018254'].keys()
    ['answers', 'heads', 'words']

    A list of the words in the instance    
    >>> data['play.v']['play.v.bnc.00018254']['words']
    [u'Our', u'opener', u'this', u'year', u'has', u'been', u'a', ...]

    A list of positions of the headwords in the instance
    >>> data['play.v']['play.v.bnc.00018254']['heads']
    [58]

    Extract the head word
    >>> data['play.v']['play.v.bnc.00018254']['words'][58]
    u'plays'

    Look at the text in the instance
    >>> ' '.join(data['play.v']['play.v.bnc.00018254']['words'])
    u"Our opener this year has been a runaway success in ..."

    Look at how this instance is sense tagged
    >>> data['rule.v']['rule.v.bnc.00080928']['answers']
    [u'3597910']
    """
    corpus = open(inFile).read()
    corpus = '<doc>%s</doc>' % (corpus)
    soup = bs(corpus,"xml")
    
    data = {}

    instances = []
    lexelts = soup.findAll('lexelt')

    for lexelt in lexelts:
        target = lexelt['item']
        data[target] = {}
        instances = lexelt.findAll('instance')

        for instance in instances:
            answers = [x['senseid'] for x in instance.findAll('answer')]
            
            instanceID = instance['id']
            data[target][instanceID] = {}
            context = instance.context
            contents = context.contents
            words = []
            heads = []
            for c in contents:
                try: #see if it's a headword
                    headword = c.contents[0].string.strip()
                    heads.append(len(words))
                    words.append(headword)
                except AttributeError:  #nope, just a string
                    text = c.string.strip()
                    words.extend(text.split())

            data[target][instanceID]['words'] = words
            data[target][instanceID]['heads'] = heads
            data[target][instanceID]['answers'] = answers

    keyFile = inFile + ".key"
    if os.path.exists(keyFile):
        keyLines = open(keyFile).readlines()
        for line in keyLines:
            fields = line.split()
            target = fields[0]
            instanceID = fields[1]
            answers = fields[2:]
            data[target][instanceID]['answers'] = answers

    return data

if __name__=='__main__':
    trainingFile = '/data/cs65/senseval3/train/EnglishLS.train'
    trainData = getData(trainingFile)
