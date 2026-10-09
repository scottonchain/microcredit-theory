#!/usr/bin/env python3
"""Run paper reproductions with the recorded contract model, without modifying either checkout.

    python reproduce.py all --contract ../microcredit-contract --dry-run
    python reproduce.py all --contract ../microcredit-contract --tables-only --output /tmp/paper-tables
    python reproduce.py pricing-and-reserve --contract ../microcredit-contract --output /tmp/pricing-reproduction

The contract checkout must contain the exact recorded commit below; its current
branch is irrelevant. The pinned analysis is extracted to a disposable directory.
Paper sources and reference data are copied there, and only a successful run is
copied to a NEW output directory. Existing output directories are refused.

--tables-only recomputes extraction tables using the committed input snapshots;
it does not rerun simulations. The full mode also runs the Python simulations.
The conserved-credit Foundry campaign and mutations remain recorded evidence:
this command recomputes their summaries, not a fresh fuzz campaign. See that
paper's instructions to reproduce the Foundry experiment in its own worktree.
"""
import argparse
import gzip
import hashlib
import importlib.metadata
import io
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTRACT_COMMIT = "b725a852b923a885ded30152e80cb9f86eb1d430"
RECIPES = {
    "conserved-credit": ("sybil_sim", ("extract_simulation.py", "mutation_summary.py")),
    "pricing-and-reserve": ("credit_risk", ("locked_reserve.py", "event_timed.py", "tail_dependence.py", "extract_credit_risk.py", "pooling_subadditivity.py")),
    "one-hop-liquidity": ("liquidity", ("extract_liquidity.py", "steady_replicates.py")),
    "issuer-policy": ("issuer_policy", ("extract_issuer_policy.py", "misspecification.py")),
    "lending-equilibrium": (None, ("equilibrium.py", "robustness_table.py")),
}
SUMMARIES = {"mutation_summary.py", "robustness_table.py"}


@dataclass(frozen=True)
class Step:
    cwd: Path
    command: tuple[str, ...]
    environment: dict[str, str] = field(default_factory=dict)


def steps(papers, workspace, tables_only=False):
    """One dependency-ordered command list serves dry runs and execution."""
    contract = workspace / "contract"
    commands = []
    for paper in papers:
        analysis, scripts = RECIPES[paper]
        directory = workspace / paper
        if analysis and not tables_only:
            commands.append(Step(contract, (sys.executable, str(contract / "analysis" / analysis / "run.py"))))
        for script in scripts:
            if tables_only and not (script.startswith("extract_") or script in SUMMARIES):
                continue
            argv = (sys.executable, str(directory / "scripts" / script))
            if script not in SUMMARIES:
                argv += (str(contract),)
            commands.append(Step(directory, argv))
            if script == "equilibrium.py":
                commands.extend(Step(directory, argv, env) for env in (
                    {"PD": "0.03", "PREMIUM": "0.06", "OUTSUB": "robust/pd3"},
                    {"PD": "0.10", "PREMIUM": "0.14", "OUTSUB": "robust/pd10"},
                ))
        if paper == "conserved-credit":
            commands.append(Step(directory, (sys.executable, str(directory / "scripts/summarize_fuzz.py"),
                                            str(workspace / "fuzz_runs.txt"), str(directory / "data/fuzz_forge_tail.txt"), "1300", "256")))
    return commands


def require_pin(contract):
    result = subprocess.run(["git", "-C", str(contract), "rev-parse", "--verify", f"{CONTRACT_COMMIT}^{{commit}}"],
                            capture_output=True, text=True)
    if result.returncode or result.stdout.strip() != CONTRACT_COMMIT:
        raise ValueError(f"the contract checkout lacks recorded commit {CONTRACT_COMMIT}; fetch it with "
                         f"git -C {shlex.quote(str(contract))} fetch --no-recurse-submodules origin {CONTRACT_COMMIT}")


def prepare_workspace(contract, papers, workspace):
    raw = subprocess.run(["git", "-C", str(contract), "archive", CONTRACT_COMMIT, "analysis"], check=True, capture_output=True).stdout
    target = workspace / "contract"
    target.mkdir()
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        archive.extractall(target, filter="data")
    for paper in papers:
        shutil.copytree(ROOT / paper, workspace / paper, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(ROOT / "paper_support.py", workspace / "paper_support.py")
    if "conserved-credit" in papers:
        with gzip.open(workspace / "conserved-credit/data/fuzz_runs.txt.gz", "rb") as source:
            (workspace / "fuzz_runs.txt").write_bytes(source.read())


def file_hashes(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob("*")) if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def environment_versions():
    versions = {"python": platform.python_version()}
    for package in ("numpy", "scipy", "networkx"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return versions


def execute(papers, contract, output, tables_only):
    output = output.resolve()
    if output.exists():
        raise ValueError(f"output already exists: {output}; choose a new directory to preserve earlier results")
    # Caller tuning must not silently change the paper's base-case scenario.
    environment = {key: value for key, value in os.environ.items() if key not in ("PD", "PREMIUM", "OUTSUB")}
    with tempfile.TemporaryDirectory(prefix="microcredit-theory-") as temporary:
        workspace = Path(temporary)
        prepare_workspace(contract, papers, workspace)
        commands = steps(papers, workspace, tables_only)
        for step in commands:
            subprocess.run(step.command, cwd=step.cwd, env={**environment, **step.environment}, check=True)
        record = {
            "contract_commit": CONTRACT_COMMIT, "mode": "tables-only" if tables_only else "python-simulations-and-tables",
            "environment": environment_versions(), "papers": papers,
            "limits": ["Reference data are copied as inputs; unchanged files are retained in the output.",
                       "Foundry campaigns and mutation experiments were not rerun.",
                       "Numerical and LP reproducibility can depend on the recorded dependency versions."],
            "commands": [{"cwd": str(s.cwd.relative_to(workspace)),
                          "argv": [a.replace(str(workspace), "<workspace>") for a in s.command],
                          "environment": s.environment} for s in commands],
            "source_sha256": {paper: file_hashes(workspace / paper / "scripts") for paper in papers},
            "shared_source_sha256": hashlib.sha256((workspace / "paper_support.py").read_bytes()).hexdigest(),
            "output_sha256": {paper: file_hashes(workspace / paper / "data") for paper in papers},
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".paper-results-", dir=output.parent) as staged:
            bundle = Path(staged) / "results"
            bundle.mkdir()
            for paper in papers:
                shutil.copytree(workspace / paper / "data", bundle / paper / "data")
            (bundle / "reproduction.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            if output.exists():
                raise ValueError(f"output appeared during reproduction: {output}; refusing to overwrite it")
            bundle.rename(output)
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper", choices=["all", *RECIPES])
    parser.add_argument("--contract", type=Path, default=ROOT.parent / "microcredit-contract")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--tables-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if not args.dry_run and args.output is None:
        parser.error("--output is required; historical paper data are never overwritten by this command")
    try:
        require_pin(args.contract)
        papers = list(RECIPES) if args.paper == "all" else [args.paper]
        if args.dry_run:
            print(f"contract model: {CONTRACT_COMMIT}; disposable workspace; no files written")
            for step in steps(papers, Path("<workspace>"), args.tables_only):
                env = " ".join(f"{key}={shlex.quote(value)}" for key, value in step.environment.items())
                print(f"{step.cwd}: {env + ' ' if env else ''}{shlex.join(step.command)}")
            return
        record = execute(papers, args.contract.resolve(), args.output, args.tables_only)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"completed {len(record['commands'])} command(s); isolated results: {args.output}")


if __name__ == "__main__":
    main()
