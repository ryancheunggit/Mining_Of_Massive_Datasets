# Nearest neighbors with LSH
from sparselsh import LSH
from scipy.sparse import csr_matrix

X = csr_matrix( [
    [ 3, 0, 0, 0, 0, 0, -1],
    [ 0, 1, 0, 0, 0, 0,  1],
    [ 1, 1, 1, 1, 1, 1,  1],
    [ 1, 0, 1, 1, 1, 1,  1]])

y = [ 0, 3, 10, 5]

query = csr_matrix( [ [ 1, 1, 1, 1, 1, 1, 0]])

lsh = LSH( 4,
           X.shape[1],
           num_hashtables=1,
           storage_config={"dict":None})

for ix in xrange(X.shape[0]):
    x = X.getrow(ix)
    c = y[ix]
    lsh.index( x, extra_data=c)

points = lsh.query(query, num_results=1)
print points[0][0][0].todense()
