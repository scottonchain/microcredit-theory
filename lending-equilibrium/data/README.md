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
| `safety_curve.csv`, `table_safety.tex`, `table_finite_pool.tex`, `table_rsafe.tex` | Figure 4 and the safety tables: lenders' risk of losing principal, finite pools, the smallest safe share |
| `table_seed.tex` | Seed capital against share over a ten-year horizon |
| `equilibrium_curves.csv`, `equilibrium_summary.csv`, `table_eq_curve.tex`, `table_equilibrium.tex` | Figure 5 and the equilibrium tables under the long-run rule |
| `table_plateau_sensitivity.tex` | The plateau on an independent set of paths and on a finer grid |
| `equilibrium_horizon_curves.csv`, `equilibrium_horizon_summary.csv`, `table_equilibrium_horizon.tex` | Figure 5 (dotted) and the equilibrium table under the common-horizon rule |
| `table_robust.tex`, `robust/` | The PD 3% and PD 10% books |
| `liquidity_curve.csv`, `table_liquidity.tex` | Figure 3 and the liquidity table |
| `table_lender.tex` | Lenders' return and earned credit |

The loss model is that of `analysis/credit_risk` in the contract repository at commit `b725a85`. The
seed of every random draw is 20261005, so two runs give byte-identical files.
