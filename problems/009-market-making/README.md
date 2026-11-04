# Problem 9 — Market making: the break-even spread under informed flow

## Claim registered before the run

In a Glosten–Milgrom-style market, a market maker who quotes a single
bid and ask faces informed traders who know the asset's value and
uninformed traders who trade at random. The spread must be wide enough
that the profit earned from uninformed flow covers the loss to
informed flow. The registered question was: what spread recovers zero
expected loss — the break-even spread — in a synthetic simulator of
this market in which the informed share is known by construction? The
verification method was registered at the same time: solve the
break-even spread analytically, and check the solution against the
simulation.

## Method

- Model. The true value V is 90 or 110 with equal probability (prior
  mean 100, half-distance delta = 10). A share mu of arriving traders
  are informed: they buy when V = 110 and sell when V = 90. The rest
  buy or sell with equal probability independently of V. The market
  maker quotes bid = 100 − h and ask = 100 + h and trades at the quote
  against every arrival; the full spread is 2h.
- Analytic solution. Buys and sells are equally likely, and
  E[V | buy] = mu · 110 + (1 − mu) · 100 = 100 + mu·delta, so the
  expected profit on a trade at half-spread h is h − mu·delta, and by
  symmetry the same for sells. The zero-expected-profit half-spread is
  therefore h* = mu·delta and the break-even spread is s* = 2·mu·delta.
  At the headline informed share mu = 0.20 the predicted spread is 4.00.
- Simulation. For each mu in {0.05, 0.10, …, 0.50}, 1,000,000 arrivals
  are generated from one stream seeded 20261104. Each arrival
  contributes a signed value term g (−(V − 100) for a buy, +(V − 100)
  for a sell), so profit at half-spread h is exactly h + g per trade
  and the simulated break-even half-spread is −mean(g). The verifier,
  fixed before the run, passes a case if the simulated break-even
  half-spread differs from mu·delta by at most three standard errors
  of the simulated mean.
- The computation was run on 4 November 2026. No external data of any
  kind was used.

## Result

| Informed share mu | Analytic break-even spread | Simulated break-even spread | Difference (standard errors) |
|---|---|---|---|
| 0.05 | 1.00 | 1.0215 | 1.08 |
| 0.10 | 2.00 | 1.9924 | 0.38 |
| 0.15 | 3.00 | 2.9828 | 0.87 |
| 0.20 | 4.00 | 4.0270 | 1.38 |
| 0.25 | 5.00 | 5.0041 | 0.21 |
| 0.30 | 6.00 | 5.9735 | 1.39 |
| 0.35 | 7.00 | 7.0118 | 0.63 |
| 0.40 | 8.00 | 8.0072 | 0.39 |
| 0.45 | 9.00 | 9.0115 | 0.64 |
| 0.50 | 10.00 | 9.9934 | 0.38 |

All ten cases pass the registered check; the largest deviation is
1.39 standard errors. The headline answer: with a fifth of flow
informed and a value that moves 10 either way, the market maker must
quote a spread of 4.00 (bid 98, ask 102) to break even in expectation —
the spread is exactly the informed share times the full value range,
2·mu·delta, because the expected loss per trade is set by how often
the counterparty knows the value and by how far the value sits from
the quote's midpoint. At that spread the market maker earns, in
expectation, 2.00 per uninformed trade and loses 8.00 per informed
trade, and at mu = 0.20 the two flows balance.

## Limits

First, this is the break-even spread for a risk-neutral market maker
with no inventory costs, no operating costs, and no competition, in a
one-shot model where the value is drawn fresh and quotes do not move
with order flow. A sequential Glosten–Milgrom market, in which quotes
are revised as orders arrive and the spread also compensates for
inventory and processing costs, would produce a wider required spread;
nothing here is claimed for it.

Second, the value distribution is two-point and symmetric and the
informed share is constant and known to the analyst (though not used
by the quoting rule beyond the fixed quote). Asymmetric values,
informed traders who sometimes abstain, or an informed share that
varies over time would change the break-even spread; the formula
s* = 2·mu·delta is exact only for the stated construction.

Third, the simulated figures are averages over 1,000,000 arrivals per
case and carry the standard errors reported in `result.json` (about
0.01 on the half-spread). They confirm the analytic value; they do not
estimate it more precisely than the exact solution already states it.

## Files

- `run_market_making.py` — the complete computation. Run it from this
  directory; it prints the per-case table and writes `result.json` in
  this directory.
- `result.json` — the machine-readable result: the model parameters,
  the headline case at mu = 0.20, and for every swept mu the analytic
  and simulated break-even spreads, the standard error, and the
  difference in standard errors.

## Reproducibility note

The figures in this document were produced by the registered run on
4 November 2026 and were then recomputed by a second, independently
written implementation. The second implementation (i) enumerated all
arrival cells (informed or uninformed × value × side) in exact
rational arithmetic and confirmed that the expected signed term is
exactly −mu·delta — hence expected profit exactly zero at h = mu·delta
— for every swept mu; and (ii) re-ran the simulation in numpy with a
different seed (777) at mu = 0.20, 0.35, and 0.50, obtaining break-even
half-spreads of 1.9936, 3.5036, and 5.0143 against the staged 2.0135,
3.5059, and 4.9967, each pair agreeing within three combined standard
errors.
