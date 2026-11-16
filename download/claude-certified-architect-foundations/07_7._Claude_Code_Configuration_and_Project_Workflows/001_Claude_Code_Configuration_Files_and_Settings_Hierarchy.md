# Claude_Code_Configuration_Files_and_Settings_Hierarchy

Source: https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Claude Code Settings and Configuration Files

Explore the Claude Code configuration hierarchy, understanding the roles and precedence of settings files and how CLAUDE.md provides persistent project context. This lesson helps you master managing project versus user settings, permissions, and where to place configuration elements to ensure reliable AI system behavior.

We'll cover the following...

- [The configuration hierarchy](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#The-configuration-hierarchy)
- [The settings files](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#The-settings-files)
- [User-global vs. project settings](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#User-global-vs-project-settings)
- [CLAUDE.md: Persistent project context](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#CLAUDEmd-Persistent-project-context)
- [What belongs in CLAUDE.md vs. settings files](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#What-belongs-in-CLAUDEmd-vs-settings-files)
- [Exercise: Assign settings to the correct file](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#Exercise-Assign-settings-to-the-correct-file)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#Whats-next)

Claude Code reads configuration from multiple files in a defined priority order. Understanding which file governs which setting, and which level takes precedence when files conflict, is tested directly on the exam. This lesson maps the complete configuration hierarchy, explains the role of each file, and covers `CLAUDE.md` as the primary mechanism for supplying project context that persists across sessions. By the end of this lesson, we will be able to:

- Name the four configuration files in the hierarchy and their scope.
- Explain which settings scope (project vs. user) takes precedence for a given setting.
- Write a `CLAUDE.md` file that gives Claude persistent project context.
- Identify which settings belong in version-controlled files vs. local-only files.

## The configuration hierarchy[#](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#The-configuration-hierarchy)

Claude Code resolves settings by reading four files in a fixed order. Later files in the order override earlier ones for the same key:

|  |  |  |  |
| --- | --- | --- | --- |
| **File** | **Scope** | **Version Controlled?** | **Purpose** |
| `~/.claude/settings.json` | User-global | No | Default behaviors and permissions for all projects |
| `.claude/settings.json` | Project-shared | Yes | Team-wide project settings committed to the repository |
| `.claude/settings.local.json` | Project-local | No | Personal overrides for the current project (in `.gitignore`) |
| `CLAUDE.md` | Project context | Yes | Persistent instructions and project knowledge for Claude |

The resolution order means that `.claude/settings.local.json` can override anything in `.claude/settings.json`, which can override anything in `~/.claude/settings.json`. `CLAUDE.md` is not a settings file; it is injected into Claude's context as documentation rather than being merged with the settings objects.

## The settings files[#](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#The-settings-files)

Each settings file is a JSON object. The keys and their types are consistent across all three files; the scope determines whose preferences the file represents. A minimal project settings file configures permissions:

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

{

"permissions": {

"allow": [

"Bash(git:\*)",

"Bash(npm run \*)",

"Read(\*\*)"

],

"deny": [

"Bash(rm -rf \*)",

"Bash(curl \*)"

]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A project-level .claude/settings.json. The permissions block allowlists specific shell patterns and denylists destructive commands. This file is committed to the repository so every team member gets the same permissions.

- `permissions.allow`**:** A list of tool call patterns that are pre-approved and do not trigger a permission prompt. `"Bash(git:*)"` allows all Git subcommands. `"Bash(npm run *)"` allows all npm script invocations. `"Read(**)"` allows reading any file in the project.
- `permissions.deny`**:** A list of tool call patterns that are always blocked, regardless of what other allow rules exist. Deny rules take precedence over allow rules. `"Bash(rm -rf *)"` blocks recursive deletion. `"Bash(curl *)"` blocks outbound HTTP requests from the shell.
- **MCP servers:** They are not registered in settings files. A project shares its servers in `.mcp.json` at the repository root, and personal servers are stored in `~/.claude.json`. Settings files only control whether project servers are approved, through keys such as `enableAllProjectMcpServers`.

## User-global vs. project settings[#](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#User-global-vs-project-settings)

The user-global file (`~/.claude/settings.json`) sets defaults that apply across every project on the machine. The project files narrow or extend those defaults for a specific repository.

A typical user-global file covers personal preferences that should apply everywhere:

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

{

"theme": "dark",

"permissions": {

"allow": [

"Read(\*\*)",

"Bash(git status)",

"Bash(git log \*)",

"Bash(git diff \*)"

]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A project settings file that adds project-specific allowances without repeating the global ones:

Ace Editor

1

2

3

4

5

6

7

8

{

"permissions": {

"allow": [

"Bash(npm run \*)",

"Bash(python -m pytest \*)"

]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

In the merged result, Claude has permission to run all Git read commands (from the global file), all `npm run` scripts, and `pytest` (from the project file). Permission lists merge rather than replace: project-level `allow` entries are added to the global `allow` list, not substituted for it.

The local override file (`.claude/settings.local.json`) follows the same pattern but is personal to one developer and excluded from version control. Use it for:

- Personal permission rules for a local tool, such as a development database client.
- Temporarily expanding permissions for a debugging session.
- Overriding a team-wide setting that conflicts with a local tool.

## CLAUDE.md: Persistent project context[#](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#CLAUDEmd-Persistent-project-context)

`CLAUDE.md` is a Markdown file that Claude Code automatically injects into Claude's context at the start of every session. It is the primary mechanism for giving Claude persistent knowledge about the project without repeating it in every conversation. The file answers questions that Claude would otherwise need to ask or infer from the codebase:

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

# Project: Northshore Order Platform

## Architecture

- Backend: FastAPI (Python 3.12), PostgreSQL 15

- Frontend: Next.js 14 (TypeScript), deployed on Vercel

- API: REST, internal services use gRPC

- Message queue: RabbitMQ (orders.created, orders.updated topics)

## Development workflow

- All changes go through pull requests; direct pushes to main are blocked

- Run `make test` before creating a PR (runs pytest + mypy + ruff)

- Database migrations use Alembic: `alembic upgrade head` to apply

## Key conventions

- Service functions return Result objects (not raise exceptions)

- All external API calls go through `src/clients/`, never inline

- Feature flags are in `config/flags.py`; check there before adding new config

## Do not modify

- `src/legacy/billing\_v1.py`: frozen, do not touch without a separate RFC

- `migrations/`: do not write migration files manually, use `make migration name=<name>`

## Common commands

- Start dev server: `make dev`

- Run tests: `make test`

- Lint: `make lint`

- Generate types: `make generate`

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A CLAUDE.md for a production service. It covers architecture, workflow, conventions, protected files, and common commands. Claude reads this at the start of every session and can answer architecture questions, use the correct commands, and respect protected files without being told each time.

- **Architecture section:** Prevents Claude from guessing the stack or suggesting incompatible approaches. Claude knows the Python version, database, and frontend framework before it reads any code.
- **Development workflow section:** Ensures Claude runs `make test` before suggesting that a PR is ready. Without this, Claude might omit tests or use a different test invocation.
- **Key conventions section:** The Result object pattern and the `src/clients/` boundary prevent Claude from writing code that violates architectural invariants.
- **Do not modify section:** Explicitly protects frozen files. Claude reads this before touching any file and will not propose changes to the files listed here.
- **Common commands section:** Claude uses the correct project-specific commands rather than inferring them or defaulting to generic alternatives.

## What belongs in CLAUDE.md vs. settings files[#](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#What-belongs-in-CLAUDEmd-vs-settings-files)

`CLAUDE.md` and the settings files solve different problems:

|  |  |
| --- | --- |
| **Need** | **Where It Goes** |
| Persistent project knowledge (architecture, conventions) | `CLAUDE.md` |
| Reusable procedures run on demand (reviews, test generation, deploys) | `.claude/skills/<name>/SKILL.md` (personal skills go in `~/.claude/skills/`) |
| Permission rules (what tools Claude can run) | `.claude/settings.json` |
| MCP server registration | `.mcp.json` (shared with the team) or `~/.claude.json` (personal, added with `claude mcp add`) |
| Personal preferences (theme, default model) | `~/.claude/settings.json` |
| Temporary overrides (local dev db, debugging permissions) | `.claude/settings.local.json` |
| Secrets and API keys | Shell environment variables, referenced as `${VAR}` in `.mcp.json` |

Reusable procedures fit neither file. A procedure such as a code review or a release checklist is too specific to load into every session through `CLAUDE.md`, and it isn’t a setting. Package it as a skill in `.claude/skills/` and commit it, and every developer gets the same `/name` workflow. Unlike `CLAUDE.md`, a skill’s full instructions load only when it’s used. The Commands, Skills, and Reusable Workflows lesson covers skills in detail.

A common mistake is putting permissions in `CLAUDE.md` (“Please ask before running npm commands”) instead of in the settings file. `CLAUDE.md` is injected as text: Claude reads it and may follow the instruction, but it is a soft behavioral instruction, not an enforced rule. Permission rules in the settings file are enforced by the Claude Code harness, regardless of what Claude decides.

## Exercise: Assign settings to the correct file[#](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#Exercise-Assign-settings-to-the-correct-file)

For each item below, decide which file it belongs in.

Technical Quiz

1.

A team wants to allow all developers to run `make test` without a permission prompt. This should apply to everyone who clones the repository.

A.

`~/.claude/settings.json`

B.

`.claude/settings.json`

C.

`.claude/settings.local.json`

D.

`CLAUDE.md`

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#Whats-next)

In the next lesson, we cover hooks: event-driven shell commands that Claude Code runs automatically before and after tool calls, at session end, and at compaction. Hooks are the primary mechanism for enforcing automated behaviors that must run regardless of what Claude decides.

Prompting and Schema Assessment Quiz

Hooks and Automated Behaviors

Ask

[The configuration hierarchy](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#The-configuration-hierarchy)

[The settings files](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#The-settings-files)

[User-global vs. project settings](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#User-global-vs-project-settings)

[CLAUDE.md: Persistent project context](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#CLAUDEmd-Persistent-project-context)

[What belongs in CLAUDE.md vs. settings files](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#What-belongs-in-CLAUDEmd-vs-settings-files)

[Exercise: Assign settings to the correct file](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#Exercise-Assign-settings-to-the-correct-file)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/claude-code-settings-and-configuration-files#Whats-next)