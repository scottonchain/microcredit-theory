# One Hop or Many: target journals and scope

This file keeps the paper focused. It records the paper's discipline and its one question, three
candidate journals for it, and what belongs in other papers instead.

## Discipline and question

**Discipline:** network science, specifically flows on social networks and credit networks.

**Question:** How much liquidity does a credit network lose when borrowing is restricted to paths of
length one, and where does the multi-hop gain come from?

**Answer in one line:** One hop roughly halves the liquidity available to borrowers without credit,
and the whole multi-hop gain comes from intermediaries relaying credit they could not pay for.

## Journals

| | Journal | Publisher | Why it fits | What a submission would need |
| --- | --- | --- | --- | --- |
| 1 (primary) | Network Science | Cambridge University Press | An interdisciplinary journal for mathematical, computational and empirical work on networks in any field, including network models of economic exchange. The paper's flow formulations, graph families and steady-state simulation are its core methods. | Format to the journal's template; expand the related work on credit networks and on flows in social graphs; add one empirical social graph to the synthetic families if a suitable public one exists. |
| 2 | Journal of Complex Networks | Oxford University Press | Publishes theory and applications of complex networks, with room for flow problems and simulation studies on network models. | Strengthen the analytic side: a bound on one-hop liquidity as a function of degree and holder share, which the sweeps suggest. |
| 3 | Applied Network Science | Springer (open access) | Publishes applications of network methods to concrete systems, including finance, with an emphasis on practical findings. | Lead with the design implications (two hops with opt-in relaying, commit on draw) and shorten the propositions. |

Journal scope for Network Science was checked on 2026-10-05 against
[the journal's page](https://www.cambridge.org/core/journals/network-science). The other two are
from general knowledge of the journals and should be confirmed before a submission. The Journal of
Network Theory in Finance was considered and set aside: it is closed for submissions.

## In scope

- The regimes: one hop, length-bounded flows, unbounded flow, a centralised lender, and the
  path-liable network.
- The equivalence of path-liable routing and one hop.
- Liquidity for a single borrower and in the steady state, sweeps over degree, holder share and
  trust, and the issued credit one hop needs for the same service.
- Who stands behind a routed loan.
- Sybil extraction as a cut in each regime.

## Out of scope (other papers)

| Topic | Discipline | Where it goes |
| --- | --- | --- |
| Loss bounds and Sybil-proofness of the one-hop protocol | Economics and computation | `conserved-credit` |
| Pricing the credit that backing creates | Credit risk | `pricing-and-reserve` |
| How holders choose whom to back, and whether backing lowers default | Development economics, game theory | Not yet a paper |
| How the issuer sets lines | Credit scoring | `issuer-policy` |

A new result belongs in this paper only if it answers the question above. Anything else starts its
own directory with its own journals file.
