# import libraries
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

# question 1
G=nx.Graph()
G.add_nodes_from(['A','B','C','D','E','F','G','H'])
G.add_edge('A','C')
G.add_edge('A','F')
G.add_edge('F','C')
G.add_edge('D','C')
G.add_edge('F','G')
G.add_edge('D','G')
G.add_edge('D','E')
G.add_edge('G','H')
G.add_edge('E','H')
G.add_edge('E','B')
G.add_edge('H','B')

A = nx.to_numpy_matrix(G)

print sum(A)
print size(A)-sum(A==0)

D = np.matrix(np.zeros((G.number_of_nodes(),G.number_of_nodes())))
i = 0
for node in G.degree():
    D[i, i] = G.degree()[node]
    i +=1

print sum(D!=0)

L = D-A
print sum(L)


# question 2
G=nx.Graph()
G.add_nodes_from([1,2,3,4,5,6])
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edge(4,2)
G.add_edge(6,2)
G.add_edge(3,4)
G.add_edge(4,5)
G.add_edge(5,6)

n = G.number_of_nodes()
A = nx.to_numpy_matrix(G)
D = np.matrix(np.zeros((n,n)))
i = 0
for node in graph.degree():
    D[i, i] = graph.degree()[node]
    i += 1

L = D-A

evals, evecs = np.linalg.eig(L)
vals = evals.copy()
vals.sort()
index =evals.tolist().index(vals[1])
values = np.array(evecs[:,index]).reshape(-1).tolist()
print values

meanval = mean(values)
print meanval

cluster1 = [i for i in range(n) if values[i] <= meanval]
print [i +1 for i in cluster1]

cluster2 = [i for i in range(n) if values[i] > meanval]
print [i +1 for i in cluster2]
