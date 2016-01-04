"""
k-means clustering algorithm implementation

contains functions for:
- the central k-means algorithm
- Manhattan distance functions
- evaluation metrics

Written by: Winnie Ngo and Eric Oh
"""

import random

def manhattanDistance(f1, f2):
    dist = 0
    for i in range(len(f1)):
        dist += abs(f1[i] - f2[i])

    return dist


def clusterInstances(X, M):
    clusters = {} # dictionary of list of instances closest to cluster c_i
    for cluster in M.keys():
        clusters[cluster] = []

    X = X.items()
    M = M.items()
    for xname, xfeatures in X:
        d_min = 100000
        m_min = ""
        for mname, mfeatures in M:
            d_xm = manhattanDistance(xfeatures, mfeatures)
            if d_xm < d_min:
                d_min = d_xm
                m_min = mname
        clusters[m_min].append((xname, xfeatures))
    
    return clusters

"""
if a cluster ever has 0 members, randomly assign the centroid to a random 
instance in the data set. Don't assign the same initial location to two
different cluster centers
"""
def calculateCenters(clusters, X):
    M_updated = {}

    clusters = clusters.items()

    for name, instances in clusters:
        if len(instances) == 0: # cluster has 0 members
            new_M = random.choice(X.values())  

        else: 
            new_M = []
            n = len(instances)  # number of instances in cluster
            m = len(instances[0][1]) # number of features/instance
            for i in range(m):
                total = 0.0
                for instance in instances:
                    total += instance[1][i]
                avg = total/n
                new_M.append(avg)
            
        M_updated[name] = new_M

    return M_updated

"""
checks for convergence
"""
def converged(M, M_updated):
    for mean in M:
        if mean not in M_updated:
            return False

    return True 

"""
calculate sum of squared errors (SSE)
"""
def calculateSSE(clusters, M):
    sse = 0
    for mname, mfeatures in M.items():
        for cname, cfeatures in clusters[mname]:
            squared_error = manhattanDistance(cfeatures, mfeatures)**2
            sse += squared_error

    return sse

"""
calculate AIC measure
"""
def calculateAIC(sse, k, M):
    return sse + 2*k*M

"""
calculate Silhouette Index of cluster result
"""
def calculateSilhouette(clusters, M, k):
    S = 0
    s_i = {} 

    # calculate s_i for all x_i
    for cname, cinstances in clusters.items():
        for xname, xfeatures in cinstances:
            # calculate the distance from x_i to all cluster means 
            # and select the smallest
            mu_min = 1000000
            mu_name = ''
   
            for key in M.keys():
                if key != cname: # ignore mean of cluster which x_i belongs to
                    mu = manhattanDistance(M[key], xfeatures)
                    if mu < mu_min:
                        mu_min = mu
                        mu_name = key

            # calculate the avg dist to all data members in the closest cluster
            bmembers = clusters[mu_name]

            total = 0.0
            for xi, xpoint in bmembers:
                total += manhattanDistance(xpoint, xfeatures)
            b_i = total/len(bmembers)
            
            # calculate the avg dist to all members of the same cluster
            amembers = clusters[cname]

            total = 0.0
            for xi, xpoint in amembers:
                if xi != xname: # all members except x_i
                    total += manhattanDistance(xpoint, xfeatures)

            if len(amembers) == 1: # clusters of 1 member 
                a_i = total
            else: # calculate avg dis 
                a_i = total/(len(amembers) - 1)
            
            # calculate silhouette index for x_i
            s_i[xname] = (b_i - a_i)/max(a_i, b_i)

    # calculate Silhouette Index
    S = 0.0
    for cname, cinstances in clusters.items():
        sum_ci = 0.0
        for xi, xfeatures in cinstances:
            sum_ci += s_i[xi]
        S += sum_ci/len(cinstances)

    S = S/k
    return S
        



"""
write the number of clusters on the first line and after have k sections in
kmeans.out
"""
def writeFile(clusters, M):
    output = open('kmeans.out', 'w')
    for index, mean in M.items():
        output.write("%s: (" % index)
        for i in range(len(mean)-1):
            output.write(' %.2f,' % mean[i])
        output.write(" %.2f )\n" % mean[len(mean)-1])
        for instances in clusters[index]:
            output.write('%s\n' % instances[0])
        output.write('\n')
    output.close()


"""
param:  X, dictionary containg dataset X = {x0, x1, ..., xn}
           where key = name and value = list of features
        K, parameter specifying how many clusters to create
return: clusters, a set of K cluster centroids
        M, means for each cluster that minimizes error
"""
def kmeans(X, K):
    # select k random centers by picking k random instances to be M0 ,..., Mk
    means0 = random.sample(X.values(), K)           
    means1 = random.sample(X.values(), K) 
    while converged(means0, means1): # make sure they don't converge initially
        means1 = random.sample(X.values(), K)

    M = {} # build M dictionarys
    M_updated = {}
    for i in range(K):
        idx = 'Cluster ' + str(i)
        M[idx] = means0[i]
        M_updated[idx] = means1[i]

    # Lloyd's algorithm 
    iterations = 0 # run k-means until convergence or 50 iterations
    while not converged(M.values(), M_updated.values()) or iterations == 50:
        M = M_updated
        # assign all points in X to clusters
        clusters = clusterInstances(X, M)
        # reevaluate centers
        M_updated = calculateCenters(clusters, X)
        # increment iterations 
        iterations += 1

    writeFile(clusters, M)

    # calculate metrics for evaluation
    sse = calculateSSE(clusters, M) 
    aic = calculateAIC(sse, K, len(M.values()[0]))
    silhouette = calculateSilhouette(clusters, M, K)

    return sse, aic, silhouette




