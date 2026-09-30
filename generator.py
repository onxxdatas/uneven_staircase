import random
import sys

# usage: python generator.py SEED N P Q MODE [NOISE_PERCENT]
# MODE: rand   - uniformly random values in [-V, V]
#       walk   - a valid (+p/-q) walk with NOISE_PERCENT% of entries corrupted
#       multi  - several interleaved valid walks (different residue classes) + noise
V = 10 ** 9


def main():
    seed, n, p, q = map(int, sys.argv[1:5])
    mode = sys.argv[5]
    noise = int(sys.argv[6]) if len(sys.argv) > 6 else 10
    rnd = random.Random(seed)
    lim = min(V, 6 * (p + q) + 6) if mode == "rand" and n <= 12 else V

    def walk(length, start):
        cur, res = start, []
        for _ in range(length):
            res.append(cur)
            cur += p if rnd.random() < q / (p + q) else -q  # roughly zero drift
        return res

    if mode == "rand":
        a = [rnd.randint(-lim, lim) for _ in range(n)]
    elif mode == "walk":
        a = walk(n, rnd.randint(-1000, 1000))
        for i in range(n):
            if rnd.randrange(100) < noise:
                a[i] += rnd.choice([-1, 1]) * rnd.randint(1, 3 * (p + q))
    else:
        a = [0] * n
        k = 4
        bases = [walk(n, rnd.randint(-50, 50)) for _ in range(k)]
        for i in range(n):
            a[i] = bases[rnd.randrange(k)][i]
            if rnd.randrange(100) < noise:
                a[i] += rnd.randint(-p - q, p + q)
    a = [max(-V, min(V, x)) for x in a]
    print(n, p, q)
    print(*a)


main()
