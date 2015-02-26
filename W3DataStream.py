import random
# sliding window average:

stream = [random.random() for i in range(99)]

def slidingWindowAverage(stream, windowSize = 10):
    window = stream[:windowSize]
    avg = mean(window)
    index = windowSize
    while True:
        j = window.pop(0)
        i = stream[index]
        window.append(i)
        index += 1
        avg += float(i-j)/windowSize
        if index >= len(stream):
            break
    return avg

avg = slidingWindowAverage(stream)

print mean(stream)
print avg


# DGIM

# I have give up on the modulo timestamp implementation

def dgim(stream, windowSize, t = 0, buckets = dict()):
    # input n to add a new bit
    # input e to exit program
    # input a number ot query
    sizes = [2**i for i in range(int(round(math.log(windowSize,2))))]
    while True:
        option = raw_input()
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

stream = [int(round(random.random())) for i in range(99)]

stream = [1 for i in range(99)]
windowSize = 10

b, t = dgim(stream, windowSize)



buckets = {65:8,80:8,87:4,92:2,95:2,98:1,100:1}
windowSize = 40
t = 101

stream = [1 for i in range(120)]

b, t = dgim(stream, windowSize, t, buckets)
