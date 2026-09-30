# How the idea was developed

**Starting point.** The well-known family "change the fewest elements so that neighbours differ by exactly 1"
reduces to a 2D chain (`|a_j - a_i| <= j - i` plus parity). I wanted a problem in the same spirit whose reduction
is *not* memorised, so that the standard template does not fit directly.

**Rejected variants.**
1. *Cyclic version* (array on a circle, first and last also adjacent): correct reduction is a longest chain
   from a point to its shifted copy, i.e. cyclic-LIS territory (divide & conquer over non-crossing paths). Far
   too heavy for Div1/Div2 and awkward to verify.
2. *Prefix/suffix halving to make the array sorted* (`floor(a/2)` on a prefix and/or suffix): the prefix-only
   version collapses to a trivial right-to-left greedy; the two-sided version needs a 2-parameter DP with no clean
   speed-up.
3. *Symmetric steps `+-1` with a height cap `[0,H]`*: the cap is irrelevant once `H >= 1`, leaving only the classic
   template.
4. *Asymmetric steps `+p / -q` with a height cap*: the cap now genuinely restricts walks (e.g. `H=1` is a dead end),
   making the pair test depend on band geometry. Dropped to keep the statement clean.

**Final formulation.** Keep the free integer edits and unbounded heights, but make the steps asymmetric with
arbitrary `p, q <= 10^9`. Parity becomes a residue class modulo `p+q`, and the dominance conditions become
one non-decreasing and one non-increasing coordinate. Ties now carry real meaning (pure-climb / pure-slide runs).
This makes the problem a three-part observation: exact pair criterion, transitivity, LNDS inside residue buckets.
Typical wrong solutions (checked against the tests, see README): ignoring the modulus, grouping by the wrong
residue, breaking ties incorrectly, using a strict LIS.

**Originality check.** Web searches for the asymmetric-step "minimum edits" formulation returned no matching problem.
