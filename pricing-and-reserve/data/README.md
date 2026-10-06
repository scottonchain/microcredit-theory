# Data behind the paper

Every table and figure reads a file here. Generated files say so in their first line; do not edit
them by hand.

| File | Produced by | Content |
| --- | --- | --- |
| `reserve_years.csv` | `scripts/locked_reserve.py` | Lenders' mean return, 1st percentile, probability of any loss and mean reserve, by year, for PD 3, 5 and 10%, two reserve shares and two release policies (200,000 paths each) |
| `reserve_sweep.csv` | `scripts/locked_reserve.py` | The locked reserve against the reserve share from 20 to 80%: return in year 30 and over 30 years, the limit of Theorem 2, loss probabilities in years 10 and 30, reserve in year 30 |
| `reserve_summary.tex` | `scripts/locked_reserve.py` | Macros for the reserve shares and long-run returns quoted in the text, including the interim 45% default |
| `event_timed_years.csv`, `table_event_timed.tex`, `table_event_quantile.tex`, `event_summary.tex` | `scripts/event_timed.py` | The event-timed finite-pool check (Section 6.5): pools of 100, 500 and 5,000 loans at the contract's timing, by year, against the annual recursion; the 99.9% annual loss quantile against the replenished quantile plus the granularity adjustment |
| `table_tail.tex`, `tail_summary.tex` | `scripts/tail_dependence.py` | Loss quantiles with a Student-t common factor against the Gaussian one (Section 4.4) |
| `pooling.csv`, `table_pooling.tex`, `pooling_summary.tex` | `scripts/pooling_subadditivity.py` | Whether the 99% loss quantile of two pooled cohorts exceeds the sum of the cohorts' quantiles: cohorts of 50 and 250 loans, three PD pairs, a common Gaussian factor, independent factors and a common Student-t factor (400,000 scenarios), with expected shortfall next to the quantile. Not yet quoted in the paper |
| `table_*.tex` (the rest) | `scripts/extract_credit_risk.py` | Rows of the horizon, loss, correlation, granularity, premium and recommendation tables, from the contract repository's `analysis/credit_risk/results`, and the reserve-policy table from this paper's simulation |
| `horizon_summary.tex` | `scripts/extract_credit_risk.py` | The marginal per-loan PD under the factor model and its scalar reconversion (Remark 1) |
| `apy_by_year.csv`, `reserve_sweep_curves.csv` | `scripts/extract_credit_risk.py` | Curves for Figures 3 and 4 |
| `loss_density.csv`, `premium_curve.csv` | `scripts/extract_credit_risk.py` | Curves for Figures 1 and 2, from the closed forms of `analysis/credit_risk/vasicek.py` |

Run order: `locked_reserve.py`, then `event_timed.py` (it reads `reserve_years.csv`), `tail_dependence.py`
and `extract_credit_risk.py`, each with the path to the contract repository. Every draw uses a fixed seed,
so two runs give byte-identical files.

The calibration ran on commit `b725a85` of the contract repository with Python 3.11, numpy 2.4 and
scipy 1.17, and its results reproduced byte for byte before this paper used them.
