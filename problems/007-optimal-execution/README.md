# Problem 7 — Optimal execution: closed form against a grid-searched policy

## Claim registered before the run

In a synthetic Almgren–Chriss market — a price process and an impact
model generated entirely by code, with no real market data — a trader
must liquidate a fixed position over a fixed horizon. A closed-form
trajectory that minimises expected cost plus a variance penalty is
known for this model. The registered question was whether a simple
grid-searched policy — the best member of a one-parameter family of
power-law trajectories — beats that closed-form trajectory on the same
criterion. The verification method was registered at the same time:
100,000 seeded price paths, the same paths for both policies (common
random numbers), with the shortfall computed by direct simulation of
the price recursion.

## Method

- Model. Initial price 100; position X = 1,000,000 shares; N = 10
  intervals of length tau = 0.1. In interval k the trader sells n_k
  shares. The mid-price follows S_k = S_{k-1} + sigma sqrt(tau) xi_k
  − gamma n_k with sigma = 2.0, permanent impact gamma = 2.5e-7, and
  xi_k independent standard normal. The execution price is
  S_{k-1} − eta n_k / tau with temporary impact eta = 5e-7 and no
  fixed per-share cost. The shortfall is C = X·S0 − (proceeds).
- Objective and closed form. Policies are scored by
  J = E[C] + lambda Var(C) with lambda = 1e-6. Algebra on the model
  gives E[C] = (eta/tau) Σ n_k² + (gamma/2)(X² − Σ n_k²) and
  Var(C) = sigma² tau Σ_{j<N} x_j², so J is an explicit quadratic in
  the trades. The closed-form trajectory is its exact minimiser under
  Σ n_k = X, obtained from the Karush–Kuhn–Tucker system; the solution
  is interior (every interval trades, none buys). Its trades, in
  shares per interval, are approximately 250,268; 188,751; 142,722;
  108,403; 82,979; 64,364; 51,030; 41,882; 36,172; 33,429 — a
  front-loaded schedule that sells a quarter of the position in the
  first interval.
- Grid family. Trajectories x(t) = X (1 − t)^alpha at the interval
  boundaries, for alpha in {0.50, 0.75, …, 3.00}; alpha = 1 is the
  linear schedule. The searched policy is the member with the lowest
  simulated J on the registered paths, so the grid is given the
  advantage of selection on the same data it is judged on.
- Simulation. 100,000 paths from one random stream seeded 20261104;
  the identical shock matrix is used for every policy. The verdict
  rule, fixed before the run: the grid policy beats the closed form
  only if its simulated J is lower by more than three batch standard
  errors (100 batches of 1,000 paths).
- The computation was run on 4 November 2026. No external data of any
  kind was used.

## Result

| Policy | Simulated E[C] ($) | Simulated Var(C) | Simulated J ($) |
|---|---|---|---|
| Closed form | 849,520 | 4.979 × 10^11 | 1,347,430 |
| Grid alpha = 1.00 (linear) | 614,605 | 1.139 × 10^12 | 1,753,494 |
| Grid alpha = 2.00 | 775,849 | 6.139 × 10^11 | 1,389,712 |
| Grid alpha = 2.50 (best) | 886,257 | 4.839 × 10^11 | 1,370,177 |
| Grid alpha = 3.00 | 999,901 | 3.919 × 10^11 | 1,391,820 |

The full 11-member grid is recorded in `result.json`. The closed
form's analytic values — E[C] = $847,447, Var = 4.976 × 10^11,
J = $1,345,056 — agree with its simulated values within Monte Carlo
error, as the registered method requires.

The grid-searched policy does not beat the closed-form trajectory.
Its best member (alpha = 2.50) has a simulated J $22,742 higher than
the closed form's, against a batch standard error of $482 — a margin
of about 47 standard errors. The answer to the registered question is
therefore no, and it could not have been otherwise in expectation: the
closed form is the exact minimiser of the stated objective over all
trajectories, and the power family does not contain it. What the run
quantifies is the cost of restricting attention to the simple family:
the best power trajectory's criterion value is only 1.7 percent above
the optimum, because a front-loaded power curve with alpha near 2.5
approximates the closed form's shape well. Note also the trade the
objective makes: the closed form accepts a higher expected cost than
the linear schedule ($849,520 against $614,605) in exchange for less
than half its variance, which the variance penalty rewards at this
lambda.

## Limits

First, the result is about this model and this objective. The closed
form is optimal by construction for the quadratic-impact,
arithmetic-walk model with the stated lambda; a different impact
model (for example transient impact with decay), a different risk
criterion, or intraday volume patterns would change both the closed
form and the gap.

Second, the grid was searched over a single one-parameter family with
11 members, and its best member was selected on the same paths used
for the comparison. That selection biases the grid's simulated J
downward; the common-random-number design and the three-standard-error
rule keep the bias from deciding the verdict here (the margin is about
47 standard errors), but the 1.7 percent figure should be read as a
lower bound on the family's true shortfall.

Third, the simulated figures are Monte Carlo estimates on 100,000
paths. The analytic E[C], Var(C), and J of the closed form are exact
for the model and are the load-bearing numbers; the simulation's role
is to confirm that a procedural implementation of the market reproduces
them, which it does within sampling error.

## Files

- `run_optimal_execution.py` — the complete computation. Run it from
  this directory; it prints the policy table and writes `result.json`
  in this directory.
- `result.json` — the machine-readable result: the model parameters,
  the closed-form trades with their analytic and simulated E[C],
  Var(C), and J, all 11 grid members' simulated figures, the best grid
  alpha, and the J difference with its batch standard error.

## Reproducibility note

The figures in this document were produced by the registered run on
4 November 2026 and were then recomputed by a second, independently
written implementation. The second implementation (i) recomputed the
analytic E[C], Var(C), and J from the linear-in-the-shocks
representation of the shortfall and matched the staged analytic values
to within a relative error of 1e-6; (ii) tested optimality directly —
500 random feasible perturbations of the closed-form trajectory (each
a convex blend with a random Dirichlet allocation) all had analytic J
at least $426 above the closed form's, as an exact minimiser requires;
and (iii) re-ran the simulation in numpy with a different seed (777),
obtaining J = $1,345,476 for the closed form and the same best grid
member (alpha = 2.50, J = $1,368,098), each within 0.5 percent of the
staged simulated values and with the same ordering.
