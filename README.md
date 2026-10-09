# Microcredit theory

> **New here or looking for updates?** Read [Credit Among Strangers](https://github.com/scottonchain/microcredit-vision), the project's blog: the newest post in full, earlier posts by date, and [VERIFY.md](https://github.com/scottonchain/microcredit-vision/blob/main/VERIFY.md) to recompute every figure. The plain-language overview is the post [Live AI agents, working toward human benefit](https://github.com/scottonchain/microcredit-vision/blob/main/posts/2026-10-06-live-ai-agents-working-toward-human-benefit.md). Papers, review opportunities and build instructions follow below.

Research papers behind the microcredit protocol: a lending pool on a public blockchain that lends
without collateral to people who lack it, and to people without a credit history, stable banking or
existing digital assets. The protocol, its tests and its analysis code are in
[microcredit-contract](https://github.com/scottonchain/microcredit-contract). The project's goal is
to help end human poverty; microcredit is a proposed means whose usefulness must be tested against
human outcomes.

Each directory holds one paper written for one discipline and one journal, with its LaTeX sources,
bibliography, figures, the data behind every number, and the compiled PDF. Each directory's
`JOURNALS.md` names three candidate journals for the paper and lists what belongs in other
papers instead, so that each paper stays focused.

## Papers

| Directory | Paper | Discipline | Primary journal | Status |
| --- | --- | --- | --- | --- |
| [conserved-credit](conserved-credit/) | Conserved Credit: Sybil-Proof Loss Bounds for Uncollateralized Lending with Free Identities | Economics and computation | ACM Transactions on Economics and Computation | Working paper, complete |
| [pricing-and-reserve](pricing-and-reserve/) | Pricing Uncollateralized Microcredit on a Public Blockchain: Short Loans, Re-lending and a Locked First-Loss Reserve | Credit risk | The Journal of Credit Risk | Working paper, complete |
| [one-hop-liquidity](one-hop-liquidity/) | One Hop or Many: What Self-Liable Intermediaries Cost a Credit Network | Network science | Network Science | Working paper, complete |
| [issuer-policy](issuer-policy/) | Credit Lines for Pseudonymous Borrowers: Identity-Gated Bayesian Lending under an On-Chain Issuance Budget | Operational research | European Journal of Operational Research | Working paper, complete |
| [lending-equilibrium](lending-equilibrium/) | Pricing the Reserve: Market Equilibrium, Lender Safety and Liquidity in an Uncollateralized On-Chain Lending Pool | Financial intermediation | Journal of Financial Intermediation | Working paper, complete |

## Technical notes

| Directory | Note | Status |
| --- | --- | --- |
| [transitive-allocation](transitive-allocation/NOTE.md) | Consented, stake-rooted, bounded-depth allocation certificates: ledger conservation, global reservation, consent bound, loss attribution and a Sybil-neutrality statement for the two-hop router, with the dynamic cases and the fixture list | Draft, not yet independently reviewed |

Scope new work against the [current team direction](https://github.com/scottonchain/microcredit-agent-testbed/tree/main/world-model)
and a concrete question about bounded, voluntary risk or measured human benefit. Existing papers
retain their recorded inputs and source pins; a new calculation has its own result identity.
Referee reports stay unchanged under `reviews/`; author responses and the revisions they led to are
in the issue that carries each report (the first, an internal report on all five papers, is
[issue #6](https://github.com/scottonchain/microcredit-theory/issues/6)).

## How to help

We are looking for outside researchers to check, attack and extend this work. Useful contributions:

- Check a proof and report a gap, however small.
- Find a behaviour of the contract that the model in a paper does not capture.
- Take on an open problem listed at the end of a paper.
- Suggest a better venue, or related work we have missed.

The [independent-review coordination issue](https://github.com/scottonchain/microcredit-theory/issues/1)
links three bounded assignments and a short report template. Reviews proceed through agreed scope,
original report, author response, revision and an outside recheck by the original reviewer. Claude
Code owns manuscript responses; Hermes recruits outside reviewers; Codex coordinates review and
reproduction. A posted invitation is not acceptance, and internal agents are not independent reviewers.
Unfavorable findings and disagreements remain part of the public record. Candidate venues imply
neither journal endorsement nor acceptance; no new payment is promised.

Open an issue in this repository and name the paper and the result. Corrections and contributions
are credited in the paper they improve.

## Build and reproduce

Run commands from this repository's root. PDF builds need TeX Live 2023 or later with `latexmk`,
`acmart`, `pgfplots` and `algorithm2e`. `latexmk` decides which dependencies need rebuilding.

```bash
make check                       # offline tooling checks; no simulations
make conserved-credit            # one paper; make all builds all five
make clean                       # auxiliary files only; keeps PDFs and data
python3 reproduce.py all --tables-only --output /tmp/paper-tables
```

[reproduce.py](reproduce.py) owns the contract source pin and ordered reproduction commands;
`--help` lists paper selectors and options. The default contract checkout is the sibling
`microcredit-contract`; its current branch is irrelevant, but it must contain the recorded commit.
Use [requirements.txt](requirements.txt) for the recorded dependencies. The reference environment
used Python 3.11.15; numerical and LP outputs can vary in other environments.

Start with `--dry-run` or `--tables-only`. Omit `--tables-only` when a question requires fresh Python
simulations. Each run uses disposable copies of scripts and data, refuses an existing output path,
and records commands, versions and hashes in `reproduction.json`. Foundry evidence is summarised
from recorded inputs; a fresh campaign has [separate instructions](conserved-credit/#fresh-foundry-experiments).
Agreement with a fixture does not establish demand or human benefit.

## Authorship

The papers are written by Claude Code, an AI agent made by Anthropic, working with the project's
human operator, who directs the research. Other AI agents working with the project contributed
attacks and reviews, as each paper's acknowledgments state.
