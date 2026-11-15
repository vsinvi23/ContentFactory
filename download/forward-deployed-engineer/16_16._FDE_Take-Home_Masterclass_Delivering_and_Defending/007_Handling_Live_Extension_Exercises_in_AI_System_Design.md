# Handling_Live_Extension_Exercises_in_AI_System_Design

Source: https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Handling Live Extension Exercises

Clarify the requirements, verify the existing baseline, and make the smallest necessary change during a live coding session. Explain your debugging hypotheses aloud and use targeted checks to isolate the cause of failures. At the end of the session, summarize completed work, verification results, and remaining issues.

We'll cover the following...

- [Clarifying the extension request](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Clarifying-the-extension-request)
- [Saving a verified baseline](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Saving-a-verified-baseline)
- [Making the smallest change](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Making-the-smallest-change)
- [Debugging out loud](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Debugging-out-loud)
- [Verifying the agreed behavior](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Verifying-the-agreed-behavior)
- [When time runs out](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#When-time-runs-out)
- [Practice: the --through extension](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Practice-the---through-extension)

“Can you let the coordinator filter this report by team?” The interviewer points to a working command:

Ace Editor

1

python task\_report.py task\_sample.csv --as-of 2026-04-15

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The report includes open tasks with a `due_date` earlier than `--as-of`. Before modifying the code, clarify the expected team-filter behavior and identify the existing conditions that must remain unchanged.

Verify the existing baseline, make the smallest necessary change, test both new and existing behavior, and report the results.

## Clarifying the extension request[#](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Clarifying-the-extension-request)

Clarify three requirements before implementing the filter:

- Should team filtering narrow the existing eligible tasks or change the eligibility rules?
- Should omitting the filter preserve the current report exactly?
- How should team matching handle whitespace, case sensitivity, blank values, and unmatched teams?

For this exercise, the interviewer confirms the following requirements:

- Add an optional `--team` argument without changing the open-status requirement or strict `due_date` comparison.
- Trim surrounding whitespace from the supplied team value and each record's team field, then compare them case-sensitively.
- Omitting `--team` must preserve the existing report. Supplying a blank team value must produce an input error.
- An unmatched team produces a successful header-only CSV.
- Validate all source rows before applying filters, including rows that do not match the requested team.

Confirm your understanding of the agreed requirements: “I’ll add a case-sensitive team filter, trim surrounding whitespace, preserve the existing output when the filter is omitted, and validate all source rows before filtering.” This lets the interviewer correct any misunderstanding before implementation begins.

Confirm whether AI assistance is permitted during the live interview. Permission for a take-home assignment does not automatically extend to other assessment stages. For example, Anthropic's published guidance distinguishes interview preparation, take-home assignments, and live interviews. It prohibits AI assistance during live interviews unless explicitly permitted. Follow the current instructions for your specific assessment.

## Saving a verified baseline[#](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Saving-a-verified-baseline)

A **recoverable baseline** includes the current code and its known verification results. A new Git branch helps organize work, but it does not save uncommitted files.

Use Python 3.10 or later and the standard library. The workspace supplies three new, independent files: `task_report.py`, `task_sample.csv`, and `test_task_report.py`. Use `python3` on macOS or Linux, or `py -3` on Windows, if that is your interpreter command; substitute it consistently below.

The sample CSV contains:

Ace Editor

1

2

3

4

5

6

task\_id,status,due\_date,team

T201,open,2026-04-14,Support

T202,open,2026-04-13,Ops

T203,completed,2026-04-12,Support

T204,open,2026-04-15,Support

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** Names the four required columns and the output column order.
- **Lines 2–3:** Supply the two baseline-eligible tasks, in their required output order.
- **Line 4:** Tests exclusion by completed status.
- **Line 5:** Tests exclusion when the due date equals the cutoff.

Open the baseline workspace and establish its actual behavior before making the extension.

Files

workspace.py

task\_report.py

python310

```
from pathlib import Path

import argparse

import zipfile

ROOT = Path(__file__).resolve().parent

PROGRAM = r'''import argparse

import csv

import re

import sys

from datetime import date

FIELDS = ("task_id", "status", "due_date", "team")

def iso_date(value):

if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):

raise ValueError("date must use YYYY-MM-DD")

return date.fromisoformat(value)

def load_tasks(path):

rows = []

with open(path, newline="", encoding="utf-8") as source:

reader = csv.DictReader(source, strict=True)

missing = set(FIELDS) - set(reader.fieldnames or [])

if missing:

raise ValueError("missing required columns: " + ", ".join(sorted(missing)))

for number, raw in enumerate(reader, start=2):

if None in raw or any(raw[name] is None for name in FIELDS):

raise ValueError(f"row {number}: malformed CSV record")

if not raw["task_id"].strip():

raise ValueError(f"row {number}: task_id must not be blank")

if not raw["team"].strip():

raise ValueError(f"row {number}: team must not be blank")

if raw["status"] not in ("open", "completed"):

raise ValueError(f"row {number}: status must be open or completed")

try:

due = iso_date(raw["due_date"])

except ValueError as exc:

raise ValueError(f"row {number}: invalid due_date") from exc

row = {name: raw[name] for name in FIELDS}

row["due_date"] = due

rows.append(row)

return rows

def select_tasks(rows, as_of):

return [row for row in rows

if row["status"] == "open" and row["due_date"] < as_of]

def main():

parser = argparse.ArgumentParser(description="Report open overdue tasks")

parser.add_argument("source")

parser.add_argument("--as-of", required=True, type=iso_date)

args = parser.parse_args()

try:

rows = load_tasks(args.source)

except (OSError, ValueError, csv.Error) as exc:

parser.error(str(exc))

selected = select_tasks(rows, args.as_of)

writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS, lineterminator="\n")

writer.writeheader()

writer.writerows(selected)

if __name__ == "__main__":

main()

'''

SAMPLE = '''task_id,status,due_date,team

T201,open,2026-04-14,Support

T202,open,2026-04-13,Ops

T203,completed,2026-04-12,Support

T204,open,2026-04-15,Support

'''

TESTS = r'''import csv

import io

import subprocess

import sys

import tempfile

import unittest

from datetime import date

from pathlib import Path

from task_report import FIELDS, load_tasks, select_tasks

ROOT = Path(__file__).resolve().parent

SAMPLE = ROOT / "task_sample.csv"

class BaselineTests(unittest.TestCase):

def cli(self, source, *flags):

return subprocess.run(

[sys.executable, str(ROOT / "task_report.py"), str(source),

"--as-of", "2026-04-15", *flags],

capture_output=True, text=True)

def test_selection(self):

selected = select_tasks(load_tasks(SAMPLE), date(2026, 4, 15))

self.assertEqual([row["task_id"] for row in selected], ["T201", "T202"])

def test_real_cli(self):

result = self.cli(SAMPLE)

self.assertEqual(result.returncode, 0, result.stderr)

reader = csv.DictReader(io.StringIO(result.stdout))

self.assertEqual(reader.fieldnames, list(FIELDS))

self.assertEqual(list(reader), [

dict(task_id="T201", status="open", due_date="2026-04-14", team="Support"),

dict(task_id="T202", status="open", due_date="2026-04-13", team="Ops")])

def test_source_errors_emit_no_report(self):

invalid_sources = [

"task_id,status,due_date\nT1,open,2026-04-14\n",

"task_id,status,due_date,team\n ,open,2026-04-14,Ops\n",

"task_id,status,due_date,team\nT1,open,2026-04-14, \n",

"task_id,status,due_date,team\nT1,pending,2026-04-14,Ops\n",

"task_id,status,due_date,team\nT1,open,2026-02-30,Ops\n"]

with tempfile.TemporaryDirectory() as folder:

source = Path(folder) / "invalid.csv"

for text in invalid_sources:

with self.subTest(text=text):

source.write_text(text, encoding="utf-8")

result = self.cli(source)

self.assertNotEqual(result.returncode, 0)

self.assertEqual(result.stdout, "")

self.assertIn("error:", result.stderr)

if __name__ == "__main__":

unittest.main()

'''

EXTENSION = r'''

# Focused acceptance checks: expectations, not recorded execution results.

class TeamAcceptanceTests(unittest.TestCase):

cli = BaselineTests.cli

def expected(self, ids, padded=False, dates=False):

records = {

"T201": dict(task_id="T201", status="open", due_date="2026-04-14",

team=" Support " if padded else "Support"),

"T202": dict(task_id="T202", status="open", due_date="2026-04-13", team="Ops")}

result = [records[key].copy() for key in ids]

if dates:

for row in result:

row["due_date"] = date.fromisoformat(row["due_date"])

return result

def assert_report(self, result, ids, padded=False):

self.assertEqual(result.returncode, 0, result.stderr)

reader = csv.DictReader(io.StringIO(result.stdout))

self.assertEqual(reader.fieldnames, list(FIELDS))

records = list(reader)

self.assertEqual(records, self.expected(ids, padded=padded))

self.assertTrue({row["task_id"] for row in records}.isdisjoint({"T203", "T204"}))

if not ids:

self.assertEqual(result.stdout, "task_id,status,due_date,team\n")

def test_selection_teams(self):

rows = load_tasks(SAMPLE)

cutoff = date(2026, 4, 15)

self.assertEqual(select_tasks(rows, cutoff), self.expected(["T201", "T202"], dates=True))

# Only normalized values enter selection. CLI owns supplied-value trimming.

for team, ids in [(None, ["T201", "T202"]), ("Support", ["T201"]),

("Ops", ["T202"]), ("support", []), ("Unknown", [])]:

with self.subTest(team=team):

selected = select_tasks(rows, cutoff, team)

self.assertEqual(selected, self.expected(ids, dates=True))

self.assertTrue({row["task_id"] for row in selected}.isdisjoint({"T203", "T204"}))

def test_cli_teams(self):

for flags, ids in [((), ["T201", "T202"]),

(("--team", "Support"), ["T201"]),

(("--team", "Ops"), ["T202"]),

(("--team", " Support "), ["T201"]),

(("--team", "support"), []),

(("--team", "Unknown"), [])]:

with self.subTest(flags=flags):

self.assert_report(self.cli(SAMPLE, *flags), ids)

def test_record_side_trimming(self):

with tempfile.TemporaryDirectory() as folder:

source = Path(folder) / "padded.csv"

source.write_text(SAMPLE.read_text(encoding="utf-8").replace(

",Support\n", ", Support \n"), encoding="utf-8")

rows = load_tasks(source)

self.assertEqual(rows[0]["team"], " Support ")

self.assertEqual(select_tasks(rows, date(2026, 4, 15), "Support"),

self.expected(["T201"], padded=True, dates=True))

for supplied in ("Support", " Support "):

self.assert_report(self.cli(source, "--team", supplied), ["T201"], padded=True)

def test_blank_supplied_team(self):

# Blank is rejected at the CLI, not passed into selection.

for supplied in ("", "   "):

with self.subTest(supplied=supplied):

result = self.cli(SAMPLE, "--team", supplied)

self.assertNotEqual(result.returncode, 0)

self.assertEqual(result.stdout, "")

self.assertIn("error:", result.stderr)

self.assertIn("--team", result.stderr)

self.assertIn("blank", result.stderr.lower())

def test_full_source_validation_with_filter(self):

cases = [

("task_id,status,due_date\nT1,open,2026-04-14\n",

"Unknown", "missing required columns: team"),

("task_id,status,due_date,team\nT201,open,2026-04-14,Support\n"

"T202,pending,2026-04-13,Ops\n",

"Support", "status must be open or completed")]

with tempfile.TemporaryDirectory() as folder:

source = Path(folder) / "invalid.csv"

for text, team, message in cases:

with self.subTest(team=team):

source.write_text(text, encoding="utf-8")

result = self.cli(source, "--team", team)

self.assertNotEqual(result.returncode, 0)

self.assertEqual(result.stdout, "")

self.assertIn("error:", result.stderr)

self.assertIn(message, result.stderr)

'''

GUIDE = '''# Task report workspace

Python 3.10+, standard library only. Run commands in this directory.

Use python3 or py -3 consistently if that is your interpreter command.

Setup does not execute the report or tests. All results remain unverified.

## Baseline stage

1. Inspect task_report.py, task_sample.csv, and test_task_report.py.

2. Predict the selected task IDs before running anything. Keep your prediction

separate from observed evidence (for example in prediction.txt).

3. Run:

python task_report.py task_sample.csv --as-of 2026-04-15

python -m unittest -v test_task_report.BaselineTests

4. Record each actual command, stdout, stderr, and exit status in evidence.md.

That note starts empty. Do not turn expected output into observed evidence.

Obtain the exit status immediately after each command ($? in a POSIX shell,

$LASTEXITCODE in PowerShell), or use subprocess.run to capture it.

Expected, not observed: the baseline CLI exits zero and emits the four-column

header followed by T201 and T202, in that order. Baseline tests should pass.

If execution is unavailable, label your written trace unverified.

baseline.zip is the untouched downloadable baseline: it contains only the three

original exercise files. Extract it into a separate directory for recovery;

do not overwrite unfinished work without saving it first.

## Extension-check stage (same workspace)

When ready, run:

python workspace.py extension

This appends acceptance checks to test_task_report.py, retaining all original

baseline assertions. It does not implement --team or execute tests. Run the

checks before or alongside your edits; they are expected to fail until the

feature is connected.

Edit task_report.py using the lesson: add the parser argument, normalize the

supplied value, reject blank input, extend the function signature and predicate,

and connect the caller. Those are the learner's edits; setup supplies no finished

implementation. Keep full-source validation before selection.

Run focused checks, the real CLI, and the unchanged regression checks:

python -m unittest -v test_task_report.TeamAcceptanceTests

python task_report.py task_sample.csv --as-of 2026-04-15 --team Support

python task_report.py task_sample.csv --as-of 2026-04-15

python -m unittest -v

Record actual results and exit statuses in evidence.md, including failures.

Expected, not observed: Support selects T201; Ops selects T202; padded Support

matches Support; lowercase support and Unknown produce header-only success.

Blank supplied values fail without CSV output. T203 and T204 remain excluded.

Record-side trimming affects matching, not the original team text in output.

The checks also require invalid other-team rows and missing headers to fail.

'''

BASELINE = {"task_report.py": PROGRAM, "task_sample.csv": SAMPLE,

"test_task_report.py": TESTS}

def setup():

# Exclusive creation preserves working edits and any existing evidence.

for name, content in {**BASELINE, "WORKSPACE.md": GUIDE, "evidence.md": ""}.items():

path = ROOT / name

if not path.exists():

with path.open("x", encoding="utf-8", newline="") as target:

target.write(content)

archive = ROOT / "baseline.zip"

if not archive.exists():

with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as saved:

for name, content in BASELINE.items():

saved.writestr(name, content)

print("Workspace ready. Read WORKSPACE.md. No report or tests have been run by setup.")

def add_extension_checks():

path = ROOT / "test_task_report.py"

if not path.exists():

raise SystemExit("Run python workspace.py first.")

text = path.read_text(encoding="utf-8")

if "class TeamAcceptanceTests(" in text:

print("Acceptance checks already present; no files changed.")

return

marker = 'if __name__ == "__main__":\n    unittest.main()'

if text.count(marker) != 1:

raise SystemExit("Test entry point changed; append acceptance checks manually before unittest.main().")

path.write_text(text.replace(marker, EXTENSION + "\n\n" + marker), encoding="utf-8")

print("Acceptance checks added. No implementation changed; no checks executed.")

if __name__ == "__main__":

parser = argparse.ArgumentParser(description="Create the task report workspace or add acceptance checks")

parser.add_argument("stage", nargs="?", choices=("baseline", "extension"), default="baseline")

args = parser.parse_args()

if args.stage == "baseline":

setup()

else:

add_extension_checks()
```

⋯

workspace code

The listing shows `workspace.py`, the setup script, not the report file you need to modify. Run `python workspace.py` once to generate the project files, then make your changes in those files.

- **Lines 1–5:** Import setup utilities and locate the script’s directory, so generated files have a predictable destination.
- **Lines 7–19:** Begin the embedded report program, declare its output fields, and define strict calendar-date parsing. These become code in `task_report.py`.
- **Lines 22–28:** Open the source CSV and reject missing required columns before processing records.
- **Lines 29–37:** Reject malformed records, blank IDs or teams, and unsupported statuses. Team filtering must not bypass these checks.
- **Lines 38–45:** Validate each due date, retain the original field values except for the parsed date, and return all validated records.
- **Lines 48–50:** Define baseline selection: open tasks strictly before the cutoff. This is the predicate you will extend in the generated report.
- **Lines 53–57:** Define the existing CLI and its required date argument. Add the optional filter alongside these arguments in `task_report.py`.
- **Lines 58–65:** Load and validate the complete source, report input errors, select records, and emit CSV. Connect the new argument at the selection call without changing validation or output.
- **Lines 68–69:** Invoke the report when its file is executed directly, preserving the familiar script entry-point pattern.
- **Lines 72–77:** Embed the four-row fixture, including the completed-task and cutoff-equality exclusions.
- **Lines 79–91:** Begin the baseline test file, import its tools and report functions, and locate the sample relative to the test file.
- **Lines 94–99:** Define a subprocess helper that exercises the real CLI and captures output and exit status.
- **Lines 101–112:** Check selection directly and check the real CLI’s exact columns, values, and ordering. These unchanged assertions protect the original behavior.
- **Lines 114–129:** Exercise invalid sources and require a nonzero exit, empty report output, and an error message.
- **Lines 132–133:** Provide the test file’s direct-execution entry point.
- **Lines 136–151:** Begin the separately installed team acceptance suite and construct expected records, including padded team text and parsed dates.
- **Lines 153–161:** Check exact CLI reports, exclusion boundaries, and the precise header-only result for no matches.
- **Lines 163–173:** Check selection with omitted and normalized team values, including case-sensitive and unknown-team cases.
- **Lines 175–183:** Exercise those cases through the CLI, adding whitespace-padded input to test normalization at the interface.
- **Lines 185–195:** Create padded source-team values and check matching at both levels. Expected output retains the original padding rather than rewriting source text.
- **Lines 197–206:** Require empty and whitespace-only supplied filters to fail clearly without emitting CSV.
- **Lines 208–224:** Require missing headers and invalid other-team rows to fail despite filtering, protecting full-source validation.
- **Lines 227–253:** Embed workspace instructions for predicting, executing, recording evidence, and using the untouched baseline archive safely.
- **Lines 255–283:** Explain how to install acceptance checks, make the extension, and verify it. Expected results are explicitly separate from execution evidence.
- **Lines 285–286:** Collect the three embedded baseline files into one mapping for setup and archiving.
- **Lines 289–295:** Create missing workspace files without overwriting existing edits or evidence.
- **Lines 296–301:** Create an untouched baseline ZIP if absent and report setup completion. Setup itself runs no checks.
- **Lines 304–316:** Install acceptance checks before the test entry point, refusing unsafe insertion and avoiding duplicate installation. This changes tests, not the implementation.
- **Lines 319–326:** Choose baseline setup or the extension-check installation stage from the command line.

The archive contains the original exercise files, not subsequent edits or verification results. Use the checkpoint procedure below to save the current working files and record their verification results.

Locate the transition between validating and loading source records and filtering eligible records. Add the new filter within that existing processing flow.

If this is a Git repository, inspect `git status --short`. Check the exercise files for credentials, sensitive information, and unrelated content before creating the checkpoint.

The following Python snippet saves the three exercise files in a separate checkpoint and records verification results for the saved copies:

Ace Editor

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

from pathlib import Path

import shutil

import subprocess

import sys

import tempfile

saved = Path(tempfile.mkdtemp(prefix="task-report-baseline-"))

for name in ("task\_report.py", "task\_sample.csv", "test\_task\_report.py"):

shutil.copy2(name, saved / name)

checks = ([sys.executable, "task\_report.py", "task\_sample.csv", "--as-of", "2026-04-15"],

[sys.executable, "-m", "unittest", "-v"])

with (saved / "verification.txt").open("w", encoding="utf-8") as log:

for command in checks:

result = subprocess.run(command, cwd=saved, capture\_output=True, text=True)

log.write(f"{command!r}\nexit={result.returncode}\n{result.stdout}{result.stderr}\n")

print(saved)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Lines 1–5:** Import the standard-library tools needed to copy files and capture checks.
- **Lines 7–9:** Create a separate directory and copy only the exercise files, including their current uncommitted contents.
- **Lines 10–11:** Define the real CLI check and existing test run.
- **Lines 12–15:** Run both against the saved files and retain exit statuses, output, and errors.
- **Line 16:** Print the checkpoint location so you can inspect and recover it.

Open `verification.txt` and review the recorded baseline checks. The expected baseline has exit code `0`, includes `T201` and `T202` in the output, and passes all baseline tests. If a baseline check fails, reproduce and diagnose it before attributing any failure to the new change. A checkpoint preserves the state of a failing implementation but does not establish a working baseline.

For the 20-minute course rehearsal, allocate 3 minutes to clarification and baseline verification, 9 to implementation, 5 to testing and debugging, and 3 to recovery or handoff. These synthetic inputs and time allocations are specific to the exercise, not requirements imposed by an employer.

## Making the smallest change[#](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Making-the-smallest-change)

Trace the existing processing flow: argument parsing, record validation, task selection, and CSV output. Add the optional `--team` argument to the CLI and pass its whitespace-trimmed value to the task-selection logic. Preserve source validation, output formatting, task ordering, date comparisons, and existing dependencies.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27818.9100000000001%27%20height=%27300.51000000000005%27/%3e)![The team filter changes CLI handling and selection, while every source row is still validated before selection and CSV output stays unchanged](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The team filter changes CLI handling and selection, while every source row is still validated before selection and CSV output stays unchanged")

The team filter changes CLI handling and selection, while every source row is still validated before selection and CSV output stays unchanged

At the argument parser, add:

Ace Editor

1

2

parser.add\_argument("--team")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

After `parse_args()`, normalize once and reject a blank supplied value:

Ace Editor

1

2

3

4

team = None if args.team is None else args.team.strip()

if team == "":

parser.error("--team must not be blank")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

`None` means no filter; an empty normalized string means invalid input. Keeping them distinct preserves the agreed omission behavior.

Change the selection function and its caller:

Ace Editor

1

2

3

4

5

6

7

8

9

def select\_tasks(rows, as\_of, team=None):

return [row for row in rows

if row["status"] == "open"

and row["due\_date"] < as\_of

and (team is None or row["team"].strip() == team)]

# In main(), after load\_tasks() has validated the entire source:

selected = select\_tasks(rows, args.as\_of, team)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** Adds an optional normalized filter while preserving existing two-argument calls.
- **Lines 2–5:** Conjoin the team condition with both original eligibility conditions and retain input order.
- **Lines 7–8:** Connect the CLI value to selection after full-source validation.

Do not move team filtering into the CSV reader: That would let invalid rows from other teams escape validation. There is no need for a team registry, new interface, or generalized filter framework.

Run `python workspace.py extension` to append the supplied acceptance checks before or alongside your edit. This stage neither implements `--team` nor executes tests. Run `python -m unittest -v test_task_report.TeamAcceptanceTests`, then run the real entry point:

Ace Editor

1

2

python task\_report.py task\_sample.csv --as-of 2026-04-15 --team Support

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Debugging out loud[#](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Debugging-out-loud)

A tempting edit replaces the old predicate instead of extending it:

Ace Editor

1

2

3

4

return [row for row in rows

if row["due\_date"] < as\_of

and (team is None or row["team"].strip() == team)]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This predicate has lost the status condition. Its expected output for `--team Support` is:

Ace Editor

1

2

3

4

task\_id,status,due\_date,team

T201,open,2026-04-14,Support

T203,completed,2026-04-12,Support

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

T203 is the observable mismatch: Its team and date match, but its completed status should exclude it. Before reading the repair, choose the next diagnostic action.

Diagnose the Support mismatch

Q1. With `--as-of 2026-04-15 --team Support`, this faulty predicate produces the CSV below:

1

2

3

return [row for row in rows

if row["due\_date"] < as\_of

and (team is None or row["team"].strip() == team)]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

1

2

3

task\_id,status,due\_date,team

T201,open,2026-04-14,Support

T203,completed,2026-04-12,Support

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

T203 should be excluded. Which next action best distinguishes incorrect status parsing from a missing selection condition?

Do you find this helpful?

A useful spoken update is:

> “T203 should be excluded by status. Either status is parsed incorrectly or my new predicate no longer checks it. I will inspect T203’s validated status and the predicate before changing parsing.”

Inspect the value directly:

Ace Editor

1

2

3

rows = load\_tasks("task\_sample.csv")

print(repr(next(row for row in rows if row["task\_id"] == "T203")["status"]))

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The expected inspection result is `‘completed’`. If your run confirms that value, parsing preserved the status correctly; inspecting the faulty predicate then identifies the missing status clause. Restore `row[“status”] == “open”` as shown in the complete selection function above.

Rerun the reproducer. The repaired Support report should contain only T201. Then run the original command and baseline tests, because the repair must also preserve the unfiltered report.

**Observable debugging** connects a mismatch to a hypothesis, a distinguishing check, its result, and the next action. Short updates at those decision points make reasoning visible. Continuous keystroke narration adds little.

Removing T203 from the fixture, or changing its expected result, would erase the evidence of the defect. Keep the agreed criterion and repair the implementation.

## Verifying the agreed behavior[#](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Verifying-the-agreed-behavior)

Run the workspace's extension tests against both the selection function and the command-line interface. With `--as-of 2026-04-15`, verify the following output records:

- Without `--team`: Return `T201` and `T202` in their original input order.
- `--team Support`: Return `T201` only.
- `--team Ops`: Return `T202` only.
- `--team ' Support '`: Produce the same report as `--team Support`.
- `--team support` or an unknown team: Exit successfully and produce a header-only CSV.

Verify the following eligibility and validation boundaries:

- `T203` remains excluded because its status is completed.
- `T204` remains excluded because its `due_date` equals `--as-of`, rather than preceding it.
- `--team ' '`: Display a clear validation error, exit with a nonzero status, and produce no CSV report.
- Missing `team` header: Report a validation error, exit with a nonzero status, and produce no CSV, even when the requested team has no matches.
- Invalid row belonging to another team: Reject the input before producing a report.

Inspect CSV contents and exit status. A process launching successfully proves little about its result. A passing feature check establishes checked new behavior; the unchanged-baseline check establishes checked preservation of earlier behavior. Both are necessary.

All outputs here remain expected until you execute and inspect them. These local checks support claims about the checked local cases, not production reliability or customer impact.

## When time runs out[#](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#When-time-runs-out)

Stop speculative editing. Name the exact remaining mismatch and preserve a separate copy of the unfinished files or a diff before recovering the baseline.

If restoration is necessary, copy the saved exercise files back deliberately and rerun the baseline command and tests. Avoid destructive repository-wide resets. Restoration recovers original behavior; it does not complete the extension.

If your observations support it, an honest handback is:

> “I restored the saved baseline and reran the original CLI and tests. The original report is working again. The extension is incomplete: The Support case still included T203 before restoration. The next check is to inspect its validated status against the selection predicate. The unfinished files are saved separately.”

If the extension passes the executed checks, summarize the implemented behavior, verification results, and any checks not run. Distinguish implemented functionality, executed checks, failures, and unverified behavior, even under time constraints.

## Practice: the `--through` extension[#](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Practice-the---through-extension)

Start a fresh baseline copy, without the completed `--team` changes. The rehearsal introduces a different date rule so you must repeat the process rather than reproduce the demonstrated predicate.

Files

start\_through\_rehearsal.py

task\_report.py

python310

```
"""Create a fresh, independent --through rehearsal using only embedded baseline files.

Run: python start_through_rehearsal.py

Then read through_rehearsal/EXTENSION.txt and work inside through_rehearsal.

Existing destinations are never overwritten. This script runs baseline checks,

not extension checks. Inspect their actual output and exit statuses.

"""

from pathlib import Path

import shutil

import subprocess

import sys

PROGRAM = r'''import argparse

import csv

import re

import sys

from datetime import date

FIELDS = ("task_id", "status", "due_date", "team")

def iso_date(value):

if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):

raise ValueError("date must use YYYY-MM-DD")

return date.fromisoformat(value)

def load_tasks(path):

rows = []

with open(path, newline="", encoding="utf-8") as source:

reader = csv.DictReader(source, strict=True)

missing = set(FIELDS) - set(reader.fieldnames or [])

if missing:

raise ValueError("missing required columns: " + ", ".join(sorted(missing)))

for number, raw in enumerate(reader, start=2):

if None in raw or any(raw[name] is None for name in FIELDS):

raise ValueError(f"row {number}: malformed CSV record")

if not raw["task_id"].strip():

raise ValueError(f"row {number}: task_id must not be blank")

if not raw["team"].strip():

raise ValueError(f"row {number}: team must not be blank")

if raw["status"] not in ("open", "completed"):

raise ValueError(f"row {number}: status must be open or completed")

try:

due = iso_date(raw["due_date"])

except ValueError as exc:

raise ValueError(f"row {number}: invalid due_date") from exc

row = {name: raw[name] for name in FIELDS}

row["due_date"] = due

rows.append(row)

return rows

def select_tasks(rows, as_of):

return [row for row in rows

if row["status"] == "open" and row["due_date"] < as_of]

def main():

parser = argparse.ArgumentParser(description="Report open overdue tasks")

parser.add_argument("source")

parser.add_argument("--as-of", required=True, type=iso_date)

args = parser.parse_args()

try:

rows = load_tasks(args.source)

except (OSError, ValueError, csv.Error) as exc:

parser.error(str(exc))

selected = select_tasks(rows, args.as_of)

writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS, lineterminator="\n")

writer.writeheader()

writer.writerows(selected)

if __name__ == "__main__":

main()

'''

TESTS = '''import csv

import io

import subprocess

import sys

import tempfile

import unittest

from datetime import date

from pathlib import Path

from task_report import FIELDS, load_tasks, select_tasks

ROOT = Path(__file__).resolve().parent

SAMPLE = ROOT / "task_sample.csv"

class BaselineTests(unittest.TestCase):

def cli(self, source, *flags):

return subprocess.run(

[sys.executable, str(ROOT / "task_report.py"), str(source),

"--as-of", "2026-04-15", *flags],

capture_output=True, text=True)

def test_selection(self):

selected = select_tasks(load_tasks(SAMPLE), date(2026, 4, 15))

self.assertEqual([row["task_id"] for row in selected], ["T201", "T202"])

def test_real_cli(self):

result = self.cli(SAMPLE)

self.assertEqual(result.returncode, 0, result.stderr)

reader = csv.DictReader(io.StringIO(result.stdout))

self.assertEqual(reader.fieldnames, list(FIELDS))

self.assertEqual(list(reader), [

dict(task_id="T201", status="open", due_date="2026-04-14", team="Support"),

dict(task_id="T202", status="open", due_date="2026-04-13", team="Ops")])

def test_source_errors_emit_no_report(self):

invalid_sources = [

"task_id,status,due_date\\nT1,open,2026-04-14\\n",

"task_id,status,due_date,team\\n ,open,2026-04-14,Ops\\n",

"task_id,status,due_date,team\\nT1,open,2026-04-14, \\n",

"task_id,status,due_date,team\\nT1,pending,2026-04-14,Ops\\n",

"task_id,status,due_date,team\\nT1,open,2026-02-30,Ops\\n"]

with tempfile.TemporaryDirectory() as folder:

source = Path(folder) / "invalid.csv"

for text in invalid_sources:

with self.subTest(text=text):

source.write_text(text, encoding="utf-8")

result = self.cli(source)

self.assertNotEqual(result.returncode, 0)

self.assertEqual(result.stdout, "")

self.assertIn("error:", result.stderr)

if __name__ == "__main__":

unittest.main()

'''

SAMPLE = '''task_id,status,due_date,team

T201,open,2026-04-14,Support

T202,open,2026-04-13,Ops

T203,completed,2026-04-12,Support

T204,open,2026-04-15,Support

T205,open,2026-04-16,Ops

'''

CARD = '''INDEPENDENT --through REHEARSAL: 20 MINUTES

Work only in this directory. The adjacent through_baseline_saved directory is

an untouched recovery copy, not an earlier lesson project. No --team solution

is included. Do not edit the saved baseline or weaken the existing tests.

CONTRACT — read this back aloud before editing

Add optional --through YYYY-MM-DD. When omitted, retain open tasks with

due_date strictly before --as-of. When supplied, instead retain open tasks

with due_date on or before --through. Keep --as-of required and validate both

supplied dates, even though --through replaces its eligibility cutoff.

Completed tasks always remain excluded. Preserve validation of every source

row, original output columns, and input order. Invalid dates must produce a

clear error, nonzero exit, and no CSV report.

ACCEPTANCE CRITERIA — expected, NOT observed results

At --as-of 2026-04-15:

omission:                 T201, T202

--through 2026-04-15:    T201, T202, T204

--through 2026-04-16:    T201, T202, T204, T205

T203 never appears. --through 2026-02-30 must fail with empty stdout.

Invalid --as-of with valid --through must also fail with empty stdout.

Missing --as-of must remain an error even when --through is supplied.

All existing source-validation checks must remain intact; also check invalid

rows that the new cutoff or completed-status rule would otherwise exclude.

Check exact columns, values and input order, not just membership counts.

0–3 MINUTES: CLARIFICATION AND BASELINE

Check assistance permissions. Read back the contract and inspect task_report.py,

test_task_report.py and task_sample.csv. Locate parsing, full-source validation,

selection and output. Review baseline_verification.txt, including commands,

stdout, stderr and exit statuses for BOTH the saved and working copies.

Expected baseline: T201 then T202, zero exit, and passing original tests.

Those expectations are not evidence: inspect the actual log. A failed or

unavailable check is not a verified working baseline. Record the absolute saved

baseline location and checked results in evidence.txt. It starts empty.

The saved copy contains the original baseline program and test harness, with

this rehearsal's five-row sample. No preceding lesson files were imported.

3–12 MINUTES: IMPLEMENTATION

Edit only the working task_report.py. Add the argument and connect it through

the CLI to selection while preserving two-argument selection calls and the

omission rule. Choose a small compatible selection interface. There is no

completed implementation supplied: this is your edit area.

Write your own focused tests in test_through.py, which starts empty. Include

selection-level assertions AND real subprocess CLI assertions. Do not merely

mock the CLI or compare predicted output with predicted output.

12–17 MINUTES: CHECKS AND DEBUGGING

Run the existing baseline suite and your focused suite:

python -m unittest -v test_task_report

python -m unittest -v test_through

Then run all discovered tests:

python -m unittest -v

Run the real CLI for all three acceptance memberships and both invalid-date

cases. Inspect stdout, stderr and exit status for each. For example:

python task_report.py task_sample.csv --as-of 2026-04-15

python task_report.py task_sample.csv --as-of 2026-04-15 --through 2026-04-15

python task_report.py task_sample.csv --as-of 2026-04-15 --through 2026-04-16

python task_report.py task_sample.csv --as-of 2026-04-15 --through 2026-02-30

python task_report.py task_sample.csv --as-of 2026-02-30 --through 2026-04-16

Use subprocess.run(..., capture_output=True, text=True) and inspect returncode,

stdout and stderr, or capture all three explicitly with your shell. Retain the

commands and actual results. A successful launch alone proves nothing.

Explain one hypothesis-and-check episode aloud: name the mismatch, your

hypothesis, a distinguishing observation, what you actually observed, and the

repair or next action. Do not edit fixtures or expected IDs to hide a defect.

OPTIONAL DELIBERATE MUTATION — only if no natural failure occurs

After verifying the extension, temporarily replace the new inclusive comparison

with a strict comparison. Run the equality-boundary check. Identify the missing

cutoff-equality record (T204 at 2026-04-15, or T205 at 2026-04-16). State a

hypothesis and distinguishing observation aloud; distinguish this deliberate

failure from a naturally occurring defect. Repair the comparison and rerun

focused AND baseline checks. Record actual results, not the expected failure.

17–20 MINUTES: RECOVERY AND BOUNDED HANDBACK

Write a concise evidence.txt containing:

- clarified contract and saved baseline location; checked baseline results;

- code changes, executed commands, outputs/exit statuses or saved log paths;

- exact failures and unrun checks, distinguished from passes;

- debugging mismatch, hypothesis, distinguishing check, observation and action;

- final handback: completed behavior, preservation evidence, limitations and

the next check. Do not claim production reliability from these local checks.

If recovering: first preserve unfinished work in a separate directory or diff

and record its location. Deliberately restore only the exercise files from

through_baseline_saved, then rerun the baseline CLI and original tests. Record

restoration results separately from extension completion. Restoration is NOT

completion of --through. Keep evidence and unfinished work; avoid repository-

wide destructive resets.

IF EXECUTION IS UNAVAILABLE

Write a command-and-predicate trace in evidence.txt: each intended command,

expected IDs or error predicate, and intended distinguishing observation.

Label EVERY run result UNVERIFIED, including baseline and recovery checks.

Predictions do not earn execution evidence. Do not report tests as passing.

'''

def main():

root = Path(__file__).resolve().parent

work = root / "through_rehearsal"

saved = root / "through_baseline_saved"

if work.exists() or saved.exists():

raise SystemExit("Refusing to overwrite an existing rehearsal or saved baseline.")

work.mkdir()

saved.mkdir()

for name, text in {"task_report.py": PROGRAM,

"test_task_report.py": TESTS,

"task_sample.csv": SAMPLE}.items():

(work / name).write_text(text, encoding="utf-8")

shutil.copy2(work / name, saved / name)

# Learner tests and evidence deliberately start with zero bytes.

(work / "test_through.py").touch()

(work / "evidence.txt").touch()

(work / "EXTENSION.txt").write_text(CARD, encoding="utf-8")

commands = [

[sys.executable, "task_report.py", "task_sample.csv", "--as-of", "2026-04-15"],

[sys.executable, "-m", "unittest", "-v", "test_task_report"],

]

with (work / "baseline_verification.txt").open("w", encoding="utf-8") as log:

log.write(f"Saved baseline: {saved}\nWorking copy: {work}\n")

for folder in (saved, work):

for command in commands:

heading = f"\ncwd={folder}\ncommand={command!r}\n"

try:

result = subprocess.run(command, cwd=folder, capture_output=True, text=True)

record = (f"exit={result.returncode}\nstdout:\n{result.stdout}"

f"\nstderr:\n{result.stderr}\n")

except OSError as exc:

record = f"UNVERIFIED: execution unavailable: {exc}\n"

log.write(heading + record)

print(heading + record)

shutil.copy2(work / "baseline_verification.txt", saved / "verification.txt")

print(f"Read {work / 'EXTENSION.txt'}")

print("No extension checks have been run. Inspect the baseline log before editing.")

if __name__ == "__main__":

main()
```

⋯

Run once to create an independent baseline rehearsal. Read the extension card, inspect the recorded baseline checks, then implement and verify --through within 20 minutes.

- **Lines 1–7:** Explain how to launch the rehearsal and distinguish baseline checks from extension checks.
- **Lines 9–12:** Import filesystem and subprocess tools for creating independent copies and recording real checks.
- **Lines 14–26:** Embed the fresh report’s imports, field order, and strict date parser. This is baseline code, not a completed extension.
- **Lines 29–52:** Repeat full-source validation from the worked exercise. Keep malformed-record, required-field, status, and date checks intact.
- **Lines 55–57:** Supply the original two-argument selection function. Extend this function in the generated `task_report.py`, preserving existing callers and the omission rule.
- **Lines 60–64:** Supply the existing CLI with required `--as-of`. Add the new argument here in the generated file; do not remove the existing requirement.
- **Lines 65–72:** Validate the source before selection and write the original CSV format. Connect the new value at the selection call while preserving this route.
- **Lines 75–76:** Retain the report’s direct-execution entry point.
- **Lines 79–91:** Embed the familiar baseline test imports and sample location.
- **Lines 94–112:** Preserve direct-selection and real-CLI assertions for the original T201/T202 report.
- **Lines 114–129:** Preserve invalid-source checks requiring errors and no CSV report.
- **Lines 132–133:** Retain the baseline test file’s direct-execution entry point.
- **Lines 136–142:** Supply the original four records plus future task T205, giving the new cutoff a distinct additional boundary.
- **Lines 144–157:** Begin the extension card with the time budget, independent-copy instructions, and clarified date, status, validation, and output contract.
- **Lines 159–169:** Specify expected memberships and error cases, including invalid or missing `--as-of` despite a supplied `--through`. These are criteria, not recorded passes.
- **Lines 171–181:** Allocate clarification and baseline time and require inspection of actual checks for both saved and working copies.
- **Lines 183–190:** Define the learner’s implementation and test-writing work. The generated `test_through.py` starts empty; write selection and subprocess CLI checks there.
- **Lines 192–207:** Provide commands for baseline, focused, and discovered tests, plus real CLI cases. Capture contents, errors, and exit statuses rather than recording only that commands launched.
- **Lines 209–211:** Require a spoken mismatch-to-hypothesis-to-check episode without weakening fixtures or expectations.
- **Lines 213–219:** Offer a labeled deliberate comparison mutation if no natural failure occurs. Diagnose its boundary mismatch before repairing it and rerunning both kinds of checks.
- **Lines 221–228:** Specify the evidence record and bounded handback, separating passes, failures, unrun checks, and local limitations.
- **Lines 230–235:** Require preservation of unfinished work before selective restoration and distinguish restored baseline behavior from extension completion.
- **Lines 237–241:** Define the written-trace alternative when execution is unavailable. Every run result must remain labeled unverified.
- **Lines 245–252:** Locate the working and saved directories and refuse to overwrite either existing destination.
- **Lines 253–257:** Write the embedded baseline files into the working directory and copy them into the separate recovery directory.
- **Lines 258–261:** Create empty learner-test and evidence files and write the extension card into the working directory.
- **Lines 262–265:** Define the baseline CLI and test commands that setup will execute.
- **Lines 266–278:** Run both commands in both directories, log their locations and actual results, and mark execution failures unverified.
- **Lines 279–281:** Copy the baseline log into the saved directory and direct you to the card. Extension checks remain unverified until you execute and inspect them.
- **Lines 284–285:** Launch rehearsal setup when this script is executed directly.

Run `python start_through_`[`rehearsal.py`](https://www.educative.io/courses/forward-deployed-engineer/rehearsal.py), open the generated `through_rehearsal` directory, and read `EXTENSION.txt`. Modify the generated report code, not the program embedded in the setup script. The setup script runs baseline checks. Inspect `baseline_verification.txt` and confirm they passed before treating the saved copy as a verified working baseline.

The new future-task requirement replaces the existing eligibility cutoff rather than adding another filter. Keep the existing tests and add checks for the new rule. Passing the new tests alone does not verify behavior when the new option is omitted.

If you cannot execute the code, provide a written trace and mark all predicted run results as unverified. A written trace is not execution evidence.

For your submission, identify one narrowly scoped extension and record the exact baseline command before making changes. A verified, recoverable baseline helps isolate regressions and restore the original behavior if the extension fails.

Presenting and Defending Your Decisions

Customer Role-Play and Scope Changes

Ask

[Clarifying the extension request](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Clarifying-the-extension-request)

[Saving a verified baseline](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Saving-a-verified-baseline)

[Making the smallest change](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Making-the-smallest-change)

[Debugging out loud](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Debugging-out-loud)

[Verifying the agreed behavior](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Verifying-the-agreed-behavior)

[When time runs out](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#When-time-runs-out)

[Practice: the --through extension](https://www.educative.io/courses/forward-deployed-engineer/handling-live-extension-exercises#Practice-the---through-extension)