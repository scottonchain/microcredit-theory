# Pricing the Reserve: target journals and scope

This file keeps the paper focused. It records the paper's discipline and its one question, three
candidate journals for it, and what belongs in other papers instead.

## Discipline and question

**Discipline:** financial intermediation, specifically the pricing of loans and the capital buffer of a
lending intermediary whose funding can be withdrawn on demand.

**Question:** Which reserve share, together with which loan rate and utilisation, clears the market of
a pool that never releases interest-funded reserve, when lenders and borrowers both respond to its terms
and the pool must stay liquid?

**Answer in one line:** The loan rate is the lenders' alternative return, the idle-cash drag, the margin that
attracts lenders, and the larger of expected loss and the reserve's share of the rate; the share is free
to lenders up to the share that covers expected loss and is then split between borrowers and lenders by the
elasticities of demand and supply; with lenders who care about losing principal, volume peaks a few points
above the expected-loss share; and outside seed capital is cheaper protection than share.

## Journals

| | Journal | Publisher | Why it fits | What a submission would need |
| --- | --- | --- | --- | --- |
| 1 (primary) | Journal of Financial Intermediation | Elsevier | Publishes research on financial intermediation, financial contracting, financial regulation and credit markets, with a balance of theory and empirical work. The paper is a model of an intermediary's loan pricing, capital buffer and funding. | The paper is already in Elsevier's format. Reviewers will want the elasticities anchored in data (the pool's own flows, or deposit and loan data from other on-chain pools), a clearer statement of what is new against the bank-capital literature, and utilisation chosen by the pool rather than fixed. |
| 2 | Journal of Financial Stability | Elsevier | Publishes theoretical and empirical analysis of financial crises and stability, including market liquidity. The liquidity result (time to exit bounded by the loan term, utilisation set by a liquidity target) and the reserve as a buffer fit its scope. | Lead with liquidity and runs; model run dynamics and the withdrawal queue as a game among lenders; connect to the stability of stablecoin lending pools. |
| 3 | Journal of Banking & Finance | Elsevier | Publishes theory, applied and policy-oriented research on banking and financial institutions, including risk management and solvency. | Compare the locked reserve with bank capital requirements and loan-loss reserves; add an empirical calibration; shorten the proofs. |

The scope statements were read on 2026-10-05 from search-result summaries of each journal's own
description: the journals' pages on ScienceDirect were not reachable from the environment that wrote this
paper. Confirm each against the journal's page before a submission. The Journal of Money, Credit and Banking
was considered and set aside: its emphasis is macroeconomic.

## In scope

- The loan-rate identity and the lenders' floor.
- Existence, uniqueness and incidence of the market equilibrium for a reserve share that is never released.
- Lenders' participation under a yield requirement and a safety-first requirement; the volume-maximising share.
- Seed capital against reserve share.
- Liquidity: time to exit, utilisation under a liquidity target, the reserve as a cash cushion.
- Earned credit as the borrower's benefit from the share.

## Out of scope (other papers)

| Topic | Discipline | Where it goes |
| --- | --- | --- |
| Loss bounds and Sybil-proofness of the protocol | Economics and computation | `conserved-credit` |
| The loss model, the premium and lenders' long-run return under a lock | Credit risk | `pricing-and-reserve` |
| Liquidity of backing between borrowers | Network science | `one-hop-liquidity` |
| How the issuer sets lines | Credit scoring | `issuer-policy` |
| Estimating loan demand and deposit supply from the pool's flows | Empirical finance | Not yet a paper; needs data |
| Utilisation-based pricing against a fixed rate | Market design | Not yet a paper |
| Borrowers' welfare under the pool | Development economics | Not yet a paper; needs outcome data |

A new result belongs in this paper only if it answers the question above. Anything else starts its own
directory with its own journals file.
