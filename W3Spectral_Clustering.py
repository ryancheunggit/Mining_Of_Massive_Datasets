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
    def __init__(self, member, cut = None):
        self.member = member
        self.cut = cut

def clusterCutScore(graph, nodes):
    cutScore = 0
    for edge in graph.edges():
        if len(set(edge).intersection(set(nodes))) == 1:
            cutScore += 1
    return cutScore

print clusterCutScore(G, [0,1,2])

clusterA = cluster([0,1,2], clusterCutScore(G, [0,1,2]))
