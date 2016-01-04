""" 
Implements Neighbor Joining - a distance based tree inference method           

Given: 
- a file containing the pairwise distances of all taxa in the tree
Do:
- infer an unrooted tree using the neighbor joining algorithm
- output the tree to standard output listing each edge in the tree
- generate a visual graph using GraphViz and save the result to an image file

Written by: Winnie Ngo and Eric Oh
"""
import sys, os
import pygraphviz as pgv 

"""
prints out information for how program should be used on the command
line.  This method is called if the user gives improper arguments
"""
def usage():
    print >> sys.stderr, "Usage: python MJTree.py <distances>"
    print >> sys.stderr, "distances - filename containing the distance matrix"

"""
checks that file exists, exits program if it doesn't
param: arg - command-line argument
"""
def check_argv(arg):
    if not os.path.exists(arg):
        print >> sys.stderr, arg, "does not exist."
        sys.exit(1)

"""
param: filename containing one line per pairwise distance in format A B d_AB
return: a dictionary of dictionaries that contains distance matrix

sample input: A B 7, A C 11, B C 6 
output D = {A: {B: 7, C: 11}, B: {C: 6, A:7}, C: {A: 11, B: 6}}
"""
def construct_D(filename):
    D = {}

    # read-in given distance matrix
    file = open(filename, 'r')
    for line in file.readlines():
        pairwise = line.strip().split() 
        
        A = pairwise[0]
        B = pairwise[1]
        d_AB = float(pairwise[2])

        if not D.has_key(A) and not D.has_key(B):
        	D[A] = {}
        	D[B] = {}
        	D[A][B] = d_AB
        	D[B][A] = d_AB
        elif not D.has_key(B):
        	D[B] = {}
        	D[A][B] = d_AB
        	D[B][A] = d_AB
        else:
        	D[A][B] = d_AB
        	D[B][A] = d_AB

    file.close()
    return D

"""
param: distance matrix, D
return: a dictionary where R[i] = r, the average distance of taxon i from all
other clusters 
"""
def construct_R(D):
	R = {}

	k = len(D.keys())
	for taxon in D.keys():
		distances = D[taxon].values() # all dik's
		r = 1.0/(k-2) * sum(distances) # average distance
		R[taxon] = r

	return R

"""
param: distance matrix, R
return: a dictionary of dictionaries that contains new distance matrix M
such that M[i][j] = D[i][j] - (R[i] + R[j])
"""
def construct_M(D, R):
    M = {}

    for A in D.keys():
        for B in D[A].keys():
        	if not M.has_key(A):
        		M[A] = {}
        	
        	M[A][B] = D[A][B] - (R[A] + R[B])

    return M

""" 
param: new distance matrix, M
return: taxon of clusters to be merged

when there's a tie breaker, returns first set of clusters found 
"""
def find_closest_clusters(M):
	d_ij = 0.0

	for A in M.keys():
		for B in M[A].keys():
			if M[A][B] < d_ij:
				d_ij = M[A][B]
				i = A
				j = B

	return i, j

"""
param: two clusters closest together in M, new node, distance matrix, R, and the tree
adds edges to the tree, prints out the edges and their distances
"""

def merge_closest_clusters(i,j,new_n,D,R,T):
        weight_ik = 0.5 * (D[i][j]+R[i]-R[j])
        if weight_ik < 1: #set minimum edge length to be 1
            weight_ik = 1

        weight_jk = 0.5 * (D[i][j]+R[j]-R[i])
        if weight_jk <1:  #set minimum edge length to be 1
            weight_jk = 1
        
        T.add_node(new_n)
        T.add_edge(i,new_n,label=weight_ik,len=weight_ik)
        T.add_edge(j,new_n,label=weight_jk,len=weight_jk)
        
        print_edges(i,j,new_n,weight_ik,weight_jk)

        return 

"""
param: two clusters, new created node, and two edge lengths
prints out the edges and their distances
"""
def print_edges(i,j,new_node,edge_ik,edge_jk):
        print i + " " + new_node + " " + str(edge_ik)
        print j + " " + new_node + " " + str(edge_jk)


"""
param:clusters to remove, new node, old distance matrix
updates the distance matrix
"""
def update_matrix(i,j,new_n,D):
        D[new_n] = {}  #insert new dictionary key for new node

        for seq in D.keys():   #calculate distances to new node
            if seq != i and seq != j and seq != new_n:
                d_kl = 0.5 * (D[i][seq]+D[j][seq]-D[i][j])
                D[new_n][seq] = d_kl
                D[seq][new_n] = d_kl
       
       #get rid of clusters that were merged
        D.pop(i,None)  
        D.pop(j,None)
        for seq in D.keys():
            if seq != new_n:
                D[seq].pop(i, None)
                D[seq].pop(j, None)

        return D

"""
param:last two clusters to merge
merges the last two remaining clusters and prints out the edge 
"""
def merge_last_two(node1,node2,D,T):
        last_weight =  D[node1][node2]
        if last_weight < 1:
            last_weight = 1
    
        T.add_edge(node1,node2,label=last_weight,len=last_weight)

        print_last_edge(node1,node2,last_weight)

        return

"""
param: last two clusters in edge, edge length
prints out the last remaining edge
"""
def print_last_edge(i,j,edge_len):
        print i + " " + j + " " + str(edge_len)

###############################################

def main():
    
    # check command-line arguments
    if len(sys.argv) != 2:
        print "Error, incorrect number of arguments"
        usage()
        sys.exit(1)

    check_argv(sys.argv[1])

    # initialization
    distance_matrix = construct_D(sys.argv[1])

    #create tree
    NJTree = pgv.AGraph()
    for seq in distance_matrix.keys():
        NJTree.add_node(seq)

    c = len(distance_matrix)
    while c > 2:
        
        #create R and M
        R = construct_R(distance_matrix)
        M = construct_M(distance_matrix,R)

        #merge closest clusters
        min_i,min_j = find_closest_clusters(M)
        new_node = min_i + "-" + min_j
        
        #update tree
        merge_closest_clusters(min_i,min_j,new_node,distance_matrix,R,NJTree)

        # update D, R, M
        distance_matrix = update_matrix(min_i,min_j,new_node,distance_matrix)

        #update c
        c = len(distance_matrix)
    
    clust1 = distance_matrix.keys()[0]
    clust2 = distance_matrix.keys()[1]
    merge_last_two(clust1,clust2,distance_matrix,NJTree)
   
    NJTree.draw("primate.png",prog="neato")


main()
