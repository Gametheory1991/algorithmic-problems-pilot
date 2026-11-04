"""
Problem 6: Multi-armed bandits - regret race on synthetic arms
Clearance-safe: fully synthetic Bernoulli arms. No external data of any
kind. All seeds are declared below, before the run.

Registered question (PILOT.md, fixed before the run):
  UCB1 vs Thompson Sampling vs epsilon-greedy: which has lowest
  cumulative regret on synthetic Bernoulli arms, including a
  non-stationary variant?
Registered verifier (fixed before the run):
  Fully synthetic, seeded; regret computed against the known true best
  arm (known by construction).

Conventions (fixed before the run):
  - Arms. K = 10 Bernoulli arms. In the stationary scenario the true
    means are mu[i] = 0.05 + 0.10 * i for i = 0..9, so the best arm is
    arm 9 with mean 0.95 and every other arm is exactly 0.10 or more
    below it per step of index. In the non-stationary scenario the
    means are the same for the first half of the horizon and are then
    reversed (mu[i] becomes mu[K - 1 - i]) at step T // 2, so the best
    arm becomes arm 0 with the same mean 0.95. The reversal is abrupt
    and is not signalled to any algorithm.
  - Horizon and replications. T = 5,000 pulls per replication,
    R = 100 independent replications per algorithm per scenario. The
    seed for a replication is
        20261104 + 100000 * scenario_index + 10000 * algorithm_index
                 + replication
    with scenario_index 0 = stationary, 1 = non-stationary and
    algorithm_index 0 = UCB1, 1 = Thompson Sampling, 2 = epsilon-greedy.
    Each replication uses its own random.Random stream.
  - Common start. Every algorithm pulls each arm once, in arm order,
    during the first K steps; those pulls count toward the horizon and
    toward regret.
  - Algorithms.
      UCB1: after the common start, pull the arm maximising
        (empirical mean) + sqrt(2 * ln(t) / n_arm),
        where t is the number of pulls made so far. Ties go to the
        lowest arm index.
      Thompson Sampling: Beta(1, 1) prior per arm; after the common
        start, sample one value from each arm's posterior
        Beta(1 + successes, 1 + failures) and pull the arm with the
        largest sample. Ties go to the lowest arm index (a tie has
        probability zero in exact arithmetic).
      Epsilon-greedy: epsilon = 0.10 fixed. After the common start, at
        each step draw u ~ Uniform(0, 1); if u < epsilon pull an arm
        chosen uniformly at random, otherwise pull the arm with the
        largest empirical mean, ties to the lowest arm index.
  - Regret. The reported regret is the cumulative pseudo-regret: the
    sum over steps of (current best true mean) - (true mean of the arm
    pulled). It is computed from the known true means, never from the
    realised rewards, so it carries no reward noise; the only variation
    across replications is in the algorithms' choices. The mean and the
    standard error of the final cumulative pseudo-regret across the
    R = 100 replications are reported per algorithm per scenario.
  - Verdict rule. An algorithm "wins" a scenario if its mean final
    cumulative pseudo-regret is the lowest of the three. Because the
    arms, the horizon, the seeds, and the regret definition are all
    fixed by construction, the verifier passes if the computation runs
    as registered and every reported regret is recomputed from the
    known means; the cross-check (a second, independently written
    implementation with different seeds) must reproduce the same
    winner in each scenario and mean regrets agreeing within three
    combined standard errors.
"""
import json
import math
import random

K = 10
T = 5_000
R = 100
SEED_BASE = 20261104
EPSILON = 0.10

MEANS = [0.05 + 0.10 * i for i in range(K)]
MEANS_REVERSED = MEANS[::-1]


def run_replication(algo_index, scenario_index, rep):
    rng = random.Random(
        SEED_BASE + 100_000 * scenario_index + 10_000 * algo_index + rep
    )
    counts = [0] * K
    successes = [0] * K
    regret = 0.0

    def current_means(step):
        if scenario_index == 1 and step >= T // 2:
            return MEANS_REVERSED
        return MEANS

    def pull(arm, step):
        nonlocal regret
        means = current_means(step)
        regret += max(means) - means[arm]
        if rng.random() < means[arm]:
            successes[arm] += 1
        counts[arm] += 1

    # Common start: one pull of each arm, in order.
    for arm in range(K):
        pull(arm, sum(counts))

    for step in range(K, T):
        means_now = current_means(step)
        if algo_index == 0:  # UCB1
            t = step  # pulls made so far
            best_arm, best_val = 0, -1.0
            for a in range(K):
                val = successes[a] / counts[a] + math.sqrt(
                    2.0 * math.log(t) / counts[a]
                )
                if val > best_val:
                    best_val, best_arm = val, a
            pull(best_arm, step)
        elif algo_index == 1:  # Thompson Sampling
            best_arm, best_val = 0, -1.0
            for a in range(K):
                val = rng.betavariate(
                    1 + successes[a], 1 + counts[a] - successes[a]
                )
                if val > best_val:
                    best_val, best_arm = val, a
            pull(best_arm, step)
        else:  # epsilon-greedy
            if rng.random() < EPSILON:
                pull(rng.randrange(K), step)
            else:
                best_arm, best_val = 0, -1.0
                for a in range(K):
                    val = successes[a] / counts[a]
                    if val > best_val:
                        best_val, best_arm = val, a
                pull(best_arm, step)
    return regret


def main():
    algo_names = ["UCB1", "Thompson Sampling", "epsilon-greedy (epsilon=0.1)"]
    scenario_names = ["stationary", "non-stationary (means reversed at T/2)"]
    results = []
    for s in range(2):
        for a in range(3):
            regrets = [run_replication(a, s, r) for r in range(R)]
            mean = sum(regrets) / R
            var = sum((x - mean) ** 2 for x in regrets) / (R - 1)
            se = math.sqrt(var / R)
            results.append(
                {
                    "scenario": scenario_names[s],
                    "algorithm": algo_names[a],
                    "mean_cumulative_pseudo_regret": mean,
                    "standard_error": se,
                    "min_replication_regret": min(regrets),
                    "max_replication_regret": max(regrets),
                }
            )
            print(
                f"{scenario_names[s]:45s} {algo_names[a]:32s} "
                f"mean regret {mean:9.2f}  (SE {se:6.2f})"
            )
    winners = {}
    for s in range(2):
        scen = [r for r in results if r["scenario"] == scenario_names[s]]
        winners[scenario_names[s]] = min(
            scen, key=lambda r: r["mean_cumulative_pseudo_regret"]
        )["algorithm"]
    out = {
        "problem": 6,
        "title": "Multi-armed bandits - regret race on synthetic arms",
        "verifier": "fully synthetic seeded Bernoulli arms; cumulative pseudo-regret computed against the known true best arm at each step (means known by construction); T=5000 pulls, R=100 replications per algorithm per scenario; seeds 20261104 + 100000*scenario + 10000*algorithm + replication",
        "arms_true_means_stationary": MEANS,
        "horizon_T": T,
        "replications_R": R,
        "results": results,
        "winners": winners,
        "verdict": (
            f"In the stationary scenario the lowest mean cumulative "
            f"pseudo-regret is {winners[scenario_names[0]]}; in the "
            f"non-stationary scenario it is {winners[scenario_names[1]]}. "
            f"Figures are in results."
        ),
    }
    with open("result.json", "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(json.dumps(winners, indent=2))


if __name__ == "__main__":
    main()
