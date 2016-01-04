""" 
1. k-nearest neighbors implementation
2. Euclidean distance function
3. evaluation metric functions (eg. sensitivity)
4. cross-validation helper method: create n-folds 

Written by Winnie Ngo + Eric Oh
"""
#######################################################
from math import *
from random import shuffle
from operator import itemgetter


"""
Euclidean distance function
"""
def euclideanDistance(x, y):
    dist = 0
    for i in range(len(x)-1):
        dist += pow(x[i] - y[i], 2)

    return sqrt(dist)

"""
Weighted distance function
"""
def weightedDistance(distance):
    return 1/(1 + distance)

"""
k-nearest neighbors algorithms

the output is a 'class membership'. an object is classified by a majority vote
of its neighbors with the object being assigned to the class most common
among its k nearest neighbors measured by the Euclidean distance function

whenever we have a new point to classify, we find its K nearest neighbors 
from the training data
"""
def kNN(trainingSet, testingSet, k, display):
    TP = FP = TN = FN = 0
    for x_i in testingSet:
	y_i = x_i[-1]

        # build distance matrix for all x_j in training set 
	distance_matrix = []
	for x_j in trainingSet:
	    if x_j != x_i:
	        distance_matrix.append((euclideanDistance(x_j, x_i), x_j))
               
        # sort distances, retrieve k nearest neighbors 
	sorted_distance_matrix = sorted(distance_matrix, key=itemgetter(0))

        
	if display:
	    print 'Distances:'
	    for x_j in sorted_distance_matrix:
		print '\t%.3f' % x_j[0]

        P = {1: 0, -1: 0} 
        for dist_xij, x_j in sorted_distance_matrix[:k]: # k nearest neighbors
       	    y_j = x_j[-1]
       	    P[y_j] += weightedDistance(dist_xij)

       	if display:
       	    print "Weighted Votes:"
   	    for c in P.keys():
   		print '\tClass %s = %f' % (c, P[c])

   	# get max p_i
   	sorted_P = sorted(P.items(), key=itemgetter(1))	
   	p_i = sorted_P[-1]
        
        if display:
            print 'Prediction: Class %s\t\t\tWeight: %f' % (p_i[0], p_i[1])

        # accumulate errors 
   	if p_i[0] == 1 and y_i == 1:
   	    TP += 1
   	elif p_i[0] == 1 and y_i == -1:
   	    FP += 1
   	elif p_i[0] == -1 and y_i == -1:
   	    TN += 1
   	elif p_i[0] == -1 and y_i == 1:
   	    FN += 1
   	
    return TP, FP, TN, FN

"""
generates n-folds from dataset for cross-validation 
"""
def generateFolds(n, dataset):
	N = len(dataset) 
	indices = range(N)
	shuffle(indices) 

	# rebuild list of objects shuffled
	shuffledData = []
	for i in indices:
	    shuffledData.append(dataset[i])

	size = float(N)/n # size of each fold

	# create folds
	testFolds = []
	trainFolds = []

	for i in range(n): # for each fold i
	    left = int(i*size) 
	    right = int((i+1)*size)
	    testFolds.append(shuffledData[left:right])
	    trainFolds.append(shuffledData[:left] + shuffledData[right:])

	return trainFolds, testFolds
