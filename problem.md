# Uneven Staircase

**Time limit:** 2 seconds  **Memory limit:** 256 MB

A hiker walks along a trail of `n` checkpoints numbered `1..n`. Checkpoint `i` has recorded altitude `a_i`.
Between two consecutive checkpoints the trail is either a **climb** that raises the altitude by exactly `p`,
or a **slide** that lowers it by exactly `q`. Formally, a sequence `b_1..b_n` is a *valid trail* if for every
`1 <= i < n`:

    b_{i+1} - b_i = +p    or    b_{i+1} - b_i = -q .

The recorded array `a` may not be a valid trail. In one edit you may replace any single `a_i` by **any integer**
(negative values and values beyond the input bounds are allowed). Find the minimum number of edits needed to turn
`a` into a valid trail.

## Input

The first line contains three integers `n`, `p`, `q` (`1 <= n <= 2*10^5`, `1 <= p, q <= 10^9`).

The second line contains `n` integers `a_1, ..., a_n` (`-10^9 <= a_i <= 10^9`).

## Output

Print one integer: the minimum number of edits.

## Examples

### Input
```
8 2 1
0 2 3 5 4 9 7 8
```
### Output
```
5
```

### Input
```
6 2 3
0 1 2 3 4 5
```
### Output
```
4
```

## Note

In the second example every adjacent difference is `+1`, which is neither `+2` nor `-3`. Keep `a_1 = 0` and
`a_6 = 5` and edit the other four: `0, 2, 4, 6, 8, 5` is a valid trail (four climbs of `+2`, then one slide of `-3`).
No valid trail can keep three of the original values, so the answer is 4.
