# Pricing the Reserve

**Pricing the Reserve: Market Equilibrium, Lender Safety and Liquidity in an Uncollateralized On-Chain
Lending Pool.** Working paper, prepared for the Journal of Financial Intermediation.

- [paper.pdf](paper.pdf): the compiled paper.
- [JOURNALS.md](JOURNALS.md): the paper's discipline, three candidate journals, and what is out of scope.
- `paper.tex`, `references.bib`, `figures/`: the sources. The figures are pgfplots.
- `data/`: every table and curve, written by `scripts/equilibrium.py`.
- `scripts/`: `equilibrium.py` (all computations), `robustness_table.py`, `run_all.sh`.

## Results

| In the paper | Statement |
| --- | --- |
| Lemma 1 | Lenders' cumulative return equals interest net of the fee, less losses, less the reserve's final balance; the long-run return is u[a(1-f) - max(EL, a r)] for independent years |
| Proposition 1 | The loan rate is the funding rate, the idle-cash drag, the lenders' margin and max(EL, a r), each scaled by utilisation and the share lenders keep; the floor is flat up to the share that covers expected loss and convex beyond |
| Proposition 2 | The market has a unique equilibrium; the rate rises and volume falls with the reserve share |
| Proposition 3 | Incidence: borrowers bear the share eps/(eta+eps) of the cost of the reserve through the rate |
| Lemma 2, Proposition 4 | With safety-first lenders, the volume-maximising share has a reserve inflow of at least expected loss; a first-order condition; a seed raises volume at every share |
| Proposition 5 | A run on a pool of 30-day loans is paid within one loan term; the utilisation allowed by a liquidity target |
| Proposition 6 | Earned credit grows at r a a year |
| Section 9 | For a 5% book at 800 bps, volume is within 1% of its maximum for shares of 41.2 to 50.2%; seed capital of 1% of deposits replaces three points of share at less than half the cost; the best share is about four to six points above the share that covers expected loss in each of three books |

The elasticities and tolerances are scenarios, not estimates.

## Build and reproduce

```bash
make                                              # latexmk -pdf paper.tex
sh scripts/run_all.sh <path to microcredit-contract>   # about 80 s; commit b725a85 of the contract repository
```

The scripts are deterministic: every draw uses a fixed seed, and two consecutive runs give identical files.
They need Python 3 with numpy and scipy, and import the loss model from `analysis/credit_risk` of the
contract repository.

## Contributing

Estimate the demand for loans and the supply of deposits from the flows of a pool (this pool's, or Aave's
or Compound's), check a proof, or propose a better treatment of lenders' tolerance for loss. Open an issue in
this repository and name the result. Contributions are credited in the paper.
