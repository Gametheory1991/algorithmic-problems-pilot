# Problem 8 — Coin systems: when is the greedy algorithm optimal?

## Claim registered before the run

The greedy change-making algorithm — repeatedly take the largest coin
not exceeding the remaining amount — is fast and is optimal for some
coin systems and not for others. The registered question was: for
which coin systems is greedy optimal at every amount up to 200? The
verification method was registered at the same time: exact dynamic
programming for the true minimum number of coins at every amount, with
the smallest counterexample amount reported for every system that
fails.

## Method

- Systems. Two groups, fixed in advance. (a) The exhaustive family of
  three-coin systems {1, a, b} with 2 ≤ a < b ≤ 50 — 1,176 systems.
  (b) A named list: the United States system {1, 5, 10, 25}, the same
  with the half dollar, the euro / sterling minor-unit system
  {1, 2, 5, 10, 20, 50}, powers of two up to 128, {1, 2, 3}, {1, 3, 4},
  {1, 4, 6}, {1, 7, 10}, {1, 10, 25}, {1, 5, 10, 20, 25}, and the
  Fibonacci denominations {1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144}.
  Every system contains the coin 1, so every amount is representable.
- Amounts 1 to 200. For each system, the exact minimum coin count at
  every amount is computed by dynamic programming
  (opt[v] = 1 + min over coins c ≤ v of opt[v − c]), and the greedy
  count is computed independently by repeated largest-coin division. A
  system is greedy-optimal up to 200 if the two agree at every amount;
  otherwise the smallest amount at which they differ is its smallest
  counterexample.
- The computation was run on 4 November 2026. No external data of any
  kind was used.

## Result

Named systems:

| System | Greedy optimal to 200? | Smallest counterexample | Greedy vs optimal there |
|---|---|---|---|
| United States {1, 5, 10, 25} | Yes | — | — |
| United States {1, 5, 10, 25, 50} | Yes | — | — |
| Euro / sterling {1, 2, 5, 10, 20, 50} | Yes | — | — |
| Powers of two {1, 2, 4, 8, 16, 32, 64, 128} | Yes | — | — |
| {1, 2, 3} | Yes | — | — |
| Fibonacci denominations | Yes | — | — |
| {1, 3, 4} | No | 6 | 3 vs 2 (4+1+1 against 3+3) |
| {1, 4, 6} | No | 8 | 3 vs 2 (6+1+1 against 4+4) |
| {1, 7, 10} | No | 14 | 5 vs 2 (10+1+1+1+1 against 7+7) |
| {1, 10, 25} | No | 30 | 6 vs 3 (25+1+1+1+1+1 against 10+10+10) |
| {1, 5, 10, 20, 25} | No | 40 | 3 vs 2 (25+10+5 against 20+20) |

In the exhaustive three-coin sweep, 349 of the 1,176 systems
{1, a, b} with 2 ≤ a < b ≤ 50 are greedy-optimal at every amount up to
200 (29.7 percent); the remaining 827 fail, each with its smallest
counterexample recorded in `result.json`. Two patterns are visible in
the recorded data. First, in 576 of the 827 failing systems (about 70
percent) the smallest counterexample is exactly 2a, twice the middle
coin: at that amount greedy commits to the large coin b (since
a < b < 2a in those systems) and pays the remainder in ones, while two
middle coins are cheaper. Second, the most common smallest
counterexamples across the sweep are the amounts 48 (45 systems), 54
(40), 60 (37), 52 (33), 42 and 56 (31 each) — larger amounts at which a
greedy commitment to several large coins first becomes wasteful. The
full distribution is in `result.json`.

## Limits

First, "optimal up to 200" is exactly that. A system certified here
could in principle fail at some amount above 200, and a system's
status is claimed only for the amounts checked. (For the named real
currency systems, optimality at all amounts is a known theorem; this
run certifies the registered range by direct computation and claims
nothing beyond it.)

Second, the sweep covers three-coin systems with denominations up to
50, plus the named list. Four-coin and larger systems have their own
failure patterns — the named list shows one: {1, 5, 10, 20, 25} fails
at 40 although its three-coin subsystems {1, 5, 25} and {1, 10, 25}
behave differently — and the sweep's percentages do not extend to
them.

Third, the criterion is the number of coins, with unlimited supply of
every denomination. Change-making with a limited till, or an objective
that weights denominations differently, is a different problem.

## Files

- `run_coin_systems.py` — the complete computation. Run it from this
  directory; it prints the named-system table and the sweep summary
  and writes `result.json` in this directory.
- `result.json` — the machine-readable result: every named system's
  status and counterexample detail, and for the sweep the counts, the
  smallest-counterexample distribution, and every failing system's
  coins, smallest counterexample, and greedy and optimal counts there.

## Reproducibility note

The figures in this document were produced by the registered run on
4 November 2026 and were then recomputed by a second, independently
written implementation. The second implementation replaced the dynamic
program with a breadth-first search on the amount graph (each coin an
edge of length equal to its value) and the greedy count with a
recursive formulation. It agreed with the staged result on every
amount of every system: all 11 named systems matched in status and in
counterexample detail, the sweep count of greedy-optimal systems
matched at 349 of 1,176, and none of the 827 recorded smallest
counterexamples differed.
