"""Revolving first-job payment guarantee: break-even contribution and finite-pool ruin by simulation.
Per job: with prob p the client defaults and the pool pays G (worker owes nothing);
with prob 1-p the client pays, and the worker remits r with prob q. Every job costs the pool c.
Ruin = the reserve cannot cover the next guarantee (reserve < G) with jobs still to run.
Exposure rule: one open guarantee at a time (sequential), so the pool never promises more than it holds."""
import random, sys
def r_break_even(p, q, G, c): return (p*G + c) / ((1-p)*q)
def sim(u, p, q, G, c, r, jobs, trials=20000, rho=0.0, cluster=5, seed=1):
    rnd = random.Random(seed); ruined = 0; served = 0
    for _ in range(trials):
        R = u; n = 0
        while n < jobs:
            if R < G: ruined += 1; break
            # correlated shock: with prob rho a cluster of `cluster` jobs shares one client outcome
            k = cluster if rnd.random() < rho else 1
            default = rnd.random() < p
            for _ in range(k):
                if n >= jobs or R < G: break
                R -= c
                if default: R -= G
                elif rnd.random() < q: R += r
                n += 1
        served += n
    return ruined/trials, served/trials
if __name__ == "__main__":
    # Reproduces every simulated figure cited in DRAFT.md (seed 1, 4,000 trials per row, 500 jobs).
    T = 4000
    print("Section 5 table: $100 reserve, one open guarantee at a time, 500 jobs")
    for p, q, G, c, load in ((0.01, 0.9, 60, 2.0, 0.0), (0.01, 0.9, 60, 2.0, 0.5), (0.03, 0.8, 60, 1.0, 0.5),
                             (0.10, 0.8, 60, 1.0, 0.5), (0.03, 0.9, 20, 2.0, 0.5), (0.10, 0.6, 20, 2.0, 0.5)):
        r = r_break_even(p, q, G, c) * (1 + load)
        pr, _ = sim(100, p, q, G, c, r, 500, trials=T)
        print(f"p={p:.2f} q={q} G={G} c={c} load={load} r={r:.2f} P(ruin)={pr:.3f}")
    print("Reserve size, G=60, c=1, q=0.8, +50% loading")
    for p in (0.03, 0.10):
        r = r_break_even(p, 0.8, 60, 1.0) * 1.5
        for u in (100, 300):
            pr, _ = sim(u, p, 0.8, 60, 1.0, r, 500, trials=T)
            print(f"p={p:.2f} u={u} P(ruin)={pr:.3f}")
    print("Correlation: blocks of 5 jobs share one client outcome with probability rho; G=20, c=1, q=0.8, +50% loading")
    for p in (0.03, 0.10):
        r = r_break_even(p, 0.8, 20, 1.0) * 1.5
        for rho in (0.0, 0.2, 0.5):
            pr, _ = sim(100, p, 0.8, 20, 1.0, r, 500, trials=T, rho=rho)
            print(f"p={p:.2f} rho={rho} P(ruin)={pr:.3f}")
