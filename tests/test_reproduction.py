"""Offline checks for reproducibility isolation and retained paper interfaces."""
import csv
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import paper_support
import reproduce

ROOT = Path(__file__).resolve().parents[1]


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SharedTablesTests(unittest.TestCase):
    def test_csv_roundtrip_preserves_quoted_multiline_and_unicode_values(self):
        with tempfile.TemporaryDirectory() as temporary:
            tables = paper_support.PaperTables(temporary, temporary, "% generated\n")
            tables.write_csv("table.csv", ["name", "value"], [["quoted, name", "line one\nline two"], ["café", "2"]])
            self.assertEqual(tables.read("table.csv"), [
                {"name": "quoted, name", "value": "line one\nline two"}, {"name": "café", "value": "2"}])

    def test_tex_preserves_original_row_terminators(self):
        with tempfile.TemporaryDirectory() as temporary:
            tables = paper_support.PaperTables(temporary, temporary, "% generated\n")
            tables.write_tex("table.tex", ["a & b", "c & d"])
            expected = "% generated\n" + "a & b " + "\\" * 2 + "\n" + "c & d " + "\\" * 2 + "\n"
            self.assertEqual((Path(temporary) / "table.tex").read_text(), expected)


class ReproductionTests(unittest.TestCase):
    def test_dry_run_has_no_output_writes(self):
        with patch.object(reproduce, "require_pin") as pin, patch.object(reproduce, "execute") as execute, patch("builtins.print"):
            reproduce.main(["all", "--dry-run", "--tables-only"])
        pin.assert_called_once()
        execute.assert_not_called()

    def test_missing_output_is_rejected_before_any_git_call(self):
        with patch.object(reproduce, "require_pin") as pin, patch("sys.stderr"):
            with self.assertRaises(SystemExit):
                reproduce.main(["all"])
        pin.assert_not_called()

    def test_missing_or_wrong_recorded_commit_is_rejected(self):
        for code, revision in ((1, ""), (0, "0" * 40)):
            with self.subTest(revision=revision), patch.object(reproduce.subprocess, "run", return_value=subprocess.CompletedProcess([], code, revision)):
                with self.assertRaisesRegex(ValueError, "fetch --no-recurse-submodules"):
                    reproduce.require_pin(Path("contract checkout"))

    def test_tables_mode_never_runs_models_and_retains_recorded_fuzz_summary(self):
        commands = reproduce.steps(list(reproduce.RECIPES), Path("/workspace"), tables_only=True)
        scripts = [Path(step.command[1]).name for step in commands]
        self.assertTrue(all(name.startswith("extract_") or name.endswith("_summary.py") or name in {"robustness_table.py", "summarize_fuzz.py"} for name in scripts))
        self.assertIn("summarize_fuzz.py", scripts)
        self.assertIn("robustness_table.py", scripts)

    def test_full_pricing_builds_event_inputs_before_their_consumers(self):
        commands = reproduce.steps(["pricing-and-reserve"], Path("/workspace"))
        scripts = [Path(step.command[1]).name for step in commands]
        self.assertLess(scripts.index("run.py"), scripts.index("locked_reserve.py"))
        self.assertLess(scripts.index("locked_reserve.py"), scripts.index("event_timed.py"))
        self.assertLess(scripts.index("event_timed.py"), scripts.index("extract_credit_risk.py"))

    def test_existing_output_is_refused_before_starting_reproduction(self):
        with tempfile.TemporaryDirectory() as temporary, patch.object(reproduce, "prepare_workspace") as prepare:
            output = Path(temporary)
            sentinel = output / "earlier-result"
            sentinel.write_bytes(b"recorded result")
            with self.assertRaisesRegex(ValueError, "output already exists"):
                reproduce.execute([], Path("contract"), output, True)
            self.assertEqual(sentinel.read_bytes(), b"recorded result")
        prepare.assert_not_called()

    def test_failed_command_leaves_no_output_and_clears_caller_scenario_overrides(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "results"
            command = reproduce.Step(Path(temporary), ("python", "experiment.py"))
            with patch.object(reproduce, "prepare_workspace"), patch.object(reproduce, "steps", return_value=[command]), patch.object(reproduce.subprocess, "run", side_effect=subprocess.CalledProcessError(1, command.command)) as run, patch.dict(os.environ, PD="0.99", PREMIUM="0.99", OUTSUB="unintended"):
                with self.assertRaises(subprocess.CalledProcessError):
                    reproduce.execute([], Path("contract"), output, False)
            self.assertFalse(output.exists())
            for key in ("PD", "PREMIUM", "OUTSUB"):
                self.assertNotIn(key, run.call_args.kwargs["env"])

    def test_manifest_hashes_exclude_runtime_bytecode(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / "model.py").write_text("pass\n")
            (directory / "__pycache__").mkdir()
            (directory / "__pycache__/model.cpython.pyc").write_bytes(b"runtime-specific")
            self.assertEqual(list(reproduce.file_hashes(directory)), ["model.py"])


class CompatibilityTests(unittest.TestCase):
    def test_robustness_table_import_does_not_read_or_write_data(self):
        with patch("builtins.open", side_effect=AssertionError("import performed data I/O")):
            module_at("robustness_table", ROOT / "lending-equilibrium/scripts/robustness_table.py")

    def test_all_papers_use_a_valid_shared_build_recipe(self):
        result = subprocess.run(["make", "--no-print-directory", "-n", "-B", "all"], cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout.count("-halt-on-error paper.tex"), len(reproduce.RECIPES))

    def test_equilibrium_wrapper_handles_spaces_and_caller_environment(self):
        with tempfile.TemporaryDirectory(prefix="paper paths ") as temporary:
            directory = Path(temporary)
            contract = directory / "contract checkout"
            contract.mkdir()
            log = directory / "calls.jsonl"
            fake_python = directory / "python recorder"
            fake_python.write_text("#!" + sys.executable + "\n"
                "import json, os, sys\n"
                "with open(os.environ['PAPER_TEST_LOG'], 'a') as handle:\n"
                "    handle.write(json.dumps({'argv': sys.argv[1:], 'env': {k: os.environ.get(k) for k in ('PD', 'PREMIUM', 'OUTSUB')}}) + '\\n')\n")
            fake_python.chmod(0o755)
            environment = {**os.environ, "PYTHON": str(fake_python), "PAPER_TEST_LOG": str(log), "PD": "0.99", "PREMIUM": "0.99", "OUTSUB": "wrong"}
            subprocess.run(["sh", str(ROOT / "lending-equilibrium/scripts/run_all.sh"), contract.name], cwd=directory, env=environment, check=True)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(len(calls), 4)
            self.assertEqual(calls[0]["env"], {"PD": "0.05", "PREMIUM": "0.08", "OUTSUB": ""})
            self.assertEqual([row["env"]["PD"] for row in calls[:3]], ["0.05", "0.03", "0.10"])
            self.assertTrue(all(row["argv"][1] == str(contract) for row in calls[:3]))
            self.assertEqual(Path(calls[-1]["argv"][0]).name, "robustness_table.py")


class MutationEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.analysis = module_at("mutation_analysis", ROOT / "conserved-credit/scripts/mutation_analysis.py")
        self.summary = module_at("mutation_summary", ROOT / "conserved-credit/scripts/mutation_summary.py")

    def test_baseline_without_test_results_never_modifies_contract(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "packages/foundry/contracts/DecentralizedMicrocredit.sol"
            source.parent.mkdir(parents=True)
            source.write_text("original source\n")
            failed = subprocess.CompletedProcess([], 1, "compiler unavailable", "")
            with patch.object(sys, "argv", ["mutation_analysis.py", temporary]), patch.object(self.analysis.subprocess, "run", return_value=failed):
                with self.assertRaisesRegex(SystemExit, "no mutant was applied"):
                    self.analysis.main()
            self.assertEqual(source.read_text(), "original source\n")

    def test_incomplete_seed_restores_source_and_does_not_report_a_missed_fault(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "packages/foundry/contracts/DecentralizedMicrocredit.sol"
            source.parent.mkdir(parents=True)
            source.write_text("original source\n")
            baseline = subprocess.CompletedProcess([], 0, "[PASS] testBaseline()", "")
            incomplete = subprocess.CompletedProcess([], 1, "compiler unavailable", "")
            with patch.object(sys, "argv", ["mutation_analysis.py", temporary]), patch.object(self.analysis, "MUTANTS", [("one", "One fault", "original", "mutated")]), patch.object(self.analysis.subprocess, "run", side_effect=[baseline, incomplete]), patch("builtins.print"):
                with self.assertRaisesRegex(RuntimeError, "seed 1 did not complete"):
                    self.analysis.main()
            self.assertEqual(source.read_text(), "original source\n")
            self.assertFalse((Path(temporary) / "data/mutation.csv").exists())

    def test_missing_mutation_target_is_detected_before_any_mutant(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "packages/foundry/contracts/DecentralizedMicrocredit.sol"
            source.parent.mkdir(parents=True)
            source.write_text("original source\n")
            baseline = subprocess.CompletedProcess([], 0, "[PASS] testBaseline()", "")
            with patch.object(sys, "argv", ["mutation_analysis.py", temporary]), patch.object(self.analysis, "MUTANTS", [("first", "First fault", "original", "mutated"), ("absent", "Missing fault", "nonexistent", "mutated")]), patch.object(self.analysis.subprocess, "run", return_value=baseline) as run:
                with self.assertRaisesRegex(SystemExit, "absent: expected one source location"):
                    self.analysis.main()
            self.assertEqual(run.call_count, 1)
            self.assertEqual(source.read_text(), "original source\n")

    def test_summary_refuses_incomplete_or_inconsistent_experiments_without_writes(self):
        for rows in ([{"status": "compile error", "seeds": 3, "seeds_detecting": 0}],
                     [{"status": "not detected", "seeds": 3, "seeds_detecting": 0}, {"status": "not detected", "seeds": 2, "seeds_detecting": 0}]):
            with self.subTest(rows=rows), tempfile.TemporaryDirectory() as temporary:
                data = Path(temporary) / "data"
                data.mkdir()
                with (data / "mutation.csv").open("w", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=["status", "seeds", "seeds_detecting"])
                    writer.writeheader()
                    writer.writerows(rows)
                table = data / "mutation_table.tex"
                table.write_text("recorded table\n")
                with patch.object(self.summary, "__file__", str(Path(temporary) / "scripts/mutation_summary.py")):
                    with self.assertRaises(SystemExit):
                        self.summary.main()
                self.assertEqual(table.read_text(), "recorded table\n")
                self.assertFalse((data / "mutation_summary.tex").exists())


if __name__ == "__main__":
    unittest.main()
