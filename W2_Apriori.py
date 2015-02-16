# Frequent Itemsets

market = { 'milk', 'coke', 'pepsi', 'beer', 'juice'}

baskets = [{ 'milk', 'coke', 'beer'},
           { 'milk', 'pepsi', 'juice'},
           { 'milk', 'beer'},
           { 'coke', 'juice'},
           { 'milk', 'pepsi', 'beer'},
           { 'milk', 'coke', 'beer','juice'},
           { 'coke', 'beer', 'juice'},
           { 'beer', 'coke'}]

class itemSet:
    def __init__(self,items, support = 0):
        self.items = items.copy()
        self.support = support
        self.numberOfItems = len(items)

#class itemSets:
#    def __init__(self, )

def frequentItemsets(market, baskets, itemsInSet = 1, supportThreshold = 1):
    itemSets = []
    from itertools import combinations
    for itemsets in combinations(market, itemsInSet):
        items = set(itemsets)
        support= sum([1 for basket in baskets if set(itemsets).issubset(basket)])
        if support >= supportThreshold:
            itemSets.append(itemSet(items,support))
    return itemSets

def printItemSet(itemSets):
    for itemSet in itemSets:
        print "{0} items set {1} with support {2}".format(itemSet.numberOfItems, itemSet.items, itemSet.support)

itemSets = frequentItemsets(market,baskets,1)
printItemSet(itemSets)

itemSets = frequentItemsets(market,baskets,1,2)
printItemSet(itemSets)

itemSets = frequentItemsets(market,baskets,2,3)
printItemSet(itemSets)


def findAllFrequentItemsets(market, baskets, supportThreshold = 0):
    itemSets = []
    for i in range(max([len(b) for b in baskets])):
        itemSets += frequentItemsets(market, baskets, i+1, supportThreshold)
    return itemSets

itemSets = findAllFrequentItemsets(market, baskets, 3)
printItemSet(itemSets)


def confidence(set1, item, baskets):
    numer = 0
    denom = 0
    for b in baskets:
        if set1.issubset(b):
            denom += 1
            if item in b:
                numer += 1
    return float(numer)/denom

set1 = {'beer', 'milk'}
item = 'coke'

print confidence(set1, item, baskets)

# Association rule

class associationRule:
    def __init__(self, lset, ritem, conf = 0):
        self.set = lset
        self.item = ritem
        self.confidence = conf

def findAssociationRule(market, baskets, cs, s, conf):
    csSets = findAllFrequentItemsets(market, baskets, cs)
    sSets = findAllFrequentItemsets(market, baskets, s)
    ruleSets = []
    for csSet in csSets:
        if csSet.numberOfItems > 1:
            for item in csSet.items:
                tempSet = csSet.items.copy()
                tempSet.remove(item)
                try:
                    index = [tempSet == sSet.items for sSet in sSets].index(True)
                    confidence = csSet.support*1.0/sSets[index].support
                except:
                    None
                if index and confidence >= conf:
                    ruleSets.append(associationRule(csSet, item, confidence ))
    return ruleSets

ruleSets =  findAssociationRule(market, baskets, 0.4, 0.5, 0.8)


def printAssociationRule(ruleSets):
    for rule in ruleSets:
        print "{0} -> {1}, with confidence {2}".format(rule.set.items, rule.item, rule.confidence)

printAssociationRule(ruleSets)

# storing frequent pairs

def itemMapInt(market):
    itemIntMap = {}
    intItemMap = {}
    for i, item in enumerate(market):
        intItemMap[i] = item
        itemIntMap[item] = i
    return itemIntMap, intItemMap

itemIntMap, intItemMap = itemMapInt(market)

# triangular matrix for frequent pairs
def freqMatrix(intItemMap, baskets, supportThreshold):
    n = len(intItemMap)
    freqMatrix = np.zeros((n,n))
    newIntItemMap = dict()
    for i in range(n-1):
        for j in range(i+1, n):
            for b in baskets:
                if set([intItemMap[i],intItemMap[j]]).issubset(b):
                    freqMatrix[j,i] += 1
                    if freqMatrix[j,i] >= supportThreshold:
                        if i not in newIntItemMap:
                            newIntItemMap[i] = intItemMap[i]
                        if j not in newIntItemMap:
                            newIntItemMap[j] = intItemMap[j]
    return freqMatrix, newIntItemMap


freqPairsMatrix, _  = freqMatrix(intItemMap, baskets, 2)
print freqPairsMatrix

def freqPairsFromMatrix(freqMatrix, itemIntMap, p1, p2):
    i = min(itemIntMap[p1],itemIntMap[p2])
    j = max(itemIntMap[p1],itemIntMap[p2])
    return freqMatrix[j,i]

print freqPairsFromMatrix(freqPairsMatrix, itemIntMap, 'coke', 'juice')

# tabular method



def freqList(baskets, intItemMap, supportThreshold):
    n = len(intItemMap)
    freqList = [0 for dummy in range((n**2-n)/2)]
    newIntItemMap = dict()
    for i in range(n-1):
        for j in range(i+1, n):
            for b in baskets:
                if set([intItemMap[i], intItemMap[j]]).issubset(b):
                    freqList[int(i*(n-(i+1)/2.0)+j-i-1)] += 1
                    if freqList[int(i*(n-(i+1)/2.0)+j-i-1)] >= supportThreshold:
                        if i not in newIntItemMap:
                            newIntItemMap[i] = intItemMap[i]
                        if j not in newIntItemMap:
                            newIntItemMap[j] = intItemMap[j]
    return freqList, newIntItemMap

freqPairsList, _ = freqList(baskets, intItemMap, 2)

print freqPairsList

def freqPairsFromList(freqList, itemIntMap, p1, p2):
    n = len(itemIntMap)
    i = min(itemIntMap[p1],itemIntMap[p2])
    j = max(itemIntMap[p1],itemIntMap[p2])
    return freqList[i*(n-(i+1)/2)+j-i-1]

print freqPairsFromList(freqPairsList, itemIntMap, 'coke', 'juice')

# A-Priori Algorithm

def naiveApriori(market, baskets, supportThreshold = 2, numItems = 2):
    previousMarket = market
    for i in range(1, numItems +1):
        currentMarket = set()
        frequentItemSets = frequentItemsets(previousMarket, baskets, i, supportThreshold)
        for itemset in frequentItemSets:
            currentMarket.update(itemset.items)
        previousMarket = currentMarket
    return frequentItemSets

frequentItemSets = naiveApriori(market, baskets, 2, 2)
printItemSet(frequentItemSets)


def freqItemsMapInt(frequentItems):
    itemIntMap = {}
    intItemMap = {}
    for i, item in enumerate(frequentItems):
        intItemMap[i] = item.items.copy().pop()
        itemIntMap[item.items.copy().pop()] = i
    return itemIntMap, intItemMap
        
        

def AprioriMatrix(market, baskets, supportThreshold = 2):
    # first pass through the data
    frequentItems = frequentItemsets(market, baskets, 1, supportThreshold)
    itemIntMap, intItemMap = freqItemsMapInt(frequentItems)
    # second pass through the data
    freqPairsMatrix, newIntItemMap = freqMatrix(intItemMap, baskets, supportThreshold)
    return freqPairsMatrix, newIntItemMap
    
M, Map = AprioriMatrix(market, baskets, 3)

print Map
    

def AprioriTabular(market, baskets, supportThreshold = 2):
    # first pass through the data
    frequentItems = frequentItemsets(market, baskets, 1, supportThreshold)
    itemIntMap, intItemMap = freqItemsMapInt(frequentItems)
    # second pass through the data
    freqPairsList, newIntItemMap = freqList(baskets, intItemMap, supportThreshold)
    return freqPairsList, newIntItemMap
    
L, Map = AprioriTabular(market, baskets, 3)

print Map  