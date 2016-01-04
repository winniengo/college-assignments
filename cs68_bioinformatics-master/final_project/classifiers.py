from sklearn import cross_validation
from sklearn import svm
from sklearn import tree
from sklearn import metrics
from sklearn import naive_bayes
from sklearn import ensemble
from sklearn import grid_search

import numpy as np
from plotClassifiers import *

def parse_data(filename):
    X = []
    y = []
    dfile = open(filename, 'r')
    for line in dfile.readlines():
        line = line.strip().split(',')
        for i in range(len(line)):
            line[i] = int(line[i])  
        X.append(line[:-1])
        
        if line[:-1] == -1:
            line[:-1] = 0
        y.append(line[-1])
    return X, y

def cross_val(skf, X, y):
    X_train = []
    X_test = []
    y_train = []
    y_test = []
    
    for train_index, test_index in skf:
        #print(len(train_index), len(test_index))
        train_X = []
        train_y = []
        test_X = []
        test_y = []
        
        for i in train_index:
            train_X.append(X[i])
            train_y.append(y[i])
        for j in test_index: 
            test_X.append(X[j])
            test_y.append(y[j])

        X_train.append(train_X)
        y_train.append(train_y)
        X_test.append(test_X)
        y_test.append(test_y)

    return X_train, X_test, y_train, y_test

def user_input():
    n = input("Perform n-folds cross validation, n: ")
    try:
        n = int(n)
    except ValueError:
        n  = 7

    display = input("Display confusion matrix (y/n): ").lower()
    if display == 'y':
        display = True
    else:
        display = False

    plot = input("Plot SVMs (y/n): ").lower()
    if plot == 'y':
        plot = True
    else:
        plot = False

    print("\n")

    return n, display, plot

def train_parameters(X, y):
    X_train, X_test, y_train, y_test = cross_validation.train_test_split( \
            X, y, test_size = 0.25, random_state = 0)

    gamma_range = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 0]
    C_range = [1, 10, 100, 1000, 10000]
    parameters = [{'kernel':['rbf'], 'gamma':gamma_range, 'C':C_range}, \
                  {'kernel':['linear'], 'C':C_range}]
    
    svr = svm.SVC()

    clf = grid_search.GridSearchCV(svr, parameters, cv=7)
    clf.fit(X_train, y_train)

    print("Best parameters:")
    print(clf.best_estimator_)

    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r" % \
                (mean_score, scores.std() / 2, params))

def main():
    # n, display, plot = user_input()
    n = 7
    display = plot = False

    fname = "dataset/leukemiaPatients.csv"
    X, y = parse_data(fname)
    
    # create stratified k folds 
    nfolds = n
    skf = cross_validation.StratifiedKFold(y, nfolds)
    X_train, X_test, y_train, y_test = cross_val(skf, X, y)

    # train parameters using grid search
    # train_parameters(X, y)
    
    # create classifiers 
    linear_clf = svm.SVC(kernel = 'linear', C = 1) # linear kernel SVM
    rbf_clf = svm.SVC(kernel = 'rbf', C = 1, gamma = 1e-05) # rbf kernel SVM
    
    linsvc_clf = svm.LinearSVC(C = 1) # linear SVM
    
    decisionTree_clf = tree.DecisionTreeClassifier() # decision tree
    randomForest_clf = ensemble.RandomForestClassifier(n_estimators=10, \
            max_depth=None, min_samples_split=1, random_state=0)
    extraTrees_clf = ensemble.ExtraTreesClassifier(n_estimators=10, \
            max_depth=None, min_samples_split=1, random_state=0)
    
    gnb_clf = naive_bayes.GaussianNB()
    
    # group for experiment
    clfs = [linear_clf, rbf_clf, linsvc_clf, \
            decisionTree_clf, randomForest_clf, extraTrees_clf, \
            gnb_clf]

    titles = ["SVM linear", "SVM rbf", "Linear SVM", "Decision Tree", \
            "Random Forest", "Extra Trees", "Gaussian Naive Bayes"]

    for i, clf in enumerate(clfs): 
        print(titles[i])

        if display:
            for k in range(kfolds):
                # train a SVM classification model
                clf.fit(X_train[k], y_train[k])
        
                # evaludate model on test set
                y_pred = clf.predict(X_test[k])

                # analyze results 
                score = clf.score(X_test[k], y_test[k])
                report = metrics.classification_report(y_test[k], y_pred, \
                    target_names= target_names)
            
                print("Score: ", score)
                print("Confusion Matrix:")
                print("%d %d\n%d %d" % (results[0][0], results[0][1], \
                                    results[1][0], results[1][1]))
        
        scores = cross_validation.cross_val_score(clf, X, y, cv=n)
        print("%0.2f (+/- %0.2f)\n" % (scores.mean() ,scores.std() * 2))
      
    if plot: 
        plot_svms(X, y)

if __name__ == "__main__":
    main()
