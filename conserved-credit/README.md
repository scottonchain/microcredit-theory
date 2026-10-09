# Conserved Credit

**Conserved Credit: Sybil-Proof Loss Bounds for Uncollateralized Lending with Free Identities.**
Working paper, prepared for ACM Transactions on Economics and Computation.

- [paper.pdf](paper.pdf): the compiled paper.
- [JOURNALS.md](JOURNALS.md): the paper's discipline, three target journals, and what is out of scope.
- `paper.tex`, `references.bib`, `figures/`: the sources. The figures are TikZ and pgfplots.
- `data/`: every number in the paper that comes from a run, with the scripts that produced it.
- `scripts/`: the scripts that extract and summarise those runs.

## Results

| In the paper | Statement | In `docs/CREDIT_MODEL.md` of the contract repository |
| --- | --- | --- |
| Theorem 4.1 | Total borrowing capacity is at most granted credit plus committed stake | Theorem 1 |
| Corollary 4.2 | A coalition's capacity does not grow with its number of accounts | |
| Lemma 5.1 | Per-account invariant (Q) | inside Theorem 2 |
| Theorem 5.3 | Realised plus potential loss is at most issued lines plus dues | Theorem 2 |
| Corollary 5.4 | The same bound for any coalition: a weighted cut | Corollary (min-cut) |
| Corollary 5.5 | Lenders bear at most the issued lines | Corollary (lenders pay only for issued lines) |
| Theorem 6.2, Proposition 6.3 | Lines that change: the bound holds for peak lines, not current ones | Theorem 2' |
| Corollary 6.4 | An issuance budget charged on held lines bounds exposure | Section 4.2 |
| Theorem 7.2, Corollary 7.3 | Farming history credit; the trilemma | Theorem 3 |
| Propositions 7.4, 7.5 | What a borrower who also lends surrenders; the pooled-reserve case | Section 4.1 |

## Build and reproduce

Use the [root build and reproduction guide](../#build-and-reproduce) with the selector
`conserved-credit` for the PDF, attack simulation and summaries of recorded evidence.

### Fresh Foundry experiments

These separate experiments use contract commit `b725a85`. Run them from disposable copies of both
repositories: the experiment scripts write this paper's `data/`, and mutation analysis edits the
contract worktree. Keep the new results separate from the recorded campaign.
Run `forge` in the contract copy's `packages/foundry` directory and the Python commands in the
theory copy's `conserved-credit` directory, passing absolute paths for the two fuzz logs.

```bash
# Stateful fuzzing (Section 8.2): raise the inline settings in
# packages/foundry/test/invariant/CreditConservation.invariant.t.sol to runs = 1300, depth = 256, then
INVARIANT_STATS_FILE=./inv_stats.txt forge test --match-path 'test/invariant/*' | tee forge.log
python3 scripts/summarize_fuzz.py inv_stats.txt forge.log 1300 256

# Mutation analysis (Section 8.3), on a disposable worktree of the contract repository:
# 14 seeded faults, three fuzz seeds each, then unit tests for any fault the fuzzing misses (about 30 minutes)
python3 scripts/mutation_analysis.py <worktree>
python3 scripts/mutation_summary.py
```

## Contributing

Review a proof, find a gap between the model and the contract, or attack an assumption. Open an
issue in this repository and name the result (for example "Lemma 5.1, default step"). Corrections
are credited in the acknowledgments.
