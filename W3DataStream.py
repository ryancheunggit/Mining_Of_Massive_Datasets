import random
# sliding window average:

stream = [random.random() for i in range(99)]

def slidingWindowAverage(stream, windowSize = 10):
    window = stream[:windowSize]
    avg = mean(window)
    index = windowSize
    while True:
        option = raw_input('n for new input, e for exit: ')
        if option == 'n':
            j = window.pop(0)
            i = stream[index]
            window.append(i)
            index += 1
            avg += float(i-j)/windowSize
            print 'current average value is {0}'.format(avg)
        if index >= len(stream) or option == 'e':
            break
    return avg

avg = slidingWindowAverage(stream)


# DGIM

# I have give up on the modulo timestamp for this implementation

def dgim(stream, windowSize, t = 0, buckets = dict()):
    # input n to add a new bit
    # input e to exit program
    # input a number ot query
    sizes = [2**i for i in range(int(round(math.log(windowSize,2))))]
    while True:
        option = raw_input('e to exit; n to add 1 bit; any number to query  ')
        if option == 'n':
            # remove too old buckets
            for key in buckets.keys():
                if key <= t-windowSize:
                    buckets.pop(key)
            # adding a new bit in
            if stream[t] == 1:
                buckets[t] = 1
            t += 1
            # buckets cascading updating
            for size in sizes:
                if sum(np.array(buckets.values()) == size) == 3:
                    keys = [b for b in buckets.keys() if buckets[b] == size]
                    keys.sort()
                    buckets.pop(keys[0])
                    buckets[keys[1]] *= 2
            if t >= len(stream):
                break
        elif option == 'e':
            break
        else:
            k = int(option)
            keys = [b for b in buckets if b >= t - k]
            keys.sort()
            s = buckets[keys[0]]*0.5
            s += sum([buckets[b] for b in keys[1:]])
            print s, k
        print buckets


    return buckets, t

random.seed(123)

stream = [1 for i in range(99)]
windowSize = 10

b, t = dgim(stream, windowSize)



buckets = {65:8,80:8,87:4,92:2,95:2,98:1,100:1}
windowSize = 40
t = 101

stream = [1 for i in range(120)]

b, t = dgim(stream, windowSize, t, buckets)


# DGIM with modulo

def dgimTimeStamp(stream, windowSize, t = 0, buckets = dict()):
    # input n to add a new bit
    # input e to exit program
    # input a number ot query
    sizes = [2**i for i in range(int(round(math.log(windowSize,2))))]
    while True:
        option = raw_input('e to exit; n to add 1 bit; any number to query  ')
        if option == 'n':
            # remove too old buckets
            timestamp = t%windowSize
            for key in buckets.keys():
                if key == timestamp:
                    buckets.pop(key)
            # adding a new bit in
            if stream[t] == 1:
                buckets[timestamp] = 1
            t += 1
            # buckets cascading updating
            for size in sizes:
                if sum(np.array(buckets.values()) == size) == 3:
                    keys = [b for b in buckets.keys() if buckets[b] == size]
                    for i in range(len(keys)):
                        if keys[i] <= timestamp:
                            keys[i] += windowSize
                    keys.sort()
                    tbr = keys[0]
                    if tbr < windowSize:
                        buckets.pop(tbr)
                    else:
                        buckets.pop(tbr - windowSize)
                    tbm = keys[1]
                    if tbm < windowSize:
                        buckets[tbm] *= 2
                    else:
                        buckets[tbm-windowSize] *= 2
            if t >= len(stream):
                break
        elif option == 'e':
            break
        else:
            k = int(option)
            keys = [i%windowSize for i in range(t-k,t)]
            initial = True
            s = 0
            for key in keys:
                if key in buckets and initial == False:
                    s += buckets[key]
                if key in buckets and initial == True:
                    s += buckets[key]*0.5
                    initial =False
            print s, t
        print buckets


    return buckets, t

b, t = dgimTimeStamp(stream, 5)


# Bloom Filters
def h1(x,length):
    b = bin(x)[2:]
    s = [b[i] for i in range(len(b)) if i % 2 == 0]
    n = ''
    for i in s:
        n += i
    return int(n,2)%length

def h2(x,length):
    b = bin(x)[2:]
    s = [b[i] for i in range(len(b)) if i % 2 == 1]
    n = ''
    for i in s:
        n += i
    return int(n,2)%length

hashes = [h1,h2]

def bloomFilter(length = 11, hashes = []):
    s = [0 for i in range(length)]
    while True:
        n = raw_input('enter a integer, filter will tell seen or not: ')
        try:
            n = int(n)
        except:
            break

        location = [h(n,length) for h in hashes]
        seen = True
        for l in location:
            if s[l] == 0:
                seen = False
        if seen == True:
            print "has seen {} before".format(n)
        else:
            print "has not seen {} before".format(n)
            for h in hashes:
                s[h(n,length)] = 1
    return s

bloomFilter(11, hashes)

# sampling a stream
