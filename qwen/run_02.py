import sys
from collections import defaultdict
from bisect import bisect_right

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    p = int(data[1])
    q = int(data[2])
    
    a = [int(data[i+3]) for i in range(n)]
    
    if n == 1:
        print(0)
        return
    
    s = p + q
    
    groups = defaultdict(list)
    
    for i in range(n):
        c_i = a[i] + i * q
        r = c_i % s
        if r < 0:
            r += s
        groups[r].append((i, c_i))
    
    max_kept = 0
    
    for r, items in groups.items():
        # Sort by c ascending, then by index descending (for tie-breaking)
        items_sorted = sorted(items, key=lambda x: (x[1], -x[0]))
        
        # Compute d values: d_i = c_i - s * i
        # We need longest non-increasing subsequence of d
        # Equivalently, longest non-decreasing subsequence of -d
        
        neg_d_values = [-(c - s * i) for (i, c) in items_sorted]
        
        # Find LNDS using patience sorting with bisect_right
        tails = []
        
        for val in neg_d_values:
            pos = bisect_right(tails, val)
            if pos == len(tails):
                tails.append(val)
            else:
                tails[pos] = val
        
        max_kept = max(max_kept, len(tails))
    
    print(n - max_kept)

solve()