# Problem 6 — Multi-armed bandits: a regret race on synthetic arms

## Claim registered before the run

Ten Bernoulli arms are generated synthetically, so the true mean of
every arm is known by construction. Three algorithms — UCB1, Thompson
Sampling, and epsilon-greedy with epsilon = 0.10 — are run on the arms,
and the registered question was which of them has the lowest cumulative
regret, both when the arm means are fixed and when they change once,
halfway through the run. The verification method was registered at the
same time: the experiment is fully synthetic and seeded, and regret is
computed against the known true best arm, so no part of the answer
depends on estimating the truth from the data the algorithms see.

## Method

- Arms and scenarios. The true means are mu[i] = 0.05 + 0.10 i for
  i = 0..9, so arm 9 is best at 0.95 and each lower arm is 0.10 further
  from the best than its neighbour. In the stationary scenario these
  means hold throughout. In the non-stationary scenario the mean
  vector is reversed at step 2,500 of 5,000, so arm 0 becomes the best
  arm with the same mean 0.95 and arm 9 falls to 0.05. The reversal is
  abrupt and is not signalled to any algorithm.
- Runs. Each algorithm is run for T = 5,000 pulls in R = 100
  independent replications per scenario. Every algorithm begins by
  pulling each arm once, in arm order. UCB1 then maximises the
  empirical mean plus sqrt(2 ln t / n); Thompson Sampling samples each
  arm's Beta posterior (uniform prior) and pulls the largest sample;
  epsilon-greedy pulls a uniformly random arm with probability 0.10
  and otherwise the arm with the largest empirical mean. The seed of
  each replication is fixed by a formula recorded in the run code
  (base 20261104).
- Regret. The reported quantity is cumulative pseudo-regret: at each
  step, the gap between the current best true mean and the true mean
  of the arm pulled, summed over the run. It is computed from the true
  means, so it contains no reward noise; variation across replications
  comes only from the algorithms' choices. Means and standard errors
  across the 100 replications are reported.
- The computation was run on 4 November 2026. No external data of any
  kind was used.

## Result

Stationary scenario (means fixed):

| Algorithm | Mean cumulative pseudo-regret | Standard error | Range across replications |
|---|---|---|---|
| Thompson Sampling | 30.51 | 0.99 | 17.2 – 93.7 |
| Epsilon-greedy (0.10) | 251.36 | 3.91 | 208.8 – 439.8 |
| UCB1 | 285.43 | 2.17 | 230.4 – 365.6 |

Non-stationary scenario (means reversed at step 2,500):

| Algorithm | Mean cumulative pseudo-regret | Standard error | Range across replications |
|---|---|---|---|
| UCB1 | 331.18 | 3.09 | 266.3 – 439.7 |
| Thompson Sampling | 556.09 | 14.06 | 298.2 – 991.9 |
| Epsilon-greedy (0.10) | 1,961.59 | 18.35 | 1,362.2 – 2,252.3 |

With fixed means, Thompson Sampling's regret is an order of magnitude
below the other two: it concentrates on the best arm within a few
hundred pulls and rarely leaves it. After the reversal the ordering
inverts in a specific way. UCB1 adapts fastest, because the confidence
bonus of an arm that has not been pulled for a long time grows without
bound, so the formerly worst arm is retried and its new mean is
learned; its non-stationary regret (331.18) is only slightly above its
stationary regret (285.43). Thompson Sampling adapts more slowly — its
posterior on the old best arm is confident and must be unlearned from
observed failures — and epsilon-greedy adapts slowest of all: it keeps
exploiting the old best arm on 90 percent of steps, while its uniform
exploration gives the new best arm only about 1 percent of steps, so
it spends most of the second half pulling an arm whose mean has fallen
to 0.05. Its mean regret of 1,961.59 is close to the roughly 2,000
that pulling the old best arm for the entire second half would cost.
The registered question therefore has a conditional answer: Thompson
Sampling is the best of the three on stationary arms, and UCB1 is the
best of the three under this single abrupt reversal.

## Limits

First, the arm means are widely spaced (gaps of 0.10) and the best mean
is 0.95, which makes identification easy; with closer means the
stationary gap between Thompson Sampling and UCB1 narrows, and nothing
here is claimed for other mean configurations, other values of
epsilon, or other horizons.

Second, the non-stationary scenario is one specific change: a single
abrupt reversal of the whole mean vector at the midpoint. It is the
change most favourable to a confidence-bonus method, because every
arm's ranking changes at once and stale estimates are wrong in a way
that exploration bonuses directly correct. Gradual drift, or a change
in a single arm, would rank the algorithms differently in general, and
no such case is tested here.

Third, pseudo-regret is computed against the true means. It measures
the quality of the algorithms' choices, not the rewards a user would
have banked; realised-reward regret would add binomial noise of order
sqrt(T) to every figure without changing the ordering at these gaps.

## Files

- `run_bandits.py` — the complete computation. Run it from this
  directory; it prints the per-scenario table and writes `result.json`
  in this directory.
- `result.json` — the machine-readable result: the true means, the
  horizon and replication count, and for each scenario and algorithm
  the mean cumulative pseudo-regret with its standard error and the
  replication range, plus the winner of each scenario.

## Reproducibility note

The figures in this document were produced by the registered run on
4 November 2026 and were then recomputed by a second, independently
written implementation. The second implementation used numpy random
streams with a different seed base (777000), a vectorised form of each
algorithm, and the same registered conventions. It reproduced the same
winner in both scenarios (Thompson Sampling stationary at 27.97, UCB1
non-stationary at 330.13), and every one of the six mean regrets agreed
with the staged figure within three combined standard errors; the
largest difference was Thompson Sampling in the non-stationary
scenario, 595.79 against 556.09, inside a three-standard-error bound
of 61.89. The staged run itself is deterministic: re-running it
reproduces the staged figures exactly.
