# Understanding_Batch_and_Synchronous_Processing_for_AI_Tasks

Source: https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Batch vs. Synchronous Processing

Explore the differences between batch and synchronous processing in AI systems, focusing on when each method is appropriate based on latency, volume, and cost. Understand how to implement batch submission and retrieval using the Message Batches API and develop effective retry strategies for failed tasks. This lesson equips you to choose processing modes that align with system requirements and optimize performance and expenses.

We'll cover the following...

- [Choosing the right mode](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Choosing-the-right-mode)
- [Synchronous processing: The baseline](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Synchronous-processing-The-baseline)
- [Batch processing with the Message Batches API](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Batch-processing-with-the-Message-Batches-API)
- [Retrieving batch results](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Retrieving-batch-results)
- [Batch retry strategy](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Batch-retry-strategy)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Complete-code)
- [How processing mode affects cost and latency](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#How-processing-mode-affects-cost-and-latency)
- [Exercise: Choose the right mode](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Exercise-Choose-the-right-mode)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Whats-next)

When Claude processes a single document and returns the result before the next request is sent, that is synchronous processing. When hundreds or thousands of documents are submitted together and results are retrieved after the batch completes, that is batch processing. The correct choice is not a matter of preference; it depends on whether the calling system needs the result immediately, how many documents arrive at once, and what the cost and throughput constraints are. This lesson covers both modes, when each fits, and how the retry pattern from the previous lesson must adapt when individual retries are no longer immediate. By the end of this lesson, we will be able to:

- Identify scenarios where synchronous processing is required and where batch processing is preferred
- Submit a batch of extraction requests using the Message Batches API and retrieve results by `custom_id`
- Explain why the immediate retry loop from the previous lesson does not apply to batch processing
- Design a batch retry strategy that resubmits only failed documents

## Choosing the right mode[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Choosing-the-right-mode)

The decision between synchronous and batch processing turns on three factors: whether a human or downstream system is waiting for the result, how many documents arrive at once, and whether cost optimization matters more than speed.

|  |  |  |
| --- | --- | --- |
| **Factor** | **Use Synchronous** | **Use Batch** |
| Latency requirement | Real-time: a user or API is waiting | Offline: results are needed within hours, not seconds |
| Volume | One document or a small burst | Hundreds to thousands of documents |
| Throughput | Low; one request at a time | High; many requests processed in parallel |
| Cost | Standard API pricing | 50% discount on input and output tokens |
| Retry granularity | Immediate per-document retry in the same loop | Re-submit only failed documents in a follow-up batch |

The 50% cost reduction for batch processing is significant for high-volume workflows. A pipeline that processes 10,000 invoices per day can cut its Claude API costs in half by switching from synchronous to batch processing, at the cost of adding latency from minutes to hours.

## Synchronous processing: The baseline[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Synchronous-processing-The-baseline)

Synchronous processing runs one request at a time and blocks until the response is returned. The retry loop from the previous lesson is an example: each document is extracted, validated, and retried within a single function call before moving to the next document. This pattern suits interactive systems where a user submits a document and waits for the result:

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

import anthropic

import json

client = anthropic.Anthropic()

def process\_document(document: str, system\_prompt: str) -> dict | None:

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=1024,

system=system\_prompt,

messages=[{"role": "user", "content": document}]

)

raw = response.content[0].text

try:

return json.loads(raw)

except json.JSONDecodeError:

return None

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A minimal synchronous extraction call. The function blocks until Claude returns a response. The caller receives a result before any other document is processed.

- **Lines 10–15:** `client.messages.create` is a blocking call. The function does not return until Claude produces a response. For a web API endpoint, this means the HTTP response is held open until extraction completes, which is acceptable for documents that complete in under a few seconds.
- **Lines 16–20:** The JSON parse and return happen in the same function call. If parsing fails, the caller receives `None` immediately and can retry or report the error inline. There is no queuing or deferred result retrieval.

## Batch processing with the Message Batches API[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Batch-processing-with-the-Message-Batches-API)

The Message Batches API accepts a list of requests, each identified by a `custom_id`, and processes them asynchronously. The caller submits the batch, receives a `batch_id`, and polls or waits for completion before retrieving results. Submitting a batch of invoice documents:

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

import anthropic

client = anthropic.Anthropic()

SYSTEM = "Extract invoice fields and return a JSON object."

def submit\_invoice\_batch(documents: list[dict]) -> str:

requests = []

for doc in documents:

requests.append(

anthropic.types.message\_create\_params.MessageCreateParamsNonStreaming(

custom\_id=doc["id"],

params={

"model": "claude-opus-4-8",

"max\_tokens": 1024,

"system": SYSTEM,

"messages": [{"role": "user", "content": doc["text"]}]

}

)

)

batch = client.messages.batches.create(requests=requests)

return batch.id

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A function that builds a list of batch request objects and submits them. Each request carries a custom\_id — the document’s identifier from the caller — so results can be matched back to their source documents when the batch completes.

- **Lines 8–18:** Each document becomes one entry in the `requests` list. `MessageCreateParamsNonStreaming` wraps a standard messages API call with a `custom_id` string. The `custom_id` is the caller's document identifier and is returned alongside the result when the batch completes.
- **Lines 19–20:** `client.messages.batches.create` submits all requests at once and returns a `Batch` object. Only `batch.id` needs to be stored; it is the handle used to poll for status and retrieve results.

## Retrieving batch results[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Retrieving-batch-results)

After submission, the batch moves through `in_progress` to `ended`. The results are retrieved by iterating the batch's result stream, where each item contains the `custom_id`, a `result` type (`succeeded`, `errored`, or `expired`), and the response message if successful.

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

import time

def retrieve\_batch\_results(batch\_id: str) -> dict[str, dict]:

while True:

batch = client.messages.batches.retrieve(batch\_id)

if batch.processing\_status == "ended":

break

time.sleep(60)

extracted = {}

errors = {}

for result in client.messages.batches.results(batch\_id):

cid = result.custom\_id

if result.result.type == "succeeded":

raw = result.result.message.content[0].text

try:

extracted[cid] = json.loads(raw)

except json.JSONDecodeError:

errors[cid] = "json\_parse\_error"

elif result.result.type == "errored":

errors[cid] = result.result.error.error.type

else:

errors[cid] = "expired"

return extracted, errors

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A polling loop that waits for the batch to finish, then separates successful extractions from errors. Successful results are parsed and stored by custom\_id. Failed results record the error type for the retry step.

- **Lines 4–7:** The polling loop checks `processing_status` every 60 seconds. For production systems, exponential backoff or a webhook notification is preferable to a fixed sleep, but fixed polling is acceptable for batch jobs that run overnight or on a schedule.
- **Lines 9–10:** Two separate dicts accumulate successful extractions (`extracted`) and failures (`errors`). Keeping them separate makes the retry step straightforward: only documents in `errors` need to be resubmitted.
- **Lines 12–22:** `client.messages.batches.results(batch_id)` returns an iterable of result objects. Each item has `custom_id` and a `result` field. The `result.type` is `"succeeded"`, `"errored"`, or `"expired"`. Only `succeeded` results contain a `message` with parseable content.
- **Lines 22–23:** An `expired` result means the document was not processed before the batch timed out. It is recorded as an error distinct from an API error, so the retry step can handle it separately if needed.

## Batch retry strategy[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Batch-retry-strategy)

The immediate per-document retry from the previous lesson does not apply to batch processing because results are not available until the whole batch completes. The retry strategy is instead a two-pass approach: run the batch, collect failures, validate successes, and resubmit a second batch containing only the documents that failed or produced invalid extractions.

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

from validate import validate\_invoice

def batch\_pipeline(documents: list[dict], system\_prompt: str) -> dict:

batch\_id = submit\_invoice\_batch(documents)

extracted, api\_errors = retrieve\_batch\_results(batch\_id)

validation\_errors = {}

valid\_results = {}

for doc\_id, result in extracted.items():

doc\_text = next(d["text"] for d in documents if d["id"] == doc\_id)

vr = validate\_invoice(doc\_text, result)

if vr.valid:

valid\_results[doc\_id] = result

else:

validation\_errors[doc\_id] = vr.errors

failed\_ids = set(api\_errors) | set(validation\_errors)

retry\_docs = [d for d in documents if d["id"] in failed\_ids]

if retry\_docs:

retry\_batch\_id = submit\_invoice\_batch(retry\_docs)

retry\_extracted, retry\_err = retrieve\_batch\_results(retry\_batch\_id)

for doc\_id, result in retry\_extracted.items():

doc\_text = next(d["text"] for d in documents if d["id"] == doc\_id)

vr = validate\_invoice(doc\_text, result)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A two-pass batch pipeline. The first batch processes all documents. The second batch re-submits only the documents that produced API errors or failed semantic validation. Documents that fail twice are not retried and are excluded from the final result.

- **Lines 4–5:** The first batch is submitted, and results are retrieved as two separate dicts: successful extractions and API-level errors.
- **Lines 9–16:** Each successful extraction is semantically validated using `validate_invoice` from the previous lesson. Extractions that pass go into `valid_results`; those that fail go into `validation_errors` alongside the error list.
- **Lines 18–19:** The set of documents needing a retry combines API errors and validation failures. Set union handles the case where a document had both an API error and a prior validation failure, ensuring it appears in the retry batch only once.
- **Lines 21–27:** The retry batch is submitted, and the results are validated again. Documents that pass on the second attempt are added to `valid_results`. Documents that fail twice are silently excluded; the caller can compare the `valid_results` keys against the original document list to find unresolved failures.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Complete-code)

We bring the batch submit function, the polling retriever, the inline semantic validator, and the two-pass pipeline from this lesson into one runnable file. We submit three sample invoices as a single batch, poll until the batch ends, validate each result, and retry only the documents that failed.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import anthropic

import json

import time

from dataclasses import dataclass

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = anthropic.Anthropic(api_key=anthropic_api_key)

SYSTEM = ("Extract invoice fields and return a JSON object with keys: "

"vendor_name, invoice_total (number), issue_date (YYYY-MM-DD), "

"due_date (YYYY-MM-DD), currency (USD/EUR/GBP/CAD/AUD). "

"Return only the JSON object.")

SAMPLE_DOCUMENTS = [

{"id": "inv-001",

"text": "Vendor: Acme Ltd. Invoice Date: 2024-11-01. Due: 2024-11-30. Total: $257.50 USD."},

{"id": "inv-002",

"text": "Supplier: Beta Corp. Invoice Date: 2024-10-15. Due: 2024-11-14. Amount: €890.00 EUR."},

{"id": "inv-003",

"text": "From: Gamma Inc. Date: 2024-09-20. Payment due: 2024-10-20. Total: GBP 1,200.00."},

]

@dataclass

class ValidationResult:

valid:  bool

errors: list

def validate_invoice(raw_input: str, extracted: dict) -> ValidationResult:

errors = []

total = extracted.get("invoice_total")

if total is not None and total < 0:

errors.append(f"invoice_total is {total} — must be positive.")

issue_date = extracted.get("issue_date", "")

due_date   = extracted.get("due_date",   "")

if issue_date and due_date and issue_date > due_date:

errors.append(f"issue_date ({issue_date}) is after due_date ({due_date}).")

vendor = extracted.get("vendor_name", "").strip()

if not vendor:

errors.append("vendor_name is empty.")

currency = extracted.get("currency", "")

if currency not in {"USD", "EUR", "GBP", "CAD", "AUD"}:

errors.append(f"currency '{currency}' is not a recognized code.")

return ValidationResult(valid=len(errors) == 0, errors=errors)

def submit_invoice_batch(documents: list[dict]) -> str:

requests = []

for doc in documents:

requests.append(

anthropic.types.message_create_params.MessageCreateParamsNonStreaming(

custom_id=doc["id"],

params={

"model":      "claude-opus-4-8",

"max_tokens": 512,

"system":     SYSTEM,

"messages":   [{"role": "user", "content": doc["text"]}]

}

)

)

batch = client.messages.batches.create(requests=requests)

print(f"  Batch submitted: {batch.id} ({len(requests)} requests)")

return batch.id

def retrieve_batch_results(batch_id: str) -> tuple[dict, dict]:

print(f"  Polling batch {batch_id}...")

while True:

batch = client.messages.batches.retrieve(batch_id)

if batch.processing_status == "ended":

break

print(f"    Status: {batch.processing_status} — waiting 10s...")

time.sleep(10)

extracted = {}

errors    = {}

for result in client.messages.batches.results(batch_id):

cid = result.custom_id

if result.result.type == "succeeded":

raw = result.result.message.content[0].text

try:

extracted[cid] = json.loads(raw)

except json.JSONDecodeError:

errors[cid] = "json_parse_error"

elif result.result.type == "errored":

errors[cid] = result.result.error.error.type

else:

errors[cid] = "expired"

print(f"  Retrieved: {len(extracted)} succeeded, {len(errors)} failed")

return extracted, errors

def batch_pipeline(documents: list[dict]) -> dict:

print("\n--- Pass 1: full batch ---")

batch_id              = submit_invoice_batch(documents)

extracted, api_errors = retrieve_batch_results(batch_id)

validation_errors = {}

valid_results     = {}

for doc_id, result in extracted.items():

doc_text = next(d["text"] for d in documents if d["id"] == doc_id)

vr = validate_invoice(doc_text, result)

if vr.valid:

valid_results[doc_id] = result

else:

validation_errors[doc_id] = vr.errors

failed_ids = set(api_errors) | set(validation_errors)

retry_docs = [d for d in documents if d["id"] in failed_ids]

if retry_docs:

print(f"\n--- Pass 2: retry batch ({len(retry_docs)} documents) ---")

retry_batch_id             = submit_invoice_batch(retry_docs)

retry_extracted, retry_err = retrieve_batch_results(retry_batch_id)

for doc_id, result in retry_extracted.items():

doc_text = next(d["text"] for d in documents if d["id"] == doc_id)

vr = validate_invoice(doc_text, result)

if vr.valid:

valid_results[doc_id] = result

else:

print("\n  All documents passed on first pass — no retry needed.")

return valid_results

if __name__ == "__main__":

print("=== Batch Invoice Extraction Pipeline ===\n")

print(f"Submitting {len(SAMPLE_DOCUMENTS)} documents...\n")

results = batch_pipeline(SAMPLE_DOCUMENTS)

print(f"\n=== Final results: {len(results)}/{len(SAMPLE_DOCUMENTS)} succeeded ===")

for doc_id, fields in results.items():

print(f"\n  {doc_id}:")

for k, v in fields.items():

print(f"    {k}: {v}")

unresolved = [d["id"] for d in SAMPLE_DOCUMENTS if d["id"] not in results]

if unresolved:

print(f"\n  Unresolved after two passes: {unresolved}")

print("  These documents should be flagged for human review.")
```

⋯

The complete two-pass batch pipeline

Batch jobs are asynchronous; the polling loop prints a status line every 10 seconds until the batch ends. Total elapsed time is typically 30–90 seconds for a three-document batch.

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

=== Batch Invoice Extraction Pipeline ===

Submitting 3 documents...

--- Pass 1: full batch ---

Batch submitted: msgbatch\_01Abc... (3 requests)

Polling batch msgbatch\_01Abc...

Status: in\_progress — waiting 10s...

Status: in\_progress — waiting 10s...

Retrieved: 3 succeeded, 0 failed

All documents passed on first pass — no retry needed.

=== Final results: 3/3 succeeded ===

inv-001:

vendor\_name: Acme Ltd.

invoice\_total: 257.5

issue\_date: 2024-11-01

due\_date: 2024-11-30

currency: USD

inv-002:

vendor\_name: Beta Corp

invoice\_total: 890.0

issue\_date: 2024-10-15

due\_date: 2024-11-14

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Batch IDs and timing vary per run; field values are deterministic for the sample documents

If any document fails validation after the first pass, a “Pass 2” block appears, with only the failing IDs resubmitted as a new batch. Documents that fail both passes are listed in the `Unresolved` line at the bottom and flagged for human review.

## How processing mode affects cost and latency[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#How-processing-mode-affects-cost-and-latency)

The trade-off between synchronous and batch processing is not just architectural; it has measurable cost and latency consequences that must match the business requirement.

Synchronous processing costs full API rates and returns results in seconds. It is the only viable option when a user or system is waiting for the result inline.

Batch processing costs half the API rate and returns results when the batch completes, which can take minutes to hours depending on batch size and API load. It is the correct choice for:

- Nightly document ingestion pipelines
- Backfill operations over historical documents
- Non-urgent analytics extraction over large corpora
- Any workflow where results feed a downstream job that runs on a schedule

Using synchronous processing for 10,000 documents when batch processing would work is a common and expensive mistake. The rate is the same per token, but the 50% batch discount applies to every input and output token across all documents, making the cost difference substantial at scale.

## Exercise: Choose the right mode[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Exercise-Choose-the-right-mode)

For each scenario, decide whether synchronous or batch processing fits, and explain the key factor that drives the choice.

Technical Quiz

1.

A customer support portal lets users upload invoices and see extracted fields displayed in real time on the page. The user waits for the result before they can proceed. Which processing mode is required?

A.

Batch processing, because invoice extraction is a high-volume operation

B.

Batch processing with a short polling interval so results appear quickly

C.

Synchronous, because the user is waiting for the result to proceed

D.

Either mode works; the choice does not matter for this use case

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Whats-next)

In the next lesson, we cover task-specific quality metrics: how to split evaluation by document type, extraction field, confidence level, and workflow stage, and why single aggregate accuracy scores hide the failure patterns that matter most in production.

Validators and Retry Feedback

Task-Specific Quality Metrics

Ask

[Choosing the right mode](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Choosing-the-right-mode)

[Synchronous processing: The baseline](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Synchronous-processing-The-baseline)

[Batch processing with the Message Batches API](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Batch-processing-with-the-Message-Batches-API)

[Retrieving batch results](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Retrieving-batch-results)

[Batch retry strategy](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Batch-retry-strategy)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Complete-code)

[How processing mode affects cost and latency](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#How-processing-mode-affects-cost-and-latency)

[Exercise: Choose the right mode](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Exercise-Choose-the-right-mode)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/batch-vs-synchronous-processing#Whats-next)