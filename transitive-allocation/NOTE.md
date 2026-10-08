# Consented, stake-rooted, bounded-depth allocation certificates: conservation and default bounds

Technical note, draft for adversarial review (status: **not yet independently reviewed**). It states and proves what
the two-hop router in [microcredit-contract](https://github.com/scottonchain/microcredit-contract)
(`TransitiveStakeRouter`, `StakeVault`, over the pool's manager gate; specification in `docs/TRANSITIVE_STAKE_ROUTER.md`
there) guarantees, marks what it does not, and maps every case to a test. It extends the conserved-credit paper
([conserved-credit](../conserved-credit/)) from one hop to two without changing its conclusion: credit is not
manufactured, and a party never loses more than it put at risk by a consent it signed. Nothing here is a claim about
borrowers' welfare, repayment rates or incentives; those are empirical and are not addressed.

## 1. Model

**Parties.** Roots R, mids M, borrowers B are sets of addresses; they may overlap as sets but the router refuses a
certificate in which a path's root, mid and borrower are not pairwise distinct (Lemma 7). Lenders L deposit to the pool.
USDC is conserved except by mint, which the model does not allow to the router or the vaults.

**Router state.** For each root r: `free[r]`, `locked[r]`, `loss[r]`, and the model-only totals `D_r` (deposited) and
`W_r` (withdrawn). For each edge key e = (from, to, borrower): `used[e]` (live exposure) and `version[e]`. For each
borrower b at most one open lot `ℓ_b = (loanId, A, ((r_i, m_i, a_i))_{i<=n})` with `1 <= n <= 4`, `a_i > 0`,
`A = Σ a_i`. Each borrower has a vault `v_b`, a contract that only the router can drive.

**Consent.** `C = (from, to, borrower, limit, maxTerm, version, expiry)`, signed (EIP-712, ERC-1271 accepted) by `from`.
A path i for borrower b carries a root consent `C_i^r` with `from = r_i`, `to = m_i`, `borrower = b` and a mid consent
`C_i^m` with `from = m_i`, `to = b`, `borrower = b`.

**Operations.** `deposit`, `withdraw` (root); `revokeEdge(to, b)` (any signer, for its own edges); `originate(b,
request, poolSig, paths)` (anyone); `sync(b)` (anyone). Environment actions on the pool that the router does not
control: anyone repays any open loan any amount; anyone calls `markDefaulted` after the loan is `LATE_PERIOD` past
due; anyone stakes and backs `b` alongside the vault; anyone sends USDC to the router or a vault.

**Admission (`originate`).** Given a borrower-signed pool request of amount `A_req`, term `T` and paths P_1..P_n, the
router (in this order, in one transaction): requires `managerOf(b) = router`; runs `sync(b)` and requires no open lot;
for i = 1..n checks distinctness, then for each of `C_i^r`, `C_i^m` with edge key e: `version = version[e]`,
`now <= expiry`, `T <= maxTerm`, a valid signature by `from`, and `used[e] + a_i <= limit`, then sets `used[e] +=
a_i`; requires `free[r_i] >= a_i` and moves `a_i` from `free[r_i]` to `locked[r_i]`; requires `Σ a_i = A_req`; sends A
to `v_b`, which stakes it and calls `back(b, A)`; requires the pool to report the vault's backing as `secured = A`,
`unsecured = 0` and `grantedCredit(v_b) = 0`; calls the pool's `borrowAndDisburseMeta` as manager; checks the new loan.
Any failure reverts the whole transaction.

**Release (`sync`).** If the lot's loan is `Repaid`, `Defaulted` or `Cancelled`: the vault calls `back(b, 0)`, unstakes
its entire stake and sends it to the router: `returned`. With `returned' = min(returned, A)` and `L = A - returned'`
the loss, the router computes shares `s_i` by the rule in Lemma 5, then for each path: `used[e_i^r] -= a_i`,
`used[e_i^m] -= a_i`, `locked[r_i] -= a_i`, `free[r_i] += a_i - s_i`, `loss[r_i] += s_i`; deletes the lot.

## 2. What the pool provides (axioms, each tied to code and a test)

These are properties of `DecentralizedMicrocredit` the proofs use. They are facts about the pool, checked by its own
suites, not proved here.

- **P1 (secured by construction).** If `grantedCredit(v) = 0` and v has no backing of b, then after `stake(x)` and
  `back(b, x)` the pool holds `stakeOf[v] = x`, `stakeCommitted[v] = x`, and v's edge on b is `secured = x`,
  `unsecured = 0` (`_setBacking`: free credit is `min(granted - committed, available) = 0`, the rest comes from free
  stake). Tests: `ColdStartFacts`, `SybilResistance`, `TransitiveStakeRouter` (`testTwoHopLoan...`).
- **P2 (stake moves only by its owner or a default).** `stakeOf[v]` rises only in `stake` called by v and falls only in
  `unstake` called by v (not below `stakeCommitted[v]`) and in `_chargeBackers`. No one can credit stake to v.
- **P3 (charge on default).** `markDefaulted` on an `Active` loan of b with unpaid principal `U = principal -
  principalRepaid` charges `fromStake = min(U, Σ_j secured_j)` to b's backers j, each `floor(fromStake · secured_j /
  Σ secured)`, slashed from their stake into the pool's cash; the rest of the loss falls on the first-loss reserve, then
  lenders. When b has no other open loan, the remaining backing of every backer is released.
- **P4 (exclusive outcomes).** A loan ends `Repaid`, `Defaulted` or `Cancelled`, once; `_chargeBackers` runs only in
  `markDefaulted`. So a `Repaid` loan never charged any backer.
- **P5 (gate).** With `managerOf[b] = router`, `_originateLoan` (hence `requestLoan`, `requestLoanMeta`,
  `borrowAndDisburseMeta`) accepts only the router as caller; `setManager` reverts while b has principal outstanding
  (including a requested loan) or any backing (CI-31; `ManagerGate.t.sol`).
- **P6 (release).** `back(b, 0)` by v with no open loan of b needing the backing frees v's edge and its
  `stakeCommitted`, after which `unstake` of the whole stake succeeds.

## 3. Results

### Theorem 1 (ledger conservation)
In every reachable state: (a) `Σ_r free[r] = totalFree`, `Σ_r locked[r] = totalLocked = Σ_b A_b` over open lots;
(b) the router's USDC balance equals `totalFree` plus USDC sent to it outside `deposit`; (c) for every root,
`D_r - W_r - loss[r] = free[r] + locked[r]`; (d) for every edge e, `used[e] = Σ a_i` over open paths whose edge is e.

*Proof.* Induction over operations, from the empty state where everything is 0. `deposit` adds x to `free[r]`,
`totalFree`, `D_r` and the balance (the balance difference is checked to equal x, so fee-on-transfer tokens are
refused). `withdraw` subtracts x from `free[r]`, `totalFree`, adds to `W_r`, and sends x. `revokeEdge` touches only
`version`. `originate` moves `a_i` from `free` to `locked` per path (so (a) and (c) are unchanged), raises `used[e]` by
`a_i` for the path's two edges (d), sends `A = Σ a_i` out of the router: the router's balance falls by A and `totalFree`
falls by `Σ a_i = A` (b). `sync` returns `returned' = A - L` USDC to the router's balance (the vault sends its entire
stake; `returned'` is the part it accounts, `returned >= returned'` and any excess is outside-sent USDC), and credits
`Σ (a_i - s_i) = A - L` to `free` and `L` to `loss`: (b), (c), (a) hold because `Σ s_i = L` (Lemma 5) and
`locked` falls by `Σ a_i = A`. (d): each `used` falls by the path amount it was raised by. Operations of the
environment (repay, default, third-party backing, donations) do not write router storage; a donation raises the balance
and is the "outside-sent" term in (b). ∎

### Theorem 2 (no resource counted twice; global reservation)
For every root r in every state, `locked[r] <= D_r - W_r` and `locked[r] = Σ a_i` over r's open paths. In particular
the same USDC cannot back two paths: parallel paths of one certificate, paths of different certificates, a root used
under two mids, or a root appearing in several lots are all debited from the one `free[r]` before they are admitted.

*Proof.* `free[r] >= 0` is enforced by the explicit `free[r] >= a_i` check before each path's debit, and paths are
processed one after another, each seeing the previous debit. By Theorem 1(c) `free + locked = D_r - W_r - loss[r] <=
D_r - W_r`, and `free >= 0`, so `locked <= D_r - W_r`. ∎

### Theorem 3 (cover): every router loan is secured by the roots' USDC
In every state with an open lot of b: the vault's stake is `A`, its backing of b is `secured = A`,
`unsecured = 0` (while the loan is `Active`), and `A = Σ a_i` equals the loan's principal.

*Proof.* Admission requires the pool to report exactly this after `back` (P1 gives it; the router verifies it, and
reverts otherwise) and then the new loan's principal equals `Σ a_i`. Until release only the pool's `_chargeBackers`
(a default, after which the loan is not `Active`) can lower the vault's stake (P2), and the vault never unstakes
before release. ∎

### Theorem 4 (consent bound): a root's exposure is what it signed
For every open path i and each of its two edges e with consent `C`: at admission `now <= C.expiry`, `C.version =
version[e]`, `T <= C.maxTerm`, `from` signed `C`, and `used[e] <= C.limit` immediately after the path was admitted. After
admission the root's loss from that lot is at most `a_i` (Theorem 5), and `locked` never exceeds the deposit
(Theorem 2). A later `revokeEdge` does not release a live lot (it changes only `version`), and it makes every earlier
consent of that edge unusable for new admissions.

*Proof.* Direct from the admission procedure; the loss bound is Theorem 5. ∎

*Remark (what the bound is not).* The limit is a cap on **live exposure along an edge at the moment of use**, not a
cumulative budget and not a per-borrower promise: a consent can be presented again after the earlier lot closes, until it
expires or is revoked. Consents of one version on one edge are interchangeable: the limit applied is the one on the
consent presented. A signer wanting a single use sets the limit to that use and revokes after.

### Lemma 5 (attribution)
Let `L` be the lot's loss, `0 <= L <= A`. The router sets `s_i = floor(L·a_i/A)` and then adds one unit, in path
order, to each of the first `L - Σ s_i` paths that still have `s_i < a_i`. Then: (i) `Σ s_i = L`; (ii) `0 <= s_i <=
a_i`; (iii) `floor(L·a_i/A) <= s_i <= floor(L·a_i/A) + 1`.

*Proof.* Each `floor` loses a fractional part below 1, so `ρ := L - Σ floor < n`. If `L = A` then `floor(L·a_i/A) = a_i`,
`ρ = 0` and nothing is added. If `L < A`, then `L·a_i/A < a_i`, so `floor(L·a_i/A) <= a_i - 1`: every path has room for
one unit, so the first `ρ <= n - 1` paths each take one, and the residual is exhausted: (i), (ii), (iii). ∎ (Fuzzed:
`testFuzzAttributionSumsToTheLossAndNeverExceedsAPath`.)

### Theorem 5 (loss bound and attribution)
When the lot's loan has closed and been synced: if it ended `Repaid` (or `Cancelled`) every root's loss is 0 and every
root recovers its full path amounts. If it ended `Defaulted` with unpaid principal `U`, the total loss `L = Σ_r loss
≤ U ≤ A`, and equals `U` when the vault is the borrower's only backer; each root `r` loses `Σ_{i: r_i = r} s_i ≤ Σ_{i:
r_i = r} a_i`, within one unit per path of its pro rata share; mids lose nothing on chain.

*Proof.* `Repaid`: by P4 no charge happened, so the vault's stake is still `A` (P2) and `returned = A`, `L = 0`,
all `s_i = 0`. `Defaulted`: by P3 the vault was charged `floor(min(U, Σ secured) · A / Σ secured)`. Since `A <= Σ
secured` (the vault is among the backers) and `U <= A`, `min(U, Σ secured) = U` and the charge is `floor(U·A/Σ
secured) <= U`, with equality when `Σ secured = A`. By P2 nothing else changed the stake, and on release it is
unstaked in full (P6): `returned = A - charge`, so `L = charge`. Lemma 5 distributes it. The router touches no mid's
funds: mids hold no deposit in the router. ∎

### Theorem 6 (lender cover)
Let a router loan of b default with k backers on b at that moment. The pool recovers from backers' stake at least
`U - (k - 1)` base units of the written-off principal, and exactly `U` if the vault is the only backer; lenders therefore
lose at most `k - 1 <= 31` base units of principal on that loan, plus unpaid interest, before the first-loss reserve
(which absorbs it first).

*Proof.* By P3 the pool charges `floor(U·σ_j/Σσ)` to each backer j; the floors sum to at least `U - (k - 1)`, and to `U`
when `k = 1` (`σ_v = Σσ`). `MAX_BACKERS_PER_BORROWER = 32`. ∎ (Invariant R5 bounds the pool's total assets below by the
deposit less the handler-tracked dust.)

### Theorem 7 (Sybil neutrality at the router)
Let X be any set of addresses controlled by one entity. Consider the lots whose borrower is in X, and suppose that in
them every root, every mid and every consent comes from X (no outsider consented to route to X or deposited to be
routed to it), and that no address outside X backs an address of X in the pool. Then the entity's net USDC position on
those lots (principal drawn + stake returned - deposits - repayments) is at most 0, and is 0 only if no interest was
paid and nothing was lost. Splitting into many roots, mids and borrowers therefore creates no credit.

*Proof.* Fix one lot of principal `A`. Its paths' roots are in X, so by Theorem 2 the lot is covered by `locked` USDC
the entity itself deposited: its cost is `A`. The entity draws `A` from the pool and the lot returns `A - L`. Let the
repayments be `P`, of which `P'` is principal (`P >= P'`, `P - P'` interest). The net is `A + (A - L) - A - P = A - L
- P`. If the loan is repaid in full, `L = 0` and `P = A + I`, so net `= -I <= 0`. If it defaults, the vault is the sole
backer (no outsider backs X), so by Theorem 5 `L = U = A - P'`, and net `= P' - P = -(interest paid) <= 0`. A loan open
at the end has not yet returned its lot and the entity holds `A` in a locked deposit against a debt of at least
`A - P'`: its position is no better. Summing over lots gives the claim. ∎

*Remark.* If outsiders do back X's borrowers at the pool, the slash is shared and the entity's loss on a default is
smaller than `U`; the difference is exactly the outsiders' slashed stake, a transfer from backers who consented to put it
at risk, not a creation of credit. The theorem also does not address a Sybil entity that receives credit from
outside the router (an issued line, dues): those are bounded by the pool-level theorems (`docs/CREDIT_MODEL.md`) and do
not flow through this contract.

### Lemma 7 (distinctness, cycles and aliases)
A certificate with a path whose root, mid and borrower are not pairwise distinct, or in which any of them is the
router, is refused. With depth 2 and roles fixed (root → mid → borrower) there is no longer cycle. *Limit:* distinct
addresses of one person are not detected; Theorem 7 is the statement of what that costs.

## 4. Dynamic cases

| Case | Status | Statement and where it is checked |
| --- | --- | --- |
| Partial repayment | holds | The lot stays locked until the loan closes; at a default the loss is the unpaid principal's charge (Thm 5). `testPartialRepaymentThenDefault...`; handler `repay` (fractions), invariant sync checks (loss = model of interest-first repayment). Limit: no early partial release of the lot. |
| Third-party repayment | holds | Anyone may repay at the pool; the borrower's pool capacity frees but the gate keeps every origination path closed (P5). `testCertifiedLoanRepaidDirectly...`; handler `attemptDirect` (about 2,800 attempts, none succeeded). |
| Cancellation | holds by atomicity | `borrowAndDisburseMeta` leaves no `Requested` loan; if the pool call reverts, the whole admission reverts. A `Cancelled` status is treated as closed, with `returned = A`. Not reachable through the router. |
| Simultaneous reservations | holds | Serialised by the chain; the second certificate sees the first debit (Thm 2). `testOneRootTwoBorrowersCannotOverdraw...`; invariants R1 to R3. |
| Stake exit | holds | Roots withdraw only `free`; the vault unstakes only inside `sync`; no one else can move vault stake (P2). `testRootCannotWithdrawALockedLot...`. |
| Rounding residuals | holds | Lemma 5 (router side), Thm 6 (pool side, at most k-1 units). Fuzz and invariant R5 with tracked dust. |
| Legacy grants | holds | The vault holds no granted credit (checked at admission), the loan is covered by the vault's stake first (P3: secured before unsecured), so a borrower's issued line or dues never shift loss away from roots nor onto them. A borrower with `defaultedLoans > 0` cannot be backed (`BorrowerInDefault`). `testDefaultedBorrowerCannotBorrowAgain...`. |
| Default charged along the path | holds | Thm 5, Lemma 5; mids bear nothing on chain. |
| Third-party backer on the same borrower | holds | The slash is shared pro rata by the pool; roots lose less; lenders' rounding dust (Thm 6). `testAThirdPartyBackerShareTheSlash...`; handler `thirdPartyBack` (about 2,800 backings, about 150 shared-slash defaults). |
| Revocation, expiry, stale version | holds | Thm 4. `testRevokedConsent...`, `testConsentExpiryVersionSigner...`, limit boundary test. |
| Stale sync | holds | A closed loan's lot stays locked until `sync`; every origination syncs first; anyone may call. Liveness, not safety. |
| Donations to router or vault | holds | Thm 1(b); the vault returns only what it staked. `testDonationToTheVault...`, handler `donate`. |
| Replay | holds | The pool nonce is consumed by the borrower's request; consents are reusable by design (Thm 4 remark). |
| Pool owner actions | **open** | The pool's owner, guardian and oracle can pause, change parameters, set a score override for an address (the router refuses an origination if the vault has granted credit; an override set later does not change a lot already backed). The theorem assumes the pool is the audited bytecode with the owner not acting against it; this is the standing assumption of the whole project. |
| Pool 32-backer slot limit | **open (liveness)** | A griefer can fill a managed borrower's 32 backer slots with 1 USDC backings; the vault's `back` then reverts. Safety is unaffected; the borrower must use another address. |
| Token behaviour | **open** | USDC blacklisting or pausing could trap a root's withdrawal or the vault's return. The router assumes a token without transfer fees or hooks (checked by the deposit balance difference). |
| Mid incentives | **open** | A mid has no capital at risk, so nothing here bounds a mid's incentive to vouch for a bad borrower; the roots bear the cost, bounded by their consents. Mid first-loss capital needs its own theorem. |
| Depth above two | **open** | Not implemented. A third hop would need the same reservation argument for an edge that is both a mid's and a root's; not proved here. |

## 5. Fixture list mapped to the invariant handler

Handler: `test/invariant/RouterHandler.sol`; campaign: `invariant/TransitiveStakeRouter.invariant.t.sol` (R1 to R6).
Unit suite: `test/TransitiveStakeRouter.t.sol` (31 tests).

| Fixture | Handler action or test | Checks |
| --- | --- | --- |
| Sybil rings (many roots, mids, borrowers) | `originate` with 1 to 4 paths over 3 roots, 3 mids, 6 borrowers | R1 to R4, Theorem 7 by construction (all USDC is root USDC) |
| Parallel paths, same root under two mids | `originate` | R3 per-edge exposure; `testRepeatedRootEdge...` |
| Diamond (shared mid edge) | `originate` with tight mid limits | `LimitExceeded` is a documented refusal; `testSharedMidEdgeLimitBindsAcrossRoots` |
| Cycle, alias (root = mid, mid = borrower, root = borrower, router) | unit tests | `testRootCannotBeItsOwnMid...` |
| Partial repayment, then default | `repay` (fractions), `warp`, `defaultOne` | sync checks against the model of interest-first repayment |
| Concurrent certificates for one root | `originate` over shared roots; `InsufficientFree` documented refusal | R1, R2, R3 |
| Root withdrawal while locked | `withdraw` (also tries `free + 1`) | violation counter |
| Stale sync | `syncOne` ordering vs `originate` (which syncs first) | R4 |
| Manager gate bypass after direct repayment | `attemptDirect` (three paths) after any state | violation counter |
| Third-party backer, shared slash, dust | `thirdPartyBack`, `thirdPartyUnback`, `defaultOne` snapshot | sync check, R5 with dust |
| Revocation and version | `revoke` | consents are rebuilt at the new version; unit tests for old versions |
| Donations | `donate` (router and vault) | R1, sync checks |
| Not yet in the handler | pool owner actions (pause, parameter changes, overrides), blacklisted token, a smart-wallet root in the campaign | listed as open above; a smart-wallet root is a unit test |

**Mutation check.** Ten deliberate bugs in the router and one in the pool's gate are each caught by these suites
(see the pull request description for the list).

## 6. What this does not show

No claim of repayment, incentive compatibility, welfare, or any property of the pool's off-chain issuer or of how roots
are found. No claim about an adversary who controls the pool's owner key, the token or the chain. The result is that
**nothing is created**: every unit a borrower draws through the router is a root's USDC held as the borrower's secured
backing, each root's exposure is bounded by what it signed and deposited, a default is charged to the roots pro rata
and not beyond their paths, and lenders are made whole up to the pool's own rounding.
