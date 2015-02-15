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
    for i in range(len(market)):
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
                    confidance = csSet.support*1.0/sSets[index].support
                except:
                    None
                if index and confidance >= conf:
                    ruleSets.append(associationRule(csSet, item, confidance ))
    return ruleSets

ruleSets =  findAssociationRule(market, baskets, 0.4, 0.5, 0.8)


def printAssociationRule(ruleSets):
    for rule in ruleSets:
        print "{0} -> {1}, with confidence {2}".format(rule.set.items, rule.item, rule.confidence)

printAssociationRule(ruleSets)
