# Problem 10 — Exact SAT counting: how a DPLL counter scales against brute force

## Claim registered before the run

A claim circulated with the October 26 OpenAI/math additions holds
that a deterministic subexponential-time exact counter exists for
fixed-width CNF formulas. This problem does not test that claim
directly — it tests the miniature version of the question behind it:
on small random 3-SAT instances, how does the runtime of a plain exact
counter (DPLL with unit propagation) actually scale as instances grow,
compared with brute-force enumeration? The verification method was
registered at the same time: the DPLL counter's model counts are
cross-checked by brute-force enumeration on every instance, and the
verifier passes only if the counts agree everywhere. Runtime figures
are measurements, reported as such.

## Method

- Instances. Random 3-SAT at the phase-transition density:
  m = round(4.26 n) clauses for n in {8, 10, 12, 14, 16, 18, 20, 22,
  24}; each clause has three distinct variables chosen uniformly and
  signs chosen uniformly. Twenty instances per size, 180 in total,
  generated from seeds fixed by formula in the run code (base
  20261104).
- Brute force. All 2^n assignments are evaluated against all clauses.
  The evaluation is bit-parallel (numpy boolean arrays spanning the
  whole assignment space), but it is a complete enumeration: every
  assignment is tested and none is pruned or sampled.
- DPLL counter. A plain recursive exact model counter: unit
  propagation to a fixed point (an empty clause contributes 0; an
  empty formula contributes 2 raised to the number of unassigned
  variables), then branching on the first literal of the first
  remaining clause and summing both branches. No clause learning, no
  component caching, no memoisation.
- Timing. Wall-clock seconds per counting call (generation excluded),
  median over the 20 instances at each size. Scaling is summarised by
  the slope of a least-squares fit of log(median time) against n,
  expressed as an effective multiplicative factor per added variable.
- The computation was run on 4 November 2026 on this machine. No
  external data of any kind was used.

## Result

The counts agree on all 180 instances. Median times:

| n | Clauses | Brute force (s) | DPLL (s) | DPLL / brute force |
|---|---|---|---|---|
| 8 | 34 | 0.0003 | 0.0002 | 0.84 |
| 10 | 43 | 0.0004 | 0.0003 | 0.87 |
| 12 | 51 | 0.0005 | 0.0005 | 0.99 |
| 14 | 60 | 0.0008 | 0.0006 | 0.75 |
| 16 | 68 | 0.0032 | 0.0009 | 0.30 |
| 18 | 77 | 0.0223 | 0.0015 | 0.07 |
| 20 | 85 | 0.1007 | 0.0020 | 0.02 |
| 22 | 94 | 0.7344 | 0.0027 | 0.004 |
| 24 | 102 | 4.1322 | 0.0040 | 0.001 |

Over this range the median brute-force time grows by an effective
factor of 1.87 per added variable — the expected doubling, diluted at
the small sizes by fixed overheads — while the median DPLL time grows
by an effective factor of 1.20 per added variable. At n = 24 the
median DPLL count takes 4 milliseconds against 4.13 seconds for
complete enumeration, a factor of about one thousand. The reason is
visible in the counts themselves: at the phase-transition density most
instances have very few satisfying assignments (the 20 instances at
n = 24 have 306 models in total), and unit propagation prunes the
search tree hard once a few variables are set, so the counter visits a
number of nodes far below 2^n. On these sizes, then, a plain exact
counter already displays the qualitative behaviour the subexponential
claim formalises — runtime growing far more slowly than the full
assignment space — although, as the Limits section states, small-size
measurements cannot establish an asymptotic rate.

## Limits

First, n ≤ 24 is miniature. The fitted factor of 1.20 per variable is
a description of these nine sizes on this machine, not an asymptotic
claim: at larger n the hardest phase-transition instances develop
search trees that unit propagation alone prunes much less effectively,
and a counter without clause learning or caching would slow markedly.
Nothing here supports or refutes the subexponential claim for
fixed-width CNF in general; it documents the small-instance behaviour
that motivates it.

Second, the instances are random at one density (4.26). Structured
instances — crafted formulas, industrial benchmarks, or densities far
from the transition — have different counting difficulty, and the
DPLL/brute-force gap would differ.

Third, the brute-force timings include the bit-parallel evaluation's
fixed setup, which is why the fitted brute-force factor (1.87) sits
below the exact factor of 2 that pure enumeration must approach as n
grows. The comparison of medians at each size, rather than the fitted
factors, is the primary measurement.

## Files

- `run_sat_counting.py` — the complete computation. Run it from this
  directory; it prints the per-size table and writes `result.json` in
  this directory. It requires numpy (used only for the brute-force
  enumeration).
- `result.json` — the machine-readable result: the parameters, the
  per-size median times and ratios, the model count of every instance
  (so any count can be rechecked without rerunning the timers), and
  the fitted scaling factors.

## Reproducibility note

The figures in this document were produced by the registered run on
4 November 2026 and were then recomputed by a second, independently
written implementation. The second implementation (i) recounted every
instance with a differently structured DPLL counter that branches on
the most frequently occurring variable instead of the first literal,
and reproduced all 180 staged model counts exactly; and (ii) recounted
by direct enumeration over itertools.product — a separate, non-vectorised
brute force — for every instance with n ≤ 14 and the first five
instances at n = 16, again agreeing with every staged count. The
timing figures are from the staged run only and will vary by machine;
the counts are exact and machine-independent.
