# Data behind the paper

Every table and figure reads a file here, written by `scripts/extract_issuer_policy.py` from
`analysis/issuer_policy/results/*.csv` in the contract repository at commit `b725a85`. Do not edit
them by hand.

| File | Content |
| --- | --- |
| `table_tiers.tex` | Table 1: tiers, identity costs, caps, priors and lines |
| `table_routes.tex` | Table 2: routes to evidence and their weights |
| `table_lines.tex`, `honest_lines.csv` | Table 3 and Figure 1: honest lines by month and true PD |
| `calibration.csv`, `calibration_summary.tex` | Figure 2 and the calibration figures quoted in the text |
| `table_budget.tex` | Table 4: issuer outcomes against the budget |
| `table_attack.tex`, `attacker_curves.csv` | Table 5 and Figure 3: identity buyers by tier |

The experiments seed every draw from a fixed base seed, and two consecutive runs gave byte-identical
results; the rerun before this paper differed only in the runtime line of the summary.
