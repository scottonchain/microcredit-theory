# Conserved Credit: target journals and scope

This file keeps the paper focused. It records the paper's discipline and its one question, three
journals that would accept it, and what belongs in other papers instead.

## Discipline and question

**Discipline:** economics and computation, specifically algorithmic mechanism design for systems
that must resist malicious agents.

**Question:** In a lending pool where accounts are free to create, how much can a coalition of
accounts cost lenders, and how much credit may repayment history earn without an accountable
issuer?

**Answer in one line:** The loss is at most the issued lines plus dues paid, for any coalition and
any number of accounts. History may earn no more than the value it irrevocably surrendered.

## Journals

| | Journal | Publisher | Why it fits | What a submission would need |
| --- | --- | --- | --- | --- |
| 1 (primary) | ACM Transactions on Economics and Computation (TEAC) | ACM | Its stated scope includes mechanism design, systems resilient against malicious agents, and reputation and trust systems. The sybilproofness literature the paper extends (Cheng and Friedman; Resnick and Sami; credit networks) appeared in ACM EC and its workshops. | The paper is already in TEAC's format (acmart, acmsmall). Reviewers will look for the tightness of the bounds, the relation to sybilproof reputation functions, and the open equilibrium question. |
| 2 | Games and Economic Behavior | Elsevier | The leading game theory journal, and it publishes algorithmic game theory. The farming theorem and the trilemma are results about strategic agents with free identities, in the line of Friedman and Resnick's work on cheap pseudonyms. | Reformat in elsarticle. Shorten the implementation section to a paragraph. Strengthen the strategic framing: state the attacker's problem as an optimisation and, ideally, add the equilibrium analysis of backers listed as an open problem. |
| 3 | Cryptoeconomic Systems | MIT Press (open access) | A journal for research on blockchains and cryptoeconomic mechanisms, which welcomes work that pairs a mechanism with an implementation. The paper's deployed contract, fuzzing and attack simulation fit its readership. | Keep the theorems, expand the implementation and validation section, and add a short comparison with deployed on-chain credit and identity systems. |

Journal scopes were checked on 2026-10-05 against each journal's own pages:
[TEAC scope](https://dl.acm.org/journal/teac/about-scope),
[Games and Economic Behavior](https://www.sciencedirect.com/journal/games-and-economic-behavior),
[Cryptoeconomic Systems](https://cryptoeconomicsystems.pubpub.org/about).

## In scope

- The model of one-hop backing, coverage and the default waterfall.
- Conservation of capacity and coalition capacity.
- The loss bound, its per-account invariant, the coalition (cut) bound and the reserve corollary.
- Lines that change, the rotation construction and the issuance budget.
- The farming theorem, the trilemma, and what counts as surrendered value.
- Validation only as far as it shows that the implementation matches the model: fuzzing, mutation
  analysis, and the attack simulation that compares mechanisms.

## Out of scope (other papers)

| Topic | Discipline | Where it goes |
| --- | --- | --- |
| Pricing the risk premium and sizing the first-loss reserve (one-factor model, Basel correlation) | Credit risk | `pricing-and-reserve` |
| What restricting backing to one hop costs in liquidity, compared with multi-hop credit networks | Network science | `one-hop-liquidity` |
| How an issuer should turn identity and history into lines (Bayesian policy within a budget) | Credit scoring, statistics | A separate paper from `analysis/issuer_policy` |
| Provisioning of overdue loans and runs by lenders | Banking | Not yet a paper |
| Recovering relayed transactions from nonces | Distributed systems | Not yet a paper |
| The detection challenge and its calibration corpus | Machine learning evaluation | Not yet a paper |

A new result belongs in this paper only if it answers the question above. Anything else starts its
own directory with its own journals file.
