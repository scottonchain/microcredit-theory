# One Hop or Many

**One Hop or Many: What Self-Liable Intermediaries Cost a Credit Network.** Working paper, prepared for
Network Science.

- [paper.pdf](paper.pdf): the compiled paper.
- [JOURNALS.md](JOURNALS.md): the paper's discipline, three target journals, and what is out of scope.
- `paper.tex`, `references.bib`, `figures/`: the sources. The figures are TikZ and pgfplots.
- `data/`: every table and curve, extracted from the contract repository's liquidity experiments, plus
  the replication and fixed-cohort runs of `scripts/steady_replicates.py`.
- `scripts/extract_liquidity.py`: the extraction; `scripts/steady_replicates.py`: the replication.

## Results

| In the paper | Statement |
| --- | --- |
| Proposition 1 | If every intermediary can be charged, on its own credit, for what it passes on, the maximum flow into a borrower equals the one-hop value (a debit to credit, not cash solvency) |
| Proposition 2 | Sybil extraction is independent of the number of Sybil accounts and at most the attack edges times the trust per edge; it equals the regime's minimum cut where the regime is an ordinary flow and the length-bounded LP dual for three hops |
| Tables 1 and 2 | One hop serves 28 to 43% of borrowers without credit in the steady state where multi-hop routing serves 83 to 100% (credit spread); between-graph standard deviation at most 0.018 at the base point |
| Table 3 | Raising the share of holders, one hop needs 2.1, 3.1 and 3.8 times the issued credit to reach the two-hop, three-hop and unbounded success rates among the remaining borrowers |
| Fixed-cohort table | With the borrowers and demand fixed and every line and trust line scaled together, one hop reaches 0.80 at four times the credit, below the two-hop rate of 0.83 |
| Table 4 | 40 to 62% of two-hop volume enters the borrower through accounts without credit |
| Table 5 | The same attack edges extract 3.3 to 7 times as much under multi-hop routing |

Revised on 6 October 2026 in response to the internal referee report (issue #6).

## Build and reproduce

Use the [root build and reproduction guide](../#build-and-reproduce) with the selector
`one-hop-liquidity` for the PDF, liquidity experiments, replication and fixed-cohort runs.

## Contributing

Run the regimes on an empirical social graph, prove a bound on one-hop liquidity in terms of degree
and holder share, or propose a routing rule with opt-in relaying. Open an issue in this repository and
name the result. Contributions are credited in the paper.
