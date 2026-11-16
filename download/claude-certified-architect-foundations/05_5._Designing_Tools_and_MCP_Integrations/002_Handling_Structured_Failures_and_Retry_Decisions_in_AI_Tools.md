# Handling_Structured_Failures_and_Retry_Decisions_in_AI_Tools

Source: https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Structured Failures and Retry Decisions

Explore how to design structured failure returns that provide actionable information for AI agents, enabling reliable error handling and retry decisions. Understand the four failure categories, the dangers of empty or None returns, and how to propagate data gaps in multi-agent architectures for clearer system responses.

We'll cover the following...

- [Why return values for failure matter](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Why-return-values-for-failure-matter)
- [The four failure categories](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#The-four-failure-categories)
- [Writing structured error strings](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Writing-structured-error-strings)
- [Why None and empty strings are dangerous](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Why-None-and-empty-strings-are-dangerous)
- [The data\_gaps pattern for multi-agent propagation](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#The-datagaps-pattern-for-multi-agent-propagation)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Complete-code)
- [Exercise: Trace the failure path](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Exercise-Trace-the-failure-path)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Whats-next)

In the previous lesson, we focused on the tool description as the mechanism for shaping when and how Claude calls a tool. This lesson covers what happens after the call: what the tool returns when something goes wrong and how that return value determines whether Claude can recover gracefully or is left guessing.

A tool that returns `None`, an empty string, or a raw Python exception message on failure is not giving Claude anything to work with. A tool that returns a structured error string tells Claude exactly what failed, why, and what the agent should do next. The difference between these two behaviors is the difference between a loop that degrades silently and a loop that reports gaps correctly. By the end of this lesson, we will be able to:

- Identify the four failure categories that tool return values must cover
- Write structured error strings that give Claude actionable information for each failure type
- Explain why `None` and the empty string are dangerous return values for tool failures
- Apply the `data_gaps` pattern for propagating failures through multi-agent systems

## Why return values for failure matter[#](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Why-return-values-for-failure-matter)

When Claude receives a tool result, it reads the content string and decides what to do next. That decision is only as good as the information in the string.

Consider a tool that retrieves a customer's billing history. Three different things could go wrong:

1. The customer account does not exist
2. The billing API is down
3. The caller does not have permission to access billing data

If all three cases return an empty string or `None`, Claude reads no content and cannot distinguish between them. It may assume the billing history is simply empty, tell the user there are no charges on record, and close the conversation with a factually wrong answer.

If each case returns a structured string that names the failure type, Claude reads the error, understands what happened, and can respond accordingly: "The account was not found," "The billing system is temporarily unavailable," or "You do not have permission to view this account's billing records."

The tool return value is not just the result of the function. It is the signal Claude uses to decide what comes next.

## The four failure categories[#](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#The-four-failure-categories)

Every tool failure falls into one of four categories. Each requires a different return structure:

|  |  |  |
| --- | --- | --- |
| **Category** | **What Happened** | **What Claude Needs to Know** |
| Access failure | The data source was unreachable | That the lookup was attempted but failed, and why |
| Empty result | The lookup succeeded, but found nothing | That the source is accessible and definitely contains no matching records |
| Validation error | The arguments Claude provided were invalid | Which argument was wrong, and what a valid value looks like |
| Permission denied | The caller lacks access rights | That the request was blocked, not that the data is absent |

The most critical distinction to understand is between access failure and an empty result. In the previous chapter on multi-agent orchestration, we saw that this distinction determines whether a coordinator reports "no records found" (a clean finding) or "could not check" (an unresolved gap). The same principle applies at the individual tool level.

The diagram below shows how these four categories map to different Claude responses.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27803.54%27%20height=%27523%27/%3e)![Four structured return categories produce four distinct Claude responses](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Four structured return categories produce four distinct Claude responses")

Four structured return categories produce four distinct Claude responses

## Writing structured error strings[#](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Writing-structured-error-strings)

A structured error string has three components: an error type prefix, a human-readable description, and an action hint.

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

def get\_billing\_history(account\_id: str, caller\_role: str = "agent") -> str:

if not account\_id.startswith("ACC-"):

return (

"VALIDATION\_ERROR: account\_id must begin with 'ACC-' (received: "

f"'{account\_id}'). Example of a valid value: 'ACC-00123'."

)

if caller\_role not in ("billing\_admin", "support\_tier2"):

return (

"PERMISSION\_DENIED: Billing history requires billing\_admin or support\_tier2 "

f"role. Caller role '{caller\_role}' is not authorized. "

"Escalate to a billing team member to retrieve this information."

)

try:

records = billing\_api.fetch(account\_id)

except BillingAPIUnavailable as exc:

return (

f"ACCESS\_FAILURE: Billing API is unreachable ({exc}). "

"The lookup was attempted but could not complete. "

"Treat this billing history as unknown, not as empty."

)

if not records:

return (

f"RESULT: Billing history for account {account\_id} is empty. "

"The account exists and the API is accessible: there are no charges on record."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A tool function that returns a distinct structured string for each of the four failure categories. Every return path gives Claude enough information to compose an accurate response.

- **Lines 25:** Validation error. The prefix `VALIDATION_ERROR:` names the category. The description says what is wrong with the argument. The example gives Claude a concrete correction to suggest to the user.
- **Lines 712:** Permission denied. The prefix `PERMISSION_DENIED:` names the category. The description names the required roles. The action hint tells Claude what to suggest: escalate rather than try another approach.
- **Lines 1420:** Access failure. The prefix `ACCESS_FAILURE:` names the category. The phrase "Treat this billing history as unknown, not as empty" is load-bearing: it tells Claude explicitly how to characterize the gap in its response, preventing the empty-equals-clean mistake.
- **Lines 2226:** Empty result. The success case with no records. Note that this is clearly labeled as a clean negative: "The account exists and the API is accessible." Claude can report "no charges on record" with confidence because the tool confirmed the source is reachable.
- **Line 28:** Successful result with data. The only case where we return JSON.

## Why `None` and empty strings are dangerous[#](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Why-None-and-empty-strings-are-dangerous)

Both `None` and `""` (empty string) are invisible failures. Claude reads them as "the tool returned nothing" and does one of two things: it assumes the lookup produced an empty result, or it re-calls the tool, hoping for a different answer.

The access-failure case is the most dangerous. If a billing API is down and the tool returns `""`, Claude reports "no billing history found" with the same confidence it would if the account genuinely had no charges. The user acts on that report. If it later turns out that the billing API was unavailable and the account has significant charges, the agent produced a false report. A raw exception message is slightly better than `None` in that it contains some information, but it is not designed for Claude to parse:

Ace Editor

1

2

3

4

5

6

7

# Wrong: letting Python exceptions propagate as strings

try:

records = billing\_api.fetch(account\_id)

except Exception as exc:

return str(exc)

# Returns something like:

# "ConnectionRefusedError: [Errno 111] Connection refused"

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Claude can read this and infer that something went wrong, but it has no category prefix to trigger the right response pattern, no action hint, and no instruction about how to characterize the gap. A structured error string is always preferable.

## The `data_gaps` pattern for multi-agent propagation[#](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#The-datagaps-pattern-for-multi-agent-propagation)

When a tool result flows through a multi-agent system, the coordinator needs to collect failure information across all specialists and surface it in the final report. The `data_gaps` field in structured results is the mechanism for this.

A tool that fails does not just return an error string to the specialist. The specialist parses that string, adds the failure to its own `data_gaps` list, and returns a result that the coordinator can process uniformly:

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

def run\_billing\_specialist(account\_id: str) -> dict:

result = get\_billing\_history(account\_id)

if result.startswith("ACCESS\_FAILURE"):

return {

"billing\_records": None,

"data\_gaps": [f"billing history: {result}"],

"status": "access\_failure"

}

if result.startswith("PERMISSION\_DENIED"):

return {

"billing\_records": None,

"data\_gaps": [f"billing history: {result}"],

"status": "permission\_denied"

}

if result.startswith("RESULT"):

return {

"billing\_records": [],

"data\_gaps": [],

"status": "empty"

}

records = json.loads(result)

return {

"billing\_records": records["records"],

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A specialist wrapper that converts tool error strings into structured result dicts. The coordinator receives the same dict shape from every path, and data\_gaps carries the failure detail upward.

- **Lines 3–7:** Access failure path. `billing_records` is `None` (unknown, not empty). The raw error string goes into `data_gaps` so the coordinator can include it in the report's disclosed gaps section. `status` is `"access_failure"`.
- **Lines 9–13:** Permission denied path. Same structure as access failure. The coordinator treats these identically for synthesis purposes: both are unresolvable gaps that must be disclosed.
- **Lines 15–19:** Empty result path. `billing_records` is `[]` (empty list, not `None`). `data_gaps` is empty. `status` is `"empty"`. The coordinator can report a clean negative.
- **Lines 21–25:** Success path. Records are populated. No gaps. The `None` vs. `[]` distinction at the record level mirrors the access failure vs. empty result distinction: `None` means unknown; `[]` means checked and found nothing.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Complete-code)

We combine all four failure categories, the structured error string pattern, and the `data_gaps` propagation chain from this lesson into a single file. No API key is requiredthe billing API is fully mocked, and each scenario is driven by which account ID and caller role the tool receives.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import json

# ─── Mock billing infrastructure (no real API needed) ─────────────────────────

class BillingAPIUnavailable(Exception):

pass

class _BillingAPI:

ACCOUNTS = {

"ACC-00100": [

{"date": "2025-03-01", "amount": 99.00,  "description": "Pro plan — monthly"},

{"date": "2025-04-01", "amount": 99.00,  "description": "Pro plan — monthly"},

],

"ACC-00200": [],          # exists but no charges

# ACC-00300 triggers a simulated API outage — see fetch()

}

def fetch(self, account_id: str) -> list[dict]:

if account_id == "ACC-00300":

raise BillingAPIUnavailable("connection to billing service timed out after 10s")

return self.ACCOUNTS.get(account_id, [])

billing_api = _BillingAPI()

# ─── Tool function: four structured failure categories ─────────────────────────

def get_billing_history(account_id: str, caller_role: str = "agent") -> str:

if not account_id.startswith("ACC-"):

return (

"VALIDATION_ERROR: account_id must begin with 'ACC-' (received: "

f"'{account_id}'). Example of a valid value: 'ACC-00123'."

)

if caller_role not in ("billing_admin", "support_tier2"):

return (

"PERMISSION_DENIED: Billing history requires billing_admin or support_tier2 "

f"role. Caller role '{caller_role}' is not authorized. "

"Escalate to a billing team member to retrieve this information."

)

try:

records = billing_api.fetch(account_id)

except BillingAPIUnavailable as exc:

return (

f"ACCESS_FAILURE: Billing API is unreachable ({exc}). "

"The lookup was attempted but could not complete. "

"Treat this billing history as unknown, not as empty."

)

if not records:

return (

f"RESULT: Billing history for account {account_id} is empty. "

"The account exists and the API is accessible: there are no charges on record."

)

return json.dumps({"account_id": account_id, "records": records})

# ─── Specialist wrapper: data_gaps propagation ────────────────────────────────

def run_billing_specialist(account_id: str) -> dict:

# Specialists run with billing_admin access via their authorization context.

result = get_billing_history(account_id, caller_role="billing_admin")

if result.startswith("ACCESS_FAILURE"):

return {

"billing_records": None,

"data_gaps":       [f"billing history: {result}"],

"status":          "access_failure",

}

if result.startswith("PERMISSION_DENIED"):

return {

"billing_records": None,

"data_gaps":       [f"billing history: {result}"],

"status":          "permission_denied",

}

if result.startswith("RESULT"):

return {

"billing_records": [],

"data_gaps":       [],

"status":          "empty",

}

records = json.loads(result)

return {

"billing_records": records["records"],

"data_gaps":       [],

"status":          "found",

}

if __name__ == "__main__":

print("=== Four failure categories in get_billing_history ===\n")

cases = [

("12345",     "billing_admin",  "validation error — bad account_id format"),

("ACC-00100", "support_tier1",  "permission denied — unauthorized role"),

("ACC-00300", "billing_admin",  "access failure — API unreachable"),

("ACC-00200", "billing_admin",  "empty result — account exists, no charges"),

("ACC-00100", "billing_admin",  "success — account with two charge records"),

]

for account_id, caller_role, label in cases:

result = get_billing_history(account_id, caller_role)

prefix = result.split(":")[0].strip()

print(f"[{label}]")

print(f"  prefix  : {prefix}")

print(f"  content : {result[:110]}{'...' if len(result) > 110 else ''}")

print()

print("=== data_gaps propagation through run_billing_specialist ===\n")

specialist_cases = [

("ACC-00100", "success — records found"),

("ACC-00200", "empty — no charges on record"),

("ACC-00300", "access failure — propagated to data_gaps"),

]

for account_id, label in specialist_cases:

r = run_billing_specialist(account_id)

print(f"[{label}]")

print(f"  billing_records : {r['billing_records']}")

print(f"  data_gaps       : {r['data_gaps']}")

print(f"  status          : {r['status']}")

print()

print("Key distinctions:")

print("  None  in billing_records → access failure (unknown — could not check)")

print("  []    in billing_records → empty result  (checked — found nothing)")

print("  [...] in billing_records → success       (checked — records returned)")
```

⋯

All four failure categories and the specialist wrapper in one file. No API key required. ACC-00300 always triggers an access failure, ACC-00200 always returns empty, and ACC-00100 with an authorized role always succeeds.

Running the script produces output like this:

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

=== Four failure categories in get\_billing\_history ===

[validation error — bad account\_id format]

prefix : VALIDATION\_ERROR

content : VALIDATION\_ERROR: account\_id must begin with 'ACC-' (received: '12345'). Example of a valid value: 'ACC-00123'.

[permission denied — unauthorized role]

prefix : PERMISSION\_DENIED

content : PERMISSION\_DENIED: Billing history requires billing\_admin or support\_tier2 role. Caller role 'support\_tier1' is...

[access failure — API unreachable]

prefix : ACCESS\_FAILURE

content : ACCESS\_FAILURE: Billing API is unreachable (connection to billing service timed out after 10s). The lookup was...

[empty result — account exists, no charges]

prefix : RESULT

content : RESULT: Billing history for account ACC-00200 is empty. The account exists and the API is accessible: there are...

[success — account with two charge records]

prefix : {

content : {"account\_id": "ACC-00100", "records": [{"date": "2025-03-01", "amount": 99.0, ...}]}

=== data\_gaps propagation through run\_billing\_specialist ===

[success — records found]

billing\_records : [{'date': '2025-03-01', 'amount': 99.0, 'description': 'Pro plan — monthly'}, ...]

data\_gaps : []

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The `None` vs. `[]` distinction in `billing_records` mirrors the access-failure vs. empty-result distinction at the coordinator level. An `ACCESS_FAILURE` string gets routed into `data_gaps` so the coordinator can disclose the gap explicitly. A `RESULT` string with no records routes to `billing_records: []`, a confirmed negative, which the coordinator can report as “no charges on record.”

## Exercise: Trace the failure path[#](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Exercise-Trace-the-failure-path)

Read the following scenario and answer the questions.

A coordinator runs a compliance specialist to check whether a company has any regulatory violations on record. The specialist calls `check_regulatory_violations(company_id="C-8821")`. The tool function attempts to query a government database, but the connection times out after 30 seconds. The tool returns:

Ace Editor

1

"ACCESS\_FAILURE: Regulatory database connection timed out after 30s. The lookup was attempted but could not complete. Treat violation status as unknown, not as clean."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Technical Quiz

1.

The specialist receives this string. What should the specialist’s `data_gaps` field contain?

A.

An empty list, because the specialist tried, and Claude should not penalize it for a timeout.

B.

The full tool return string as the only element in a list labeled `"error"`

C.

`["timeout"]`

D.

`["regulatory violations: ACCESS_FAILURE: Regulatory database connection timed out after 30s..."]`

---

1 / 3

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Whats-next)

In the next lesson, we move from individual tool design to the server layer: how MCP (Model Context Protocol) exposes tools to Claude, how to configure an MCP server, and how tool registration in MCP maps to the concepts we have built so far.

Tool Descriptions That Guide Selection

MCP Configuration and Tool Distribution

Ask

[Why return values for failure matter](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Why-return-values-for-failure-matter)

[The four failure categories](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#The-four-failure-categories)

[Writing structured error strings](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Writing-structured-error-strings)

[Why None and empty strings are dangerous](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Why-None-and-empty-strings-are-dangerous)

[The data\_gaps pattern for multi-agent propagation](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#The-datagaps-pattern-for-multi-agent-propagation)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Complete-code)

[Exercise: Trace the failure path](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Exercise-Trace-the-failure-path)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/structured-failures-and-retry-decisions#Whats-next)