from stemming import porter
import numpy as np
from numpy.linalg import pinv


documents = ['this is the first document, this really is',
             'nothing will stop this from been the second doument, second is not a bad order',
             'I wonder if three documents would be ok as an example, example like this is stupid',
             'ok I think four documents is enough, I I I I think so.']

def TFIDF(documents):
    terms = []
    termsInDocs = dict()
    # word list and count 'in what documnet' did the word appears
    for i, d in enumerate(documents):
        content = [porter.stem(term) for term in d.strip(',.').split()]
        for c in content:
            if c not in terms:
                termsInDocs[c] = [i]
                terms.append(c)
            else:
                termsInDocs[c].append(i)
    # generate the TF matrix
    F = np.zeros((len(terms),len(documents)))
    for i, term in enumerate(terms):
        for doc in termsInDocs[term]:
            F[i, doc] += 1
    TF = F/F.max(0)

    IDF = np.ones((len(terms),1))
    for i in range(len(terms)):
        IDF[i] = math.log(float(len(terms))/len(set(termsInDocs[terms[i]])))

    TF_IDF = TF*IDF
    return F, TF, IDF, TF_IDF, terms

F, _, _, _, _ = TFIDF(documents)

M = np.matrix(F).transpose()

def columnSelect(M,c):
    M2 = np.multiply(M,M)
    cP = M2.sum(axis = 0)
    cP /= cP.sum()
    C = np.random.choice(range(shape(M)[1]), size = c, replace = True, p = cP.tolist()[0])
    Cd = M[:,C] * np.diag(np.sqrt(1.0/c*cP[:,C]).tolist()[0])
    return Cd
    

def CUR(M, c, r):
    
    C = columnSelect(M,c)
    R = columnSelect(M.transpose(),r).transpose()
    U = pinv(C,c) * M * pinv(R,r)

    return C, U, R
    

np.random.seed(123)

C, U, R = CUR(M, 2, 2)
