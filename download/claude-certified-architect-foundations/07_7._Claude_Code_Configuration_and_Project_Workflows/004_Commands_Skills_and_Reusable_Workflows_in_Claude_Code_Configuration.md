# Commands_Skills_and_Reusable_Workflows_in_Claude_Code_Configuration

Source: https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Commands, Skills, and Reusable Workflows

Explore how to build reusable Claude Code workflows with commands and skills. Learn where they live, how arguments work, how skills are invoked by a developer or by Claude, how to control the tools a skill can use, and how to choose between CLAUDE.md, skills, hooks, and subagents. The lesson also covers commands that produce structured output for CI pipelines.

We'll cover the following...

- [Where commands live](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Where-commands-live)
- [Writing a command file](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Writing-a-command-file)
- [The $ARGUMENTS placeholder](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#The-ARGUMENTS-placeholder)
- [Structured output for CI pipelines](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Structured-output-for-CI-pipelines)
- [User commands for personal workflows](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#User-commands-for-personal-workflows)
- [Project vs. user commands: The decision rule](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Project-vs-user-commands-The-decision-rule)
- [From commands to skills](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#From-commands-to-skills)
- [Writing a skill](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Writing-a-skill)
- [Who can invoke a skill](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Who-can-invoke-a-skill)
- [Controlling tool use in a skill](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Controlling-tool-use-in-a-skill)
- [Choosing the right reusable mechanism](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Choosing-the-right-reusable-mechanism)
- [Putting it together: A reusable review workflow](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Putting-it-together-A-reusable-review-workflow)
  - [Sharing a workflow across repositories: Plugins](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Sharing-a-workflow-across-repositories-Plugins)
- [Exercise: Design the right command](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Exercise-Design-the-right-command)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Whats-next)

A Claude Code command is a Markdown file that Claude Code loads as a prompt template when a developer types its slash name in chat. Instead of pasting the same review instructions into every session, the team writes them once in a command file, commits it to the repository, and each developer invokes it the same way. This lesson starts with command files, then moves to skills, the newer format that commands have been merged into, and ends with how to choose the right reusable mechanism for a workflow. By the end of this lesson, we will be able to:

- Create a project command file and explain where it must be placed to be available to the team.
- Use the `$ARGUMENTS` placeholder to pass runtime input into a command prompt.
- Design a command that produces structured output for use outside the interactive session.
- Explain the difference between project commands and user commands.
- Write a skill with a `SKILL.md` file and control whether the developer, Claude, or both can invoke it.
- Explain what `allowed-tools` does and does not do.
- Choose between CLAUDE.md, a skill, a hook, and a subagent for a reusable workflow.

## Where commands live[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Where-commands-live)

Commands are Markdown files stored in specific directories. Their location determines who can invoke them:

|  |  |  |  |
| --- | --- | --- | --- |
| **Directory** | **Scope** | **Invoked As** | **Version Controlled?** |
| `.claude/commands/` | Project-shared | `/name` | Yes |
| `~/.claude/commands/` | User-global | `/name` | No |

A file at `.claude/commands/review.md` is invoked as `/review`. A file at `~/.claude/commands/summarize.md` is invoked as `/summarize`. Subdirectories are allowed and create namespaced commands: `.claude/commands/db/migrate.md` is invoked as `/db:migrate`.

The project commands directory is committed to the repository alongside `CLAUDE.md` and `.claude/settings.json`. Every developer who clones the repository gets the same commands without any personal setup.

## Writing a command file[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Writing-a-command-file)

A command file is a Markdown prompt. Claude Code reads the entire file content and sends it as the user turn when the command is invoked. The file can contain any instructions, context, or structure that a regular prompt can contain. Here is a code review command for a Python project:

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

Review the changes in the current git diff for the following:

1. Correctness: logic errors, off-by-one errors, incorrect conditionals

2. Safety: SQL injection, command injection, path traversal, unvalidated input

3. Style: violations of the project conventions in CLAUDE.md

4. Test coverage: functions added or changed without corresponding test changes

For each finding, output a JSON object on its own line:

{"file": "<path>", "line": <n>, "severity": "error|warning|suggestion", "message": "<one sentence>"}

After all findings, output a summary line:

{"summary": true, "errors": <n>, "warnings": <n>, "suggestions": <n>}

If there are no findings, output:

{"summary": true, "errors": 0, "warnings": 0, "suggestions": 0}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Saved at .claude/commands/review.md. Invoked with /review. Claude reads the current git diff and outputs one JSON object per finding plus a summary line. The output format is machine-readable so a CI script can parse it.

- **Numbered review criteria:** Explicit numbered steps reduce the chance that Claude skips a category. “Review the changes” with no structure produces inconsistent coverage across invocations.
- **JSON-per-line output format:** Each finding is a self-contained JSON object on its own line (newline-delimited JSON). A CI script can read stdout line by line and parse each line independently without accumulating the full output first.
- **Summary object:** The final line gives a count of each severity level. A CI step that fails on `errors > 0` only needs to parse the summary line, not every finding.
- **Reference to CLAUDE.md:** The command defers to `CLAUDE.md` for project conventions rather than repeating them in the command file. When conventions change, updating `CLAUDE.md` updates the review criteria automatically.

## The $ARGUMENTS placeholder[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#The-ARGUMENTS-placeholder)

When a command is invoked with text after the command name, Claude Code substitutes that text for every occurrence of `$ARGUMENTS` in the command file. This turns a static prompt into a parameterized template. Here is a test generation command that accepts a file path:

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

Generate pytest tests for the module at $ARGUMENTS.

Requirements:

- One test function per public function or method in the module

- Use `pytest.mark.parametrize` for functions with more than two distinct input shapes

- Mock all external calls (database, HTTP, filesystem) using `pytest.mock.patch`

- Each test must have a docstring that states what behavior it verifies

Write the tests to a file at `tests/test\_$ARGUMENTS` where `$ARGUMENTS` is the filename only,

not the full path. For example, if $ARGUMENTS is `src/billing/invoices.py`,

write to `tests/test\_invoices.py`.

Do not run the tests after writing them.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Saved at .claude/commands/gen-tests.md. Invoked as /gen-tests src/billing/invoices.py. $ARGUMENTS is replaced with src/billing/invoices.py everywhere it appears in the file.

- `$ARGUMENTS` **in the output path:** The second occurrence of `$ARGUMENTS` in the write-path instruction uses the same substitution. The clarifying example prevents Claude from writing to `tests/test_src/billing/invoices.py` (including the full path) instead of `tests/test_invoices.py`.
- **“Do not run the tests”:** An explicit boundary. Without this, Claude may attempt to run the tests after writing them, which could trigger a permission prompt or cause unexpected side effects if the module has dependencies that aren’t installed.
- **Invocation example:** `/gen-tests src/orders/fulfillment.py` → Claude generates tests for `src/orders/fulfillment.py` and writes them to `tests/test_fulfillment.py`.

If no text follows the command name, `$ARGUMENTS` resolves to an empty string. Command files that require an argument should state this explicitly in the prompt so Claude reports the missing argument rather than proceeding with an empty substitution.

## Structured output for CI pipelines[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Structured-output-for-CI-pipelines)

Commands that produce structured output can be used in automated pipelines without human review. Claude Code supports a `--print` flag that runs a command non-interactively and writes the output to stdout, making it composable with shell scripts.

Run the review command from a CI step:

Ace Editor

1

2

claude --print /review > review\_output.jsonl

python ci/check\_review.py review\_output.jsonl

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The `check_review.py` script reads the output and fails the CI step if any errors were found:

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

import json

import sys

findings = []

summary = None

for line in sys.stdin:

line = line.strip()

if not line:

continue

obj = json.loads(line)

if obj.get("summary"):

summary = obj

else:

findings.append(obj)

if summary is None:

print("ERROR: no summary line in review output", file=sys.stderr)

sys.exit(1)

for f in findings:

if f["severity"] == "error":

print(f"ERROR {f['file']}:{f['line']}: {f['message']}")

if summary["errors"] > 0:

print(f"\n{summary['errors']} error(s) found. CI failed.")

sys.exit(1)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A CI script that reads the newline-delimited JSON output from the review command. It exits with code 1 if any error-severity findings exist, and code 0 otherwise. The separation between parsing and policy (what counts as a failure) keeps the script simple.

- `sys.stdin` **reading:** The script reads from stdin so it can be composed in a pipeline: `claude --print /review | python ci/check_review.py`.
- `obj.get("summary")` **check:** The summary object is identified by its `"summary": true` field, not by its position in the output. This makes it robust if Claude outputs findings after the summary in some runs.
- **Exit code for CI:** Exiting with code 1 causes most CI systems (GitHub Actions, GitLab CI, Jenkins) to mark the step as failed. The calling pipeline decides whether to block the PR or only annotate it.

## User commands for personal workflows[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#User-commands-for-personal-workflows)

User-level commands in `~/.claude/commands/` work identically to project commands but apply across all projects on the machine. They are the right place for personal productivity workflows that are not team conventions.

Common user command use cases:

- A personal `summarize` command that produces a commit message from the current diff in the developer’s preferred style
- A `standup` command that summarizes what changed since the last commit and formats it as a daily standup update
- An `explain` command that reads a selected file and explains it at the level of detail the developer prefers
- A debugging `trace` command that adds structured logging to a selected function, following a personal convention

User commands are not committed to the repository. They travel with the developer across projects and machines (if `~/.claude/commands/` is managed in a dotfiles repository).

## Project vs. user commands: The decision rule[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Project-vs-user-commands-The-decision-rule)

The decision between project and user commands comes down to one question: Is this a team convention or a personal preference? The table below maps the relevant factors to the right choice.

|  |  |
| --- | --- |
| **Use Project Commands When** | **Use User Commands When** |
| The workflow is a team convention | The workflow is a personal preference |
| The output format must be consistent across contributors | The output format is for personal use only |
| New team members should have the command without setup | The command applies to work habits, not project structure |
| The command references project-specific paths or `CLAUDE.md` | The command is generic across projects |

The exam tests this distinction in the form of: “A team wants all developers to run the same pre-commit review. Where does this command belong?” The answer is `.claude/commands/` (project-shared, version-controlled).

## From commands to skills[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#From-commands-to-skills)

Claude Code has merged custom commands into skills. A command file and a skill both create a slash command and run the same way: `.claude/commands/review.md` and `.claude/skills/review/SKILL.md` each give you `/review`. Existing command files keep working, but skills are the recommended format for new work because they add three things a single command file can’t:

- A folder for supporting files, such as reference docs, examples, and scripts.
- Frontmatter that controls who can invoke the skill.
- Automatic loading: Claude can pick a skill on its own when the conversation matches the skill’s description.

A skill is a folder whose name becomes the command, with a `SKILL.md` file inside it. These are the main places a skill can live:

|  |  |  |
| --- | --- | --- |
| **Location** | **Path** | **Who Gets It** |
| Project | `.claude/skills/<name>/SKILL.md` | Everyone in the repository (commit it) |
| Personal | `~/.claude/skills/<name>/SKILL.md` | You, in every project on this machine |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Anyone with the plugin enabled, invoked as `/plugin-name:skill-name` |
| Enterprise | The managed settings directory | Everyone your organization deploys it to |

When two skills share a name, enterprise wins over personal, and personal wins over project. A skill also wins over a command file of the same name. Plugin skills are namespaced, so they never collide with local skills.

## Writing a skill[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Writing-a-skill)

Here is the review command from earlier, rewritten as a skill:

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

---

description: Reviews the current git diff for correctness, safety, style, and test coverage, and outputs one JSON object per finding. Use when the user asks for a code review or wants to check changes before committing.

argument-hint: [focus-area]

---

Review the changes in the current git diff. If a focus area is given, review only that area: $ARGUMENTS

Apply the review criteria in [criteria.md](criteria.md).

For each finding, output a JSON object on its own line:

{"file": "<path>", "line": <n>, "severity": "error|warning|suggestion", "message": "<one sentence>"}

After all findings, output a summary line:

{"summary": true, "errors": <n>, "warnings": <n>, "suggestions": <n>}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Saved at .claude/skills/review/SKILL.md. Invoked as /review, or loaded by Claude when a developer asks for a review. The detailed criteria live in criteria.md in the same folder.

- **`description`****:** Claude always sees each skill’s description, but loads the full body only when the skill is used. A good description says what the skill does and when to use it, with the main use case first. A vague description (“Helps with code”) means Claude rarely picks the skill on its own.
- **`argument-hint`****:** Shows a hint in the `/` menu. `$ARGUMENTS` works the same way as in command files.
- **Supporting files:** `criteria.md` loads only when Claude follows the link, so long reference material costs almost nothing until it’s needed. Keep `SKILL.md` short (the docs suggest under 500 lines). A `scripts/` folder holds code the skill runs rather than reads.

## Who can invoke a skill[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Who-can-invoke-a-skill)

By default, both the developer and Claude can invoke a skill. Two frontmatter fields change that:

|  |  |  |
| --- | --- | --- |
| **Setting** | **Who Can Invoke It** | **Use It For** |
| Default | Developer (`/name`) and Claude | Most workflows, such as reviews and test generation |
| `disable-model-invocation: true` | Only the developer | Workflows with side effects, such as `/deploy`, that should never start on their own |
| `user-invocable: false` | Only Claude | Background knowledge, such as a legacy-system guide, that isn’t an action anyone would type |

A developer runs a skill by putting `/name` at the start of a message. Claude loads a skill on its own when the conversation matches its description, unless `disable-model-invocation` is set.

## Controlling tool use in a skill[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Controlling-tool-use-in-a-skill)

Three frontmatter fields shape what a skill can do while it runs:

- **`allowed-tools`****:** Tools Claude can use without asking during the turn that invokes the skill, for example `allowed-tools: Bash(git add *) Bash(git commit *)`. It pre-approves; it does not restrict. Any tool not listed still follows your normal permission rules.
- **`disallowed-tools`****:** Tools removed entirely while the skill is active. Use it to stop a skill from, say, editing files.
- **`context: fork`****:** Runs the skill in a separate subagent with its own context. Use it for heavy work, such as a large codebase search, so only the result comes back to the main conversation.

**Exam trap:** `allowed-tools` doesn’t create an allowlist. To block a tool inside a skill, use `disallowed-tools` or a deny rule in settings.

## Choosing the right reusable mechanism[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Choosing-the-right-reusable-mechanism)

Each mechanism fits a different kind of reuse:

|  |  |  |
| --- | --- | --- |
| **Mechanism** | **When It Applies** | **Use It For** |
| `CLAUDE.md` | Loaded into every session | Conventions Claude should always follow, such as code style or the test command |
| Skill | On demand, by `/name` or when Claude matches the description | Repeatable procedures, such as reviews, test generation, or release notes |
| Skill with `context: fork`, or a subagent | On demand, in a separate context | Heavy or noisy work whose details shouldn’t fill the main conversation |
| Hook | Automatically, on an event such as `PostToolUse` | Steps that must run every time without relying on Claude, such as formatting or logging |
| Command file | Same as a skill | Existing workflows; prefer skills for new ones |

A rule of thumb:

- If Claude should always know it, use `CLAUDE.md`.
- If someone runs it as a procedure, make it a skill.
- If it must happen every time without exception, use a hook.

## Putting it together: A reusable review workflow[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Putting-it-together-A-reusable-review-workflow)

Real workflows combine several mechanisms. Here is how a team packages its pre-merge review so it runs the same way in every session and in CI:

Ace Editor

1

2

3

4

5

6

7

repo/

├── CLAUDE.md ← conventions every session follows

├── .mcp.json ← shared MCP servers, if the review needs any

└── .claude/

├── settings.json ← permissions and the formatting hook

├── skills/review/SKILL.md ← the /review procedure (plus criteria.md)

└── agents/security-reviewer.md ← a subagent for the security pass

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A repository that shares its review workflow. Every file is committed, so each developer and the CI runner get the same setup.

- `CLAUDE.md`**:** The conventions every review checks against, such as code style and the test command.
- `/review` **skill:** The procedure itself. Developers run it, Claude can pick it up when asked for a review, and CI runs the same skill with `claude --print "/review"`.
- **Hook:** A `PostToolUse` hook in `.claude/settings.json` runs the formatter after every edit, so formatting never depends on Claude remembering it.
- **Subagent:** The review skill hands the security pass to a subagent defined in `.claude/agents/`. It runs in its own context window with read-only tools, and only its findings come back to the main conversation.

A subagent is a Markdown file with YAML frontmatter. The body becomes its system prompt:

Ace Editor

1

2

3

4

5

6

7

---

name: security-reviewer

description: Reviews a diff for injection, authentication, and secrets issues. Use for the security pass of a code review.

tools: Read, Grep, Glob

---

You are a security reviewer. For each issue, report the file, line, severity, and a one-sentence explanation.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Saved at .claude/agents/security-reviewer.md. Only name and description are required. Claude uses the description to decide when to delegate. If tools is omitted, the subagent inherits every tool available to subagents.

### Sharing a workflow across repositories: Plugins[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Sharing-a-workflow-across-repositories-Plugins)

Committing these files shares the workflow with one repository. To reuse it across many repositories, package it as a plugin. A plugin is a folder that can bundle skills, subagents, hooks, and MCP servers, with an optional manifest at `.claude-plugin/plugin.json`. Teams install it from a marketplace with `/plugin`. Its components are namespaced under the plugin name, so the review skill runs as `/review-kit:review`.

Ace Editor

1

2

3

4

5

6

review-kit/

├── .claude-plugin/plugin.json ← name, version, description

├── skills/review/SKILL.md

├── agents/security-reviewer.md

├── hooks/hooks.json

└── .mcp.json

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The same workflow packaged as a plugin. Once a repository enables it, the skill runs as /review-kit:review.

**Exam tip:** Commit the files to `.claude/` to share a workflow with one repository; package it as a plugin to share it across many.

## Exercise: Design the right command[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Exercise-Design-the-right-command)

For each scenario, decide where the command file belongs, how it should handle arguments, and which CI integration pattern fits the requirement.

Technical Quiz

1.

A team wants every developer who types `/pr-description` to get a pull request description generated from the current branch’s commits compared to `main`. The description format must be consistent across all contributors. Where should this command file be saved, and how is it invoked?

A.

`~/.claude/commands/pr-description.md`, invoked as `/pr-description`

B.

`CLAUDE.md` with an instruction block for generating PR descriptions

C.

`.claude/commands/pr-description.md`, invoked as `/pr-description`

D.

`.claude/settings.json` as a `hooks.Stop` command that runs at session end

---

1 / 7

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Whats-next)

In the next lesson, we cover planning mode and CI automation: how Claude Code’s plan-first workflow separates intent from execution, and how to structure an automated review pipeline that produces output a CI system can act on without human interaction.

Permissions and Access Control

Planning, Iteration, and CI Automation

Ask

[Where commands live](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Where-commands-live)

[Writing a command file](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Writing-a-command-file)

[The $ARGUMENTS placeholder](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#The-ARGUMENTS-placeholder)

[Structured output for CI pipelines](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Structured-output-for-CI-pipelines)

[User commands for personal workflows](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#User-commands-for-personal-workflows)

[Project vs. user commands: The decision rule](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Project-vs-user-commands-The-decision-rule)

[From commands to skills](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#From-commands-to-skills)

[Writing a skill](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Writing-a-skill)

[Who can invoke a skill](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Who-can-invoke-a-skill)

[Controlling tool use in a skill](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Controlling-tool-use-in-a-skill)

[Choosing the right reusable mechanism](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Choosing-the-right-reusable-mechanism)

[Putting it together: A reusable review workflow](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Putting-it-together-A-reusable-review-workflow)

[Sharing a workflow across repositories: Plugins](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Sharing-a-workflow-across-repositories-Plugins)

[Exercise: Design the right command](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Exercise-Design-the-right-command)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/commands-skills-and-reusable-workflows#Whats-next)