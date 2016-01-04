""" 
main program which runs classification algorithms to predict leukemia types

1. read in and parse input files
2. call k-nearest neighbors methods implemented in classifiers.py
3. use n-fold cross-validation to estimate generalization error

Written by Eric Oh + Winnie Ngo
"""
#####################################################
import sys, os, math
from classifiers import *

"""
prints out information for how program should be used on the command line. This method is called if the user gives improper arguments
"""
def usage():
    print >> sys.stderr, "Usage: python leukemiaPredictor.py <k> <trainingFile>"
    print >> sys.stderr, "k, the number of neighbors to consider"
    print >> sys.stderr, "trainingFile, file name of the training set"

"""
checks that file exists, exists program if it doesn't 
param: arg - commmand line argument
"""
def check_argv(arg):
    if os.path.exists(arg):
	return arg
    else:
	print >> sys.stderr, arg, "does not exist."
        sys.exit(1)

"""
checks that k is a positive integer, exits program if it isn't
param: arg - command line argument
"""
def check_k(arg):
    try:
        k = int(arg)
    except ValueError:
        print >> sys.stderr, "<k> must be an integer"
        sys.exit(1)

    if k < 0:
        print >> sys.stderr, "<k> number of clusters must be greather than 0"
        sys.exit(1)

    return k

"""
parse input file
"""
def parse_file(filename):
    X = [] # objects 
    pfile = open(filename, 'r')
    for line in pfile.readlines():
        line = line.strip().split(',')
	for i in range(len(line)):
	    line[i] = int(line[i])
        X.append(line)
    return X

####################################################
def main():
    # check command-line arguments
    if len(sys.argv) != 3:
        print "Error, incorrect number of arguments"
        usage()
        sys.exit(1)
    
    k = check_k(sys.argv[1])
    inputFile = check_argv(sys.argv[2])

    usr_input = raw_input("Display intermediate results? [y/n] ")
    if usr_input.lower() in ['yes', 'y']:
        display = True
    else:
        display = False


    print "\nClassification using k-nearest neighbors with k = %d and 5 folds"%k
    print

    X = parse_file(inputFile) 
    trainingFolds, testingFolds = generateFolds(5, X) 

    total_TP = 0.0
    total_FP = 0.0
    total_TN = 0.0
    total_FN = 0.0
    
    for i in range(len(trainingFolds)): # for each fold, run k-NN
        if display:
            print "\nFOLD %d" % i
            print 'Training on', trainingFolds[i]
            print 'Testing on', testingFolds[i]
        

        # call k-Nearest Neighbors on folds 
        TP, FP, TN, FN = kNN(trainingFolds[i], testingFolds[i], k, display)

        total_TP += TP
        total_FP += FP
        total_TN += TN
        total_FN += FN 

    # calculate and display measures of errors 
    N = len(X) # number of total predictions 
    accuracy = (total_TP + total_TN)/N
    sensitivity = total_TP/(total_TP + total_FN)
    specificity = total_TN/(total_TN + total_FP)

    print 'Results:\n'
    print "Accuracy: %.2f" % accuracy
    print 'Sensitivity: %.2f' % sensitivity
    print "Specificity: %.2f" % specificity
    print

main()


