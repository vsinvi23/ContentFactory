# Enforce_AI_System_Rules_Outside_the_Prompt_for_Reliability

Source: https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Guardrails Outside the Prompt

Explore how to enforce critical business rules in AI systems by moving constraints from prompts into programmatic checks. Learn to implement pre-execution input validation, post-execution result filtering, and confirmation flags for irreversible actions. This lesson helps you build reliable, deterministic guardrails in Claude-powered agent workflows to prevent costly mistakes and ensure compliance beyond prompt guidance.

We'll cover the following...

- [Why the system prompt is not enough](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Why-the-system-prompt-is-not-enough)
- [Pre-execution enforcement: Checking inputs before the tool runs](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Pre-execution-enforcement-Checking-inputs-before-the-tool-runs)
- [Post-execution enforcement: Filtering results before Claude reads them](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Post-execution-enforcement-Filtering-results-before-Claude-reads-them)
- [The confirmation flag pattern for irreversible actions](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#The-confirmation-flag-pattern-for-irreversible-actions)
- [When to use prompt guidance vs. programmatic enforcement](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#When-to-use-prompt-guidance-vs-programmatic-enforcement)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Complete-code)
- [Exercise: Choose the enforcement point](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Exercise-Choose-the-enforcement-point)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Whats-next)

Every agent we have built so far relies on Claude to follow instructions in the system prompt. That works well for guidance, tone, formatting, and tool preference, but it is the wrong mechanism for rules that must hold without exception. In this lesson, we move critical constraints out of the prompt and into the dispatch function, where enforcement is deterministic. By the end of this lesson, we will be able to:

- Explain why system prompt instructions are insufficient for critical business rules.
- Implement a pre-execution policy check that intercepts a tool call before it runs.
- Implement a post-execution check that filters or modifies a tool result before Claude reads it.
- Apply the confirmation-flag pattern for irreversible actions.

## Why the system prompt is not enough[#](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Why-the-system-prompt-is-not-enough)

Consider this system prompt line:

> “Never apply a discount greater than 20%. Discounts above 20% require manager approval.”

Claude will follow these instructions most of the time. But system prompt compliance is a probability, not a guarantee. Under unusual phrasing, adversarial inputs, or edge cases that the developer did not test, Claude may reason its way past the constraint. The model does not interpret instructions as hard rules; it weighs them against context and produces the most likely response. For a business rule like a discount cap, “most of the time” is not a standard we can ship. A single 35%-off transaction that bypasses the prompt instruction costs real money and can potentially violate a compliance policy.

The correct fix is to move enforcement out of the prompt and into code. The `dispatch_tool` function we built in the previous chapter is the natural enforcement point: every tool call passes through it before the underlying function runs. Add a policy check there so it executes every time, regardless of what Claude decides or what the user says.

## Pre-execution enforcement: Checking inputs before the tool runs[#](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Pre-execution-enforcement-Checking-inputs-before-the-tool-runs)

A pre-execution check intercepts the tool call arguments before the underlying function executes. If the arguments violate a policy, the check blocks the call and returns a structured error string to Claude instead of running the function. Claude reads that error and decides how to respond, typically by explaining to the user that the action is not permitted.

We will apply this to an `apply_discount` tool capped at 20%:

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

def apply\_discount(order\_id: str, rate: float) -> str:

if rate > 0.20:

return (

f"POLICY\_VIOLATION: Discount rate {rate:.0%} exceeds the 20% maximum. "

"Discounts above 20% require manager approval. "

"The discount was not applied."

)

new\_total = calculate\_discounted\_total(order\_id, rate)

return f"Discount of {rate:.0%} applied to order {order\_id}. New total: ${new\_total:.2f}."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The apply\_discount function enforces the cap before touching any order data. If the rate exceeds 20%, the function returns an error string without calling calculate\_discounted\_total.

- **Lines 1–6:** The first thing the function does is check the `rate` argument. If it is above 0.20, the function returns a structured error string. It does not reach the line that modifies order data. The cap is enforced regardless of what Claude put in the `input` dict.
- **Line 7:** Only if the check passes do we call the underlying calculation. The guard is upstream of any side effect.
- **Lines 8–9:** On success, we return a confirmation string. Claude reads this and confirms the discount to the user.
- This pattern differs from a check inside `dispatch_tool`. Placing the guard inside the function itself means it is enforced even if someone calls `apply_discount` directly from outside the agent loop, a belt-and-suspenders approach.

For cases where the check needs access to context that the function does not have (such as the calling user’s role or session state), the guard goes in the dispatcher:

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

def dispatch\_tool(name: str, input\_args: dict, user\_role: str = "agent") -> str:

if name == "apply\_discount":

rate = input\_args.get("rate", 0)

if rate > 0.20 and user\_role != "manager":

return (

f"POLICY\_VIOLATION: Discount rate {rate:.0%} exceeds 20%. "

"Manager approval required."

)

return apply\_discount(\*\*input\_args)

return f"Unknown tool: {name}"

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A dispatcher-level guard that also checks caller role. The check runs before apply\_discount is called, using context (user role) that the function itself would not have access to.

- **Line 1:** `dispatch_tool` now accepts a `user_role` parameter. In a production system, this would come from the session or request context, not from Claude’s input.
- **Lines 3–8:** The policy check runs before `apply_discount` is called. If the rate is above the cap and the caller is not a manager, the function returns a structured error. Claude reads the error and explains the situation to the user.
- **Line 9:** Only if the check passes does `apply_discount` execute.

## Post-execution enforcement: Filtering results before Claude reads them[#](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Post-execution-enforcement-Filtering-results-before-Claude-reads-them)

A post-execution check intercepts the tool result after the function runs, before Claude reads it. This is the right pattern when the concern is what information Claude should be allowed to see, not what action it should be allowed to take.

The most common use case is redacting sensitive fields from a data lookup result. Consider a `get_employee_record` tool that returns a full record, including salary and tax ID. Claude should be able to read the name, title, and department, but not the sensitive financial fields. Here is the post-execution check applied in the dispatcher:

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

SENSITIVE\_FIELDS = {"salary", "tax\_id", "bank\_account\_number"}

def dispatch\_tool(name: str, input\_args: dict) -> str:

if name == "get\_employee\_record":

raw\_result = get\_employee\_record(\*\*input\_args)

return redact\_sensitive\_fields(raw\_result, SENSITIVE\_FIELDS)

return f"Unknown tool: {name}"

def redact\_sensitive\_fields(record: dict, fields\_to\_redact: set) -> str:

redacted = {

key: "[REDACTED]" if key in fields\_to\_redact else value

for key, value in record.items()

}

return json.dumps(redacted)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A post-execution filter applied in the dispatcher. The tool function runs and returns the full record; the dispatcher redacts sensitive fields before converting the result to the string Claude will read.

- **Line 1:** `SENSITIVE_FIELDS` is a module-level constant, a single place to maintain the redaction list.
- **Lines 3–5:** The dispatcher calls `get_employee_record` and gets the full result, then immediately passes it through `redact_sensitive_fields`. Claude never receives the raw record.
- **Lines 9–14:** `redact_sensitive_fields` iterates over the record dict and replaces any key in `SENSITIVE_FIELDS` with `"[REDACTED]"`. The result is serialized to a JSON string for the tool result `content` field.

The key point is that Claude literally cannot reveal what it never receives. A system prompt instruction saying “do not repeat salary information” still requires Claude to have seen the salary and then decide not to repeat it. The post-execution filter removes that decision from the model entirely.

## The confirmation flag pattern for irreversible actions[#](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#The-confirmation-flag-pattern-for-irreversible-actions)

Some tool calls cannot be undone: deleting a record, sending an email, or archiving an account. For these, a useful pattern is to require an explicit `confirmed` field in the tool’s input schema. Claude must set `confirmed: true` to proceed; without it, the function returns a summary of what would happen and waits.

Here is the pattern applied to a `delete_campaign` tool:

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

def delete\_campaign(campaign\_id: str, confirmed: bool = False) -> str:

campaign = get\_campaign\_summary(campaign\_id)

if not confirmed:

return (

f"CONFIRMATION\_REQUIRED: This will permanently delete campaign '{campaign['name']}' "

f"({campaign['recipient\_count']} recipients, created {campaign['created\_date']}). "

"To confirm deletion, call this tool again with confirmed=true."

)

execute\_campaign\_deletion(campaign\_id)

return f"Campaign '{campaign['name']}' has been permanently deleted."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The delete\_campaign function requires confirmed=True to execute. On the first call without confirmation, it returns a summary of what would be deleted, giving Claude and, through Claude, the user, a checkpoint before the irreversible action runs.

- **Lines 1–2:** The function fetches the campaign summary regardless of the `confirmed` flag. This is needed to populate the confirmation message.
- **Lines 4–9:** When `confirmed` is `false` (the default), the function returns a human-readable description of the action and its scope. Claude reads this and presents it to the user before proceeding.
- **Lines 11–12:** Only when `confirmed` is explicitly `true` does the deletion execute. The default of `false` means a call without the argument never deletes anything, which is the safe default.

In the tool definition, `confirmed` is included in the schema so Claude knows it can provide it:

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

{

"name": "delete\_campaign",

"description": (

"Permanently delete a marketing campaign and all its data. "

"This action cannot be undone. "

"On the first call, return a summary of what will be deleted. "

"Only execute the deletion when confirmed=true is explicitly provided."

),

"input\_schema": {

"type": "object",

"properties": {

"campaign\_id": {"type": "string"},

"confirmed": {"type": "boolean", "description": "Set to true only after the user has reviewed the deletion summary."}

},

"required": ["campaign\_id"]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The tool definition for delete\_campaign. The description tells Claude when to set confirmed=true. The confirmed field is not required; its absence defaults to the safe, non-destructive path.

- **Lines 2–6:** The description is load-bearing here. It tells Claude the expected two-step flow: the first call surfaces the summary, and the second call (with `confirmed=true`) executes. Without this guidance, Claude might set `confirmed=true` on the first call.
- **Lines 14–15:** `confirmed` is present in `properties` but absent from `required`. This means Claude can omit it on the first call, and the function defaults to the safe path. Requiring it would force Claude to always provide a value, which creates ambiguity about what the default should be.

## When to use prompt guidance vs. programmatic enforcement[#](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#When-to-use-prompt-guidance-vs-programmatic-enforcement)

Not every constraint needs a code-level guard. The rule is: if violating the constraint has real-world consequences that cannot be reversed, the enforcement belongs in code. If the constraint is a quality preference with no hard consequence for occasional deviation, it belongs in the prompt. The table below shows examples of each category:

|  |  |  |
| --- | --- | --- |
| **Constraint** | **Type** | **Enforcement Point** |
| Discount rate must not exceed 20% | Business rule | Code (pre-execution check) |
| Sensitive fields must not be shown | Security rule | Code (post-execution filter) |
| Deletion requires explicit confirmation | Irreversibility guard | Code (confirmation flag) |
| Responses should be concise | Style preference | System prompt |
| Use formal language with enterprise customers | Tone preference | System prompt |
| Try the FAQ tool before escalating | Routing preference | System prompt |

The three code-enforced rules in the table share one property: Violating them produces a result that cannot be corrected after the fact. A 35% discount was applied. A salary was revealed. A campaign was deleted. Prompt instructions can guide the model toward correct behavior under normal conditions, but they cannot guarantee it under all conditions.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Complete-code)

We bring all three enforcement patterns from this lesson, the pre-execution discount cap, the post-execution sensitive-field filter, and the confirmation flag for irreversible actions, into one runnable file. No API key is needed; the script runs entirely in Python, and we see the outcome of each enforcement check printed in sequence.

Python

```
import json

# Mock helper functions (replace with real implementations in production)

def calculate_discounted_total(order_id: str, rate: float) -> float:

base_totals = {"ORD-001": 150.00, "ORD-002": 320.00}

base = base_totals.get(order_id, 100.00)

return round(base * (1 - rate), 2)

def get_employee_record(employee_id: str) -> dict:

return {

"name": "Jane Smith", "title": "Senior Engineer",

"department": "Engineering", "email": "jane@example.com",

"salary": 120000, "tax_id": "XXX-XX-1234",

"bank_account_number": "****5678"

}

def get_campaign_summary(campaign_id: str) -> dict:

return {"name": "Summer Sale 2024", "recipient_count": 15000, "created_date": "2024-06-01"}

def execute_campaign_deletion(campaign_id: str) -> None:

print(f"  [executed] Campaign {campaign_id} permanently deleted.")

SENSITIVE_FIELDS = {"salary", "tax_id", "bank_account_number"}

def apply_discount(order_id: str, rate: float) -> str:

if rate > 0.20:

return (f"POLICY_VIOLATION: Discount rate {rate:.0%} exceeds the 20% maximum. "

"Discounts above 20% require manager approval. The discount was not applied.")

new_total = calculate_discounted_total(order_id, rate)

return f"Discount of {rate:.0%} applied to order {order_id}. New total: ${new_total:.2f}."

def redact_sensitive_fields(record: dict, fields_to_redact: set) -> str:

redacted = {k: "[REDACTED]" if k in fields_to_redact else v for k, v in record.items()}

return json.dumps(redacted, indent=2)

def delete_campaign(campaign_id: str, confirmed: bool = False) -> str:

campaign = get_campaign_summary(campaign_id)

if not confirmed:

return (f"CONFIRMATION_REQUIRED: This will permanently delete campaign "

f"'{campaign['name']}' ({campaign['recipient_count']} recipients, "

f"created {campaign['created_date']}). "

"To confirm deletion, call this tool again with confirmed=true.")

execute_campaign_deletion(campaign_id)

return f"Campaign '{campaign['name']}' has been permanently deleted."

def dispatch_tool(name: str, input_args: dict, user_role: str = "agent") -> str:

if name == "apply_discount":

rate = input_args.get("rate", 0)

if rate > 0.20 and user_role != "manager":

return (f"POLICY_VIOLATION: Discount rate {rate:.0%} exceeds 20%. "

"Manager approval required.")

return apply_discount(**input_args)

if name == "get_employee_record":

raw_result = get_employee_record(**input_args)

return redact_sensitive_fields(raw_result, SENSITIVE_FIELDS)

if name == "delete_campaign":

return delete_campaign(**input_args)

return f"Unknown tool: {name}"

if __name__ == "__main__":

print("=== Pre-execution: discount within cap ===")

print(dispatch_tool("apply_discount", {"order_id": "ORD-001", "rate": 0.10}))

print("\n=== Pre-execution: discount exceeds cap (non-manager) ===")

print(dispatch_tool("apply_discount", {"order_id": "ORD-001", "rate": 0.35}))

print("\n=== Pre-execution: discount exceeds cap (manager role) ===")

print(dispatch_tool("apply_discount", {"order_id": "ORD-001", "rate": 0.35}, user_role="manager"))

print("\n=== Post-execution: employee record with sensitive fields redacted ===")

print(dispatch_tool("get_employee_record", {"employee_id": "EMP-42"}))

print("\n=== Confirmation flag: delete campaign (unconfirmed) ===")

print(dispatch_tool("delete_campaign", {"campaign_id": "CAMP-007"}))

print("\n=== Confirmation flag: delete campaign (confirmed) ===")

print(dispatch_tool("delete_campaign", {"campaign_id": "CAMP-007", "confirmed": True}))
```

⋯

All three enforcement patterns in one file

The script runs six cases in sequence: a valid discount, a blocked over-cap discount (agent role), an approved over-cap discount (manager role), a redacted employee record, an unconfirmed campaign deletion, and a confirmed deletion.

Output is deterministic; no API call is required.

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

=== Pre-execution: discount within cap ===

Discount of 10% applied to order ORD-001. New total: $135.00.

=== Pre-execution: discount exceeds cap (non-manager) ===

POLICY\_VIOLATION: Discount rate 35% exceeds 20%. Manager approval required.

=== Pre-execution: discount exceeds cap (manager role) ===

Discount of 35% applied to order ORD-001. New total: $97.50.

=== Post-execution: employee record with sensitive fields redacted ===

{

"name": "Jane Smith",

"title": "Senior Engineer",

"department": "Engineering",

"email": "jane@example.com",

"salary": "[REDACTED]",

"tax\_id": "[REDACTED]",

"bank\_account\_number": "[REDACTED]"

}

=== Confirmation flag: delete campaign (unconfirmed) ===

CONFIRMATION\_REQUIRED: This will permanently delete campaign 'Summer Sale 2024' ...

=== Confirmation flag: delete campaign (confirmed) ===

[executed] Campaign CAMP-007 permanently deleted.

Campaign 'Summer Sale 2024' has been permanently deleted.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Output

The manager-role case shows that the same 35% discount rate that is blocked for a non-manager is approved when `user_role="manager"` is passed to the dispatcher. The redacted record shows that `salary`, `tax_id`, and `bank_account_number` are replaced with `"[REDACTED]"` before the string is returned; Claude never sees those values.

## Exercise: Choose the enforcement point[#](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Exercise-Choose-the-enforcement-point)

Read each constraint. Decide: Should this be enforced in the system prompt or with a programmatic check in the dispatch function?

Technical Quiz

1.

A legal document agent must never include specific legal advice and should only provide general legal information. Violations are not contractually consequential, but they are still a compliance concern. What is the most appropriate enforcement approach?

A.

System prompt instruction. Enough here, since a rule with no contractual stakes needs only guidance.

B.

Programmatic post-execution filter. Strip any text matching legal advice patterns before Claude’s response is returned.

C.

Pre-execution check in `dispatch_tool`. Block the tool call if the task involves legal advice.

D.

A separate classifier model that reviews every response before it is shown to the user.

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Whats-next)

In the next lesson, we examine the third reliability concern introduced in this chapter: session management. Long-running agents build up context that can become stale, consume the context window, or cause the agent to drift from its original goal. We cover four session strategies: resume, fork, summarize, and clean session. We also introduce fact preservation to connect this lesson to the context management chapter.

Fixed Workflows and Adaptive Agents

Session Strategy and Context Primer

Ask

[Why the system prompt is not enough](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Why-the-system-prompt-is-not-enough)

[Pre-execution enforcement: Checking inputs before the tool runs](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Pre-execution-enforcement-Checking-inputs-before-the-tool-runs)

[Post-execution enforcement: Filtering results before Claude reads them](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Post-execution-enforcement-Filtering-results-before-Claude-reads-them)

[The confirmation flag pattern for irreversible actions](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#The-confirmation-flag-pattern-for-irreversible-actions)

[When to use prompt guidance vs. programmatic enforcement](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#When-to-use-prompt-guidance-vs-programmatic-enforcement)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Complete-code)

[Exercise: Choose the enforcement point](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Exercise-Choose-the-enforcement-point)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/guardrails-outside-the-prompt#Whats-next)