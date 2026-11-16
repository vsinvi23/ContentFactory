# Understanding_Information_Provenance_for_Reliable_AI_Context_Management

Source: https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Information Provenance

Explore the importance of provenance annotation in AI workflows to track source, confidence, timestamp, and agent role for each finding. Understand how to implement provenance-annotated structures, resolve conflicts between competing outputs, and maintain provenance through multi-agent pipelines to ensure reliable, auditable results in long-running sessions.

We'll cover the following...

- [Why provenance matters](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Why-provenance-matters)
- [The four provenance fields](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#The-four-provenance-fields)
- [Implementing a provenance-annotated finding](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Implementing-a-provenance-annotated-finding)
- [Recording provenance in the extraction output](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Recording-provenance-in-the-extraction-output)
- [Resolving conflicts between competing findings](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Resolving-conflicts-between-competing-findings)
- [Propagating provenance through a pipeline](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Propagating-provenance-through-a-pipeline)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Complete-code)
- [Exercise: Apply provenance reasoning](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Exercise-Apply-provenance-reasoning)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Whats-next)

Two agents investigate the same contract clause and reach different conclusions. One classifies it as an indemnification clause; the other classifies it as a limitation of liability. Both are plausible. Both used the same source document. Without provenance, a record of which agent produced which finding, from which passage, with what confidence, and at what point in the session, there is no principled way to decide which output to trust. The session has two answers and no mechanism to choose between them. Provenance annotation is the mechanism that enables conflict resolution, and it is the difference between a system that produces outputs and one that produces auditable outputs. By the end of this lesson, we will be able to:

- Explain why provenance annotation is necessary for long-running and multi-agent workflows
- Define the four provenance fields: source, confidence, timestamp, and agent role
- Implement a provenance-annotated finding structure and apply it to the extraction output
- Apply a conflict resolution strategy that uses provenance to choose between competing findings

## Why provenance matters[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Why-provenance-matters)

In a single-turn extraction, every output is produced by the same model call using the same input. Provenance is trivially traceable. In a multi-turn session or a multi-agent pipeline, the origin of each finding is no longer obvious:

- A coordinator agent summarizes findings from three specialist agents. The summary is cleaner than the original outputs, but it has no record of which specialist produced which claim.
- A session runs for 40 turns. A finding from turn six is referenced in turn 38. The turn-six source document is no longer in the context.
- Two extraction passes over the same document produce different values for the same field.

In each case, the downstream consumer of the output has no way to evaluate which finding to trust without knowing where it came from. Provenance annotation solves this by attaching origin metadata to every finding at the point it is generated.

Provenance is not about blame; it is about resolution. When two findings conflict, provenance provides the information needed to decide:

- Which source document was each finding drawn from?
- How confident was the extracting agent?
- Which agent performed the extraction, and what is its scope of authority?
- Was one finding produced before a corrective action was taken?

## The four provenance fields[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#The-four-provenance-fields)

A minimal provenance record has four fields:

|  |  |  |
| --- | --- | --- |
| **Field** | **What It Records** | **Why It Matters** |
| `source` | Document name, URL, passage identifier, or tool name that produced the value | Enables the finding to be traced back to its origin and verified independently |
| `confidence` | The extracting agent's stated confidence: `"high"`, `"medium"`, or `"low"` | Enables downstream systems to weight findings and flag low-confidence outputs for review |
| `timestamp` | ISO 8601 datetime when the finding was produced | Enables recency comparison when the same field is extracted at different points in the session |
| `agent_role` | The role or identity of the agent that produced the finding | Enables authority comparison: a specialist agent's finding on its domain outweighs a generalist's finding on the same topic |

These four fields are the minimum. Specific workflows may add fields such as `extraction_pass` (first pass vs. retry), `reviewer` (human or automated validator that checked the finding), or `supersedes` (the ID of a prior finding that this one replaces).

## Implementing a provenance-annotated finding[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Implementing-a-provenance-annotated-finding)

A finding combines the extracted value with its provenance record. Keeping them together as a single object prevents the value from being separated from its metadata as it passes through the pipeline:

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

from dataclasses import dataclass, field

from datetime import datetime, timezone

from typing import Optional

@dataclass

class Provenance:

source: str

confidence: str

timestamp: str

agent\_role: str

@dataclass

class Finding:

field\_name: str

value: str

provenance: Provenance

finding\_id: str = ""

def make\_finding(

field\_name: str,

value: str,

source: str,

confidence: str,

agent\_role: str,

finding\_id: str = ""

) -> Finding:

ts = datetime.now(timezone.utc).isoformat()

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A Finding dataclass that bundles the extracted value with a Provenance record. make\_finding generates the timestamp at creation time so the record is always current. finding\_id is optional but useful when findings reference each other in conflict resolution.

- **Lines 5–9:** `Provenance` is a separate dataclass rather than inline fields on `Finding`. Keeping provenance as a nested object makes it easy to pass the provenance block separately when needed (for example, to a conflict resolver that receives only the metadata, not the values).
- **Lines 11–14:** `Finding` holds the field name, the extracted string value, and the provenance record. Storing `field_name` on the finding allows a list of findings to be self-describing; each finding knows which field it represents.
- **Lines 24–26:** The timestamp is generated inside `make_finding` using `datetime.now(timezone.utc)` to ensure UTC. Consistent timezone handling matters when findings from different agents in different time zones are compared by recency.

## Recording provenance in the extraction output[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Recording-provenance-in-the-extraction-output)

When Claude extracts structured output from a document, each field value can be wrapped in a provenance-annotated finding rather than returned as a plain value. The system prompt instructs Claude to include provenance fields in its JSON output:

Ace Editor

1

2

3

4

5

6

7

Extract the following fields from the contract. For each field, return:

- "value": the extracted text, verbatim from the document

- "confidence": "high", "medium", or "low"

- "source\_passage": the exact sentence or clause you extracted the value from

Return a JSON object where each key is a field name and each value is

{"value": "...", "confidence": "...", "source\_passage": "..."}.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

An extraction result following this prompt:

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

"clause\_type": {

"value": "indemnification",

"confidence": "high",

"source\_passage": "Party A shall indemnify and hold harmless Party B from any claims..."

},

"effective\_date": {

"value": "2024-09-01",

"confidence": "high",

"source\_passage": "This Agreement is effective as of September 1, 2024."

},

"liability\_cap": {

"value": "USD 500,000",

"confidence": "medium",

"source\_passage": "in no event shall either party's liability exceed five hundred thousand dollars"

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

An extraction result where each field carries its own confidence and source passage. The source\_passage field is the provenance equivalent of a citation: it tells a reviewer exactly where in the document the value was found.

The `source_passage` field serves double duty: it allows a reviewer to verify the extraction manually, and it allows a conflict resolver to compare two competing extractions by examining whether they drew from the same passage or different ones.

## Resolving conflicts between competing findings[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Resolving-conflicts-between-competing-findings)

Conflict resolution applies when two findings for the same field carry different values. The resolution strategy uses provenance to choose rather than defaulting to the most recent or the first.

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

from typing import Optional

CONFIDENCE\_RANK = {"high": 3, "medium": 2, "low": 1}

AUTHORITY\_RANK = {

"contract\_specialist": 4,

"legal\_reviewer": 3,

"generalist\_extractor": 2,

"fallback\_extractor": 1,

}

def resolve\_conflict(a: Finding, b: Finding) -> Finding:

conf\_a = CONFIDENCE\_RANK.get(a.provenance.confidence, 0)

conf\_b = CONFIDENCE\_RANK.get(b.provenance.confidence, 0)

if conf\_a != conf\_b:

return a if conf\_a > conf\_b else b

auth\_a = AUTHORITY\_RANK.get(a.provenance.agent\_role, 0)

auth\_b = AUTHORITY\_RANK.get(b.provenance.agent\_role, 0)

if auth\_a != auth\_b:

return a if auth\_a > auth\_b else b

return a if a.provenance.timestamp > b.provenance.timestamp else b

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A conflict resolver that applies three tiebreakers in order: confidence rank, then agent authority rank, then recency. Each tiebreaker falls through to the next if the two findings are equal on that dimension.

- **Lines 3–10:** `CONFIDENCE_RANK` and `AUTHORITY_RANK` are defined as module-level dictionaries rather than inside the function. This makes the ranking policy inspectable and modifiable without changing the resolver logic.
- **Lines 17–18:** Confidence is checked first because it is the most direct signal of extraction quality. A high-confidence finding from a generalist outweighs a low-confidence finding from a specialist for the same field.
- **Lines 20–22:** Agent authority is checked second. If two findings have the same confidence, the one from the agent with domain expertise takes precedence. A `contract_specialist` outweighs a `generalist_extractor` on contract clause classification.
- **Lines 24–25:** Recency is the final tiebreaker. If two findings are equal on confidence and authority, the more recent one is preferred. Recency assumes that later extractions had more context or benefited from corrections applied earlier in the session.

## Propagating provenance through a pipeline[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Propagating-provenance-through-a-pipeline)

Provenance is only useful if it is preserved as findings pass between pipeline stages. When a coordinator agent summarizes findings from specialist agents, the summary must carry the provenance of each underlying finding, not just the coordinator’s own metadata.

A coordinator summary that preserves provenance:

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

def summarize\_findings(findings: list[Finding]) -> str:

lines = []

for f in findings:

p = f.provenance

lines.append(

f"Field: {f.field\_name}\n"

f" Value: {f.value}\n"

f" Confidence: {p.confidence}\n"

f" Source: {p.source}\n"

f" Agent: {p.agent\_role}\n"

f" Timestamp: {p.timestamp}"

)

return "\n\n".join(lines)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A summary function that formats each finding with its full provenance block. This output is passed as the coordinator’s context for synthesis, ensuring the coordinator sees each claim alongside its origin.

When the coordinator passes this summary to Claude for synthesis, Claude can reference the source and agent for each claim in its output. A synthesis instruction that reinforces provenance:

Ace Editor

1

2

3

4

5

You are synthesizing findings from multiple specialist agents.

For each conclusion you draw, cite the field name, the agent role,

and the confidence level of the finding you are drawing from.

Do not merge findings from different sources without noting the sources separately.

If two findings conflict, report both with their provenance rather than silently choosing one.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A synthesis instruction that makes provenance part of the expected output format. “Report both with their provenance rather than silently choosing one” ensures conflicts surface in the output rather than disappearing inside a summary.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Complete-code)

We bring the `Provenance` and `Finding` dataclasses, the `make_finding` factory, the three-tier conflict resolver, and the findings summary formatter from this lesson into one runnable file. We need no API key. We create two competing findings for the same field, resolve the conflict, then print a formatted summary of a multi-agent findings list.

Python

```
from dataclasses import dataclass, field

from datetime import datetime, timezone

from typing import Optional

@dataclass

class Provenance:

source:     str

confidence: str

timestamp:  str

agent_role: str

@dataclass

class Finding:

field_name: str

value:      str

provenance: Provenance

finding_id: str = ""

def make_finding(

field_name: str,

value:      str,

source:     str,

confidence: str,

agent_role: str,

finding_id: str = ""

) -> Finding:

ts = datetime.now(timezone.utc).isoformat()

return Finding(

field_name=field_name,

value=value,

provenance=Provenance(

source=source,

confidence=confidence,

timestamp=ts,

agent_role=agent_role

),

finding_id=finding_id

)

CONFIDENCE_RANK = {"high": 3, "medium": 2, "low": 1}

AUTHORITY_RANK = {

"contract_specialist":  4,

"legal_reviewer":       3,

"generalist_extractor": 2,

"fallback_extractor":   1,

}

def resolve_conflict(a: Finding, b: Finding) -> Finding:

conf_a = CONFIDENCE_RANK.get(a.provenance.confidence, 0)

conf_b = CONFIDENCE_RANK.get(b.provenance.confidence, 0)

if conf_a != conf_b:

winner = a if conf_a > conf_b else b

print(f"  Resolved by confidence: {winner.provenance.confidence} wins")

return winner

auth_a = AUTHORITY_RANK.get(a.provenance.agent_role, 0)

auth_b = AUTHORITY_RANK.get(b.provenance.agent_role, 0)

if auth_a != auth_b:

winner = a if auth_a > auth_b else b

print(f"  Resolved by authority: {winner.provenance.agent_role} wins")

return winner

winner = a if a.provenance.timestamp > b.provenance.timestamp else b

print(f"  Resolved by recency: most recent timestamp wins")

return winner

def summarize_findings(findings: list[Finding]) -> str:

lines = []

for f in findings:

p = f.provenance

lines.append(

f"Field: {f.field_name}\n"

f"  Value:      {f.value}\n"

f"  Confidence: {p.confidence}\n"

f"  Source:     {p.source}\n"

f"  Agent:      {p.agent_role}\n"

f"  Timestamp:  {p.timestamp}"

)

return "\n\n".join(lines)

if __name__ == "__main__":

print("=== Information Provenance Demo ===\n")

finding_a = make_finding(

field_name="clause_type",

value="limitation_of_liability",

source="contract_v2.pdf, clause 4.2",

confidence="high",

agent_role="generalist_extractor",

finding_id="F-001"

)

finding_b = make_finding(

field_name="clause_type",

value="indemnification",

source="contract_v2.pdf, clause 4.2",

confidence="medium",

agent_role="contract_specialist",

finding_id="F-002"

)

print("Finding A:")

print(f"  value={finding_a.value}, confidence={finding_a.provenance.confidence}, "

f"agent={finding_a.provenance.agent_role}")

print("\nFinding B:")

print(f"  value={finding_b.value}, confidence={finding_b.provenance.confidence}, "

f"agent={finding_b.provenance.agent_role}")

print("\n=== Resolving conflict (confidence → authority → recency) ===")

winner = resolve_conflict(finding_a, finding_b)

print(f"  Winner: {winner.value} (from {winner.provenance.agent_role})")

findings = [

make_finding("clause_type",    "limitation_of_liability", "contract_v2.pdf §4.2",   "high",   "generalist_extractor"),

make_finding("effective_date", "2024-09-01",              "contract_v2.pdf §1",      "high",   "contract_specialist"),

make_finding("liability_cap",  "USD 500,000",             "contract_v2.pdf §4.2(b)", "medium", "legal_reviewer"),

]

print("\n=== Findings Summary (for coordinator synthesis) ===")

print(summarize_findings(findings))
```

⋯

The full provenance stack: dataclasses, factory, conflict resolver, and summary formatter

Finding A has `confidence=high` and Finding B has `confidence=medium`, so the resolver picks A without even checking authority. The findings summary shows all three fields with their full provenance metadata, in a format ready for a coordinator’s synthesis prompt.

**Expected output:**

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

=== Information Provenance Demo ===

Finding A:

value=limitation\_of\_liability, confidence=high, agent=generalist\_extractor

Finding B:

value=indemnification, confidence=medium, agent=contract\_specialist

=== Resolving conflict (confidence → authority → recency) ===

Resolved by confidence: high wins

Winner: limitation\_of\_liability (from generalist\_extractor)

=== Findings Summary (for coordinator synthesis) ===

Field: clause\_type

Value: limitation\_of\_liability

Confidence: high

Source: contract\_v2.pdf §4.2

Agent: generalist\_extractor

Timestamp: 2026-06-15T...

Field: effective\_date

Value: 2024-09-01

Confidence: high

Source: contract\_v2.pdf §1

Agent: contract\_specialist

Timestamp: 2026-06-15T...

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Timestamps are the actual UTC time the script runs; all other values are deterministic

To test the authority tier, change both `confidence` values to `"high"`. Now the resolver skips the confidence check and falls through to the authority comparison: `contract_specialist` (rank 4) beats `generalist_extractor` (rank 2), and the winner flips to Finding B.

## Exercise: Apply provenance reasoning[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Exercise-Apply-provenance-reasoning)

Each scenario describes a situation where provenance determines the correct action. Apply the rules from this lesson.

Technical Quiz

1.

A pipeline runs two extraction passes over the same contract. Pass 1 (agent role: `"generalist_extractor"`, confidence: `"high"`) classifies `clause_type` as `"limitation_of_liability"`. Pass 2 (agent role: `"contract_specialist"`, confidence: `"medium"`) classifies the same field as `"indemnification"`. Using the three-tiebreaker resolution order (confidence → authority → recency), which finding wins?

A.

Pass 2, because authority is checked before confidence and the specialist ranks higher

B.

Pass 2, because the specialist agent was run after the generalist and is therefore more recent

C.

Pass 1, because the generalist extractor ran first and established the baseline

D.

Pass 1, because confidence is checked first and high outranks medium

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Whats-next)

In the next lesson, we close this chapter with an assessment quiz that covers case facts, context placement, long-session health, and information provenance through scenario-based questions.

Long Session Health

Context Management Assessment Quiz

Ask

[Why provenance matters](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Why-provenance-matters)

[The four provenance fields](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#The-four-provenance-fields)

[Implementing a provenance-annotated finding](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Implementing-a-provenance-annotated-finding)

[Recording provenance in the extraction output](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Recording-provenance-in-the-extraction-output)

[Resolving conflicts between competing findings](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Resolving-conflicts-between-competing-findings)

[Propagating provenance through a pipeline](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Propagating-provenance-through-a-pipeline)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Complete-code)

[Exercise: Apply provenance reasoning](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Exercise-Apply-provenance-reasoning)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/information-provenance#Whats-next)