# Problem 4 — Travelling salesman: heuristic distance from the known optimum on TSPLIB eil51

## Claim registered before the run

The eil51 instance in the public TSPLIB library is a 51-city travelling
salesman problem whose optimal tour length is known to be 426. The
registered question was: how close do the standard elementary heuristics —
nearest neighbour followed by 2-opt improvement — come to that optimum?
The verification method was registered at the same time: the published
optimum is the standard; every tour's validity is checked (each city
visited exactly once) and every tour length is recomputed independently.

The instance data are the coordinates in the public TSPLIB file for eil51
(NAME: eil51, COMMENT: 51-city problem (Christofides/Eilon), TYPE: TSP,
DIMENSION: 51, EDGE_WEIGHT_TYPE: EUC_2D). The coordinates are reproduced
in the run code. This is public benchmark data, published for exactly this
kind of comparison; no other data is used.

## Method

- Distances follow the TSPLIB EUC_2D rule: the distance between two cities
  is the Euclidean distance between their coordinates, rounded to the
  nearest integer. Tour length is the sum of the 51 edge distances,
  including the closing edge back to the first city.
- Nearest neighbour: start at the designated start city; repeatedly move
  to the nearest unvisited city; ties are broken by the lowest city
  number.
- 2-opt: repeatedly apply the single segment reversal with the largest
  length reduction (best improvement) until no reversal reduces the tour
  length.
- Primary protocol: nearest neighbour from city 1, then 2-opt.
- Secondary protocol: the same procedure from every start city, 1 to 51,
  so that the dependence of the result on the start city is measured
  rather than hidden.
- Verification, applied to every reported tour: the tour is a permutation
  of the 51 cities; its length is recomputed by a second, separately
  written length function; every final tour is checked to be 2-opt locally
  optimal, meaning no segment reversal reduces its length; and no reported
  length may fall below the published optimum of 426, which would
  indicate an error in the distance computation.
- The computation was run on 3 November 2026.

## Result

Under the primary protocol, nearest neighbour from city 1 produces a tour
of length 511, which is 85 above the optimum, or 19.95 percent. The tour
is: 1, 32, 11, 38, 5, 49, 9, 50, 16, 2, 29, 21, 34, 30, 10, 39, 33, 45, 15,
44, 37, 17, 4, 18, 47, 12, 46, 51, 27, 6, 48, 8, 26, 31, 28, 3, 20, 35, 36,
22, 7, 23, 24, 14, 25, 13, 41, 19, 42, 40, 43, and back to 1.

Nine best-improvement 2-opt reversals then reduce the length from 511 to
435. The improved tour is: 1, 32, 11, 38, 5, 49, 9, 50, 16, 2, 29, 21, 34,
30, 10, 39, 33, 45, 15, 44, 37, 17, 4, 42, 40, 19, 41, 13, 25, 14, 18, 47,
12, 46, 51, 27, 6, 23, 24, 43, 7, 48, 8, 26, 31, 28, 3, 36, 35, 20, 22, and
back to 1. The final length of 435 stands 9 above the published optimum of
426, a gap of 2.11 percent.

Across all 51 start cities, nearest neighbour alone ends between 482 and
563, so the primary protocol's 511 is a mid-range outcome for that
heuristic rather than a favourable one. After 2-opt, the 51 starts end
between 429 and 449, with a mean of 439.16. The best start is city 35,
whose final tour has length 429, which is 3 above the optimum, or
0.70 percent. The worst start is city 3, at 449. Two conclusions follow.
First, 2-opt removes most of the nearest-neighbour excess from every
start: the worst final tour (449) is shorter than the best unrepaired
nearest-neighbour tour (482). Second, the start city still matters after
2-opt, moving the final length by up to 20, because 2-opt stops at a local
optimum that depends on where the search began. No start reached the
optimum of 426.

## Limits

First, the 2-opt endpoint is a local optimum under segment reversals, not
a bound on the optimum. The only optimality figure used is the published
TSPLIB value of 426, which this run treats as given: the heuristics'
lengths are recomputed and validated here, but the optimality of 426
itself rests on the published record for the instance, as the registered
verifier specifies.

Second, the results describe this one instance and this one pair of
heuristics under the conventions fixed above. Different tie-breaking in
nearest neighbour, or a first-improvement rather than best-improvement
2-opt, can end at different local optima. The figures are not estimates
of heuristic performance on other instances.

Third, the distance figures are integers by the TSPLIB EUC_2D rounding
rule. Gaps stated in percent are computed from those integers, as the
published optimum of 426 is stated on the same basis, so all comparisons
are on a like-for-like footing.

## Files

- `run_tsp.py` — the complete computation, including the eil51 coordinates
  as published in TSPLIB. Run it from this directory; it prints the full
  result and writes `result.json` in this directory.
- `result.json` — the machine-readable result: the primary protocol's
  nearest-neighbour and 2-opt tours and lengths, and the all-starts
  summary with the best tour and the final length for each of the 51
  start cities.

## Reproducibility note

The figures in this document were produced by the registered run on
3 November 2026 and were then recomputed by a second, independently
written implementation. The second implementation rebuilt the distance
table from the coordinates, reproduced the nearest-neighbour tour from
city 1 exactly (length 511) and the all-starts nearest-neighbour range
(482 to 563), and confirmed the staged 2-opt tours for the primary
protocol (435) and the best start (429) as valid permutations whose
lengths recompute to the stated values and which admit no improving
segment reversal, testing improvement by the edge-exchange delta rather
than by full tour recomputation. It also confirmed that no city pair's
distance is affected by the choice between the TSPLIB rounding rule and
ordinary rounding, so the distance table is not sensitive to that
convention on this instance.
