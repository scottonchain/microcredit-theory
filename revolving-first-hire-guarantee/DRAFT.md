**INTERNAL DRAFT: not a public claim, offer, solicitation, commitment, or proven model.**

# A revolving first-job payment guarantee: reserve arithmetic, solvency and benefit

Written by Claude Code (AI agent), 2026-10-11, as the analysis Codex requested on testbed board 15
(comment 6111178929) for the operator's proposal relayed there (6111230093, amended 6111239163).
Literature review is deliberately light. Every number below is either arithmetic stated in the text
or the output of [`ruin.py`](ruin.py) in this folder, which anyone can rerun with Python 3 and no
dependencies. No money, outreach, worker, client or programme is involved.

## 1. The problem it addresses

A person with no completed jobs struggles to get a first one. Clients choose people with reviews;
a newcomer has none. In Pallais's 2010 oDesk experiment (NBER working paper w18917), inexperienced
workers given one short paid job and a public rating were far more likely to find further work two
months later (about 30% against about 12%). The barrier documented there is on the **client's**
side: the client's uncertainty about an unknown worker.

## 2. Two sibling designs, and the risk each one insures

| | Earlier candidate: client-refund guarantee | New candidate: revolving first-job payment guarantee |
| --- | --- | --- |
| Who is protected | The client | The worker |
| Risk insured | The newcomer's work fails the client's acceptance | The client does not pay for accepted work |
| Who pays the wage | The client | The client |
| When the reserve pays | On a failed delivery, it refunds the client | On client nonpayment, it pays the worker up to G |
| Replenishment | None (earlier design) | A successful, paid worker returns a small capped contribution r |
| Worker owes anything on a claim | No | No |

The earlier design acts on the barrier in section 1. The new design acts on a different one: a
worker's exposure to a client who does not pay. That difference is the central question in
section 8.

## 3. Variables

- `p`: probability that the client defaults or does not pay for an accepted job.
- `q`: probability that a worker remits the contribution, given the client paid.
- `G`: the guarantee, the most the reserve pays on one job.
- `c`: the reserve's cash and administrative cost per job (payment fees, checks, support time).
- `r`: the contribution a paid worker returns.
- `w`: the wage of the job; `u`: the starting reserve.

## 4. Reserve scorecard: break-even contribution

Per job, the expected change in the reserve is

    E[Δ reserve] = (1 − p) q r − p G − c

so the contribution that keeps the reserve level on average is

    r* = (p G + c) / ((1 − p) q)

| p | q | G | c | r* | r* as share of a $60 wage |
| --- | --- | --- | --- | --- | --- |
| 1% | 0.9 | $60 | $0.50 | $1.23 | 2.1% |
| 3% | 0.8 | $60 | $1.00 | $3.61 | 6.0% |
| 10% | 0.8 | $60 | $1.00 | $9.72 | 16.2% |
| 3% | 0.8 | $20 | $1.00 | $2.06 | 3.4% |
| 10% | 0.8 | $20 | $1.00 | $4.17 | 6.9% |

When nonpayment is rare, the per-job cost `c` dominates the contribution. When it is common, the
contribution becomes a large tax on exactly the workers the scheme means to help.

The same formula prices a revolving version of the earlier client-refund guarantee, with the
failure share `f` in place of `p` and the refund in place of `G`. With a $60 refund, c = $1 and
q = 0.8, it needs $5.26 (8.8% of the wage) at f = 5%, $9.72 (16.2%) at f = 10% and $17.99 (30%) at
f = 18%. Revolving the client-side guarantee is only plausible where delivery failure is low.

## 5. Average break-even is not solvency

A finite reserve can run out on a run of bad luck even when the average is level. `ruin.py`
simulates a $100 reserve that backs one open job at a time, stops when it cannot cover the next
guarantee, and runs 500 jobs (4,000 trials per row).

| p | q | G | c | Loading on r* | Chance the $100 runs out within 500 jobs |
| --- | --- | --- | --- | --- | --- |
| 1% | 0.9 | $60 | $2.00 | none | 68% |
| 1% | 0.9 | $60 | $2.00 | +50% | 18% |
| 3% | 0.8 | $60 | $1.00 | +50% | 39% |
| 10% | 0.8 | $60 | $1.00 | +50% | 51% |
| 3% | 0.9 | $20 | $2.00 | +50% | 0.1% |
| 10% | 0.6 | $20 | $2.00 | +50% | 3.6% |

Three rules follow:

1. **Safety loading.** Charging exactly `r*` leaves the reserve a fair coin flip around its
   starting value, and a $100 reserve fails more often than not. A loading of the order of 50% is
   needed before ruin becomes rare.
2. **Exposure cap.** The guarantee per job must be small against the reserve. A $100 reserve can
   stand behind a $20 guarantee with low ruin risk; it cannot stand behind $60. For G = $60 with a
   50% loading, ruin within 500 jobs falls from 39% to 1.5% at p = 3%, and from 51% to 4.8% at
   p = 10%, when the reserve grows from $100 to $300.
3. **Reserve floor.** Stop issuing new guarantees while the reserve is below a floor (for example
   2G), and resume as contributions rebuild it.

**Correlation.** Failures are not independent if one client hires several newcomers. In the
simulation, letting a block of 5 jobs share one client's outcome with probability 0.2 raises ruin
for G = $20, p = 3% from 0.3% to 15%; with probability 0.5, to 20%. At p = 10% the same steps take
it from 3% to 28% and 36%. A cap of one open guarantee per client is therefore part of the design,
not a refinement.

**What this means for the claim.** With positive loading, caps and a floor, a reserve can in
principle revolve for a long time with a stated probability of not running out. It cannot be
promised to last for ever, and a $100 reserve cannot be said to last at all until measured `p`,
`q`, `c` and correlation support it.

## 6. Contribution design

- **Percentage of the paid wage, with a dollar cap.** Losses scale with the guarantee, which
  scales with the wage, so a percentage fits; the cap protects workers on larger jobs. A pure
  percentage undercharges very small jobs where `c` dominates, so either set a minimum job size or
  accept a small cross-subsidy.
- **Collect it when the payment arrives, or not at all.** Recovering it afterwards turns `q` into
  a debt-collection problem. If it cannot be taken at the moment of payment, treat it as a pledge
  that is never pursued, and price the shortfall through `q`.
- **Never owed on a claim.** A worker whose client did not pay owes nothing, as the proposal says.

## 7. Guarantee, loan or insurance?

It is not a loan: nothing is advanced to the worker when the client pays, and nothing is repaid
after a claim. Economically it is mutual payment insurance with the premium collected only from
those who were paid, closer to a mutual guarantee or invoice insurance than to microcredit. The
contribution after success is a contingent obligation. Collected at source, it is a fee; pursued
later, it becomes a small personal debt, which the design should avoid.

## 8. The strongest challenge: does it create first jobs?

Two scorecards must be kept apart. The reserve scorecard (sections 4 and 5) asks whether the pool
survives. The benefit scorecard asks whether people are better off per sponsor dollar:

    M = (incremental net spendable earnings caused by the guarantee
         + measured incremental follow-on earnings − contributions paid − displacement and harms)
        / (sponsor capital consumed + fees, support and administration it funds + capital-lock cost)

Contributions recapitalise the pool and are a cost to workers, so they appear in the numerator as
a deduction and are reported separately as recapitalisation. A self-sustaining reserve makes the
denominator small, which can make `M` look large. That is exactly where honesty matters: if the
guarantee causes no extra jobs or earnings, the numerator is negative, because workers pay
contributions for protection that changed nothing.

On a platform with funded escrow, client nonpayment is already largely covered for work done
through the platform's own process: fixed-price milestones are funded before work, and logged
hourly work has the platform's own protection. There, `p` should be small, the guarantee
duplicates existing protection, and the barrier Pallais documented (the client's choice to hire)
is untouched. So on such platforms the expected causal effect is close to zero.

The payment guarantee can matter where nonpayment is a real and uncovered risk: direct clients
found off a platform, small local businesses, informal and community work, invoice work paid late.
There it may let a newcomer accept work they would otherwise refuse, or take on a client they
could not otherwise trust. That is a testable claim, and it is the claim the route rests on.

## 9. Minimum viable pilot and what it can show

A $100 reserve can test **take-up, `q`, operating cost `c`, and whether the offer changes what work
newcomers accept and earn**. It cannot estimate `p` precisely or establish solvency: estimating a
3% nonpayment rate to within 2 points at 95% confidence takes about 280 jobs, and to within 1
point about 1,100.

A bounded first pilot:

- **Channel:** work where nonpayment risk is real and no escrow applies, through a programme or
  community that already connects newcomers with clients. Not marketplace work covered by escrow.
- **Exposure:** G at most $20 (one fifth of the reserve), one open guarantee per client, reserve
  floor 2G.
- **Contribution:** a percentage of the paid wage with a small cap, taken at payment or pledged
  and never pursued.
- **Causal test:** offer the guarantee on a seeded random half of eligible jobs or applications,
  so the difference in accepted work and earnings can be attributed to it.
- **Measure:** offers, take-up, jobs accepted, client payments and nonpayments (`p`), remittances
  (`q`), costs (`c`), wages, fees, hours, prior earnings, follow-on paid work at 8 weeks,
  disputes and complaints.
- **Report:** both scorecards, the gross leverage, the incremental `M` with its attribution method
  and uncertainty, and every failure.

## 10. Reject or modify if

- the offer does not change accepted work or earnings in the randomised comparison;
- measured nonpayment is so low that the guarantee only adds cost, or so high that the
  break-even contribution harms workers;
- remittance `q` is low enough to need debt collection;
- costs, correlation or ruin risk need more capital than the benefit justifies;
- displacement erases the net gain;
- a simpler mechanism (escrow, prepayment, an existing programme) does as much for less.

## 11. Open questions for the team

1. Which channel has real, uncovered nonpayment risk for newcomers and a programme that can offer
   the guarantee within its own rules?
2. Should the sibling designs be combined (protect the client against failed delivery and the
   worker against nonpayment), and does the combined contribution stay tolerable?
3. Who administers claims and evidence of nonpayment, and what does that cost per job?
