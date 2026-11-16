# Hooks_and_Automated_Behaviors_in_Claude_Code_Workflows

Source: https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Hooks and Automated Behaviors

Explore how to implement hooks in Claude Code to automate behaviors during different agent lifecycle events. Understand the five hook events, configure them with matchers and shell commands, and learn how PreToolUse hooks can block tool calls safely. Distinguish when to use hooks versus dispatch\_tool guards to manage tool interactions and enforce policies effectively.

We'll cover the following...

- [The five hook events](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-five-hook-events)
- [Hook configuration](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Hook-configuration)
- [How PreToolUse hooks receive data](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#How-PreToolUse-hooks-receive-data)
- [The exit code protocol](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-exit-code-protocol)
- [PostToolUse hooks: Logging and side effects](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#PostToolUse-hooks-Logging-and-side-effects)
- [The Stop hook: Session-end automation](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-Stop-hook-Session-end-automation)
- [Hooks vs. dispatch\_tool guards](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Hooks-vs-dispatchtool-guards)
- [Exercise: Choose the right mechanism](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Exercise-Choose-the-right-mechanism)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Whats-next)

A hook is a shell command that Claude Code runs in response to a specific event in the agent life cycle. Hooks are the right mechanism for behaviors that must happen every time an event fires, such as logging every file write, blocking specific shell patterns before Claude runs them, or notifying a Slack channel when Claude finishes a task. Like code-level guards in `dispatch_tool`, hooks operate deterministically. Unlike `dispatch_tool` guards, hooks are shell commands configured in settings files, not Python functions embedded in the agent code. By the end of this lesson, we will be able to:

- Name the five hook events and when each fires.
- Write a hook configuration entry in the settings file with a matcher and a command.
- Explain the exit code protocol for `PreToolUse` hooks and how it blocks tool calls.
- Distinguish the appropriate use cases for hooks vs. `dispatch_tool` guards.

## The five hook events[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-five-hook-events)

Each hook event fires at a distinct point in the Claude Code life cycle. Understanding which event fires when, and whether it can stop the action, is the foundation of hook design.

|  |  |
| --- | --- |
| **Event** | **When It Fires** |
| `PreToolUse` | Before any tool call executes |
| `PostToolUse` | After a tool call completes |
| `Stop` | When Claude finishes a turn (`end_turn` or `stop_sequence`) |
| `PreCompact` | Before Claude Code compresses the conversation history |

`PreToolUse` is the only event where a hook can prevent the action from occurring. For all other events, the hook runs after the fact and cannot reverse what happened.

## Hook configuration[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Hook-configuration)

Hooks are declared in the `hooks` object in any settings file. The structure nests by event name, then by a list of hook groups, each with a `matcher` and a list of commands:

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

{

"hooks": {

"PreToolUse": [

{

"matcher": "Bash",

"hooks": [

{

"type": "command",

"command": "python3 /project/.claude/hooks/validate\_bash.py"

}

]

}

],

"PostToolUse": [

{

"matcher": "Write",

"hooks": [

{

"type": "command",

"command": "bash /project/.claude/hooks/log\_file\_write.sh"

}

]

}

],

"Stop": [

{

"matcher": "",

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A settings file with three hooks: a PreToolUse validator for Bash calls, a PostToolUse logger for file writes, and a Stop notifier that fires at session end.

- **Top-level** `"hooks"` **key:** Contains an object whose keys are event names. Each event maps to a list of hook group objects.
- `"matcher": "Bash"`**:** Restricts the hook to fire only when the matched tool is called. For `PreToolUse` and `PostToolUse`, the matcher is the tool name. An empty string `""` matches all events (used for `Stop`, which has no tool context).
- `"hooks"` **inside the group:** A list of command objects. Each has `"type": "command"` and a `"command"` string that Claude Code runs in a shell subprocess.
- **Multiple hooks per event:** A single event can have multiple hook groups with different matchers. Each matching group runs its commands in order.

## How PreToolUse hooks receive data[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#How-PreToolUse-hooks-receive-data)

When a `PreToolUse` hook fires, Claude Code writes a JSON object to the hook process's stdin. The hook reads this to learn what tool is about to be called and with what arguments:

Ace Editor

1

2

3

4

5

6

7

{

"session\_id": "sess\_abc123",

"tool\_name": "Bash",

"tool\_input": {

"command": "rm -rf /tmp/build\_artifacts"

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A hook script reads this JSON, inspects the arguments, and exits with the appropriate code. Here is a Python hook that blocks any `rm -rf` command, regardless of path:

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

import json

import sys

data = json.load(sys.stdin)

command = data.get("tool\_input", {}).get("command", "")

if "rm -rf" in command:

print("BLOCKED: rm -rf commands are not permitted.", file=sys.stderr)

sys.exit(2)

sys.exit(0)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A PreToolUse hook that reads the Bash command from stdin JSON and exits with code 2 if it contains rm -rf. Claude Code reads the stderr message and surfaces it to Claude as the reason the call was blocked.

- `json.load(sys.stdin)`**:** Reads the JSON payload that Claude Code writes to stdin before running the hook. The `tool_input` field contains the arguments Claude intended to pass.
- `sys.exit(2)`**:** Exit code two is the block signal for `PreToolUse`. Claude Code cancels the tool call, reads the hook's stderr output, and injects it into Claude's context as the reason for the block. Claude then responds to the user, explaining that the action was not permitted.
- `sys.exit(0)`**:** Exit code zero means allow. The tool call proceeds normally.

## The exit code protocol[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-exit-code-protocol)

For `PreToolUse` hooks, the exit code has a precise meaning:

|  |  |  |
| --- | --- | --- |
| **Exit Code** | **Meaning** | **Claude Code Behavior** |
| `0` | Allow | The tool call proceeds normally |
| `2` | Block | Tool call is cancelled; hook's stderr is shown to Claude as the reason |
| Any other non-zero | Warning | Tool call still proceeds; Claude Code logs a warning |

Exit code two is the deliberate block. Any other nonzero exit (such as one) indicates a hook failure, not an intentional block. Claude Code treats it as an unexpected error and allows the tool call to proceed, rather than silently blocking everything when a hook crashes.

This distinction matters for reliability. If a hook script has a bug and exits with code one, the tool call is not silently blocked. The developer sees a warning, investigates the hook, and fixes it. An accidental block from a buggy hook is harder to diagnose than a warning log entry.

## PostToolUse hooks: Logging and side effects[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#PostToolUse-hooks-Logging-and-side-effects)

`PostToolUse` hooks run after the tool has completed and receive the tool input and output in the stdin JSON:

Ace Editor

1

2

3

4

5

6

{

"session\_id": "sess\_abc123",

"tool\_name": "Write",

"tool\_input": {"file\_path": "/src/api/orders.py", "content": "..."},

"tool\_response": "File written successfully"

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A logging hook that appends every file write to an audit log:

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

import json

import sys

from datetime import datetime

data = json.load(sys.stdin)

path = data.get("tool\_input", {}).get("file\_path", "unknown")

result = data.get("tool\_response", "")

ts = datetime.utcnow().isoformat()

with open("/var/log/claude\_writes.log", "a") as f:

f.write(f"{ts}\t{path}\t{result[:80]}\n")

sys.exit(0)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A PostToolUse logging hook. It reads the file path from tool\_input and the result from tool\_response, appends a timestamped line to an audit log, and exits 0. The tool has already completed; the exit code has no effect on the outcome.

- `tool_response`**:** The string returned by the tool function. For `Write`, this is Claude Code’s confirmation message. For `Bash`, it would be the command’s stdout.
- **Exit code in PostToolUse:** The exit code does not block or modify the tool result because the tool has already executed. Exit code zero is conventional. A nonzero exit produces a warning in Claude Code’s logs but does not affect the session.
- `result[:80]`**:** Truncating the result before writing prevents large tool outputs (for example, a long `Bash` stdout) from bloating the audit log.

## The Stop hook: Session-end automation[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-Stop-hook-Session-end-automation)

The `Stop` hook fires when Claude finishes a response turn. It has no tool context and receives a simpler payload:

Ace Editor

1

2

3

4

{

"session\_id": "sess\_abc123",

"stop\_reason": "end\_turn"

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A Slack notification hook that fires at session end:

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

import json

import os

import sys

import urllib.request

data = json.load(sys.stdin)

reason = data.get("stop\_reason", "unknown")

webhook = os.environ["SLACK\_WEBHOOK\_URL"]

payload = json.dumps({

"text": f"Claude Code session ended ({reason}). Review the transcript."

}).encode()

req = urllib.request.Request(

webhook,

data=payload,

headers={"Content-Type": "application/json"}

)

urllib.request.urlopen(req)

sys.exit(0)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A Stop hook that posts a Slack notification when Claude finishes a turn. SLACK\_WEBHOOK\_URL is read from the environment, not hardcoded. The hook uses the stdlib urllib to avoid any dependency on third-party packages.

- `stop_reason`**:** Can be `"end_turn"`, `"stop_sequence"`, `"max_tokens"`, or `"tool_use"` (if the session ended mid-tool-call). The hook can branch on this value to send different messages for different endings.
- **Environment variable for the webhook:** The webhook URL is a secret and belongs in the shell environment, not in the hook script or the settings file.
- `urllib.request`**:** Using the standard library avoids requiring `requests` or other packages in the hook environment. Hook scripts run in a plain shell subprocess without the project’s virtualenv activated by default.

## Hooks vs. dispatch\_tool guards[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Hooks-vs-dispatchtool-guards)

Both hooks and `dispatch_tool` guards can intercept tool calls before they execute. The correct choice depends on the context:

|  |  |  |
| --- | --- | --- |
| **Aspect** | **Hook (**`PreToolUse`**)** | `dispatch_tool` **guard** |
| Language | Any shell-executable language | Python (within the agent code) |
| Scope | All Claude Code tool calls, including built-in tools like `Bash` and `Write` | Only tools routed through your `dispatch_tool` function |
| Configuration | Settings file; no code changes needed | Requires modifying agent Python code |
| Session context access | Via stdin JSON (session\_id, tool name, arguments) | Full Python session object |
| Deployment | Works for Claude Code CLI and IDE extensions | Works only in custom agent loops |

The exam tests this distinction. Use hooks to intercept Claude Code's built-in tools (`Bash`, `Read`, `Write`, `Edit`) and to implement cross-cutting behaviors that apply to all tools. Use `dispatch_tool` guards for policy checks that require Python logic, access to application state, or enforcement in a custom agent loop that does not use Claude Code.

## Exercise: Choose the right mechanism[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Exercise-Choose-the-right-mechanism)

For each scenario, identify the correct hook event, exit code, or tool boundary. Apply the event timing rules and the hooks vs. guards distinction from this lesson.

Technical Quiz

1.

A team wants to ensure that every time Claude Code runs a `Bash` command, the command is logged to a file with a timestamp once the command has finished. No code changes to the agent loop are acceptable. What is the correct mechanism?

A.

Add a `dispatch_tool` wrapper that logs every Bash invocation before calling the shell

B.

A `PostToolUse` hook on `Bash` that reads the command from stdin and appends it to a log

C.

Add a `PreToolUse` hook that logs the command and exits 0

D.

Add a `UserPromptSubmit` hook that writes each Bash command to the log file

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Whats-next)

In the next lesson, we cover the permissions system in depth: how `allow` and `deny` patterns are matched, the precedence rules when both match the same tool call, and how to design a permission set that gives Claude enough access to be useful while blocking genuinely dangerous operations.

Claude Code Settings and Configuration Files

Permissions and Access Control

Ask

[The five hook events](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-five-hook-events)

[Hook configuration](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Hook-configuration)

[How PreToolUse hooks receive data](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#How-PreToolUse-hooks-receive-data)

[The exit code protocol](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-exit-code-protocol)

[PostToolUse hooks: Logging and side effects](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#PostToolUse-hooks-Logging-and-side-effects)

[The Stop hook: Session-end automation](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#The-Stop-hook-Session-end-automation)

[Hooks vs. dispatch\_tool guards](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Hooks-vs-dispatchtool-guards)

[Exercise: Choose the right mechanism](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Exercise-Choose-the-right-mechanism)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/hooks-and-automated-behaviors#Whats-next)