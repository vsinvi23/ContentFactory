# Designing_Effective_Escalation_and_Human_Review_in_AI_Systems

Source: https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Escalation and Human Review

Explore how to design escalation mechanisms that allow AI agents to signal human review when necessary. Understand the key conditions triggering escalation, how to create informative approval packets, and implement signals that pause autonomous workflows for safe human decisions. This lesson helps you differentiate appropriate escalation from costly over- or under-escalation to build more reliable AI systems.

We'll cover the following...

- [The four escalation conditions](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-four-escalation-conditions)
- [The approval packet](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-approval-packet)
- [Implementing the escalation signal](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Implementing-the-escalation-signal)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Complete-code)
- [The tool description as the escalation policy](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-tool-description-as-the-escalation-policy)
- [Over-escalation and under-escalation](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Over-escalation-and-under-escalation)
- [Exercise: Design the escalation](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Exercise-Design-the-escalation)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Whats-next)

Escalation is the mechanism by which an agent signals that it cannot, or should not, proceed autonomously. It is not a last resort triggered by catastrophic failure; it is a designed workflow stage that fires when the action ahead is beyond what the agent is authorized to decide alone. An agent that never escalates is either operating in a domain where every action is low stakes and reversible, or it is taking actions it should not. An agent that escalates well produces a structured handoff packet, a compact document that tells the human reviewer exactly what decision is needed, why the agent stopped, and what information is available to inform the decision. This lesson covers when to escalate, what the packet must contain, and how to design the escalation signal so that the workflow can resume after the reviewer acts. By the end of this lesson, we will be able to:

- Identify the four conditions that should trigger escalation
- Write an approval packet that contains the information a reviewer needs, and nothing else
- Implement an escalation signal that halts the agent loop and surfaces the packet to the reviewer
- Distinguish over-escalation from appropriate escalation and explain why both are costly

## The four escalation conditions[#](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-four-escalation-conditions)

An agent should escalate when it encounters one of four conditions. These conditions share a common property: The agent has the information needed to describe the decision, but not the authority to make it.

- **High-impact irreversible actions.** Actions that cannot be undone after execution, such as deleting records, sending external communications, submitting regulatory filings, and transferring funds, require human approval before execution, not after. The cost of an error is too high to discover only in post hoc review.
- **Policy gaps.** The agent’s instructions define the boundaries of authorized behavior. When the situation falls outside those boundaries (for example, a customer request type that the instructions do not address, a document format the schema was not designed for, or a jurisdiction not covered by the configured rules), the agent cannot safely apply the closest matching rule. Applying an approximate rule to a situation it was not designed for can produce a result that is worse than stopping.
- **Conflicting evidence.** When two sources of information produce incompatible conclusions, and the agent cannot determine which to trust using its provenance resolution rules, escalation is the correct action. Silently choosing one and discarding the other removes information that the reviewer may need.
- **Confidence below threshold.** When the agent’s stated confidence for a required field or decision falls below the system’s defined floor (for example, all three required fields extracted at `"low"` confidence), the extraction should be flagged rather than passed through as if it were reliable.

## The approval packet[#](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-approval-packet)

An approval packet is the structured output that the agent produces when it escalates. Its purpose is to give the reviewer everything they need to make a decision, and nothing they don’t. A packet that is too long forces the reviewer to reread the original source material. A packet that is too short forces the reviewer to ask follow-up questions before deciding. An approval packet has five sections:

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

=== ESCALATION PACKET ===

CASE REFERENCE

Case ID: CLM-2024-4471

Policy ref: POL-2024-0091-B

Claimant: Torres, Alejandra

ESCALATION REASON

Condition: Conflicting evidence

Summary: Pass 1 (contract\_specialist, high confidence) classified clause 4.2

as an indemnification clause. Pass 2 (legal\_reviewer, medium confidence)

classified the same clause as a limitation of liability.

The conflict resolver could not determine a winner because the

source passages cited by each agent refer to different paragraphs

of the same section.

AVAILABLE EVIDENCE

Pass 1 source passage: "Party A shall indemnify and hold harmless Party B from

and against any claims, damages, losses, and expenses..."

Pass 2 source passage: "Notwithstanding the foregoing, in no event shall either

party's aggregate liability exceed the amounts paid in the preceding twelve months."

DECISION REQUIRED

Classify clause 4.2 as one of:

(a) indemnification\_clause

(b) limitation\_of\_liability

(c) mixed — contains elements of both; document both classifications

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

An approval packet for a conflicting evidence escalation. Each section has a distinct purpose: case reference anchors the packet to a specific case; escalation reason explains why the agent stopped; available evidence gives the reviewer the raw material; decision required specifies exactly what input is needed; next step explains what the reviewer’s decision enables.

The decision section is the most important. It must be specific enough that the reviewer can answer it without reading anything outside the packet. A decision section that says “please review the contract” is not a packet; it is a request to redo the work. A decision section that says “classify as (a), (b), or (c)” is actionable in under one minute.

## Implementing the escalation signal[#](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Implementing-the-escalation-signal)

In an agent loop, escalation is implemented as a tool call that halts execution and surfaces the packet. The tool does not return a value that the agent can use to continue autonomously; it waits for human input before the loop resumes.

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

import anthropic

import json

client = anthropic.Anthropic()

ESCALATE\_TOOL = {

"name": "escalate\_for\_review",

"description": (

"Halt the current workflow and surface an approval packet to a human reviewer. "

"Use this tool when the action ahead is irreversible, when the situation is "

"outside the defined policy boundaries, when evidence conflicts and cannot be "

"resolved, or when confidence is below the required threshold. "

"Do not use this tool for routine errors or retryable failures."

),

"input\_schema": {

"type": "object",

"properties": {

"case\_reference": {"type": "string"},

"escalation\_reason": {"type": "string"},

"evidence\_summary": {"type": "string"},

"decision\_required": {"type": "string"},

"next\_step": {"type": "string"}

},

"required": [

"case\_reference",

"escalation\_reason",

"decision\_required",

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A tool definition and handler for escalation. The tool schema specifies exactly what the agent must provide in the packet. handle\_escalation formats the packet, notifies the reviewer, and blocks until a decision is returned — halting the agent loop until the human acts.

- **Lines 7–11:** The tool description is written from Claude’s perspective. It tells Claude when to call the tool and when not to. “Do not use this tool for routine errors or retryable failures” prevents the agent from escalating on validation errors that the retry loop should handle.
- **Lines 19–22:** `required` includes `case_reference`, `escalation_reason`, `decision_required`, and `next_step`, but not `evidence_summary`. Evidence is optional because some escalations (policy gaps, for example) have no competing evidence to present, only a gap to report.
- **Lines 24–33:** `handle_escalation` formats and routes the packet, then calls `wait_for_reviewer_decision`, which blocks. The agent loop cannot continue until this function returns a reviewer decision. The return value is injected back into the conversation as the tool result, allowing the agent to resume from the `next_step` using the reviewer’s input.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Complete-code)

We bring the escalation tool definition, the clause retrieval tool, the packet formatter, and the full agent loop from this lesson into one runnable file. We give Claude a task with deliberately conflicting prior classification results, one of the four escalation conditions, and watch Claude trigger the `escalate_for_review` tool and print a full five-section approval packet.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import anthropic

import json

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = anthropic.Anthropic(api_key=anthropic_api_key)

SYSTEM = """You are a contract review agent. Review clauses and extract structured information.

When you encounter conflicting evidence, a policy gap, low confidence after retries,

or an irreversible action requiring approval, use the escalate_for_review tool."""

ESCALATE_TOOL = {

"name": "escalate_for_review",

"description": (

"Halt the current workflow and surface an approval packet to a human reviewer. "

"Use this tool when the action ahead is irreversible, when the situation is "

"outside the defined policy boundaries, when evidence conflicts and cannot be "

"resolved, or when confidence is below the required threshold. "

"Do not use this tool for routine errors or retryable failures."

),

"input_schema": {

"type": "object",

"properties": {

"case_reference":    {"type": "string"},

"escalation_reason": {"type": "string"},

"evidence_summary":  {"type": "string"},

"decision_required": {"type": "string"},

"next_step":         {"type": "string"}

},

"required": [

"case_reference",

"escalation_reason",

"decision_required",

"next_step"

]

}

}

GET_CLAUSE_TOOL = {

"name": "get_clause_text",

"description": "Retrieve the full text of a specific clause from the contract by clause number.",

"input_schema": {

"type": "object",

"properties": {

"clause_number": {"type": "string", "description": "e.g. '4.2'"}

},

"required": ["clause_number"]

}

}

CLAUSES = {

"4.2": (

"Party A shall indemnify and hold harmless Party B from and against any claims, "

"damages, losses, and expenses. Notwithstanding the foregoing, in no event shall "

"either party's aggregate liability exceed the amounts paid in the preceding twelve months."

)

}

def format_escalation_packet(tool_input: dict) -> str:

return (

"=== ESCALATION PACKET ===\n"

f"CASE REFERENCE\n  {tool_input['case_reference']}\n\n"

f"ESCALATION REASON\n  {tool_input['escalation_reason']}\n\n"

f"EVIDENCE\n  {tool_input.get('evidence_summary', 'None provided')}\n\n"

f"DECISION REQUIRED\n  {tool_input['decision_required']}\n\n"

f"NEXT STEP\n  {tool_input['next_step']}\n"

"=== END PACKET ==="

)

def handle_escalation(tool_input: dict) -> str:

packet = format_escalation_packet(tool_input)

print("\n" + packet + "\n")

reviewer_decision = (

"classify as (c) mixed — clause contains both indemnification "

"and limitation of liability elements"

)

print(f"[Simulated reviewer decision]: {reviewer_decision}\n")

return reviewer_decision

def dispatch_tool(name: str, tool_input: dict) -> str:

if name == "get_clause_text":

return CLAUSES.get(tool_input["clause_number"], "Clause not found.")

if name == "escalate_for_review":

return handle_escalation(tool_input)

return f"Unknown tool: {name}"

def run_review_agent(task: str) -> str:

messages = [{"role": "user", "content": task}]

while True:

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=4096,

system=SYSTEM,

tools=[GET_CLAUSE_TOOL, ESCALATE_TOOL],

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

print(f"  [tool_call] {block.name}({json.dumps(block.input)})")

result = dispatch_tool(block.name, block.input)

tool_results.append({

"type":        "tool_result",

"tool_use_id": block.id,

"content":     result

})

messages.append({"role": "user", "content": tool_results})

continue

if response.stop_reason == "max_tokens":

raise RuntimeError("Response truncated.")

return ""

if __name__ == "__main__":

task = (

"Review clause 4.2 of contract CLM-2024-4471 (policy POL-2024-0091-B, "

"claimant Torres, Alejandra). "

"Two prior passes produced conflicting classifications: "

"Pass 1 called it an indemnification clause; Pass 2 called it a limitation of liability. "

"Classify the clause and escalate if the conflict cannot be resolved."

)

print("=== Contract Review Agent — Escalation Demo ===\n")

print(f"Task: {task}\n")

final = run_review_agent(task)

print(f"Final agent response:\n{final}")
```

⋯

The escalation tool, clause retriever, packet formatter, and agent loop assembled

Claude will call `get_clause_text("4.2")` to read the actual clause, recognize that the text contains both indemnification and limitation-of-liability language, then call `escalate_for_review` with a five-section packet. The simulated reviewer replies with the mixed classification, and Claude uses that decision in its final response.

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

=== Contract Review Agent — Escalation Demo ===

Task: Review clause 4.2 of contract CLM-2024-4471 ...

[tool\_call] get\_clause\_text({"clause\_number": "4.2"})

[tool\_call] escalate\_for\_review({"case\_reference": "CLM-2024-4471", ...})

=== ESCALATION PACKET ===

CASE REFERENCE

CLM-2024-4471 / POL-2024-0091-B / Torres, Alejandra

ESCALATION REASON

Conflicting prior classifications for clause 4.2 that cannot be resolved ...

EVIDENCE

Pass 1: indemnification. Pass 2: limitation of liability. Clause text contains both elements.

DECISION REQUIRED

Classify clause 4.2 as (a) indemnification, (b) limitation of liability, or (c) mixed.

NEXT STEP

Apply the classification to the coverage determination and proceed to Step 3.

=== END PACKET ===

[Simulated reviewer decision]: classify as (c) mixed — clause contains both ...

Final agent response:

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The exact packet wording varies per run since Claude composes it; structural elements (packet sections, tool call sequence) are consistent.

The key behavioral guarantee is that Claude does not guess between two equally plausible classifications. When it cannot resolve the conflict programmatically, it surfaces the full evidence in structured form and blocks until a human provides the decision.

## The tool description as the escalation policy[#](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-tool-description-as-the-escalation-policy)

The escalation tool’s description is not just documentation; it is the agent’s escalation policy. Claude reads the tool description to decide when `escalate_for_review` is the correct call. A vague description produces over-escalation (the agent escalates whenever it is uncertain) or under-escalation (the agent never escalates because the description does not match its current situation). A comparison of vague vs. specific tool descriptions:

|  |  |  |
| --- | --- | --- |
| **Version** | **Description Text** | **Problem** |
| Too vague | "Use this when you are not sure what to do" | Escalates on every difficult judgment call, overwhelming reviewers |
| Too narrow | "Use this only when a tool call returns an error" | Never escalates on policy gaps or conflicting evidence |
| Correct | Lists four specific conditions with "do not use for..." exclusions | Fires on the intended conditions and does not fire outside them |

The exclusion clause, “do not use this tool for routine errors or retryable failures,” is as important as the inclusion conditions. Without it, an agent that encounters a validation error has two plausible choices: retry with feedback (the correct action) or escalate (unnecessary). The exclusion clause guides the agent away from escalation in cases that the retry loop handles.

## Over-escalation and under-escalation[#](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Over-escalation-and-under-escalation)

Both failure modes are costly, and neither is obvious until the system is running at scale.

- **Over-escalation** occurs when the agent escalates situations it has the authority and information to handle. The symptom is a review queue full of packets where every decision is obvious: low-value actions, retryable errors, and cases that fit the defined policy exactly. Reviewers stop reading the queue carefully because most packets do not require genuine judgment. When a packet that genuinely requires a decision arrives, it may be dismissed along with the routine ones.
- **Under-escalation** occurs when the agent takes actions it should not decide alone. The symptom is silent downstream errors: an agent that sent an external communication without approval, applied the wrong policy rule to an out-of-scope case, or resolved a conflicting finding without flagging the conflict. These errors are often discovered only after the fact, and the cost depends on the irreversibility of the action taken.

The correct calibration is to escalate on the four defined conditions, and only those conditions. The tool description, the system prompt, and the `dispatch_tool` guards together define the boundary between autonomous action and required review.

## Exercise: Design the escalation[#](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Exercise-Design-the-escalation)

Each scenario presents a situation in a running agent. Identify whether escalation is required and, if so, what the decision section of the packet should contain.

Technical Quiz

1.

An agent processes expense reports. For a report flagged with an amount of $14,200, the company policy specifies that amounts over $10,000 require manager approval before reimbursement is processed. The agent has confirmed the amount and the policy rule. Should the agent escalate, and why?

A.

Yes. Over $10,000 is a defined policy trigger, so a manager must approve before payment

B.

No. The agent has confirmed the amount and the policy rule, so it has all the information needed to proceed autonomously

C.

Yes, but only if the amount exceeds $20,000, which represents a more significant threshold

D.

No. The agent should apply the closest matching policy rule and proceed, flagging the decision in the audit log

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Whats-next)

In the next lesson, we cover partial failures and recovery: how to distinguish between access failures, empty results, stale data, and partial completion, and how to write coordinator-safe result objects that carry enough information for the coordinator to decide whether to retry, escalate, or continue with incomplete data.

Context Management Assessment Quiz

Partial Failures and Recovery

Ask

[The four escalation conditions](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-four-escalation-conditions)

[The approval packet](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-approval-packet)

[Implementing the escalation signal](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Implementing-the-escalation-signal)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Complete-code)

[The tool description as the escalation policy](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#The-tool-description-as-the-escalation-policy)

[Over-escalation and under-escalation](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Over-escalation-and-under-escalation)

[Exercise: Design the escalation](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Exercise-Design-the-escalation)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/escalation-and-human-review#Whats-next)