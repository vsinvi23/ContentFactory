# Understanding_Planning_Iteration_and_CI_Automation_with_Claude_Code

Source: https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Planning, Iteration, and CI Automation

Explore how to differentiate between direct execution and plan-first modes in Claude Code, understand when each approach helps prevent mistakes, and learn to set up non-interactive CI automation pipelines. This lesson equips you to apply architectural decisions, run automated reviews, and integrate Claude Code safely into production workflows.

We'll cover the following...

- [Direct execution vs. plan-first](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Direct-execution-vs-plan-first)
- [Using plan mode](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Using-plan-mode)
- [When plan-first prevents expensive mistakes](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#When-plan-first-prevents-expensive-mistakes)
- [Non-interactive execution with --print](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Non-interactive-execution-with---print)
- [Exit codes from --print](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Exit-codes-from---print)
- [A CI automation pipeline](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#A-CI-automation-pipeline)
- [Connecting plan mode to CI](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Connecting-plan-mode-to-CI)
- [Exercise: Choose the right approach](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Exercise-Choose-the-right-approach)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Whats-next)

Claude Code can either execute tasks directly or produce a plan first and wait for approval before making any changes. The choice between these modes is an architectural decision with real consequences: direct execution is fast, but irreversible changes happen immediately. Plan-first gives the developer a checkpoint to catch wrong assumptions before they become wrong files. This lesson covers both modes, when each is appropriate, and how to run Claude Code in automated pipelines without interactive sessions. By the end of this lesson, we will be able to:

- Explain the difference between direct execution and plan-first mode in Claude Code
- Identify the task types where plan-first mode prevents expensive mistakes
- Use `claude --print` to run Claude Code non-interactively and capture structured output
- Sketch a CI automation pipeline that uses a project command to produce reviewable output

## Direct execution vs. plan-first[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Direct-execution-vs-plan-first)

In the default interactive mode, Claude Code reads a task, decides what to do, and starts executing: reading files, writing code, and running shell commands. The developer sees each tool call as it happens and can deny individual steps. Plan-first mode changes this sequence. Claude Code produces a written plan describing what it intends to do and then stops. No files are changed. No commands are run. The developer reads the plan, requests changes if needed, and then approves execution. Only after approval does Claude Code begin making changes.

|  |  |  |
| --- | --- | --- |
| **Mode** | **When Changes Happen** | **Developer Checkpoint** |
| Direct execution | Immediately, as Claude decides each step | Per tool call (approve/deny) |
| Plan-first | Only after the developer approves the plan | Before any changes begin |

The per-tool-call checkpoint in direct execution is fine for small tasks where each step is obvious. For larger tasks involving many file changes, a database migration, or a refactor that touches interfaces used by multiple services, approving 50 individual tool calls is impractical. Plan-first mode gives a single checkpoint for the whole task.

## Using plan mode[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Using-plan-mode)

Plan mode is activated with the `/plan` slash command at the start of a session task. Claude Code reads the request, explores the relevant code, and produces a plan in structured prose before executing anything.

A developer asks Claude to refactor the order-processing service to use a new database client:

Ace Editor

1

2

3

/plan Refactor src/services/orders.py to use the new DatabaseClient from

src/db/client.py instead of the legacy db\_connection module. All existing

tests must still pass after the change.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Claude Code responds with a plan like:

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

Plan for order service refactor:

1. Read src/services/orders.py to identify all uses of db\_connection

2. Read src/db/client.py to understand the DatabaseClient interface

3. Read tests/test\_orders.py to understand what the tests exercise

4. Replace the import: `from legacy import db\_connection` → `from src.db.client import DatabaseClient`

5. Replace each db\_connection.execute() call with the DatabaseClient equivalent

6. Update the module-level initialization if db\_connection was initialized at import time

7. Run pytest tests/test\_orders.py to verify nothing broke

Estimated changes: 1 file modified (src/services/orders.py), 0 files created, 0 files deleted.

No schema changes. No migration required.

Proceed?

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The developer reads this, notices that step six mentions module-level initialization, wants to check that assumption, and replies, “Check step six first and update the plan if the initialization is more complex.” Claude revises before executing.

Without plan mode, Claude would have started writing changes to `orders.py` immediately, and the developer would discover the initialization complexity mid-execution, after some files were already modified.

## When plan-first prevents expensive mistakes[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#When-plan-first-prevents-expensive-mistakes)

Plan-first mode is valuable when the cost of a wrong assumption is high. The relevant factors are irreversibility, scope, and the presence of dependencies that the developer knows about but Claude may not.

- **Use plan-first when:**

  - The task modifies more than three to five files.
  - The task touches a file listed in `CLAUDE.md` as protected or requiring special handling.
  - The task involves database migrations, schema changes, or deployment configuration.
  - The task refactors a public interface used by code that Claude has not read yet.
  - The task deletes files or directories.
- **Direct execution is appropriate when:**

  - The task is a small, local change (fix a bug in one function, add a field to one struct).
  - The scope is fully visible in a single file that Claude has already read.
  - The change is trivially reversible with `git checkout`.
  - The developer wants fast iteration and will review the git diff before committing.

A useful heuristic: If explaining the task requires more than two sentences, a plan-first approach will likely surface at least one clarifying assumption worth checking before execution begins.

## Non-interactive execution with `--print`[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Non-interactive-execution-with---print)

Claude Code can run without an interactive session using the `--print` flag. The flag accepts a prompt string (or a slash command), executes it, writes the output to stdout, and exits. No session is maintained, and no user interaction is possible.

The basic form for running a project command non-interactively:

Ace Editor

1

claude --print "/review"

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

With a prompt string directly:

Ace Editor

1

claude --print "Summarize the changes in the current git diff in three bullet points."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Combining shell variables and piping to a file:

Ace Editor

1

2

3

BRANCH=$(git rev-parse --abbrev-ref HEAD)

claude --print "List all TODO comments added in commits on branch $BRANCH since main." \\

> todo\_report.txt

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The `--print` flag makes Claude Code composable in shell scripts. Standard Unix conventions apply: stdout carries the output, stderr carries warnings and diagnostic messages, and the exit code signals success or failure.

## Exit codes from `--print`[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Exit-codes-from---print)

When running non-interactively, Claude Code exits with codes that shell scripts and CI systems can act on:

|  |  |
| --- | --- |
| **Exit Code** | **Meaning** |
| `0` | Task completed normally |
| `1` | Claude Code itself encountered an error (API failure, authentication problem) |
| `2` | A `PreToolUse` hook blocked a tool call, and the task could not be completed |

Exit code 0 means Claude Code ran to completion; it does not mean the output is correct or that Claude found no problems. A review command that produces `{"summary": true, "errors": 5}` exits with code 0 because Claude Code itself succeeded. The calling script is responsible for reading the output and deciding whether the findings constitute a failure.

This is the same separation shown in the previous lesson’s `check_review.py` script: Claude Code produces findings, and the CI script applies policy.

## A CI automation pipeline[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#A-CI-automation-pipeline)

Combining project commands, `--print`, and a CI step produces a fully automated review pipeline. Here is the structure for a GitHub Actions workflow that runs the project review command on every pull request:

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

name: Claude Code Review

on:

pull\_request:

branches: [main]

jobs:

review:

runs-on: ubuntu-latest

steps:

- uses: actions/checkout@v4

- name: Set up Python

uses: actions/setup-python@v5

with:

python-version: "3.12"

- name: Install Claude Code

run: npm install -g @anthropic-ai/claude-code

- name: Run review command

env:

ANTHROPIC\_API\_KEY: ${{ secrets.ANTHROPIC\_API\_KEY }}

run: |

claude --print "/review" > review\_output.jsonl

- name: Check review output

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A GitHub Actions workflow that runs the project review command on every pull request targeting main. The ANTHROPIC\_API\_KEY is stored as a repository secret and injected into the environment.

- `actions/checkout@v4`**:** Checks out the PR branch so Claude Code has access to the current diff and the `.claude/commands/` directory.
- `npm install -g @anthropic-ai/claude-code`**:** Installs Claude Code in the CI runner. This is the standard installation path for CI environments that do not have Claude Code preinstalled.
- `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}`**:** The API key is stored as a GitHub Actions secret, not in the workflow file or the repository. Claude Code reads it from the environment at runtime.
- `claude --print "/review" > review_output.jsonl`**:** Runs the review command non-interactively and writes the output to a file. The workflow then runs the check script as a separate step so each step’s success or failure is independently visible in the CI log.
- `python ci/check_review.py < review_output.jsonl`**:** The check script (from the previous lesson) reads the review output from stdin and exits with code 1 if errors were found. A non-zero exit from this step marks the CI job as failed.

## Connecting plan mode to CI[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Connecting-plan-mode-to-CI)

Plan mode and `--print` serve opposite ends of the automation spectrum. Plan mode is for interactive, human-reviewed work where the developer wants a checkpoint before changes are made. `--print` is for automated, non-interactive work where no human is in the loop during execution.

The two can be combined in a staged workflow:

Ace Editor

1

2

3

4

5

6

1. Developer runs: claude "/plan Refactor the auth middleware per the new spec"

2. Claude Code produces a plan and stops.

3. Developer reviews the plan and approves or modifies it.

4. Developer approves execution: Claude Code makes the changes.

5. CI runs automatically: claude --print "/review" | python ci/check\_review.py

6. CI result is posted to the pull request.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Steps 1–4 use plan mode to catch wrong assumptions before changes. Steps 5–6 use automated review to catch errors after changes. The two mechanisms address different failure modes: plan mode catches “Claude misunderstood the task,” and CI review catches “Claude introduced a bug or style violation.”

## Exercise: Choose the right approach[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Exercise-Choose-the-right-approach)

For each scenario, decide between direct execution, plan-first mode, and `--print` automation. Apply the scope, reversibility, and interactivity criteria from this lesson.

Technical Quiz

1.

A developer asks Claude Code to add a single null-check to one function in `src/utils/formatter.py`. The function is four lines long, and the change is two lines. What mode is appropriate?

A.

Plan-first mode, because any code change could have unexpected consequences

B.

Plan-first mode only if the file is listed in `CLAUDE.md`

C.

`--print` mode, because the output should be reviewed before applying

D.

Direct execution, because the scope is small and fully visible in one function

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Whats-next)

In the next lesson, we close this chapter with an assessment quiz covering the full Claude Code configuration system, including settings hierarchy, hooks, permissions, commands, and CI automation through scenario-based questions.

Commands, Skills, and Reusable Workflows

Claude Code Configuration and Workflows Assessment Quiz

Ask

[Direct execution vs. plan-first](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Direct-execution-vs-plan-first)

[Using plan mode](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Using-plan-mode)

[When plan-first prevents expensive mistakes](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#When-plan-first-prevents-expensive-mistakes)

[Non-interactive execution with --print](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Non-interactive-execution-with---print)

[Exit codes from --print](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Exit-codes-from---print)

[A CI automation pipeline](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#A-CI-automation-pipeline)

[Connecting plan mode to CI](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Connecting-plan-mode-to-CI)

[Exercise: Choose the right approach](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Exercise-Choose-the-right-approach)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/planning-iteration-and-ci-automation#Whats-next)