
# question 2

market = set(range(1,101))

baskets = [{i for i in range(1,j+1) if (1.0*j/i)%2 == 0} for j in range(1,101)]

# the naive method
# ruleSets = findAssociationRule(market, baskets, 0.5, 0.6, 0.8)

# printAssociationRule(ruleSets)

# simple checking the options
print confidence({2,3,5}, 45, baskets)

print confidence({4,6}, 24, baskets)

print confidence({3,5}, 1, baskets)

print confidence({8, 12}, 96, baskets)

# question 3:

freqPairs = naiveApriori(market, baskets, 1)
printItemSet(freqPairs)
