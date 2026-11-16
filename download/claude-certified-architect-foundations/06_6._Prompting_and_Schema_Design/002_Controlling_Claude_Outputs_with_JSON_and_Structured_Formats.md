# Controlling_Claude_Outputs_with_JSON_and_Structured_Formats

Source: https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Output Format Control and Structured Outputs

Explore methods to ensure Claude's responses are schema-valid JSON to simplify integration with downstream systems. Learn to use JSON Outputs and strict tool use features to guarantee structured output and tool call arguments. Understand the limitations of simple prompt instructions and legacy techniques, and apply practical solutions for production-ready AI architectures.

We'll cover the following...

- [Why “return JSON” in the system prompt is not enough](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Why-return-JSON-in-the-system-prompt-is-not-enough)
- [Technique 1: Precise system prompt instructions](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-1-Precise-system-prompt-instructions)
- [Technique 2: JSON outputs, a guaranteed schema match](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-2-JSON-outputs-a-guaranteed-schema-match)
- [Technique 3: Strict tool use, guaranteeing tool call arguments](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-3-Strict-tool-use-guaranteeing-tool-call-arguments)
- [Technique 4: Stop sequences, bounding free text](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-4-Stop-sequences-bounding-free-text)
- [Legacy technique: Assistant turn prefilling](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Legacy-technique-Assistant-turn-prefilling)
- [Choosing the right technique](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Choosing-the-right-technique)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Complete-code)
- [Exercise: Diagnose a format failure](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Exercise-Diagnose-a-format-failure)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Whats-next)

An agent that produces freeform prose is difficult to integrate with downstream systems. A pipeline that extracts fields from a response needs predictable structure. A coordinator that reads specialist results needs JSON it can parse without a fragile regex. This lesson covers how to move Claude from “usually returns JSON” to output that is guaranteed to match a schema, by construction, on every call.

By the end of this lesson, we will be able to:

- Use the JSON Outputs feature (`output_config.format`) to guarantee schema-valid structured output
- Use strict tool use to guarantee that a tool call’s arguments match its schema
- Write system prompt instructions that guide content quality alongside a guaranteed shape

## Why “return JSON” in the system prompt is not enough[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Why-return-JSON-in-the-system-prompt-is-not-enough)

A system prompt instruction like “Return your answer as a JSON object” works most of the time. It fails in three specific situations:

- **Situation 1:** Claude adds a preamble. Instead of starting with `{`, Claude writes “Here is the JSON object you requested:” followed by the JSON. The response is valid if you strip the first line, but it breaks any parser that calls `json.loads()` on the raw string.
- **Situation 2:** Claude wraps JSON in a markdown code block. Claude returns ```` ```json\n{...}\n``` ```` instead of `{...}`. This is syntactically correct markdown but not directly parseable as JSON.
- **Situation 3:** Claude adds an explanation after the JSON. The JSON is valid but is followed by “Note: the `status` field will be null if the order has not shipped yet.” The parser sees everything after the closing `}` as a syntax error.

All three situations share a root cause: a system prompt instruction is a request, not a constraint. Nothing stops Claude from adding text around the JSON except its own judgment about what a helpful answer looks like, and that holds regardless of which model is generating the response. In the rest of the lesson, we will cover how to remove that judgment call from the format entirely, so a response is guaranteed to match a schema rather than usually matching one.

## Technique 1: Precise system prompt instructions[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-1-Precise-system-prompt-instructions)

A system prompt still matters even with a guarantee in place; it guides *what* goes into the fields. A precise instruction needs three elements: a format statement, field definitions, and an example.

Ace Editor

1

2

3

4

5

6

7

SYSTEM = """You are an order status classifier.

Classify the intent and urgency of each customer message. Use the customer's

own words to judge urgency; do not assume urgency from topic alone.

- "intent" is one of: "status\_check", "cancel", "modify\_address", "other"

- "urgency" is one of: "high", "normal", "low\""""

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A precise system prompt: it states the task, defines the allowed values for each field, and gives Claude the judgment criteria for urgency. This shapes what goes into the response.

- **Field definitions:** Each field is named and given its allowed values. “One of: …” constrains `intent` and `urgency` to a fixed set of values instead of free text.
- **Judgment criteria:** “Use the customer’s own words to judge urgency” tells Claude how to decide, not just what the possible answers are. A schema can constrain `urgency` to three values; only the system prompt can tell Claude which of the three actually applies.

![bulb](002_Controlling_Claude_Outputs_with_JSON_and_Structured_Formats_images/img_321a9bd0b1d3.png)

**Why this is not enough on its own:** Nothing here stops Claude from adding a preamble or trailing commentary around the object; a prohibition in a system prompt is a request Claude usually honors, not a constraint it cannot violate. That guarantee comes from the technique below.

## Technique 2: JSON outputs, a guaranteed schema match[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-2-JSON-outputs-a-guaranteed-schema-match)

The JSON outputs feature constrains Claude’s token sampling itself, so that only schema-valid JSON can be generated. This is not a stronger prompt; it is a different mechanism entirely (grammar-constrained decoding). Pass a JSON Schema via `output_config.format`, and the response is guaranteed to match it. There is no preamble to strip, no markdown fence to detect, and no trailing commentary to bound, because none of those are reachable outputs anymore.

The Python SDK’s `messages.parse()` helper accepts a Pydantic model directly and returns an instance of it:

Python

```
from pydantic import BaseModel

from anthropic import Anthropic

client = Anthropic()

class OrderIntent(BaseModel):

order_id: str | None

intent: str

urgency: str

def classify_order_intent(user_message: str) -> OrderIntent:

response = client.messages.parse(

model="claude-opus-4-8",

max_tokens=256,

system=SYSTEM,

messages=[{"role": "user", "content": user_message}],

output_format=OrderIntent

)

return response.parsed_output
```

⋯

JSON Outputs via the messages.parse() helper. The Pydantic model is both the schema Claude's output is constrained to and the type the caller gets back.

- **Line 6:** `OrderIntent` is a plain Pydantic model. Its fields and types become the JSON Schema sent to the API.
- **Line 17:** `output_format=OrderIntent` is the SDK helper’s shorthand for building the underlying `output_config.format` request; it derives the schema from the model automatically.
- **Line 19:** `response.parsed_output` is already an `OrderIntent` instance, not a string and not a dict. There is nothing to parse, because the response cannot be anything other than valid, schema-matching JSON.

The equivalent raw request, for contexts without the SDK’s Pydantic integration, passes the schema directly:

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

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=256,

system=SYSTEM,

messages=[{"role": "user", "content": user\_message}],

output\_config={

"format": {

"type": "json\_schema",

"schema": {

"type": "object",

"properties": {

"order\_id": {"anyOf": [{"type": "string"}, {"type": "null"}]},

"intent": {"type": "string"},

"urgency": {"type": "string"}

},

"required": ["order\_id", "intent", "urgency"],

"additionalProperties": False

}

}

}

)

result = json.loads(response.content[0].text)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The raw output\_config.format request. additionalProperties: false and a complete required list are mandatory. The API rejects a schema missing either with a 400 error. The response text is guaranteed-valid JSON, so json.loads() here cannot raise JSONDecodeError.

Two restrictions matter in practice: every object in the schema needs `additionalProperties: false`, and numeric or string length constraints like `minimum` or `maxLength` are not supported (the SDK strips them from what Claude sees and folds the constraint into the field description instead; validation on the response still enforces the original constraint).

Recursive schemas and external `$ref`s are also unsupported. None of this is a workaround to discover mid-project: the API rejects a non-conforming schema with a 400 error immediately, at request time, not after a bad response comes back.

## Technique 3: Strict tool use, guaranteeing tool call arguments[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-3-Strict-tool-use-guaranteeing-tool-call-arguments)

JSON outputs govern Claude’s final text response. When the guarantee you need is on the arguments Claude passes to a tool instead, the equivalent feature is strict tool use: set `"strict": true` on a tool definition, and that tool’s calls are constrained to match its `input_schema` the same way JSON Outputs constrains the text response.

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

FLIGHT\_TOOL = {

"name": "search\_flights",

"strict": True,

"input\_schema": {

"type": "object",

"properties": {

"destination": {"type": "string"},

"date": {"type": "string", "format": "date"}

},

"required": ["destination", "date"],

"additionalProperties": False

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A tool definition with strict: true. Claude's call to search\_flights is guaranteed to match this schema exactly, no missing date, no extra fields, no malformed date string.

The two features are complementary rather than competing: a single request can use `output_config.format` to guarantee the shape of Claude’s final answer, and `strict: true` on any tools it calls along the way to guarantee those calls’ arguments too. The previous chapter covers tool design in depth; the relevant point here is that “guaranteed structure” is not limited to final JSON responses; it also extends to tool calls.

## Technique 4: Stop sequences, bounding free text[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-4-Stop-sequences-bounding-free-text)

Stop sequences are a current, fully supported feature on every model. They bound a non-schema-enforced response, a short free-text answer that should not run on into unrequested elaboration, by cutting generation off as soon as a specific string appears.

Ace Editor

1

2

3

4

5

6

7

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=128,

system="Answer in one sentence. Do not add caveats or follow-up questions.",

stop\_sequences=["###END###"],

messages=[{"role": "user", "content": "What is the capital of France?"}]

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A stop sequence bounding a free-text answer

`stop_sequences` must contain at least one non-whitespace character; an all-whitespace sequence like `"\n\n"` is rejected with a 400 error on the current API, so a distinct marker like `"###END###"` (included via the system prompt, in practice) is used instead.

If the response you need is structured, reach for JSON Outputs instead of trying to bound it with a stop sequence; a schema guarantee makes trailing commentary unreachable at the source, which is strictly stronger than stopping generation after a specific string appears. Stop sequences are the right tool only when there is no schema to enforce in the first place.

## Legacy technique: Assistant turn prefilling[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Legacy-technique-Assistant-turn-prefilling)

Older code and tutorials may show a technique called assistant turn prefilling: adding an assistant message ending in `{"role": "assistant", "content": "{"}` to force Claude’s response to begin with a specific character, eliminating preamble text by making it structurally impossible to write anything before the prefill.

This worked because the API allowed a request to end on an assistant turn, and Claude would continue generating from that point. Claude 4.6 and later models reject this outright: a request must end with a user turn, and attempting to prefill raises a 400 error.

Every model that still accepts a prefill predates that cutoff, and Anthropic retires older model generations on an ongoing basis: Claude 3.5 Sonnet and 3.7 Sonnet are already gone this way, and the remaining pre-4.6 models are next in the same rotation, whenever their own retirement dates land. There is no durable model left to build new code around this technique, only ones with a shrinking runway. Check the [model deprecations page](https://platform.claude.com/docs/en/about-claude/model-deprecations) for current status.

If you inherit code that uses prefilling, the fix is to replace the prefill with `output_config.format` which achieves the same “no preamble” outcome.

## Choosing the right technique[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Choosing-the-right-technique)

Each technique in this lesson answers a different question, and using the wrong one for a given goal either under-delivers (a prompt that only reduces the odds of a failure) or reaches for something that no longer works at all (prefilling). The table below maps each goal to the technique that actually guarantees it.

|  |  |  |
| --- | --- | --- |
| **Goal** | **Technique** | **Notes** |
| Guarantee the final response matches a JSON schema | JSON Outputs (output\_config.format) | No retries needed; valid by construction; every current model |
| Guarantee a tool call’s arguments match a schema | Strict tool use (strict: true) | Complementary to JSON Outputs; applies to tool inputs, not the final response |
| Guide field content and semantics | Precise system prompt | Still valuable alongside a guarantee; the schema shapes structure, not meaning |
| Bound a free-text response that is not schema-enforced | Stop sequences | Still fully supported; the sequence must include a non-whitespace character |

For a production extraction pipeline, JSON Outputs does the heavy lifting on its own:

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

class Invoice(BaseModel):

vendor\_name: str

invoice\_date: str

line\_items: list[str]

total\_amount: str

EXTRACT\_SYSTEM = """Extract invoice fields from the text.

Use the vendor's own wording for line items; do not summarize or abbreviate them."""

def extract\_invoice(text: str) -> Invoice:

response = client.messages.parse(

model="claude-opus-4-8",

max\_tokens=512,

system=EXTRACT\_SYSTEM,

messages=[{"role": "user", "content": text}],

output\_format=Invoice

)

return response.parsed\_output

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A production-grade invoice extraction function. The system prompt guides content quality (how to phrase line items); output\_format=Invoice guarantees the shape. There is no example block in the system prompt, no prefill, no stop sequence, and no parsing step, the schema alone determines what a valid response looks like.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Complete-code)

We implement all three current techniques from this lesson in one executable file. `classify_order_intent` and `extract_invoice` use `messages.parse()` with a Pydantic model, so the response is guaranteed to match the schema with no parsing step. `plan_trip` combines `output_config.format` for the final answer with `strict: true` on a tool definition, showing both guarantees in a single request.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import json

from pydantic import BaseModel

from anthropic import Anthropic

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = Anthropic(api_key=anthropic_api_key)

SYSTEM = """You are an order status classifier.

Classify the intent and urgency of each customer message. Use the customer's

own words to judge urgency; do not assume urgency from topic alone.

- "intent" is one of: "status_check", "cancel", "modify_address", "other"

- "urgency" is one of: "high", "normal", "low\""""

class OrderIntent(BaseModel):

order_id: str | None

intent: str

urgency: str

def classify_order_intent(user_message: str) -> OrderIntent:

response = client.messages.parse(

model="claude-opus-4-8",

max_tokens=256,

system=SYSTEM,

messages=[{"role": "user", "content": user_message}],

output_format=OrderIntent

)

return response.parsed_output

EXTRACT_SYSTEM = """Extract invoice fields from the text.

Use the vendor's own wording for line items; do not summarize or abbreviate them."""

class Invoice(BaseModel):

vendor_name: str

invoice_date: str

line_items: list[str]

total_amount: str

def extract_invoice(text: str) -> Invoice:

response = client.messages.parse(

model="claude-opus-4-8",

max_tokens=512,

system=EXTRACT_SYSTEM,

messages=[{"role": "user", "content": text}],

output_format=Invoice

)

return response.parsed_output

FLIGHT_TOOL = {

"name": "search_flights",

"strict": True,

"input_schema": {

"type": "object",

"properties": {

"destination": {"type": "string"},

"date": {"type": "string", "format": "date"}

},

"required": ["destination", "date"],

"additionalProperties": False

}

}

TRIP_SCHEMA = {

"type": "object",

"properties": {

"summary": {"type": "string"},

"next_steps": {"type": "array", "items": {"type": "string"}}

},

"required": ["summary", "next_steps"],

"additionalProperties": False

}

def plan_trip(request: str) -> dict:

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=512,

messages=[{"role": "user", "content": request}],

output_config={"format": {"type": "json_schema", "schema": TRIP_SCHEMA}},

tools=[FLIGHT_TOOL]

)

tool_call = next((b for b in response.content if b.type == "tool_use"), None)

text_block = next((b for b in response.content if b.type == "text"), None)

return {

"tool_call": {"name": tool_call.name, "input": tool_call.input} if tool_call else None,

"summary": json.loads(text_block.text) if text_block else None

}

if __name__ == "__main__":

print("=== classify_order_intent: JSON Outputs with a Pydantic model ===\n")

classify_cases = [

"I was charged $120 but my plan is only $80/month. Can you explain this?",

"URGENT: Please cancel order ORD-4421 immediately, I ordered the wrong size.",

]

for msg in classify_cases:

result = classify_order_intent(msg)

print(f"Input  : {msg[:70]}{'...' if len(msg) > 70 else ''}")

print(f"Output : {result.model_dump_json()}")

print()

print("=== extract_invoice: JSON Outputs with a Pydantic model ===\n")

invoice = (

"INVOICE\n"

"Vendor: Nexus Technology Partners\n"

"Invoice Date: April 15, 2025\n"

"Line Items:\n"

"  Cloud hosting (monthly): $450.00\n"

"  Managed backup service: $75.00\n"

"Total Due: $525.00"

)

result = extract_invoice(invoice)

print(result.model_dump_json(indent=2))

print()

print("=== plan_trip: JSON Outputs combined with strict tool use ===\n")

result = plan_trip("Help me plan a trip to Paris departing May 15, 2026.")

print(json.dumps(result, indent=2))
```

⋯

All three current techniques in one file, with no `son.loads() on an unguaranteed string anywhere

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

=== classify\_order\_intent: JSON Outputs with a Pydantic model ===

Input : I was charged $120 but my plan is only $80/month. Can you explain this?

Output : {"order\_id":null,"intent":"other","urgency":"normal"}

Input : URGENT: Please cancel order ORD-4421 immediately, I ordered the wrong size.

Output : {"order\_id":"ORD-4421","intent":"cancel","urgency":"high"}

=== extract\_invoice: JSON Outputs with a Pydantic model ===

{

"vendor\_name": "Nexus Technology Partners",

"invoice\_date": "2025-04-15",

"line\_items": [

"Cloud hosting (monthly): $450.00",

"Managed backup service: $75.00"

],

"total\_amount": "$525.00"

}

=== plan\_trip: JSON Outputs combined with strict tool use ===

{

"tool\_call": {

"name": "search\_flights",

"input": {"destination": "Paris", "date": "2026-05-15"}

},

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Expected output, deterministic in shape (every field guaranteed present with the correct type), though the exact wording Claude generates for free-text fields varies between runs

Every field in every output above is guaranteed to be present with the correct type; that is not a claim about this particular run, it is a property of the request itself. No code path in this file can raise `JSONDecodeError` because there is no code path where Claude’s response can be anything other than schema-valid JSON.

## Exercise: Diagnose a format failure[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Exercise-Diagnose-a-format-failure)

A developer writes this call for a sentiment classifier, on a currently active model, without JSON Outputs:

Ace Editor

1

2

3

4

5

6

7

8

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=128,

system='Classify the sentiment of the message. Return JSON with a "sentiment" key.',

messages=[{"role": "user", "content": user\_message}]

)

raw = response.content[0].text

result = json.loads(raw)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

On most inputs `json.loads(raw)` succeeds. On 12% of inputs, it raises a `json.JSONDecodeError`. The developer logs the failing `raw` values and sees these patterns:

- Pattern A: `"Here is the sentiment classification:\n{\\"sentiment\\": \\"positive\\"}"`
- Pattern B: ```` "```json\n{\\"sentiment\\": \\"neutral\\"}\n```" ````
- Pattern C: `"{\\"sentiment\\": \\"negative\\"}\n\nThis message expresses a negative tone."`

Technical Quiz

1.

Patterns A, B, and C all stem from the same underlying issue, even though the model being called is current, not a retired one. What is it?

A.

A system prompt instruction is a request, not a constraint on what Claude can generate

B.

Claude’s `max_tokens` limit is set too low, truncating the response before the JSON closes properly

C.

The three patterns are unrelated bugs, each one requiring its own independent, unrelated fix

D.

The mock sentiment values used in testing do not match the schema Claude was actually given

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Whats-next)

In the next lesson, we cover few-shot examples and chain-of-thought prompting: how to use examples to calibrate output quality and how to guide Claude's reasoning process for tasks that require explicit intermediate steps.

System Prompt Structure and Instruction Hierarchy

Few-Shot Examples and Chain-of-Thought Prompting

Ask

[Why “return JSON” in the system prompt is not enough](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Why-return-JSON-in-the-system-prompt-is-not-enough)

[Technique 1: Precise system prompt instructions](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-1-Precise-system-prompt-instructions)

[Technique 2: JSON outputs, a guaranteed schema match](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-2-JSON-outputs-a-guaranteed-schema-match)

[Technique 3: Strict tool use, guaranteeing tool call arguments](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-3-Strict-tool-use-guaranteeing-tool-call-arguments)

[Technique 4: Stop sequences, bounding free text](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Technique-4-Stop-sequences-bounding-free-text)

[Legacy technique: Assistant turn prefilling](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Legacy-technique-Assistant-turn-prefilling)

[Choosing the right technique](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Choosing-the-right-technique)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Complete-code)

[Exercise: Diagnose a format failure](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Exercise-Diagnose-a-format-failure)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/output-format-control-and-structured-outputs#Whats-next)