# Debugging_Agent_Transcripts_Using_Structured_Logging

Source: https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Debugging the Agent Transcript

Explore how to implement structured logging within agent loops to capture API calls, stop reasons, tool actions, and results. Understand how to read agent transcripts and identify bugs such as missing assistant turns. This lesson equips you to diagnose and fix loop failures by analyzing detailed logs and message states, ensuring reliable AI system behavior.

We'll cover the following...

- [What to log and why](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#What-to-log-and-why)
- [The logging helper](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#The-logging-helper)
- [Instrumenting the loop](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Instrumenting-the-loop)
- [Reading a clean run](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Reading-a-clean-run)
- [Reading a failing run](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Reading-a-failing-run)
- [Printing the full messages array](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Printing-the-full-messages-array)
- [Catching the error instead of crashing](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Catching-the-error-instead-of-crashing)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Complete-code)
- [Exercise: Read the transcript](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Exercise-Read-the-transcript)
- [What's next?](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Whats-next)

The loop from the previous lessons works, but when it breaks, there is nothing to inspect. The messages array changes on every iteration, tool calls come and go, and errors surface only as wrong output or silent `None` returns. Without visibility into what happened between the first API call and the final answer, debugging is guesswork.

In this lesson, we instrument the loop with structured logging that prints state at each decision point. We then use that output to trace a failing run and identify the exact turn where it went wrong.

By the end of this lesson, we will have:

- A logging helper that formats message-array turns in human-readable form
- Turn-level log output for every API call, stop reason, tool call, and tool result
- A failing transcript annotated to show where and why it breaks
- A methodology for reading agent transcripts that applies to any loop

## What to log and why[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#What-to-log-and-why)

A loop produces four types of events worth capturing, each at a different moment in the iteration:

|  |  |  |
| --- | --- | --- |
| **Event** | **When It Fires** | **What to Capture** |
| API call | Before `client.messages.create()` | Turn count, message count, input token estimate |
| Stop reason | After the response arrives | `stop_reason`, response `id`, output token count |
| Tool dispatch | Before each tool function runs | Tool name, input arguments |
| Tool result | After each tool function returns | Tool name, result string (truncated if long) |

These four points cover the full life cycle of one iteration. Any failure in the loop, wrong stop reason handling, missing tool result, ID mismatch, or truncation will be visible in at least one of these log lines.

## The logging helper[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#The-logging-helper)

Rather than scattering `print()` calls throughout the loop, we write one helper that formats any event as a consistent, scannable line:

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

import json

def log(event: str, \*\*kwargs) -> None:

parts = [f"[{event}]"]

for key, value in kwargs.items():

if isinstance(value, (dict, list)):

parts.append(f"{key}={json.dumps(value, default=str)[:120]}")

else:

parts.append(f"{key}={value}")

print(" ".join(parts))

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A minimal logging helper. It formats an event name and key-value pairs into a single scannable line, truncating long values to keep output readable.

- **Line 1:** We import `json` to serialize dicts and lists inline.
- **Line 3:** `log` takes an event name and any number of keyword arguments. The caller decides what context to attach.
- **Lines 4–8:** We build a list of formatted parts. Dicts and lists are serialized with `json.dumps` and truncated to 120 characters; long tool results would otherwise flood the terminal. Scalar values (strings, ints) are formatted as-is.
- **Line 9:** We join all parts with two spaces and print. Two spaces make the key-value pairs easy to scan without a full table structure.

## Instrumenting the loop[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Instrumenting-the-loop)

With the helper in place, we add four log calls to the loop body:

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

def run\_agent(task: str) -> str:

messages = [{"role": "user", "content": task}]

turn = 0

while True:

turn += 1

log("api\_call", turn=turn, messages=len(messages))

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=1024,

system=SYSTEM,

tools=TOOLS,

messages=messages

)

log("stop\_reason",

turn=turn,

reason=response.stop\_reason,

response\_id=response.id,

output\_tokens=response.usage.output\_tokens

)

if response.stop\_reason == "end\_turn":

for block in response.content:

if block.type == "text":

return block.text

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The instrumented loop. Four log() calls bracket the main decision points. The turn counter makes each iteration traceable in the output.

- **Line 3:** We add a `turn` counter initialized to zero. It increments at the top of each iteration, so turn 1 is the first API call.
- **Line 7:** The `api_call` log fires before every API request. `messages=len(messages)` tells us how many turns are in the array at the time of the call.
- **Lines 16–21:** The `stop_reason` log fires immediately after the response arrives, before any branching. `response_id` and `output_tokens` are included because they are the most useful fields when correlating a log line to a specific API call in a debug session.
- **Line 33:** The `tool_call` log fires before each tool function runs. `block.input` is the dict Claude populated, and logging it here reveals any incorrect arguments before the function executes.
- **Line 35:** The `tool_result` log fires immediately after each tool function returns. Comparing `tool_call` and `tool_result` lines tells us whether the function received the right arguments and returned a usable result.
- **Lines 43–44:** The `error` log fires before raising. In production, this would also write to a structured log sink, not just the terminal.

## Reading a clean run[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Reading-a-clean-run)

Running the agent on the success path from the previous lesson produces output like this:

Ace Editor

1

2

3

4

5

6

[api\_call] turn=1 messages=1

[stop\_reason] turn=1 reason=tool\_use response\_id=msg\_01ABC output\_tokens=47

[tool\_call] name=cancel\_order input={"order\_id": "9999"}

[tool\_result] name=cancel\_order result=Order 9999 has been successfully cancelled.

[api\_call] turn=2 messages=3

[stop\_reason] turn=2 reason=end\_turn response\_id=msg\_01DEF output\_tokens=28

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Log output for the success path. Two iterations, one tool call, clean end\_turn on turn 2.

Reading this left to right, top to bottom:

- Turn 1 starts with one message in the array (the user task). The response is `tool_use`, with 47 output tokens.
- The loop calls `cancel_order` with `order_id: "9999"` and receives the success string.
- Turn 2 starts with three messages: the user task, the assistant tool\_use turn, and the user tool\_result turn. The response is `end_turn`, with 28 output tokens.

The message count at each `api_call` line is the fastest way to confirm that appends are happening correctly. Turn 1 starts with one message. After the tool cycle, turn 2 starts with three. If turn 2 started with two (only the task and one append instead of two), the assistant turn was not appended before the tool result, which is exactly the bug from the previous lesson.

## Reading a failing run[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Reading-a-failing-run)

Now let us look at a run where the messages array has the bug from the previous lesson: the assistant turn is missing before the tool result. It is tempting to assume Claude just gets confused by a malformed history and does something unexpected. In practice, the Messages API validates message structure before it ever runs inference: every `tool_result` block must reference a `tool_use_id` that appears in a `tool_use` block from the immediately preceding assistant turn. When that assistant turn is missing, the very next API call is rejected outright. The log output looks like this:

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

[api\_call] turn=1 messages=1

[stop\_reason] turn=1 reason=tool\_use response\_id=msg\_01ABC output\_tokens=47

[tool\_call] name=cancel\_order input={"order\_id": "9999"}

[tool\_result] name=cancel\_order result=Order 9999 has been successfully cancelled.

[api\_call] turn=2 messages=2

Traceback (most recent call last):

File "agent.py", line 19, in run\_agent

response = client.messages.create(

...

anthropic.BadRequestError: Error code: 400 - {'error': {'type': 'invalid\_request\_error',

'message': "messages.1.content.0: unexpected `tool\_use\_id` found in `tool\_result` blocks: toolu\_01ABC.

Each `tool\_result` block must have a corresponding `tool\_use` block in the previous message."}}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Log output from the broken loop. The message count at turn 2 is 2 instead of 3, and the next API call fails outright with a 400 error instead of producing another response.

The failure is visible on turn 2’s `api_call` line: `messages=2` when it should be `messages=3`. The developer appended the tool result but not the assistant turn, so the array has the user task and the tool result with no intermediate assistant turn. The API detects this immediately: the `tool_result` block’s `tool_use_id` does not match any `tool_use` block in the previous message, so the request is rejected before Claude ever sees it. The loop has no `try/except` around the API call, so the exception propagates up and crashes the process on turn 2.

The table below shows the correct and broken message arrays side by side at the start of turn two:

|  |  |
| --- | --- |
| **Correct (messages=3)** | **Broken (messages=2)** |
| Turn 1: user task | Turn 1: user task |
| Turn 2: assistant tool\_use | *(missing)* |
| Turn 3: user tool\_result | Turn 2: user tool\_result |

The `messages=` count in the `api_call` log line is a single number that reveals the entire problem, and it appears one log line before the API confirms it: a 400 `invalid_request_error` naming the exact `tool_use_id` it could not match.

## Printing the full messages array[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Printing-the-full-messages-array)

For complex failures, the message count is not enough. We need to see what is actually in the array. A `dump_messages` utility does this:

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

def dump\_messages(messages: list) -> None:

print(f"\n=== Messages array ({len(messages)} turns) ===")

for i, msg in enumerate(messages):

role = msg["role"]

content = msg["content"]

if isinstance(content, str):

print(f" [{i}] {role}: {content[:100]}")

elif isinstance(content, list):

for block in content:

btype = block.get("type") if isinstance(block, dict) else block.type

if btype == "text":

text = block.get("text") if isinstance(block, dict) else block.text

print(f" [{i}] {role}/text: {text[:100]}")

elif btype == "tool\_use":

name = block.get("name") if isinstance(block, dict) else block.name

print(f" [{i}] {role}/tool\_use: {name}")

elif btype == "tool\_result":

content\_val = block.get("content") if isinstance(block, dict) else block.content

print(f" [{i}] {role}/tool\_result: {str(content\_val)[:100]}")

print("=== End ===\n")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A messages array dump utility. It prints every turn with its role and a summarized view of its content blocks, making the array structure scannable at a glance.

- **Lines 1–2:** `dump_messages` takes the list and prints a header showing the total turn count.
- **Lines 3–4:** We enumerate to get the index `i` alongside each message. The index makes it easy to reference a specific turn when describing a bug.
- **Lines 5–7:** If the content is a plain string (the format used for user text messages built inline), we print it truncated to 100 characters.
- **Lines 8–20:** If the content is a list of blocks (the format used for assistant responses and tool results), we print each block’s type and a summary of its content. We check both dict and object access patterns because the API client can return either, depending on the SDK version and context.

Call `dump_messages(messages)` at the start of any failing iteration to see the full array state at that point:

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

if response.stop\_reason == "tool\_use":

messages.append({"role": "assistant", "content": response.content})

tool\_results = []

for block in response.content:

if block.type == "tool\_use":

log("tool\_call", name=block.name, input=block.input)

result = dispatch\_tool(block.name, block.input)

log("tool\_result", name=block.name, result=result)

tool\_results.append({

"type": "tool\_result",

"tool\_use\_id": block.id,

"content": result

})

messages.append({"role": "user", "content": tool\_results})

dump\_messages(messages) # remove after debugging

continue

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Adding dump\_messages to the tool\_use branch prints the full array state after each tool cycle. Remove the call before shipping.

- **Line 15:** The dump call goes after both appends and before `continue`, so it captures the array in its correct post-cycle state. In a correct loop, this should show three more turns than the last time the dump ran.

## Catching the error instead of crashing[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Catching-the-error-instead-of-crashing)

Because a missing assistant turn fails fast at the API boundary, wrapping the API call in a `try/except` turns a bare traceback into a diagnosable log line:

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

try:

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=1024,

system=SYSTEM,

tools=TOOLS,

messages=messages

)

except anthropic.BadRequestError as e:

log("error", reason="bad\_request", detail=str(e))

dump\_messages(messages)

raise

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Catching BadRequestError around the API call lets us log the error and dump the exact messages array that caused it before re-raising. The dump shows precisely which turn is missing.

Since the exception is raised by `client.messages.create()` itself, `dump_messages` here shows the array as it existed going into the failed call, before the request was rejected. In the broken loop, that dump has no `assistant` entry at all, only the original task and the tool result, one line of evidence confirming the missing append.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Complete-code)

We pull the logging helper, the `dump_messages` utility, and the fully instrumented loop from this lesson into one file. When you run it, you get a structured log for each turn, API call, stop reason, tool call, and tool result, followed by the final answer. This gives you a complete view of what happened between the first request and the last response.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import anthropic

import json

SYSTEM = "You are a customer support agent. Help customers with order inquiries and cancellations."

TOOLS = [

{

"name": "get_order_status",

"description": (

"Look up the current status of a customer order by its ID. "

"Use this when the customer asks about an order, shipment, or delivery."

),

"input_schema": {

"type": "object",

"properties": {"order_id": {"type": "string"}},

"required": ["order_id"]

}

},

{

"name": "cancel_order",

"description": (

"Cancel an order that has not yet shipped. "

"Use this only when the customer explicitly requests cancellation."

),

"input_schema": {

"type": "object",

"properties": {"order_id": {"type": "string"}},

"required": ["order_id"]

}

}

]

def get_order_status(order_id: str) -> str:

mock_orders = {"5678": "Shipped, expected delivery June 14.",

"9999": "Processing, not yet dispatched."}

return mock_orders.get(order_id, f"Order {order_id} not found.")

def cancel_order(order_id: str) -> str:

if order_id == "9999":

return f"Order {order_id} has been successfully cancelled."

if order_id == "5678":

return (f"ERROR: Order {order_id} cannot be cancelled. "

"It has already shipped. The customer may request a return after delivery.")

return f"ERROR: Order {order_id} not found. Cannot cancel."

def dispatch_tool(name: str, input_args: dict) -> str:

if name == "get_order_status":

return get_order_status(**input_args)

if name == "cancel_order":

return cancel_order(**input_args)

return f"Unknown tool: {name}"

def log(event: str, **kwargs) -> None:

parts = [f"[{event}]"]

for key, value in kwargs.items():

if isinstance(value, (dict, list)):

parts.append(f"{key}={json.dumps(value, default=str)[:120]}")

else:

parts.append(f"{key}={value}")

print("  ".join(parts))

def dump_messages(messages: list) -> None:

print(f"\n=== Messages array ({len(messages)} turns) ===")

for i, msg in enumerate(messages):

role    = msg["role"]

content = msg["content"]

if isinstance(content, str):

print(f"  [{i}] {role}: {content[:100]}")

elif isinstance(content, list):

for block in content:

btype = block.get("type") if isinstance(block, dict) else block.type

if btype == "text":

text = block.get("text") if isinstance(block, dict) else block.text

print(f"  [{i}] {role}/text: {text[:100]}")

elif btype == "tool_use":

name = block.get("name") if isinstance(block, dict) else block.name

print(f"  [{i}] {role}/tool_use: {name}")

elif btype == "tool_result":

cv = block.get("content") if isinstance(block, dict) else block.content

print(f"  [{i}] {role}/tool_result: {str(cv)[:100]}")

print("=== End ===\n")

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = anthropic.Anthropic(api_key=anthropic_api_key)

def run_agent(task: str) -> str:

messages = [{"role": "user", "content": task}]

turn = 0

while True:

turn += 1

log("api_call", turn=turn, messages=len(messages))

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=1024,

system=SYSTEM,

tools=TOOLS,

messages=messages

)

log("stop_reason", turn=turn, reason=response.stop_reason,

response_id=response.id, output_tokens=response.usage.output_tokens)

if response.stop_reason == "end_turn":

for block in response.content:

if block.type == "text":

return block.text

return ""

if response.stop_reason == "tool_use":

messages.append({"role": "assistant", "content": response.content})

tool_results = []

for block in response.content:

if block.type == "tool_use":

log("tool_call", name=block.name, input=block.input)

result = dispatch_tool(block.name, block.input)

log("tool_result", name=block.name, result=result)

tool_results.append({

"type": "tool_result",

"tool_use_id": block.id,

"content": result

})

messages.append({"role": "user", "content": tool_results})

continue

if response.stop_reason == "max_tokens":

log("error", reason="max_tokens", output_tokens=response.usage.output_tokens)

raise RuntimeError(f"Response truncated after {response.usage.output_tokens} tokens.")

if response.stop_reason == "stop_sequence":

for block in response.content:

if block.type == "text":

return block.text

return ""

if __name__ == "__main__":

print("=== Cancelling order #9999 (success path) ===")

answer = run_agent("Please cancel my order #9999.")

print(f"\nFinal answer: {answer}")

print("\n=== Cancelling order #5678 (error path) ===")

answer = run_agent("Please cancel my order #5678.")

print(f"\nFinal answer: {answer}")
```

⋯

The fully instrumented loop with four log events per iteration

Each run prints a log line before the API call, a line with the stop reason and token count after each response, and a line before and after each tool dispatch. Read the `messages=` count on every `[api_call]` line to verify that state management is correct across turns.

**Expected log structure:**

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

=== Cancelling order #9999 (success path) ===

[api\_call] turn=1 messages=1

[stop\_reason] turn=1 reason=tool\_use response\_id=msg\_01ABC output\_tokens=47

[tool\_call] name=cancel\_order input={"order\_id": "9999"}

[tool\_result] name=cancel\_order result=Order 9999 has been successfully cancelled.

[api\_call] turn=2 messages=3

[stop\_reason] turn=2 reason=end\_turn response\_id=msg\_01DEF output\_tokens=28

Final answer: Your order #9999 has been successfully cancelled. ...

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Response IDs and token counts differ across runs; the turn count and messages= count at each [api\_call] line are deterministic

Turn one starts with `messages=1` (the initial user task). After the tool cycle, turn two starts with `messages=3`: the user task, the appended assistant `tool_use` turn, and the appended user `tool_result` turn. A count of `messages=2` in turn two would immediately reveal the missing assistant turn bug from the lesson.

## Exercise: Read the transcript[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Exercise-Read-the-transcript)

The following log output was captured from an agent run. Read it and answer the questions below.

Ace Editor

1

2

3

4

5

6

[api\_call] turn=1 messages=1

[stop\_reason] turn=1 reason=tool\_use response\_id=msg\_01AAA output\_tokens=39

[tool\_call] name=get\_order\_status input={"order\_id": "7777"}

[tool\_result] name=get\_order\_status result=Order 7777 not found.

[api\_call] turn=2 messages=2

[error] reason=bad\_request detail=Error code: 400 - messages.1.content.0: unexpected `tool\_use\_id` found in `tool\_result` blocks: toolu\_01AAA. Each `tool\_result` block must have a corresponding `tool\_use` block in the previous message.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A failing transcript from an agent run. The second api\_call line is followed by a caught BadRequestError instead of a stop\_reason line.

Try each one before reading the answers.

Technical Quiz

1.

What does the `messages=2` count on turn 2 tell us about the loop’s state management?

A.

The assistant turn was skipped, so the array has 2 turns, not 3.

B.

The loop is correctly appending one message per iteration.

C.

The loop is resetting the messages array after each iteration.

D.

`messages=2` is the expected count on turn 2 for a single-tool agent

---

1 / 4

## What's next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Whats-next)

We now have a loop that handles all four stop reasons, processes both successful and error tool results, and produces a scannable log of every decision point. In the next lesson, we take all the mechanics from this chapter, including loop control, stop reasons, tool results, state management, and debugging, and test them in a scenario-based assessment quiz.

Stop Reasons and Tool Results

Agent Loop Assessment Quiz

Ask

[What to log and why](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#What-to-log-and-why)

[The logging helper](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#The-logging-helper)

[Instrumenting the loop](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Instrumenting-the-loop)

[Reading a clean run](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Reading-a-clean-run)

[Reading a failing run](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Reading-a-failing-run)

[Printing the full messages array](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Printing-the-full-messages-array)

[Catching the error instead of crashing](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Catching-the-error-instead-of-crashing)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Complete-code)

[Exercise: Read the transcript](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Exercise-Read-the-transcript)

[What's next?](https://www.educative.io/courses/claude-certified-architect-foundations/debugging-the-agent-transcript#Whats-next)