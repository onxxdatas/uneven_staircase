import sys


def reachable(g, dy, p, q):
    # can g steps of (+p | -q) produce total change dy?  (direct enumeration, no formulas)
    return any(p * k - q * (g - k) == dy for k in range(g + 1))


def main():
    data = sys.stdin.read().split()
    n, p, q = int(data[0]), int(data[1]), int(data[2])
    a = list(map(int, data[3:3 + n]))
    best = 0
    for mask in range(1, 1 << n):
        idx = [i for i in range(n) if mask >> i & 1]
        if len(idx) <= best:
            continue
        if all(reachable(idx[t + 1] - idx[t], a[idx[t + 1]] - a[idx[t]], p, q)
               for t in range(len(idx) - 1)):
            best = len(idx)
    print(n - best)


main()
