# Problem 1 — Bin packing: First-Fit Decreasing against the exact optimum

## Claim registered before the run

First-Fit Decreasing is a standard heuristic for packing items into the smallest
number of bins of fixed capacity. The registered question was: on small instances,
how often does this heuristic use more bins than the optimum, and what is the
largest gap? The verification method was registered at the same time: the optimum
for each instance is computed by exhaustive subset dynamic programming, which
examines every partition of the items into feasible bins, so the optimum it returns
is proven rather than estimated.

## Method

- Bin capacity: 100.
- Items per instance: 12, with sizes drawn uniformly from the integers 15 to 60.
- Instances: 200, generated with seeds 0 to 199 (one `random.Random(seed)` stream
  per instance).
- Heuristic: sort items in decreasing order and place each item in the first bin
  with sufficient remaining capacity, opening a new bin when no existing bin fits.
- Optimum: subset dynamic programming over all 2^12 subsets. A subset is feasible
  when its total size does not exceed 100. The minimum number of bins is the
  minimum number of feasible subsets that partition the full set.
- Validation: for every instance, both packings were checked programmatically.
  Each packing must contain every item exactly once, and no bin may exceed the
  capacity of 100.

## Result

The computation was run on 1 November 2026 and all 200 instances passed both
validation checks.

- First-Fit Decreasing used more bins than the optimum in 30 of 200 instances,
  which is 15 percent of the sample.
- The maximum gap was 1 bin. The mean gap was 0.15 bins.
- The first instance attaining the maximum gap was seed 8, with item sizes
  29, 38, 39, 23, 27, 60, 17, 20, 23, 30, 47, and 28.
  - First-Fit Decreasing produced 5 bins: [60, 39], [47, 38], [30, 29, 28],
    [27, 23, 23, 20], [17].
  - The proven optimum is 4 bins: [23, 47, 28] with total 98; [27, 17, 20, 30]
    with total 94; [39, 60] with total 99; and [29, 38, 23] with total 90.
    The four bins contain all 12 items exactly once, and no bin exceeds 100.

## Limits

These figures describe the stated sample only: 200 instances at 12 items per
instance with sizes uniform on 15 to 60 and capacity 100. They do not estimate the
performance of First-Fit Decreasing at other item counts, size distributions, or
capacities, and they do not revise the known worst-case approximation guarantees
for the algorithm, which are established results in the literature and are not
tested here.

## Files

- `run_binpacking.py` — the complete computation. Run it from this directory;
  it writes `result.json` in this directory.
- `result.json` — the machine-readable result, including the seed 8 instance and
  both of its packings.

## Reproducibility note

The first execution of this computation on 1 November 2026 calculated all figures
correctly and passed all validation checks, and then failed to write its result
file because the output path named a directory that does not exist. The figures
were recovered from the printed output of that execution and were re-verified
against the two packings before publication. The published code writes to a path
relative to the directory from which it is run, which removes that failure.
