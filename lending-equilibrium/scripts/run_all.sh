#!/bin/sh
# Reproduce every number of the paper: the PD 5% book, then the PD 3% and PD 10% books, then the
# robustness table. Usage: sh scripts/run_all.sh <path to microcredit-contract>
set -eu
C=${1:-../../microcredit-contract}
python3 scripts/equilibrium.py "$C"
PD=0.03 PREMIUM=0.06 OUTSUB=robust/pd3 python3 scripts/equilibrium.py "$C"
PD=0.10 PREMIUM=0.14 OUTSUB=robust/pd10 python3 scripts/equilibrium.py "$C"
python3 scripts/robustness_table.py
