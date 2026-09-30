# PLACEHOLDER: paste Qwen3-235B-A22B-2507 (thinking off) attempt 3 here verbatim.
import sys
from collections import defaultdict

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    p = int(input_data[idx]); idx += 1
    q = int(input_data[idx]); idx += 1
    a = [int(input_data[idx + i]) for i in range(n)]; idx += n
    
    r = p + q
    
    # val[i] = a[i] + i*q (0-indexed, corresponds to 1-indexed position i+1)
    vals = [a[i] + i * q for i in range(n)]
    
    if r == 0:
        print(n)
        return
    
    # Group positions by val[i] % r
    groups = defaultdict(list)
    for i in range(n):
        v = vals[i] % r
        groups[v].append(i)
    
    max_kept = 0
    
    for v, positions in groups.items():
        m = len(positions)
        if m == 1:
            max_kept = max(max_kept, 1)
            continue
        
        # For each position, compute x = val and y = r*(pos+1) - val
        # We need longest subsequence with x non-decreasing and y non-decreasing
        xs = []
        ys = []
        for pos in positions:
            x = vals[pos]
            y = r * (pos + 1) - vals[pos]
            xs.append(x)
            ys.append(y)
        
        # Coordinate compress y values
        all_y = sorted(set(ys))
        y_map = {y_val: i + 1 for i, y_val in enumerate(all_y)}
        ny = len(all_y)
        
        # DP with CDQ divide and conquer
        dp = [1] * m
        
        def cdq(l, r):
            if l >= r:
                return
            
            mid = (l + r) // 2
            cdq(l, mid)
            
            # Get left and right indices sorted by x
            left_indices = sorted(range(l, mid + 1), key=lambda i: xs[i])
            right_indices = sorted(range(mid + 1, r + 1), key=lambda i: xs[i])
            
            # Fenwick tree for max query on y
            tree = [0] * (ny + 1)
            
            def update(y, val):
                while y <= ny:
                    if val > tree[y]:
                        tree[y] = val
                    y += y & (-y)
            
            def query(y):
                result = 0
                while y > 0:
                    if tree[y] > result:
                        result = tree[y]
                    y -= y & (-y)
                return result
            
            # Process right half using left half
            j = 0
            for ri in right_indices:
                while j < len(left_indices) and xs[left_indices[j]] <= xs[ri]:
                    li = left_indices[j]
                    cy = y_map[ys[li]]
                    update(cy, dp[li])
                    j += 1
                
                cy_r = y_map[ys[ri]]
                best = query(cy_r)
                if best + 1 > dp[ri]:
                    dp[ri] = best + 1
            
            cdq(mid + 1, r)
        
        cdq(0, m - 1)
        
        max_kept = max(max_kept, max(dp))
    
    print(n - max_kept)

solve()