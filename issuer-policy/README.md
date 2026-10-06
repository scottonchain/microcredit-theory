# Credit Lines for Pseudonymous Borrowers

**Credit Lines for Pseudonymous Borrowers: Identity-Gated Bayesian Lending under an On-Chain Issuance
Budget.** Working paper, prepared for the European Journal of Operational Research.

- [paper.pdf](paper.pdf): the compiled paper.
- [JOURNALS.md](JOURNALS.md): the paper's discipline, three target journals, and what is out of scope.
- `paper.tex`, `references.bib`, `figures/`: the sources. The figures are pgfplots.
- `data/`: every table and curve, extracted from the contract repository's issuer-policy experiments,
  plus the misspecification runs of `scripts/misspecification.py`.
- `scripts/extract_issuer_policy.py`: the extraction; `scripts/misspecification.py`: three scoring rules in five worlds.

## Results

| In the paper | Statement |
| --- | --- |
| Lemma 1 | The loss an account can cause over its lifetime is at most its highest line plus its dues |
| Proposition 1 | With tier caps no larger than the cost of an identity, the profit from buying identities, measured against passive lending, is bounded by their cost; the two other channels (the pooled reserve under stress, honest backing) are named and bounded |
| Proposition 2 | Under exponential demand, a first-order surrogate of the pool's expected surplus is concave in the line and maximised at μ·ln(i/p); the cash-flow objective's optimum is lower by μ·ln(1−p), at most 0.29 USDC |
| Proposition 3 | Greedy allocation within the budget and the per-report cap is optimal (a laminar matroid) |
| Lemma 2 | A release front-run cannot make a correctly planned report revert |
| Section 7 | 925 reports accepted; calibration in every decile of the assumed world; attackers lose in every tier at the true identity cost |
| Misspecification tables | On a common panel independent of the lending decision, the repayment evidence improves on the tier prior by a measurable but small amount at a two-year horizon and the weights do not improve on an unweighted rule; every scoring rule is wrong by the same factor when the population or the hazard moves; the weights close the zero-cost routes (farm line 6.10 against 15.00 unweighted) |

Revised on 6 October 2026 in response to the internal referee report (issue #6).

## Build and reproduce

```bash
make                                                                      # latexmk -pdf paper.tex
python3 analysis/issuer_policy/run.py                                     # in the contract repository, about 35 s
python3 scripts/extract_issuer_policy.py <path to microcredit-contract>   # commit b725a85
python3 scripts/misspecification.py <path to microcredit-contract>        # about 25 s
```

## Contributing

Measure the price of identities in a real proof-of-personhood or KYC market, compare the policy with a
standard scoring model on the same data, or extend the allocation to several issuers sharing one
budget. Open an issue in this repository and name the result. Contributions are credited in the paper.
