# Data behind the paper

Every number in Section 8 comes from a file here. Generated files say so in their first line; do
not edit them by hand.

| File | Produced by | Content |
| --- | --- | --- |
| `attack_profit.csv` | `scripts/extract_simulation.py` | Attacker net profit against the number of accounts for three attacks (Figure 5) |
| `attack_table.tex` | `scripts/extract_simulation.py` | Rows of Table 3 |
| `fuzz_runs.txt.gz` | the invariant suite's `afterInvariant` | One line per fuzzing run: loans, defaults, charges, Sybil activity, how much of each bound was used, and every operation's accepted, rejected and skipped calls. Forge appends a copy of each property's last run, 13 lines in all, which the summary drops |
| `fuzz_forge_tail.txt` | `forge test` | The end of the campaign's output, with the suite result |
| `fuzz_summary.csv`, `fuzz_stats.tex` | `scripts/summarize_fuzz.py` | Totals over the campaign (Table 1 and the abstract) |
| `mutation.csv` | `scripts/mutation_analysis.py` | Each seeded fault, the number of fuzz seeds (of three) that detected it, and the properties or unit tests that failed |
| `mutation_table.tex`, `mutation_summary.tex` | `scripts/mutation_summary.py` | Table 2 and the sentence that summarises it |

The campaign ran on commit `b725a85` of the contract repository with Foundry 1.5.1, Solidity
0.8.33, `runs = 1300`, `depth = 256` and `fail-on-revert = true`. It took 21 minutes on four
cores.
