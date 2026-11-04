"""
Problem 5: Optimal stopping - prophet / secretary threshold
Clearance-safe: no external data at all. The dynamic program is exact
rational arithmetic; the simulation uses a fixed seed declared below.

Registered question (PILOT.md, fixed before the run):
  What is the exact optimal threshold policy for the classic secretary
  problem at n = 10, 50, 100?
Registered verifier (fixed before the run):
  Exact dynamic programming value vs 200,000-trial Monte Carlo simulation,
  fixed seed - the two must agree within simulation error.

The problem (fixed before the run):
  n candidates arrive one at a time in uniformly random order. Only the
  relative rank of each candidate among those seen so far is observed.
  Each candidate must be hired or passed on immediately and permanently.
  The payoff is 1 if the single best of all n candidates is hired, and 0
  otherwise.

Conventions (fixed before the run):
  - Dynamic program. Let W(i) be the optimal probability of eventual
    success standing before candidate i is interviewed, with no candidate
    yet hired. W(n + 1) = 0. Candidate i is the best seen so far with
    probability 1 / i; if it is, hiring it wins with probability i / n
    (it must also be the best overall), while passing returns W(i + 1).
    A candidate that is not the best seen so far can never be the best
    overall, so it is always passed. Hence
        W(i) = (1/i) * max(i/n, W(i+1)) + (1 - 1/i) * W(i+1).
    The dynamic program is evaluated in exact rational arithmetic
    (fractions.Fraction). The optimal policy it produces is recorded
    position by position, and is checked to be of threshold form: a first
    position s such that records are hired from position s onward and
    passed before s. The threshold is reported as "observe the first
    s - 1 candidates, then hire the first who is the best seen so far".
  - Independent exact cross-check. For a threshold that observes the
    first m candidates (m = s - 1) and then hires the first record, the
    classical formula gives the success probability exactly:
        P = (m / n) * sum_{i=m+1}^{n} 1 / (i - 1)   for m >= 1,
        P = 1 / n                                   for m = 0.
    The maximum of this expression over all m, in exact rational
    arithmetic, must equal the dynamic-programming value exactly, and the
    maximising m must be unique; both are asserted, not assumed.
  - Monte Carlo. 200,000 trials per value of n, one random.Random stream
    seeded with 20261103, trials run in the order n = 10, 50, 100. Each
    trial draws a uniformly random permutation and plays the
    dynamic-programming-optimal threshold policy. "Agree within
    simulation error" is fixed before the run as: the absolute difference
    between the Monte Carlo frequency and the exact value is at most
    three standard errors, where the standard error is
    sqrt(p * (1 - p) / 200000) with p the exact value.
"""
import json
import math
import random
from fractions import Fraction

N_VALUES = [10, 50, 100]
TRIALS = 200_000
SEED = 20261103


def dp_optimal(n):
    """Exact DP. Returns (W(1), list of stop-at-record decisions per
    position, threshold s or None)."""
    W = [Fraction(0)] * (n + 3)  # 1-based; W[n + 1] = 0
    stop = [False] * (n + 2)
    for i in range(n, 0, -1):
        hire_value = Fraction(i, n)
        if hire_value >= W[i + 1]:
            best_next = hire_value
            stop[i] = True
        else:
            best_next = W[i + 1]
        W[i] = Fraction(1, i) * best_next + Fraction(i - 1, i) * W[i + 1]
    threshold = None
    for i in range(1, n + 1):
        if stop[i]:
            threshold = i
            break
    # threshold structure: once stopping is optimal it stays optimal
    if threshold is not None:
        assert all(stop[i] for i in range(threshold, n + 1)), \
            "DP policy is not of threshold form"
        assert all(not stop[i] for i in range(1, threshold)), \
            "DP policy is not of threshold form"
    return W[1], stop, threshold


def threshold_formula(n, m):
    """Exact success probability of 'observe first m, then first record'."""
    if m == 0:
        return Fraction(1, n)
    return Fraction(m, n) * sum(
        (Fraction(1, i - 1) for i in range(m + 1, n + 1)), Fraction(0))


def simulate(n, observe, trials, rng):
    """Play the threshold policy on random permutations; candidates are
    the values 1..n with n the best overall. Returns the win count."""
    wins = 0
    base = list(range(1, n + 1))
    for _ in range(trials):
        perm = base[:]
        rng.shuffle(perm)
        best_seen = 0
        hired = 0
        for idx, val in enumerate(perm):
            if val > best_seen:
                best_seen = val
                if idx >= observe:
                    hired = val
                    break
        if hired == n:
            wins += 1
    return wins


def main():
    rng = random.Random(SEED)
    rows = []
    all_agree = True
    for n in N_VALUES:
        value, _stop, threshold = dp_optimal(n)
        observe = threshold - 1
        # independent exact cross-check over every threshold
        formula_values = {m: threshold_formula(n, m) for m in range(0, n)}
        best_formula = max(formula_values.values())
        argmax = [m for m, v in formula_values.items() if v == best_formula]
        assert best_formula == value, \
            f"n={n}: formula maximum {best_formula} != DP value {value}"
        assert argmax == [observe], \
            f"n={n}: formula argmax {argmax} != DP threshold m={observe}"
        wins = simulate(n, observe, TRIALS, rng)
        freq = wins / TRIALS
        p = float(value)
        se = math.sqrt(p * (1 - p) / TRIALS)
        diff = abs(freq - p)
        agree = diff <= 3 * se
        all_agree = all_agree and agree
        rows.append({
            "n": n,
            "optimal_threshold_first_hire_position": threshold,
            "observe_first": observe,
            "exact_probability_fraction": f"{value.numerator}/{value.denominator}",
            "exact_probability": p,
            "monte_carlo_trials": TRIALS,
            "monte_carlo_wins": wins,
            "monte_carlo_frequency": freq,
            "standard_error": se,
            "absolute_difference": diff,
            "difference_in_standard_errors": diff / se,
            "agrees_within_3_standard_errors": agree,
        })
    result = {
        "problem": 5,
        "title": "Optimal stopping - prophet / secretary threshold",
        "verifier": ("exact dynamic programming value (rational arithmetic) "
                     "vs 200,000-trial Monte Carlo simulation per n, fixed "
                     "seed 20261103; agreement required within three "
                     "standard errors; dynamic-programming value also "
                     "checked exactly against the classical threshold "
                     "formula maximised over all thresholds"),
        "seed": SEED,
        "trials_per_n": TRIALS,
        "results": rows,
        "verdict": (
            "The exact dynamic program gives a threshold policy at each n, "
            "the classical formula maximised over all thresholds reproduces "
            "the dynamic-programming value exactly at the same threshold, "
            "and the Monte Carlo frequency agrees with the exact value "
            "within simulation error at every n."
            if all_agree else
            "VERIFICATION FAILED - Monte Carlo disagrees with the exact "
            "value beyond three standard errors at some n; see results."),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    with open("result.json", "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
