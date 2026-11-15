# When_to_Use_the_Claude_Agent_SDK_for_AI_System_Design

Source: https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# When to Reach for the Claude Agent SDK

Explore how to decide between the Claude Agent SDK and the Messages API for building AI workflows. Understand the SDK's built-in agent loop, tools, permissions, hooks, and session management, and learn how these features help manage complex, multi-step tasks with control and auditability. This lesson equips you to evaluate architectural choices based on workflow complexity, operational responsibilities, and customer ownership for AI system design.

We'll cover the following...

- [What the Agent SDK packages](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#What-the-Agent-SDK-packages)
- [Choosing between them in an answer](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Choosing-between-them-in-an-answer)
- [Running an agent with query()](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Running-an-agent-with-query)
- [Keeping a session with ClaudeSDKClient](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Keeping-a-session-with-ClaudeSDKClient)
- [Permissions and hooks as control](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Permissions-and-hooks-as-control)
- [Choosing the SDK for the right reasons](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Choosing-the-SDK-for-the-right-reasons)

An important architectural decision when building Claude-powered applications is whether to use the Messages API directly or the Claude Agent SDK. In a technical interview, you may be asked to evaluate both approaches for a customer workflow. The decision requires more than choosing an API. You need to explain the capabilities, implementation effort, operational responsibilities, and ongoing costs associated with each approach.

A well-supported recommendation identifies the capabilities provided by the SDK, explains how they fit the workflow, and addresses deployment, permissions, monitoring, and operational ownership. The following examples continue the expense audit scenario, where an agent reviews employee expense reports against company policy and determines the appropriate next step within its authorized scope.

## What the Agent SDK packages[#](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#What-the-Agent-SDK-packages)

The **Claude Agent SDK** is Anthropic’s library for building agents with the same agent loop, tools, and context management that power Claude Code. With the Messages API, our code writes the loop that sends requests, runs tools, and returns results. With the SDK, that loop comes built in, along with the pieces an agent usually needs around it.

The SDK packages several capabilities that we would otherwise write ourselves.

- **Agent loop:** The SDK sends requests, runs tool calls, and feeds results back until the task ends or hits a limit.
- **Built-in tools:** File reading and editing, shell commands, search, and web access, which we can turn off when an agent does not need them.
- **Custom tools:** Our own Python functions, exposed to Claude through an in-process server.
- **Permissions:** Rules that decide which tools run automatically and which ones are denied.
- **Hooks:** Our own functions that run at named points in the loop, such as before a tool runs.
- **Sessions, sub-agents, and skills:** Conversation memory across turns, specialized agents for parts of a task, and packaged instructions Claude loads when a task matches them.

The table below compares the two options on the points interviewers care about:

|  |  |  |
| --- | --- | --- |
| **Aspect** | **Raw Messages API** | **Claude Agent SDK** |
| Agent loop | Our code writes and maintains it | The SDK runs it |
| Tool execution | Our code calls each function and builds every tool\_result | The SDK runs tools and returns results to Claude |
| Control points | Any line of our own code | Permission modes, allowed tools, and hooks at named events |
| Runtime footprint | A lightweight HTTP client library | A Python package that runs a bundled Claude Code CLI process |

Knowing what the SDK contains is the first half of the answer. The second half is knowing when that package is worth its weight.

## Choosing between them in an answer[#](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Choosing-between-them-in-an-answer)

The raw Messages API fits work with a fixed shape. A single classification call, a document extraction step, or a short tool loop with two lookups all stay small and predictable. Tight latency or cost budgets also favor the raw API because we control every request.

The SDK fits work where Claude needs to take several steps on its own. Multi-step tasks over files or many tools, workflows that need hooks to enforce rules, and assistants that hold a session across turns all benefit from the SDK’s built-in loop and controls.

The best interview answers tie the choice to what happens after handoff. The customer’s team will own whatever we build. A raw API loop is code they can read line by line, while the SDK brings a larger runtime and its own release cycle to track. A sample answer for the expense workflow sounds like this:

For a straightforward policy check, I'd use the Messages API directly. The workflow needs only two lookups, and a small, explicit tool loop would be easy for the finance team's engineers to inspect and maintain. If the workflow expands to multiple tool calls, conditional approval steps, and human review, I'd consider the Agent SDK to reduce the orchestration code we'd need to maintain. The SDK handles the agent loop, while a `PreToolUse` hook can check approval requests before execution. I'd also enforce the approval limit in the backend and log each decision for audit.

That answer rests on two SDK skills: running an agent and controlling what it can do. We start with running one.

## Running an agent with `query()`[#](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Running-an-agent-with-query)

The `query()` function runs one task from start to finish. It takes a prompt and an options object and returns a stream of messages as the agent works. An `AssistantMessage` carries Claude’s text and tool calls, and a final `ResultMessage` carries the outcome, the number of turns, and the total cost.

Custom tools are ordinary Python functions. The `@tool` decorator defines each one with a name, a description, and its input types. The `create_sdk_mcp_server` function groups those tools into an in-process server that runs inside our application.

**Custom tool names:**

The SDK names each custom tool with the pattern `mcp__<server>__<tool>`. A `get_expense_report` tool on an `expenses` server becomes `mcp__expenses__get_expense_report`, and permission rules and hooks refer to that full name.

Let’s build a read-only version of the expense agent that checks three reports against their policy limits:

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
import asyncio

import json

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, ToolUseBlock, create_sdk_mcp_server, query, tool

# In-memory data stands in for the company's expense and policy systems.

REPORTS = {

"EXP-2001": {"employee": "Dana Ruiz", "category": "meals", "amount_usd": 68.40},

"EXP-2002": {"employee": "Sam Okafor", "category": "lodging", "amount_usd": 412.00},

"EXP-2003": {"employee": "Lee Chen", "category": "airfare", "amount_usd": 2380.00},

}

POLICY_LIMITS_USD = {"meals": 75.00, "lodging": 350.00, "airfare": 2500.00}

def as_result(data, is_error=False):

"""Wrap a Python value as a tool result."""

return {"content": [{"type": "text", "text": json.dumps(data)}], "is_error": is_error}

@tool("get_expense_report", "Look up one expense report by its ID.", {"report_id": str})

async def get_expense_report(args):

if args["report_id"] not in REPORTS:

return as_result(f"No expense report with ID {args['report_id']}.", is_error=True)

return as_result(REPORTS[args["report_id"]])

@tool("get_policy_limit", "Look up the per-expense limit in US dollars for one category.", {"category": str})

async def get_policy_limit(args):

if args["category"] not in POLICY_LIMITS_USD:

return as_result(f"No policy limit for category {args['category']}.", is_error=True)

return as_result({"category": args["category"], "limit_usd": POLICY_LIMITS_USD[args["category"]]})

TOOLS = [get_expense_report, get_policy_limit]

expense_server = create_sdk_mcp_server(name="expenses", version="1.0.0", tools=TOOLS)

options = ClaudeAgentOptions(

model="claude-sonnet-5-5",

system_prompt="You check expense reports against policy limits. End with one line per report: ID, within or over policy.",

env={"ANTHROPIC_API_KEY": "{{ANTHROPIC_API_KEY}}"},

mcp_servers={"expenses": expense_server},

tools=[],

allowed_tools=[f"mcp__expenses__{t.name}" for t in TOOLS],

permission_mode="dontAsk",

max_turns=10,

)

async def main():

async for message in query(prompt="Check reports EXP-2001, EXP-2002, and EXP-2003.", options=options):

if isinstance(message, AssistantMessage):

for block in message.content:

if isinstance(block, ToolUseBlock):

print("Tool call:", block.name.removeprefix("mcp__expenses__"), block.input)

elif isinstance(message, ResultMessage):

print("\n" + message.result)

print(f"\nTurns: {message.num_turns}, cost: ${message.total_cost_usd:.4f}")

asyncio.run(main())
```

⋯

Running a read-only expense audit agent with two custom tools through query()

- **Lines 7–12:** We created `REPORTS` and `POLICY_LIMITS_USD` to stand in for the company’s expense and policy systems.
- **Lines 15–17:** We wrote `as_result` to wrap any Python value in the result format the SDK expects, with an `is_error` flag for failures.
- **Lines 20–31:** We defined two tools with `@tool`. Each one returns an error result when it cannot find what Claude asked for.
- **Lines 34–35:** We grouped both tools into an in-process server named `expenses` with `create_sdk_mcp_server`.
- **Lines 37–46:** We configured the agent. `env` passes our API key, `tools=[]` turns off the built-in tools, `allowed_tools` approves our two tools, `permission_mode="dontAsk"` denies anything not approved, and `max_turns` caps the loop.
- **Lines 50–54:** We ran the task with `query()` and printed each tool call Claude made.
- **Lines 55–57:** We printed the final result, the number of turns, and the cost from the `ResultMessage`.

Here’s what one run printed:

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

Tool call: get\_expense\_report {'report\_id': 'EXP-2001'}

Tool call: get\_expense\_report {'report\_id': 'EXP-2002'}

Tool call: get\_expense\_report {'report\_id': 'EXP-2003'}

Tool call: get\_policy\_limit {'category': 'meals'}

Tool call: get\_policy\_limit {'category': 'lodging'}

Tool call: get\_policy\_limit {'category': 'airfare'}

I compared each report's amount to the policy limit for its category:

- EXP-2001 (meals): $68.40 against a $75 limit.

- EXP-2002 (lodging): $412 against a $350 limit, so $62 over.

- EXP-2003 (airfare): $2,380 against a $2,500 limit.

EXP-2001: within policy

EXP-2002: over policy

EXP-2003: within policy

Turns: 7, cost: $0.0098

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The SDK ran every tool call and returned every result without a loop of our own. The `ResultMessage` also reported the turn count and cost, which are the first numbers a customer asks about.

## Keeping a session with `ClaudeSDKClient`[#](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Keeping-a-session-with-ClaudeSDKClient)

The `query()` function suits a single task. When a user sends several messages to the same agent, `ClaudeSDKClient` keeps one session open so each new question builds on the earlier ones.

In the code below, we ask the agent about a hotel report and then ask a follow-up question that only makes sense with that context.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
import asyncio

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, TextBlock

options = ClaudeAgentOptions(

model="claude-sonnet-5-5",

system_prompt="You are an expense audit assistant for a finance team. Answer in one or two sentences.",

env={"ANTHROPIC_API_KEY": "{{ANTHROPIC_API_KEY}}"},

tools=[],

max_turns=3,

)

async def print_reply(client):

"""Print the text of the agent's reply to the latest question."""

async for message in client.receive_response():

if isinstance(message, AssistantMessage):

for block in message.content:

if isinstance(block, TextBlock):

print(block.text)

async def main():

async with ClaudeSDKClient(options=options) as client:

await client.query("A hotel report is $412 and the lodging limit is $350. Is it within policy?")

await print_reply(client)

# The session keeps the earlier turn, so this follow-up has context.

await client.query("Write a one-sentence note to the employee about what to do next.")

await print_reply(client)

asyncio.run(main())
```

⋯

Holding a two-turn conversation with an expense assistant through ClaudeSDKClient

- **Lines 5–11:** We configured an assistant with no tools and a short system prompt.
- **Lines 14–20:** We wrote `print_reply` to stream the agent’s reply to the latest question and print its text.
- **Line 24:** We opened a session with `ClaudeSDKClient`, which closes when the block ends.
- **Lines 25–26:** We asked the first question and printed the reply.
- **Lines 29–30:** We asked a follow-up in the same session and printed the reply.

The two replies below show the follow-up building on the first answer.

Ace Editor

1

2

3

No, $412 exceeds the $350 lodging limit by $62 (about 17.7% over). Unless there's an approved exception or the limit is per-night and this is a multi-night total, it would need to be flagged for pre-approval or a justification.

Your hotel expense of $412 exceeds the $350 lodging limit by $62, so please submit a written justification or any pre-approval documentation for the overage (or confirm whether the amount covers multiple nights) so we can finish processing your report.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The second question never mentions the amount or the limit, yet the note includes both. The session carried that context forward.

A running agent is useful, and an agent that can act needs limits. That’s where interviewers push hardest.

## Permissions and hooks as control[#](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Permissions-and-hooks-as-control)

A key question in agent design is: "How do you prevent an agent from performing unauthorized actions?" A system prompt can instruct Claude to follow specific rules, but those instructions alone cannot guarantee compliance. Permissions and hooks let developers enforce restrictions before tool execution, while backend authorization provides an additional layer of protection.

Permissions decide which tools may run at all. An explicit `allowed_tools` list with `permission_mode="dontAsk"` keeps the agent to exactly the tools we approved. A **hook** is a function the SDK calls at a named event in the agent loop. A `PreToolUse` hook runs before a tool executes, can inspect the tool’s input, and can deny the call with a reason that Claude reads.

Now we give the agent two actions, approve and flag, and add a hook that blocks approval of any report above $1,000. The policy limit for airfare is $2,500, so the EXP-2003 airfare report passes policy but still needs a person to approve it.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
import asyncio

import json

from claude_agent_sdk import ClaudeAgentOptions, HookMatcher, ResultMessage, create_sdk_mcp_server, query, tool

REPORTS = {

"EXP-2001": {"employee": "Dana Ruiz", "category": "meals", "amount_usd": 68.40},

"EXP-2002": {"employee": "Sam Okafor", "category": "lodging", "amount_usd": 412.00},

"EXP-2003": {"employee": "Lee Chen", "category": "airfare", "amount_usd": 2380.00},

}

POLICY_LIMITS_USD = {"meals": 75.00, "lodging": 350.00, "airfare": 2500.00}

APPROVAL_LIMIT_USD = 1000.00

DECISIONS = {}

def as_result(data, is_error=False):

"""Wrap a Python value as a tool result."""

return {"content": [{"type": "text", "text": json.dumps(data)}], "is_error": is_error}

@tool("get_expense_report", "Look up one expense report by its ID.", {"report_id": str})

async def get_expense_report(args):

if args["report_id"] not in REPORTS:

return as_result(f"No expense report with ID {args['report_id']}.", is_error=True)

return as_result(REPORTS[args["report_id"]])

@tool("get_policy_limit", "Look up the per-expense limit in US dollars for one category.", {"category": str})

async def get_policy_limit(args):

if args["category"] not in POLICY_LIMITS_USD:

return as_result(f"No policy limit for category {args['category']}.", is_error=True)

return as_result({"category": args["category"], "limit_usd": POLICY_LIMITS_USD[args["category"]]})

@tool("approve_report", "Approve an expense report that is within policy.", {"report_id": str})

async def approve_report(args):

DECISIONS[args["report_id"]] = "approved"

return as_result({"report_id": args["report_id"], "status": "approved"})

@tool("flag_report", "Send an expense report to a finance reviewer with the reason.", {"report_id": str, "reason": str})

async def flag_report(args):

DECISIONS[args["report_id"]] = f"flagged: {args['reason']}"

return as_result({"report_id": args["report_id"], "status": "flagged"})

async def require_human_approval(input_data, tool_use_id, context):

"""Deny approve_report for any report above the approval limit."""

report_id = input_data["tool_input"].get("report_id", "")

# Read the real amount from our records instead of trusting the model's arguments.

if report_id in REPORTS and REPORTS[report_id]["amount_usd"] > APPROVAL_LIMIT_USD:

print(f"Hook: blocked approve_report for {report_id}")

return {

"hookSpecificOutput": {

"hookEventName": input_data["hook_event_name"],

"permissionDecision": "deny",

"permissionDecisionReason": f"Reports over ${APPROVAL_LIMIT_USD:,.0f} need a human approver.",

}

}

print(f"Hook: allowed approve_report for {report_id}")

return {}

TOOLS = [get_expense_report, get_policy_limit, approve_report, flag_report]

expense_server = create_sdk_mcp_server(name="expenses", version="1.0.0", tools=TOOLS)

SYSTEM_PROMPT = """You audit expense reports for a finance team.

For each report, look it up, check it against its category's policy limit,

then approve it if it is within policy or flag it with the reason if it is not.

If an approval is blocked, flag the report with the reason you received."""

options = ClaudeAgentOptions(

model="claude-sonnet-5-5",

system_prompt=SYSTEM_PROMPT,

env={"ANTHROPIC_API_KEY": "{{ANTHROPIC_API_KEY}}"},

mcp_servers={"expenses": expense_server},

tools=[],

allowed_tools=[f"mcp__expenses__{t.name}" for t in TOOLS],

permission_mode="dontAsk",

hooks={"PreToolUse": [HookMatcher(matcher="mcp__expenses__approve_report", hooks=[require_human_approval])]},

max_turns=20,

)

async def main():

async for message in query(prompt="Audit reports EXP-2001, EXP-2002, and EXP-2003.", options=options):

if isinstance(message, ResultMessage):

print(f"\nTurns: {message.num_turns}, cost: ${message.total_cost_usd:.4f}")

print("Decisions:")

for report_id, decision in DECISIONS.items():

print(f"  {report_id}: {decision}")

asyncio.run(main())
```

⋯

Enforcing a $1,000 human-approval limit on an expense agent with a PreToolUse hook

- **Lines 12–13:** We set the human-approval limit at $1,000 and created `DECISIONS` to record what happens to each report.
- **Lines 35–44:** We added two action tools. `approve_report` records an approval, and `flag_report` records a referral with its reason.
- **Lines 47–61:** We wrote the `require_human_approval` hook. It looks up the report’s real amount in our own records and denies the call with a reason when the amount is over the limit.
- **Lines 67–70:** We told Claude to flag any report whose approval is blocked, using the reason it received.
- **Line 80:** We attached the hook to `PreToolUse` with a `HookMatcher`, so it runs only before `approve_report`.
- **Lines 86–91:** We ran the audit and printed the turn count, the cost, and every recorded decision.

The output below shows the hook allowing one approval and blocking another.

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

Hook: allowed approve\_report for EXP-2001

Hook: blocked approve\_report for EXP-2003

Turns: 11, cost: $0.0181

Decisions:

EXP-2001: approved

EXP-2002: flagged: Lodging expense of $412.00 exceeds the $350.00 policy limit by $62.00.

EXP-2003: flagged: Approval blocked: Reports over $1,000 need a human approver. Airfare of $2,380.00 is within the $2,500.00 policy limit.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Each report followed a different path. EXP-2001 passed policy, and the hook let it through. Claude flagged EXP-2002 itself because it broke policy. EXP-2003 passed policy, so Claude tried to approve it, and the hook stopped the call and handed back a reason Claude used to flag it.

The hook reads the amount from our own records instead of trusting Claude’s arguments. That detail matters in an interview because it shows the rule holds even if the model is confused or manipulated.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27621%27%20height=%27271%27/%3e)![ A PreToolUse hook decides before the tool runs](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 " A PreToolUse hook decides before the tool runs")

A PreToolUse hook decides before the tool runs

With the loop, the session, and the controls in view, the original interview question has a complete answer.

## Choosing the SDK for the right reasons[#](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Choosing-the-SDK-for-the-right-reasons)

The Agent SDK earns its place when Claude needs to take several steps, use many tools, and act under rules that the customer can audit. The raw Messages API stays the better fit for small, fixed workflows that a customer’s team can read end to end. A strong answer weighs that difference against the customer’s ownership after handoff, then shows how permissions and hooks keep the agent within its limits. Interviewers hear in that answer a candidate who chooses tools based on what the deployment needs.

Messages API and Tool Use Under Questioning

Defending a Sub-Agent Design

Ask

[What the Agent SDK packages](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#What-the-Agent-SDK-packages)

[Choosing between them in an answer](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Choosing-between-them-in-an-answer)

[Running an agent with query()](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Running-an-agent-with-query)

[Keeping a session with ClaudeSDKClient](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Keeping-a-session-with-ClaudeSDKClient)

[Permissions and hooks as control](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Permissions-and-hooks-as-control)

[Choosing the SDK for the right reasons](https://www.educative.io/courses/forward-deployed-engineer/when-to-reach-for-the-claude-agent-sdk#Choosing-the-SDK-for-the-right-reasons)