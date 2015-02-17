market = { 'milk', 'coke', 'pepsi', 'beer', 'juice'}

baskets = [{ 'milk', 'coke', 'beer'},
           { 'milk', 'pepsi', 'juice'},
           { 'milk', 'beer'},
           { 'coke', 'juice'},
           { 'milk', 'pepsi', 'beer'},
           { 'milk', 'coke', 'beer','juice'},
           { 'coke', 'beer', 'juice'},
           { 'beer', 'coke'}]

# PCY Algorithm
def PCY(market, baskets, supportThreshold):
    # the first pass
    Counts = dict()
    buckets = dict()
    frequentItems = set()
    frequentItemSets = []
    for basket in baskets:
        # find frequent items
        for item in market:
            if set([item]).issubset(basket):
                if item not in Counts:
                    Counts[item] = 1
                else:
                    Counts[item] += 1
                    # update the list of frequent items
                    if Counts[item] >= supportThreshold:
                        frequentItems.update(set([item]))

        # find frequent buckets
        from itertools import combinations
        for itemPairs in combinations(basket,2 ):
            if hash(itemPairs) not in buckets:
                buckets[hash(itemPairs)] = 1
            else:
                buckets[hash(itemPairs)] += 1

        # convert bucket counts to a bit array
        '''
        from bitarray import bitarray
        hashedBuckets = buckets.keys()
        bitMap = bitarray([buckets[bucket] >= supportThreshold for bucket in hashedBuckets])
        # second pass
        for itemPairs in combinations(frequentItems,2):
            try:
                ind = hashedBuckets.index(hash(itemPairs))
            except:
                ind = None
            if ind and bitMap[ind]:
                frequentItemSets.append(set(itemPairs))
        '''

    for bucket in buckets:
        if buckets[bucket] >= supportThreshold:
            buckets[bucket] = True
        else:
            buckets[bucket] = False

    # second pass
    for itemPairs in combinations(frequentItems,2):
        if buckets[hash(itemPairs)]:
            frequentItemSets.append(set(itemPairs))
    return frequentItemSets

print PCY(market, baskets, 3)

# Multistage Algorithm
def Multistage(market, baskets, supportThreshold):
    # the first pass
    Counts = dict()
    buckets = dict()
    p2buckets = dict()
    frequentItems = set()
    frequentItemSets = []

    def p2hash(x):
        return hash(x)^2

    for basket in baskets:
        # find frequent items
        for item in market:
            if set([item]).issubset(basket):
                if item not in Counts:
                    Counts[item] = 1
                else:
                    Counts[item] += 1
                    # update the list of frequent items
                    if Counts[item] >= supportThreshold:
                        frequentItems.update(set([item]))

        # find frequent buckets
        from itertools import combinations
        for itemPairs in combinations(basket,2 ):
            if hash(itemPairs) not in buckets:
                buckets[hash(itemPairs)] = 1
            else:
                buckets[hash(itemPairs)] += 1
    # pass 2
    for bucket in buckets:
        if buckets[bucket] >= supportThreshold:
            buckets[bucket] = True
        else:
            buckets[bucket] = False

    for basket in baskets:
        for itemPairs in combinations(frequentItems,2):
            if buckets[hash(itemPairs)] and set(itemPairs).issubset(basket):
                if p2hash(itemPairs) not in p2buckets:
                    p2buckets[p2hash(itemPairs)] = 1
                else:
                    p2buckets[p2hash(itemPairs)] += 1

    for bucket in p2buckets:
        if p2buckets[bucket] >= supportThreshold:
            p2buckets[bucket] = True
        else:
            p2buckets[bucket] = False

    # third pass
    for itemPairs in combinations(frequentItems,2):
        if buckets[hash(itemPairs)] and p2buckets[p2hash(itemPairs)]:
            frequentItemSets.append(set(itemPairs))

    return frequentItemSets

print Multistage(market, baskets, 3)

# Simple Algorithm

def simple(market, baskets, supportThreshold, sampleSize, numSamples):
    itemSets = []
    candidateSets = []
    for i in range(numSamples):
        sampleBaskets = [baskets[ind] for ind in np.random.random_integers(0, len(baskets)-1, sampleSize)]
        itemSets += (findAllFrequentItemsets(market, sampleBaskets, supportThreshold*float(sampleSize)/len(baskets)))
    for itemSet in itemSets:
        if itemSet.items not in candidateSets:
            candidateSets.append(itemSet.items)
    return candidateSets
    
candidateSets = simple(market, baskets, 4, 4, 2)

# compared with true frequent itemsets
itemSets = findAllFrequentItemsets(market, baskets, 4)
printItemSet(itemSets)

# Simple Algorithm with a second pass validation
def simpleWithValidation(market, baskets, supportThreshold, sampleSize, numSamples):
    itemSets = []
    candidateSets = []
    counts = dict()
    for i in range(numSamples):
        sampleBaskets = [baskets[ind] for ind in np.random.random_integers(0, len(baskets)-1, sampleSize)]
        itemSets += findAllFrequentItemsets(market, sampleBaskets, supportThreshold*float(sampleSize)/len(baskets)/1.25)
    for i in itemSets:
        if i.items not in candidateSets:
            candidateSets.append(i.items)
    
    candidateSets = [itemSet(i) for i in candidateSets]
    
    # second pass validation
    for basket in baskets:
        for i in candidateSets:
            if set(i.items).issubset(basket):
                if i not in counts:
                    counts[i] = 1
                else:
                    counts[i] += 1
    
    candidateSets = []
    for i in counts:
        if counts[i] >= supportThreshold:
            candidateSets.append(i.items)
            
    return candidateSets
    
print simpleWithValidation(market, baskets, 4, 4, 2)