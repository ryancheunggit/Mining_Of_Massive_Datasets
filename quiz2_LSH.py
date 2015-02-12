import numpy as np

# question 1

# question 2
def minhashing(BM, permu):
    retList = np.array([0 for dummy in range(shape(BM)[1])])
    for i in range(len(permu)):
        if len(retList.nonzero()[0]) == len(retList):
            return retList
            break
        else:
            tup = BM[permu.index(i),:].getA()[0].nonzero()[0]
            if len(tup) != 0:
                for j in tup:
                    if retList[j] == 0:
                        retList[j] = i+1
    return retList

BM = np.matrix('0 1 1 0; 1 0 1 1; 0 1 0 1; 0 0 1 0; 1 0 1 0; 0 1 0 0')
print BM

permu = [2,5,3,0,4,1]

minh = minhashing(BM,permu)

print [permu.index(minh[i]-1)+1 for i in range(4)]


# question 3
def LSH(SigMatrix, bands = math.ceil(float(shape(SigMatrix)[0])/2)):
    blens = ceil(float(shape(SigMatrix)[0])/bands)
    candidatePairs = {}
    for b in range(int(bands)):
        rows = SigMatrix[b*blens:min(shape(SigMatrix)[0],(b+1)*blens),:]
        for i in range(shape(rows)[1]):
            for j in range(i+1,shape(rows)[1]):
                if sum(rows[:,i]==rows[:,j]) == len(rows[:,i]):
                    if (i+1,j+1) not in candidatePairs:
                        candidatePairs[(i+1,j+1)] = 1
                    else:
                        candidatePairs[(i+1,j+1)] += 1
    return candidatePairs

sigM = np.matrix([[1,2,1,1,2,5,4],
                  [2,3,4,2,3,2,2],
                  [3,1,2,3,1,3,2],
                  [4,1,3,1,2,4,4],
                  [5,2,5,1,1,5,1],
                  [6,1,6,4,1,1,4]])

print LSH(sigM, 3).keys()

# question 4
def shingles(text,k):
    S = dict()
    for i in range(len(text)-k+1):
        if text[i:i+k] not in S:
            S[text[i:i+k]] = 1
        else:
            S[text[i:i+k]] += 1
    return S

text1 = 'ABRACADABRA'
text2 = 'BRICABRAC'
D1 = shingles(text1, 2)
D2 = shingles(text2, 2)
print len(D1.keys())
print len(D2.keys())

S1, S2 = set(D1.keys()), set(D2.keys())
print len(set.intersection(S1,S2))

def jaccardSimilarityOfTwoDict(D1,D2):
    S1, S2 = set(D1.keys()), set(D2.keys())
    return float(len(set.intersection(S1,S2)))/len(set.union(S1,S2))

print jaccardSimilarityOfTwoDict(D1,D2)

# question 6

tuples = [(53,10),(63,8),(56,15),(56,13)]
points = [(0,0),(100,40)]
for tup in tuples:
    L1 = []
    L2 = []
    for p in points:
        l1 = abs(tup[0]-p[0])+abs(tup[1]-p[1])
        l2 = ((tup[0]-p[0])**2 + (tup[1]-p[1])**2)**0.5
        L1.append(l1)
        L2.append(l2)
        #print tup,p,l1, l2
    print L1.index(min(L1))+1, L2.index(min(L2))+1
