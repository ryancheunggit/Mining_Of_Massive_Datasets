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
        if tokenize and (len(s) >= klen):
            s = hash(s)
        if s not in S:
            S[s] = 1
        else:
            S[s] += 1
    return S

S3P = shingles(text3,3, True, 2)
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

M = generateBMatrix(Dicts, range(6))
print M

def jaccardSimilarityFromTwoArray(A1,A2):
    return float(sum(A1+A2 == 2))/sum(A1+A2 != 0)

def jaccardSimilarityFromBMatrix(BM):
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

def signatureMatrix(BM,minhashNum = 100):
    from random import shuffle
    retMatrix = np.zeros((minhashNum,shape(BM)[1]))
    permu = range(shape(BM)[0])
    for i in range(minhashNum):
        shuffle(permu)
        retMatrix[i,:] = minhashing(BM, permu)
    return retMatrix

sigM = signatureMatrix(BM,1000)

def similarityOfSignatures(sigM):
    retList = []
    n = shape(sigM)[1]
    for i in range(n):
        for j in range(i+1,n):
            retList.append((i+1,j+1, \
            float(sum(sigM[:,i]==sigM[:,j]))/shape(sigM)[0]))
    return retList

print similarityOfSignatures(sigM)


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

print QuickSig(BM, hashes)

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

print LSH(sigM, 500)
