import pandas
from pandas import DataFrame

df = DataFrame([[1,2,3,4,5],[2,3,2,5,3],[5,5,5,3,2]],
               index = ['A','B','C'],
               columns = ['M','N','P','Q','R'])

df1 = df.radd(-1*mean(df, 1), axis = 0)

df2 = df1.radd(-1*mean(df1, 0), axis = 1)

print df2


avals = [0,0.5,1,2]
for aval in avals:
    df =DataFrame([[1,0,1,0,1,2],[1,1,0,0,1,6],[0,1,0,1,0,2]],
                index = ['A', 'B', 'C'])
    df[5] = df[5]*aval
    a = df.loc['A']
    b = df.loc['B']
    c = df.loc['C']
    ab = dot(a,b)/norm(a)/norm(b)
    ac = dot(a,c)/norm(a)/norm(c)
    bc = dot(b,c)/norm(c)/norm(b)
    print 'alpha is {0}'.format(aval)
    print '    Distance between AB is{}\n \
    Distance between AC is{}\n \
    Distance between BC is{}\n'.format(arccos(clip(ab, -1, 1)),arccos(clip(ac, -1, 1)),arccos(clip(bc, -1, 1)))
