import numpy as np

def createA(M, b):
    n = shape(M)[0]
    A = b*M + (1.0-b)*1.0/n*np.ones(n)
    return A

def powerIteration(A, err=0.01):
    n = shape(A)[0]
    r = 1.0/n*np.ones((n,1))
    while sum(abs(A*r-r)) > err:
        r = A*r
    return r


# question 1

M = np.matrix([[0,0,0],
               [0.5,0,0],
               [0.5,1,1]])
b = 0.7
A = createA(M,b)
r = powerIteration(A)

print 3*(r[0]+r[1])
print 3*(r[0]+r[2])
print 3*(r[0]+r[1])
print 3*(r[1]+r[2])

# question 2
M = np.matrix([[0,  0,1],
               [0.5,0,0],
               [0.5,1,0]])
b = 0.85
A = createA(M,b)
r = powerIteration(A,0.00001)

print 0.85*r[2]-r[1]-0.575*r[0]
print r[1]-0.475*r[0]-0.05*r[2]
print r[0]-0.9*r[2]-0.05*r[1]
print 0.95*r[1]-0.475*r[0]-0.05*r[2]

# question 3
M = np.matrix([[0,  0,1],
               [0.5,0,0],
               [0.5,1,0]])
b = 1
A = createA(M,b)

r = np.ones((3,1))
for i in range(5):
    r = A*r
    print "iteration {0}".format(str(i+1))
    print r

r = np.ones((3,1))
while sum(abs(A*r-r)) > 0.00000000001:
    r = A*r
print r

# question 4
# a psudo map-reducer solution

def map(inputKVPairs):
    mapRetList = []
    from sympy import primefactors
    for kv in inputKVPairs:
        for p in primefactors(kv[1]):
            mapRetList.append((p,v))
    return mapRetList

def shuffle(mapRetList):
    Dict = {}
    for kv in mapRetList:
        if kv[0] not in Dict:
            Dict[kv[0]] = [kv[1]]
        else:
            Dict[kv[0]].append(kv[1])
    shuffleRetList = []
    for k in Dict:
        shuffleRetList.append((k,Dict[k]))
    return shuffleRetList

def reduce(inputKVPairs):
    reduceRetList = []
    for kv in inputKVPairs:
        reduceRetList.append((kv[0],sum(kv[1])))
    return reduceRetList


inputKVPairs = [(1,15),(2,21),(3,24),(4,30),(5,49)]

L = map(inputKVPairs)
D = shuffle(L)
R = reduce(D)

print R
