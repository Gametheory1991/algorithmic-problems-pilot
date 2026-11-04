"""
Problem 8: Coin systems - when is greedy optimal?
Clearance-safe: pure exact computation on coin systems stated below.
No external data of any kind.

Registered question (PILOT.md, fixed before the run):
  For which coin systems up to value 200 is the greedy change-making
  algorithm optimal?
Registered verifier (fixed before the run):
  Exact dynamic programming for the true minimum number of coins at
  every amount; smallest counterexample amount reported per failing
  system.

Conventions (fixed before the run):
  - Amounts are 1..200 (value 200 in the registered question). Every
    system contains the coin 1, so every amount is representable.
  - Systems examined, fixed in advance:
      (a) the exhaustive family of three-coin systems {1, a, b} with
          2 <= a < b <= 50 (1,176 systems);
      (b) a named list: the United States system {1, 5, 10, 25} and
          with the half dollar {1, 5, 10, 25, 50}; the euro / sterling
          minor-unit system {1, 2, 5, 10, 20, 50}; powers of two
          {1, 2, 4, 8, 16, 32, 64, 128}; {1, 2, 3}; {1, 3, 4};
          {1, 4, 6}; {1, 7, 10}; {1, 10, 25}; {1, 5, 10, 20, 25};
          and the Fibonacci system {1, 2, 3, 5, 8, 13, 21, 34, 55,
          89, 144}.
  - Greedy: repeatedly take the largest coin not exceeding the
    remaining amount.
  - Exact optimum: dynamic programming over amounts 0..200,
    opt[v] = 1 + min over coins c <= v of opt[v - c].
  - A system is "greedy-optimal up to 200" if greedy and optimum agree
    at every amount 1..200. For a failing system the smallest
    counterexample amount is reported, with the greedy and optimal
    coin counts at that amount, together with the number of failing
    amounts in 1..200.
"""
import json

V = 200

NAMED = [
    ("United States {1,5,10,25}", [1, 5, 10, 25]),
    ("United States with half dollar {1,5,10,25,50}", [1, 5, 10, 25, 50]),
    ("Euro / sterling minor units {1,2,5,10,20,50}", [1, 2, 5, 10, 20, 50]),
    ("Powers of two {1,2,4,8,16,32,64,128}", [1, 2, 4, 8, 16, 32, 64, 128]),
    ("{1,2,3}", [1, 2, 3]),
    ("{1,3,4}", [1, 3, 4]),
    ("{1,4,6}", [1, 4, 6]),
    ("{1,7,10}", [1, 7, 10]),
    ("{1,10,25}", [1, 10, 25]),
    ("{1,5,10,20,25}", [1, 5, 10, 20, 25]),
    ("Fibonacci {1,2,3,5,8,13,21,34,55,89,144}", [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]),
]


def greedy_count(coins_desc, v):
    n = 0
    for c in coins_desc:
        q, v = divmod(v, c)
        n += q
    return n


def optimal_table(coins, vmax=V):
    opt = [0] * (vmax + 1)
    for v in range(1, vmax + 1):
        opt[v] = 1 + min(opt[v - c] for c in coins if c <= v)
    return opt


def examine(coins):
    coins_desc = sorted(coins, reverse=True)
    opt = optimal_table(coins)
    failing = []
    for v in range(1, V + 1):
        if greedy_count(coins_desc, v) != opt[v]:
            failing.append(v)
    if not failing:
        return {"coins": coins, "greedy_optimal_up_to_200": True,
                "smallest_counterexample": None}
    s = failing[0]
    return {
        "coins": coins,
        "greedy_optimal_up_to_200": False,
        "smallest_counterexample": s,
        "greedy_coins_at_counterexample": greedy_count(coins_desc, s),
        "optimal_coins_at_counterexample": opt[s],
        "failing_amounts_count": len(failing),
    }


def main():
    named_results = []
    for label, coins in NAMED:
        r = examine(coins)
        r = {"system": label, **r}
        named_results.append(r)
        print(label, "->", "OPTIMAL" if r["greedy_optimal_up_to_200"]
              else f"fails at {r['smallest_counterexample']} "
                   f"(greedy {r['greedy_coins_at_counterexample']} vs "
                   f"optimal {r['optimal_coins_at_counterexample']})")

    sweep = []
    for a in range(2, 51):
        for b in range(a + 1, 51):
            sweep.append(examine([1, a, b]))
    n_systems = len(sweep)
    n_optimal = sum(1 for r in sweep if r["greedy_optimal_up_to_200"])
    failing = [r for r in sweep if not r["greedy_optimal_up_to_200"]]
    # Distribution of smallest counterexamples among failing systems.
    from collections import Counter
    dist = Counter(r["smallest_counterexample"] for r in failing)
    print(f"sweep: {n_optimal} of {n_systems} three-coin systems greedy-optimal up to 200")
    print("smallest-counterexample distribution (amount: #systems), top 10:",
          dist.most_common(10))

    out = {
        "problem": 8,
        "title": "Coin systems - when is greedy optimal?",
        "verifier": "exact dynamic programming for the true minimum number of coins at every amount 1..200; greedy count computed independently by repeated largest-coin division; smallest counterexample amount reported per failing system",
        "max_amount": V,
        "named_systems": named_results,
        "three_coin_sweep": {
            "family": "{1, a, b} with 2 <= a < b <= 50",
            "systems_examined": n_systems,
            "greedy_optimal": n_optimal,
            "greedy_failing": n_systems - n_optimal,
            "smallest_counterexample_distribution_top10": [
                {"amount": amt, "systems": cnt} for amt, cnt in dist.most_common(10)
            ],
            "failing_systems": failing,
        },
        "verdict": (
            f"Of the {n_systems} three-coin systems {{1, a, b}} with "
            f"2 <= a < b <= 50, {n_optimal} are greedy-optimal at every "
            f"amount up to 200 and {n_systems - n_optimal} fail, each "
            f"with the smallest counterexample recorded. Named-system "
            f"results are in named_systems."
        ),
    }
    with open("result.json", "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    main()
