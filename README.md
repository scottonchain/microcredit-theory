# Microcredit theory

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
| [one-hop-liquidity](one-hop-liquidity/) | One Hop or Many: What Solvent Intermediaries Cost a Credit Network | Network science | Network Science | Working paper, complete |

A further paper will cover the issuer's lending policy (credit scoring), from the contract
repository's `analysis/issuer_policy`.

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

## Build

Each paper builds with `make` in its directory (TeX Live 2023 or later, with `acmart`, `pgfplots`
and `algorithm2e` where the paper uses them).

## Authorship

The papers are written by Claude Code, an AI agent made by Anthropic, working with the project's
human operator, who directs the research. Other AI agents working with the project contributed
attacks and reviews, as each paper's acknowledgments state.
