"""
Problem 2: Sorting networks - can a comparator be removed?
Clearance-safe: no external data at all. The only inputs are all 256 binary
strings of length 8, enumerated by the verifier itself.

Registered question (PILOT.md, fixed before the run):
  Take the known 8-input, 19-comparator network; is every comparator necessary?
Registered verifier (fixed before the run):
  Zero-one principle - exhaustive check over all 256 binary inputs for the
  full network and for each single-comparator removal, with a concrete
  failing input as counterexample.

Network under test: Batcher's odd-even mergesort network for 8 inputs,
generated below by the standard recursive construction (sort each half,
then odd-even merge). The construction must yield exactly 19 comparators;
the generated list is printed verbatim in result.json.

Conventions (fixed before the run):
  - Wires are numbered 0..7. A binary input is written as an 8-character
    string b0 b1 ... b7, where bi is the value on wire i.
  - Inputs are enumerated in increasing order of the integer whose binary
    representation is that string (wire 0 is the most significant bit).
  - The counterexample recorded for a removal is the first failing input
    in that enumeration order.
  - A comparator (i, j), i < j, swaps the values on wires i and j when
    they are out of order (larger value on the lower-numbered wire).
  - An output is sorted when it is non-decreasing from wire 0 to wire 7.
"""
import json


def odd_even_merge(lo, n, r, out):
    step = r * 2
    if step < n:
        odd_even_merge(lo, n, step, out)
        odd_even_merge(lo + r, n, step, out)
        for i in range(lo + r, lo + n - r, step):
            out.append((i, i + r))
    else:
        out.append((lo, lo + r))


def odd_even_merge_sort(lo, n, out):
    if n > 1:
        m = n // 2
        odd_even_merge_sort(lo, m, out)
        odd_even_merge_sort(lo + m, m, out)
        odd_even_merge(lo, n, 1, out)


def batcher_network_8():
    out = []
    odd_even_merge_sort(0, 8, out)
    return out


def apply_network(network, bits):
    x = list(bits)
    for (i, j) in network:
        if x[i] > x[j]:
            x[i], x[j] = x[j], x[i]
    return x


def is_sorted(x):
    return all(x[k] <= x[k + 1] for k in range(len(x) - 1))


def all_binary_inputs():
    # Integer 0..255; wire 0 is the most significant bit.
    for v in range(256):
        yield tuple((v >> (7 - i)) & 1 for i in range(8))


def bits_to_str(bits):
    return "".join(str(b) for b in bits)


def check_network(network):
    """Return (failures, first_failing_input, output_on_first_failure)."""
    failures = 0
    first_in = None
    first_out = None
    for bits in all_binary_inputs():
        out = apply_network(network, bits)
        if not is_sorted(out):
            failures += 1
            if first_in is None:
                first_in = bits
                first_out = out
    return failures, first_in, first_out


def main():
    network = batcher_network_8()
    assert len(network) == 19, f"construction yielded {len(network)} comparators"

    full_failures, full_first_in, _ = check_network(network)
    full_sorts = full_failures == 0

    removals = []
    necessary = 0
    for k in range(len(network)):
        reduced = network[:k] + network[k + 1:]
        failures, first_in, first_out = check_network(reduced)
        is_necessary = failures > 0
        if is_necessary:
            necessary += 1
        removals.append({
            "comparator_number": k + 1,
            "comparator": list(network[k]),
            "necessary": is_necessary,
            "failing_inputs": failures,
            "inputs_tested": 256,
            "smallest_counterexample": bits_to_str(first_in) if first_in else None,
            "output_on_counterexample": bits_to_str(first_out) if first_out else None,
        })

    result = {
        "problem": 2,
        "title": "Sorting networks - can a comparator be removed?",
        "network": {
            "name": "Batcher odd-even mergesort network, 8 inputs",
            "inputs": 8,
            "comparators": [list(c) for c in network],
            "comparator_count": len(network),
        },
        "verifier": ("zero-one principle: exhaustive check over all 256 binary "
                     "inputs for the full network and for each of the 19 "
                     "single-comparator removals"),
        "spec": ("n=8 wires; 19 comparators; 256 binary inputs enumerated with "
                 "wire 0 as most significant bit; counterexample = first "
                 "failing input in that order"),
        "full_network": {
            "inputs_tested": 256,
            "failing_inputs": full_failures,
            "sorts_all_binary_inputs": full_sorts,
        },
        "removals": removals,
        "necessary_count": necessary,
        "comparator_count": len(network),
        "all_comparators_necessary": necessary == len(network),
    }

    print(f"Full network: {full_failures} failing inputs of 256 "
          f"(sorts = {full_sorts})")
    for r in removals:
        print(f"  remove comparator {r['comparator_number']:2d} "
              f"{tuple(r['comparator'])}: failing inputs = "
              f"{r['failing_inputs']:3d}, smallest counterexample = "
              f"{r['smallest_counterexample']}")
    print(f"Necessary comparators: {necessary} of {len(network)}")
    print("RESULT_JSON_BEGIN")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("RESULT_JSON_END")

    try:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=2, sort_keys=True)
    except OSError as e:
        print(f"note: direct result.json write failed ({e}); "
              f"the JSON above on stdout is the canonical copy")


if __name__ == "__main__":
    main()
