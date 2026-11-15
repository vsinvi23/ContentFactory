# Selecting_the_Right_Stack_and_Structuring_Your_FDE_Project

Source: https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Choosing a Stack and Project Structure

Explore how to choose a familiar, minimal stack by attaching a required job to every component. Understand how to structure a repository so a reviewer can find the entry point, core rule, inputs, and checks in minutes, preparing you to avoid over-engineering without losing clarity.

We'll cover the following...

- [Justifying each component](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Justifying-each-component)
- [Choosing a minimal stack](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Choosing-a-minimal-stack)
- [Structuring one inspectable process](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Structuring-one-inspectable-process)
- [Making the repository navigable](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Making-the-repository-navigable)
- [When to add tools](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#When-to-add-tools)
- [Practice: The workshop app](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Practice-The-workshop-app)
  - [Compare with a Streamlit proposal](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Compare-with-a-Streamlit-proposal)

Which components are necessary for a dispatch-report submission: a browser frontend, web server, database, job queue, containers, or Python?

Consider the following fictional assignment brief:

> - Build a local command that you run whenever you need it. It should read `shipments.csv`, list every shipment whose status is exactly `delayed`, and write the results to a readable report.
> - If the input can’t be read, the command must fail visibly instead of producing an empty report that looks successful.
> - Include focused checks and instructions for running the command. Hosting, browser access, saving data between runs, scheduling, and login are not required.

The required data path is short: Read CSV records, select delayed shipments, and write their identifiers and regions. Python can perform every step in one process.

Choose the smallest understandable implementation that preserves the required workflow and makes its behavior easy to inspect.

## Justifying each component[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Justifying-each-component)

The proposed repository includes `frontend/`, `backend/`, `worker/`, `infrastructure/`, and database migrations. The author also proposes containerization to make the project appear production-ready. Before accepting the proposed architecture, identify the requirement that justifies each runtime component. Identify any reasoning biases reflected in the proposals. Select “none” when no listed bias applies. This does not establish that the component is necessary.

Annotate each component: brief obligation or removal rationale

AI Analysis Report

Tag each sentence that hides a statistical bias, then submit your audit.

0 / 3 flagged

frontend/: To judge what this submission needs, consider only browser-based repository examples; their interfaces suggest we should include one too.

backend/: Successful multi-service submissions include a separate backend server, so we should copy that structure without examining unsuccessful attempts.

worker/: Add a queue-driven worker to run the report outside the main process, although the brief asks for an on-demand local command.

infrastructure/: Include hosting configuration alongside the local command, although the brief supplies no deployment destination.

Database migrations: Define stored shipment tables, although the report only needs to read shipments.csv and retain no records between runs.

Containers: The newest repository examples use containers, so add them solely to make this submission look production-ready.

Python report logic: Keep a local command that reads shipments.csv, selects supplied status exactly equal to delayed, writes identifiers and regions, and visibly fails on unreadable input; include focused checks and execution instructions.

Do you find this helpful?

The frontend has no browser task to support. The worker has no scheduled or background task. The database has no requirement to retain records between runs. Hosting infrastructure has no deployment destination. A separate backend server adds a network boundary to a workflow that can execute locally.

Removing these components preserves the customer’s capability: They still invoke a command and receive the requested report. Containers could serve a concrete environment requirement, but appearance alone supplies no such requirement here.

Useful submission qualities include working code, sensible structure, edge-case handling, and a clear explanation of choices. Treat these as guidance, rather than a fixed employer scoring formula.

## Choosing a minimal stack[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Choosing-a-minimal-stack)

A **stack** is the set of languages, libraries, and runtime tools used to deliver the application. Choose it against the workflow, assignment constraints, your familiarity, setup burden, and ease of explanation.

For this example, assume you know Python’s `csv`, `argparse`, and `unittest`, with limited experience using browser frameworks or containers. The supplied CSV is small and already well formed:

Ace Editor

1

2

3

4

shipment\_id,status,region

S201,delayed,North

S202,delivered,East

S203,delayed,West

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** Names the three fields used by the report.
- **Lines 2–4:** Supply two delayed shipments and one delivered shipment; no inferred lateness or date calculation is needed.

Three approaches could produce the required report:

- **Standard-library command:** Covers CSV reading, argument parsing, selection, report writing, and checks with familiar tools. After installing the documented Python version, there are no third-party packages to install. Explaining the run path takes three operations: Read, select, write.
- **Command with a familiar data library:** Also covers the requirements. It adds a package installation and dependency declaration. It can be the clearer choice when required operations involve transformations that the learner already expresses confidently with that library.
- **Multi-service application:** Can cover the requirements if it also supplies the requested local command, but introduces service startup, configuration, and cross-component tracing. This learner would also spend effort learning tools that contribute no requested capability.

Choose the standard-library command for these records and this familiarity profile. Another learner could reasonably choose a familiar data library when it substantially simplifies the required work.

**Dependencies** are libraries or tools the project requires. Every installation or configuration step becomes part of the handoff. Count that burden, but do not turn dependency count into a competition: One familiar library can remove more complexity than it adds.

## Structuring one inspectable process[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Structuring-one-inspectable-process)

Consider the same S201 record in three implementations:

1. **Multi-service implementation:** The browser uploads S201 to a server, the server stores it in a database, a queue passes work to a worker, and the worker selects S201 and produces a report. S201 still qualifies because its supplied status is `delayed`; the additional transitions contribute no requested behavior.
2. **Tangled script:** One loop parses arguments, opens the CSV, checks `row[“status”]`, and writes formatted strings. S201 may still reach the report correctly, but finding or checking the selection rule requires reading through file and interface details. A vaguely named `main.py` gives little guidance about where that rule lives.
3. **Single process with named responsibilities:** The entry point coordinates reading, selection, and writing. S201 moves through ordinary Python function calls, and the status rule can be inspected or checked separately.

An **entry point** is where execution begins. Keep its orchestration thin: It should connect the steps while leaving their substantive work in clearly named functions.

For the third implementation, use this repository layout:

- `README.md`: Prerequisite, sample command, expected behavior, and check command.
- `dispatch_report/__init__.py`: Marks the application package.
- `dispatch_report/__main__.py`: Parses input and output paths, coordinates execution, and surfaces failures.
- `dispatch_report/files.py`: Defines `read_shipments` and `write_report`.
- `dispatch_report/selection.py`: Defines `select_delayed`.
- `samples/shipments.csv`: Contains the supplied three records.
- `tests/test_selection.py`: Checks the delayed-status decision.
- `tests/test_command.py`: Checks report contents and visible command failure.
- `.gitignore`: Excludes generated `outputs/` files and local Python artifacts.

The generated report belongs at `outputs/delayed.txt`; it is distinct from the supplied sample input. The writer creates the output’s parent directory when needed, so a clean clone does not need an existing `outputs/` folder.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27924.6999999999999%27%20height=%27210.7%27/%3e)![One Python process](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "One Python process")

One Python process

These boundaries remain inside one process. They require neither separate services nor abstract base classes. A smaller submission using clearly separated functions in one file is also defensible; extract a module when it clarifies a responsibility, rather than to reach a prescribed file count.

Now inspect the implementation before running anything. Record your predictions in the empty response fields in `README.md`, saving them locally if no response editor is available. Then reveal its comparison and read the walkthrough below. This is a self-check, not an automatic grader; execution afterward is optional.

Files

dispatch\_report/\_\_main\_\_.py

dispatch\_report/\_\_init\_\_.py

dispatch\_report/files.py

dispatch\_report/selection.py

samples/shipments.csv

tests/test\_selection.py

tests/test\_command.py

.gitignore

README.md

markdown

```
import argparse

from pathlib import Path

import sys

from .files import read_shipments, write_report

from .selection import select_delayed

def main(argv=None):

parser = argparse.ArgumentParser(description='Write a delayed shipment report.')

parser.add_argument('--input', type=Path, required=True)

parser.add_argument('--output', type=Path, required=True)

args = parser.parse_args(argv)

try:

shipments = read_shipments(args.input)

delayed = select_delayed(shipments)

write_report(delayed, args.output)

except (OSError, UnicodeError) as error:

print(f'dispatch_report: file access failed: {error}', file=sys.stderr)

return 1

return 0

if __name__ == '__main__':

raise SystemExit(main())
```

⋯

Inspect the complete files, record your predictions in README.md, then open the comparison. Execution is optional and requires Python 3.10 or newer

In `dispatch_report/__main__.py` file:

- **Lines 10–13:** Argument parsing produces `Path` objects so file handling stays outside the command interface.
- **Lines 15–17:** Thin orchestration connects read, select, and write without embedding their responsibilities.
- **Lines 18–21:** File access or encoding failure returns nonzero immediately; it is not converted into an empty record list.
- **Lines 24–25:** The module guard translates main’s return value into the process exit status.

In `dispatch_report/files.py` file:

- **Lines 5–6:** Materializing `DictReader` inside the context keeps reading within the lifetime of the open UTF-8 file.
- **Line 10:** Parent creation supports a clean checkout without an existing output directory.
- **Lines 11–15:** Formatting belongs to the writer, including an explicit successful zero-selection message.

In `dispatch_report/selection.py` file:

- **Line 2:** The supplied status is compared exactly; no normalization or inferred lateness is introduced.

In `tests/test_selection.py` file:

- **Lines 8–13:** Ordinary supplied records test the decision independently of file access.

In `tests/test_command.py` file:

- **Lines 11–16:** A subprocess checks the actual package entry point using the current Python interpreter, capturing errors separately from standard output.
- **Lines 18–25:** A temporary destination verifies parent creation and exact report contents, including exclusion of the delivered record.
- **Lines 27–35:** Missing input must produce readable failure and must not reach directory creation.
- **Lines 37–45:** A readable input with no delayed records must succeed, distinguishing zero selection from unreadable input.

The entry point only connects read, select, and write; the status rule lives alone in selection.py; failures return a nonzero exit instead of an empty report; and two test files check the decision and the full command separately.

The expected report contains `S201 / North` and `S203 / West`, with no S202. These are expected results from the supplied records. The code has not been run or tested.

Separating file operations from the decision lets a selection check pass ordinary records directly to `select_delayed`. A command check then covers the connections and failure behavior. Both are useful because a correct selection function alone cannot establish that the command reads or writes the right files.

## Making the repository navigable[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Making-the-repository-navigable)

Use two minutes as a course orientation heuristic, not an employer rule. Starting at the repository root, locate:

- The sample command in `README.md`.
- The entry point in `dispatch_report/__main__.py`.
- The exact status rule in `dispatch_report/selection.py`.
- The input under `samples/` and output destination under `outputs/`.
- The focused checks under `tests/`.

After the documented Python prerequisite, the sample command is:

Ace Editor

1

python -m dispatch\_report --input samples/shipments.csv --output outputs/delayed.txt

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Run it from the repository root using the documented Python interpreter. The `-m` form starts the package’s `__main__.py`; `write_report` creates `outputs/` before writing the report.

If the input cannot be opened, the entry point displays a clear error on standard error and exits with a nonzero status. It skips selection and writing rather than inventing an empty record list. Any preexisting report remains unchanged; do not mistake it for a fresh result.

For the proposed checks, the README can give:

Ace Editor

1

python -m unittest discover -s tests

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Finding these items demonstrates navigability. Finding these items shows the project is navigable; it doesn’t prove correctness or reproducibility, which still need a run from a clean clone.

## When to add tools[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#When-to-add-tools)

Require a concrete trigger and a job for each addition:

- **Supplied database requirement:** Database access earns a place because the workflow must read or write that database.
- **Required browser interaction:** A small, familiar browser interface earns a place because a local-command-only submission would omit required behavior.
- **Required API integration:** A familiar HTTP client can simplify the required requests and response handling.
- **Mandatory unfamiliar tool:** Accommodate the tool and make its setup explicit. Familiarity is a preference within the assignment’s constraints, not permission to replace them silently.

The dispatch brief supplies no scheduling or durable-storage requirement. Do not prebuild queues, adapters, or a generic plugin system for extensions that nobody requested. Add a boundary when an actual responsibility needs one.

## Practice: The workshop app[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Practice-The-workshop-app)

Use this independent fictional brief:

> In 180 active-work minutes, create a local browser interface where a workshop coordinator uploads a well-formed CSV containing `workshop_id`, `capacity`, and `booked`, then sees remaining seats for every workshop. Include focused checks, documented execution, and a README. No hosting, login, persistence, or scheduling is required.

The supplied rows are W1/20/15 and W2/12/12. Expected remaining seats are `20 − 15 = 5` and `12 − 12 = 0`.

Assume you know Python, `csv`, `unittest`, and Streamlit, but have not used containers or a separate JavaScript frontend.

Write your independent architecture proposal before consulting the comparison below. Include:

- Your stack and each component’s required role.
- A repository sketch, entry point, sample input, and checks.
- Setup obligations and an upload-to-calculation-to-display trace.
- Reasons for rejecting the proposed database and worker.
- Your assessment of the activity’s two claims.

You do not need to implement the interface or calculate another time budget. Supplied input:

Ace Editor

1

2

3

4

csv workshop\_id,capacity,booked

W1,20,15

W2,12,12

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

input

Assume you know:

Workshop Capacity — Architecture Proposal

Your task

You are proposing a small, inspectable application for a workshop coordinator. Preserve the required browser workflow while choosing components you can justify and documenting a repository another reviewer can follow.

Tap any claim to classify it, and click on References to verify authorities.

TOWorkshop coordinatorFROMArchitecture reviewerDATEOctober 19, 2026SUBJECTLocal browser workflow for workshop capacity

Background

> “In 180 active-work minutes, create a local browser interface where a workshop coordinator uploads a well-formed CSV containing `workshop_id`, `capacity`, and `booked`, then sees remaining seats for every workshop. Include focused checks, documented execution, and a README. No hosting, login, persistence, or scheduling is required.”

Supplied input: W1 has capacity 20 and 15 booked; W2 has capacity 12 and 12 booked.

Assume you know Python, `csv`, `unittest`, and Streamlit, but have not used containers or a separate JavaScript frontend.

Issue

Write an independent architecture proposal before consulting the comparison answer. Include your chosen stack, each component's requirement-serving role, a small repository sketch, the execution entry point, and a trace from uploaded CSV through calculation to the displayed table. Identify sample inputs and focused checks, document setup obligations, and explain why you reject the proposed database and worker additions. Also assess the two short claims below. No implementation or additional time budget is needed.

Analysis

“A command-only report is sufficient because it calculates the same values” — supported by the dispatch-report brief's requirement for an on-demand local command.

“A database and worker are necessary to make the submission professional.” A mandatory professional-submission rule requires both components even when the brief has no retained-state or background-task requirement.

Choosing a familiar browser framework guarantees that the reviewer can run the application from a clean clone without dependency installation or documented prerequisites.

Conclusion

The proposal must preserve upload and browser display, expose the remaining-seat calculation for inspection, and identify where the sample data and checks live. Expected results from the supplied rows are W1: `20 − 15 = 5` and W2: `12 − 12 = 0`.

Recommendation

Keep each runtime component tied to a required capability. Make the entry point, calculation, sample input, checks, and setup instructions easy to locate; do not treat file count or dependency count as the goal.

Do you find this helpful?

### Compare with a Streamlit proposal[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Compare-with-a-Streamlit-proposal)

A suitable stack is Python with Streamlit for local browser interaction, `csv` for reading the upload, and `unittest` for focused checks. Streamlit is a justified dependency because it supplies the requested browser workflow through a familiar interface approach.

A compact repository could contain:

- `README.md`: Prerequisites, dependency installation, launch command, and check command.
- `requirements.txt`: Declares the chosen Streamlit dependency version.
- `app.py`: Browser entry point, upload handling, CSV reading, and table display.
- `capacity.py`: Defines a function that returns each workshop’s remaining seats from its capacity and booked values.
- `samples/workshops.csv`: Contains W1 and W2.
- `tests/test_capacity.py`: Checks expected remaining seats of 5 and 0.
- `tests/test_upload.py`: Checks the upload-to-calculation boundary using the sample content.

After the documented environment and dependency setup, `python -m streamlit run app.py` launches the interface. Trace the workflow:

1. The coordinator uploads the CSV.
2. `app.py` reads records and passes numeric capacity and booked values to the calculation function.
3. It displays each workshop with the returned result.

The rejected additions lack required jobs:

- **Database:** No retained-state obligation
- **Worker:** No background task
- **Containers and separate JavaScript frontend:** Additional learning and setup without satisfying an otherwise missing requirement

Other justified layouts are acceptable if the browser workflow and calculation remain traceable.

A command-only solution would calculate 5 and 0 correctly while still omitting the required interaction. That is the decisive stack test: Can every required step survive the proposed simplification?

For your own brief:

- Attach an obligation to every runtime component.
- Identify the entry point, core decision, sample input, output destination, and checks.

Once that path is clear, inspect the actual input: Which assumptions about its cleanliness survive contact with the records?

Scoping the MVP

Working with Messy Data

Ask

[Justifying each component](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Justifying-each-component)

[Choosing a minimal stack](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Choosing-a-minimal-stack)

[Structuring one inspectable process](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Structuring-one-inspectable-process)

[Making the repository navigable](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Making-the-repository-navigable)

[When to add tools](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#When-to-add-tools)

[Practice: The workshop app](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Practice-The-workshop-app)

[Compare with a Streamlit proposal](https://www.educative.io/courses/forward-deployed-engineer/choosing-a-stack-and-project-structure#Compare-with-a-Streamlit-proposal)