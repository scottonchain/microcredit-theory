#!/bin/sh
# Compatibility command: regenerate this paper's data in place.
# Prefer ../../reproduce.py for isolated, pinned reproduction into a separate output directory.
set -eu
paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
contract_dir=${1:-"$paper_dir/../../microcredit-contract"}
contract_dir=$(CDPATH= cd -- "$contract_dir" && pwd)
python_bin=${PYTHON:-python3}
PD=0.05 PREMIUM=0.08 OUTSUB= "$python_bin" "$paper_dir/scripts/equilibrium.py" "$contract_dir"
PD=0.03 PREMIUM=0.06 OUTSUB=robust/pd3 "$python_bin" "$paper_dir/scripts/equilibrium.py" "$contract_dir"
PD=0.10 PREMIUM=0.14 OUTSUB=robust/pd10 "$python_bin" "$paper_dir/scripts/equilibrium.py" "$contract_dir"
"$python_bin" "$paper_dir/scripts/robustness_table.py"
