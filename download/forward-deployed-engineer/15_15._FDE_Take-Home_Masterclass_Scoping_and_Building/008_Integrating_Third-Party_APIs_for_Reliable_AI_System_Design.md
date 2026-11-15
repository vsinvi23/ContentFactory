# Integrating_Third-Party_APIs_for_Reliable_AI_System_Design

Source: https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Integrating Third-Party APIs

Explore how to read an API contract before writing a client, covering pagination, error meanings, rate limits, and write guarantees. Understand how to classify failures, bound retries, and use stable idempotency keys so a lost response never creates a duplicate, preparing you to build integrations that fail safely.

We'll cover the following...

- [Defining the integration goal](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Defining-the-integration-goal)
- [Reading the API contract](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Reading-the-API-contract)
- [Handling pagination safely](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Handling-pagination-safely)
- [Which failures deserve another request?](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Which-failures-deserve-another-request)
- [Using stable idempotency keys](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Using-stable-idempotency-keys)
- [Testing with fake services](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Testing-with-fake-services)
- [Practice: The warehouse API](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Practice-The-warehouse-API)

The service creates review batch `B70`, but the response is lost before reaching the client. The client times out while waiting for the response. The service committed the batch, but the client cannot determine whether the operation succeeded because it received no response. Retrying the request could return the existing result or create a duplicate batch, depending on the service's idempotency guarantees.

Build reliable integrations by validating requests and responses against the API contract, limiting retry attempts, and verifying whether operations are safe to repeat. A generic retry decorator cannot determine whether repeating a request will cause unintended side effects.

## Defining the integration goal[#](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Defining-the-integration-goal)

A support manager needs one review batch containing every open case in a fixed snapshot. The assignment has two steps:

1. Retrieve all open cases from snapshot snap-17.
2. Create one review batch containing their IDs.

A successful HTTP response satisfies neither step on its own. An incomplete export could omit a case; a repeated create could assign the same work twice. Unlike a local file write, this output changes a remote system, so a timeout needs careful handling.

## Reading the API contract[#](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Reading-the-API-contract)

An **integration contract** defines authentication requirements, request and response schemas, pagination, error handling, rate limits, and idempotency guarantees for write operations. Review the contract before implementing the client to identify required behavior and integration constraints.

Use the following fictional API contract:

- **Access:** Live mode requires `SUPPORT_API_BASE_URL` and a bearer token stored in `SUPPORT_API_TOKEN`. If either value is missing, fail validation before making a network request.
- **Retrieval:** Request `GET /cases?snapshot_id=snap-17&status=open` without a `cursor` parameter. For subsequent pages, include the `cursor` value returned by the previous response.
- **Page schema:** Each response must contain `items`, `snapshot_id`, and `next_cursor`. Every item must have a nonempty string `id` and `status` set to `open`. The `next_cursor` value must be a nonempty string or `null` for the final page.
- **Snapshot:** The `snap-17` snapshot remains fixed, and each matching case appears exactly once across its pages.
- **Create:** Send `POST /review-batches` with `snapshot_id` and `case_ids` in the request body and `Idempotency-Key` in the request header. The response must include `batch_id`.
- **Duplicate protection:** Within 24 hours, repeating a request with the same idempotency key and payload returns the original batch. Reusing the key with a different payload returns HTTP `409 Conflict`.

Keep credentials in environment variables, never in source code or committed fixtures. A .env.example file can name the variables with placeholder values. Don’t print raw exception text or response bodies in error messages, since they can leak headers or customer data; report a short error category instead.

## Handling pagination safely[#](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Handling-pagination-safely)

The first page returns `C11` and `C12` with `next_cursor="c2"`. The second page returns `C13` with `next_cursor=null`.

Validate each complete page against the response schema before accepting its records. Do not expose the collected IDs until a valid response returns `next_cursor=null`. Prevent infinite pagination loops by tracking previously used cursors and enforcing a maximum of ten pages. If pagination requires an eleventh page, report a page-limit error instead of returning incomplete results.

Identify the expected API requests and results for both valid and malformed final-page responses.

A successful retrieval returns exactly three case IDs: `C11`, `C12`, and `C13`. A missing `next_cursor` field violates the response contract. An explicit `next_cursor=null` indicates that retrieval is complete.

If any page fails validation, abort retrieval without publishing an export or sending a batch-creation request. Without this safeguard, a malformed second page could cause a partial result containing only two cases to be incorrectly reported as complete.

Retrieving all pages establishes completeness under the contract's fixed-snapshot guarantee. Paginating through a changing dataset does not independently guarantee a consistent result.

## Which failures deserve another request?[#](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Which-failures-deserve-another-request)

Apply the following retry rules based on the API response:

- **400, 401, 403, 409:** Do not retry. Repeating an unchanged request will not resolve invalid parameters, authentication failures, insufficient permissions, or idempotency-key conflicts.
- **429:** Retry after the specified delay, provided the `Retry-After` header contains a valid nonnegative integer representing seconds. Treat a missing or invalid header as a contract violation.
- **503 and request time-outs:** Retry only when the operation is safe to repeat under the API's idempotency guarantees.
- **Other responses:** Stop and report the outcome. Do not retry unspecified failures automatically.

Enforce the following request limits:

1. **Request time-out:** Set a five-second timeout for each attempt to prevent an unresponsive request from blocking execution indefinitely.
2. **Attempt limit:** Allow a maximum of three attempts per request, including the initial attempt.

For HTTP `429`, wait for the full delay specified by `Retry-After` before retrying. If the delay exceeds the configured ten-second wait limit, stop and report the failure without retrying.

For HTTP `503` and request timeouts, apply backoff delays of one second before the second attempt and two seconds before the third. Inject the sleep function into the client so tests can verify retry delays without introducing real wait times.

Do not apply this retry policy to other APIs without checking their contracts. For example, GitHub may return HTTP `403` or `429` for rate limiting and provides rate-limit information through headers such as `Retry-After` and `X-RateLimit-Reset`. Its guidance requires clients to respect the specified delay and limit repeated requests.

## Using stable idempotency keys[#](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Using-stable-idempotency-keys)

**Idempotency** ensures that repeating an operation does not produce additional side effects after the first successful execution. An idempotency key prevents duplicate operations only when the service provides a documented guarantee.

Generate the idempotency key before entering the retry loop. Reuse the same key and unchanged payload for every attempt. For this example, use idempotency key `op-72` and payload `{"snapshot_id":"snap-17","case_ids":["C11","C12","C13"]}`.

Trace the request sequence and resulting service state:

1. **Client, attempt 1:** Sends the payload with idempotency key `op-72`.
2. **Service:** Creates batch `B70` and associates the result with idempotency key `op-72`.
3. **Network:** The response is lost in transit. The client times out without receiving the batch ID.
4. **Client, attempt 2:** Waits one second, then retries with the unchanged payload and idempotency key `op-72`.
5. **Service:** Recognizes the existing idempotency key and returns batch `B70` without creating a duplicate.
6. **Client:** Receives `batch_id="B70"`. The service contains exactly one batch.

Two implementation errors can bypass idempotency protection:

- **Regenerating the key on retry:** The first attempt uses `op-72` and creates `B70`. The second uses `op-73` and creates `B71`. The service treats the requests as separate operations, resulting in duplicate batches.
- **Retrying a POST without idempotency guarantees:** Without a documented idempotency guarantee, reusing the key does not establish retry safety. If the request times out, stop automatic retries and report the outcome as unknown.

If a write times out without confirmation, report `write_outcome_unknown` rather than `failed`, because the operation may have committed. Retain the idempotency key and a safe reference to the request payload for reconciliation with the provider.

Idempotency guarantees differ across API providers and versions. For example, Stripe API v1 can return the stored response for a repeated idempotency key, including HTTP `500` responses. Keys may expire after 24 hours, and reusing a key with different parameters produces an error. API v2 uses different idempotency behavior. Verify idempotency behavior against the documentation for the specific API and version in use.

## Testing with fake services[#](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Testing-with-fake-services)

Use a **fake service** to simulate response loss deterministically. An in-memory implementation lets you control request outcomes. A stateful fake can verify that a batch was committed before the response was lost. A sequence of predefined responses alone cannot verify the service's internal state.

The following three files use only the Python 3.10+ standard library. The client accepts any object that implements a `request()` method, allowing tests to inject a fake service. These examples use simulated responses and do not implement live networking. Document this limitation in the README.

Run `python3 fake_support_service.py` to execute the example, and `python3 -m unittest -v test_support_api` to run the tests. On Windows, replace `python3` with `py`.

Before reviewing the tests, predict the request sequence, retry delays, and total number of batches created.

Python 3.14.0

```
"""In-memory stand-in for the support API. Nothing here touches a network.

Running this file prints the worked example (fixture mode only)."""

import json

from support_api import Response, SupportClient

PAGES = {

None: {"items": [{"id": "C11", "status": "open"}, {"id": "C12", "status": "open"}],

"snapshot_id": "snap-17", "next_cursor": "c2"},

"c2": {"items": [{"id": "C13", "status": "open"}],

"snapshot_id": "snap-17", "next_cursor": None},

}

class FakeSupportService:

def __init__(self, script=None, honors_keys=True, lose_first_create_response=False):

self.script = list(script or [])

self.honors_keys = honors_keys

self.lose_response = lose_first_create_response

self.calls = []

self.batches = {}

self.saved = {}

def request(self, method, path, params, headers, payload, timeout):

key = headers.get("Idempotency-Key")

self.calls.append({"method": method, "cursor": params.get("cursor"), "key": key, "payload": payload})

scripted = self.script.pop(0) if self.script else None

if isinstance(scripted, Exception):

raise scripted

if scripted is not None:

return scripted

if method == "GET":

return Response(200, json.loads(json.dumps(PAGES[params.get("cursor")])))

if self.honors_keys and key in self.saved:

saved_payload, batch_id = self.saved[key]

return Response(200, {"batch_id": batch_id}) if saved_payload == payload else Response(409)

batch_id = "B" + str(70 + len(self.batches))

self.batches[batch_id] = payload

if self.honors_keys:

self.saved[key] = (payload, batch_id)

if self.lose_response:

self.lose_response = False

raise TimeoutError("response lost after the batch was stored")

return Response(201, {"batch_id": batch_id})

def worked_example():

fake = FakeSupportService([Response(429, headers={"Retry-After": "2"})], lose_first_create_response=True)

waits = []

client = SupportClient(fake, sleep=waits.append, new_key=lambda: "op-72")

case_ids, batch_id = client.run()

return fake, waits, case_ids, batch_id

if __name__ == "__main__":

fake, waits, case_ids, batch_id = worked_example()

print("Mode: fixture (simulated); live verification not performed")

print("GET cursors:", [c["cursor"] for c in fake.calls if c["method"] == "GET"])

print("Case IDs:", case_ids, "| Waits:", waits)

print("POST keys:", [c["key"] for c in fake.calls if c["method"] == "POST"])

print("Batch returned:", batch_id, "| Batches stored:", list(fake.batches))
```

⋯

The `support_api.py` holds every decision from this lesson:

- `valid_page` checks the whole page (snapshot, required fields, item shape, duplicate IDs) before any ID is accepted.
- `fetch_case_ids` follows cursors, rejects a reused cursor, stops after ten pages, and returns only when it sees an explicit null.
- `send` and classify handle each response: return on 200 or 201, stop on terminal statuses, wait the full Retry-After for 429, and back off one then two seconds for 503 and timeouts, for at most three attempts.
- `create_batch` builds the key and payload once, so every POST attempt reuses them.
- `Errors` carry a short category; after a timed-out write, any failure becomes write\_outcome\_unknown with the key and payload attached.

The `fake_support_service.py` stores the batch *before* raising the timeout. That ordering is what makes a timeout compatible with a committed write.

For the worked example, the expected evidence is:

- `GET requests`**:** First page (receives 429 with Retry-After: 2), first page again, then cursor C2
- `IDs:` Exactly C11, C12, C13
- `POST attempts:` Two, both with key op-72 and identical payloads
- `Batches created`**:** One, B70
- `Waits:` [2, 1], two seconds for the rate limit and one before the POST retry
- `Label:` Fixture mode; live verification not performed

The six tests cover the cases that matter most: the full worked trace, a malformed page that must never reach POST, a 401 that gets exactly one attempt, a 429 that waits the full delay (or stops when the delay is too long), a reused key that creates one batch while a new key creates two, and an unprotected POST that stops with write\_outcome\_unknown instead of retrying. The decisive check for the write is the fake’s batch count, not just a successful final response.

Passing tests show the client follows the modeled contract. A quick live check against a real sandbox would show only that your credentials and endpoint worked once; it complements these tests rather than replacing them.

## Practice: The warehouse API[#](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Practice-The-warehouse-API)

Consider the following independent warehouse API contract:

- `GET /orders?page=N` starts at page 1 and returns `orders`, a list of string IDs, and `has_more`, a boolean. An empty `orders` list does not end pagination when `has_more=true`.
- Retry GET requests that return HTTP `502`. Treat HTTP `401` as terminal. Allow no more than two attempts per request, including the initial attempt.
- The contract does not guarantee idempotency for `POST /dispatches`.

The scripted responses are:

- page 1 returns `orders=["O8"]` and `has_more=true.`
- page 2 returns `orders=[]` and `has_more=true.`
- page 3 initially returns HTTP `502`, then succeeds with `orders=["O9"]` and `has_more=false`. The service creates dispatch `D8`, but the client times out before receiving the response.

Draft an independent execution plan before reviewing the proposed analysis. Specify the GET request sequence, complete set of retrieved order IDs, pagination termination condition, and safe handling of the POST timeout. Explain how the client should handle a page 2 response that omits the required `has_more` field.

Apply the same integration principles across APIs: validate responses, limit retry attempts, and verify whether write operations are safe to repeat. Each API contract defines its pagination termination conditions, retryable errors, and idempotency guarantees. Document these decisions before implementing retry logic.

Working with Messy Data

Building LLM-Powered Solutions

Ask

[Defining the integration goal](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Defining-the-integration-goal)

[Reading the API contract](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Reading-the-API-contract)

[Handling pagination safely](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Handling-pagination-safely)

[Which failures deserve another request?](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Which-failures-deserve-another-request)

[Using stable idempotency keys](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Using-stable-idempotency-keys)

[Testing with fake services](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Testing-with-fake-services)

[Practice: The warehouse API](https://www.educative.io/courses/forward-deployed-engineer/integrating-third-party-apis#Practice-The-warehouse-API)