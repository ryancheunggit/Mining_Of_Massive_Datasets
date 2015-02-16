# question 1
N = [40000, 100000, 20000, 50000]
M = [60000000, 100000000, 60000000, 80000000]
for i in range(4):
    print N[i]*(N[i]-1)/2.0 - (1000000+M[i])

for i in range(4):
    print min((1000000 + M[i]*12),(2*N[i]*(N[i]-1)))/100000000



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
