# Designing_Effective_Context_Handoff_in_Multi-Agent_Systems

Source: https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Context Handoff Design

Explore how to design precise handoff packets that coordinators send to specialists for task delegation in multi-agent AI systems. Learn to structure inputs and outputs, preserve data provenance, and resolve conflicts, improving reliability and clarity in complex AI workflows.

We'll cover the following...

- [What the handoff packet is](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#What-the-handoff-packet-is)
  - [The before: A messy coordinator handoff](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#The-before-A-messy-coordinator-handoff)
  - [The after: A scoped handoff packet](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#The-after-A-scoped-handoff-packet)
  - [Information provenance: Why sources must travel with results](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Information-provenance-Why-sources-must-travel-with-results)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Complete-code)
- [Exercise: Design the handoff](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Exercise-Design-the-handoff)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Whats-next)

The coordinator-specialist split from the previous lesson only works if the coordinator sends the right context to each specialist. Too little context, and the specialist cannot complete their task. Too much context, and the specialist's input is polluted with irrelevant information that degrades its decisions. In this lesson, we design the handoff packet: the structured object the coordinator sends to each specialist and the structure the specialist returns.

By the end of this lesson, we will be able to:

- Identify the four components of a well-formed handoff packet.
- Transform an overloaded coordinator prompt into scoped, per-specialist handoffs.
- Define the expected output shape specialists should return.
- Explain why information provenance must be preserved through the handoff chain.

## What the handoff packet is[#](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#What-the-handoff-packet-is)

A handoff packet is the structured input that the coordinator sends to a specialist when delegating a subtask. It replaces the coordinator's full conversation history with a curated, minimal set of information: exactly what the specialist needs to do its job, and nothing else. A well-formed handoff packet has four components:

|  |  |  |
| --- | --- | --- |
| **Component** | **What It Contains** | **Why It Matters** |
| **Goal** | One sentence describing what the specialist should accomplish | Anchors the specialist's task; prevents scope drift |
| **Inputs** | The specific data the specialist needs (IDs, names, parameters) | Prevents the specialist from having to infer context from surrounding noise |
| **Constraints** | Limits on the specialist's behavior (time range, scope, depth) | Keeps specialists from over-reaching or retrieving irrelevant data |
| **Output shape** | The exact structure the coordinator expects back | Makes synthesis predictable; enables the coordinator to detect missing fields |

These four components together give the specialist a complete, self-contained task description. The specialist should be able to complete its work using only the handoff packet. It should never need to ask the coordinator for clarification.

### The before: A messy coordinator handoff[#](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#The-before-A-messy-coordinator-handoff)

Here is the kind of handoff that appears in under-designed systems: the coordinator's full conversation history forwarded to each specialist.

Ace Editor

1

2

3

4

5

6

7

8

# Poorly designed handoff — full coordinator history passed to specialist

def delegate\_to\_financial\_specialist(coordinator\_messages: list, company: str) -> str:

specialist\_prompt = (

f"Here is the full context of our investigation so far:\n\n"

f"{format\_messages(coordinator\_messages)}\n\n"

f"Based on all of the above, please analyze {company}'s financial health."

)

return run\_specialist(FINANCIAL\_SPECIALIST\_SYSTEM, specialist\_prompt)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A poorly designed handoff. The specialist receives the coordinator’s full message history, every prior exchange, every other specialist’s result, and every piece of coordinator reasoning before receiving their actual task.

- **Lines 3–6:** The specialist prompt is built by serializing the entire `coordinator_messages` list. This includes the user's original request, the coordinator's decomposition reasoning, results from any specialists that already ran, and any coordinator-internal deliberation. The actual task instruction (“analyze financial health”) is a single appended line after all of this.

The problems this creates are direct:

- The specialist's input token count is the size of the coordinator's full history, not just the financial task.
- Irrelevant content, such as another specialist's legal analysis or the original user phrasing, introduces noise into financial reasoning.
- If a prior specialist's result contains a dollar figure that conflicts with the financial data, the financial specialist may factor it in and produce a confused synthesis.
- The coordinator cannot predict what shape the financial specialist will return because the task description is vague.

### The after: A scoped handoff packet[#](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#The-after-A-scoped-handoff-packet)

Here is the same delegation rewritten with a structured handoff:

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

from dataclasses import dataclass

@dataclass

class HandoffPacket:

goal: str

inputs: dict

constraints: dict

output\_shape: dict

def build\_financial\_handoff(company: str, fiscal\_year: int) -> HandoffPacket:

return HandoffPacket(

goal=(

"Assess the financial health of the target company for acquisition due diligence. "

"Focus on solvency, growth trajectory, and near-term debt obligations."

),

inputs={

"company\_name": company,

"fiscal\_year": fiscal\_year,

"currency": "USD"

},

constraints={

"time\_range": f"{fiscal\_year - 2} to {fiscal\_year}",

"data\_sources": ["financial\_statements", "credit\_ratings", "debt\_schedule"],

"depth": "summary — no raw data dumps"

},

output\_shape={

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A structured HandoffPacket dataclass. Each field is explicit and typed. The coordinator builds one packet per specialist; each packet is self-contained.

- **Lines 3–8:** The `HandoffPacket` dataclass makes the four components concrete. Every handoff has exactly these four fields: goal, inputs, constraints, and output shape. The coordinator cannot accidentally omit one.
- **Lines 12–15:** The goal is one focused statement. It names the purpose (financial health), the use case (acquisition due diligence), and the priority areas (solvency, growth, debt). The specialist uses this to calibrate how deep to go without the coordinator specifying every step.
- **Lines 16–20:** `inputs` contains only the parameters needed to execute the lookups: company name, fiscal year, and currency. The specialist makes no assumptions about these values; they are provided explicitly.
- **Lines 21–25:** `constraints` bound the specialist's behavior. The `time_range` prevents the specialist from pulling data outside the relevant window. `data_sources` names the permitted tools. `depth` says “summary” to prevent the specialist from returning full financial statement dumps that would overwhelm the coordinator's synthesis step.
- **Lines 26–31:** `output_shape` tells the specialist exactly what to return. Each field name is paired with a description of its type and content. The `sources` field is new; it asks the specialist to record where each piece of data came from. This enables the coordinator to resolve conflicts by provenance.

Now converting the packet to a specialist prompt:

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

import json

def packet\_to\_prompt(packet: HandoffPacket) -> str:

return f"""

Goal: {packet.goal}

Inputs:

{json.dumps(packet.inputs, indent=2)}

Constraints:

{json.dumps(packet.constraints, indent=2)}

Required output fields (return as JSON):

{json.dumps(packet.output\_shape, indent=2)}

Return only the JSON object. Do not include commentary outside the JSON.

"""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A function that converts a HandoffPacket into a formatted specialist prompt. The output constraint at the end ensures the specialist returns a parseable structure.

- **Lines 3–16:** Each section of the packet maps directly to a labeled block in the prompt. The specialist reads goal, inputs, constraints, and output shape in that order, which is a natural sequence from “why am I doing this” to “what exactly do I return.”
- **Line 17:** The final instruction tells Claude to return only JSON. Combined with the `output_shape` definition above, this makes the specialist's response predictable enough for the coordinator to parse without brittle string matching.

### Information provenance: Why sources must travel with results[#](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Information-provenance-Why-sources-must-travel-with-results)

When specialists return results, each data point should carry its source. The coordinator synthesizes results from multiple specialists, and when two specialists return conflicting values, the coordinator needs a way to decide which to trust.

Source type is the deciding signal. A value retrieved directly from a verified financial database is more reliable than a value extracted from a PDF report. A court record from a government registry is more reliable than a mention in a news article. Here is an example of what the financial specialist's result looks like when it includes provenance:

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

financial\_result = {

"key\_metrics": {

"revenue\_2025": "$142M",

"gross\_margin": "61%",

"debt\_to\_equity": "0.43",

"cash\_position": "$18M"

},

"risk\_flags": [

"Debt maturity spike in Q3 2026 — $24M due within 18 months"

],

"data\_gaps": [

"Profitability breakdown by product line — requires premium data subscription"

],

"sources": [

"financial\_statements: SEC EDGAR filing (verified)",

"credit\_ratings: Moody's API (verified)",

"debt\_schedule: Annual report PDF page 44 (extracted)"

]

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A financial specialist result with provenance included. Each source is labeled with its type: verified (directly from authoritative API) or extracted (parsed from a document). The coordinator uses these labels when results conflict.

- **Lines 2–7:** `key_metrics` contains the four requested values. No extra fields and no raw data dumps.
- **Lines 8–10:** `risk_flags` contains exactly one finding. The flag is specific: the amount, the timeline, and the nature of the risk.
- **Lines 11–13:** `data_gaps` names what was requested but not retrieved and includes the reason. The coordinator reads this and knows the analysis is incomplete in a specific, named way.
- **Lines 14–18:** `sources` lists each data source used and its type. `(verified)` means the data came directly from an authoritative API. `(extracted)` means it was parsed from a document and may have extraction errors. If the legal specialist’s result contradicts the debt figure, the coordinator compares source types to decide which to trust.

The coordinator’s synthesis step reads `sources` before resolving conflicts:

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

def resolve\_conflict(value\_a: str, source\_a: str, value\_b: str, source\_b: str) -> str:

verified\_types = {"SEC EDGAR filing", "Moody's API", "government registry"}

a\_is\_verified = any(t in source\_a for t in verified\_types)

b\_is\_verified = any(t in source\_b for t in verified\_types)

if a\_is\_verified and not b\_is\_verified:

return value\_a

if b\_is\_verified and not a\_is\_verified:

return value\_b

return f"CONFLICT: {value\_a} ({source\_a}) vs {value\_b} ({source\_b}) — requires human review"

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A simple provenance-based conflict resolver. Verified sources win over extracted sources. When both have equal provenance quality, the conflict is escalated to human review rather than resolved by averaging or guessing.

- **Lines 2–3:** The resolver checks each source against a set of known verified source types. This is a deterministic check, and it does not ask Claude to judge which source seems more reliable.
- **Lines 5–8:** If one source is verified and the other is not, the verified value wins unconditionally.
- **Line 9:** When both are verified, or both are extracted (equal provenance quality), the conflict is surfaced explicitly rather than resolved by averaging or choosing arbitrarily. Averaging two conflicting financial figures is statistically unsound, so the coordinator reports the conflict and routes it to human review.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Complete-code)

We bring the `HandoffPacket` dataclass, the prompt formatter, a sample specialist result with provenance, and the conflict resolver from this lesson into one runnable file. No API key is required. When you run it, you see exactly what a coordinator sends to a specialist, and you can watch two competing values from different source types get resolved.

Python

```
import json

from dataclasses import dataclass

@dataclass

class HandoffPacket:

goal:         str

inputs:       dict

constraints:  dict

output_shape: dict

def build_financial_handoff(company: str, fiscal_year: int) -> HandoffPacket:

return HandoffPacket(

goal=(

"Assess the financial health of the target company for acquisition due diligence. "

"Focus on solvency, growth trajectory, and near-term debt obligations."

),

inputs={"company_name": company, "fiscal_year": fiscal_year, "currency": "USD"},

constraints={

"time_range":   f"{fiscal_year - 2} to {fiscal_year}",

"data_sources": ["financial_statements", "credit_ratings", "debt_schedule"],

"depth":        "summary, no raw data dumps"

},

output_shape={

"key_metrics": "dict — revenue, gross_margin, debt_to_equity, cash_position",

"risk_flags":  "list[str] — any financial red flags identified",

"data_gaps":   "list[str] — metrics that could not be retrieved and why",

"sources":     "list[str] — data sources used and their type (verified/extracted)"

}

)

def packet_to_prompt(packet: HandoffPacket) -> str:

return (

f"Goal: {packet.goal}\n\n"

f"Inputs:\n{json.dumps(packet.inputs, indent=2)}\n\n"

f"Constraints:\n{json.dumps(packet.constraints, indent=2)}\n\n"

f"Required output fields (return as JSON):\n{json.dumps(packet.output_shape, indent=2)}\n\n"

"Return only the JSON object. Do not include commentary outside the JSON."

)

def resolve_conflict(value_a: str, source_a: str, value_b: str, source_b: str) -> str:

verified_types = {"SEC EDGAR filing", "Moody's API", "government registry"}

a_is_verified  = any(t in source_a for t in verified_types)

b_is_verified  = any(t in source_b for t in verified_types)

if a_is_verified and not b_is_verified:

return value_a

if b_is_verified and not a_is_verified:

return value_b

return (f"CONFLICT: {value_a} ({source_a}) vs {value_b} ({source_b})"

" — requires human review")

SAMPLE_FINANCIAL_RESULT = {

"key_metrics": {"revenue_2025": "$142M", "gross_margin": "61%",

"debt_to_equity": "0.43", "cash_position": "$18M"},

"risk_flags":  ["Debt maturity spike in Q3 2026: $24M due within 18 months"],

"data_gaps":   ["Profitability breakdown by product line — requires premium data subscription"],

"sources":     ["financial_statements: SEC EDGAR filing (verified)",

"credit_ratings: Moody's API (verified)",

"debt_schedule: Annual report PDF page 44 (extracted)"]

}

if __name__ == "__main__":

packet = build_financial_handoff("Acme Corp", 2025)

print("=== Handoff Packet Prompt ===")

print(packet_to_prompt(packet))

print("\n=== Sample Specialist Result (with provenance) ===")

print(json.dumps(SAMPLE_FINANCIAL_RESULT, indent=2))

print("\n=== Conflict Resolution: verified vs. extracted source ===")

result = resolve_conflict("$142M", "SEC EDGAR filing",

"$130M", "Annual report PDF page 44 (extracted)")

print(f"  Winner: {result}")

print("\n=== Conflict Resolution: both extracted (escalate) ===")

result = resolve_conflict("$142M", "Annual report PDF (extracted)",

"$130M", "Press release (extracted)")

print(f"  Outcome: {result}")
```

⋯

The handoff packet builder, prompt formatter, sample result, and conflict resolver in one file

The script builds a financial specialist handoff packet for “Acme Corp” (fiscal year 2025), formats it as a specialist prompt, prints a sample result with provenance labels, and then resolves two conflict cases: one where a verified source beats an extracted source, and one where both sources are extracted.

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

=== Handoff Packet Prompt ===

Goal: Assess the financial health of the target company for acquisition due diligence. ...

Inputs:

{

"company\_name": "Acme Corp",

"fiscal\_year": 2025,

"currency": "USD"

}

...

=== Conflict Resolution: verified vs. extracted source ===

Winner: $142M

=== Conflict Resolution: both extracted (escalate) ===

Outcome: CONFLICT: $142M (Annual report PDF (extracted)) vs $130M (Press release (extracted)) — requires human review

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Output

When one source is verified (SEC EDGAR) and the other is extracted (PDF), the verified value wins without any further reasoning. When both sources are extracted, the resolver cannot distinguish them by provenance quality and surfaces the conflict for human review rather than making an arbitrary choice.

## Exercise: Design the handoff[#](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Exercise-Design-the-handoff)

Read the scenario and answer the questions below.

A coordinator is running a competitive intelligence task. It needs to gather three things about a competitor: recent patent filings, key executive hires from the last 12 months, and publicly reported product roadmap items. It has three specialists: a patent analyst, a talent analyst, and a product intelligence analyst. All three tasks are independent.

Technical Quiz

1.

The talent analyst’s handoff packet needs a `constraints` field. The coordinator wants the analyst to focus only on VP-level and above hires from the last 12 months and to use only public sources (LinkedIn, press releases, company blog). Which `constraints` dict is correct?

A.

```
{"level": "VP and above", "time_range": "last 12 months", "sources": ["LinkedIn", "press releases", "company blog"]}
```

B.

```
{"level": "all executive levels", "time_range": "last 5 years", "sources": "any public source", "include_interim": True}
```

C.

```
{"task": "find executive hires", "company": competitor_name}
```

D.

```
{"confirmed": True, "max_tokens": 1024}
```

---

1 / 3

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Whats-next)

In the next lesson, we run parallel specialists, collect their results, and practice the synthesis step: merging findings, resolving conflicts by provenance, and treating partial failures as explicit signals rather than clean results.

Coordinator and Specialist Roles

Parallel Work and Result Synthesis

Ask

[What the handoff packet is](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#What-the-handoff-packet-is)

[The before: A messy coordinator handoff](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#The-before-A-messy-coordinator-handoff)

[The after: A scoped handoff packet](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#The-after-A-scoped-handoff-packet)

[Information provenance: Why sources must travel with results](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Information-provenance-Why-sources-must-travel-with-results)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Complete-code)

[Exercise: Design the handoff](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Exercise-Design-the-handoff)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/context-handoff-design#Whats-next)