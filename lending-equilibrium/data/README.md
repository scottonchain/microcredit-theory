# Data behind the paper

Every table and figure reads a file here, written by `scripts/equilibrium.py` (the PD 5% book) and, for
`robust/pd3`, `robust/pd10` and `table_robust.tex`, by the same script with `PD`, `PREMIUM` and `OUTSUB`
set (see `scripts/run_all.sh`). Do not edit them by hand.

| File | Content |
| --- | --- |
| `summary.tex` | The numbers quoted in the text, as macros |
| `table_decomposition.tex` | Table 2: the production rate by reserve share |
| `table_floor.tex`, `floor_curve.csv` | Table 3 and Figure 1: the floor |
| `table_incidence.tex` | Table 4: the incidence formula against numerical derivatives |
| `supply_demand.csv` | Figure 2: demand and supply of loans |
| `safety_curve.csv`, `table_safety.tex`, `table_rsafe.tex` | Figure 4, Tables 6 and 7: lenders' risk of losing principal |
| `table_seed.tex` | Table 8: seed capital against share |
| `equilibrium_curves.csv`, `equilibrium_summary.csv`, `table_eq_curve.tex`, `table_equilibrium.tex` | Figure 5, Tables 9 and 10: the equilibrium |
| `table_robust.tex`, `robust/` | Table 11: the PD 3% and PD 10% books |
| `liquidity_curve.csv`, `table_liquidity.tex` | Figure 3 and Table 5: liquidity |
| `table_lender.tex` | Table 12: lenders' return and earned credit |

The loss model is that of `analysis/credit_risk` in the contract repository at commit `b725a85`. The
seed of every random draw is 20261005, so two runs give byte-identical files.
