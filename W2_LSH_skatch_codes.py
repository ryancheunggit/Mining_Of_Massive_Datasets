# scatch codes along lectures

def shingles(text,k):
    S = dict()
    for i in range(len(text)-k+1):
        if text[i:i+k] not in S:
            S[text[i:i+k]] = 1
        else:
            S[text[i:i+k]] += 1
    return S

text = 'The dog which chased the cat'
text2 = 'The dog that chased the cat'
text2 = 'The dog that \n chased the cat'
S1 = shingles(text,3)
S2 = shingles(text2,3)
S3 = shingles(text3,3)
# adding tokenize when the shingles are too long
def shingles(text,k,tokenize = False,klen = 20):
    S = dict()
    for i in range(len(text)-k):
        s = text[i:i+3]
        if tokenize and k > klen:
            s = hash(s)
        if s not in S:
            S[s] = 1
        else:
            S[s] += 1
    return S

S3P = shingles(text3,3, True, 2)

print shingles(text,3, True, 2)
# Jaccard Similarity
def jaccardSimilarityOfTwoDict(D1,D2):
    S1, S2 = set(D1.keys()), set(D2.keys())
    return float(len(set.intersection(S1,S2)))/len(set.union(S1,S2))

print jaccardSimilarityOfTwoDict(S1,S2)

D1 = {1:1,
      2:1,
      4:1}

D2 = {0:1,
      2:1,
      4:1,
      5:1}

D3 = {}
print jaccardSimilarityOfTwoDict(D1,D2)

# try to generate Boolean Matrices:

def generateBMatrix(Dicts, rowNames = None):
    if rowNames == None:
        rowNames = list(set(sum([d.keys() for d in Dicts])))
    nrow, ncol = len(rowNames), len(Dicts)
    M = np.zeros((nrow,ncol))
    for i in range(nrow):
        for j in range(ncol):
            if rowNames[i] in Dicts[j].keys():
                M[i][j] = 1
    return M

Dicts = [D1, D2, D3]

M = generateBMatrix(Dicts)
print M

Dicts = [D1,D2]
M = generateBMatrix(Dicts, range(6))
print M

def jaccardSimilarityFromTwoArray(A1,A2):
    return float(sum(A1+A2 == 2))/sum(A1+A2 != 0)

def jaccardSimilarityFromBMatrix(M):
    n = shape(M)[1]
    retList = []
    for i in range(n):
        for j in range(i+1,n):
            retList.append((i,j,jaccardSimilarityFromTwoArray(M[:,i],M[:,j])))
    return retList

print jaccardSimilarityFromBMatrix(M)

# Minhashing

BM  = np.matrix('1 0 1 0;1 0 0 1;0 1 0 1; 0 1 0 1; 0 1 0 1;1 0 1 0;1 0 1 0')

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

permu = [[2,3,6,5,0,1,4],
         [3,1,0,2,5,6,4],
         [0,2,6,5,1,4,3]]

for p in permu:
    print minhashing(BM, p)


def signatureMatrix(BM,minhashNum = 100):
    from random import shuffle
    retMatrix = np.zeros((minhashNum,shape(BM)[1]))
    permu = range(shape(BM)[0])
    for i in range(minhashNum):
        shuffle(permu)
        retMatrix[i,:] = minhashing(BM, permu)
    return retMatrix

random.seed(123)
sigM = signatureMatrix(BM)

print sigM[1:5]

def similarityOfSignatures(sigM):
    retList = []
    n = shape(sigM)[1]
    for i in range(n):
        for j in range(i+1,n):
            retList.append((i+1,j+1, \
            float(sum(sigM[:,i]==sigM[:,j]))/shape(sigM)[0]))
    return retList

print similarityOfSignatures(sigM)
print jaccardSimilarityFromBMatrix(BM)

# implementation

# try it on the example in slides
BM = np.matrix('1 0;0 1;1 1;1 0;0 1')

hashes = [lambda x: x%5,
          lambda x: (2*x+1)%5]

def QuickSig(BM,hashes):
    retMatrix = infty*np.ones((len(hashes),shape(BM)[1]))
    for i in range(shape(BM)[0]):
        hs = []
        for h in hashes:
            hs.append(h(i+1))
        for j in range(shape(BM)[1]):
            if BM[i,j] == 1:
                for k in range(len(hs)):
                    if hs[k] < retMatrix[k,j]:
                        retMatrix[k,j] = hs[k]
    return retMatrix

QuickSig(BM, hashes)

# generate random hash functions!
_memomask = {}

def hash_function(n):
    import random
    mask = _memomask.get(n)
    if mask is None:
        random.seed(n)
        mask = _memomask[n] = random.getrandbits(32)
    def myhash(x):
        return hash(x) ^ mask
    return myhash

# try it on pervious example data set with new implementation and random hashes
BM  = np.matrix('1 0 1 0;1 0 0 1;0 1 0 1; 0 1 0 1; 0 1 0 1;1 0 1 0;1 0 1 0')

random.seed(123)
hashes = [hash_function(n) for n in range(100)]

QsigM = QuickSig(BM, hashes)

print similarityOfSignatures(QsigM)

# LSH

def LSH(SigMatrix, bands = math.ceil(float(shape(SigMatrix)[0])/2)):
    blens = ceil(float(shape(SigMatrix)[0])/bands)
    candidatePairs = {}
    for b in range(int(bands)):
        rows = SigMatrix[b*blens:min(shape(SigMatrix)[0],(b+1)*blens),:]
        for i in range(shape(rows)[1]):
            for j in range(i+1,shape(rows)[1]):
                if sum(rows[:,i]==rows[:,j]) == len(rows[:,i]):
                    if (i,j) not in candidatePairs:
                        candidatePairs[(i,j)] = 1
                    else:
                        candidatePairs[(i,j)] += 1
    return candidatePairs

print LSH(sigM, 50)


# distance measurements

# euclidean distance

def L1norm(x,y):
    return sum(abs(x-y))

def L2norm(x,y):
    return sum((x-y)**2)**0.5

def Linftynorm(x,y):
    return sum((x-y)**infty)**(1.0/infty)


print L1norm(np.array([1,2]),np.array([2,3]))

print L2norm(np.array([1,2]),np.array([2,3]))

print Linftynorm(np.array([1,2]),np.array([2,3]))

# Jaccard distance for sets

def jaccardDistance(set1,set2):
    return 1 - len(set.intersection(set1,set2))*1.0/len(set.union(set1,set2))

print jaccardDistance({1,2},{2,3})

# cosine distance for vectors

def cosineDistance(v1,v2):
    c = dot(v1,v2)/norm(v1)/norm(v2)
    angle = arccos(clip(c, -1, 1))
    return angle

v1 = np.array((0,1))
v2 = np.array((1,0))

print cosineDistance(v1,v2)

# edit distance:

def lcs(xstr, ystr):
    if not xstr or not ystr:
        return ""
    x, xs, y, ys = xstr[0], xstr[1:], ystr[0], ystr[1:]
    if x == y:
        return x + lcs(xs, ys)
    else:
        return max(lcs(xstr, ys), lcs(xs, ystr), key=len)

def editDistance(s1,s2):
    return len(s1)+len(s2)-2*len(lcs(s1,s2))

print editDistance('Heolld World','Hello Walled')

# hamming distance
def hammingDistance(bv1, bv2):
    return sum(abs(bv1-bv2))

bv1 = np.array([1,0,1,0,1])

bv2 = np.array([1,0,0,1,1])

print hammingDistance(bv1,bv2)


import distance

print distance.hamming("hamming", "hamning")
