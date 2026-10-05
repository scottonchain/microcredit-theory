# Credit Lines for Pseudonymous Borrowers: target journals and scope

This file keeps the paper focused. It records the paper's discipline and its one question, three
journals that would accept it, and what belongs in other papers instead.

## Discipline and question

**Discipline:** operational research in credit, specifically credit scoring and the allocation of
credit limits.

**Question:** How should an issuer set credit lines for pseudonymous borrowers when a contract caps
the total it may put at risk, evidence is thin and can be manufactured, and identities can be bought?

**Answer in one line:** Gate lines on costly identities with caps no larger than an identity's price,
weight evidence by the risk lenders bore, size each line at μ·ln(i/p), and allocate within the budget
greedily, which is optimal because the constraints form a laminar matroid.

## Journals

| | Journal | Publisher | Why it fits | What a submission would need |
| --- | --- | --- | --- | --- |
| 1 (primary) | European Journal of Operational Research | Elsevier (with EURO) | Publishes OR methodology and decision-making practice, with a long line of credit-scoring and banking papers (Crook, Edelman and Thomas 2007; Lessmann et al. 2015). The paper combines scoring, profit-based limit setting and constrained allocation. | The paper is already in Elsevier's format. Reviewers will want a comparison with a standard scoring baseline on the same simulated data and a sensitivity analysis of the late ratio and the prior. |
| 2 | Journal of the Operational Research Society | Taylor & Francis | A home of profit-based credit scoring and limit-setting work, including much of the Edinburgh credit-scoring tradition. | Shorten the incentive-compatibility section and expand the managerial discussion of setting tier costs and budgets. |
| 3 | IMA Journal of Management Mathematics | Oxford University Press | Publishes mathematical models for management decisions, including special issues on credit risk and scoring. | Lead with the matroid allocation and the front-running lemma, and move the simulation to an appendix. |

EJOR's scope and its record in credit scoring were checked on 2026-10-05 against
[the journal's page](https://www.sciencedirect.com/journal/european-journal-of-operational-research).
The other two are from general knowledge of the journals and should be confirmed before a submission.

## In scope

- Eligibility by costly identity and the incentive-compatibility condition on tier caps.
- Evidence weights, the Beta-Binomial posterior and the per-cycle default probability.
- The profit-maximising line under exponential demand.
- Greedy allocation within the budget and the per-report cap, its optimality, and robustness to
  front-running.
- The simulation: contract compliance, farms, honest lines, calibration, budget and attackers.

## Out of scope (other papers)

| Topic | Discipline | Where it goes |
| --- | --- | --- |
| The loss bounds the issuance budget rests on, and the farming theorem | Economics and computation | `conserved-credit` |
| The premium and reserve that price the issuer's lines | Credit risk | `pricing-and-reserve` |
| Liquidity of backing between borrowers | Network science | `one-hop-liquidity` |
| The market price of identities and proof of personhood | Security economics | Not yet a paper; needs data |

A new result belongs in this paper only if it answers the question above. Anything else starts its
own directory with its own journals file.
