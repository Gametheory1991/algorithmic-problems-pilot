"""
Problem 3: Scheduling - Smith's rule, and where it breaks
Clearance-safe: no external data at all. Every instance is enumerated by the
program itself from the value ranges fixed below; there are no inputs other
than those ranges.

Registered question (PILOT.md, fixed before the run):
  Smith's rule (order by ratio) is claimed optimal for minimising weighted
  completion time with no release dates. Verify exhaustively for all small
  instances, then find the smallest counterexample once release dates are
  added.
Registered verifier (fixed before the run):
  Brute force over all permutations for n <= 8.

Conventions (fixed before the run):
  - Single machine, nonpreemptive scheduling. The objective is the weighted
    sum of completion times, sum_j w_j * C_j.
  - A job is a tuple (p, w) in Part A and (p, w, r) in Part B, where p is
    the processing time, w the weight, and r the release date.
  - Smith's rule orders jobs by non-decreasing ratio p / w. Ties are broken
    by smaller release date, then smaller p, then smaller w, then position
    in the instance list. (For equal ratios any order gives the same
    objective value, by the standard adjacent-exchange identity; the
    tie-break only fixes which sequence is reported.)
  - Part A (no release dates; every r = 0). Exhaustive instance sets:
      set 1: p, w in {1, 2, 3}, n = 1..6
      set 2: p, w in {1, 2},    n = 1..8
    An instance is a multiset of jobs. Both the Smith objective and the
    optimum depend only on the multiset, so each multiset is checked once,
    against every distinct permutation of its jobs. The number of labelled
    instances each set represents (value-range size to the power n, summed)
    is reported alongside. As a second, independent check, the optimum is
    also computed by subset dynamic programming and must agree with the
    brute-force optimum on every multiset.
  - Part B (release dates added). The Smith extension tested is the static
    ratio order: jobs run in Smith order, each starting at the later of the
    machine's free time and its own release date, so the machine may idle
    waiting for the next job in the order. The optimum under release dates
    is the minimum over all permutations, each permutation scheduled by the
    same start-time rule. n = 1 is checked over the bound B = 3 (it cannot
    fail: one job has one permutation). For n = 2 the search runs over
    bounds B = 1, 2, 3, ... in order; at each bound, p, w range over
    {1..B} and r over {0..B}; an instance is a pair of job tuples sorted in
    non-decreasing lexicographic order, and instances are enumerated in
    lexicographic order of the flattened tuple (p1, w1, r1, p2, w2, r2).
    The first counterexample in that enumeration is reported; every
    instance before it in the order has been checked and is not a
    counterexample, which is the sense in which it is the smallest.
  - Informational only (outside the registered verifier): for the reported
    counterexample, the run also evaluates a priority variant that never
    idles while a released job waits, choosing among released jobs by the
    same ratio order. This is labelled simulation of one instance, not a
    verified claim about the variant.
"""
import itertools
import json
from fractions import Fraction


def objective_no_release(order):
    """sum_j w_j * C_j for a sequence of (p, w) jobs, all released at 0."""
    t = 0
    total = 0
    for (p, w) in order:
        t += p
        total += w * t
    return total


def objective_with_release(order):
    """sum_j w_j * C_j for a sequence of (p, w, r) jobs; each job starts at
    max(machine free time, r)."""
    t = 0
    total = 0
    for (p, w, r) in order:
        t = max(t, r) + p
        total += w * t
    return total


def schedule_with_release(order):
    """Full schedule detail for a sequence of (p, w, r) jobs."""
    t = 0
    rows = []
    total = 0
    for (p, w, r) in order:
        start = max(t, r)
        end = start + p
        rows.append({"job": [p, w, r], "start": start, "completion": end})
        total += w * end
        t = end
    return rows, total


def smith_order(jobs):
    """Smith's rule: non-decreasing p / w; ties by (r, p, w, index).
    Jobs may be (p, w) or (p, w, r); a missing r counts as 0."""
    def key(item):
        idx, job = item
        p, w = job[0], job[1]
        r = job[2] if len(job) > 2 else 0
        return (Fraction(p, w), r, p, w, idx)
    return [job for (_, job) in sorted(enumerate(jobs), key=key)]


def brute_force_optimum_no_release(jobs):
    """Minimum objective over all distinct permutations of the multiset."""
    best = None
    for perm in set(itertools.permutations(jobs)):
        val = objective_no_release(perm)
        if best is None or val < best:
            best = val
    return best


def dp_optimum_no_release(jobs):
    """Independent optimum by subset dynamic programming:
    f(S) = min over j in S of f(S without j) + w_j * (total p of S)."""
    n = len(jobs)
    total_p = [0] * (1 << n)
    for mask in range(1, 1 << n):
        low = mask & (-mask)
        j = low.bit_length() - 1
        total_p[mask] = total_p[mask ^ low] + jobs[j][0]
    f = [0] * (1 << n)
    for mask in range(1, 1 << n):
        f[mask] = min(
            f[mask ^ (1 << j)] + jobs[j][1] * total_p[mask]
            for j in range(n)
            if mask & (1 << j)
        )
    return f[(1 << n) - 1]


def multisets(job_types, n):
    """All multisets of size n drawn from job_types, as sorted tuples."""
    return itertools.combinations_with_replacement(job_types, n)


def part_a():
    sets = [
        {"name": "set1_p_w_in_1_2_3", "values": (1, 2, 3), "n_max": 6},
        {"name": "set2_p_w_in_1_2", "values": (1, 2), "n_max": 8},
    ]
    out_sets = []
    grand_multisets = 0
    grand_labelled = 0
    grand_checked = 0
    for spec in sets:
        types = [(p, w) for p in spec["values"] for w in spec["values"]]
        set_multisets = 0
        set_labelled = 0
        set_checked = 0
        failures = []
        dp_disagreements = []
        for n in range(1, spec["n_max"] + 1):
            set_labelled += len(types) ** n
            for jobs in multisets(types, n):
                set_multisets += 1
                smith_val = objective_no_release(smith_order(list(jobs)))
                brute_val = brute_force_optimum_no_release(jobs)
                dp_val = dp_optimum_no_release(list(jobs))
                set_checked += 1
                if dp_val != brute_val:
                    dp_disagreements.append(
                        {"jobs": [list(j) for j in jobs],
                         "brute_force": brute_val, "subset_dp": dp_val})
                if smith_val != brute_val:
                    failures.append(
                        {"jobs": [list(j) for j in jobs],
                         "smith": smith_val, "optimal": brute_val})
        out_sets.append({
            "name": spec["name"],
            "values": list(spec["values"]),
            "n_range": [1, spec["n_max"]],
            "multisets_checked": set_multisets,
            "labelled_instances_represented": set_labelled,
            "smith_failures": failures,
            "dp_bruteforce_disagreements": dp_disagreements,
        })
        grand_multisets += set_multisets
        grand_labelled += set_labelled
        grand_checked += set_checked
    return {
        "sets": out_sets,
        "total_multisets_checked": grand_multisets,
        "total_labelled_instances_represented": grand_labelled,
        "smith_optimal_on_all_checked": all(
            not s["smith_failures"] for s in out_sets),
        "dp_agrees_with_brute_force_on_all": all(
            not s["dp_bruteforce_disagreements"] for s in out_sets),
    }


def check_instance_with_release(jobs):
    """Return (smith_value, optimal_value) for a list of (p, w, r) jobs."""
    smith_val = objective_with_release(smith_order(jobs))
    best = None
    for perm in set(itertools.permutations(jobs)):
        val = objective_with_release(perm)
        if best is None or val < best:
            best = val
    return smith_val, best


def part_b():
    # n = 1: check every instance at bound B = 3 (cannot fail, verified anyway)
    n1_checked = 0
    n1_failures = 0
    types_b3 = [(p, w, r) for p in (1, 2, 3) for w in (1, 2, 3)
                for r in (0, 1, 2, 3)]
    for job in types_b3:
        s, o = check_instance_with_release([job])
        n1_checked += 1
        if s != o:
            n1_failures += 1

    # n = 2: smallest counterexample in the fixed enumeration
    examined = 0
    found = None
    bound = 0
    while found is None:
        bound += 1
        types = [(p, w, r) for p in range(1, bound + 1)
                 for w in range(1, bound + 1)
                 for r in range(0, bound + 1)]
        for pair in itertools.combinations_with_replacement(types, 2):
            examined += 1
            s, o = check_instance_with_release(list(pair))
            if s != o:
                found = {"bound": bound, "jobs": [list(j) for j in pair],
                         "smith": s, "optimal": o,
                         "instances_examined_up_to_and_including": examined}
                break

    jobs = [tuple(j) for j in found["jobs"]]
    smith_seq = smith_order(jobs)
    smith_rows, smith_total = schedule_with_release(smith_seq)
    best_perm = None
    best_val = None
    for perm in set(itertools.permutations(jobs)):
        val = objective_with_release(perm)
        if best_val is None or val < best_val:
            best_val = val
            best_perm = perm
    opt_rows, opt_total = schedule_with_release(best_perm)
    assert smith_total == found["smith"] and opt_total == found["optimal"]

    # Informational: priority variant on this instance (never idles while a
    # released job waits; among released jobs picks by Smith key).
    t = 0
    remaining = list(jobs)
    prio_rows = []
    prio_total = 0
    while remaining:
        avail = [j for j in remaining if j[2] <= t]
        if not avail:
            t = min(j[2] for j in remaining)
            avail = [j for j in remaining if j[2] <= t]
        nxt = smith_order(avail)[0]
        start = max(t, nxt[2])
        end = start + nxt[0]
        prio_rows.append({"job": list(nxt), "start": start, "completion": end})
        prio_total += nxt[1] * end
        t = end
        remaining.remove(nxt)

    found["smith_order"] = [list(j) for j in smith_seq]
    found["smith_schedule"] = smith_rows
    found["optimal_order"] = [list(j) for j in best_perm]
    found["optimal_schedule"] = opt_rows
    found["gap"] = found["smith"] - found["optimal"]
    found["priority_variant_on_this_instance"] = {
        "objective": prio_total,
        "schedule": prio_rows,
        "note": "informational only; outside the registered verifier",
    }
    return {
        "n1": {"bound": 3, "instances_checked": n1_checked,
               "failures": n1_failures},
        "n2_smallest_counterexample": found,
    }


def main():
    a = part_a()
    b = part_b()
    result = {
        "problem": 3,
        "title": "Scheduling - Smith's rule, and where it breaks",
        "verifier": ("brute force over all permutations for n <= 8; "
                     "subset dynamic programming as an independent "
                     "cross-check of the optimum"),
        "part_a_no_release_dates": a,
        "part_b_release_dates": b,
        "verdict": (
            "Smith's rule matched the brute-force optimum on every checked "
            "instance without release dates, and the stated n = 2 instance "
            "is the smallest counterexample in the registered enumeration "
            "once release dates are added."
            if a["smith_optimal_on_all_checked"]
            and a["dp_agrees_with_brute_force_on_all"]
            and b["n1"]["failures"] == 0
            else "VERIFICATION FAILED - see failures in this file"),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    with open("result.json", "w") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
