# Code_Quality_Testing_and_Reproducibility_in_FDE_Assignments

Source: https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Code Quality, Testing, and Reproducibility

Identify how undocumented file paths, suppressed exceptions, and tests that only check file existence can conceal failures in a submission. Write assertions that verify expected behavior, introduce controlled code mutations to verify that tests detect failures, and confirm that the project runs with a single command from a fresh repository clone so reviewers can reproduce the results without relying on undocumented setup steps.

We'll cover the following...

- [Separating code responsibilities](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Separating-code-responsibilities)
- [Writing behavioral assertions](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Writing-behavioral-assertions)
- [Testing with deliberate mutations](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Testing-with-deliberate-mutations)
- [Adding end-to-end smoke tests](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Adding-end-to-end-smoke-tests)
- [Clean-clone verification](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Clean-clone-verification)
- [Can you repair the refund-report handoff?](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Can-you-repair-the-refund-report-handoff)

The maintenance report runs successfully in the developer’s local environment. The report fails from a fresh repository clone because the script references `/Users/dev/Downloads/assets.csv`, a local file that is not included in the repository. The screenshot shows a completed report, but the reviewer cannot reproduce the result.

Another version catches all exceptions and generates an empty report instead of reporting the failure. An unreadable input file is incorrectly reported as a successful run with no assets requiring service.

A reproducible handoff requires clearly separated responsibilities, tests that detect incorrect behavior, and a verified execution path from a fresh repository clone.

For this separate assignment, read `service_assets.csv` and select records where `status` is exactly `active` and `service_hours >= 100`. Preserve the relative order of qualifying records from the input file. Use the following fixture to verify the results:

Ace Editor

1

2

3

4

5

6

asset\_id,service\_hours,status

A1,120,active

A2,100,active

A3,99,active

A4,150,retired

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** Names the three required input columns.
- **Lines 2–3:** Supply the above-threshold and exact-threshold active assets.
- **Lines 4–5:** Supply exclusions for insufficient hours and retired status.

The expected report has columns `asset_id,service_hours` and records `A1,120` followed by `A2,100`. A valid input with no qualifying assets produces a header-only report successfully. Invalid or unreadable input must fail before report writing.

## Separating code responsibilities[#](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Separating-code-responsibilities)

The tempting shortcut combines a machine-specific path, selection, and error suppression:

Ace Editor

1

2

3

4

5

6

7

try:

assets = read\_assets('/Users/dev/Downloads/assets.csv')

due = select\_due\_assets(assets)

except Exception:

due = []

write\_report('service\_due.csv', due)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Lines 1–3:** Read an untracked absolute path and attempt selection.
- **Lines 4–5:** Convert every failure, including programming defects, into an empty result.
- **Line 6:** Write a plausible success artifact even when input handling failed.

A file-existence test accepts this failure. Repair the path, failure boundary, and assertions before considering more infrastructure.

For this workflow, one module with four named functions is enough:

- `read_assets(input_path)`: Read and validate the complete CSV.
- `select_due_assets(assets)`: Apply the status and inclusive threshold rules without filesystem effects.
- `write_report(output_path, assets)`: Write the customer-facing columns in order.
- `main(argv)`: Parse explicit paths, orchestrate the workflow, and translate expected failures into command-line behavior.

Reject missing required columns and nonnumeric, nonfinite, or negative hours. An unreadable file needs a message identifying the input path. At the **CLI boundary**, where application results become process results, expected validation and filesystem failures become standard-error messages and nonzero exits. Unexpected programming defects should remain visible rather than being disguised as success.

Inspect the files and predict the intended response to an asset with `service_hours=NaN`. The displayed `service_due.py` is incomplete: **line 38** contains `def_placeholder`.

Use the completion below before running tests or the prediction experiment:

Files

service\_due.py

test\_service\_due.py

verify\_service.py

service\_assets.csv

service\_run.md

markdown

```
import subprocess

import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():

checks = subprocess.run(

[sys.executable, '-m', 'unittest', '-v', 'test_service_due'], cwd=ROOT)

if checks.returncode != 0:

print('Verification failed; fixture workflow was not run.', file=sys.stderr)

return checks.returncode

output = ROOT / 'output' / 'service_due.csv'

workflow = subprocess.run(

[sys.executable, str(ROOT / 'service_due.py'),

'--input', str(ROOT / 'service_assets.csv'), '--output', str(output)], cwd=ROOT)

if workflow.returncode != 0:

return workflow.returncode

print(f'LOCAL FIXTURE RUN: report written to {output}')

print(output.read_text(encoding='utf-8'), end='')

return 0

if __name__ == '__main__':

raise SystemExit(main())
```

⋯

Inspect the files and predict what happens for an asset with service\_hours=NaN: is a report created, is the exit status zero, and what message appears? Then click Run to execute the tests and the fixture workflow.

The `service_due.py` has four functions:

- `read_assets` validates the whole CSV before returning anything;
- `select_due_assets` applies the active-status and inclusive 100-hour rules with no file access;
- `write_report` writes only the two customer columns; and main turns expected input and file errors into a stderr message and exit status 1, while letting real programming bugs stay visible. The tests check exact records and order, the 100-hour boundary, the retired exclusion, four kinds of invalid hours, a missing column, and three real command runs.
- `verify_service.py` runs the tests first and only then runs the workflow on the fixture

To complete the displayed application, replace `def_placeholder` on **line 38**, including its leading space, with this implementation:

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

18

19

20

21

22

23

24

25

26

27

def select\_due\_assets(assets):

return [row for row in assets

if row['status'] == 'active'

and Decimal(row['service\_hours']) >= 100]

def write\_report(output\_path, assets):

path = Path(output\_path)

path.parent.mkdir(parents=True, exist\_ok=True)

with path.open('w', encoding='utf-8', newline='') as destination:

writer = csv.DictWriter(destination, fieldnames=['asset\_id', 'service\_hours'])

writer.writeheader()

for row in assets:

writer.writerow({key: row[key] for key in writer.fieldnames})

def main(argv=None):

parser = argparse.ArgumentParser(description='Report active assets due for service')

parser.add\_argument('--input', required=True, type=Path)

parser.add\_argument('--output', required=True, type=Path)

args = parser.parse\_args(argv)

try:

assets = read\_assets(args.input)

due = select\_due\_assets(assets)

write\_report(args.output, due)

except InputError as error:

print(str(error), file=sys.stderr)

return 1

except OSError as error:

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Selection has no filesystem effects. Report writing receives an explicit path and emits only the required columns. The CLI catches expected input and filesystem failures, not every exception.

With this completion, validation finishes before output writing begins. One invalid row therefore prevents a misleading partial report. The NaN experiment should produce a nonzero application exit, the finite-and-nonnegative error, and no report; these remain expected outcomes until executed.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27741%27%20height=%27301%27/%3e)![Complete CLI flow](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Complete CLI flow")

Complete CLI flow

## Writing behavioral assertions[#](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Writing-behavioral-assertions)

A **behavioral test** asserts an observable acceptance criterion. It can call a public helper, but its expectation concerns the required result rather than private implementation steps.

Derive assertions directly from this brief:

- **Exact membership and order:** The selected records are exactly `A1/120` and `A2/100`, in that order. This detects missing A2, unexpected A3, and incorrectly included A4.
- **Equality:** An active asset at exactly 100 qualifies. Include a dedicated threshold test so this boundary is easy to locate.
- **Retirement:** A4 is excluded despite its 150 hours.
- **No matches:** Valid input produces a successful report containing only `asset_id,service_hours`.
- **Invalid hours:** Text, `NaN`, infinity, and negative values produce validation failures rather than an empty selection.
- **Unusable schema:** A missing `status` column produces a useful validation failure.

Avoid assertions such as “the parser helper was called once.” A reasonable refactor could change that call count while preserving every customer-visible result.

The report’s contents matter because they drive the maintenance decision. Merely asserting that some file exists leaves its membership, values, order, and even header unchecked.

## Testing with deliberate mutations[#](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Testing-with-deliberate-mutations)

Executing a line does not establish that its behavior was checked. Coverage records execution; assertions determine which mistakes become visible.

Use a **deliberate mutation**: A temporary, intentional defect introduced to check whether the relevant test notices. The useful habit is to provide tests that fail when the answer changes.

Perform the whole cycle:

1. Run the original suite with `python -m unittest -v test_service_due`. Establish the baseline before changing anything.
2. In `select_due_assets`, replace `Decimal(row[‘service_hours’]) >= 100` with `Decimal(row[‘service_hours’]) > 100`.
3. Run the same suite again. Inspect the failing exact-record assertion and the dedicated equality assertion.
4. Restore `>=` and rerun the suite. Keep the corrected implementation in the submission.

With the mutation, A1 still qualifies because 120 is greater than 100. A2 disappears because 100 is not greater than 100. A3 and A4 remain excluded.

The exact-record assertion now compares expected `[(‘A1’, ‘120’), (‘A2’, ‘100’)]` with actual `[(‘A1’, ‘120’)]`. A check that the report file exists still passes: The program wrote a report containing the wrong records.

Predict each check separately for the threshold mutation and for removal of the entry-point call. Also consider what happens when the tracked fixture is absent. Compare your predictions with the interaction’s explanations.

Predict which service\_due.py checks fail

↓ Entry

📄Tracked service\_assets.csv

↓ Entry

🔧Defect 1: >= 100 becomes > 100

↓ Entry

🚪Defect 2: Remove the entry-point call

📁Fresh report file exists

🔍Helper returns exact records

✅Subprocess success generates exact report

⚠️Subprocess missing-input behavior

106%

Failure simulator

Pick a component to knock out — see how far the damage spreads.⌀ badges show each node’s blast radius — the bigger the number, the closer it is to a single point of failure.

Do you find this helpful?

Removing the entry-point call leaves helper assertions intact, but the script can exit zero without doing any work. The success smoke test must therefore check the generated CSV, not status alone. The missing-input smoke test also detects the absent error handling: it expects nonzero status and an identifying message.

Catching the threshold mutation is targeted evidence for the inclusive boundary. It does not establish entry-point wiring or fixture availability. The results described here are expected results; no execution transcript is being claimed.

## Adding end-to-end smoke tests[#](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Adding-end-to-end-smoke-tests)

A **smoke test** is a small end-to-end check through the real entry point. Here, a subprocess launches `service_due.py` with the current Python interpreter, explicit arguments, and an explicit working directory.

The package’s successful smoke test:

1. Creates a fresh temporary destination.
2. Runs the actual script on the tracked fixture.
3. Checks exit status zero.
4. Parses the generated CSV and checks its columns and exact records.

A second subprocess test supplies a nonexistent input in another fresh destination. It requires a nonzero exit, standard error containing `Cannot read input` and the missing filename, and no generated report.

These checks expose broken argument handling, missing entry-point wiring, and output-directory behavior that an isolated selection test cannot exercise. Using a fresh destination matters: A report left by yesterday’s successful run cannot serve as evidence for today’s failed command.

## Clean-clone verification[#](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Clean-clone-verification)

The package uses Python 3.12 and only its standard library. No third-party installation, service account, API key, container runtime, or hosted application is needed.

Track these five handoff files: the completed `service_due.py`, `service_assets.csv`, `test_service_due.py`, `verify_service.py`, and `service_run.md`. Keep generated reports out of the committed inputs.

Put these instructions in `service_run.md`:

> **Requirements:**
>
> - Python 3.12, available as `python` in the active environment.
> - No third-party packages or credentials needed.
>
> **How to run:**
>
> From the repository root, run `python verify_service.py`.
>
> The command first runs the focused tests. If any test fails, it stops with a nonzero exit status. If all tests pass, it runs the real workflow on `service_assets.csv` and creates `output/service_due.csv`.
>
> **Expected output:**
>
> The rows should appear in this order. On success, the command prints `LOCAL FIXTURE RUN` and the output file path.
>
> **Limits:**
>
> This only verifies behavior on local fixture data. It makes no claim about live integrations or live model quality.

The runner uses `sys.executable` for both subprocesses, so verification uses the same interpreter throughout. It propagates failure instead of printing a success message after a failed check.

Verify the committed revision independently:

1. Clone the committed repository into a separate directory. Do not copy the existing working folder or its generated output.
2. Create a fresh environment with the supported runtime. On Windows, use `py -3.12 -m venv .venv`, then `.venv\Scripts\activate` in Command Prompt. On macOS or Linux, use `python3.12 -m venv .venv`, then `source .venv/bin/activate`.
3. Confirm `python --version` reports Python 3.12, then run `python verify_service.py` from the repository root.
4. Inspect the exit status and parse the generated report. Record the revision and environment actually checked.

If a project uses third-party packages, commit reproducible dependency declarations and document their installation command or include installation in a bootstrap command. Relying on a package installed globally on the author’s machine recreates the original handoff problem.

Containers and hosting are optional unless the assignment requires them. Neither repairs a missing fixture, and each should earn any extra prerequisite it imposes on the reviewer.

## Can you repair the refund-report handoff?[#](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Can-you-repair-the-refund-report-handoff)

Apply the same evidence chain to an independent refund task. The starting implementation reads `~/Downloads/refunds.csv`, selects `amount < 50`, catches all exceptions as empty success, and has only a file-existence test.

Write your repair or concrete implementation-and-test specification in the empty `refund_answer.txt`. Inspect `refund_due_bad.py` as the defective starting point, not a completed answer. You may use a different module layout if responsibilities and verification remain clear.

Run `refund_task.py` after writing an attempt to reveal its self-review checklist. If you implement runnable tests, `python refund_task.py --tests MODULE` can execute your unittest module. The checklist does not automatically grade a specification or establish clean-clone reproducibility.

Files

refund\_task.py

refund\_answer.txt

refunds.csv

refund\_due\_bad.py

python310

```
import argparse

import subprocess

import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parent

ANSWER = ROOT / 'refund_answer.txt'

TASK = """Independent refund-report repair

Inspect refund_due_bad.py separately; it is defective, not a completed answer.

Its sole existing test invokes main() and asserts

Path('refund_due.csv').exists(). It leaves report contents unchecked.

Write code or a concrete implementation-and-test specification in the empty

refund_answer.txt. You may add implementation, tests, and handoff files alongside

it and identify those files in your answer. No particular module count,

container, web interface, or dependency manager is required.

Use the tracked refunds.csv unchanged:

refund_id,amount,status

R1,49,requested

R2,50,requested

R3,51,requested

R4,20,paid

Select exact status requested and finite, nonnegative amount at most 50.

Preserve input order and output only refund_id,amount. Expected records are

exactly [('R1', '49'), ('R2', '50')]. Exclude R3 for amount and R4 for status.

A valid no-match input may succeed with a header-only report. Invalid or

unreadable input must fail visibly with nonzero status before report writing.

Your handoff must supply:

- Explicit paths, responsibility boundaries, and narrow expected-error handling.

- Exact-output, equality-boundary, invalid-input, and unreadable-input assertions.

- A real-entry-point subprocess smoke test using the current interpreter,

explicit working directory, tracked fixture, and a fresh temporary output.

Check status and parsed CSV, not just file existence.

- A reversible boundary mutation: repair to <= 50, establish the baseline,

mutate <= to <, name the exact assertion that must break, restore <=,

and rerun. Distinguish predictions from observed results.

- Clean-clone prerequisites and one verification command that runs tests,

propagates failures, and only then generates a labeled local fixture report.

State the supported runtime and actual dependency installation path, or

explicitly say standard-library-only. Describe a separate fresh-clone check

without copied local data, old reports, or credentials. Limit evidence claims

to fixture behavior.

Run this script again after writing an attempt to reveal the reference checklist.

Optional: --tests MODULE runs your unittest module using the current interpreter

from the repository root, after an attempt exists. It reports actual process

status; it does not automatically grade a prose specification or prove a clean

clone. Without execution, supply concrete assertions and label results unobserved.

"""

def show_checklist():

print("""Reference checklist: compare your attempt, then revise

[ ] Explicit input/output paths and tracked refunds.csv replace Downloads.

[ ] Functions separate complete input validation, pure selection, output, and

CLI handling; module count is not graded.

[ ] Missing columns, malformed records, nonnumeric/nonfinite/negative amounts

fail before writing. Expected input and operational failures cross a narrow

boundary to useful stderr and nonzero status; bugs are not empty success.

[ ] Unreadable-input subprocess assertion checks nonzero status, stderr naming

the input problem/path, and no new report in a fresh destination.

[ ] Successful CSV assertion checks columns ['refund_id', 'amount'] and exactly

[('R1', '49'), ('R2', '50')] in order, including R2 at exactly 50.

R3 and R4 are excluded; valid no-match input is header-only success.

[ ] Smoke test uses sys.executable, the real script, explicit arguments and cwd,

the tracked fixture, a fresh temporary output, status, and parsed CSV.

[ ] Mutation evidence starts with repaired <= 50 and a passing baseline.

Temporarily changing <= to < must break the exact-record assertion:

expected [('R1', '49'), ('R2', '50')], actual [('R1', '49')].

A dedicated equality assertion should also fail. Restore <= and rerun.

File existence alone would miss this defect.

[ ] Handoff names a supported runtime and either an actual dependency install

command with tracked declarations or an explicit standard-library-only claim.

[ ] One command, for example python verify_refunds.py, runs tests, propagates

failures, and only then generates a report labeled LOCAL FIXTURE RUN.

[ ] Independently clone the committed revision into another directory, prepare

the documented fresh environment, and run that command. Do not copy local

data, generated reports, or credentials. Record revision, environment,

status, and parsed report only if actually checked.

[ ] Claims are fixture-only. Predicted mutation effects and planned clean-clone

checks are not execution evidence. Minimal correct handoffs earn full credit;

extra infrastructure does not replace assertions.

This is acceptance-based self-review, not an automatic correctness verdict.

""")

def main():

parser = argparse.ArgumentParser(description='Independent refund handoff workspace')

parser.add_argument('--tests', metavar='MODULE', help='Run your unittest module')

args = parser.parse_args()

print(TASK)

try:

attempt = ANSWER.read_text(encoding='utf-8')

except OSError as error:

print(f'Cannot read answer area: {error}', file=sys.stderr)

return 1

if not attempt.strip():

print('Answer area is empty. Write your attempt in refund_answer.txt first.')

return 0

print('Attempt found. No correctness or execution result is implied.')

show_checklist()

if args.tests:

result = subprocess.run(

[sys.executable, '-m', 'unittest', '-v', args.tests], cwd=ROOT)

print(f'Observed test-process exit status: {result.returncode}')

return result.returncode

print('No test module requested. Use --tests MODULE if you have runnable tests.')

return 0

if __name__ == '__main__':

raise SystemExit(main())
```

⋯

Write your independent repair or concrete implementation-and-test specification in the empty refund\_answer.txt. Run refund\_task.py to submit an attempt and reveal the reference checklist. The defective script is not an answer.

- `refund_answer.txt` starts empty. Put your implementation or concrete specification here, identifying any additional files you create.
- `refund_due_bad.py` is the defective starting point: it reads a hidden home-directory path, uses a strict amount < 50 comparison, turns every exception into an empty success, and always exits 0.
- `refund_task.py` shows the task and reveals a self-review checklist once refund\_answer.txt contains your attempt.

The weak starting test cannot distinguish an empty report caused by suppressed input failure from a legitimate no-match result. Your assertions must make that distinction observable. Record predictions as predictions, and claim mutation or clean-clone results only after performing those checks.

A convincing handoff gives the reviewer both a usable command and a way to challenge its result. Additional infrastructure earns no credit when the decisive evidence is still missing.

Evaluating and Guardrailing LLM Output

Designing Around the End User's Workflow

Ask

[Separating code responsibilities](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Separating-code-responsibilities)

[Writing behavioral assertions](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Writing-behavioral-assertions)

[Testing with deliberate mutations](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Testing-with-deliberate-mutations)

[Adding end-to-end smoke tests](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Adding-end-to-end-smoke-tests)

[Clean-clone verification](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Clean-clone-verification)

[Can you repair the refund-report handoff?](https://www.educative.io/courses/forward-deployed-engineer/code-quality-testing-and-reproducibility#Can-you-repair-the-refund-report-handoff)