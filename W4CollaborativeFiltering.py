import pandas as pd

HP1 = np.array([4,5,nan,nan])
HP2 = np.array([nan,5,nan,3])
HP3 = np.array([nan,4,nan,nan])
TW  = np.array([5,nan,2,nan])
SW1 = np.array([1,nan,4,nan])
SW2 = np.array([nan,nan,5,nan])
SW3 = np.array([nan,nan,nan,3])

from pandas import DataFrame
df = DataFrame({'HP1':HP1, 
                'HP2':HP2,
                'HP3':HP3,
                'TW': TW,
                'SW1':SW1,
                'SW2':SW2,
                'SW3':SW3}, index = ['A','B','C','D'])

print df

def jaccardSimilarity(r1, r2):
     return float(sum((r1 >0 ) & (r2 > 0)))/sum((r1 >0 ) | (r2 >0))
    
from itertools import combinations

for i,j in combinations(df.index, 2):
    print "Jaccard similarity between {0} and {1} is {2}".format(i,j,jaccardSimilarity(df.loc[i], df.loc[j]))
    
def cosineSimilarity(df, i1, i2):
    df0 = df.replace(nan,0)
    c = dot(df0.loc[i1],df0.loc[i2])/norm(df0.loc[i1])/norm(df0.loc[i2])
    return c
    
for i,j in combinations(df.index, 2):
    print "Cosine similarity between {0} and {1} is {2}".format(i,j,cosineSimilarity(df,i,j))


def normalizeDF(df):       
    dfn = df.radd(-1*sum(df,1)/sum(df > 0,1),0)
    return dfn  
    
dfn = normalizeDF(df)
for i,j in combinations(dfn.index, 2):
    print "Cosine similarity between {0} and {1} is {2}".format(i,j,cosineSimilarity(dfn,i,j))

# User- User filtering


def ratingPredictions(df, u, i, k, s = False):
    rated = df[i] > 0
    N = [ind for ind in rated.index if rated[ind]]
    try:
        N.remove(u)
    except:
        None
    if N == []:
        return None
    dfn = normalizeDF(df)
    sim = []
    for neighbor in N:
        if cosineSimilarity(dfn, u, neighbor) > 0:
            sim.append(cosineSimilarity(dfn, u, neighbor))
        else:
            sim.append(0)
    nnid = [N[ind] for ind in sorted(range(len(sim)), key=lambda i: sim[i])[-k:]]
    p = 0
    q = 0
    if s:
        for nid in nnid:
            p += df.at[nid,i] * sim[N.index(nid)]
            q += sim[N.index(nid)]
        return float(p)/q
    else:
        for nid in nnid:
            p += df.at[nid, i]
            q += 1
        return float(p)/q

print ratingPredictions(df, "A", "HP2", 2)
 
print ratingPredictions(df, "A", "HP2", 2, True)

