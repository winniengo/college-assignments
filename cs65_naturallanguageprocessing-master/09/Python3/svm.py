def extractFeatures(tweetData):

    features = []
    tweetIDs = tweetData["tweets"].keys()
    for tweetID in tweetIDs:
        features += tweetData["tweets"][tweetID]["postFeatures"]
        print(features)
    return features


def constructXY(tweetData):

    #Xfile = open('inputX.txt', 'w')
    #Yfile = open('inputY.txt', 'w')

    #print len(featuresList)
    X = [] # list of all features per tweets
    Y = [] # all class per tweets
    tweetIDs = tweetData["tweets"].keys()
    for tweetID in tweetIDs:
        answer = tweetData["tweets"][tweetID]["answers"][0]
        features = tweetData["tweets"][tweetID]["postFeatures"]
        #x = [0] * len(featuresList) # features per tweet
        #for feature in features:
        #    index = featuresList.index(feature)
        #    x[index] += 1

        X.append(features)
        #y = convert(answer)
        #Y.append(convert(answer))
        Y.append(answer)

        #xstring = ''
        #for i in range(len(x)):
        #    xstring += '%d ' % x[i]

        #xstring += '\n'
        #Xfile.write(xstring)
        #Yfile.write(y)

    #Xfile.close()
    #Yfile.close()
        
    return X, Y


def convert(className):
    if className == "negative":
        return '0'
    elif className == 'neutral':
        return '1'
    else: # 'positive'
        return '2'
    
