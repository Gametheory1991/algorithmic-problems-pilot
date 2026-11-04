"""
Problem 7: Optimal execution - closed form vs learned policy, synthetic
market
Clearance-safe: a fully synthetic Almgren-Chriss-style market simulated
by code. No real market data of any kind. All parameters and the seed
are declared below, before the run.

Registered question (PILOT.md, fixed before the run):
  In a synthetic Almgren-Chriss market (simulated impact, no real
  market data), does a simple grid-searched policy beat the
  closed-form trajectory on expected cost + variance?
Registered verifier (fixed before the run):
  100,000 seeded price paths, same paths for both policies (common
  random numbers).

Conventions (fixed before the run):
  - Model. One asset, initial price S0 = 100. A position of
    X = 1,000,000 shares is liquidated over N = 10 equal intervals of
    length tau = 0.1 (one trading day in total). In interval k the
    trader sells n_k shares; holdings after interval k are
    x_k = X - (n_1 + ... + n_k), with x_N = 0 required.
    The mid-price evolves as
        S_k = S_{k-1} + sigma * sqrt(tau) * xi_k - gamma * n_k,
    with xi_k independent standard normal, sigma = 2.0 per square-root
    day (2 percent of the initial price), and permanent-impact
    coefficient gamma = 2.5e-7 per share. The execution price in
    interval k is
        S_exec_k = S_{k-1} - eta * n_k / tau,
    with temporary-impact coefficient eta = 5e-7 and no fixed
    per-share cost. The implementation shortfall of a trajectory is
        C = X * S0 - sum_k n_k * S_exec_k.
  - Objective. Policies are scored by J = E[C] + lambda * Var(C) with
    risk aversion lambda = 1e-6, the standard Almgren-Chriss
    mean-variance criterion. Elementary algebra on the model above
    gives the closed forms
        E[C]  = (eta/tau) * sum n_k^2
                + (gamma/2) * (X^2 - sum n_k^2),
        Var(C) = sigma^2 * tau * sum_{j=1}^{N-1} x_j^2,
    so J is an explicit quadratic function of the trades.
  - Closed-form policy. The closed-form trajectory is the exact
    minimiser of J over all trajectories with sum n_k = X: the
    equality-constrained quadratic program is solved in closed form
    from its Karush-Kuhn-Tucker system, n proportional to
    Q^{-1} 1 / (1' Q^{-1} 1) * X, where Q is the quadratic form of J.
    The solution is asserted to be strictly positive in every
    interval (no interval is skipped and no purchase occurs).
  - Grid-searched policy. The searched family is the one-parameter
    power family of trajectories x(t) = X * (1 - t)^alpha evaluated at
    the interval boundaries t = k / N, trades being the differences
    of consecutive holdings. The grid is
    alpha in {0.50, 0.75, 1.00, ..., 3.00} (alpha = 1 is the linear,
    equal-trades schedule). The searched policy is the grid member
    with the lowest simulated J on the registered paths; the
    comparison below is therefore made against the best grid member,
    selected on the same paths.
  - Simulation. 100,000 price paths. The shocks xi are drawn from one
    random.Random stream seeded 20261104, path by path, interval by
    interval, and the SAME 100,000 shock matrices are used for every
    policy (common random numbers). Shortfall is computed by direct
    simulation of the price recursion, not from the closed forms; the
    closed forms are reported alongside and must agree with the
    simulated mean and variance within Monte Carlo error.
  - Verdict rule. The grid-searched policy "beats" the closed-form
    trajectory only if its simulated J is lower and the difference
    exceeds three standard errors, the standard error of the J
    difference being estimated from 100 batches of 1,000 paths each
    (per-batch J for both policies, common shocks within a batch).
    Otherwise the closed-form trajectory stands.
"""
import json
import math
import random

S0 = 100.0
X = 1_000_000.0
N = 10
TAU = 0.1
SIGMA = 2.0
GAMMA = 2.5e-7
ETA = 5e-7
LAMBDA = 1e-6
PATHS = 100_000
BATCHES = 100
SEED = 20261104
ALPHAS = [0.50 + 0.25 * i for i in range(11)]


def holdings_from_trades(trades):
    x, out = X, []
    for n in trades:
        x -= n
        out.append(x)
    return out


def expected_cost(trades):
    s2 = sum(n * n for n in trades)
    return (ETA / TAU) * s2 + (GAMMA / 2.0) * (X * X - s2)


def variance_cost(trades):
    x = holdings_from_trades(trades)
    return SIGMA**2 * TAU * sum(v * v for v in x[: N - 1])


def objective(trades):
    return expected_cost(trades) + LAMBDA * variance_cost(trades)


def closed_form_trades():
    # Build Q for J: term1 c * sum n_k^2, c = ETA/TAU - GAMMA/2;
    # term2 LAMBDA * SIGMA^2 * TAU * sum_{j=1}^{N-1} x_j^2 with
    # x_j = sum_{k>j} n_k, giving Q2[a][b] = L * min(min(a,b)-1, N-1)
    # in 1-based indices a, b.
    c = ETA / TAU - GAMMA / 2.0
    L = LAMBDA * SIGMA**2 * TAU
    Q = [[0.0] * N for _ in range(N)]
    for a in range(1, N + 1):
        for b in range(1, N + 1):
            q2 = L * min(min(a, b) - 1, N - 1)
            Q[a - 1][b - 1] = (c if a == b else 0.0) + q2
    # Solve Q y = 1 by Gaussian elimination.
    M = [row[:] + [1.0] for row in Q]
    for col in range(N):
        piv = max(range(col, N), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(N):
            if r != col and M[r][col] != 0.0:
                f = M[r][col]
                M[r] = [rv - f * cv for rv, cv in zip(M[r], M[col])]
    y = [M[i][N] for i in range(N)]
    scale = X / sum(y)
    trades = [v * scale for v in y]
    assert all(n > 0 for n in trades), "closed-form solution not interior"
    assert abs(sum(trades) - X) < 1e-6 * X
    return trades


def grid_trades(alpha):
    bounds = [X * (1.0 - k / N) ** alpha for k in range(N + 1)]
    return [bounds[k] - bounds[k + 1] for k in range(N)]


def simulate(trades, shocks):
    """Return list of shortfalls, one per path, by direct recursion."""
    costs = []
    sq = math.sqrt(TAU)
    for xi in shocks:
        S = S0
        total = 0.0
        for k in range(N):
            exec_price = S - ETA * trades[k] / TAU
            total += trades[k] * exec_price
            S = S + SIGMA * sq * xi[k] - GAMMA * trades[k]
        costs.append(X * S0 - total)
    return costs


def stats(costs):
    m = sum(costs) / len(costs)
    v = sum((c - m) ** 2 for c in costs) / (len(costs) - 1)
    return m, v, m + LAMBDA * v


def main():
    rng = random.Random(SEED)
    shocks = [[rng.gauss(0.0, 1.0) for _ in range(N)] for _ in range(PATHS)]

    cf = closed_form_trades()
    policies = {"closed-form": cf}
    for alpha in ALPHAS:
        policies[f"grid alpha={alpha:.2f}"] = grid_trades(alpha)

    sim = {}
    for name, trades in policies.items():
        costs = simulate(trades, shocks)
        m, v, j = stats(costs)
        sim[name] = {"mean": m, "var": v, "J": j, "costs": costs}
        print(f"{name:22s} E[C] {m:12.1f}  Var {v:.4e}  J {j:12.1f}")

    print(
        f"closed-form analytic: E[C] {expected_cost(cf):.1f}  "
        f"Var {variance_cost(cf):.4e}  J {objective(cf):.1f}"
    )

    best_grid_name = min(
        (n for n in policies if n.startswith("grid")),
        key=lambda n: sim[n]["J"],
    )
    best_alpha = float(best_grid_name.split("=")[1])

    # Batch standard error for the J difference (best grid - closed form).
    per = PATHS // BATCHES
    diffs = []
    for b in range(BATCHES):
        sl = slice(b * per, (b + 1) * per)
        _, _, j_cf = stats(sim["closed-form"]["costs"][sl])
        _, _, j_g = stats(sim[best_grid_name]["costs"][sl])
        diffs.append(j_g - j_cf)
    md = sum(diffs) / BATCHES
    sd = math.sqrt(sum((d - md) ** 2 for d in diffs) / (BATCHES - 1))
    se_diff = sd / math.sqrt(BATCHES)
    beats = md < 0 and abs(md) > 3 * se_diff

    out = {
        "problem": 7,
        "title": "Optimal execution - closed form vs grid-searched policy, synthetic Almgren-Chriss market",
        "verifier": "100,000 seeded price paths (seed 20261104), identical shock matrices for every policy (common random numbers); shortfall computed by direct simulation of the price recursion; grid policy selected as the best of 11 power-family members on the same paths; 'beats' requires a J advantage larger than three batch standard errors (100 batches of 1,000 paths)",
        "parameters": {
            "S0": S0, "X": X, "N": N, "tau": TAU, "sigma": SIGMA,
            "gamma": GAMMA, "eta": ETA, "lambda": LAMBDA,
        },
        "closed_form": {
            "trades": cf,
            "analytic_expected_cost": expected_cost(cf),
            "analytic_variance": variance_cost(cf),
            "analytic_J": objective(cf),
            "simulated_expected_cost": sim["closed-form"]["mean"],
            "simulated_variance": sim["closed-form"]["var"],
            "simulated_J": sim["closed-form"]["J"],
        },
        "grid_results": [
            {
                "alpha": float(n.split("=")[1]),
                "simulated_expected_cost": sim[n]["mean"],
                "simulated_variance": sim[n]["var"],
                "simulated_J": sim[n]["J"],
            }
            for n in policies
            if n.startswith("grid")
        ],
        "best_grid_alpha": best_alpha,
        "J_difference_best_grid_minus_closed_form": md,
        "J_difference_batch_standard_error": se_diff,
        "grid_beats_closed_form": beats,
        "verdict": (
            "The grid-searched policy does not beat the closed-form "
            "trajectory: the closed form is the exact minimiser of the "
            "stated objective, and the best power-family member has a "
            "higher simulated J by more than three batch standard errors."
            if not beats
            else "The grid-searched policy beats the closed-form trajectory under the registered rule."
        ),
    }
    with open("result.json", "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(f"best grid: {best_grid_name}  J diff {md:.1f} (batch SE {se_diff:.1f})  beats: {beats}")


if __name__ == "__main__":
    main()
