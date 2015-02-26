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

nodes = range(6)
communities = [community([0,1,2], 1),
               community([3,4,5], 1),
               community([0,5], 1),
               community([2,3], 1)]

G = AGM(nodes,communities)
nx.draw_networkx(G)


# cluster measures

class cluster:
    def __init__(self, member, cut = None, conductance = None):
        self.member = member
        self.cut = cut
        self.conductance = conductance

# cut score
def clusterCutScore(graph, nodes):
    cutScore = 0
    for edge in graph.edges():
        if len(set(edge).intersection(set(nodes))) == 1:
            cutScore += 1
    return cutScore

print clusterCutScore(G, [0,1,2])

clusterA = cluster([0,1,2], clusterCutScore(G, [0,1,2]))

# conductance

def clusterConductanceScore(graph, nodes):
    m = graph.number_of_edges()
    volA = sum([len(graph.neighbors(node)) for node in nodes])
    cut = clusterCutScore(graph, nodes)
    return float(cut)/min(volA, 2*m-volA)

print clusterConductanceScore(G, [0,1,2])

nodes = [0,1,2]

clusterA = cluster(nodes, clusterCutScore(G, nodes), clusterConductanceScore(G, nodes))

# laplacian


A = nx.to_numpy_matrix(G)

print A

D = np.matrix(np.zeros((G.number_of_nodes(),G.number_of_nodes())))
for node in G.degree():
    D[node, node] = G.degree()[node]

print D

L = D-A

print L

def laplacianOfGraph(graph):
    n = graph.number_of_nodes()
    A = nx.to_numpy_matrix(graph)
    D = np.matrix(np.zeros((n,n)))
    for node in graph.degree():
        D[node, node] = graph.degree()[node]
    L = D-A
    return L

def naiveSpectralClustering(graph):
    n = graph.number_of_nodes()
    L = laplacianOfGraph(graph)
    evals, evecs = np.linalg.eig(L)
    vals = evals.copy()
    vals.sort()
    index =evals.tolist().index(vals[1])
    values = np.array(evecs[:,index]).reshape(-1).tolist()
    cluster1 = [i for i in range(n) if values[i] <= 0]
    cluster2 = [i for i in range(n) if values[i] > 0]
    return cluster1, cluster2

print laplacianOfGraph(G)

c1, c2 = naiveSpectralClustering(G)
print c1
print c2
