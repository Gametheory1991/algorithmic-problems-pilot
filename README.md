# Algorithmic Problems Pilot

This repository contains a small pilot study in quantitative computer science and
algorithms. The pilot follows a fixed procedure modelled on public AI research
collections: a problem is stated in advance, the method that will verify an answer
is registered before any computation runs, and a result is described as proven only
when that verification has passed. Results that rest on simulation are labelled as
simulation evidence. Results that have not been run are labelled as registered and
not yet run.

This is a personal project. It uses public data and synthetic data only. It uses no
employer data, no employer systems, and no non-public market data, and it expresses
the author's own work and opinions only.

## Catalogue

The pilot registers ten problems. Five problems have been run and verified. Five
problems are registered with their verification methods stated and have not been
run.

| No. | Problem | Status | Verification method |
|-----|---------|--------|---------------------|
| 1 | Bin packing: First-Fit Decreasing against the exact optimum | Run and verified | Exhaustive subset dynamic programming; both packings validated item by item |
| 2 | Sorting networks: necessity of each comparator in the 8-input network | Run and verified | Exhaustive check over all 256 binary inputs (zero-one principle) |
| 3 | Scheduling: Smith's rule, and its smallest failure case with release dates | Run and verified | Exhaustive check over all permutations for n ≤ 8 |
| 4 | Travelling salesman: heuristic distance from the known optimum on TSPLIB eil51 | Run and verified | Published optimum of 426; tour validity and length recomputed independently |
| 5 | Optimal stopping: exact threshold for the secretary problem | Run and verified | Exact dynamic programming against 200,000-trial Monte Carlo simulation, fixed seed |
| 6 | Multi-armed bandits: regret of UCB1, Thompson Sampling, and epsilon-greedy | Registered, not run | Synthetic arms; true best arm known by construction |
| 7 | Optimal execution: closed-form trajectory against a searched policy, synthetic market | Registered, not run | 100,000 seeded simulated price paths, common random numbers |
| 8 | Coin systems: conditions under which the greedy algorithm is optimal | Registered, not run | Exact dynamic programming at every amount up to 200 |
| 9 | Market making: break-even spread in a synthetic informed-flow simulator | Registered, not run | Analytic solution checked against simulation with the informed share known by construction |
| 10 | Exact SAT counting: scaling of a DPLL counter against brute force | Registered, not run | Counts cross-checked by brute-force enumeration on instances with at most 24 variables |

The full registration text for all ten problems is in [PILOT.md](PILOT.md).

## Verified results

Problem 1 has been completed. In 200 synthetic bin-packing instances generated on
1 November 2026 (bin capacity 100, 12 items per instance, item sizes drawn uniformly
from 15 to 60, seeds 0 to 199), the First-Fit Decreasing heuristic used one more bin
than the proven optimum in 30 instances, which is 15 percent of the sample. The
maximum gap was 1 bin and the mean gap was 0.15 bins. The manuscript, the code, and
the machine-readable result are in
[problems/001-bin-packing](problems/001-bin-packing/).

Problem 2 has been completed. The 8-input sorting network produced by Batcher's
odd-even mergesort construction has 19 comparators. Run on 2 November 2026 under
the registered verifier (the zero-one principle, applied exhaustively), the full
network sorted all 256 binary inputs with no failures, and each of the 19
single-comparator removals failed on at least one input, so every comparator is
necessary. In total 5,120 cases were checked (20 networks × 256 inputs); 620 of
the 4,864 removal cases (12.7 percent) produced an unsorted output. The
manuscript, the code, and the machine-readable result are in
[problems/002-sorting-networks](problems/002-sorting-networks/).

Problem 3 has been completed. Without release dates, Smith's rule (ordering
jobs by non-decreasing ratio of processing time to weight) matched the
brute-force optimum on every instance checked exhaustively on 3 November 2026:
5,498 job multisets representing 685,250 labelled instances, covering all
processing times and weights in {1, 2, 3} up to 6 jobs and all in {1, 2} up to
8 jobs, with a subset dynamic program agreeing with the brute-force optimum
throughout. With release dates added, the smallest counterexample to the
static ratio order, in the enumeration registered in advance, has two jobs of
processing time 1 — weights 1 and 2, release dates 0 and 1 — on which the
ratio order scores 7 against an optimum of 5, because it leaves the machine
idle waiting for the higher-priority job while a released job waits. The
manuscript, the code, and the machine-readable result are in
[problems/003-scheduling](problems/003-scheduling/).

Problem 4 has been completed. On the public TSPLIB eil51 instance (published
optimum 426), nearest neighbour from city 1, run on 3 November 2026, produced
a tour of length 511, and best-improvement 2-opt reduced it to 435, which is
9 above the optimum, or 2.11 percent. Run from all 51 start cities, nearest
neighbour ended between 482 and 563 and 2-opt ended between 429 and 449, with
no start reaching the optimum. Every reported tour was validated as a
permutation of the 51 cities, its length recomputed by a second
implementation, and its final form checked to admit no improving 2-opt
reversal. The manuscript, the code, and the machine-readable result are in
[problems/004-tsp](problems/004-tsp/).

Problem 5 has been completed. For the classic secretary problem, the exact
optimal policy, computed by dynamic programming in rational arithmetic on
3 November 2026, is to observe the first 3 of 10, 18 of 50, and 37 of 100
candidates and then hire the first who is the best seen so far, with exact
success probabilities 0.398690 (the fraction 3349/8400), 0.374275, and
0.371043 respectively. The classical threshold formula, maximised over all
thresholds in exact arithmetic, reproduced the dynamic-programming value and
threshold at each n, and a 200,000-trial Monte Carlo simulation of the policy
at each n (fixed seed 20261103) agreed with the exact value within 1.43
standard errors or less, inside the registered three-standard-error band.
The manuscript, the code, and the machine-readable result are in
[problems/005-optimal-stopping](problems/005-optimal-stopping/).

## How results are produced and corrected

Each problem directory contains a manuscript stating the claim, the method, the
result, and the limits of the result, together with the code and the result file
that support it. Corrections and withdrawals, if any occur, will be recorded in
[HISTORY.md](HISTORY.md), and earlier versions will remain accessible through the
repository history.

## Licence

MIT. See [LICENSE](LICENSE).
