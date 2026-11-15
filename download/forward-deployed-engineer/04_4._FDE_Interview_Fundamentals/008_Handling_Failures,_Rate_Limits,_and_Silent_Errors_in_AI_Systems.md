# Handling_Failures,_Rate_Limits,_and_Silent_Errors_in_AI_Systems

Source: https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Handling Failures, Rate Limits, and Silent Errors

Explore how integrations fail, from timeouts and rate limits to calls that succeed without finishing the job. Learn how to decide which failures earn a retry, how idempotency and durable state make retries safe, and how retries share limited capacity. Understand how to detect silent errors and who repairs what cannot be retried.

We'll cover the following...

- [What evidence makes S204 ready](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#What-evidence-makes-S204-ready)
- [Which failures earn another attempt](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Which-failures-earn-another-attempt)
- [Retries alongside 20 live shipments per minute](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Retries-alongside-20-live-shipments-per-minute)
- [Following a timed-out A1 safely with A2](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Following-a-timed-out-A1-safely-with-A2)
- [How B77 survives a failed dispatch update](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#How-B77-survives-a-failed-dispatch-update)
- [Who repairs S205 and who authorizes replay](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Who-repairs-S205-and-who-authorizes-replay)
- [Noticing an HTTP 200 with a pending label](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Noticing-an-HTTP-200-with-a-pending-label)
- [Practice: Recovering Nacre’s badge job without copying Tern](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Practice-Recovering-Nacres-badge-job-without-copying-Tern)

Tern Dispatch’s workers are healthy, yet shipment S204 is still pending after a courier request timed out. Recovery must establish what happened remotely and finish the shipment without booking it twice. This is the evidence problem behind a reliable integration and behind a convincing interview answer.

## S204: Opening Evidence

|  |  |  |
| --- | --- | --- |
| **Observation** | **What It Establishes** | **What Remains Unknown** |
| All workers healthy | Process availability | Business progress |
| Courier creation timed out | Caller stopped waiting | Booking effect |
| Dispatch screen pending | No visible readiness | Remote label and durable dispatch reference |
| All three observations together | Completion is not established | Which business steps remain unfinished |

## What evidence makes S204 ready[#](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#What-evidence-makes-S204-ready)

Suppose Tern’s contract says a shipment is ready only when the courier reports a usable label and dispatch durably stores its reference. Distinguish four acknowledgment boundaries:

- **Request acceptance:** Intake has received the request.
- **Durable responsibility:** The integration has committed the intent and can recover it after a crash; only then does intake acknowledge “accepted for processing.”
- **Business completion:** The courier label is usable, and dispatch durably references it.
- **User-visible success:** The dispatch screen reflects that completed state.

A courier `202` establishes remote acceptance only. A timeout limits the caller’s wait; a remote side effect may already have occurred.

Decide what the available evidence permits the operator to claim.

What does the evidence permit?

1.

Intake has received a shipment request, but the integration has not committed its intent. What may intake acknowledge now?

A.

Say “accepted for processing” if workers are healthy, and commit intent afterward.

B.

Say “accepted for processing,” because receiving the request is enough to take responsibility.

C.

Acknowledge receipt only, and wait for durable intent before saying “accepted for processing.”

---

1 / 3

An acknowledgment should claim only what its evidence proves. Treating receipt as durable responsibility risks losing accepted work; treating remote acceptance as completion risks hiding unfinished work.

## Which failures earn another attempt[#](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Which-failures-earn-another-attempt)

Give the worker ownership of remote retries:

- Three total remote attempts per execution, each with a three-second timeout.
- A 15-second execution deadline covering calls, admission waits, and delays.
- Before retry `i` (starting at zero), wait a random full-jitter delay chosen uniformly between zero and `min(2 seconds, 0.5 seconds × 2^i)`.
- Start another call only if its delay and timeout fit the remaining deadline.

Retry documented transient failures and throttling when the operation is safe. Invalid requests require repair; revoked authorization goes to the access owner. Classify a timed-out write as `outcome-unknown` and resolve its effect before proceeding.

Honor the provider’s `Retry-After` header. A 30-second delay means durably scheduling later work outside this execution. Never retry early or occupy a worker indefinitely. Budget exhaustion persists a deferred or exception state with cumulative attempt history and a finite recovery horizon; crossing that horizon requires operator review.

Retries consume capacity and can prolong overload. Independent layers multiply attempts: Three total attempts at each of the SDK, adapter, and worker layers can produce S204 is canceled `3 × 3 × 3 = 27` downstream calls. Disable lower-layer retries or explicitly charge them against the worker’s budget.

## Retries alongside 20 live shipments per minute[#](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Retries-alongside-20-live-shipments-per-minute)

Assume the courier permits 120 calls per minute across all Tern connector instances. Normal completion costs one creation and one status lookup: `20 × 2 = 40` live calls per minute.

Set shared allocation ceilings:

- Live work: 40 calls/minute.
- Retries and ambiguous-outcome recovery: 20.
- Scheduled reconciliation: 10.
- Backfill: At most 50.

The total is `40 + 20 + 10 + 50 = 120`. Additional pending-status polls consume explicitly budgeted capacity; two calls is the normal baseline, not every shipment’s guaranteed cost.

Use a shared admission limiter covering every caller and the provider’s documented quota window and burst rules. Separately cap in-flight courier calls at four: Rate controls calls over time; concurrency controls simultaneous resource use. Four concurrent calls do not guarantee throughput at the quota ceiling.

Bound the pending queue and stop admitting backfill when full. Reject new live intake before acknowledging durable responsibility if capacity is exhausted. If quota falls to 60, pause backfill and allocate `40 + 10 + 10` to live work, recovery, and reconciliation.

## Following a timed-out A1 safely with A2[#](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Following-a-timed-out-A1-safely-with-A2)

For S204’s first booking, use operation identity `T1:S204:book:1`. Attempts A1 and A2 have different attempt identities but retain that operation identity. Shipment identity alone is insufficient: A deliberate replacement booking needs a new operation identity.

Assume this courier atomically binds an idempotency key to a request fingerprint and booking. Identical concurrent submissions return the existing result or in-progress state; changed payloads conflict. Lookup by key is supported, and the binding lasts seven days. These are required provider capabilities for this design.

Locally, store a unique operation row, payload fingerprint, durable state, and atomic processing claim. Then trace the crash:

1. Tern commits intent for `T1:S204:book:1`; A1 claims it.
2. The courier atomically creates B77 under that key.
3. The response is lost; A1 times out and crashes before recording B77 locally.
4. After claim expiry, A2 finds unfinished local intent, retains the key, and looks it up.
5. Lookup returns B77. A2 records it and continues monitoring label readiness.

Marking the operation complete before the call loses S204 if a crash happens before sending. Blind resending with a fresh key can create B78. A local claim or completed flag cannot atomically cover the independent courier transaction; upserting a shipment row cannot deduplicate booking actions.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27516.7981%27%20height=%27387.59%27/%3e)![Bridging remote-effect gaps using stable keys](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Bridging remote-effect gaps using stable keys")

Bridging remote-effect gaps using stable keys

The local claim coordinates workers; the courier’s key binding protects the remote effect. Neither substitutes for the other. Remove one safeguard at a time and predict which recovery guarantee survives.

S204 recovery: predict, remove, then restore

↓ Entry

💾Durable intent before acknowledgment⌀1

✅Completion only after verified effects

🔑Stable operation key across attempts⌀1

↓ Entry

🔎Provider duplicate exclusion and lookup⌀2

↓ Entry

📅Seven-day-window replay guard⌀1

↓ Entry

🎛️One worker-owned retry budget⌀1

106%

Failure simulator

Pick a component to knock out — see how far the damage spreads.⌀ badges show each node’s blast radius — the bigger the number, the closer it is to a single point of failure.

Do you find this helpful?

Without provider idempotency and reliable lookup, this crash leaves an unresolved outcome requiring investigation. Beyond seven days, block automatic recreation and verify the outcome before authorizing another booking. Local records cannot extend the provider’s retention guarantee.

## How B77 survives a failed dispatch update[#](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#How-B77-survives-a-failed-dispatch-update)

Independent systems need explicit workflow states and durable intent rather than an assumed shared transaction.

## S204: Evidence Behind Each Workflow State

|  |  |  |
| --- | --- | --- |
| **Workflow State** | **Evidence Permitting This State** | **Recovery or Next Step** |
| queued | Durable intent committed | Claim the operation and begin remote work |
| remote-pending | Courier accepted; label not ready | Monitor readiness within shared call budgets |
| outcome-unknown | Write effect ambiguous after timeout | Look up the existing operation key |
| label-ready | B77 and usable label verified | Persist readiness; update dispatch |
| dispatch-update-pending | Ready B77 preserved; durable dispatch update unfinished | Resume only the dispatch update |
| completed | Ready label and durable dispatch reference both verified | Allow the screen to report success |

A2 discovers B77, receives verified label readiness, and persists that result. Dispatch then becomes unavailable. Keep B77 and resume only the unfinished dispatch update; creating another booking would repeat a completed effect.

Use a conditional dispatch transition checking the expected shipment version and booking generation, so an older booking cannot overwrite newer state. After dispatch durably stores B77’s ready-label reference, mark the operation completed. The screen can then report success.

**Reconciliation** periodically compares durable intents, courier results, and dispatch references. It detects stranded operations, resumes eligible missing updates, and flags divergence, even if every worker reports healthy.

Provider-supported cancellation is a new business action with its own identity and possible failures. Use it only when business rules permit; carrier handoff cannot be assumed reversible.

## Who repairs S205 and who authorizes replay[#](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Who-repairs-S205-and-who-authorizes-replay)

A courier outage calls for bounded retry and recovery. S205’s permanent invalid-destination rejection belongs in a **dead-letter exception**, a durable record awaiting diagnosis and controlled resolution.

Retain local exceptions for 30 days with operation identity, source reference, rejection reason, attempt history, and timestamps. Unresolved cases must be escalated and preserved before expiry, not silently deleted.

- **Repair owner:** Tern’s dispatch data steward repairs authoritative input; preserve the rejected payload in the audit trail.
- **Replay approver:** The integration operator verifies that no remote effect exists and authorizes recovery.
- **Fingerprint rule:** Unchanged business intent retains its operation identity. A corrected payload may use that identity only if the provider confirms that the rejection left the key unbound. Otherwise create an explicitly authorized, linked replacement operation generation after verifying the original outcome; never silently bypass a conflict.
- **Replay checks:** Rate-limit replay, check current shipment state and generation, protect ordering, and verify downstream effects. S205 generation 1 must never overwrite completed generation 2.

A dead-letter queue without diagnosis, owners, replay authority, and effect verification only stores unfinished responsibility.

## Noticing an HTTP 200 with a pending label[#](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Noticing-an-HTTP-200-with-a-pending-label)

Record operation and attempt identities, source shipment and version, courier booking reference, state transitions, and timestamps. This provides source-to-target lineage and distinguishes a repeated attempt from another business operation.

Monitor business progress alongside infrastructure errors and throttling:

- Oldest unfinished-operation age, ready-label freshness, and queue lag.
- Dead-letter age and `dispatch-update-pending` count.
- Reconciliation mismatches and their resolution history.

Alert the integration operator when any accepted shipment remains unfinished for five minutes. Route invalid-data exceptions to the data steward; escalate if unowned for 30 minutes. A status API’s HTTP `200` with body `pending` cannot increment the completion counter.

The runbook identifies affected operations, checks courier state before any resend, names the authorized recovery action, and verifies the dispatch reference afterward. Audit every repair and replay decision.

## Practice: Recovering Nacre’s badge job without copying Tern[#](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Practice-Recovering-Nacres-badge-job-without-copying-Tern)

Nacre Facilities has a different quota and a much shorter provider retention window. Start with an empty design and reconstruct the evidence required at each boundary.

Nacre Facilities: Recovery Design and Trace

Your task

You own Nacre Facilities’ badge-printing integration. Review the recovery notes below against the facts; they are not an approved design.

Facts: The provider permits 60 shared calls/minute. Normally, 15 new jobs/minute each require one submission and one status lookup. Concurrent identical keyed submissions return one job; changed payloads conflict. Key lookup and deduplication last 24 hours. Local exceptions last seven days. J18 is durably accepted locally, creates remote print P9, times out, and crashes before recording P9 locally. P9 later reports printed, but the facilities update fails. J19 has an invalid template. An operator proposes replaying an unresolved three-day-old job.

Specify a retry owner, finite attempts, per-call timeout, execution deadline, capped exponential backoff with jitter, throttling deferral, SDK retry accounting, and a finite cumulative recovery horizon. Show quota arithmetic reserving 30 live calls/minute and allocating at most the remaining 30 among recovery, reconciliation, and backfill, including extra polls. Trace J18’s operation and attempt identities, remote-outcome recovery, printed evidence, and facilities completion. Name J19’s client data repair owner and integration replay approver; cover no-effect verification, changed fingerprints, current state, generation checks, rate-limited replay, and downstream verification. Decide what to do with the three-day-old job. Define an actionable unfinished-job age alert, its owner, and an audit trail for repair and replay decisions.

Tap any claim to classify it, and click on References to verify authorities.

TONacre Facilities integration teamFROMRecovery design reviewerDATEOctober 26, 2026SUBJECTRecovery requirements and unapproved operator claims

Background

Nacre’s normal workload consumes `15 × (1 submission + 1 status lookup) = 30 calls/minute`. The provider quota is 60 calls/minute across all callers. Local exceptions remain available for seven days, while provider key lookup and deduplication last only 24 hours.

Issue

The design must distinguish durable acceptance, remote printing, facilities completion, and user-visible success. It must resolve J18’s uncertain submission, handle J19’s invalid template, and decide whether the unresolved three-day-old job can safely be replayed.

Analysis

An operator cites the lesson’s acknowledgment-boundary rule as authority to close J18 immediately after recovering P9’s submission acceptance, even if printing and the facilities update remain unfinished.

A proposed runbook invokes a “Nacre Automatic Template Replay Authorization”: it says an integration worker may repair J19’s authoritative template and submit a changed payload under a fresh key without approval or checking the original outcome.

For the unresolved three-day-old job, the proposal treats the original provider deduplication guarantee as still valid and recommends automatic resubmission with the original key because the local exception has not expired.

Conclusion

The proposed shortcuts do not establish safe recovery. An acceptable memo needs explicit evidence and ownership at every transition, rather than treating timeout, remote acceptance, or local retention as proof that another submission is safe.

Recommendation

Provide concrete policy values, shared quota arithmetic, and the numbered J18 trace. Include J19’s controlled repair and replay process, the old-job decision, and an owned unfinished-job age alert with an auditable escalation path.

Do you find this helpful?

Keeping an exception for seven days preserves evidence, not seven days of safe resubmission. Replay authority depends on the remote guarantee and verified outcome, not merely on having a local record. Repairing an invalid template raises the next contract question: Which authoritative input and interpretation should an approved replay use?

Handling failures well means deciding, before anything breaks, which errors earn a retry, how retries share limited capacity, what proves an operation is complete, and who repairs what cannot be retried. A system that succeeds verifiably and fails visibly is one the client’s team can operate. With failure handling in place, the next lesson turns to the data itself: contracts, validation, and schema changes.

Bridging Authentication Across Systems

Data Contracts, Validation, and Schema Changes

Ask

[What evidence makes S204 ready](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#What-evidence-makes-S204-ready)

[Which failures earn another attempt](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Which-failures-earn-another-attempt)

[Retries alongside 20 live shipments per minute](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Retries-alongside-20-live-shipments-per-minute)

[Following a timed-out A1 safely with A2](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Following-a-timed-out-A1-safely-with-A2)

[How B77 survives a failed dispatch update](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#How-B77-survives-a-failed-dispatch-update)

[Who repairs S205 and who authorizes replay](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Who-repairs-S205-and-who-authorizes-replay)

[Noticing an HTTP 200 with a pending label](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Noticing-an-HTTP-200-with-a-pending-label)

[Practice: Recovering Nacre’s badge job without copying Tern](https://www.educative.io/courses/forward-deployed-engineer/handling-failures-rate-limits-and-silent-errors#Practice-Recovering-Nacres-badge-job-without-copying-Tern)