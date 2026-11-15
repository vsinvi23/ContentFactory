# FDE_System_Design_for_Pipelines_Reliability_and_Access_Control

Source: https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# FDE System Design: Pipelines, Reliability, and Access Control

Design reliable FDE systems by defining user promises, assigning clear responsibilities, and implementing robust error handling. Establish access controls, manage data freshness, and account for delayed updates and concurrent edits. Validate operations, enforce authorization, track data provenance, manage versioning, and use atomic transactions to prevent inconsistencies. Connect user expectations to concrete enforcement mechanisms and verifiable evidence of compliance.

We'll cover the following...

- [Start with promises, not components](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Start-with-promises-not-components)
- [The smallest useful architecture](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#The-smallest-useful-architecture)
- [Getting changes in within five minutes](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Getting-changes-in-within-five-minutes)
- [Writing safely: The K42 operation](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Writing-safely-The-K42-operation)
- [When the response is lost](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#When-the-response-is-lost)
- [Signals, Containment, and Recovery](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Signals-Containment-and-Recovery)
  - [Common system-design follow-ups](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Common-system-design-follow-ups)

A coordinator must see current stock and request an authorized replenishment. An outside partner must never receive internal notes. A system design has to explain how those promises survive delayed data, concurrent edits, lost responses and exports.

A correct function can’t supply those guarantees on its own. A defensible design connects every promise the user can see to three things: where it is enforced, what evidence is stored, and what happens when it fails.

## Start with promises, not components[#](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Start-with-promises-not-components)

Write the acceptance test first. An east-depot coordinator sees sufficiently current availability, requests a permitted change, and gets either a confirmed outcome or an explicit “unresolved” state. A partner receives only approved information.

Then work through five steps:

1. Clarify the actor, the permitted change, the authoritative inputs, the freshness needed, the failure tolerance and the disclosure boundaries.
2. Trace the data a read needs and the command a write sends.
3. Assign each responsibility, the state it owns, and its inputs and outputs.
4. Specify failure, recovery, and security behavior.
5. Challenge each guarantee with a concrete scenario.

**Latency** is how long an operation takes. **Freshness** is how current the data behind the answer is. A query can return in 100 milliseconds and still show yesterday’s stock.

Ask about record volume, change rate, concurrent users, the read/write mix, and the source API’s capabilities. Can the source list changes, give versions and deletion markers, and resume from a cursor? Record supplied values separately from your assumptions. If no scale is given, don’t invent millions of records or propose sharding.

## The smallest useful architecture[#](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#The-smallest-useful-architecture)

The example is invented practice, not a verified interview question. Stock owns item availability, and Dispatch owns delivery status. An approved mapping links `Stock:S31` to `Dispatch:D88`, and an east-depot coordinator may copy availability from one to the other.

|  |  |  |
| --- | --- | --- |
| **Responsibility** | **Owns** | **Returns** |
| Ingestion and validation | Source records, versions, cursor, quarantine | Accepted records, or rejections with reasons |
| Caller authorization | Who may read or command what | Permitted view, or explicit denial |
| Permission enforcement and operation store | Accepted requests and their outcomes | Pending, unknown, or confirmed |
| Target adapter | Translation to Dispatch’s write contract | Target evidence of the outcome |
| Disclosure control | Approved partner fields and recipients | An allowlisted release |

The boxes are logical responsibilities. They can start inside one application with background workers rather than as separate services. A read goes through authorization to a validated state, and returns permitted fields plus their age. A write is checked, stored as an operation, and sent through the adapter, and only target evidence confirms it.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27831%27%20height=%27541%27/%3e)![Dispatch and stock data pass through validation, permissions, and release](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Dispatch and stock data pass through validation, permissions, and release")

Dispatch and stock data pass through validation, permissions, and release

Naming a queue guarantees nothing. What matters is what the messages contain, who owns them, and what happens when they fail.

## Getting changes in within five minutes[#](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Getting-changes-in-within-five-minutes)

Suppose the freshness requirement is five minutes end to end. Stock supports polling for changed records, so poll every minute. One candidate budget: 1 minute for the source to publish, 1 minute waiting for the poll, 2 for retrieval and validation, and 1 to publish and serve, for 1 + 1 + 2 + 1 = 5. These are assumptions to measure, not guarantees.

|  |  |  |
| --- | --- | --- |
| **Ingestion Style** | **Fits When** | **Cost** |
| Full batch reload | The source is small enough to reload within the budget | Simple, but repeats work |
| Changed-record polling | The source can list changes and resume from a cursor | Needs a durable cursor and replay rules |
| Streaming | Freshness needs seconds, and the source emits events | Most moving parts to operate |

Changed-record polling fits here because the source supports it and the budget allows it.

Each landed record keeps its source, version, event time, retrieval time, and batch identity. Publish only after validating required fields, types, approved identities, and allowed values. Advance the cursor only together with the stored input, so a crash can’t skip changes.

Rules that keep data honest:

- **Order by source version, not arrival time.** Once `S31/v11` is accepted, a late-arriving `v10` can’t replace it.
- **Quarantine unexplained changes.** If availability strings suddenly become numeric codes, hold those records until the meaning is agreed. Otherwise `1` could become a confident but wrong answer.
- **Show last-known-good data with its age.** A rejected update must not leave an old value labeled as current. Block commands that need data you can’t revalidate.
- **A partial poll proves nothing about deletions.** Only an explicit deletion marker from Stock deactivates the mapping.

In Foundry, dataset transactions such as SNAPSHOT (replace) and APPEND (add only) affect incremental pipelines, and a declared schema doesn’t guarantee that the files conform. Domain validation still needs explicit checks. A committed dataset transaction also doesn’t cover an external write to Dispatch. Keep that evidence separate.

## Writing safely: The K42 operation[#](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Writing-safely-The-K42-operation)

Current records: `Stock:S31/v11` shows `Available`, and `Dispatch:D88/v6` shows `Unavailable` with delivery status `Loaded`.

The coordinator requests operation `K42`. Its stored request is fixed: the mapping, source version 11, desired availability `Available` and expected target version 6. Before sending, revalidate the caller’s authority, the mapping and the source state. The adapter sends only the availability field. It never touches delivery status.

- **Guard succeeds:** Dispatch checks version 6, sets availability, keeps `Loaded` and moves to version 7.
- **A concurrent edit wins first:** Dispatch is past version 6, so the write fails without overwriting anything. Refresh and get a new confirmation rather than weakening the guard.

A Dispatch echo of the copied availability isn’t new Stock authority. Track where a value came from, so the sync doesn’t loop.

## When the response is lost[#](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#When-the-response-is-lost)

The tempting design sends the update, then sets a local `processed = true` flag. If Dispatch commits and the app crashes before setting the flag, the effect happened, but the record says it didn’t. Retrying under a new key `K43` could repeat it.

Assume Dispatch offers a stronger contract, and say so explicitly:

- It stores the effect and the result for key `K42` together, atomically.
- Reusing `K42` with a different payload is rejected.
- A repeated `K42` returns the stored result before the version check runs.
- Results are kept for an agreed retry window.

|  |  |  |
| --- | --- | --- |
| **Step** | **Local State** | **Dispatch State** |
| 1. Store request, then send | K42 accepted | v6 |
| 2. Dispatch commits | K42 accepted | v7, K42 → success |
| 3. Response lost | K42 unknown | v7, K42 → success |
| 4. Retry identical K42 | K42 confirmed, v7 | Unchanged, stored result returned |

Editing the expected version to 7, changing the payload, or creating `K43` would be a *new* attempt, not a recovery of the old one.

**Practice:** Recover an unknown outcome. The fake Dispatch below implements the contract above. The operation’s response is lost. Complete `recover` so the operation is confirmed, and the change is applied exactly once.

Python 3.14.0

```
class Dispatch:

"""Fake target: conditional write, with idempotency results stored alongside the effect."""

def __init__(self):

self.version = 6

self.availability = "Unavailable"

self.status = "Loaded"

self.effects = 0

self.results = {}

def apply(self, key, payload):

if key in self.results:

stored_payload, result = self.results[key]

if stored_payload != payload:

return ("rejected", "key reused with a different payload")

return result

if payload["expected_version"] != self.version:

return ("conflict", self.version)

self.availability = payload["availability"]

self.version += 1

self.effects += 1

result = ("success", self.version)

self.results[key] = (payload, result)

return result

def recover(ops, dispatch, key):

op = ops[key]

# TODO: if op["state"] is "unknown", resend the SAME key with the SAME payload.

#       On "success", set state to "confirmed" and record the target version.

#       Any other result means "needs review". Never invent a new key or edit the payload.
```

⋯

Recover a lost response without repeating the change.

Without that contract, a local duplicate table can’t close the gap between the target committing and your process crashing. A version guard alone may block a second write, but a conflict doesn’t prove who changed the target. Reconcile from target history or operator review, keep the outcome marked “unknown” if the evidence is missing, and never promise exactly-once effects. Recheck permission before any retry that could make a new change. Once the retry window expires, retries lose their guarantee.

## Signals, Containment, and Recovery[#](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Signals-Containment-and-Recovery)

|  |  |  |
| --- | --- | --- |
| **Signal** | **Containment** | **Recover When** |
| Coverage age over 5 minutes | Mark the view stale and block commands that need current data | Coverage and validity are restored |
| Operation pending past its deadline | Keep it pending or unknown, and check the target before resending | The outcome is reconciled |
| Quarantine rate above baseline | Isolate affected records and publish no guesses | The data contract is agreed |
| Pipeline failure or abnormal duration | Route to the pipeline owner with stage and scope | The schedule and outputs are healthy |

Technical Quiz

1.

A dashboard loads in 80 milliseconds, but the stock it shows is from yesterday. Which statement is correct?

A.

The system is fast, so it meets a five-minute freshness requirement.

B.

Latency is low, but freshness is poor. They are different properties.

C.

Freshness and latency are the same measure.

D.

Caching would make the data current.

---

1 / 2

### Common system-design follow-ups[#](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Common-system-design-follow-ups)

Interviewers often test a design with follow-ups like these.

1.

Why not use streaming?

Show Answer

1 / 5

The decisive test is the lost-response case. A design earns its diagram when it preserves what is known, exposes what is unknown, and recovers only under guarantees the target actually supplies. Next, the same approach is applied to a complete operational design with trade-offs made end to end.

The Coding Round: User Needs and Changing Requirements

Case Study: Designing an Operational System With Trade-offs

Ask

[Start with promises, not components](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Start-with-promises-not-components)

[The smallest useful architecture](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#The-smallest-useful-architecture)

[Getting changes in within five minutes](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Getting-changes-in-within-five-minutes)

[Writing safely: The K42 operation](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Writing-safely-The-K42-operation)

[When the response is lost](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#When-the-response-is-lost)

[Signals, Containment, and Recovery](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Signals-Containment-and-Recovery)

[Common system-design follow-ups](https://www.educative.io/courses/forward-deployed-engineer/fde-system-design-pipelines-reliability-and-access-control#Common-system-design-follow-ups)