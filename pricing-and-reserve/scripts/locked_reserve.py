#!/usr/bin/env python3
"""Multi-year first-loss reserve under two release policies (Section 6 of the paper).

The pool's reserve receives a share r of every interest payment and pays losses before lenders.
The deployed contract never releases interest-funded reserve (it keeps all dues ever paid), so the
balance is "locked". The credit-risk calibration in the contract repository instead assumed a cap
with the surplus released to lenders. This script simulates both, with the one-factor model of
analysis/credit_risk (imported from the contract repository) and losses per exposure-year in a pool
that re-lends after write-offs.

Usage: python3 scripts/locked_reserve.py <path to microcredit-contract>

Writes data/reserve_years.csv (by year), data/reserve_sweep.csv (long-run results against r) and
data/reserve_summary.tex (macros used by paper.tex).
"""
import csv
import pathlib
import sys

import numpy as np

CONTRACT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "../../microcredit-contract")
sys.path.insert(0, str(CONTRACT / "analysis/credit_risk"))
import vasicek as vs  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent.parent / "data"
SEED = 20261005
PATHS = 200_000
YEARS = 30
U = 0.85
FEE = 0.0
EFFR = vs.EFFR
# Recommended premiums of the calibration (bps) at annual PD 3 / 5 / 10%.
CASES = [(0.03, 0.0600), (0.05, 0.0800), (0.10, 0.1400)]
RECOMMENDED_R = {0.03: 0.55, 0.05: 0.65, 0.10: 0.75}


def simulate(pd, rho, apr, r, cap, tag):
    """Lender return, lender loss and reserve per unit of deposits, for YEARS independent years.

    Per year: inflow u*apr*r; loss u*D with D the replenished default rate given the factor; the
    reserve pays first; lenders take the rest. With a finite cap the balance above it is released
    to lenders; with cap=None the reserve is locked.
    """
    rng = np.random.default_rng(np.random.SeedSequence([SEED, tag]))
    inflow = U * apr * r
    bal = np.zeros(PATHS)
    apy = np.empty((YEARS, PATHS))
    lender_loss = np.empty((YEARS, PATHS))
    reserve = np.empty((YEARS, PATHS))
    gross_loss = np.empty((YEARS, PATHS))
    for t in range(YEARS):
        p = vs.conditional_pd(pd, rho, rng.standard_normal(PATHS))
        d = np.asarray(vs.replenished_default_rate(np.clip(p, 0.0, 1 - 1e-12)))
        loss = U * d
        avail = bal + inflow
        ll = np.maximum(loss - avail, 0.0)
        bal = np.maximum(avail - loss, 0.0)
        released = np.zeros(PATHS)
        if cap is not None:
            released = np.maximum(bal - cap, 0.0)
            bal = bal - released
        apy[t] = U * apr * (1 - FEE - r) - ll + released
        lender_loss[t] = ll
        reserve[t] = bal
        gross_loss[t] = loss
    return apy, lender_loss, reserve, gross_loss


def check_identity(apr, r, apy, reserve, gross_loss):
    """Cumulative lender return = u*apr*(1-f)*T - total losses - final reserve, path by path."""
    lhs = apy.sum(axis=0)
    rhs = U * apr * (1 - FEE) * apy.shape[0] - gross_loss.sum(axis=0) - reserve[-1]
    err = float(np.max(np.abs(lhs - rhs)))
    if err > 1e-9:
        sys.exit(f"accounting identity fails by {err}")
    return err


def main() -> None:
    OUT.mkdir(exist_ok=True)
    year_rows, sweep_rows, macros = [], [], {}
    tag = 0
    for pd, premium in CASES:
        rho = vs.basel_other_retail_correlation(pd)
        apr = EFFR + premium
        el = vs.replenished_expected_loss(pd, rho)
        l99 = float(vs.replenished_loss_quantile(pd, rho, 0.99))
        cap = U * (l99 - el)
        r_el = el / apr
        for r_label, r in (("expected loss", r_el), ("recommended", RECOMMENDED_R[pd])):
            for policy, c in (("released above cap", cap), ("locked", None)):
                tag += 1
                apy, ll, res, gl = simulate(pd, rho, apr, r, c, tag)
                err = check_identity(apr, r, apy, res, gl)
                for t in range(YEARS):
                    year_rows.append({
                        "annual_pd": pd, "rho": round(rho, 6), "apr": apr, "reserve_share_case": r_label,
                        "reserve_share": round(r, 6), "policy": policy, "year": t + 1,
                        "mean_apy": float(apy[t].mean()), "apy_p01": float(np.quantile(apy[t], 0.01)),
                        "p_lender_loss": float((ll[t] > 1e-12).mean()),
                        "mean_reserve": float(res[t].mean()), "identity_max_error": err,
                    })
        # long-run sweep over r at this PD, locked reserve
        for r in np.round(np.arange(0.20, 0.801, 0.025), 3):
            tag += 1
            apy, ll, res, gl = simulate(pd, rho, apr, float(r), None, tag)
            sweep_rows.append({
                "annual_pd": pd, "apr": apr, "reserve_share": float(r), "r_over_r_el": float(r / r_el),
                "mean_apy_years_1_30": float(apy.mean()), "mean_apy_year_30": float(apy[-1].mean()),
                "long_run_formula": U * (apr * (1 - FEE) - max(el, apr * float(r))),
                "p_lender_loss_year_10": float((ll[9] > 1e-12).mean()),
                "p_lender_loss_year_30": float((ll[-1] > 1e-12).mean()),
                "mean_reserve_year_30": float(res[-1].mean()),
            })
        key = {0.03: "Three", 0.05: "Five", 0.10: "Ten"}[pd]
        macros[f"REl{key}"] = f"{100 * r_el:.0f}"
        macros[f"Apr{key}"] = f"{100 * apr:.2f}"
        macros[f"LongRunLocked{key}"] = f"{100 * U * (apr * (1 - FEE) - max(el, apr * RECOMMENDED_R[pd])):.2f}"
        macros[f"LongRunAtEl{key}"] = f"{100 * U * (apr * (1 - FEE) - el):.2f}"
        macros[f"RRec{key}"] = f"{100 * RECOMMENDED_R[pd]:.0f}"
        # The interim production default of 45% (contract commit 1812e7d, 6 October 2026).
        macros[f"LongRunFortyFive{key}"] = f"{100 * U * (apr * (1 - FEE) - max(el, apr * 0.45)):.2f}"
    macros["Effr"] = f"{100 * EFFR:.2f}"

    def write(name, rows):
        with open(OUT / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    write("reserve_years.csv", year_rows)
    write("reserve_sweep.csv", sweep_rows)
    with open(OUT / "reserve_summary.tex", "w") as fh:
        fh.write("% Generated by scripts/locked_reserve.py; do not edit.\n")
        for k, v in macros.items():
            fh.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
    print(macros)


if __name__ == "__main__":
    main()
