# Few-Shot_Examples_and_Chain-of-Thought_Prompting_Techniques

Source: https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Few-Shot Examples and Chain-of-Thought Prompting

Explore how to apply few-shot examples and chain-of-thought prompting to guide Claude's reasoning for complex tasks. This lesson helps you design effective prompts with positive and negative examples, format them correctly, and distinguish visible reasoning from internal extended thinking to achieve reliable AI outputs.

We'll cover the following...

- [What few-shot examples do](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#What-few-shot-examples-do)
- [Placement: System prompt vs. user turn](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Placement-System-prompt-vs-user-turn)
- [Negative examples](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Negative-examples)
- [Chain-of-thought prompting](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Chain-of-thought-prompting)
- [Chain-of-thought vs. extended thinking](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Chain-of-thought-vs-extended-thinking)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Complete-code)
- [How many examples to use](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#How-many-examples-to-use)
- [Exercise: Choose the right technique](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Exercise-Choose-the-right-technique)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Whats-next)

A well-structured system prompt sets the rules. Examples show Claude what following those rules looks like in practice. These two mechanisms are complementary: rules constrain the space of valid outputs, and examples pull Claude toward the best output within that space. This lesson covers how to place and format examples for maximum effect, and how to instruct Claude to reason through complex tasks before committing to an answer. By the end of this lesson, we will be able to:

- Place a few-shot example in the correct location and format for a given task
- Write positive and negative examples that steer Claude away from common errors
- Apply chain-of-thought instructions to tasks that require intermediate reasoning steps
- Distinguish between chain-of-thought in the prompt and the extended thinking API feature

## What few-shot examples do[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#What-few-shot-examples-do)

A few-shot example is a completed input-output pair that Claude reads before it processes the actual request. It demonstrates the desired output, not just describes it. Claude infers the expected format, tone, level of detail, and handling of edge cases from the examples rather than from its interpretation of the written instructions. Three situations signal that few-shot examples are needed:

- The output has a non-obvious structure. A JSON schema with nested arrays, specific field names, or unusual enum values benefits from a concrete example far more than a written description of the schema.
- The task involves subtle judgment. Classifying support tickets as “billing,” “technical,” or “account” is straightforward. Distinguishing “billing dispute” from “billing inquiry” from “payment failure” requires examples that show how edge cases are handled.
- The written instructions are not reducing errors. If Claude’s output is consistent but wrong in a specific way, an example that shows the correct output for that case is often more effective than additional written instructions.

## Placement: System prompt vs. user turn[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Placement-System-prompt-vs-user-turn)

Few-shot examples can go in the system prompt or in the user turn. The choice depends on whether the examples apply to every request or only to a specific input type.

- System prompt examples apply to every conversation turn. They are the right choice when the examples illustrate the general output format or the handling of a category of input that will appear frequently.
- User turn examples apply only to the current request. They are the right choice when the task is a one-time operation with a specific desired output style that would not generalize.

For most agent pipelines, examples go in the system prompt because the agent handles a consistent class of inputs. The structure looks like this:

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

CLASSIFY\_SYSTEM = """You are a support ticket classifier for Meridian Cloud.

Classify each ticket into exactly one of these categories:

- billing\_dispute: customer contests a charge or invoice total

- billing\_inquiry: customer asks about charges without disputing them

- payment\_failure: a payment attempt was declined or could not be processed

- technical\_error: a product or API is not working as expected

- account\_access: login, password, or permission issues

- feature\_request: customer asks for a capability that does not exist yet

- other: does not fit the above categories

Return a JSON object with fields "category" and "confidence" (high/medium/low).

Examples:

Input: "I was charged $120 but my plan is $80/month. Please explain."

Output: {"category": "billing\_dispute", "confidence": "high"}

Input: "When does my billing cycle reset each month?"

Output: {"category": "billing\_inquiry", "confidence": "high"}

Input: "My card ending in 4421 was declined when I tried to upgrade."

Output: {"category": "payment\_failure", "confidence": "high"}

Input: "The /v2/events endpoint has been returning 503 errors since yesterday."

Output: {"category": "technical\_error", "confidence": "high"}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A system prompt with five positive examples. Each example pairs a realistic input with the correct output. The examples are formatted consistently: “Input:” on one line, “Output:” on the next, with a blank line separating pairs.

- **Category definitions:** Each category is defined with a one-line description before the examples. The definitions set the rule; the examples demonstrate application.
- **Example format:** “Input:”/“Output:” pairs are visually distinct and consistent. Claude reads the pattern and mirrors it.
- **Coverage:** The five examples cover the five most commonly confused categories. `billing_dispute` vs. `billing_inquiry` is the hardest distinction, so both get an example to show the difference.
- **No example for** **`feature_request`** **or** **`other`****:** Not every category needs an example. Low-ambiguity categories are handled by the definition alone.

## Negative examples[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Negative-examples)

A negative example shows Claude what the wrong output looks like and why it is wrong. Negative examples are most useful when Claude is making a consistent, specific mistake that positive examples have not corrected.

The format pairs the wrong output with an explanation, then the correct output:

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

CLASSIFY\_SYSTEM\_V2 = """...

Examples:

Input: "I was charged twice this month."

Wrong output: {"category": "billing\_inquiry", "confidence": "high"}

Why wrong: The customer is disputing a duplicate charge, not merely asking about it.

Correct output: {"category": "billing\_dispute", "confidence": "high"}

Input: "How do I export my invoice as a PDF?"

Output: {"category": "billing\_inquiry", "confidence": "high"}

"""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A negative example paired with a corrected positive example. The “Why wrong” line explains the reasoning, helping Claude generalize the correction beyond this specific case.

- **Negative + correction pairing:** A negative example without a correction leaves Claude with the error and no guidance on what to do instead. Always pair the negative with the correct output.
- **“Why wrong” explanation:** The explanation helps Claude understand the principle, not just memorize the case. Without it, Claude may correctly handle this exact input but still make the same error with slightly different phrasing.

## Chain-of-thought prompting[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Chain-of-thought-prompting)

Chain-of-thought (CoT) instructs Claude to reason step by step before producing a final answer. It is most valuable for tasks where the answer depends on intermediate calculations, multi-step logic, or several pieces of evidence that must be weighed together.

The basic pattern adds one instruction to the system prompt and optionally a visible reasoning section to the output schema:

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

TRIAGE\_SYSTEM = """You are a medical records triage assistant.

Given a patient intake form, assess urgency level (critical/urgent/routine) and

recommend the appropriate care pathway.

Think through the following before giving your answer:

1. Identify any symptoms that indicate a time-sensitive condition.

2. Check for contraindications with any listed medications.

3. Note any missing required fields that would affect the assessment.

Then state your urgency level and recommended pathway.

Return a JSON object with:

- "reasoning": string (your step-by-step analysis, 2-4 sentences)

- "urgency": string ("critical", "urgent", or "routine")

- "pathway": string (one of: "emergency", "same-day", "scheduled", "telemedicine")

Example:

Input: "Patient reports chest pain (8/10) for 2 hours. Medications: metformin. No allergies."

Output: {

"reasoning": "Chest pain at 8/10 severity for 2+ hours is a potential cardiac event. Metformin is not a contraindication. All required fields present.",

"urgency": "critical",

"pathway": "emergency"

}

Return only the JSON object."""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A chain-of-thought prompt for a medical triage task. The numbered thinking steps guide the reasoning process. The reasoning field in the output schema captures the visible reasoning, which can be reviewed for audit purposes.

- **Numbered thinking steps:** The three numbered steps direct Claude to consider specific factors in a specific order. Without this structure, Claude reasons freely, which may skip important checks. Ordered steps are more reliable than “think carefully before answering.”
- **`reasoning`** **field in the output:** Capturing reasoning in a structured field serves two purposes: it gives Claude a designated place to write its intermediate thinking, and it produces an auditable trace that can be reviewed when an output is questioned.
- **Example with reasoning included:** The example shows what a complete reasoning field looks like, including appropriate length (two to four sentences) and the connection between reasoning and conclusion.

## Chain-of-thought vs. extended thinking[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Chain-of-thought-vs-extended-thinking)

The chain-of-thought pattern in the previous section asks Claude to write its reasoning as part of the visible output. The extended thinking API feature is different: it gives Claude a separate, internal reasoning budget that runs before the visible response.

|  |  |  |
| --- | --- | --- |
| **Aspect** | **Chain-of-Thought in Prompt** | **Extended Thinking API** |
| Reasoning location | Inside the visible response content | In a separate `thinking` block, before the text response |
| Prompt token cost | Reasoning is in the output, counts toward max\_tokens | Thinking has its own separate budget parameter |
| Auditability | Reasoning is in the response you parse | Thinking blocks are returned in `response.content` alongside text |
| Best for | Tasks where reasoning improves output, and you want it in the result | Complex multi-step tasks where longer reasoning improves accuracy without bloating the response content |

To use extended thinking, set the `thinking` parameter on the API call:

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

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=1024,

thinking={

"type": "enabled",

"budget\_tokens": 5000

},

system=SYSTEM,

messages=messages

)

text\_blocks = [b for b in response.content if b.type == "text"]

thinking\_blocks = [b for b in response.content if b.type == "thinking"]

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Enabling extended thinking. The thinking dict sets a separate token budget for the internal reasoning phase. The response content contains both thinking blocks and text blocks; they are separated by type after the call returns.

- **`budget_tokens`****:** Controls how many tokens Claude can spend on internal reasoning before producing the visible response. Higher values improve accuracy on complex tasks at a higher cost. For routine classification tasks, extended thinking adds cost without benefit.
- **`thinking`** **blocks:** Returned in `response.content` alongside `text` blocks. They contain Claude’s internal reasoning and can be logged for audit or debugging, but they are not part of the parseable response content.
- **`text`** **block separation:** Parsing should operate only on `text` blocks. `thinking` blocks are reasoning artifacts, not structured output.

**The key distinction:** Chain-of-thought in the prompt is a prompting technique that works on any model. Extended thinking is an API feature available on specific models. Use chain-of-thought when you want visible reasoning in the parseable output. Use extended thinking when you need deeper reasoning on complex tasks and prefer to keep the output clean.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Complete-code)

We run both prompting techniques from this lesson back-to-back: the few-shot ticket classifier and the chain-of-thought triage assistant. The first function shows how examples pull Claude toward the correct category boundary; the second shows how numbered reasoning steps produce a visible `reasoning` field alongside the final answer.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import json

import re

import anthropic

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = anthropic.Anthropic(api_key=anthropic_api_key)

def _parse_json(text: str) -> dict:

text = text.strip()

m = re.search(r'```(?:json)?\s*\n?([\s\S]+?)\n?\s*```', text)

if m:

text = m.group(1).strip()

start, end = text.find('{'), text.rfind('}') + 1

if start != -1 and end > start:

text = text[start:end]

return json.loads(text)

CLASSIFY_SYSTEM = """You are a support ticket classifier for Meridian Cloud.

Classify each ticket into exactly one of these categories:

- billing_dispute: customer contests a charge or invoice total

- billing_inquiry: customer asks about charges without disputing them

- payment_failure: a payment attempt was declined or could not be processed

- technical_error: a product or API is not working as expected

- account_access: login, password, or permission issues

- feature_request: customer asks for a capability that does not exist yet

- other: does not fit the above categories

Return a JSON object with fields "category" and "confidence" (high/medium/low).

Examples:

Input: "I was charged $120 but my plan is $80/month. Please explain."

Output: {"category": "billing_dispute", "confidence": "high"}

Input: "When does my billing cycle reset each month?"

Output: {"category": "billing_inquiry", "confidence": "high"}

Input: "My card ending in 4421 was declined when I tried to upgrade."

Output: {"category": "payment_failure", "confidence": "high"}

Input: "The /v2/events endpoint has been returning 503 errors since yesterday."

Output: {"category": "technical_error", "confidence": "high"}

Input: "I need to add a team member but the invite button is greyed out."

Output: {"category": "account_access", "confidence": "medium"}

Return only the JSON object."""

def classify_ticket(message: str) -> dict:

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=128,

system=CLASSIFY_SYSTEM,

messages=[{"role": "user", "content": message}]

)

for block in response.content:

if block.type == "text":

return _parse_json(block.text)

raise ValueError("No text block in response")

TRIAGE_SYSTEM = """You are a medical records triage assistant.

Given a patient intake form, assess urgency level (critical/urgent/routine) and

recommend the appropriate care pathway.

Think through the following before giving your answer:

1. Identify any symptoms that indicate a time-sensitive condition.

2. Check for contraindications with any listed medications.

3. Note any missing required fields that would affect the assessment.

Then state your urgency level and recommended pathway.

Return a JSON object with:

- "reasoning": string (your step-by-step analysis, 2-4 sentences)

- "urgency": string ("critical", "urgent", or "routine")

- "pathway": string (one of: "emergency", "same-day", "scheduled", "telemedicine")

Example:

Input: "Patient reports chest pain (8/10) for 2 hours. Medications: metformin. No allergies."

Output: {

"reasoning": "Chest pain at 8/10 severity for 2+ hours is a potential cardiac event. Metformin is not a contraindication. All required fields present.",

"urgency": "critical",

"pathway": "emergency"

}

Return only the JSON object."""

def triage_patient(intake_form: str) -> dict:

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=512,

system=TRIAGE_SYSTEM,

messages=[{"role": "user", "content": intake_form}]

)

for block in response.content:

if block.type == "text":

return _parse_json(block.text)

raise ValueError("No text block in response")

if __name__ == "__main__":

print("=== Few-shot ticket classifier ===\n")

tickets = [

"I was charged twice this month — two identical $99 charges on the 1st and 2nd.",

"How do I export my invoice as a PDF?",

"Our webhook endpoint stopped receiving events at 14:00 UTC today.",

"Can you add bulk CSV import for contacts? We need it for our migration.",

"I can't log in — it says my account is suspended but I received no email about it.",

]

for ticket in tickets:

result = classify_ticket(ticket)

print(f"Ticket     : {ticket[:70]}{'...' if len(ticket) > 70 else ''}")

print(f"Category   : {result.get('category')}")

print(f"Confidence : {result.get('confidence')}")

print()

print("=== Chain-of-thought triage ===\n")

intakes = [

"Patient: 67F. Sudden severe headache (10/10) starting 20 min ago. No prior history. Medications: lisinopril. No allergies.",

"Patient: 34M. Mild sore throat for 3 days, no fever. Medications: none. No allergies. Requesting same-day appointment.",

"Patient: 52F. Chest tightness and shortness of breath for 45 min. Medications: aspirin, atorvastatin. No allergies.",

]

for intake in intakes:

result = triage_patient(intake)

reasoning = result.get("reasoning", "")

print(f"Intake     : {intake[:80]}{'...' if len(intake) > 80 else ''}")

print(f"Urgency    : {result.get('urgency')}")

print(f"Pathway    : {result.get('pathway')}")

print(f"Reasoning  : {reasoning[:130]}{'...' if len(reasoning) > 130 else ''}")

print()
```

⋯

Both prompting techniques in one file. `classify\_ticket` uses five positive few-shot examples in the system prompt. `triage\_patient` uses chain-of-thought steps and captures intermediate reasoning in the `reasoning` JSON field.

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

=== Few-shot ticket classifier ===

Ticket : I was charged twice this month — two identical $99 charges on the 1st and 2nd.

Category : billing\_dispute

Confidence : high

Ticket : How do I export my invoice as a PDF?

Category : billing\_inquiry

Confidence : high

Ticket : Our webhook endpoint stopped receiving events at 14:00 UTC today.

Category : technical\_error

Confidence : high

Ticket : Can you add bulk CSV import for contacts? We need it for our migration.

Category : feature\_request

Confidence : high

Ticket : I can't log in — it says my account is suspended but I received no email about it.

Category : account\_access

Confidence : medium

=== Chain-of-thought triage ===

Intake : Patient: 67F. Sudden severe headache (10/10) starting 20 min ago. No prior history...

Urgency : critical

Pathway : emergency

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The five examples in `CLASSIFY_SYSTEM` show Claude where the `billing_dispute` vs. `billing_inquiry` boundary falls. This distinction most often produces misclassifications without examples. The `reasoning` field in the triage output is an auditable trace: it shows which criteria drove the urgency decision and which medication checks were run, without adding those details to the user-facing response content.

## How many examples to use[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#How-many-examples-to-use)

The effective range for few-shot examples is two to five. Below two, edge cases are underspecified. Above five, the system prompt grows significantly, adding input tokens on every call and potentially diluting attention on the instructions that follow the examples.

A practical guideline:

|  |  |
| --- | --- |
| **Task Complexity** | **Recommended Examples** |
| Simple classification, clear categories | 2-3 (one per ambiguous boundary) |
| Extraction with nested structure | 2 (one standard, one with missing fields) |
| Multi-label or scored output | 3-5 (covering the score range) |
| Complex reasoning or judgment | 2-3 with chain-of-thought reasoning shown |

More examples rarely help when fewer examples fail. If three examples are not producing reliable output, the problem is usually in the instructions or the category definitions, not in the example count.

## Exercise: Choose the right technique[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Exercise-Choose-the-right-technique)

For each scenario, decide whether few-shot examples, chain-of-thought, or neither is the appropriate addition.

Technical Quiz

1.

A developer builds a pipeline that extracts a vendor\_name field from invoices. JSON Outputs (`output_config.format`) guarantees every response is schema-valid, and the extracted vendor\_name is correct 97% of the time. On 3% of inputs, Claude extracts the bill-to company name instead of the vendor name. Which addition best fixes this?

A.

A negative example marking the bill-to name wrong and the vendor name correct

B.

Add chain-of-thought steps to reason through which name is the vendor

C.

Add a stop sequence to prevent Claude from writing multiple name candidates

D.

Increase the example count from 0 to 5 to cover more input variations

---

1 / 3

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Whats-next)

In the next lesson, we cover extended thinking in depth alongside prompt injection awareness: how to recognize when a user turn attempts to override system prompt instructions and what prompt-level defenses can reduce the attack surface.

Output Format Control and Structured Outputs

Extended Thinking and Prompt Injection Defense

Ask

[What few-shot examples do](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#What-few-shot-examples-do)

[Placement: System prompt vs. user turn](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Placement-System-prompt-vs-user-turn)

[Negative examples](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Negative-examples)

[Chain-of-thought prompting](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Chain-of-thought-prompting)

[Chain-of-thought vs. extended thinking](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Chain-of-thought-vs-extended-thinking)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Complete-code)

[How many examples to use](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#How-many-examples-to-use)

[Exercise: Choose the right technique](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Exercise-Choose-the-right-technique)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/few-shot-examples-and-chain-of-thought-prompting#Whats-next)