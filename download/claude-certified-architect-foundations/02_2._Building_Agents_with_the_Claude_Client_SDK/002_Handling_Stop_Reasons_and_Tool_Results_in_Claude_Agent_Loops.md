# Handling_Stop_Reasons_and_Tool_Results_in_Claude_Agent_Loops

Source: https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Stop Reasons and Tool Results

Explore how to extend Claude client SDK agent loops to handle all stop reasons and integrate tools that can succeed or fail. Understand how to manage tool results in message arrays, debug state issues, and ensure stable AI agent responses without hallucination or silent failures.

We'll cover the following...

- [The two cases we left unhandled](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#The-two-cases-we-left-unhandled)
- [Adding a tool that can fail](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Adding-a-tool-that-can-fail)
- [What error results look like in the messages array](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#What-error-results-look-like-in-the-messages-array)
- [Dispatch function, updated](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Dispatch-function-updated)
- [Running both paths](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Running-both-paths)
- [What breaks when the state is inaccurate](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#What-breaks-when-the-state-is-inaccurate)
- [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Complete-code)
- [Exercise: Trace the broken loop](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Exercise-Trace-the-broken-loop)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Whats-next)

In the previous lesson, we built a loop that handles the happy path: Claude calls a tool, we return the result, and Claude answers. That loop handled two stop reasons correctly but left two unhandled: `"max_tokens"` and `"stop_sequence"`. It also assumed the tool would always succeed.

In this lesson, we extend the loop to handle all four stop reasons, introduce a tool that can fail, and trace what actually changes in the messages array when errors are returned. Then we break the loop on purpose to see what inaccurate state management looks like. By the end of this lesson, we will have:

- A loop that branches correctly on all four stop reasons
- A mock tool that returns both success and structured error responses
- A comparison of the messages array when tool results carry errors vs. successes
- A concrete demonstration of what breaks when tool results are appended with the wrong role

## The two cases we left unhandled[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#The-two-cases-we-left-unhandled)

The loop from the previous lesson only acted on `"tool_use"` and `"end_turn"`. The other two stop reasons were silently ignored, meaning the loop would fall off the end of the while block without returning anything. That is a silent failure: the function returns `None`, and the caller gets no signal about what went wrong.

Before adding error-returning tools, we need to close these two branches. Here’s the full four-branch skeleton that replaces the loop body:

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

while True:

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=1024,

system=SYSTEM,

tools=TOOLS,

messages=messages

)

if response.stop\_reason == "end\_turn":

for block in response.content:

if block.type == "text":

return block.text

return ""

if response.stop\_reason == "tool\_use":

messages.append({"role": "assistant", "content": response.content})

tool\_results = []

for block in response.content:

if block.type == "tool\_use":

result = dispatch\_tool(block.name, block.input)

tool\_results.append({

"type": "tool\_result",

"tool\_use\_id": block.id,

"content": result

})

messages.append({"role": "user", "content": tool\_results})

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The four-branch loop body. Each stop reason has an explicit action. No branch falls through silently.

- **Lines 1–8:** The API call is unchanged from the previous lesson. The model, token limit, system prompt, tools list, and messages array are all sent on every iteration.
- **Lines 10–14:** `"end_turn"` finds the text block and returns it. If no text block is present (uncommon but possible when Claude ends a turn after only a tool call), we return an empty string rather than `None`.
- **Lines 16–27:** `"tool_use"` appends the assistant turn, dispatches each tool, collects results, appends them as a `user` turn, and calls `continue` to start the next iteration. The `continue` is explicit here to make the control flow readable.
- **Lines 29–32:** `"max_tokens"` raises an error. A truncated response is not a valid output. Raising here means the caller can catch the exception, log it, and retry with a larger budget or escalate to a human. Silent pass-through would send incomplete data downstream.
- **Lines 34–38:** `"stop_sequence"` extracts the text and returns it. In structured output pipelines, the stop sequence marks the clean boundary of the output. The content up to that point is intentional and complete.

## Adding a tool that can fail[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Adding-a-tool-that-can-fail)

Real tools fail: a database is unavailable, an order ID does not exist, an API returns a `500` error. The agent loop must be able to receive and process those failures, not just successes. A tool that can only return success is not a usable tool in production.

We will add two tools: the order status tool from the previous lesson and a new `cancel_order` tool that can fail:

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

TOOLS = [

{

"name": "get\_order\_status",

"description": (

"Look up the current status of a customer order by its ID. "

"Use this when the customer asks about an order, shipment, or delivery."

),

"input\_schema": {

"type": "object",

"properties": {

"order\_id": {"type": "string", "description": "The order ID to look up"}

},

"required": ["order\_id"]

}

},

{

"name": "cancel\_order",

"description": (

"Cancel an order that has not yet shipped. "

"Use this only when the customer explicitly requests cancellation."

),

"input\_schema": {

"type": "object",

"properties": {

"order\_id": {"type": "string", "description": "The order ID to cancel"}

},

"required": ["order\_id"]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Two tool definitions. cancel\_order will return a structured error for orders that cannot be cancelled, giving Claude enough information to explain the outcome to the user.

- **Lines 2–16:** `get_order_status` is carried over from the previous lesson. Its definition is unchanged.
- **Lines 17–30:** `cancel_order` is new. The description constrains when Claude should call it: only on explicit customer requests or only for unshipped orders. These constraints are informational for Claude, not enforced in code. The tool implementation itself is the enforcement boundary.

Now the mock implementations:

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

def get\_order\_status(order\_id: str) -> str:

mock\_orders = {

"5678": "Shipped — expected delivery June 14.",

"9999": "Processing — not yet dispatched.",

}

return mock\_orders.get(order\_id, f"Order {order\_id} not found.")

def cancel\_order(order\_id: str) -> str:

cancellable = {"9999"}

already\_shipped = {"5678"}

if order\_id in cancellable:

return f"Order {order\_id} has been successfully cancelled."

if order\_id in already\_shipped:

return (

f"ERROR: Order {order\_id} cannot be cancelled. "

"It has already shipped. "

"The customer may request a return after delivery."

)

return f"ERROR: Order {order\_id} not found. Cannot cancel."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Mock implementations for both tools. cancel\_order returns a plain string in all cases, but the string content signals success or failure. Claude reads this string and decides how to respond.

- **Lines 1–6:** `get_order_status` is unchanged from the previous lesson.
- **Lines 9–10:** We use sets for fast membership checks. `cancellable` is the set of orders that can be canceled; `already_shipped` is the set that cannot.
- **Lines 12–14:** If the order is cancellable, we return a success string. Claude will read this and confirm cancellation to the user.
- **Lines 15–19:** If the order has already shipped, we return an error string with explicit context: what failed, why, and what the customer can do instead. This is structured error design: the tool gives Claude enough information to compose a helpful response without hallucinating a resolution.
- **Lines 20–21:** If the order is not found, we return a distinct error string. Claude can report that the order does not exist rather than guessing.

## What error results look like in the messages array[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#What-error-results-look-like-in-the-messages-array)

The tool result format is the same whether the content is a success or an error; it is always a plain string in the `content` field. What differs is what Claude does with that string. Here is the messages array after a failed cancellation attempt:

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

messages = [

{

"role": "user",

"content": "Please cancel my order #5678."

},

{

"role": "assistant",

"content": [

{"type": "text", "text": "I'll attempt to cancel that order now."},

{

"type": "tool\_use",

"id": "toolu\_01ABC",

"name": "cancel\_order",

"input": {"order\_id": "5678"}

}

]

},

{

"role": "user",

"content": [

{

"type": "tool\_result",

"tool\_use\_id": "toolu\_01ABC",

"content": "ERROR: Order 5678 cannot be cancelled. It has already shipped. The customer may request a return after delivery."

}

]

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The messages array after an error result. The tool result is structurally identical to a success result, the difference is in the string content that Claude reads.

- **Lines 1–4:** These lines show Turn 1, which contains the user’s cancellation request as one message with one text block.
- **Lines 5–16:** These lines show Turn 2: Claude’s response. The assistant turn contains both a narration text block (“I’ll attempt to cancel…”) and the `tool_use` block with `id: "toolu_01ABC"`. Both blocks are preserved exactly as received from the API.
- **Lines 17–28:** These lines indicate Turn 3: the tool result. The `tool_use_id` matches the `id` from turn 2 exactly. The `content` is the error string from `cancel_order`. Claude will read this string on the next iteration and decide how to respond to the user. In this case, it will explain that the order has shipped and describe the return option.
- The structure of this turn is identical to a successful result. The loop code does not need to inspect whether the result is an error; that is Claude’s job.

## Dispatch function, updated[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Dispatch-function-updated)

The dispatch function needs one new branch for the second tool:

Ace Editor

1

2

3

4

5

6

def dispatch\_tool(name: str, input\_args: dict) -> str:

if name == "get\_order\_status":

return get\_order\_status(\*\*input\_args)

if name == "cancel\_order":

return cancel\_order(\*\*input\_args)

return f"Unknown tool: {name}"

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Updated dispatcher with a branch for each tool. Unknown tool names return an informative error string.

- **Lines 1–2:** `dispatch_tool` still receives the tool name and a dict of inputs from the `tool_use` block.
- **Lines 3–4:** `get_order_status` branch, unchanged from the previous lesson.
- **Lines 5–6:** `cancel_order` branch. The `**input_args` unpacking works the same way: `{"order_id": "5678"}` becomes `cancel_order(order_id="5678")`.
- **Line 7:** The unknown-tool fallback. Returning a string here means Claude gets an error message it can reason about rather than the loop crashing.

## Running both paths[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Running-both-paths)

Let’s run two tasks side by side to observe both the success path and the error path:

Ace Editor

1

2

3

4

5

6

7

8

SYSTEM = "You are a customer support agent. Help customers with order inquiries and cancellations."

if \_\_name\_\_ == "\_\_main\_\_":

print("--- Success path ---")

print(run\_agent("Please cancel my order #9999."))

print("\n--- Error path ---")

print(run\_agent("Please cancel my order #5678."))

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Two runs: one cancellable order and one that has already shipped. Both complete without exceptions, the loop handles the error through Claude, not through the code.

- **Lines 1:** The system prompt is updated to include cancellations.
- **Lines 3–5:** The first run requests cancellation of order 9999, which is in the `cancellable` set. Claude will call `cancel_order`, receive a success string, and confirm to the user.
- **Lines 7–8:** The second run requests cancellation of order 5678, which is in `already_shipped`. Claude will call `cancel_order`, receive the error string, and compose a response explaining the situation and describing the return option.

**Expected output:**

Ace Editor

1

2

3

4

5

--- Success path ---

Your order #9999 has been successfully cancelled. If you have any other questions, feel free to ask.

--- Error path ---

I'm sorry, but order #5678 cannot be cancelled because it has already shipped. You should receive it by June 14. Once it arrives, you're welcome to request a return.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Claude reads the error string and synthesizes a coherent, helpful response. The loop code never inspected the error string, Claude handled the semantic interpretation.

Notice that Claude did not echo the raw error string. It read the error content and produced a natural-language explanation. This is by design: the tool returns a machine-readable description of what happened, and Claude converts it into a customer-appropriate reply.

## What breaks when the state is inaccurate[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#What-breaks-when-the-state-is-inaccurate)

The loop works because the messages array is accurate: every turn is appended in the correct order, with the correct roles, and no content is stripped. Let’s break one of those assumptions deliberately to see the failure mode.

**Scenario:** After receiving `stop_reason: "tool_use"`, the developer appends only the tool result and skips appending the assistant turn first.

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

# Broken loop — missing the assistant turn append

if response.stop\_reason == "tool\_use":

# BUG: assistant turn not appended here

tool\_results = []

for block in response.content:

if block.type == "tool\_use":

result = dispatch\_tool(block.name, block.input)

tool\_results.append({

"type": "tool\_result",

"tool\_use\_id": block.id,

"content": result

})

messages.append({"role": "user", "content": tool\_results})

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A broken loop: the assistant turn is not appended before the tool result. Claude receives a tool result with no corresponding tool\_use block in the conversation history.

- **Lines 3–4:** The comment marks where the missing append would go. The variable `response.content` is never added to the messages array.
- **Lines 5–13:** The tool result is built and appended correctly—the format is right, and the `tool_use_id` matches. But the messages array now has a `tool_result` block that references an ID Claude has no record of requesting.
- **Line 14:** Claude receives a conversation where the user has sent a tool result for a tool call that does not exist anywhere in the history. From Claude’s perspective, the result arrived out of nowhere.

The result is unpredictable: Claude may attempt to re-request the tool, may produce a confused clarifying response, or may hallucinate a continuation that ignores the tool result entirely. The exact behavior depends on context, but none of the outcomes are correct. The conversation record is broken because the state is inaccurate.

The comparison below shows what the messages array looks like in the correct and broken cases:

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

# Correct messages array after one tool cycle

[

{"role": "user", "content": "Cancel order #9999."},

{"role": "assistant", "content": [tool\_use\_block, text\_block]}, # present

{"role": "user", "content": [tool\_result\_block]},

]

# Broken messages array — assistant turn missing

[

{"role": "user", "content": "Cancel order #9999."},

# missing

{"role": "user", "content": [tool\_result\_block]},

]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The correct messages array vs. the broken one. The broken array has two consecutive user turns, the tool result has no assistant turn to anchor it.

- **Lines 2–5:** In the correct case, the messages array has alternating roles: user, assistant, user. Claude can trace the tool result back to the `tool_use` block by ID.
- **Lines 8–10:** In the broken case, two consecutive `user` turns appear. The tool result is a floating message with no anchor. The `tool_use_id` references an ID that does not exist in any prior assistant turn.

This is the most common loop bug the exam tests: the developer handles the tool call correctly, but forgets to append the assistant turn before appending the tool result. The fix is always the same: append `{"role": "assistant", "content": response.content}` before building the tool results list.

## Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Complete-code)

We bring all four `stop_reason` branches, both tool implementations, and the two demonstration runs from this lesson into one file. Running it, we exercise both the success path (a cancellable order) and the error path (an already-shipped order). You can watch Claude read the tool’s error string and compose a different response for each case without any conditional logic in the loop code.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import anthropic

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

"properties": {

"order_id": {"type": "string", "description": "The order ID to look up"}

},

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

"properties": {

"order_id": {"type": "string", "description": "The order ID to cancel"}

},

"required": ["order_id"]

}

}

]

def get_order_status(order_id: str) -> str:

mock_orders = {

"5678": "Shipped, expected delivery June 14.",

"9999": "Processing, not yet dispatched.",

}

return mock_orders.get(order_id, f"Order {order_id} not found.")

def cancel_order(order_id: str) -> str:

cancellable     = {"9999"}

already_shipped = {"5678"}

if order_id in cancellable:

return f"Order {order_id} has been successfully cancelled."

if order_id in already_shipped:

return (

f"ERROR: Order {order_id} cannot be cancelled. "

"It has already shipped. "

"The customer may request a return after delivery."

)

return f"ERROR: Order {order_id} not found. Cannot cancel."

def dispatch_tool(name: str, input_args: dict) -> str:

if name == "get_order_status":

return get_order_status(**input_args)

if name == "cancel_order":

return cancel_order(**input_args)

return f"Unknown tool: {name}"

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = anthropic.Anthropic(api_key=anthropic_api_key)

def run_agent(task: str) -> str:

messages = [{"role": "user", "content": task}]

while True:

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=1024,

system=SYSTEM,

tools=TOOLS,

messages=messages

)

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

result = dispatch_tool(block.name, block.input)

tool_results.append({

"type": "tool_result",

"tool_use_id": block.id,

"content": result

})

messages.append({"role": "user", "content": tool_results})

continue

if response.stop_reason == "max_tokens":

raise RuntimeError(

f"Response truncated after {response.usage.output_tokens} tokens. "

"Increase max_tokens or shorten the task."

)

if response.stop_reason == "stop_sequence":

for block in response.content:

if block.type == "text":

return block.text

return ""

if __name__ == "__main__":

print("--- Success path ---")

print(run_agent("Please cancel my order #9999."))

print("\n--- Error path ---")

print(run_agent("Please cancel my order #5678."))
```

⋯

The extended loop with all four stop reason branches and two tools

The script runs two tasks in sequence.

- The success path calls `cancel_order` with order `9999` and receives a success string.
- The error path calls it with order `5678` and receives an error string.

The loop code is identical for both runs; only the content of the tool result string changes.

**Expected output:**

Ace Editor

1

2

3

4

5

--- Success path ---

Your order #9999 has been successfully cancelled. If you have any other questions, feel free to ask.

--- Error path ---

I'm sorry, but order #5678 cannot be cancelled because it has already shipped. You should receive it by June 14. Once it arrives, you're welcome to request a return.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Exact phrasing varies across runs; the key observation is that Claude generates different responses for the success and error strings without the loop ever inspecting either.

The loop code never reads the content of the tool result. Claude does. The two different responses are entirely Claude’s work; the loop only handles structure (appending turns, building `tool_result` blocks, and routing on `stop_reason`).

## Exercise: Trace the broken loop[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Exercise-Trace-the-broken-loop)

Read the scenario and answer the questions below.

A developer builds a billing inquiry agent with two tools: `get_balance` and `get_recent_charges`. During testing, they notice that when the agent calls both tools in the same turn (a multi-tool response), the second API call always produces a confused response that re-requests one of the tools. The developer’s tool dispatch code correctly calls both functions and returns both results. The system prompt and tool definitions are correct.

Technical Quiz

1.

The developer’s loop appends each tool result as a separate `user` message instead of collecting all results into a single `user` turn with a list. Which problem does this cause?

A.

The API rejects requests with multiple consecutive `user` messages and returns a 400 error.

B.

There is no problem; appending tool results as separate messages is the documented approach

C.

Each separate `user` message resets Claude’s context, so the second tool result is processed without knowledge of the first.

D.

Tool results split across separate turns may not be correlated correctly with the multi-tool request.

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Whats-next)

The loop now handles all four stop reasons and processes both success and error tool results. What it still lacks is observability: when something goes wrong, there is no way to see what the messages array looked like at the point of failure. In the next lesson, we add lightweight logging to the loop so every API call, every stop reason, and every tool dispatch is visible in the terminal during a run.

Building the Agent Loop: Client SDK from Scratch

Debugging the Agent Transcript

Ask

[The two cases we left unhandled](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#The-two-cases-we-left-unhandled)

[Adding a tool that can fail](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Adding-a-tool-that-can-fail)

[What error results look like in the messages array](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#What-error-results-look-like-in-the-messages-array)

[Dispatch function, updated](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Dispatch-function-updated)

[Running both paths](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Running-both-paths)

[What breaks when the state is inaccurate](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#What-breaks-when-the-state-is-inaccurate)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Complete-code)

[Exercise: Trace the broken loop](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Exercise-Trace-the-broken-loop)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/stop-reasons-and-tool-results#Whats-next)