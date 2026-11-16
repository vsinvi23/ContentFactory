# Designing_Reliable_Claude_Systems_with_End-to-End_Audits

Source: https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# End-to-End System Design and Reliability Audit

Explore how to design and audit Claude-powered AI systems focusing on escalation strategies, partial failure recovery, provenance tracking, and conflict resolution. Learn to create specialist-coordinator architectures, manage batch workflows, and produce traceable outputs for compliance and reliability.

We'll cover the following...

- [The scenario brief](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#The-scenario-brief)
- [Step 1: Choose the architecture shape](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-1-Choose-the-architecture-shape)
- [Step 2: Design the specialist agents](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-2-Design-the-specialist-agents)
- [Step 3: Design the tools](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-3-Design-the-tools)
- [Step 4: Design conflict resolution and escalation](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-4-Design-conflict-resolution-and-escalation)
- [Step 5: Batch processing and context management](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-5-Batch-processing-and-context-management)
- [Step 6: Provenance and the underwriter packet](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-6-Provenance-and-the-underwriter-packet)
- [Step 7: Quality metrics](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-7-Quality-metrics)
- [The architecture sketch](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#The-architecture-sketch)
- [Self-evaluation checklist](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Self-evaluation-checklist)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Whats-next)

The scenario studio presents a realistic engineering brief, the kind of problem that appears in a certification exam question or a real architectural review. The goal is not to find the one correct answer, but to demonstrate that every major design decision can be justified using the patterns from this course: where guardrails belong, when to escalate, how to handle partial failures, what provenance to attach, and how to measure quality. After working through the scenario and the architecture, the self-evaluation checklist at the end of this lesson gives you a structured way to audit any Claude-powered System Design.

## The scenario brief[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#The-scenario-brief)

The following brief captures the organizational context, current state, stakeholder requirements, and operating constraints that the architecture must address. Read through it completely before moving to Step 1.

- **Organization:** A mid-size commercial lending company processes 400–600 loan application packages per month. Each package is a set of documents: income statements, tax returns, bank statements, property appraisals, and a cover letter from the applicant.
- **Current state:** A team of five underwriters reviews each package manually. Each underwriter takes three to four hours per package. The backlog grows during peak season. The organization wants to automate the initial extraction and risk-flagging stage to reduce the time each underwriter spends on routine data gathering while keeping humans responsible for all credit decisions.
- **Requirements from stakeholders:**

  - Extract structured data from each document type: income figures, asset values, liability amounts, employment status, and property details.
  - Flag risk indicators: income-to-debt ratio above the threshold, income source not verifiable from the documents, appraisal date more than 90 days old, and missing required documents.
  - Escalate any package where extraction confidence is low, where two documents provide conflicting values for the same field, or where a required document is absent.
  - Produce a structured summary packet for the underwriter that shows all extracted fields, their confidence levels, their source documents, and any risk flags, with enough provenance that the underwriter can verify any value without rereading the full package.
  - Measure extraction quality by document type and by field, not just overall.
  - All credit decisions remain with human underwriters; the system produces the extraction packet only.
- **Constraints:**

  - Packages arrive overnight in batches; a four-hour turnaround is acceptable.
  - Some document types (handwritten income supplements and nonstandard appraisal forms) are harder to extract reliably.
  - The company is subject to fair lending regulations: every extracted value must be traceable to its source document.

## Step 1: Choose the architecture shape[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-1-Choose-the-architecture-shape)

The first decision is between a single-agent pipeline and a multi-agent coordinator-specialist system.

- **Against a single agent:** Each document type requires different extraction logic. A single agent that processes all document types in one pass will apply a generic prompt to specialized cases. An income statement and a bank statement are structurally different; a prompt optimized for one will underperform on the other. A single agent also provides no natural place to apply document-type-specific validators.
- **For a coordinator + specialists:** A coordinator receives the full package manifest and delegates each document to the appropriate specialist. Each specialist has a focused system prompt, a document-type-specific schema, and its own validator. The coordinator synthesizes findings, resolves conflicts using provenance, and produces the final packet. This matches the pattern from Chapter 4: specialists have bounded scope, and coordinators synthesize.
- **Decision:** Use a coordinator + specialist architecture. The coordinator handles routing, conflict resolution, escalation decisions, and packet assembly. Specialist agents handle extraction for: (1) income statements, (2) tax returns, (3) bank statements, (4) property appraisals, and (5) cover letters.

## Step 2: Design the specialist agents[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-2-Design-the-specialist-agents)

Each specialist agent is a single-purpose extraction unit. Its design follows the tool and prompt patterns from Chapters 5 and 6.

**System prompt structure for each specialist:**

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

You are a [document\_type] extraction specialist for commercial loan underwriting.

=== EXTRACTION TARGETS ===

[Field list with descriptions, constraints, and "do not extract" guidance]

=== END EXTRACTION TARGETS ===

For each field, return:

- "value": the extracted text or number, verbatim from the document

- "confidence": "high", "medium", or "low"

- "source\_passage": the exact sentence or number you extracted the value from

Return a JSON object. If a field is not present in the document, return

{"value": null, "confidence": "low", "source\_passage": "not found in document"}.

Do not estimate or infer values that are not explicitly stated.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

System prompt structure for each specialist

Each specialist uses:

- A document-type-specific schema with semantic validation, not just structural validation.
- A retry loop with field-specific feedback (Chapter 8 pattern).
- `PartialResult` output, even on success, so the coordinator always receives a uniform object (Chapter 10 pattern).

**Semantic validators per document type:**

|  |  |
| --- | --- |
| **Document Type** | **Semantic Rules** |
| Income statement | Monthly income > 0; period (month/year) is present and not in the future |
| Tax return | Adjusted gross income matches line references; filing year is present; signatures field noted |
| Bank statement | Balance is numeric; statement period is consecutive months; ending balance > 0 or flagged if negative |
| Property appraisal | Appraisal date not more than 90 days before package receipt date; appraiser license number present |
| Cover letter | Loan purpose stated; applicant name matches other documents |

## Step 3: Design the tools[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-3-Design-the-tools)

Each specialist has access to a focused set of tools. Shared tools live at the coordinator level. The tool design follows Chapter 5 patterns: structured errors, explicit “do not use when” guidance, and scoped access.

**Specialist-level tools:**

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

DOCUMENT\_FETCH\_TOOL = {

"name": "fetch\_document\_section",

"description": (

"Retrieve a specific section of the current document by section label. "

"Use this when you need to re-read a specific part of the document for "

"extraction verification. "

"Do not use this tool to retrieve documents other than the one assigned "

"to you for this extraction task."

),

"input\_schema": {

"type": "object",

"properties": {

"section\_label": {"type": "string"}

},

"required": ["section\_label"]

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

**Coordinator-level tools:**

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

ESCALATE\_TOOL = {

"name": "escalate\_for\_review",

"description": (

"Halt processing and surface an escalation packet to a human underwriter. "

"Use this tool when: (1) a required document is absent from the package; "

"(2) two documents provide conflicting values for the same field and the "

"conflict cannot be resolved by provenance rules; "

"(3) extraction confidence for a required field is 'low' after retry. "

"Do not use this tool for single-document extraction errors that the "

"specialist retry loop should handle."

),

...

}

PACKAGE\_COMPLETE\_TOOL = {

"name": "mark\_package\_complete",

"description": (

"Signal that all extraction is complete and the underwriter packet is ready. "

"Call this only after all specialists have returned results, all conflicts "

"have been resolved or escalated, and the packet has been assembled. "

"Do not call this tool if any required field is missing or unresolved."

),

...

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

**Access control:** `dispatch_tool` guards enforce that specialists cannot call coordinator tools, and the coordinator cannot call document-level fetch tools directly. Tool access is scoped by agent role and enforced programmatically.

## Step 4: Design conflict resolution and escalation[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-4-Design-conflict-resolution-and-escalation)

The coordinator receives `PartialResult` objects from all five specialists. For each field that appears in more than one document, it applies the provenance-based conflict resolver from Chapter 9.

**Conflict resolution order:** confidence → authority → recency.

Ace Editor

1

2

3

4

5

6

7

AUTHORITY\_RANK = {

"income\_statement\_specialist": 5,

"tax\_return\_specialist": 4,

"bank\_statement\_specialist": 3,

"appraisal\_specialist": 4,

"cover\_letter\_specialist": 1,

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Income figures that appear in both the income statement and the tax return: The income statement specialist has higher authority for current income, and the tax return specialist has higher authority for annual figures. The coordinator resolves by field. The authority table is keyed by specialist role, so each document type's natural authority for each field type can be expressed.

**Escalation conditions, such as tool description exclusions and explicit triggers:**

|  |  |
| --- | --- |
| **Condition** | **Action** |
| Required document absent from package | Escalate immediately before specialist processing |
| Same field, two documents, values differ >5% after authority resolution | Escalate with both values and source passages |
| Required field, all specialist extractions at `"low"` confidence | Escalate after retry |
| Appraisal date > 90 days old | Flag as risk indicator in packet (not escalation, the underwriter decides) |
| Income-to-debt ratio above threshold | Flag as risk indicator in packet |

The distinction between escalation and risk flagging is important: Escalation halts the pipeline and requires human action before the packet can be assembled. Risk flagging records a finding in the packet and allows processing to continue; the human makes the credit decision, not the pipeline.

## Step 5: Batch processing and context management[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-5-Batch-processing-and-context-management)

- **Batch processing:** 400–600 packages per month with a four-hour turnaround and no real-time latency requirement. This is the definition of the batch processing use case from Chapter 8. The pipeline submits each document within a package as a batch request, retrieves results, validates them, and runs a second batch for any documents that failed or produced low-confidence output.
- **Retry strategy:** A two-pass batch model. The first batch processes all documents in a package. The second batch resubmits only the documents that failed validation or produced confidence below the threshold. Documents that fail the second pass trigger escalation or data-gap recording.
- **Context management within the coordinator:** Each package is a separate coordinator session. The coordinator's system prompt includes a case facts block:

Ace Editor

1

2

3

4

5

6

7

=== PACKAGE FACTS (do not rephrase or approximate) ===

Package ID: PKG-2024-10042

Applicant name: Vasquez, Marina R.

Receipt date: 2024-11-14

Required docs: income\_statement, tax\_return\_2022, tax\_return\_2023,

bank\_statement\_3mo, property\_appraisal, cover\_letter

=== END PACKAGE FACTS ===

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A scratchpad is maintained per package: which specialists have returned results, which fields are resolved, which are in conflict, and which are awaiting retry. The coordinator session is bound to the package; it does not accumulate across packages, so context pressure is manageable within a four-hour batch window.

## Step 6: Provenance and the underwriter packet[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-6-Provenance-and-the-underwriter-packet)

The final underwriter packet is the coordinator's primary output. Every field in the packet must carry provenance: source document name, source passage, extraction confidence, and specialist role.

A packet entry:

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

{

"field": "annual\_income",

"value": "$127,400",

"provenance": {

"source\_document": "income\_statement\_2024.pdf",

"source\_passage": "Annual gross compensation: $127,400",

"confidence": "high",

"specialist\_role": "income\_statement\_specialist",

"extraction\_time": "2024-11-14T03:22:10Z"

},

"conflict\_note": null,

"risk\_flags": []

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

When a conflict is resolved by provenance, `conflict_note` records both values and which one was chosen:

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

{

"field": "annual\_income",

"value": "$127,400",

"provenance": { ... },

"conflict\_note": {

"alternate\_value": "$118,000",

"alternate\_source": "cover\_letter\_specialist",

"resolution\_method": "authority — income\_statement\_specialist outranks cover\_letter\_specialist",

"alternate\_passage": "My current annual income is approximately $118,000."

},

"risk\_flags": []

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The underwriter reads the packet and can verify any value by reading the cited passage without reprocessing the documents. Fair lending compliance is satisfied: every extracted value is traceable to its source, and conflicts are documented rather than silently resolved.

## Step 7: Quality metrics[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-7-Quality-metrics)

The metrics layer from Chapter 8 applies at two levels:

- **Per-field accuracy:** Ground truth is established from a sample of packages that underwriters review in detail. Field-level accuracy is computed separately for each extraction target across each document type.
- **Workflow stage metrics per document type:**

|  |  |
| --- | --- |
| **Metric** | **What It Surfaces** |
| First-pass success rate by document type | Whether handwritten income supplements need a separate specialist |
| Retry rate by field | Which fields fail validation most often |
| Second-pass success rate | Whether retry feedback is specific enough |
| Escalation rate | How often is human intervention required beyond flagging |

A healthy pipeline for this scenario is first-pass success above 90% for standard digital documents, with a higher escalation rate (10–15%) accepted for nonstandard document types. The escalation rate for standard documents should be below 3%.

## The architecture sketch[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#The-architecture-sketch)

A one-page description of the assembled system:

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

LOAN PACKAGE EXTRACTION PIPELINE

Ingestion

- Packages arrive as PDF bundles, classified by document type

- Coordinator session opens with PACKAGE FACTS block + required doc list

Specialist Agents (one per document type)

- Focused system prompt + document-type schema

- Semantic validator (domain rules, not just schema)

- Retry loop with field-specific feedback (max 2 retries)

- PartialResult output: fields + failure\_type + recovery\_hint

Coordinator

- Routes each document to the correct specialist

- Collects PartialResults; applies provenance-based conflict resolver

- Routes by failure\_type: access\_failure → escalate,

empty\_result → data\_gap, partial\_completion → retry specialist

- Flags risk indicators in packet (income ratio, appraisal age)

- Escalates on: absent required document, unresolvable conflict,

required field at low confidence after retry

- Assembles underwriter packet with full provenance per field

Processing Mode

- Batch (Message Batches API) — 4h turnaround acceptable

- Two-pass: first batch all docs, second batch failures only

Metrics

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Self-evaluation checklist[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Self-evaluation-checklist)

Use this checklist to evaluate any Claude-powered System Design. Each item maps to a specific course pattern. A *no* answer on any item identifies a gap to address before the system is production-ready.

**Agent loop:**

- Does the loop terminate on `stop_reason`, not on Claude’s output text?
- Does every tool call receive a `tool_result` block in the next turn?
- Is there a maximum retry count on every retry loop, with a defined behavior on exhaustion?

**Tool design:**

- Does every tool return a structured error type, not a free-text error string?
- Does every tool description include explicit *do not use when* guidance?
- Are tool access boundaries enforced programmatically (not only in the prompt)?

**Prompt and schema design:**

- Are classification and extraction criteria measurable and observable, not qualitative?
- Does the system prompt place stable facts in a delimited case facts block with a verbatim instruction?
- Are per-request documents in the user message rather than the system prompt?
- Does retry feedback name the field, the extracted value, the violated rule, and a directive?
- Does semantic validation run after schema validation?

**Context management:**

- Are stable facts anchored at the top of the context and reinforced on summarization?
- Is there a defined context pressure threshold that triggers summarization or delegation?
- Is there a scratchpad or equivalent state record that lists completed steps?

**Provenance and conflict resolution:**

- Does every extracted finding carry a source, confidence, timestamp, and agent role?
- Is provenance preserved through every synthesis or coordinator step?
- Does the conflict resolver apply a defined tiebreaker order?
- Are unresolvable conflicts escalated rather than silently resolved?

**Escalation and partial failures:**

- Are the four escalation conditions defined and encoded in the tool description?
- Does the escalation packet include a case reference, reason, evidence, decision required, and next step?
- Are partial failure types classified explicitly (access failure, empty result, stale data, partial completion)?
- Are access failures and empty results routed differently from partial completions?

**Metrics:**

- Is accuracy stratified by document type and by field?
- Are workflow stage metrics tracked: first-pass rate, retry rate, second-pass rate, escalation rate?
- Is confidence calibration verified: does accuracy decrease monotonically from high to medium to low?

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Whats-next)

In the final lesson, we close the course with an integrated assessment quiz that combines agent loops, tools, prompts, context management, provenance, escalation, and automation choices across new scenario stems, in the same format as the certification exam scenarios.

Anti-Pattern Reference

Reliability and Capstone Assessment Quiz

Ask

[The scenario brief](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#The-scenario-brief)

[Step 1: Choose the architecture shape](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-1-Choose-the-architecture-shape)

[Step 2: Design the specialist agents](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-2-Design-the-specialist-agents)

[Step 3: Design the tools](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-3-Design-the-tools)

[Step 4: Design conflict resolution and escalation](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-4-Design-conflict-resolution-and-escalation)

[Step 5: Batch processing and context management](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-5-Batch-processing-and-context-management)

[Step 6: Provenance and the underwriter packet](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-6-Provenance-and-the-underwriter-packet)

[Step 7: Quality metrics](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Step-7-Quality-metrics)

[The architecture sketch](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#The-architecture-sketch)

[Self-evaluation checklist](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Self-evaluation-checklist)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/end-to-end-system-design-and-reliability-audit#Whats-next)