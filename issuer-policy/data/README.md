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
| `table_objective.tex`, `objective_summary.tex` | The surrogate objective against the cash-flow objective at each tier's prior (Section 5) |
| `misspecification.csv`, `table_misspecification.tex`, `table_misspecification_lines.tex`, `misspecification_summary.tex` | Three scoring rules in five worlds on the policy sample, with pooled cluster-bootstrap intervals (`scripts/misspecification.py`, Section 7) |
| `misspecification_paired.csv`, `table_misspecification_panel.tex` | The same rules on the common panel, and the paired Brier differences between rules on the panel and on the matched policy sample (`scripts/misspecification.py`, Section 7) |

The experiments seed every draw from a fixed base seed, and two consecutive runs gave byte-identical
results; the rerun before this paper differed only in the runtime line of the summary.
