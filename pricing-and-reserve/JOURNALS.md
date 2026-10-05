# Pricing Uncollateralized Microcredit: target journals and scope

This file keeps the paper focused. It records the paper's discipline and its one question, three
journals that would accept it, and what belongs in other papers instead.

## Discipline and question

**Discipline:** credit risk, specifically portfolio credit risk models and the pricing of loan
portfolios.

**Question:** What premium and what first-loss reserve should an uncollateralized on-chain lending
pool of short loans set, and what does its reserve rule cost lenders?

**Answer in one line:** Convert per-loan default rates to annual ones, correct for re-lending and
pool size, and price at 600, 800 and 1,400 basis points for annual PDs of 3, 5 and 10%. Under a
reserve that is never released, any reserve share above expected loss over the loan rate is a
permanent transfer from lenders.

## Journals

| | Journal | Publisher | Why it fits | What a submission would need |
| --- | --- | --- | --- | --- |
| 1 (primary) | The Journal of Credit Risk | Risk.net (Infopro Digital) | Its scope covers portfolio credit risk models, default probability estimation, correlation, loss distributions, capital adequacy, and, explicitly, the credit risk implications of blockchain, crypto-currencies and fintech firms. | The paper fits as it stands. Reviewers will look for the treatment of the asset correlation and for a stress analysis with serially correlated years, which the limitations list. |
| 2 | The Journal of Risk Finance | Emerald | Publishes theoretical and empirical work on financial risk management, and lists blockchain and risk, FinTech and risk, and cryptocurrency and risk management among its topics. | Shorten the derivations, expand the discussion of the reserve as a risk-management policy, and add a comparison with deposit-insurance and first-loss tranches in securitisation. |
| 3 | Finance Research Letters | Elsevier | A letters journal that publishes short results in finance, including many on crypto-asset markets and decentralized finance. | Cut to the locked-reserve result: Theorems 1 and 2, the production corollary and one figure, within the journal's length limit. |

Journal scopes were checked on 2026-10-05 against each journal's own pages:
[The Journal of Credit Risk](https://www.risk.net/static/about-the-journal-of-credit-risk),
[The Journal of Risk Finance](https://www.emeraldgrouppublishing.com/journal/jrf).
Finance Research Letters' scope is from general knowledge of the journal and should be confirmed
before a submission.

## In scope

- Converting default rates between loan terms and the annual horizon.
- The one-factor loss distribution, the Basel retail correlation and a correlation grid.
- Re-lending after write-offs, and finite pools (granularity adjustment and Monte Carlo).
- Break-even premiums at the loan and pool level, the largest PD a premium carries, and secured
  principal.
- Sizing the first-loss reserve, the accounting identity for lenders' return, and the long-run cost
  of a reserve that is never released.

## Out of scope (other papers)

| Topic | Discipline | Where it goes |
| --- | --- | --- |
| Why interest-funded reserve must stay locked: credit earned from dues, farming, Sybil accounts | Economics and computation | `conserved-credit` |
| Whether unsecured backing lowers default (joint liability) | Development economics | Not yet a paper; needs data |
| Provisioning of overdue loans and runs by lenders before write-off | Banking | Not yet a paper |
| How the issuer sets each borrower's line | Credit scoring | A separate paper from `analysis/issuer_policy` |
| Liquidity of one-hop backing | Network science | `one-hop-liquidity` |

A new result belongs in this paper only if it answers the question above. Anything else starts its
own directory with its own journals file.
