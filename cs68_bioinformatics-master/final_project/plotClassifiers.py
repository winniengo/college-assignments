from sklearn import cross_validation, svm
from sklearn.feature_selection import SelectPercentile, SelectKBest, f_classif
import matplotlib.pylab as pl

from numpy import * 
from classifiers import *


def convert_data(X, y):
    """ 
    Convert dataset into numpy.ndarray for plotting
    """   
    return array(X), array(y)

def plot_svms(X, y): 
    print("\nPlotting SVMs")

    X, y = convert_data(X, y)
    target_names = ['ALL 0', 'AML  1']
    
    # plot using two most weighted features     
    X = SelectKBest(f_classif, k=10).fit_transform(X, y)
    X = X[:, :2]

    # create SVMs and fit data
    linear_clf = svm.SVC(kernel = 'linear', C = 1.0).fit(X, y)
    rbf_clf = svm.SVC(kernel = 'rbf', C = 1.0).fit(X, y)
    linsvc_clf = svm.LinearSVC(C = 1).fit(X, y)

    # create a mesh to plot in
    h = 5 # step size in mesh
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = meshgrid(arange(x_min, x_max, h), arange(y_min, y_max, h))

    # titles for the plots
    titles = ["SVM with linear kernel", "SVM with rbf kernel", "Linear SVM"]

    clfs = [linear_clf, rbf_clf, linsvc_clf]
    
    for i, clf in enumerate(clfs):
        Z = clf.predict(c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        pl.contourf(xx, yy, Z, cmap=pl.cm.Paired)
        pl.axis('off')

        # Plot also the training points
        pl.scatter(X[:, 0], X[:, 1], c=y, cmap=pl.cm.Paired)

        pl.title(titles[i])
        pl.show()
   
if __name__ == "__main__":
    fname = "dataset/leukemiaPatients.csv"
    X, y = parse_data(fname)
    plot_svms(X, y)
