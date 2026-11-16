# Claude_Code_Permissions_and_Access_Control_for_Secure_AI_Workflows

Source: https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Permissions and Access Control

Explore how Claude Code enforces permissions and access control at the tool call level, independent of Claude's decisions. This lesson covers pattern syntax, precedence rules where deny overrides allow, and designing minimal permission sets following the principle of least privilege. Learn to apply permissions across multiple settings files to prevent unauthorized or risky operations while enabling safe, user-approved actions.

We'll cover the following...

- [Pattern syntax](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Pattern-syntax)
- [Precedence: Deny overrides allow](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Precedence-Deny-overrides-allow)
- [Unmatched tool calls: The prompt fallback](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Unmatched-tool-calls-The-prompt-fallback)
- [Designing a minimal permission set](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Designing-a-minimal-permission-set)
- [Layering permissions across settings files](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Layering-permissions-across-settings-files)
- [Exercise: Apply the rules](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Exercise-Apply-the-rules)
- [What's next?](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Whats-next)

The permissions system is how Claude Code enforces access control at the harness level, independent of what Claude decides. When a tool call matches a `deny` pattern, Claude Code cancels it regardless of Claude’s reasoning. When it matches an `allow` pattern, it proceeds without prompting the user. For everything else, Claude Code pauses and asks. This lesson covers the pattern syntax, precedence rules, and the practical design of a minimal permission set for a production project. By the end of this lesson, we will be able to:

- Write `allow` and `deny` patterns using the correct syntax for built-in tools.
- Explain the precedence rule when an `allow` and a `deny` pattern both match the same tool call.
- Identify what happens when a tool call matches neither `allow` nor `deny`.
- Design a permission set that follows the principle of least privilege.

## Pattern syntax[#](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Pattern-syntax)

Permission patterns use the form `ToolName(argument-pattern)`. The tool name matches one of Claude Code’s built-in tools. The argument pattern is a glob applied to the relevant argument of that tool call. The built-in tools and their matchable arguments are:

|  |  |  |
| --- | --- | --- |
| **Tool** | **Matched Argument** | **Example Pattern** |
| `Bash` | The shell command string | `Bash(git *)` |
| `Read` | The file path | `Read(src/**)` |
| `Write` | The file path | `Write(src/**)` |
| `Edit` | The file path | `Edit(src/**)` |
| `Glob` | The glob pattern argument | `Glob(**)` |
| `Grep` | The search pattern | `Grep(**)` |
| `WebFetch` | The URL | `WebFetch(https://docs.anthropic.com/*)` |
| `WebSearch` | The search query | `WebSearch(*)` |

Glob syntax follows standard conventions: `*` matches any sequence of characters within a path segment, `**` matches any path, including subdirectories, and `?` matches a single character.

A pattern with no argument, written as `ToolName(*)`, matches any call to that tool regardless of the argument:

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

{

"permissions": {

"allow": [

"Read(\*\*)",

"Bash(git \*)",

"Bash(npm run \*)",

"Bash(python -m pytest \*)",

"WebFetch(https://docs.anthropic.com/\*)"

],

"deny": [

"Bash(rm \*)",

"Bash(curl \*)",

"Bash(wget \*)",

"Bash(ssh \*)",

"Write(/etc/\*)",

"Write(~/\*)"

]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A permission set for a Python/Node project. The allow list pre-approves common development commands. The deny list blocks deletion, outbound network requests from the shell, and writes outside the project directory.

- `Read(**)`**:** Allows Claude to read any file. Reading is generally safe, and a blanket allow is common. This includes reading outside the project directory unless scoped further.
- `Bash(git *)`**:** Allows all Git subcommands. The `*` after `git`  matches any continuation, so `git status`, `git log`, `git diff`, and `git commit` are all allowed.
- `Bash(npm run *)`**:** Allows npm scripts, but not arbitrary npm commands. `npm install`, `npm publish`, and `npm uninstall` are not matched and will prompt the user.
- `Bash(rm *)`**:** Blocks `rm` entirely, including `rm -rf`, `rm -r`, and `rm filename`. Without this, Claude Code would prompt for each `rm` call rather than blocking it.
- `Write(/etc/*)` **and** `Write(~/*)`**:** Blocks writes to system configuration directories and the user’s home directory root. These are locations where an accidental write could affect the machine beyond the project.

## Precedence: Deny overrides allow[#](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Precedence-Deny-overrides-allow)

When a tool call matches both an `allow` pattern and a `deny` pattern, the `deny` pattern wins. There is no way to allow a tool call that a `deny` pattern matches. Consider this configuration:

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

{

"permissions": {

"allow": [

"Bash(\*)"

],

"deny": [

"Bash(rm \*)"

]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

`Bash(rm -rf /tmp/test)` matches both `Bash(*)` (allow) and `Bash(rm *)` (deny). The deny rule takes precedence, and the call is blocked.

This precedence direction is intentional. It means you can write a broad allow rule (`Bash(*)`) and carve out exceptions with deny rules, and the deny rules will always hold. The alternative, where allow overrides deny, would make the deny list ineffective whenever a broad allow pattern existed.

The exam tests this directly: if a question presents a configuration where both an allow and a deny match the same call, the answer is always that the call is blocked.

## Unmatched tool calls: The prompt fallback[#](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Unmatched-tool-calls-The-prompt-fallback)

When a tool call matches neither an `allow` nor a `deny` pattern, Claude Code pauses and prompts the user to approve or deny the specific call. The user can choose to allow it once, allow it for the session, or deny it.

This means an empty permissions object is not the same as blocking all tool calls. It means every tool call requires explicit user approval. Conversely, the absence of a `deny` entry for a tool does not mean that tool is silently allowed. It means the user will be asked.

The prompt fallback is the default for anything not explicitly configured. This is why production Claude Code configurations include a deliberate allow list. Without it, Claude Code interrupts the user for every tool call, including harmless ones like reading files and running tests.

## Designing a minimal permission set[#](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Designing-a-minimal-permission-set)

The principle of least privilege applied to Claude Code permissions is to allow the minimum set of operations that lets Claude complete its task and deny everything that could cause irreversible or wide-impact effects. Here’s a practical checklist for a new project permission set:

- **Allow:**

  - File reads across the project (`Read(**)`)
  - The project’s standard test, lint, and build commands
  - Git read operations (`git status`, `git log`, `git diff`)
  - Any MCP server tool calls the project uses
- **Deny:**

  - Recursive deletion (`Bash(rm *)` or, more specifically, `Bash(rm -rf *)`)
  - Outbound network access from the shell (`Bash(curl *)`, `Bash(wget *)`)
  - Remote access commands (`Bash(ssh *)`, `Bash(scp *)`)
  - Writes outside the project root
  - Package publishing or deployment commands (`Bash(npm publish *)`, `Bash(git push *)`)
- **Leave as prompt-required (neither allow nor deny):**

  - Git write operations (`git commit`, `git push`, `git branch`)
  - File deletions
  - Package installation
  - Any command that modifies persistent state that the developer should review

The third category is deliberate. Operations that are not dangerous enough to deny outright, but that the developer wants to see before they happen, belong in neither list. The user reviews and approves them one at a time during the session, building up familiarity with what Claude is doing before deciding to add them to the allow list.

## Layering permissions across settings files[#](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Layering-permissions-across-settings-files)

Claude Code reads permission rules from several settings files at once: your user file (`~/.claude/settings.json`), the project's shared `.claude/settings.json`, your personal `.claude/settings.local.json`, and any managed settings your organization deploys. It doesn't pick one file. It combines the allow and deny lists from all of them, and the deny-wins rule applies across files. The project files are read only from the directory where you start Claude Code, so a `.claude/settings.json` inside a subdirectory has no effect unless you start Claude Code there.

A team setup with a shared file, one developer's local overrides, and their user file:

Ace Editor

1

2

3

4

project/

.claude/settings.json ← shared: team allow and deny lists, committed

.claude/settings.local.json ← personal: one developer's extra rules, not committed

~/.claude/settings.json ← user: personal rules for every project

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The shared project file adds deny rules for sensitive payments operations. They apply to everyone who works in the repository, whatever their own files allow:

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

{

"permissions": {

"deny": [

"Bash(psql \*)",

"Bash(python manage.py migrate \*)",

"Write(services/payments/migrations/\*)"

]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A deny list in the shared project settings file. These rules combine with the rules in every developer's user and local files, and because deny always wins, no personal allow rule can override them.

- **Deny rules combine across files:** Claude Code merges the allow and deny lists from every settings file it loads. A deny rule in any file applies, and an allow rule in another file, even a personal local file, does not override it.
- **Migration write protection:** `Write(services/payments/migrations/*)` prevents Claude from creating migration files directly. The team convention requires running `make migration name=<name>` instead (defined in `CLAUDE.md`).

## Exercise: Apply the rules[#](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Exercise-Apply-the-rules)

For each scenario, apply the permission rules from this lesson to determine what Claude Code does. Focus on the precedence rule, the prompt fallback, and the distinction between blocking and requiring approval.

Technical Quiz

1.

A project has this permission configuration:

```
{

"permissions": {

"allow": ["Bash(*)", "Read(**)"],

"deny":  ["Bash(rm *)", "Bash(curl *)"]

}

}
```

Claude Code attempts to run `Bash` with command `curl https://api.example.com/data`. What happens?

A.

The call is blocked because `Bash(curl *)` is in the deny list and deny overrides allow

B.

The call is allowed because `Bash(*)` is in the allow list and it matches any Bash command

C.

The user is prompted because the call matches both allow and deny and Claude Code cannot decide

D.

The call is allowed only if the URL uses HTTPS

---

1 / 4

## What's next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Whats-next)

In the next lesson, we cover commands and skills: how to define reusable Claude Code workflows as slash commands in the settings, how to constrain what tools a skill may use, and how to build a CI-friendly automation that produces structured output that's reviewable outside the interactive session.

Hooks and Automated Behaviors

Commands, Skills, and Reusable Workflows

Ask

[Pattern syntax](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Pattern-syntax)

[Precedence: Deny overrides allow](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Precedence-Deny-overrides-allow)

[Unmatched tool calls: The prompt fallback](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Unmatched-tool-calls-The-prompt-fallback)

[Designing a minimal permission set](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Designing-a-minimal-permission-set)

[Layering permissions across settings files](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Layering-permissions-across-settings-files)

[Exercise: Apply the rules](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Exercise-Apply-the-rules)

[What's next?](https://www.educative.io/courses/claude-certified-architect-foundations/permissions-and-access-control#Whats-next)