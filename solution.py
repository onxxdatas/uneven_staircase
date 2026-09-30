import sys
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); p = int(data[1]); q = int(data[2])
    m = p + q
    groups = {}
    for i in range(1, n + 1):
        a = int(data[2 + i])
        A = a + q * i          # must be non-decreasing along a kept chain
        C = p * i - a          # must be non-decreasing along a kept chain (C = -B)
        groups.setdefault(A % m, []).append((A, C))
    best = 0
    for lst in groups.values():
        lst.sort()
        tails = []
        for _, c in lst:
            k = bisect_right(tails, c)
            if k == len(tails):
                tails.append(c)
            else:
                tails[k] = c
        if len(tails) > best:
            best = len(tails)
    print(n - best)


main()
