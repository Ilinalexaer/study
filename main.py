import itertools
from functools import reduce

def get_biggest(numbers):
    result = []
    nl = sorted(list(map(str, numbers)), reverse=True)
    print(nl)
    for i in range(9, -1, -1):
        listlist = []
        for j in nl:
            if j[0] == str(i):
                listlist.append(j)
        if listlist:
            ulist = []
            perm_set = itertools.permutations(listlist)
            for i in perm_set:
                ulist.append(reduce(lambda x, y: x + y, i))
            result.append(max(ulist))
    return int(reduce(lambda x, y: x + y, result))


print(get_biggest([72, 7274]))
