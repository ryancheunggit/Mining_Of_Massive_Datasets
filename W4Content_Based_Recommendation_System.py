from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix
import scipy

items = ['this is the first document, this really is',
             'nothing will stop this from been the second doument, second is not a bad order',
             'I wonder if three documents would be ok as an example, example like this is stupid',
             'ok I think four documents is enough, I I I I think so.']

# will simply using tfidf as the item - profile
# row = item(documents) column = feature(term)
vectorizer = CountVectorizer(min_df=1)
counts = vectorizer.fit_transform(items)
# column  = item(documents) row = feature(term)
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(counts).transpose()

print tfidf.todense()

# user's rating for this four documents
# cloumn = user row = items(documents)
ratings = csr_matrix([[5, 0, 0, 2], [3, 3, 0, 0], [2, 1, 1, 1], [0, 0, 1, 1]], dtype = u'double')
# normalize
usersn = ratings - ratings.mean(0)

userprofile = tfidf.dot(usersn)

userprofile = csr_matrix(userprofile)


# smaller score suggest more similarity between user and item
for i in range(4):
    # iterative over 4 users
    scores = []
    u = userprofile[:,i]
    for j in range(4):
        # iterative over 4 documents
        v = tfidf[:,j]
        scores.append(sum(u.transpose().dot(v).todense())/np.linalg.norm(u.todense())/np.linalg.norm(v.todense()))
    print "document recommended for user {0} is document number {1}".format(i+1, scores.index(max(scores))+1)
