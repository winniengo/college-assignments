"""
- read in and parse input files
- call clustering methods implemented in clustering.py
- output results to standard output file

Written by: Eric Oh and Winnie Ngo
"""
#####################################################
import sys, os, math
from clustering import kmeans

"""
prints out information for how program should be used on the command line. This method is called if the user gives improper arguments
"""
def usage():
    print >> sys.stderr, "Usage: python run_kmeans.py <k> <geneFile> <geneAnnotations>"
    print >> sys.stderr, "k - number of clusters to use (integer)"
    print >> sys.stderr, "geneFile - name of the file containing the gene expression profiles"
    print >> sys.stderr, "geneAnnotations - (optional) name of file containing annotations about each instance"


"""
checks that file exists, exists program if it doesn't 
param: arg - commmand line argument
"""
def check_argv(arg):
    valid = False
    while not valid:
        if os.path.exists(arg):
            valid = True
        else:
            print >> sys.stderr, arg, "does not exist."
            sys.exit(1)

    return check_argv


"""
checks that k is a positive integer, exists program if it isn't
param: arg - command line argument
return: integer specifying number of clusters to use
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
param: filename containing a gene per line 
return: dictionary of dictionaries that contains distance matrix
"""
def construct_geneMatrix(profile_file, name_file):
    D = {}

    # read in given csv file containing gene instances
    pfile = open(profile_file, 'r')
    profiles = pfile.readlines()

    # if specified, read in given csv file containg gene annotations 
    if name_file != None: 
        nfile = open(name_file, 'r')
        names = nfile.readlines()
        nfile.close()
    else: # construct annotations by line number in profile file
        names = []
        for i in range(len(profiles)):
            names.append('x' + str(i))

    # construct (gene, features) dictionary
    for i in range(len(profiles)):
        D[names[i].strip()] = profiles[i].strip().split(',')

    pfile.close()
    return D
               
"""
param: original gene matrix
return: normalized gene matrix
"""
def normalize_matrix(matrix):
    featureLength = len(matrix[matrix.keys()[0]])

    for j in range(featureLength):
        sum = 0
        for gene in matrix.keys():
            sum += float(matrix[gene][j])**2
        length = math.sqrt(sum)
        for gene in matrix.keys():
            matrix[gene][j] = float(matrix[gene][j]) / length

    return matrix

####################################################
def main():

    # check command-line arguments
    if len(sys.argv) not in [3, 4]:
        print "Error, incorrect number of arguments"
        usage()
        sys.exit(1)
    
    
    k = check_k(sys.argv[1])
    check_argv(sys.argv[2])
    if len(sys.argv) == 4: # optional, file containing annotations
        check_argv(sys.argv[3])
        # initialize gene matrix using annotations
        geneMatrix = construct_geneMatrix(sys.argv[2], sys.argv[3])
    else: 
        # index instances by line number in original file
        geneMatrix = construct_geneMatrix(sys.argv[2], None)
    
    #normalize matrix
    geneMatrix = normalize_matrix(geneMatrix)

    # call kmeans clustering on input files
    sse, aic, silhouette = kmeans(geneMatrix, k)

    # print results
    print "K-means with k = %d\n" % k
    print "%-15s %.2f\n%-15s %.2f\n%-15s %.2f\n" % ('SSE:', sse, 'AIC:', aic,'Silhouette:', silhouette)



main()
