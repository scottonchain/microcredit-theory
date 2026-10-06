# Referee report: microcredit-theory

**Recommendation: major revision before journal submission.**

**Reviewed version:** [`b84b916656c1724188597b94bec5f8b1b9e7c9a0`](https://github.com/scottonchain/microcredit-theory/tree/b84b916656c1724188597b94bec5f8b1b9e7c9a0).
**Supporting code:** microcredit-contract [`b725a852b923a885ded30152e80cb9f86eb1d430`](https://github.com/scottonchain/microcredit-contract/tree/b725a852b923a885ded30152e80cb9f86eb1d430), the version cited by the papers.
**Date:** 6 October 2026 UTC / 5 October 2026 America/Denver.
**Reviewer:** Codex, an OpenAI AI assistant, commissioned by the project's operator. The exact serving model identifier is not available to this review. This is an internal, operator-requested referee-style assessment, not an independent outside review, journal decision, security audit, or completion of the independent-review milestone in issue #1. No subagents were used.

## Overall assessment

The strongest contribution is the explicit accounting of credit commitments, realised losses, and residual exposure in *Conserved Credit*. In particular, distinguishing cash recovered from stake from credit burned against an unsecured backer is essential and is handled carefully. The fixed-line invariant and its induction appear sound under the stated exact-arithmetic state machine; I found no counterexample to Lemma 5.1, Theorem 5.3, or the reserve corollary in this pass. The changing-line result appropriately bounds current exposure rather than lifetime losses across an unlimited succession of newly funded accounts.

The repository is unusually inspectable: complete sources, generated tables, pinned supporting code, and recorded adverse tests are available. My reruns of the locked-reserve simulation and the base lending-equilibrium calculation reproduced the tracked outputs byte for byte. Reproducibility is therefore a substantive strength. It does not, however, establish that the model is the right economic model or that every interpretation of its results follows.

The principal weaknesses are stronger claims in prose than in the actual propositions; a conflation of ordinary cuts with length-bounded flow duals; incomplete specification of the attacker's profit benchmark; and economic recommendations that combine long-run returns with finite-horizon risk and capital costs. Several numerical studies validate a deliberately favourable data-generating model, rather than testing whether their conclusions survive plausible misspecification.

| Paper | Assessment of the examined core | Main revision needed |
| --- | --- | --- |
| Conserved Credit | Fixed-line accounting proof appears supported | Narrow the advertised guarantee; make implementation error bounds and validation coverage explicit |
| Pricing and Reserve | Reserve identity and bounded/i.i.d. loss version of the long-run formula appear supported | Repair horizon notation, qualify tail claims, and connect reserve timing to an actual finite pool |
| One Hop or Many | Path-liable equivalence appears supported | Correct the three-hop cut argument and the interpretation of equivalent service |
| Issuer Policy | Concavity and restricted allocation argument are useful | Define the profit and identity guarantees precisely; validate scoring under misspecification |
| Lending Equilibrium | Rate identity and yield-only incidence derivation appear supported | Reconcile time horizons and restrict the liquidity and policy conclusions |

This review concerns all five manuscripts and selected supporting code. It is not a line-by-line verification of the Solidity implementation. Scope and execution receipts are recorded below.

## Conserved Credit

Source: [`conserved-credit/paper.tex`](https://github.com/scottonchain/microcredit-theory/blob/b84b916656c1724188597b94bec5f8b1b9e7c9a0/conserved-credit/paper.tex).

### C1 — State precisely what “Sybil-proof” establishes [major: claim scope]

**Locations:** abstract; Sections 4–7; discussion and conclusion.

The results bound losses by resources and external commitments; they do not show that no attacker can profit, that social manipulation is prevented, or that a live issuance budget limits lifetime loss. The paper itself correctly gives a profitable colluding-backer example, a pooled-reserve exception, and repeated loss through budget reuse. Those qualifications should travel with the headline guarantee.

There are also three distinct right-hand sides: fixed issued lines for cumulative loss; peak/held lines for current exposure; and cumulative unsecured commitments across a coalition boundary. The latter is not simply the capacity of the current graph cut. Repeatedly cut and recommit the same edge and its cumulative commitment grows even if its present capacity does not.

**Requested revision:** put these guarantees and their domains in one theorem-summary table. Use “loss bounded by issued resources and cumulative external commitments” where that is the actual result. Explain separately whether a conventional strategy-comparison definition of Sybilproofness is proved. The sentence after Corollary 5.5 that dues cost lenders nothing should say that dues add no *uncovered principal-loss budget* under that corollary; the pricing papers show that withholding the corresponding interest can cost lenders yield.

### C2 — Complete the bridge from the real-arithmetic theorem to the implementation [major: validation scope]

**Locations:** Remark 3.3, Section 8.2–8.3, implementation appendix; `data/mutation.csv`.

The paper acknowledges integer division and forgiveness of balances below one cent, but the implementation-facing guarantee still relies on a qualitative correction. Repeated small forgiveness events are not bounded by a single cent over the lifetime of the system. Likewise, a fixed-line fuzz campaign does not establish changing-line safety, and a symbol-to-function table is not a refinement proof.

The disclosed mutation results are informative: eleven mutants are detected by fuzzing; three require unit tests, including self-backing and reserve release. I reproduced that summary from the committed records. This is a known coverage gap acknowledged by the authors, not a newly discovered implementation failure.

**Requested revision:** state an explicit cumulative error term indexed by affected defaults, backing edges, and forgiven closures, then state the integer-arithmetic version of the guarantee. Document which changing-line and budget-release transitions are covered by which harness. Add targeted adversarial sequences for the three acknowledged harness gaps before advertising coverage of every implemented bound. Distinguish a separately coded test oracle from an independently operated reviewer.

### C3 — Constrain the farming theorem to the mechanism class actually proved [clarification]

**Locations:** Definition 7.1, Theorem 7.2, Corollary 7.3.

The proof needs a history that can be reproduced across arbitrarily many fresh accounts, leaves usable uncharged credit, and permits that credit to be disbursed under the lending rules. Finite capital for one execution alone does not state all of these properties. The theorem includes a liquidity proviso, but the “no lending protocol” formulation of the trilemma hides it and the account-local credit-rule assumptions.

**Requested revision:** state the replication/admissibility assumptions and the profit benchmark explicitly, and quantify the trilemma over that class. This preserves the useful attack construction without presenting it as a theorem about every possible lending protocol.

## Pricing Uncollateralized Microcredit

Source: [`pricing-and-reserve/paper.tex`](https://github.com/scottonchain/microcredit-theory/blob/b84b916656c1724188597b94bec5f8b1b9e7c9a0/pricing-and-reserve/paper.tex).

### P1 — Conditional independence does not justify annualising the marginal per-loan PD [major: mathematical specification]

**Location:** Proposition 1 and its use alongside the one-factor model in Section 4.

If the per-loan default probability varies with a persistent factor, the correct marginal relationship is

\[
\mathrm{PD}=1-\mathbb E[(1-p_T(Z))^n],
\]

not generally \(1-(1-\mathbb E[p_T(Z)])^n\). The scalar formula is valid for a homogeneous hazard, or conditionally with both sides indexed by the factor. The proposition states conditional independence but writes unconditional-looking quantities.

A check using the manuscript's Gaussian factor model at annual PD 5%, correlation 0.15, and \(n=365/30\) gives marginal per-loan PD 0.4293355%; applying the scalar conversion to that marginal gives 5.1001707%, rather than 5%. This is a notation/assumption error; it does not show that the conditional re-lending transform in Proposition 2 is wrong.

Also, repeated independent loan outcomes give a geometric number of completed cycles until default. An exponential default time and fractional cycle counts require a continuous-hazard interpolation; they do not follow from discrete independence alone.

**Requested revision:** distinguish conditional probabilities, marginal probabilities, and the homogeneous illustrative conversion. State the continuous-time convention and avoid converting a reported institutional repayment rate to annual borrower PD unless its denominator, cohort, and rollover assumptions match.

### P2 — Remove the claimed Gaussian lower bound [major: unsupported mathematical claim]

**Location:** first item of Section 7, “Limitations.”

The statement that the reported quantiles are lower bounds at a given correlation does not follow from choosing a Gaussian factor. Correlation does not order all upper-tail loss quantiles. Adding independent Gaussian factors can preserve the same Gaussian latent covariance and give exactly the same distribution; alternative dependence structures can move different quantiles in different directions.

**Requested revision:** replace “lower bounds” with an explicitly model-conditional statement. If conservatism is important to the pricing recommendation, provide specified alternative copulas/factor dynamics and report their effects. A correlation sweep is useful but does not establish robustness to dependence outside that family.

### P3 — Keep the valid reserve identity separate from a claim about an operating pool [major: economic model]

**Locations:** Sections 4.2, 5, 6; `scripts/locked_reserve.py`.

The pathwise accounting identity is convincing within the specified recursion. That recursion receives a full year's deterministic interest before paying that year's losses, maintains constant exposure and deposits, and uses an infinitely granular conditional loss rate. The real protocol receives interest when individual loans repay, can experience defaults before that inflow arrives, and lends from a balance sheet that changes after losses and withdrawals. These differences matter most during reserve formation, where the paper's protection claims are strongest.

The instantaneous replacement assumption also differs from the contractual write-off delay. The paper acknowledges a revolving simulation, but the recommendation adds the *static* portfolio granularity adjustment to the transformed replenished quantile. That combined approximation needs its own validation; validation of its two ingredients separately is not sufficient.

**Requested revision:** specify what replenishes losses and keeps the exposure base constant. Add an event-timed, finite-pool check with the stated origination, interest, maturity, and write-off rules. Report the error of the combined replenishment/granularity approximation and first-year reserve coverage. Retain the accounting and long-run results as conditional theorems, not evidence that those omitted mechanisms are immaterial.

## One Hop or Many

Source: [`one-hop-liquidity/paper.tex`](https://github.com/scottonchain/microcredit-theory/blob/b84b916656c1724188597b94bec5f8b1b9e7c9a0/one-hop-liquidity/paper.tex).

### N1 — Proposition 2 needs an LP-dual argument for three-hop flow [major: proof correction]

**Locations:** Proposition 2 and its proof; Section 4, length-bounded flows; Table 5.

The ordinary max-flow/min-cut theorem does not directly prove the stated equality for every regime. The paper itself explains that three-hop flow has shared-capacity constraints across positions and is not an ordinary flow on an unconstrained layered graph. The supporting implementation correctly distinguishes the LP dual: `analysis/liquidity/model.py::khop_dual` explicitly calls it a fractional length-bounded cut. That distinction disappears in the manuscript's proof.

For a simple five-node path, with credit 100 only at node 0 and capacity 25 in each direction on each edge, the ordinary flow/minimum cut to node 4 is 25, whereas the three-hop flow and its LP dual are both zero. My execution returned `(25, 25)` and `(0, 0)` respectively. This example shows why an ordinary cut is insufficient; it is not a counterexample to correctly stated LP duality.

**Requested revision:** state separate equalities for ordinary flow networks and for the three-hop path/position LP with its explicitly defined dual. Prove the bound \(gc\) and invariance under the number of Sybil sinks directly by terminating paths at their first Sybil node; those conclusions can survive this correction. Rename the three-hop “cut” column accordingly. The implementation already provides much of the required distinction.

### N2 — “Equivalent service” changes the set of borrowers [major: experimental interpretation]

**Locations:** Section 5.2; supporting `analysis/liquidity/run.py::equivalence_settings` and `task_steady`.

Increasing the holder share also removes accounts from the borrower population, because holders never borrow. The equivalence experiment further rescales the simulated duration by \((1-q)/(1-q_0)\), maintaining the intended request intensity per remaining borrower. That is a coherent experiment, but it does not measure the extra issuance required to serve the *same borrowers with the same demand*. The headline “two to four times the issued credit for the same service” is stronger than the experiment.

**Requested revision:** either qualify the estimand as service to the remaining nonholder population under this rescaling, or add a fixed borrower cohort and fixed demand process while varying available backing resources. Report uncertainty across graph and holder-set draws; five time batches from a single steady-state graph do not measure between-network uncertainty. Treat the fresh-network borrower observations as clustered within their three graphs.

### N3 — Credit capacity is not cash solvency [clarification]

**Locations:** title; Proposition 1 interpretation; discussion.

The path-liable equivalence follows from the defined throughput constraint. It is useful, but it is not a general theorem that solvent intermediaries eliminate gains from intermediation. An issued line can be burned without recovering any cash, as the companion paper carefully explains. “Can pay,” “solvent,” and “bears the loss” should distinguish a debit to future borrowing capacity from cash compensation of lenders. State exactly which contractual liability or collateral the throughput constraint represents.

## Issuer Policy

Source: [`issuer-policy/paper.tex`](https://github.com/scottonchain/microcredit-theory/blob/b84b916656c1724188597b94bec5f8b1b9e7c9a0/issuer-policy/paper.tex).

### I1 — Define the profit benchmark and preserve the known pooled-reserve qualification [major: guarantee scope]

**Locations:** Proposition 1, its proof, abstract and conclusion; compare *Conserved Credit*, Proposition 7.5.

The proposition claims an upper bound under any strategy, including participation as a lender, but does not fully define the wealth benchmark. If it means total investment profit, ordinary returns from lending to other borrowers must be included. If it means the gain from deviating from passive lending, it must include the benefit when the attacker's dues absorb other borrowers' losses before the attacker withdraws.

The companion paper explicitly calculates that second channel. With \(I=1,r=0.3,f=0,s=0.91\), the direct interest/history term used here is −0.063; the companion's same-stress passive-lender comparison is +0.21, with an additional loss shield of 0.273. The supporting issuer-policy README already discloses the CI-21 residual case, but the manuscript omits it.

This comparison is **not** evidence that the attacker has positive absolute wealth change during the stress, nor a demonstrated attack on the illustrative identity tiers. It shows why “unprofitable whatever the attacker does” needs a precise counterfactual and why the stronger no-profitable-deviation reading has not been established. Honest backing \(H\) is another expressly allowed positive term, so it also needs to be excluded from an unqualified no-profit statement.

**Requested revision:** define initial/final wealth, passive returns, the timing or constancy of lender share \(s\), and all external loss and income terms. Restate the theorem for that benchmark and incorporate, exclude by assumption, or eliminate the pooled-reserve channel. Make the lifetime *identity* constraint explicit: the code makes the first bound address the live one; a future address-rotation mechanism must carry credit charges as well as repayment/default history. One live address at a time alone is not the lifetime invariant.

### I2 — The maximised objective is not yet derived as the pool's expected profit [major: economic specification]

**Locations:** Proposition 2; Section 7 simulation; `analysis/issuer_policy/policy.py::expected_profit` and the allocator.

The calculus for \(\Pi(\ell)=i\mu(1-e^{-\ell/\mu})-p\ell\) is correct. Its economic interpretation is incomplete. Normal demand is specified conditional on not defaulting, while defaulting borrowers draw the whole line and do not pay the stated interest. Even a simplified cash-basis premium-minus-principal-loss objective is therefore

\[
(1-p)i\mu(1-e^{-\ell/\mu})-p\ell,
\]

with optimum \(\mu\log((1-p)i/p)\) when positive. Charging funding on defaulted balances adds another term. Fees, utilisation, and the locked reserve create further distinctions between gross loan surplus and lender return. The issuer does not itself supply the capital, so “issuer profit” also needs a beneficiary and a cash-flow definition.

**Requested revision:** derive the objective from explicit period cash flows and identify whose objective is maximised. If the existing function is a first-order surplus surrogate, label it accordingly and quantify its approximation error. Reconcile the policy's 65% reserve setting and positive “profit” with the companion pricing paper's finding that lenders earn below the funding rate at that setting. The two statements can coexist, but they are not the same profitability criterion.

### I3 — Calibration under the assumed world does not validate the evidence weights [major: statistical validation]

**Locations:** Section 4 and Section 7 calibration; limitations.

The simulation uses the population from which the prior was fitted and generates lateness with the assumed late/default ratio. It is reassuring that the machinery behaves reasonably there, but it does not establish that risk-weighted repayments improve prediction or resist strategic histories. Fractional likelihood weights define a generalized/power update, not automatically a calibrated posterior for the actual observation process. Survivorship, selective lending, delayed outcomes, and weights that depend on loan outcome also need treatment.

**Requested revision:** compare tier-only scoring, unweighted updating, and the proposed weights on the same independently generated borrower paths. Misspecify the tier mix and late/default relationship; include time-varying risk and histories engineered at positive but small cost. Report a proper scoring rule and calibration by exposure and time, with uncertainty respecting repeated observations within borrowers. The narrow statement that selected zero-cost histories receive zero weight is supported; the conclusion that manufactured history is worthless is much broader.

## Lending Equilibrium

Source: [`lending-equilibrium/paper.tex`](https://github.com/scottonchain/microcredit-theory/blob/b84b916656c1724188597b94bec5f8b1b9e7c9a0/lending-equilibrium/paper.tex).

### E1 — The reserve-choice conclusion depends on mixing infinite and finite horizons [major: central economic assumption]

**Locations:** participation model; Proposition 4; Section 9.1.

Lenders evaluate yield over an infinite horizon but principal-loss probability over the first ten years. That particular combination drives the conclusion that some volume-maximising share must cover expected loss. The paper acknowledges that early lenders receive lower finite-horizon returns even below that threshold; the participation rule does not price this cost.

For a lender evaluating expected average return over \(H\) years, the paper's own identity gives

\[
y_H=u[a(1-f)-\mathrm{EL}]-\frac{\mathbb E R_H-k}{H}.
\]

At \(H=1\), the negative-return event is \(uL_1>ua(1-f)+k\), independent of the reserve share. Increasing the share can therefore reduce finite-horizon expected return without improving that safety criterion at all. This is not a counterexample to Proposition 4 under its stated participation rule; it is a direct demonstration that the rule is material to the recommended policy.

**Requested revision:** justify the hybrid horizon or add participation based on a common holding period/discounted utility, including initial reserve state and entry cohorts. Re-evaluate the optimum and near-optimal interval. Volume is also not borrower welfare: the paper correctly disclaims welfare evidence, and the objective should remain labelled as volume maximisation.

### E2 — The one-term exit bound is conditional; the proposed lateness correction is invalid [major: claim correction]

**Locations:** Proposition 5, the paragraph immediately following it, abstract and conclusion.

With a fixed deposit claim, no new lending, uniform maturities, and every loan repaying on time, the basic cash-exhaustion calculation is correct. The abstract's claim that the pool's structure bounds exit by one term omits the repayment assumption. More seriously, replacing the repayment rate \(u\) by \((1-\pi)u\) does not specify when late loans eventually pay and cannot guarantee settlement.

Example: deposits 1, utilisation 0.85, reserve zero, and 10% of the loan book paying only on day 365. Initial cash plus all on-time principal is \(0.15+0.9(0.85)=0.915\). The proposed slowed-rate calculation suggests a full run finishes in 33.33 days. It cannot: the remaining 0.085 is unavailable until day 365. Default instead of late repayment makes the distinction between original deposits and impaired withdrawal claims essential.

**Requested revision:** retain the proposition as an on-time-repayment benchmark. For late/defaulting loans, use a cumulative collection process and the actual queue/share-valuation rules, distinguishing time to receive full face value from time to redeem a reduced claim. Also use \(T(1-c/u)^+\) for a full run; the printed expression becomes negative when the reserve cushion exceeds the loan book. State \(0\le\bar w<T\) for the utilisation inequality.

### E3 — Capital-cost comparisons and policy prescriptions require a common optimisation problem [major: interpretation]

**Locations:** Sections 9.1–9.2 and 11; `scripts/equilibrium.py::section_c`.

The code prices seed capital as \(hk\) per year while matching protection only over ten years. That can represent a perpetual annuity opportunity-cost convention, but it is not automatically the finite-horizon cost of an irreversible contribution with no terminal recovery. At horizon \(H\), the equivalent annual cost of such a contribution discounted at \(h\) is \(kh/[1-(1+h)^{-H}]\). The reserve-share cost is also evaluated with the long-run formula rather than the same finite-horizon cash flows.

Two further prescriptions do not follow from the cited results. With heterogeneous safety tolerances and endogenous rates, Proposition 4 does not imply the general rule \(\max\{r_c,r_{safe}\}\) printed below Table 5; that rule needs a specified single-tolerance, fixed-rate cost-minimisation problem. Nor does the incidence formula restore the original lending volume after a share increase: its own volume derivative is negative.

**Requested revision:** compare the present values of both interventions over the same horizon, stating who funds the seed and whether it earns or recovers anything. Label the single-tolerance rule as a separate problem, and change the incidence interpretation to a market-clearing rate with generally lower volume. Reassess the statement that seed capital is cheaper as a conditional numerical result.

## Further comments and publication contribution

1. **Novelty:** identify what is new relative to the closest cited work, rather than treating an implementation-specific application as a new general theorem. The conservation invariant is the strongest candidate. The reserve recursion is a Lindley process, the incidence calculation is familiar comparative statics, and the one-hop equivalence follows directly from the imposed node capacities. A claim-by-claim comparison with prior work would help establish the incremental contribution. The cited [*Trust Is Risk*](https://eprint.iacr.org/2017/156.pdf), for example, already develops monetary trust and Sybil resilience, in a materially different cash-backed construction; explaining that difference is more useful than a broad claim of solving Sybil resistance.
2. **Paper division:** two manuscripts derive essentially the same locked-reserve return formula. Cite one canonical derivation and give a clear statement of the incremental research question in the other. Splitting into five venue-specific documents does not by itself establish five journal-level contributions.
3. **Proposition 4 proof, lending equilibrium:** the final inequality after choosing \(r_1=\mathrm{EL}/a^*(r_0)\) needs an explicit step. Since \(r_0\) was already a global maximiser, the newly obtained volume must be equal; strict demand monotonicity then makes the rates equal. Without that step the preceding inequality alone gives the opposite direction for the product.
4. **Earned-credit growth:** the exponential in Proposition 6 is a continuous-payment approximation. Under discrete 30-day repayment and redrawing, the corresponding idealised growth factor is \((1+raT/365)^m\), assuming no default and no other binding caps. Label the approximation and quantify its small difference.
5. **Uncertainty of the optimal-share interval:** the reported interval 41.25–50.25% comes from a reserve grid of 0.25 percentage points and interpolation of a coarser safety surface. Provide Monte Carlo/grid sensitivity before interpreting its endpoints precisely. My exact rerun confirms reproducibility, not precision relative to the underlying continuous model.
6. **Long-run theorem assumptions:** in Pricing and Reserve, independence, a common mean, and individually finite variances are not by themselves the usual sufficient strong-law conditions for a non-identically distributed sequence. State i.i.d. losses, bounded losses, or an appropriate variance-summability condition. Lending Equilibrium already supplies boundedness. Avoid asserting recurrence/null recurrence for all independent, nonstationary or degenerate increments when only sublinear reserve growth is needed.
7. **Small-pool risk:** the reserve and equilibrium simulations use conditional asymptotic losses. The separate finite-pool exercise shows idiosyncratic risk matters; carry at least one finite-pool version into the reserve/safety results. Correlated years and loss of interest income during stress are particularly relevant to the early-reserve conclusions.
8. **Deployment language:** distinguish constructor/development defaults, `DeployProduction` settings, and an observed deployment at a date/block. “Deployed” 500 bps and “production” 800 bps refer to different configurations in these sources. Avoid universal statements that all public-chain lending is overcollateralised; restrict the motivation to the cited systems and the stated permissionless setting.

## Reproduction and evidence record

All execution used disposable local checkouts; no manuscript or implementation was changed by the review. The report is the review deliverable.

**Environment:** Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0; NetworkX 3.6.1 installed into an isolated review dependency directory for the network tests. The paper's stated NumPy version differs; the rerun outputs below nevertheless matched.

| Check | Observed result |
| --- | --- |
| `python -m unittest discover analysis/credit_risk` in pinned contract repo | 31 tests, all passed |
| `python -m unittest discover analysis/issuer_policy` | 42 tests run; 41 passed, 1 skipped (optional ABI dependency) |
| `python -m unittest discover analysis/liquidity` | 26 tests, all passed |
| `python -m unittest discover analysis/sybil_sim` | 53 tests, all passed |
| Pricing: `python scripts/locked_reserve.py <contract-checkout>` | Completed; both reserve CSVs and summary macros matched committed files byte for byte |
| Equilibrium: `python scripts/equilibrium.py <contract-checkout>` | Completed for the base 5% PD case; generated base outputs matched byte for byte; 102 macros, EL approximately 0.0515, expected-loss share approximately 0.4176 |
| Conserved Credit: rerun `summarize_fuzz.py` on decompressed committed run records and `fuzz_forge_tail.txt`, arguments `1300 256` | Reproduced 4,326,400 calls, 13 properties, 99.98% maximum global-bound use; output files matched |
| Conserved Credit: rerun `mutation_summary.py` | Reproduced eleven mutants detected by every fuzz seed and three detected by unit tests; output files matched |
| Four-edge path, conditional-PD conversion, and delayed repayment example | Numerical outputs given in N1, P1, E2 and reproducible below |
| PDFs | Extracted text from all five committed PDFs and spot-checked theorem labels/statements against sources; not a fresh TeX build or exhaustive source/PDF correspondence check |

The contract tests above are the repository's existing tests, not new independent proofs. The fuzz and mutation entries reproduce summaries of supplied records; I did **not** rerun the Foundry campaigns or the fork-based pooled-reserve experiment. I did not regenerate the complete graph, issuer, or original credit-calibration experiment grids, nor the 3% and 10% equilibrium robustness runs. Bibliographic checking was selective, not exhaustive. Passing tests should not be used to close a modeling objection without an argument addressing it.

Minimal checks, run from the pinned contract repository with NumPy, SciPy and NetworkX available:

```python
import sys
import numpy as np
import networkx as nx
from scipy.integrate import quad
from scipy.stats import norm

sys.path.insert(0, "analysis/liquidity")
import model as m

net = m.Network.from_graph(nx.path_graph(5), np.array([100., 0, 0, 0, 0]), 25)
state = m.State.fresh(net)
print(m.khop_dual(net, state, [4], 3))       # (0.0, 0.0)
print(m.min_cut(net, state, [4])[:2])        # (25.0, 25.0)

pd, rho, n = 0.05, 0.15, 365 / 30
def annual_conditional(z):
    return norm.cdf((norm.ppf(pd) - np.sqrt(rho)*z) / np.sqrt(1-rho))
pt = quad(lambda z: (1-(1-annual_conditional(z))**(1/n))*norm.pdf(z), -10, 10)[0]
print(pt, 1-(1-pt)**n)                     # 0.00429335537, 0.0510017070

u, late_fraction, term = 0.85, 0.1, 30
print(1-u + (1-late_fraction)*u)           # only 0.915 collected by day 30
print(term/(1-late_fraction))             # proposed correction: 33.3333 days
# If late loans pay on day 365, no cash arrives between days 30 and 365.
```

## Requested author response

Please respond by finding ID (C1–C3, P1–P3, N1–N3, I1–I3, E1–E3), stating agree/disagree/clarify, the supporting argument or experiment, and the revision commit where applicable. Preserve this original report; place responses and any reviewer recheck in a separate record. An evidenced disagreement is an acceptable response. An internal response/recheck does not substitute for the independently operated reviews sought in issues #1–#4.
