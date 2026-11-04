"""
Problem 4: Travelling salesman - heuristic gap on a public benchmark
Data: the public TSPLIB instance eil51 (51 cities, Christofides/Eilon),
reproduced verbatim in COORDS below from the TSPLIB file
(NAME: eil51, TYPE: TSP, DIMENSION: 51, EDGE_WEIGHT_TYPE: EUC_2D).
This is public benchmark data; no other data is used.

Registered question (PILOT.md, fixed before the run):
  How close do nearest-neighbour + 2-opt get to the known optimum on the
  public TSPLIB eil51 instance (known optimum 426)?
Registered verifier (fixed before the run):
  Published optimum; tour length recomputed independently, tour validity
  checked (every city once).

Conventions (fixed before the run):
  - Distances follow the TSPLIB EUC_2D rule: the distance between two
    cities is the Euclidean distance rounded to the nearest integer,
    int(sqrt(dx^2 + dy^2) + 0.5). Tour length is the sum of the 51 edge
    distances, including the closing edge back to the first city.
  - Cities are numbered 1 to 51 as in the TSPLIB file.
  - Primary protocol: nearest neighbour starting at city 1. At each step
    the tour moves to the nearest unvisited city; ties are broken by the
    lowest city number. The resulting tour is then improved by 2-opt:
    repeatedly apply the single segment reversal with the largest length
    reduction (best improvement) until no reversal reduces the length.
  - Secondary protocol: the same procedure from every start city, 1 to 51.
    The best, worst, and mean final lengths over the 51 starts are
    reported, so the dependence on the start city is measured rather than
    hidden.
  - Verification: every reported tour is checked to be a permutation of
    the 51 cities (each city exactly once); every reported final tour is
    checked to be 2-opt locally optimal (no segment reversal reduces its
    length); and every reported tour length is recomputed by a second,
    separately written length function before it is accepted. No reported
    length may fall below the published optimum of 426; if one did, that
    would show an error in the distance computation, and the run would
    fail rather than report it.
"""
import json
import math

# TSPLIB eil51 node coordinates, cities 1..51 in file order.
COORDS = [
    (37, 52), (49, 49), (52, 64), (20, 26), (40, 30), (21, 47), (17, 63),
    (31, 62), (52, 33), (51, 21), (42, 41), (31, 32), (5, 25), (12, 42),
    (36, 16), (52, 41), (27, 23), (17, 33), (13, 13), (57, 58), (62, 42),
    (42, 57), (16, 57), (8, 52), (7, 38), (27, 68), (30, 48), (43, 67),
    (58, 48), (58, 27), (37, 69), (38, 46), (46, 10), (61, 33), (62, 63),
    (63, 69), (32, 22), (45, 35), (59, 15), (5, 6), (10, 17), (21, 10),
    (5, 64), (30, 15), (39, 10), (32, 39), (25, 32), (25, 55), (48, 28),
    (56, 37), (30, 40),
]
N = len(COORDS)
PUBLISHED_OPTIMUM = 426


def dist(i, j):
    """TSPLIB EUC_2D distance between 0-based city indices i and j."""
    dx = COORDS[i][0] - COORDS[j][0]
    dy = COORDS[i][1] - COORDS[j][1]
    return int(math.sqrt(dx * dx + dy * dy) + 0.5)


D = [[dist(i, j) for j in range(N)] for i in range(N)]


def tour_length(tour):
    return sum(D[tour[k]][tour[(k + 1) % N]] for k in range(N))


def tour_length_independent(tour):
    """Second length computation: coordinates and rounding redone from
    scratch, edges walked in reverse order."""
    total = 0
    for k in range(N - 1, -1, -1):
        a = COORDS[tour[k]]
        b = COORDS[tour[(k + 1) % N]]
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        total += int(math.hypot(dx, dy) + 0.5)
    return total


def nearest_neighbour(start):
    tour = [start]
    unvisited = set(range(N)) - {start}
    while unvisited:
        cur = tour[-1]
        nxt = min(unvisited, key=lambda c: (D[cur][c], c))
        tour.append(nxt)
        unvisited.remove(nxt)
    return tour


def two_opt(tour):
    """Best-improvement 2-opt until no reversal reduces the length.
    Returns (tour, number of improving reversals applied)."""
    tour = list(tour)
    moves = 0
    while True:
        best_gain = 0
        best_pair = None
        cur_len = tour_length(tour)
        for i in range(N - 1):
            for j in range(i + 2, N):
                if i == 0 and j == N - 1:
                    continue  # reversing the whole tour changes nothing
                cand = tour[:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]
                gain = cur_len - tour_length(cand)
                if gain > best_gain:
                    best_gain = gain
                    best_pair = (i, j)
        if best_pair is None:
            return tour, moves
        i, j = best_pair
        tour = tour[:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]
        moves += 1


def is_two_optimal(tour):
    cur_len = tour_length(tour)
    for i in range(N - 1):
        for j in range(i + 2, N):
            if i == 0 and j == N - 1:
                continue
            cand = tour[:i + 1] + tour[i + 1:j + 1][::-1] + tour[j + 1:]
            if tour_length(cand) < cur_len:
                return False
    return True


def check(tour, length, label):
    assert sorted(tour) == list(range(N)), f"{label}: not a permutation"
    assert tour_length(tour) == length, f"{label}: length mismatch (walk 1)"
    assert tour_length_independent(tour) == length, \
        f"{label}: length mismatch (independent walk)"
    assert length >= PUBLISHED_OPTIMUM, \
        f"{label}: length {length} below published optimum - distance error"


def run_from(start):
    nn = nearest_neighbour(start)
    nn_len = tour_length(nn)
    check(nn, nn_len, f"NN from {start + 1}")
    opt, moves = two_opt(nn)
    opt_len = tour_length(opt)
    check(opt, opt_len, f"2-opt from {start + 1}")
    assert is_two_optimal(opt), f"2-opt from {start + 1}: not locally optimal"
    return {
        "start_city": start + 1,
        "nearest_neighbour_length": nn_len,
        "nearest_neighbour_tour": [c + 1 for c in nn],
        "two_opt_length": opt_len,
        "two_opt_moves": moves,
        "two_opt_tour": [c + 1 for c in opt],
        "two_opt_gap_above_optimum": opt_len - PUBLISHED_OPTIMUM,
        "two_opt_gap_percent": round(
            100.0 * (opt_len - PUBLISHED_OPTIMUM) / PUBLISHED_OPTIMUM, 2),
    }


def main():
    primary = run_from(0)
    all_starts = [run_from(s) for s in range(N)]
    lengths = [r["two_opt_length"] for r in all_starts]
    nn_lengths = [r["nearest_neighbour_length"] for r in all_starts]
    best = min(all_starts, key=lambda r: r["two_opt_length"])
    worst = max(all_starts, key=lambda r: r["two_opt_length"])
    result = {
        "problem": 4,
        "title": "Travelling salesman - heuristic gap on a public benchmark",
        "instance": "TSPLIB eil51 (51 cities, Christofides/Eilon), EUC_2D",
        "verifier": ("published optimum 426; every tour validated as a "
                     "permutation of the 51 cities and its length recomputed "
                     "by a second, separately written length function; every "
                     "final tour checked 2-opt locally optimal"),
        "published_optimum": PUBLISHED_OPTIMUM,
        "primary_protocol_start_city_1": primary,
        "all_starts": {
            "starts_run": N,
            "nearest_neighbour_length_min": min(nn_lengths),
            "nearest_neighbour_length_max": max(nn_lengths),
            "two_opt_length_min": min(lengths),
            "two_opt_length_max": max(lengths),
            "two_opt_length_mean": round(sum(lengths) / N, 2),
            "best_start_city": best["start_city"],
            "best_tour": best["two_opt_tour"],
            "worst_start_city": worst["start_city"],
            "per_start_two_opt_lengths": {
                str(r["start_city"]): r["two_opt_length"] for r in all_starts},
        },
        "verdict": (
            f"Nearest neighbour from city 1 gives {primary['nearest_neighbour_length']}, "
            f"and 2-opt improves it to {primary['two_opt_length']}, which is "
            f"{primary['two_opt_gap_above_optimum']} above the published optimum of 426 "
            f"({primary['two_opt_gap_percent']} percent). Across all 51 start cities, "
            f"2-opt ends between {min(lengths)} and {max(lengths)}."),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    with open("result.json", "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
