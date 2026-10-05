# Data behind the paper

Every table and figure reads a file here. Generated files say so in their first line; do not edit
them by hand.

| File | Produced by | Content |
| --- | --- | --- |
| `reserve_years.csv` | `scripts/locked_reserve.py` | Lenders' mean return, 1st percentile, probability of any loss and mean reserve, by year, for PD 3, 5 and 10%, two reserve shares and two release policies (200,000 paths each) |
| `reserve_sweep.csv` | `scripts/locked_reserve.py` | The locked reserve against the reserve share from 20 to 80%: return in year 30 and over 30 years, the limit of Theorem 2, loss probabilities in years 10 and 30, reserve in year 30 |
| `reserve_summary.tex` | `scripts/locked_reserve.py` | Macros for the reserve shares and long-run returns quoted in the text |
| `table_*.tex` | `scripts/extract_credit_risk.py` | Rows of Tables 2 to 9, from the contract repository's `analysis/credit_risk/results` and this paper's simulation |
| `apy_by_year.csv`, `reserve_sweep_curves.csv` | `scripts/extract_credit_risk.py` | Curves for Figures 3 and 4 |
| `loss_density.csv`, `premium_curve.csv` | `scripts/extract_credit_risk.py` | Curves for Figures 1 and 2, from the closed forms of `analysis/credit_risk/vasicek.py` |

The calibration ran on commit `b725a85` of the contract repository with Python 3.11, numpy 2.4 and
scipy 1.17, and its results reproduced byte for byte before this paper used them.
