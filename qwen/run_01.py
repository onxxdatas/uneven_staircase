import sys
from collections import defaultdict

def solve():
    input_data = sys.stdin.buffer.read().split()
    ptr = 0
    n = int(input_data[ptr]); ptr += 1
    p = int(input_data[ptr]); ptr += 1
    q = int(input_data[ptr]); ptr += 1
    a = [int(input_data[ptr + i]) for i in range(n)]
    
    if n == 1:
        print(0)
        return
    
    pq = p + q
    
    # For position i (0-indexed, representing checkpoint i+1):
    # If b[i+1] = a[i], then a[i] = b[1] + c*p - (i)*q where c is climbs in first i steps
    # => a[i] + i*q = b[1] + c*(p+q)
    # => a[i] + i*q ≡ b[1] (mod pq)
    # Let val_i = a[i] + i*q, r_i = val_i mod pq, k_i = (val_i - r_i) / pq
    # Then c_i = k_i - K where K = (b[1] - r_i) / pq (same for all kept positions with same residue)
    # Constraint: 0 <= c_i <= i, i.e., 0 <= k_i - K <= i => k_i - i <= K <= k_i
    
    # For two kept positions i < j with same residue:
    # c_j - c_i = k_j - k_i must satisfy 0 <= k_j - k_i <= j - i
    # This means: k_i <= k_j and k_j - k_i <= j - i
    
    # Group by residue
    groups = defaultdict(list)
    for i in range(n):
        val = a[i] + i * q
        r = val % pq
        k = (val - r) // pq
        groups[r].append((i, k))
    
    max_keep = 0
    
    for r, items in groups.items():
        if not items:
            continue
        
        m = len(items)
        
        # Find longest subsequence (in index order) where for consecutive elements (i1,k1), (i2,k2):
        # k1 <= k2 and k2 - k1 <= i2 - i1
        
        # Use DP with optimization via sorting and BIT
        # Sort by k, then by index ascending for equal k
        items_sorted = sorted(items, key=lambda x: (x[1], x[0]))
        
        # We need to find longest chain where indices are increasing and the k constraint holds.
        # Since we sorted by k, when processing in this order, k is non-decreasing.
        # We need to ensure indices are also increasing (subsequence constraint) and k2-k1 <= i2-i1.
        
        # The constraint k2 - k1 <= i2 - i1 can be rewritten as k2 - i2 <= k1 - i1.
        # Let d = k - i. Then we need d non-increasing along with index increasing.
        
        # So we want: process in order of increasing k (ties broken by increasing index),
        # and find longest subsequence with increasing index and non-increasing d.
        
        # Since within equal k, index is increasing, d = k - i is decreasing, so d is automatically non-increasing.
        # Across different k values, we need d to be non-increasing.
        
        # Approach: Process items in sorted order. For each item, find the best previous item
        # with smaller/equal k, smaller/equal d, and smaller index.
        # Since we process in order of (k, index), all previous items have k <= current k.
        # We need d >= current_d and index < current_index.
        
        # Use coordinate compression on d values and a BIT indexed by d.
        # But we also need index < current_index. Since we process in order of (k, index),
        # items with same k are processed in increasing index order. Items with smaller k were processed earlier.
        
        # Actually, since we want index increasing, and we're looking for subsequences,
        # we can use a different approach: 
        # Sort by (k, -d) or equivalently (k, i) since d = k - i.
        # Wait, d = k - i, so -d = i - k. Sorting by (k, i) is the same as sorting by (k, -d).
        
        # After sorting by (k, i), we want the longest subsequence with increasing i and non-increasing d.
        # Since d = k - i, and k is non-decreasing in our sort, d non-increasing means k - i non-increasing.
        
        # Key insight: after sorting by (k, i), if we just find LIS of i values, that gives us
        # a subsequence with increasing i. But we also need d non-increasing.
        
        # Hmm, let me think again. After sorting by (k, i):
        # - k is non-decreasing
        # - For equal k, i is increasing, so d = k - i is decreasing (good!)
        # - For different k values, we need to check if d is non-increasing
        
        # So the issue is only across different k values. Within the same k, it's automatically fine.
        
        # Let me use a simpler O(m^2) DP for now and see if it passes, then optimize if needed.
        
        # Actually for n up to 2*10^5, O(m^2) per group could be too slow in worst case.
        # Let me implement the BIT-based approach properly.
        
        # Collect d values for compression
        d_vals = []
        for idx_pos, k_val in items:
            d_vals.append(k_val - idx_pos)
        
        unique_d = sorted(set(d_vals))
        d_to_idx = {d: i for i, d in enumerate(unique_d)}
        num_d = len(unique_d)
        
        # BIT for prefix maximum (we'll invert d so that larger d maps to smaller index)
        # Query: max among d' >= d_current, which is prefix query on inverted index
        
        bit = [0] * (num_d + 1)
        
        def bit_update(i, val):
            i += 1
            while i <= num_d:
                if val > bit[i]:
                    bit[i] = val
                i += i & (-i)
        
        def bit_query(i):
            i += 1
            res = 0
            while i > 0:
                if bit[i] > res:
                    res = bit[i]
                i -= i & (-i)
            return res
        
        # Process items in sorted order by (k, i)
        dp_best = 0
        for idx_pos, k_val in items_sorted:
            d_val = k_val - idx_pos
            d_idx = d_to_idx[d_val]
            # Invert: we want d' >= d_val, which means d_idx' >= d_idx in original ordering
            # In BIT with inversion: position = num_d - 1 - d_idx
            inv_idx = num_d - 1 - d_idx
            best = bit_query(inv_idx)
            new_dp = best + 1
            bit_update(inv_idx, new_dp)
            if new_dp > dp_best:
                dp_best = new_dp
        
        max_keep = max(max_keep, dp_best)
    
    print(n - max_keep)

solve()