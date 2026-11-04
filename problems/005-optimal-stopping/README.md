# Problem 5 — Optimal stopping: the exact threshold for the secretary problem

## Claim registered before the run

In the classic secretary problem, n candidates arrive one at a time in
uniformly random order. Only the relative rank of each candidate among
those seen so far is observed. Each candidate must be hired or passed on
immediately and permanently, and the payoff is 1 if the single best of all
n candidates is hired and 0 otherwise. The registered question was: what
is the exact optimal threshold policy at n = 10, 50, and 100? The
verification method was registered at the same time: the exact dynamic
programming value against a Monte Carlo simulation of 200,000 trials with
a fixed seed, the two required to agree within simulation error. Agreement
was fixed before the run as an absolute difference of at most three
standard errors, the standard error being computed from the exact value.

## Method

- Dynamic program. Let W(i) be the optimal probability of eventual
  success standing before candidate i, with no candidate yet hired.
  Candidate i is the best seen so far with probability 1 / i; if it is,
  hiring it wins with probability i / n, while passing returns W(i + 1).
  A candidate who is not the best seen so far cannot be the best overall
  and is always passed. The recursion is therefore
  W(i) = (1/i) × max(i/n, W(i+1)) + (1 − 1/i) × W(i+1), with W(n + 1) = 0.
  It was evaluated in exact rational arithmetic, so the values below are
  exact fractions, not approximations. The policy the recursion produces
  was checked to be of threshold form: records are passed before some
  first position s and hired from position s onward.
- Independent exact cross-check. For a policy that observes the first m
  candidates and then hires the first who is the best seen so far, the
  success probability is known in closed form: (m/n) × the sum of
  1/(i − 1) for i from m + 1 to n, for m at least 1, and 1/n for m = 0.
  This expression was maximised over all m in exact rational arithmetic,
  and both the maximum and the maximising m were required to equal the
  dynamic program's value and threshold exactly. They did, at all three
  values of n.
- Monte Carlo. The dynamic-programming-optimal threshold policy was
  played on 200,000 uniformly random permutations per value of n, from a
  single random stream seeded with 20261103, in the order n = 10, 50, 100.
- The computation was run on 3 November 2026. No external data of any kind
  was used.

## Result

| n | Observe first | Hire records from position | Exact probability | Monte Carlo (200,000 trials) | Difference |
|---|---|---|---|---|---|
| 10 | 3 | 4 | 3349/8400 = 0.398690 | 0.397120 (79,424 wins) | 1.43 standard errors |
| 50 | 18 | 19 | 0.374275 | 0.373655 (74,731 wins) | 0.57 standard errors |
| 100 | 37 | 38 | 0.371043 | 0.370345 (74,069 wins) | 0.65 standard errors |

The exact fractions at n = 50 and n = 100 are, respectively,
3221930344783839990101/8608456956238879740000 and
13983373923308456694625973177420433229969/37686689313358095764612869694763407328000;
both are recorded in full in `result.json`. The standard error at each n
is between 0.00108 and 0.00110, so the registered three-standard-error
band is about ±0.0033, and every Monte Carlo frequency falls well inside
it. The verifier therefore passes at all three values of n.

The optimal observation counts — 3 of 10, 18 of 50, and 37 of 100 — are in
each case the integer nearest to n divided by e (3.68, 18.39, and 36.79)
rounded in the direction the exact computation selects, and the success
probabilities approach the limiting value 1/e = 0.367879 from above as n
grows: 0.398690 at n = 10, 0.374275 at n = 50, and 0.371043 at n = 100.
Even under the optimal policy, the best candidate is hired only about
37 to 40 percent of the time; the remaining probability is lost in roughly
equal measure to hiring an early record who is later surpassed and to
passing the best candidate during the observation phase.

## Limits

First, the exact values settle the registered question for the classic
problem as stated: uniformly random arrival order, relative ranks only,
one hire, and a payoff of 1 for the best candidate and 0 otherwise.
Variants — a payoff for the second-best candidate, a cost per interview,
the option to recall a passed candidate, or a known distribution of
candidate quality with cardinal values observed — have different optimal
policies, and nothing here is claimed for them.

Second, the Monte Carlo figures are simulation evidence for the exact
values, not measurements of them. The exact probabilities rest on the
rational-arithmetic dynamic program and its agreement with the closed-form
threshold formula at every n; the simulation's role under the registered
verifier is to confirm that an independent, procedural implementation of
the policy reproduces those values within sampling error, which it does.

Third, the threshold the dynamic program returns is optimal among all
policies, not only among threshold policies: the recursion optimises the
hire-or-pass decision at every position directly. That the resulting
policy is of threshold form is a checked output of the run, stated in the
Method section, not an assumption built into it.

## Files

- `run_optimal_stopping.py` — the complete computation. Run it from this
  directory; it prints the full result and writes `result.json` in this
  directory.
- `result.json` — the machine-readable result: for each n, the optimal
  threshold, the exact probability as a fraction and as a decimal, the
  Monte Carlo win count and frequency, the standard error, and the
  difference in standard errors.

## Reproducibility note

The figures in this document were produced by the registered run on
3 November 2026 and were then recomputed by a second, independently
written implementation. The second implementation evaluated the recursion
in floating point and agreed with the exact values to within 1e-12 at all
three values of n, re-derived each optimal observation count from the
closed-form threshold formula, confirmed the n = 10 fraction 3349/8400
directly from that formula, and ran a separate 200,000-trial simulation
per n with a different seed (777) and a different permutation sampler; its
frequencies (0.39981, 0.37568, and 0.37134) each fall within 1.30 standard
errors of the exact values. The staged simulation's seed is 20261103, as
registered in the run code before the run.
