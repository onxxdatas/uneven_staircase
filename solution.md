# Solution

## 1. Reduce to "keep as many elements as possible"
Edited entries can be any integers, so the answer is `n - K`, where `K` is the maximum size of a set of
indices whose values can stay unchanged. For kept indices `i < j` (consecutive among kept ones) with gap
`g = j - i` and `d = a_j - a_i`, the elements in between are free, so the only requirement is that `g` steps
of `+p` / `-q` sum to `d`. Different consecutive pairs do not interact. A single kept element is always fine, so `K >= 1`.

## 2. Pair condition in closed form
Let `x` be the number of climbs (`0 <= x <= g`). Then `d = p*x - q*(g-x)`, i.e.

    x = (d + q*g) / (p+q)         must be an integer with 0 <= x <= g.

Define, for every index `i`,

    A_i = a_i + q*i        B_i = a_i - p*i .

Then `d + q*g = A_j - A_i` and `p*g - d = B_i - B_j`, so the pair `(i, j)` is compatible iff

    A_j >= A_i,   B_j <= B_i,   A_j ≡ A_i (mod p+q).

(`A_j - A_i = (p+q)x` and `B_i - B_j = (p+q)(g-x)`; the two inequalities are exactly `x >= 0` and `x <= g`.)
Note `A_i - B_i = (p+q)*i`, so the residue of `A_i` mod `(p+q)` equals that of `B_i`, and two different points can never
have equal `(A,B)`.

## 3. Compatibility is transitive
Inequalities and equality of residues are transitive, so a set is valid iff it is a **chain** in this partial
order (no need to check only consecutive pairs). Any chain automatically has increasing indices, because
`(A_j - A_i) + (B_i - B_j) = (p+q)(j-i)`.

## 4. Algorithm
1. Bucket indices by `A_i mod (p+q)` (a dict of lists).
2. In each bucket sort by `(A, C)` where `C = -B = p*i - a_i`.
3. Longest **non-decreasing** subsequence of `C` (patience sorting with `bisect_right`).
   Ties are meaningful: equal `A` means a run of pure `-q` slides; equal `C` means a run of pure `+p` climbs,
   so sorting must be by `(A, C)` ascending and the LNDS must be non-strict.
4. `K` = max over buckets; print `n - K`.

Complexity `O(n log n)` time, `O(n)` memory. Values reach about `2*10^14` -- fine for Python integers
(use 64-bit in C++).

## 5. Verification
`solution_bf.py` tries all subsets of kept indices and checks each consecutive pair by enumerating the number of
climbs directly (no formulas). It agrees with `solution.py` on 1500 random small cases and on tests 1-8.
