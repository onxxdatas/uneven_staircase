# Uneven Staircase

Contents follow the required folder layout.

* `solution.py` -- O(n log n) accepted solution; `solution_bf.py` -- exponential brute force (n <= ~14).
* `generator.py` -- `python generator.py SEED N P Q MODE [NOISE%]`, MODE in `rand | walk | multi`.
* `test_cases/` -- 13 tests: edge (n=1, extremes, ties, residue trap), small brute-verified, and 5 large (n = 2e5).
  Tests 1-8 were cross-checked with `solution_bf.py`; the solution was also stress-tested on 1500 random small cases.
* Largest tests run in ~0.15 s locally with CPython.

## Qwen runs -- ACTION REQUIRED
The `qwen/` folder contains **placeholders only**. Qwen3-235B-A22B-2507 (thinking disabled) has to be run by you
at https://chat.qwen.ai/ : paste `problem.md` three times in fresh chats, share each conversation, put the links in
`qwen/conversations.md`, and save each returned program in `run_01.py` .. `run_03.py`. Run each against
`test_cases/` (`for i in 1 2 3 ...; do python run_0X.py < $i.in | diff - $i.out; done`) and confirm each fails at
least one test. If one passes everything, tweak the statement (e.g. change the constraints) or add tests before submitting.

Sanity check performed on my side: five plausible wrong variants (no modulus, wrong residue, wrong tie order,
strict LIS, residue of `a` only) each fail several of these tests.
