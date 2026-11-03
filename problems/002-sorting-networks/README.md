# Problem 2 — Sorting networks: whether any comparator can be removed

## Claim registered before the run

A sorting network is a fixed sequence of comparators. Each comparator is tied to
an ordered pair of wires and swaps the values on those two wires when they are
out of order. The network registered for this problem is the standard network
for 8 inputs with 19 comparators, produced by Batcher's odd-even mergesort
construction. The registered question was: is every one of the 19 comparators
necessary, in the sense that removing any single comparator leaves a network
that no longer sorts every input?

The verification method was registered at the same time. By the zero-one
principle, a comparator network sorts every possible input if and only if it
sorts every binary input, so the check is exhaustive over all 256 binary
inputs of length 8. The full network and each of the 19 networks formed by
removing exactly one comparator were each tested on all 256 binary inputs.
A comparator is counted as necessary when at least one binary input fails
after its removal, and the smallest such input, in the enumeration order
defined below, is recorded as the counterexample.

## Method

- Inputs: 8 wires, numbered 0 to 7. A binary input is written as an
  8-character string b0 b1 ... b7, where bi is the value on wire i.
- Enumeration: inputs were tested in increasing order of the integer whose
  binary representation is the input string, with wire 0 as the most
  significant bit. The counterexample recorded for each removal is the first
  failing input in this order.
- Comparators, in the order the network applies them: (0, 1), (2, 3), (0, 2),
  (1, 3), (1, 2), (4, 5), (6, 7), (4, 6), (5, 7), (5, 6), (0, 4), (2, 6),
  (2, 4), (1, 5), (3, 7), (3, 5), (1, 2), (3, 4), (5, 6). Comparators 1 to 5
  sort the first four wires, comparators 6 to 10 sort the last four wires,
  and comparators 11 to 19 merge the two sorted halves.
- An output is counted as sorted when it is non-decreasing from wire 0 to
  wire 7.
- Sample: the check is exhaustive, not sampled. Twenty networks (the full
  network and 19 single-comparator removals) were each tested on all 256
  binary inputs, which is 5,120 cases in total.
- The computation was run on 2 November 2026. No external data of any kind
  was used: the only inputs are the 256 binary strings, which the verifier
  enumerates itself.

## Result

The full 19-comparator network sorted all 256 binary inputs, with 0 failing
inputs, which confirms that it is a sorting network for 8 inputs.

Every single-comparator removal failed. Each of the 19 comparators is
therefore necessary: removing any one of them leaves a network that does not
sort all inputs. Across the 19 removals, 620 of the 4,864 removal cases
failed, which is 12.7 percent. The full result for each removal is as
follows, with the failing count stated out of 256 inputs tested.

| Comparator removed | Wires | Failing inputs of 256 | Smallest counterexample | Output on that input |
|---|---|---|---|---|
| 1 | (0, 1) | 16 | 10000000 | 00000010 |
| 2 | (2, 3) | 16 | 00100000 | 00000010 |
| 3 | (0, 2) | 22 | 11000000 | 00001001 |
| 4 | (1, 3) | 22 | 01000000 | 00000010 |
| 5 | (1, 2) | 32 | 01010001 | 00001011 |
| 6 | (4, 5) | 16 | 00001000 | 00000010 |
| 7 | (6, 7) | 16 | 00000010 | 00000010 |
| 8 | (4, 6) | 22 | 00001100 | 00001001 |
| 9 | (5, 7) | 22 | 00000100 | 00000010 |
| 10 | (5, 6) | 32 | 00010101 | 00001011 |
| 11 | (0, 4) | 15 | 11110000 | 10000111 |
| 12 | (2, 6) | 55 | 00110000 | 00001001 |
| 13 | (2, 4) | 100 | 00110011 | 00100111 |
| 14 | (1, 5) | 55 | 01110000 | 00100011 |
| 15 | (3, 7) | 15 | 00010000 | 00000010 |
| 16 | (3, 5) | 100 | 00010001 | 00001001 |
| 17 | (1, 2) | 16 | 01110111 | 01011111 |
| 18 | (3, 4) | 32 | 00010111 | 00010111 |
| 19 | (5, 6) | 16 | 00010001 | 00000101 |

The two removals that damage the network most are comparators 13 and 16,
which are the comparators (2, 4) and (3, 5) in the final merge stage. Each
leaves 100 of 256 inputs unsorted, which is 39.1 percent of all inputs. The
two removals that damage it least are comparators 11 and 15, which are
(0, 4) and (3, 7), each leaving 15 of 256 inputs unsorted, which is
5.9 percent. No removal leaves the network intact, so the answer to the
registered question is complete: all 19 comparators are necessary, and no
comparator can be removed from this network.

## Limits

This result is a statement about the single network named above, tested
under the registered verifier. Three limits apply.

First, the registered verifier tests single-comparator removals only. The
run makes no claim about networks formed by removing two or more
comparators, and no such networks were tested.

Second, the result shows that every comparator in this network is
necessary. It does not compare this network with other 8-input networks,
and it does not test whether a different arrangement of 19 comparators, or
of fewer comparators, sorts 8 inputs. The known result in the literature
that 19 comparators is the smallest possible size for an 8-input sorting
network is consistent with this outcome, but it is not what this run
tested, and this run neither confirms nor revises it.

Third, the completeness of the check rests on the zero-one principle, which
is the basis the verifier was registered with: for comparator networks,
sorting all 256 binary inputs is equivalent to sorting all inputs. The run
tested exactly those 256 inputs for each network, with no sampling and no
approximation, so within that basis the figures above are exact.

## Files

- `run_sorting_network.py` — the complete computation. Run it from this
  directory; it prints the full result and writes `result.json` in this
  directory.
- `result.json` — the machine-readable result: the comparator list, the
  full-network check, and for each removal the failing count, the smallest
  counterexample, and the output the reduced network produces on it.

## Reproducibility note

The figures in this document were produced by the registered run on
2 November 2026 and were then recomputed by a second, independently written
implementation of the same verifier. The two implementations agree on all
20 checks: the full-network result and, for each of the 19 removals, the
failing count and the smallest counterexample. During the same session the
host intermittently refused file writes, so the result file was written
through repeated attempts and was accepted only when its contents read back
exactly; no figure in this document comes from a file that failed that
check.
