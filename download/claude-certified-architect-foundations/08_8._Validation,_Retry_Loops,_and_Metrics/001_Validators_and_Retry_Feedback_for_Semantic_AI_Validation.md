# Validators_and_Retry_Feedback_for_Semantic_AI_Validation

Source: https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Validators and Retry Feedback

Understand the difference between structural and semantic validation and learn to write validators that catch semantic errors. Explore how to provide Claude with precise retry feedback to correct outputs efficiently. Implement retry loops that enhance AI reliability by targeting specific error corrections and avoiding repeated mistakes.

We'll cover the following...

- [Structural vs. semantic validation](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Structural-vs-semantic-validation)
- [Writing a semantic validator](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Writing-a-semantic-validator)
- [Generic vs. specific retry feedback](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Generic-vs-specific-retry-feedback)
- [The retry loop](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#The-retry-loop)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Complete-code)
- [When not to retry](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#When-not-to-retry)
- [Exercise: Design the feedback](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Exercise-Design-the-feedback)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Whats-next)

A schema check confirms that the output has the right shape: the required keys are present, the types match, and the array is not empty. It does not confirm that the values are meaningful. A validator that only checks structure will pass outputs where `confidence` is `"high"` but the extracted `invoice_total` is negative, or where `category` is a valid enum value but plainly wrong for the input. This lesson covers how to write validators that catch those semantic errors, and how to phrase retry feedback so that the next attempt fixes the problem rather than producing a different wrong answer. By the end of this lesson, we will be able to:

- Distinguish structural validation from semantic validation and explain why both are necessary
- Write a validator that catches field-level semantic errors in extracted output
- Identify the difference between generic retry wording and specific retry feedback
- Implement a retry loop with a feedback message that names the exact error

## Structural vs. semantic validation[#](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Structural-vs-semantic-validation)

Structural validation checks the form of the output. Semantic validation checks whether the values are coherent, consistent, and correct given the input.

The distinction matters because Claude almost never returns malformed JSON after output-format techniques are applied. The errors that reach production are semantic: the right keys, the wrong values. A few examples of outputs that pass structural validation but fail semantically:

|  |  |  |
| --- | --- | --- |
| **Field** | **Structural Check Passes** | **Semantic Problem** |
| `invoice_total` | Value is a number | Value is negative; invoices cannot have negative totals |
| `issue_date` | Value is a string | Value is after `due_date`; invoices cannot be due before they are issued |
| `category` | Value is a valid enum member | Value is `"billing_inquiry"` but the ticket describes a system outage |
| `confidence` | Value is `"high"`, `"medium"`, or `"low"` | Value is `"high"` but three required fields are missing from the extraction |

The validator must encode the rules that make values meaningful, not just the rules that make them structurally correct.

## Writing a semantic validator[#](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Writing-a-semantic-validator)

A semantic validator is a function that takes the parsed output and the original input, applies domain rules, and returns either a success signal or a list of specific error messages. Returning a list rather than raising on the first error gives Claude a complete picture of what to fix in one retry. Here’s a validator for an invoice extraction output:

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

from typing import Optional

@dataclass

class ValidationResult:

valid: bool

errors: list[str]

def validate\_invoice(raw\_input: str, extracted: dict) -> ValidationResult:

errors = []

total = extracted.get("invoice\_total")

if total is not None and total < 0:

errors.append(

f"invoice\_total is {total}, but invoice totals cannot be negative. "

"Re-read the document and extract the correct positive total."

)

issue\_date = extracted.get("issue\_date", "")

due\_date = extracted.get("due\_date", "")

if issue\_date and due\_date and issue\_date > due\_date:

errors.append(

f"issue\_date ({issue\_date}) is after due\_date ({due\_date}). "

"The issue date must be on or before the due date. "

"Check both dates in the source document."

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A semantic validator for invoice extraction. Each check tests a domain rule, not just a type. Each error message names the field, states the problem, and tells Claude what to look for in the source document.

- **Lines 17:** The `ValidationResult` dataclass defines the return type with `valid` (bool) and `errors` (list of strings). Returning a dataclass rather than raising on the first failure allows every check in the function to run before returning. Claude receives the complete error list in one retry prompt rather than fixing one field per attempt.
- **Lines 1217:** The `invoice_total` check enforces the domain rule that totals are non-negative. A negative number is syntactically valid JSON; only a semantic rule catches it. The error message names the field with its actual extracted value and tells Claude exactly where to look in the source document.
- **Lines 1926:** ISO 8601 date strings compare correctly as plain strings, so `issue_date > due_date` is a valid temporal check without parsing. This inconsistency cannot be expressed in a JSON schema, making it a semantic-only rule.
- **Lines 3541:** The currency check constrains the field to a normalized set of codes. A schema `enum` could enforce the same constraint structurally, but the error message here lists the valid values explicitly; that is information a generic schema validation error cannot provide to Claude.
- **Lines 1241:** Every error message follows the same pattern: the field name with its extracted value, the violated rule, and a directive that sends Claude back to the source document. This structure gives Claude the specific context it needs to correct each field in a single retry.

## Generic vs. specific retry feedback[#](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Generic-vs-specific-retry-feedback)

When a validator returns errors, those errors become the retry prompt. The quality of the feedback determines whether the retry succeeds.

Generic feedback tells Claude something went wrong, but not what:

Ace Editor

1

The extraction was incorrect. Please try again.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

After reading this, Claude has no new information. It will produce a similar output with the same errors, or it will fix one thing and introduce another problem.

Specific feedback names the field, states the exact value, explains why it is wrong, and gives Claude a directive:

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

The following errors were found in your extraction:

1. invoice\_total is -245.00, but invoice totals cannot be negative.

Re-read the document and extract the correct positive total.

2. issue\_date (2024-03-20) is after due\_date (2024-03-15).

The issue date must be on or before the due date.

Check both dates in the source document.

Please correct only the fields listed above and return the full updated JSON.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The instruction correct only the fields listed above and return the full updated JSON prevents Claude from re-extracting fields that were already correct, which could introduce new errors in previously valid fields.

## The retry loop[#](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#The-retry-loop)

A retry loop runs the extraction, validates the result, and, if validation fails, constructs a feedback message and retries up to a maximum number of attempts.

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

import json

import anthropic

client = anthropic.Anthropic()

def extract\_with\_retry(

document: str,

system\_prompt: str,

max\_retries: int = 3

) -> dict | None:

messages = [{"role": "user", "content": document}]

for attempt in range(max\_retries):

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=1024,

system=system\_prompt,

messages=messages

)

raw\_text = response.content[0].text

try:

extracted = json.loads(raw\_text)

except json.JSONDecodeError as e:

feedback = f"The response was not valid JSON: {e}. Return only a JSON object."

messages.append({"role": "assistant", "content": raw\_text})

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A retry loop that appends the assistant’s previous response and the feedback message to the conversation before retrying. This preserves the full extraction context across attempts so Claude can correct specific fields without losing the rest.

- **Line 12:** `messages` is initialized with the document as the first user turn. Each retry appends the assistant’s previous output and the feedback to this list, so Claude reads the full conversation history on every attempt: the original document, the previous extraction, and the specific errors. That gives it the context needed for targeted correction.
- **Lines 23–29:** A `JSONDecodeError` is treated as a separate failure mode from semantic validation. The feedback names the parse error directly, and `continue` skips the validation step to retry immediately. This prevents Claude from trying to apply semantic correction rules to a response that wasn’t even valid JSON.
- **Lines 35–36:** On the final attempt, if validation still fails, the function returns `None` rather than retrying. The caller must handle `None` by logging the failure, escalating to a human reviewer, or applying a fallback. A loop without this bound retries indefinitely on a hard extraction failure.
- **Lines 41–45:** The feedback message wraps the numbered error list and closes with “correct only the fields listed above and return the full updated JSON.” This instruction scopes the correction to failing fields so Claude does not re-extract fields that were already valid, which would reintroduce new errors in previously clean fields.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Complete-code)

We bring the `ValidationResult` dataclass, the four-rule semantic validator, and the retry loop from this lesson into one runnable file. We submit a sample invoice to Claude, run the validator on the extracted output, and see a status line for each attempt before the script returns the final extracted fields.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import anthropic

import json

from dataclasses import dataclass

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = anthropic.Anthropic(api_key=anthropic_api_key)

SYSTEM_PROMPT = """Extract invoice fields from the document and return a JSON object with these keys:

- vendor_name: string

- invoice_total: number (positive)

- issue_date: string (YYYY-MM-DD)

- due_date: string (YYYY-MM-DD)

- currency: string (USD, EUR, GBP, CAD, or AUD)

Return only the JSON object with no extra text."""

SAMPLE_INVOICE = """

INVOICE

Vendor: Acme Supplies Ltd.

Invoice Date: 2024-11-01

Due Date: 2024-11-30

Invoice #: INV-2024-0042

Items:

Office supplies ........... $245.00

Shipping .................. $12.50

Total Due: $257.50 USD

"""

@dataclass

class ValidationResult:

valid:  bool

errors: list

def validate_invoice(raw_input: str, extracted: dict) -> ValidationResult:

errors = []

total = extracted.get("invoice_total")

if total is not None and total < 0:

errors.append(

f"invoice_total is {total}, but invoice totals cannot be negative. "

"Re-read the document and extract the correct positive total.")

issue_date = extracted.get("issue_date", "")

due_date   = extracted.get("due_date",   "")

if issue_date and due_date and issue_date > due_date:

errors.append(

f"issue_date ({issue_date}) is after due_date ({due_date}). "

"The issue date must be on or before the due date. "

"Check both dates in the source document.")

vendor = extracted.get("vendor_name", "").strip()

if not vendor:

errors.append("vendor_name is empty. Locate the vendor or supplier name in the "

"document header and extract it.")

currency = extracted.get("currency", "")

valid_currencies = {"USD", "EUR", "GBP", "CAD", "AUD"}

if currency not in valid_currencies:

errors.append(f"currency is '{currency}', which is not a recognized code. "

f"Use one of: {', '.join(sorted(valid_currencies))}.")

return ValidationResult(valid=len(errors) == 0, errors=errors)

def extract_with_retry(document: str, system_prompt: str, max_retries: int = 3) -> dict | None:

messages = [{"role": "user", "content": document}]

for attempt in range(max_retries):

print(f"  [attempt {attempt + 1}] Calling API...")

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=1024,

system=system_prompt,

messages=messages

)

raw_text = response.content[0].text

try:

extracted = json.loads(raw_text)

except json.JSONDecodeError as e:

feedback = f"The response was not valid JSON: {e}. Return only a JSON object."

print(f"  [attempt {attempt + 1}] JSON parse error — retrying with feedback.")

messages.append({"role": "assistant", "content": raw_text})

messages.append({"role": "user",      "content": feedback})

continue

result = validate_invoice(document, extracted)

if result.valid:

print(f"  [attempt {attempt + 1}] Validation passed.")

return extracted

if attempt == max_retries - 1:

print(f"  [attempt {attempt + 1}] Validation failed on final attempt. Giving up.")

return None

error_list = "\n".join(f"{i+1}. {e}" for i, e in enumerate(result.errors))

feedback = (

"The following errors were found in your extraction:\n\n"

f"{error_list}\n\n"

"Please correct only the fields listed above and return the full updated JSON.")

print(f"  [attempt {attempt + 1}] Validation errors — retrying with feedback.")

messages.append({"role": "assistant", "content": raw_text})

messages.append({"role": "user",      "content": feedback})

return None

if __name__ == "__main__":

print("=== Invoice Extraction with Semantic Validation ===\n")

result = extract_with_retry(SAMPLE_INVOICE, SYSTEM_PROMPT, max_retries=3)

if result:

print("\nExtracted fields:")

for k, v in result.items():

print(f"  {k}: {v}")

else:

print("\nExtraction failed after all retries. Document flagged for human review.")
```

⋯

The validator and retry loop with a sample invoice

The sample invoice has valid dates (issue November 1, due November 30) and a clear vendor name, so Claude’s first extraction will typically pass all four validator rules on the first attempt. To observe the retry behavior, change `Due Date` in the sample to a date before `Invoice Date`. The validator will fire and send specific feedback before the next attempt.

**Expected output for a clean extraction:**

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

=== Invoice Extraction with Semantic Validation ===

[attempt 1] Calling API...

[attempt 1] Validation passed.

Extracted fields:

vendor\_name: Acme Supplies Ltd.

invoice\_total: 257.5

issue\_date: 2024-11-01

due\_date: 2024-11-30

currency: USD

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

If a semantic error is present, additional [attempt N] lines appear with the specific error before validation passes on a later attempt

The validator runs four independent rules and collects all errors before returning. Claude receives the full list in a single retry prompt rather than one error per attempt. The instruction “correct only the fields listed above and return the full updated JSON” prevents Claude from re-extracting already valid fields and introducing new errors.

## When not to retry[#](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#When-not-to-retry)

Retry loops are appropriate for semantic errors in which Claude had the information needed to extract the correct value but made a mistake. They are not appropriate when:

- **The source document does not contain the field:** If `vendor_name` is genuinely absent from the document, retrying with feedback will produce hallucinated values as Claude tries to satisfy the requirement. The validator should distinguish between “extracted but wrong” and “field is absent from the source,” and return the latter as a `data_gap` rather than a validation error that triggers a retry.
- **The same error appears on every attempt:** Two consecutive identical errors indicate a systematic problem in the system prompt or the validator rule, not a one-time extraction mistake. The retry loop should detect repeated identical errors and treat them as a hard failure.
- **The failure is a permission or access error:** A tool call that returns `PERMISSION_DENIED` does not improve with retrying. The retry budget is for semantic correction, not for working around access failures.

## Exercise: Design the feedback[#](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Exercise-Design-the-feedback)

Read each scenario and answer the question about validator design or retry feedback.

Technical Quiz

1.

A validator checks invoice extraction output. The source document says `"Net 30 days"`, and Claude extracts `payment_terms` as `"Net 30 days"`, copied verbatim. The validator has no rule for `payment_terms`. The output is returned as valid, but downstream processing fails because it expects `"NET30"`, `"NET60"`, or `"IMMEDIATE"`. What should the validator add?

A.

A semantic check against the allowed set (`NET30`, `NET60`, `IMMEDIATE`), with feedback listing them

B.

A structural check confirming `payment_terms` is present and non-empty, since the field content already looks reasonable

C.

A retry using the feedback “payment\_terms is wrong, please fix it,” without naming which values are actually acceptable

D.

No validator change; leave normalization to the downstream consumer, since format conversion is business logic, not extraction

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Whats-next)

In the next lesson, we cover batch vs. synchronous processing: when to run extraction workflows synchronously for real-time use cases, when to switch to batch processing for large document volumes, and how the processing mode affects retry strategy, cost, and latency.

Claude Code Configuration and Workflows Assessment Quiz

Batch vs. Synchronous Processing

Ask

[Structural vs. semantic validation](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Structural-vs-semantic-validation)

[Writing a semantic validator](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Writing-a-semantic-validator)

[Generic vs. specific retry feedback](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Generic-vs-specific-retry-feedback)

[The retry loop](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#The-retry-loop)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Complete-code)

[When not to retry](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#When-not-to-retry)

[Exercise: Design the feedback](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Exercise-Design-the-feedback)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/validators-and-retry-feedback#Whats-next)