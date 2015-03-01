import time
import networkx as nx
import numpy as np
import scipy
from sklearn.preprocessing import normalize

# skipping the description in file
def skip_lines(input_file, n):
    for i in range(n):
        input_file.next()

def parseNetwork(filename):
    # create a empty directed graph in networkx
    G = nx.DiGraph()
    # parse the network
    with open(filename, 'r') as f:
        skip_lines(f, 4)
        for row in f:
            content = row.strip().split('\t')
            G.add_edge(content[0], content[1])

    index = G.nodes().index('99')
    # conver to scipy sparse matrix
    Gsparse = nx.to_scipy_sparse_matrix(G,dtype = u'double', format = u'coo')
    Gsparse = Gsparse.transpose()
    # normalize the matrix
    Gsparse = normalize(Gsparse, norm='l1', axis=0)
    return G, Gsparse

def pageRank(M, b, maxIter = 200, err = 10**-10):
    n = M.shape[0]
    r = normalize(np.ones((n,1),dtype = u'double'), norm='l1', axis = 0)
    for i in range(maxIter):
        rp = (1-b)*M*r
        rp += (1-sum(rp))/n
        if np.linalg.norm(rp - r) <= err:
            print "took {} iteration to converge".format(i+1)
            r = rp
            break
        else:
            r = rp
    return r


def main():
    filename = 'web-Google.txt'
    start = time.time()
    G, M = parseNetwork(filename)
    end = time.time()
    print 'generating the matrix M takes {} seconds\n'.format(end - start)

    start = time.time()
    r = pageRank(M, 0.2)
    end = time.time()
    print 'calculating pagerank takes {} seconds\n'.format(end - start)
    print 'the pagerank value for website named 99 is {}'.format(r[G.nodes().index('99')])

    start = time.time()
    nr = nx.pagerank_scipy(G, 0.8, tol = 10**-10)
    end = time.time()
    print 'calculating pagerank using networkx implementation takes {} seconds \n'.format(end - start)
    print 'the pagerank value for website named 99 is {}'.format(nr['99'])

if __name__=="__main__":
    main()
