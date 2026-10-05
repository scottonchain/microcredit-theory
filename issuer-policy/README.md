# Credit Lines for Pseudonymous Borrowers

**Credit Lines for Pseudonymous Borrowers: Identity-Gated Bayesian Lending under an On-Chain Issuance
Budget.** Working paper, prepared for the European Journal of Operational Research.

- [paper.pdf](paper.pdf): the compiled paper.
- [JOURNALS.md](JOURNALS.md): the paper's discipline, three target journals, and what is out of scope.
- `paper.tex`, `references.bib`, `figures/`: the sources. The figures are pgfplots.
- `data/`: every table and curve, extracted from the contract repository's issuer-policy experiments.
- `scripts/extract_issuer_policy.py`: the extraction.

## Results

| In the paper | Statement |
| --- | --- |
| Lemma 1 | The loss an account can cause over its lifetime is at most its highest line plus its dues |
| Proposition 1 | With tier caps no larger than the cost of an identity, buying identities is unprofitable whatever the history |
| Proposition 2 | Under exponential demand, expected profit is concave in the line and maximised at μ·ln(i/p) |
| Proposition 3 | Greedy allocation within the budget and the per-report cap is optimal (a laminar matroid) |
| Lemma 2 | A release front-run cannot make a correctly planned report revert |
| Section 7 | 925 reports accepted; calibration in every decile; attackers lose in every tier at the true identity cost |

## Build and reproduce

```bash
make                                                                      # latexmk -pdf paper.tex
python3 analysis/issuer_policy/run.py                                     # in the contract repository, about 35 s
python3 scripts/extract_issuer_policy.py <path to microcredit-contract>   # commit b725a85
```

## Contributing

Measure the price of identities in a real proof-of-personhood or KYC market, compare the policy with a
standard scoring model on the same data, or extend the allocation to several issuers sharing one
budget. Open an issue in this repository and name the result. Contributions are credited in the paper.
