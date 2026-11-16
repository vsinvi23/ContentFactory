# Handling_Partial_Failures_and_Recovery_in_Claude_AI_Systems

Source: https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Partial Failures and Recovery

Explore how to identify and handle four types of partial failures in Claude AI workflows, including access failures, empty results, stale data, and partial completions. Learn to create coordinator-safe result objects and implement routing logic for effective recovery and escalation in production pipelines.

We'll cover the following...

- [The four partial failure types](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#The-four-partial-failure-types)
- [The coordinator-safe result object](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#The-coordinator-safe-result-object)
- [Producing partial results in practice](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Producing-partial-results-in-practice)
- [Coordinator routing by failure type](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Coordinator-routing-by-failure-type)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Complete-code)
- [What not to do: Treating all partial failures as retryable](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#What-not-to-do-Treating-all-partial-failures-as-retryable)
- [Exercise: Classify and route](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Exercise-Classify-and-route)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Whats-next)

A total failure is easy to handle: every field is missing, the tool call returned an error, and the document cannot be processed. A partial failure is harder. Some fields succeeded; others did not. The tool returned a result, but it was empty, outdated, or covered only part of the document. In a pipeline, partial failures can propagate silently if the result object does not carry enough information for the coordinator to distinguish them from success. A coordinator that receives `{"status": "ok", "fields": {}}` cannot tell whether the extraction found nothing because the document had no extractable content, because a tool call failed halfway through, or because the document is from last quarter and should have been refreshed before processing.

This lesson covers how to classify partial failures precisely and how to build result objects that give the coordinator the information it needs to act. By the end of this lesson, we will be able to:

- Distinguish the four partial failure types and explain why each requires a different response.
- Write a coordinator-safe result object that carries a failure type, available data, and a recovery hint.
- Implement coordinator logic that routes each failure type to the correct recovery action.
- Explain why treating all partial failures as retryable is a design antipattern.

## The four partial failure types[#](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#The-four-partial-failure-types)

Partial failures look similar on the surface. The pipeline did not produce a complete result, but partial failures arise from different causes and require different responses.

- **Access failure:** The agent attempted to call a tool or retrieve a resource and received a permission error, a network timeout, or a service unavailability response. No data was returned. The document or resource exists, but the agent could not reach it. Retrying with the same credentials will fail again unless the access problem is fixed first.
- **Empty result:** The tool call succeeded and the query executed correctly, but the result set was empty. The document was processed, the extraction ran, and nothing matching the query criteria was found. This is not an error; it is accurate information. Retrying will return the same empty result. The correct response is to treat the absence as data: record that the field is genuinely absent from this source and continue.
- **Stale data:** The tool call succeeded and returned data, but the data is outdated relative to the task's requirements. A document retrieved from a cache may be from a prior quarter. A pricing record may be from before a fee change that is relevant to the current calculation. The agent has data but cannot use it without first determining whether its age makes it unreliable for this decision.
- **Partial completion:** The agent began a multi-step process and completed some steps but not others before failing. Some fields are extracted correctly and have passed validation; others were not reached before the failure. The completed work is valid and should not be discarded. Only the incomplete portion needs recovery.

## The coordinator-safe result object[#](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#The-coordinator-safe-result-object)

A coordinator-safe result object carries three things: the data that was successfully produced, the failure classification for what was not, and a recovery hint that tells the coordinator what to do next. The coordinator should not need to inspect the error message or rerun the step to decide how to respond.

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

from dataclasses import dataclass, field

from typing import Optional

@dataclass

class PartialResult:

step: str

status: str

fields: dict

failure\_type: Optional[str] = None

failure\_detail: Optional[str] = None

recovery\_hint: Optional[str] = None

@property

def is\_complete(self) -> bool:

return self.status == "complete"

@property

def is\_recoverable(self) -> bool:

return self.failure\_type in ("empty\_result", "partial\_completion")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A PartialResult dataclass that separates extracted data (fields) from failure metadata. failure\_type is a controlled vocabulary — one of "access\_failure", "empty\_result", "stale\_data", or "partial\_completion" — not a free-text error message. recovery\_hint tells the coordinator the recommended next action.

- **Lines 4–10:** `fields` holds whatever data was successfully extracted before or despite the failure. For a partial completion, this may be a full dict with some keys; for an access failure, it will be empty. The coordinator checks `fields` for any salvageable data, regardless of failure type.
- **Lines 12–13:** `is_complete` is a property rather than a status comparison in caller code. This prevents callers from comparing status strings directly and makes the check readable at the coordinator level: `if result.is_complete`.
- **Lines 15–16:** `is_recoverable` encodes which failure types the coordinator can handle without escalation. Access failures and stale data are not considered recoverable by the agent alone; they require external action (fix permissions, refresh the source) before a retry can succeed.

## Producing partial results in practice[#](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Producing-partial-results-in-practice)

A specialist agent that performs multi-step extraction should produce a `PartialResult` at each step boundary so that a failure at step three does not discard the work from steps one and two:

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

def extract\_contract\_fields(document: str) -> PartialResult:

fields = {}

try:

fields["parties"] = extract\_parties(document)

fields["effective\_date"] = extract\_date(document)

except PermissionError as e:

return PartialResult(

step="party\_and\_date\_extraction",

status="failed",

fields=fields,

failure\_type="access\_failure",

failure\_detail=str(e),

recovery\_hint="Check tool permissions before retrying."

)

try:

clause\_results = extract\_clauses(document)

if not clause\_results:

fields["clauses"] = []

return PartialResult(

step="clause\_extraction",

status="partial",

fields=fields,

failure\_type="empty\_result",

failure\_detail="No clauses matched the extraction criteria.",

recovery\_hint="Treat clause absence as data; continue to validation."

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

An extraction function that catches different failure types at different steps and returns a PartialResult with the correct classification. The party and date fields are preserved in the fields dict even when clause extraction fails, so the coordinator does not discard valid work.

- **Lines 6–14:** A `PermissionError` during the first extraction block returns an `access_failure` result. The `fields` dict at this point may be empty or partial; whatever succeeded before the permission error is preserved.
- **Lines 17–26:** An empty `clause_results` is classified as `empty_result`, not as an error. The function sets `fields["clauses"] = []` explicitly to signal that the query ran and found nothing, rather than that it was not attempted. The recovery hint tells the coordinator to treat absence as data and continue.
- **Lines 27–37:** A `TimeoutError` during clause extraction returns a `partial_completion`. The recovery hint names which fields are valid and which step to retry, so the coordinator does not need to rerun the party and date extraction.

## Coordinator routing by failure type[#](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Coordinator-routing-by-failure-type)

The coordinator receives a list of `PartialResult` objects from specialist agents and must decide what to do with each. The routing logic is a direct translation of the failure type taxonomy:

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

def route\_result(result: PartialResult) -> str:

if result.is\_complete:

return "pass\_to\_validation"

match result.failure\_type:

case "access\_failure":

return "escalate"

case "empty\_result":

return "accept\_as\_data\_gap"

case "stale\_data":

return "escalate\_or\_refresh"

case "partial\_completion":

return "retry\_incomplete\_steps"

case \_:

return "escalate"

def coordinate(results: list[PartialResult]) -> dict:

routing = {}

for r in results:

action = route\_result(r)

routing[r.step] = {

"action": action,

"fields": r.fields,

"hint": r.recovery\_hint

}

return routing

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A coordinator that routes each result to one of four recovery actions based on failure type. The routing logic is a match statement on the controlled vocabulary, so adding a new failure type requires only adding a new case. The \_ fallback escalates any unrecognized failure type.

- **Lines 6–7:** Access failures are routed to escalation, not retry. Retrying an access failure without fixing the permission problem will produce the same result. The escalation packet should include the failure detail so the reviewer knows what permission to grant.
- **Lines 8–9:** Empty results are accepted as data gaps. The coordinator records that the field is absent from this source and continues. Retrying an empty query against the same source is wasteful.
- **Lines 10–11:** Stale data is routed to escalate-or-refresh. The coordinator either flags the data age for a human decision or calls a refresh tool that retrieves a current version before continuing. The routing is ambiguous here by design; whether to refresh automatically or escalate depends on how stale the data is and whether an automatic refresh tool is available.
- **Lines 12–13:** Partial completions are routed to a retry of only the incomplete steps. The coordinator uses the `fields` dict from the result to determine which steps produced valid output and the `recovery_hint` to target the retry correctly.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Complete-code)

We bring the `PartialResult` dataclass, the four failure-mode extraction functions, the coordinator router, and all four demo scenarios from this lesson into one runnable file. We need no API key. We run each failure mode in sequence and see the coordinator's routing decision for each.

Python

```
from dataclasses import dataclass

from typing import Optional

@dataclass

class PartialResult:

step:           str

status:         str

fields:         dict

failure_type:   Optional[str] = None

failure_detail: Optional[str] = None

recovery_hint:  Optional[str] = None

@property

def is_complete(self) -> bool:

return self.status == "complete"

@property

def is_recoverable(self) -> bool:

return self.failure_type in ("empty_result", "partial_completion")

def extract_parties(document: str) -> list:

return ["Party A: Acme Corp", "Party B: Beta Ltd"]

def extract_date(document: str) -> str:

return "2024-09-01"

def extract_clauses(document: str, start_clause: int = 1) -> list:

all_clauses = [

"§1 Definitions", "§2 Term", "§3 Payment", "§4 Liability", "§5 Indemnification"

]

return all_clauses[start_clause - 1:]

def extract_contract_fields(document: str, simulate_failure: str = "none") -> PartialResult:

fields = {}

try:

if simulate_failure == "permission":

raise PermissionError("Access denied: document vault requires elevated credentials.")

fields["parties"]        = extract_parties(document)

fields["effective_date"] = extract_date(document)

except PermissionError as e:

return PartialResult(

step="party_and_date_extraction",

status="failed",

fields=fields,

failure_type="access_failure",

failure_detail=str(e),

recovery_hint="Check tool permissions before retrying."

)

try:

if simulate_failure == "empty":

clause_results = []

elif simulate_failure == "timeout":

fields["clauses_partial"] = extract_clauses(document)[:2]

raise TimeoutError("Clause extraction timed out after processing 2 of 5 clauses.")

else:

clause_results = extract_clauses(document)

if not clause_results:

fields["clauses"] = []

return PartialResult(

step="clause_extraction",

status="partial",

fields=fields,

failure_type="empty_result",

failure_detail="No clauses matched the extraction criteria.",

recovery_hint="Treat clause absence as data; continue to validation."

)

fields["clauses"] = clause_results

except TimeoutError as e:

return PartialResult(

step="clause_extraction",

status="partial",

fields=fields,

failure_type="partial_completion",

failure_detail=str(e),

recovery_hint=(

"Retry clause extraction only. "

"Party and date fields in `fields` are valid."

)

)

return PartialResult(step="full_extraction", status="complete", fields=fields)

def route_result(result: PartialResult) -> str:

if result.is_complete:

return "pass_to_validation"

match result.failure_type:

case "access_failure":

return "escalate"

case "empty_result":

return "accept_as_data_gap"

case "stale_data":

return "escalate_or_refresh"

case "partial_completion":

return "retry_incomplete_steps"

case _:

return "escalate"

def coordinate(results: list[PartialResult]) -> list[dict]:

routing = []

for r in results:

action = route_result(r)

routing.append({

"step":   r.step,

"action": action,

"fields": list(r.fields.keys()),

"hint":   r.recovery_hint

})

return routing

SAMPLE_DOCUMENT = "SERVICE AGREEMENT between Acme Corp and Beta Ltd, effective 2024-09-01."

if __name__ == "__main__":

scenarios = [

("none",       "Clean extraction (complete)"),

("permission", "Access failure during party extraction"),

("empty",      "Empty clause result"),

("timeout",    "Timeout during clause extraction (partial completion)"),

]

results = []

for failure_mode, label in scenarios:

print(f"\n=== {label} ===")

result = extract_contract_fields(SAMPLE_DOCUMENT, simulate_failure=failure_mode)

results.append(result)

print(f"  step:           {result.step}")

print(f"  status:         {result.status}")

print(f"  failure_type:   {result.failure_type}")

print(f"  is_complete:    {result.is_complete}")

print(f"  is_recoverable: {result.is_recoverable}")

if result.recovery_hint:

print(f"  recovery_hint:  {result.recovery_hint}")

print(f"  fields extracted: {list(result.fields.keys())}")

print("\n=== Coordinator Routing ===")

routing = coordinate(results)

for entry in routing:

print(f"\n  step: {entry['step']}")

print(f"    action: {entry['action']}")

print(f"    fields: {entry['fields']}")

if entry["hint"]:

print(f"    hint:   {entry['hint']}")
```

⋯

All four failure modes and the coordinator router in one file

Each scenario exercises a different branch of the `PartialResult` taxonomy: complete extraction, access failure, empty clause set, and timeout with partial data. The coordinator section shows how each failure type maps to a distinct downstream action.

Expected output is deterministic; no API call is required.

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

=== Clean extraction (complete) ===

step: full\_extraction

status: complete

failure\_type: None

is\_complete: True

is\_recoverable: False

fields extracted: ['parties', 'effective\_date', 'clauses']

=== Access failure during party extraction ===

step: party\_and\_date\_extraction

status: failed

failure\_type: access\_failure

is\_complete: False

is\_recoverable: False

recovery\_hint: Check tool permissions before retrying.

fields extracted: []

=== Empty clause result ===

step: clause\_extraction

status: partial

failure\_type: empty\_result

is\_complete: False

is\_recoverable: True

recovery\_hint: Treat clause absence as data; continue to validation.

fields extracted: ['parties', 'effective\_date', 'clauses']

=== Timeout during clause extraction (partial completion) ===

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The `is_recoverable` property shows the key distinction: access failures are not recoverable and should be escalated immediately, while empty results and partial completions are recoverable (the coordinator can route them without human intervention). The timeout case preserves the two clauses that were extracted before the cutoff; the retry only needs to restart from clause three, not clause one.

## What not to do: Treating all partial failures as retryable[#](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#What-not-to-do-Treating-all-partial-failures-as-retryable)

A common anti-pattern is to route all partial failures to a retry loop, reasoning that “more attempts cannot hurt.” It can.

- Retrying an access failure calls the same tool with the same credentials, hits the same permission wall, and burns retry budget without making progress. The third retry produces the same error as the first. Meanwhile, the document sits in the pipeline queue.
- Retrying an empty result reruns a query that returned nothing. The source has not changed between retries. The second and third attempts return the same empty result. When all retries are exhausted, the pipeline escalates, introducing delay and reviewer load for a result that was correct on the first attempt.
- Retrying a stale data result downloads the same cached version again unless the retry explicitly clears the cache or calls a different endpoint. Without a mechanism to reach fresher data, a retry is equivalent to rereading the same document.

The retry loop is designed for one failure type: partial completion, where the agent stopped partway through because of a transient error and can resume from where it left off. Applying it to all failure types dilutes its effectiveness and inflates the escalation queue with failures that could have been classified and handled on the first attempt.

## Exercise: Classify and route[#](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Exercise-Classify-and-route)

Each scenario describes a partial failure in a running pipeline. Identify the failure type and the correct coordinator action.

Technical Quiz

1.

A specialist agent calls a pricing database tool to retrieve the current fee schedule. The tool returns a result with `"last_updated": "2024-03-01"`. The current date is 2024-11-14, and the task requires current-quarter pricing. What failure type is this, and what is the correct coordinator action?

A.

Partial completion — retry only the pricing tool call and keep the rest of the work

B.

Access failure — escalate so an admin can review the tool’s permissions

C.

Stale data — refresh or escalate to get the current-quarter fee schedule

D.

Empty result — accept the absence of current data as a data gap and continue

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Whats-next)

In the next lesson, we compile an anti-pattern reference that consolidates the failure modes, design mistakes, and incorrect assumptions from across the course into a single reference for architectural review.

Escalation and Human Review

Anti-Pattern Reference

Ask

[The four partial failure types](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#The-four-partial-failure-types)

[The coordinator-safe result object](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#The-coordinator-safe-result-object)

[Producing partial results in practice](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Producing-partial-results-in-practice)

[Coordinator routing by failure type](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Coordinator-routing-by-failure-type)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Complete-code)

[What not to do: Treating all partial failures as retryable](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#What-not-to-do-Treating-all-partial-failures-as-retryable)

[Exercise: Classify and route](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Exercise-Classify-and-route)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/partial-failures-and-recovery#Whats-next)