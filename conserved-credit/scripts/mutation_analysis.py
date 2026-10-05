#!/usr/bin/env python3
"""Mutation analysis of the credit-invariant fuzzing (Section 8.3).

Seeds one fault at a time into contracts/DecentralizedMicrocredit.sol of a checkout of the
contract repository, runs the invariant suite at its default (inline) size under three fixed fuzz
seeds, records which properties fail, and restores the file. Run it on a disposable worktree, never on a checkout
with work in progress:

    git -C microcredit-contract worktree add --detach /tmp/mutrun b725a85
    ln -s "$PWD/microcredit-contract/lib" /tmp/mutrun/lib   # or init the submodules there
    python3 scripts/mutation_analysis.py /tmp/mutrun

A fault the fuzzing does not detect is then run against the unit tests.

Writes data/mutation.csv; scripts/mutation_summary.py turns it into the table and summary.
"""
import csv
import pathlib
import re
import subprocess
import sys

# (identifier, description for the paper, original source, mutated source)
MUTANTS = [
    ("coverage", "Coverage ignored: unsecured backing always counts in full",
     "total += cover >= committed ? edge.unsecured : Math.mulDiv(edge.unsecured, cover, committed);",
     "total += edge.unsecured;"),
    ("no-burn", "A default does not burn the unsecured backers' credit",
     "if (charged > 0) creditLoss[backer] += charged;",
     "if (charged > 0) {}"),
    ("no-slash", "A default does not slash the secured backers' stake",
     "stakeOf[backer] -= slashed;",
     "stakeOf[backer] -= 0;"),
    ("free-ignores-loans", "Free credit ignores the backer's own loans",
     "credit = Math.min(granted > committed ? granted - committed : 0, available);",
     "credit = granted > committed ? granted - committed : 0;"),
    ("pass-on", "Received backing can be passed on",
     "credit = Math.min(granted > committed ? granted - committed : 0, available);",
     "credit = available;"),
    ("commit-unrecorded", "Backing with credit does not record the commitment",
     "creditCommitted[backer] += fromCredit;",
     "creditCommitted[backer] += 0 * fromCredit;"),
    ("cut-in-use", "Backing can be cut below what the borrower owes",
     "require(_activePrincipal(borrower) <= limit, BackingInUse());",
     "require(true || _activePrincipal(borrower) <= limit, BackingInUse());"),
    ("early-release", "Backing is released at a default while the borrower has other open loans",
     "bool release = activeLoanCount[borrower] == 0;",
     "bool release = true;"),
    ("defaulter-keeps-credit", "A defaulted account keeps its granted credit",
     "if (defaultedLoans[account] != 0) return 0;",
     "// mutated: defaulted accounts keep their credit"),
    ("limit-not-available", "A new loan is checked against the limit, not the unused limit",
     "require(amount <= available, BorrowLimitExceeded());",
     "require(amount <= limit, BorrowLimitExceeded());"),
    ("net-interest-dues", "Dues are credited on interest net of the fee, not the reserve share",
     "duesPaid[loan.borrower] += toReserve;",
     "duesPaid[loan.borrower] += interest - fee;"),
    ("release-dues", "The owner may release dues from the reserve",
     "require(amount + Math.max(totalImpaired, totalDuesPaid) <= firstLossReserve, ExceedsReserve());",
     "require(amount + totalImpaired <= firstLossReserve, ExceedsReserve());"),
    ("unstake-committed", "Committed stake can be withdrawn",
     "require(staked - amount >= stakeCommitted[msg.sender], StakeCommitted());",
     "require(true || staked - amount >= stakeCommitted[msg.sender], StakeCommitted());"),
    ("self-backing", "An account may back itself",
     "require(borrower != backer, SelfBacking());",
     "require(true || borrower != backer, SelfBacking());"),
]

def parse_results(out: str):
    """Forge prints [PASS] or [FAIL: reason] and, for a failure, the shrunk call sequence before
    the test's name, so each name takes the status of the last marker above it."""
    status = {}
    current = None
    for line in out.splitlines():
        if "[PASS]" in line:
            current = "pass"
        elif "[FAIL" in line:
            current = "fail"
        for name in re.findall(r"\b((?:invariant|test)\w*)\(", line):
            if current and name not in status:
                status[name] = current
    failed = sorted(n for n, s in status.items() if s == "fail")
    passed = sorted(n for n, s in status.items() if s == "pass")
    return failed, passed


SEEDS = [1, 2, 3]  # fuzz seeds; detection by fuzzing is reported as a count over these


def main() -> None:
    root = pathlib.Path(sys.argv[1]) / "packages/foundry"
    src = root / "contracts/DecentralizedMicrocredit.sol"
    original = src.read_text()
    unit_cmd = ["forge", "test", "--no-match-path", "test/invariant/*"]
    base = subprocess.run(unit_cmd, cwd=root, capture_output=True, text=True, timeout=3600)
    baseline_failed, _ = parse_results(base.stdout + base.stderr)
    print(f"unit tests failing without any fault (ignored below): {baseline_failed}", flush=True)
    results = []
    try:
        for ident, desc, old, new in MUTANTS:
            if original.count(old) != 1:
                sys.exit(f"{ident}: the original line occurs {original.count(old)} times")
            src.write_text(original.replace(old, new))
            failed, passed, detections = set(), set(), 0
            for seed in SEEDS:
                proc = subprocess.run(["forge", "test", "--match-path", "test/invariant/*", "--fuzz-seed", str(seed)],
                                      cwd=root, capture_output=True, text=True, timeout=3600)
                out = proc.stdout + proc.stderr
                (root / f"mutant-{ident}-seed{seed}.log").write_text(out)
                f, p = parse_results(out)
                failed |= set(f)
                passed |= set(p)
                detections += bool(f)
            failed, passed = sorted(failed), sorted(passed)
            unit_failed = []
            if not failed and passed:
                # Not caught by the fuzzing: run the unit tests (fork tests skip without an RPC).
                unit = subprocess.run(unit_cmd, cwd=root, capture_output=True, text=True, timeout=3600)
                (root / f"mutant-{ident}-unit.log").write_text(unit.stdout + unit.stderr)
                unit_failed = [n for n in parse_results(unit.stdout + unit.stderr)[0] if n not in baseline_failed]
            if not (failed or passed):
                status = "compile error"
            elif failed:
                status = "detected by fuzzing"
            elif unit_failed:
                status = "detected by unit tests"
            else:
                status = "not detected"
            results.append((ident, desc, status, detections, failed, unit_failed))
            print(f"{ident}: {status} in {detections}/{len(SEEDS)} seeds {failed or unit_failed}", flush=True)
    finally:
        src.write_text(original)

    out_dir = pathlib.Path(__file__).resolve().parent.parent / "data"
    with open(out_dir / "mutation.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["mutant", "description", "status", "seeds_detecting", "seeds", "failed_properties", "failed_unit_tests"])
        for ident, desc, status, detections, failed, unit_failed in results:
            w.writerow([ident, desc, status, detections, len(SEEDS), " ".join(failed), " ".join(unit_failed)])
    print("wrote data/mutation.csv; run scripts/mutation_summary.py for the table and the summary")

if __name__ == "__main__":
    main()
