# Problem 3 — Scheduling: Smith's rule, and where it breaks

## Claim registered before the run

Smith's rule orders jobs on a single machine by non-decreasing ratio of
processing time to weight, p / w, and is claimed to minimise the weighted sum
of completion times, sum_j w_j * C_j, when all jobs are available at time
zero. The registered question had two parts. First, verify the claim
exhaustively for all small instances. Second, once release dates are added,
find the smallest counterexample. The verification method was registered at
the same time: brute force over all permutations for n ≤ 8.

Two conventions were fixed before the run, because the second part of the
question is not defined without them. The Smith extension tested with
release dates is the static ratio order: jobs run in Smith order, each
starting at the later of the machine's free time and its own release date,
so the machine may idle waiting for the next job in the order. Ties in the
ratio are broken by smaller release date, then smaller processing time,
then smaller weight. For equal ratios any order gives the same objective
value, by the standard adjacent-exchange identity, so the tie-break fixes
only which sequence is reported, never the value.

## Method

Part A, no release dates. Two exhaustive instance sets were checked.

- Set 1: processing times and weights each in {1, 2, 3}, with n from 1 to 6.
- Set 2: processing times and weights each in {1, 2}, with n from 1 to 8.

An instance is a multiset of jobs. The Smith objective and the optimum both
depend only on the multiset, so each multiset was checked once, against
every distinct permutation of its jobs. Set 1 contains 5,004 multisets,
representing 597,870 labelled instances; set 2 contains 494 multisets,
representing 87,380 labelled instances. In total 5,498 multisets,
representing 685,250 labelled instances, were checked. As an independent
second computation of the optimum, subset dynamic programming was run on
every multiset and required to agree with the brute-force optimum.

Part B, release dates added. Instances with n = 1 were checked at value
bound 3 (36 instances; a single job has only one permutation, so no failure
is possible, and none was found). For n = 2 the search ran over value
bounds B = 1, 2, 3, ... in order. At each bound, processing times and
weights range over {1..B} and release dates over {0..B}. An instance is a
pair of job tuples sorted in non-decreasing lexicographic order, and
instances were enumerated in lexicographic order of the flattened tuple
(p1, w1, r1, p2, w2, r2). The first counterexample in that enumeration is
reported; every instance before it was checked and is not a counterexample,
which is the sense in which the reported instance is the smallest. The
computation was run on 3 November 2026. No external data of any kind was
used: every instance is enumerated by the program from the ranges above.

## Result

Part A. Smith's rule matched the brute-force optimum on all 5,498
multisets, in both sets, with no exception. The subset dynamic programming
optimum agreed with the brute-force optimum on every multiset. Within the
registered instance sets, the claim is verified exhaustively: for every
instance with processing times and weights in {1, 2, 3} and at most 6 jobs,
and every instance with processing times and weights in {1, 2} and at most
8 jobs, ordering by Smith's rule attains the minimum weighted sum of
completion times.

Part B. The smallest counterexample in the registered enumeration is the
eighth instance examined (three instances at bound 1, then the fifth at
bound 2). It has two jobs, each of processing time 1:

- Job A: processing time 1, weight 1, release date 0. Ratio 1.
- Job B: processing time 1, weight 2, release date 1. Ratio 1/2.

Smith's rule places job B first, because its ratio is smaller. Job B cannot
start until its release date at time 1, so the machine stands idle from
time 0 to time 1, job B runs from 1 to 2, and job A runs from 2 to 3. The
objective is 2 × 2 + 1 × 3 = 7.

The other order is better. Job A runs from 0 to 1, and job B, released at
time 1, runs from 1 to 2 with no idle time at all. The objective is
1 × 1 + 2 × 2 = 5. The static ratio order therefore exceeds the optimum by
2, on an instance with two jobs and every value equal to 0, 1, or 2. The
failure is caused by the idle time: the ratio order commits the machine to
a job that has not been released while a released job waits.

One further figure is reported for this instance only, as information and
not as a verified claim. A priority variant that never idles while a
released job is waiting, choosing among released jobs by the same ratio
order, runs job A first on this instance and attains the optimum of 5. No
claim about that variant in general is made or tested here.

## Limits

First, Part A is exhaustive over the two registered instance sets only. It
does not test larger values of the processing times and weights at n = 7
or 8, and it does not test n above 8. Smith's rule is in fact a proven
theorem for this problem, so the run's contribution is an exhaustive
small-instance confirmation under the registered verifier, not a new proof.

Second, the Part B counterexample is smallest in the enumeration order
fixed above: fewest jobs, then smallest value bound, then lexicographic
order of the flattened tuple. A different definition of "smallest" could
select a different instance, and the manuscript makes no claim under any
other ordering.

Third, the counterexample concerns the static ratio order defined above.
It shows that this extension of Smith's rule to release dates is not
optimal. It does not show that every scheduling rule that consults the
ratios fails with release dates, and the single-instance priority-variant
figure in the Result section is not evidence about any rule in general.
With release dates the problem is in any case strongly NP-hard, so no
simple ordering rule is expected to be optimal.

## Files

- `run_scheduling.py` — the complete computation. Run it from this
  directory; it prints the full result and writes `result.json` in this
  directory.
- `result.json` — the machine-readable result: the Part A set counts and
  failure lists (both empty), and the Part B counterexample with its Smith
  schedule, its optimal schedule, and the gap.

## Reproducibility note

The figures in this document were produced by the registered run on
3 November 2026 and were then recomputed by a second, independently
written implementation. The second implementation checked Part A with a
separately written subset dynamic program and re-ran the Part B
enumeration from the empty instance upward; it found the same
counterexample, at the same position (eighth examined), with the same
Smith value of 7 and optimum of 5, and it agreed with the brute-force
optimum on all 5,498 Part A multisets. The counterexample's two schedules
were also verified by hand: 2 × 2 + 1 × 3 = 7 for the Smith order, and
1 × 1 + 2 × 2 = 5 for the optimal order.
