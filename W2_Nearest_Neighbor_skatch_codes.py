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

# Frequent Itemsets

items = { 'milk', 'coke', 'pepsi', 'beer', 'juice'}

baskets = [{ 'milk', 'coke', 'beer'},
           { 'milk', 'pepsi', 'juice'},
           { 'milk', 'beer'},
           { 'coke', 'juice'},
           { 'milk', 'pepsi', 'beer'},
           { 'milk', 'coke', 'beer','juice'},
           { 'coke', 'beer', 'juice'},
           { 'beer', 'coke'}]

def frequentItemsets(items, baskets, itemsInSet = 1, threshold = 0):
    freqItems = []
    supports = []
    from itertools import combinations
    for itemsets in combinations(items, itemsInSet):
        freqItems.append(set(itemsets))
        supports.append(sum([1 for basket in baskets if set(itemsets).issubset(basket)]))
        if supports[-1] <= threshold:
            freqItems.pop()
            supports.pop()
    return freqItems, supports

def printFreqItemWithSupport(freqItems,supports):
    for i in range(len(freqItems)):
        print freqItems[i], supports[i]

fis, sup = frequentItemsets(items,baskets,1)
printFreqItemWithSupport(fis, sup)

fis, sup = frequentItemsets(items,baskets,1,2)
printFreqItemWithSupport(fis, sup)

fis, sup = frequentItemsets(items,baskets,2)
printFreqItemWithSupport(fis, sup)
