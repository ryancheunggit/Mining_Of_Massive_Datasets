from stemming import porter
import numpy as np

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

# M is the input matrix representing 4 documents and 35 terms

U,s,V = np.linalg.svd(M, full_matrices=False)
S = np.diag(s)

print np.allclose(np.identity(4), U.transpose()*U)
print np.allclose(M, np.dot(U, np.dot(S, V)))

# projection
print (U*S).transpose()
P = (U*S).transpose()

# Dimensionality Reduction

Mproj2 = np.dot(U[:,:2], S[:2,:2])

print Mproj2

# plot 2-D projections
x = Mproj2[:,0].transpose().tolist()[0]
y = Mproj2[:,1].transpose().tolist()[0]

plt.plot(x,y, 'ko')
for i in range(len(x)):
    plt.text(x[i]+0.1,y[i]+0.1, str(i+1))

Mrecov = np.dot(Mproj2, V[:2,:])

print Mrecov
# pca using scikit learn

m = np.matrix([[1,1],[2,2],[3,4]])
pca = deco.PCA(2)
m_r = pca.fit(m).transform(m)
print ('explained variance (first %d components): %.2f'%(2, sum(pca.explained_variance_ratio_)))
