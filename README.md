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

The pilot registers ten problems. One problem has been run and verified. Nine
problems are registered with their verification methods stated and have not been
run.

| No. | Problem | Status | Verification method |
|-----|---------|--------|---------------------|
| 1 | Bin packing: First-Fit Decreasing against the exact optimum | Run and verified | Exhaustive subset dynamic programming; both packings validated item by item |
| 2 | Sorting networks: necessity of each comparator in the 8-input network | Registered, not run | Exhaustive check over all 256 binary inputs (zero-one principle) |
| 3 | Scheduling: Smith's rule, and its smallest failure case with release dates | Registered, not run | Exhaustive check over all permutations for n ≤ 8 |
| 4 | Travelling salesman: heuristic distance from the known optimum on TSPLIB eil51 | Registered, not run | Published optimum of 426; tour validity and length recomputed independently |
| 5 | Optimal stopping: exact threshold for the secretary problem | Registered, not run | Exact dynamic programming against 200,000-trial Monte Carlo simulation, fixed seed |
| 6 | Multi-armed bandits: regret of UCB1, Thompson Sampling, and epsilon-greedy | Registered, not run | Synthetic arms; true best arm known by construction |
| 7 | Optimal execution: closed-form trajectory against a searched policy, synthetic market | Registered, not run | 100,000 seeded simulated price paths, common random numbers |
| 8 | Coin systems: conditions under which the greedy algorithm is optimal | Registered, not run | Exact dynamic programming at every amount up to 200 |
| 9 | Market making: break-even spread in a synthetic informed-flow simulator | Registered, not run | Analytic solution checked against simulation with the informed share known by construction |
| 10 | Exact SAT counting: scaling of a DPLL counter against brute force | Registered, not run | Counts cross-checked by brute-force enumeration on instances with at most 24 variables |

The full registration text for all ten problems is in [PILOT.md](PILOT.md).

## Verified result

Problem 1 has been completed. In 200 synthetic bin-packing instances generated on
1 November 2026 (bin capacity 100, 12 items per instance, item sizes drawn uniformly
from 15 to 60, seeds 0 to 199), the First-Fit Decreasing heuristic used one more bin
than the proven optimum in 30 instances, which is 15 percent of the sample. The
maximum gap was 1 bin and the mean gap was 0.15 bins. The manuscript, the code, and
the machine-readable result are in
[problems/001-bin-packing](problems/001-bin-packing/).

## How results are produced and corrected

Each problem directory contains a manuscript stating the claim, the method, the
result, and the limits of the result, together with the code and the result file
that support it. Corrections and withdrawals, if any occur, will be recorded in
[HISTORY.md](HISTORY.md), and earlier versions will remain accessible through the
repository history.

## Licence

MIT. See [LICENSE](LICENSE).
