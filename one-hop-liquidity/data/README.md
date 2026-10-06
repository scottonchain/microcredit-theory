# Data behind the paper

Every table and figure reads a file here, written by `scripts/extract_liquidity.py` from
`analysis/liquidity/results/*.csv` in the contract repository at commit `b725a85`. Do not edit them
by hand.

| File | Content |
| --- | --- |
| `table_fresh.tex`, `table_steady.tex` | Tables 1 and 2: the base point on a fresh network and in the steady state |
| `table_equivalence.tex` | Table 3: issued credit one hop needs to match each regime |
| `table_liability.tex` | Table 4: routed share, mean hops, relayed and remote shares, storage slots |
| `table_sybil.tex` | Table 5: Sybil extraction by regime |
| `degree_ws.csv`, `degree_sbm_half.csv` | Figure 2: success against mean degree |
| `borrowable_ws.csv` | Figure 3: probability of drawing at least x |
| `equivalence_curve.csv` | Figure 4: one-hop success against the share of holders |
| `steady_replicates.csv`, `table_steady_replicates.tex` | The base point's steady state on three independent graphs, with graph 0's difference from the published row (`scripts/steady_replicates.py`) |
| `replicates_check.txt` | The acceptance check of graph 0 against the published row: exact for the flow regimes, within 0.005 for the three-hop linear programme; a failure stops the script before any other output (`scripts/steady_replicates.py`) |
| `equivalence_line.csv`, `table_equivalence_line.tex` | The fixed-cohort equivalence: one-hop success when every line is scaled together with the trust per edge, and when the line alone is scaled (`scripts/steady_replicates.py`) |
| `replicates_summary.tex` | Macros for the replication and fixed-cohort figures quoted in the text |
| `replicates_environment.txt` | The Python, NumPy, SciPy and NetworkX versions that produced the committed replication data |

The experiments seed every task from its own parameters, so their outputs are identical on every run
and for any number of processes.
