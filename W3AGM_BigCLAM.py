# import libraries
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
# community class definition
class community:
    def __init__(self, member, prob):
        self.member = member
        self.prob = prob
# AGM
def AGM(nodes,communities):
    # import library
    from itertools import combinations
    from random import random

    # creating an empty graph
    G=nx.Graph()
    # add nodes to the graph
    G.add_nodes_from(nodes)

    # generate links within communities
    for c in communities:
        for nodePairs in combinations(c.member,2):
            if random() <= c.prob:
                G.add_edge(nodePairs[0], nodePairs[1])
    return G


# example graph with two communities
nodes = range(12)
communities = [community(range(8), 0.8),
               community(range(4,12), 0.8)]
G = AGM(nodes,communities)
nx.draw(G)

# example graph with three communities
nodes = range(24)
communities = [community(range(12), 0.8),
               community(range(6,17), 0.8),
               community(range(8,12)+range(17,24), 0.8)]
G = AGM(nodes,communities)
nx.draw(G)

# CMSMatrix to graph
def graphFromCMSMatrix(CMSMatrix):
    # creating an empty graph
    G=nx.Graph()
    # add nodes to the graph
    G.add_nodes_from(range(shape(F)[0]))

    from itertools import combinations
    from random import random
    # add edges to the graph

    for nodePairs in combinations(G.nodes(),2):
        u, v = nodePairs
        if random() <= 1- exp(-1*F[u,:]*F[v,:].transpose()):
            G.add_edge(u,v)
    return G

F = np.matrix('0 1.2 0 0.2; 0.5 0 0 0.8; 0 1.8 1 0')
G =  graphFromCMSMatrix(F)
nx.draw(G)


# estimate the matrix

def bigClam(graph, numCommunities, maxIter = 999, param = 0.01):
    # initialize a random matrix
    F = np.matrix(np.ones((len(graph.nodes()), numCommunities)))

    # start iterating
    for i in range(maxIter):
        # iterative over the rows of the matrix
        for row in range(shape(F)[0]):
            # calculating the gradient
            gradient = np.matrix(np.zeros((1,numCommunities)))
            u = F[row,:]
            for col in range(numCommunities):
                v = F[col,:]
                if col in G.neighbors(row):
                    gradient += v*float(exp(-1*u*v.transpose())/(1-exp(-1*u*v.transpose())))
                if col not in G.neighbors(row):
                    gradient -= v

            F[row,:] = F[row,:] + param*gradient
            for i in range(numCommunities):
                if F[row,i] < 0:
                    F[row,i] = 0


    return F

nodes = range(24)
communities = [community(range(12), 0.8),
               community(range(6,17), 0.8),
               community(range(8,12)+range(17,24), 0.8)]
G = AGM(nodes,communities)
nx.draw(G)
F = bigClam(G, 3)
F
