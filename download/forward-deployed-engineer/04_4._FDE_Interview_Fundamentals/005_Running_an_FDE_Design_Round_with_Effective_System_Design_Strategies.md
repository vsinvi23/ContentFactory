# Running_an_FDE_Design_Round_with_Effective_System_Design_Strategies

Source: https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Running an FDE Design Round

Explore how to pace an FDE design round from discovery to a closing recommendation. Learn how to state assumptions, trace one workflow end to end, and check feasibility with simple arithmetic. Understand how to revise a commitment when the interviewer changes a constraint and how to close clearly in about a minute.

We'll cover the following...

- [Moving from discovery to a design before time runs out](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Moving-from-discovery-to-a-design-before-time-runs-out)
- [A first version Alder would actually use](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#A-first-version-Alder-would-actually-use)
- [Narrating the trace of claim C204](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Narrating-the-trace-of-claim-C204)
- [Testing handoff capacity at 12 arrivals per minute](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Testing-handoff-capacity-at-12-arrivals-per-minute)
- [When Repair halves the quota](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#When-Repair-halves-the-quota)
- [Closing in roughly one minute](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Closing-in-roughly-one-minute)
- [Practice: Reproducing the reasoning on three new prompts](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Practice-Reproducing-the-reasoning-on-three-new-prompts)

Twelve minutes have passed, and the candidate is still asking questions. There are several constraints on the table but no design the interviewer can inspect. The recovery is to summarize what matters, declare the assumptions that make progress possible, and trace one useful workflow far enough to test its feasibility. A strong design conversation makes connected decisions visible and revises them when the evidence changes.

## Moving from discovery to a design before time runs out[#](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Moving-from-discovery-to-a-design-before-time-runs-out)

Discovery should establish an agreed scope, implementable components, and the smallest viable solution. Document working assumptions and identify what needs validation rather than waiting for a complete specification.

Use the following 45-minute practice schedule as a guide. Adjust the timing based on the interview format and the interviewer's priorities:

- **0–8 minutes:** Define the desired outcome, constraints, and initial scope.
- **8–13 minutes:** Identify the initial workflow and assign responsibilities.
- **13–27 minutes:** Trace one end-to-end operation and calculate feasibility against the key constraints.
- **27–38 minutes:** Evaluate failure scenarios and address interviewer follow-up questions.
- **38–45 minutes:** Explain key trade-offs and present the final design recommendation.

Organize the round with the CLIENT checklist from the previous lesson. This schedule, the CLIENT checklist, and the self-review rubric below are practice aids for this course, not official employer requirements or scoring rubrics.

Keep three categories in your notes: confirmed facts, declared assumptions, and unresolved questions. At minute twelve, a candidate might say:

“The outcome and approval boundary are clear. I’ll scope one product line, assume the documented Repair interface supports duplicate-safe creation, and flag that for verification. May I trace that workflow, then test capacity?”

That gives the interviewer a concrete assumption to challenge while preserving time for design.

## A first version Alder would actually use[#](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#A-first-version-Alder-would-actually-use)

Suppose Alder Appliances’ coordinators spend a median of 25 minutes from warranty-claim approval to a repair ticket becoming visible. The pilot target is 10 minutes for one product line, with an agreed maximum normal-operation data age of 15 minutes. The median workflow target and the maximum data-age requirement measure different things.

Claims owns approval and customer details; Repair owns ticket state. The **thin slice**, an independently useful workflow, creates and links one repair ticket per approved claim and exposes unresolved handoffs to coordinators. Exclude claim approval, scheduling, and replacement of either application. A successful connector demonstration alone supplies no evidence of user value, adoption, or production ownership; delivery must establish those outcomes.

The supplied access facts are:

- Claims provides a read-only API using a service API key.
- Repair permits writes through a restricted service account.
- An approved internal host can reach both APIs.
- An approved connector is available; verify its authenticated API access and pagination before claiming reuse.

Reusable components reduce custom implementation. Connector availability still leaves field mappings, business rules, ownership conflicts, and exception handling to resolve.

For Alder, custom responsibilities include approval eligibility, claim-to-ticket mapping, operation tracking, testing, and exceptions. Propose these assignments for agreement:

- Integration team: Runtime operation, alerts, and connector maintenance.
- Warranty operations: Exception resolution and approval of eligibility rules.
- Repair application owner: API permissions and ticket contract.
- Warranty operations and Repair application owner jointly: Approval of future business mappings; the integration team implements and tests them.

Keep customer data on the approved path, limit coordinator access to authorized claims, protect service credentials, and avoid customer details in diagnostic logs. Confirm retention and access requirements before deployment.

## Narrating the trace of claim C204[#](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Narrating-the-trace-of-claim-C204)

Define the identities before describing retries:

- **Entity identity:** Which business object the records describe: `claim_id C204`.
- **Operation identity:** Which business operation is being performed: `repair-handoff:C204:v1`.
- **Attempt identity:** Which execution is running: `A1`, or `A2` on a retry. Retries retain the operation identity.

Trace the data, state changes, and promises aloud:

1. “Claims reports C204 as approved. I validate eligibility and map its permitted customer and claim fields into Repair’s ticket contract.”
2. “I persist a pending handoff with `repair-handoff:C204:v1`. Only after that durable write do I treat the integration as responsible for tracking the handoff through completion or an explicit exception.”
3. “Worker attempt A1 sends a create request with the stable operation key. Repair returns accepted job `J88`. This acknowledges request acceptance; it does not yet identify a created ticket.”
4. “For this design, I assume Repair’s documented contract makes accepted jobs durable, supports operation-key deduplication, and exposes terminal status by job ID. These are interface assumptions to verify.”
5. “A status lookup for J88 returns ticket `T901`. I persist that link and mark the handoff completed. The coordinator now sees ‘Repair ticket created: T901.’ Before confirmation, the display remains pending.”

Request acceptance, durable responsibility, business completion, and user-visible success are separate boundaries. Under the assumed contract, Repair’s acceptance transfers durable job responsibility, while business completion requires ticket confirmation. If another execution is needed, A2 uses the same operation identity; it does not represent a second intended handoff.

The two durable boundaries assign different responsibilities: the integration tracks the handoff, while Repair executes the accepted job. Neither alone justifies displaying a completed ticket. Match each observation below to the promise it establishes.

What does each observation promise?

Observation from C204’s trace

J88’s status confirms T901; the integration persists its link and marks the handoff completed.

Repair returns accepted job J88 to attempt A1.

The integration persists C204’s pending handoff.

Claims reports C204 as approved.

Promise established

Business completion is recorded; showing “Repair ticket created: T901” is justified.

Source authorization evidence for the handoff.

Integration takes durable responsibility for tracking completion or an explicit exception.

Request accepted; Repair owns a durable job under the assumed documented contract.

Match each observation to the promise it establishes under Alder’s declared contract. Submit to check correctness and explanations, then correct any mismatches.

Do you find this helpful?

The important interview signal is attaching a specific promise to each response. An HTTP success code without its interface contract cannot establish that the coordinator’s work is finished.

## Testing handoff capacity at 12 arrivals per minute[#](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Testing-handoff-capacity-at-12-arrivals-per-minute)

Declare the inputs: 1,200 approved claims daily, a sustained planning peak of 12 per minute, average record payload 2 KB, source pages of 100 records, and a source quota of 30 requests per minute.

For a 240-record backlog:

- Page count = ceiling(records / page size) = ceiling(240 / 100) = 3 pages.
- Approximate record payload = records × average size = 240 × 2 KB = 480 KB, excluding protocol overhead.

Those source reads fit the stated minute-level quota if the budget is otherwise available. Destination calls are the tighter constraint:

- Repair quota: 60 calls/minute, with 20 reserved for other users.
- Available budget: 60 − 20 = 40 calls/minute.
- Assume one creation call and one status lookup per completed handoff.
- API-limited capacity = available calls / calls per operation = 40 / 2 = 20 handoffs/minute.
- Net backlog reduction = capacity − continuing arrivals = 20 − 12 = 8/minute.
- Recovery time = backlog / net reduction = 240 / 8 = 30 minutes.

Twenty handoffs per minute is optimistic: Extra lookups, retries, or other bottlenecks lower it. The daily average cannot substitute for the sustained-peak calculation.

Freshness includes source publication delay, discovery delay, waiting, and processing. If source publication delay is negligible, polling every five minutes plus assumed waiting and processing below two minutes suggests approximately seven minutes of normal data age. It is an estimate, not a guarantee. A 30-minute backlog recovery already rules out an unconditional 15-minute freshness promise; recovery needs a separate commitment.

## When Repair halves the quota[#](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#When-Repair-halves-the-quota)

The interviewer changes Repair’s total quota to 30 calls per minute, with 10 reserved for other users. Decide what happens to capacity and the original commitment before continuing.

Revise the quota commitment

1.

Repair’s total quota falls from 60 to 30 calls per minute, and its reservation for other users falls from 20 to 10. Each handoff still needs two calls; approved claims arrive at a sustained 12 per minute, with 240 already waiting. Which response is defensible?

A.

Increase queue capacity to absorb the backlog and keep the 15-minute freshness promise, with one handoff per approved claim and stable operation keys.

B.

Retract the freshness commitment and seek more quota, verified lower-call semantics, or an agreed narrower scope with manual handling for excluded claims, while preserving approval authority, one handoff per approved claim, and stable operation identity.

C.

Give retries new operation identities so Repair can process them independently, improving throughput enough to keep the freshness promise.

D.

Add workers to restore the original completion rate and keep the 15-minute freshness promise, with approval checks and stable operation keys.

---

1 / 1

The revised calculation is:

- Available calls = 30 − 10 = 20/minute.
- Capacity = 20 / 2 = 10 handoffs/minute.
- Backlog change = 12 arrivals − 10 completions = 2 additional handoffs/minute.

Recovery time exists only when processing capacity exceeds the arrival rate. Here, the backlog grows under the sustained-peak assumption. More workers cannot expand the API budget; a queue stores waiting work without increasing completion capacity.

Say what changes:

“I retract the original freshness commitment for this workload. Can we change peak duration, secure more quota, verify a supported lower-call workflow, or narrow the pilot? I recommend delaying that commitment until one option is validated.”

If narrowing the pilot, obtain business agreement and retain manual handling for excluded claims. Preserve approval authority, one repair handoff per approved claim, and stable operation identity across retries. Follow-ups should revise affected decisions and commitments; the recommendation should explain rejected alternatives, remaining risks, and conditions that would change the choice.

Consider this failed answer:

“The connector already handles the integration. I will add a queue and more workers, mark the claim successful when Repair accepts it, and keep the 15-minute promise after the quota reduction.”

Its four observable failures are:

- Transport reuse hides unresolved mapping and ownership decisions.
- Accepted work is displayed as a completed ticket.
- Worker count is treated as API capacity.
- The freshness promise contradicts 10 completions against 12 arrivals per minute.

Fix it by naming custom responsibilities and owners, displaying pending until ticket confirmation, calculating the bottleneck, and renegotiating a concrete constraint.

## Closing in roughly one minute[#](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Closing-in-roughly-one-minute)

Close with decisions and evidence rather than a tour of components:

“For one product line, I recommend a connector-assisted approved-claim handoff, targeting a median reduction from 25 to 10 minutes without moving approval authority. It creates and links repair tickets and exposes exceptions; approval, scheduling, and application replacement stay outside scope. The supplied credentials and internal route support the connections; connector behavior, duplicate-safe creation, and durable asynchronous acceptance still need verification. Each claim keeps a stable handoff operation key, and pending becomes completed only after ticket confirmation. The reduced quota supports 10 handoffs per minute against 12 arrivals, so I cannot promise the original freshness target. Subject to agreement, the integration team owns runtime and alerts, warranty operations owns exceptions, and warranty operations and the Repair application owner jointly approve mapping extensions. I reject an all-product rollout until quota and ownership are established. Next, validate the two-call estimate and acceptance contract, then agree on quota or narrower scope. Outage recovery needs its own freshness commitment.”

The close must agree with the trace and arithmetic. Confidently defending an unchanged diagram would conceal the most consequential finding.

## Practice: Reproducing the reasoning on three new prompts[#](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Practice-Reproducing-the-reasoning-on-three-new-prompts)

Use eight review dimensions:

1. Discovery and scope.
2. Quantitative feasibility.
3. Business semantics.
4. Entity and operation identity.
5. Authentication and reachable interfaces.
6. Failures and acknowledgment boundaries.
7. Security and access boundaries.
8. Recommendation, trade-offs, and ownership.

For each, score 0 for absent, 1 for asserted but unsupported, or 2 for explicit evidence tied to the prompt. Quote a sentence or calculation from the answer to support each score, and write one improvement for every weak dimension. There is no passing total or employer prediction.

Complete three compact mini-rounds:

- **Invoice handoff:** Reduce median approved-invoice-to-ledger-entry time from 30 to 10 minutes without bypassing approval. Peak arrivals: 8/minute. Posting and confirmation: 2 calls/invoice. Quota: 30/minute, with 10 reserved. Backlog: 100. Follow-up: Total quota falls to 20, still reserving 10.
- **Return handoff:** Reduce median approved-return-to-intake-ticket time from 40 to 15 minutes while supervisors retain approval. Peak arrivals: 4/minute. Creation and confirmation: 2 calls/operation. Available budget: 12/minute. Backlog: 40. Follow-up: Intake write permission is withdrawn.
- **Access handoff:** Reduce median approved-request-to-provisioning-ticket time from 20 to 5 minutes while security retains approval. Peak arrivals: 3/minute. Creation and confirmation: 2 calls/operation. Available budget: 10/minute. Backlog: 20. Follow-up: Security prohibits request data from leaving the client network.

For each, the source owns approval and its stable identifier (`invoice_id`, `return_id`, or `request_id`) and offers a read-only service-key API. The destination owns posting or ticket state, permits restricted service-account writes, and supports stable operation keys and confirmation lookup. Both APIs are initially reachable from an approved internal host. Missing contractual details remain declared assumptions.

Produce six concise outputs per prompt: a scoped opening with assumptions; a one-operation trace with acknowledgment meanings; capacity and recovery arithmetic; response to the changed constraint; closing recommendation with owners; and the evidence-based eight-dimension review.

Try drafting all three mini-rounds in separate notes before reading the reference-review notes below. Those notes mix sound reasoning with unsupported commitments; they are not model answers. Audit them against the prompt facts, then revise the drafts.

Three Handoffs: Audit the Review Notes

Your task

You are the integration designer preparing three independent design conversations: invoice posting, return intake, and access provisioning. Each needs an inspectable workflow, defensible arithmetic, and a revised recommendation when constraints change. The reference-review notes below mix sound reasoning with unsupported commitments; they are not model answers.

Tap any claim to classify it, and click on References to verify authorities.

TOPractice designerFROMDesign review partnerDATEOctober 26, 2026SUBJECTIndependent handoff designs and changed-constraint review

Background

Before reading the reference-review notes, draft all three mini-rounds in your own initially empty notes. For each, write six concise outputs: **1)** scoped opening and declared assumptions; **2)** one-operation trace and acknowledgment meanings; **3)** capacity and recovery arithmetic; **4)** changed-constraint response; **5)** closing recommendation and owners; **6)** eight-dimension evidence review. Keep confirmed facts, assumptions, and unresolved questions separate.

Issue

**Invoice:** Target median approved-invoice-to-ledger-entry time from 30 to 10 minutes, preserving approval. Source owns approval and `invoice_id`, with a read-only service-key API. Ledger owns posting state, permits restricted service-account writes, and supports operation-key deduplication and confirmation lookup. An approved internal host reaches both. Peak: 8/minute; posting plus confirmation: 2 calls/invoice; total quota: 30/minute, 10 reserved; backlog: 100. Follow-up: total quota becomes 20, still reserving 10.

**Return:** Target median approved-return-to-intake-ticket time from 40 to 15 minutes; supervisors retain approval. Returns owns approval and `return_id`, with a read-only service-key API. Intake owns ticket state, permits restricted service-account writes, and supports stable operation keys and ticket lookup. An approved internal host reaches both. Peak: 4/minute; 2 calls/operation; 12 available calls/minute; backlog: 40. Follow-up: Intake write permission is withdrawn.

**Access:** Target median approved-request-to-provisioning-ticket time from 20 to 5 minutes; security retains approval. Requests owns approval and `request_id`, with a read-only service-key API. Provisioning owns ticket state, permits restricted service-account creation, and supports stable operation keys and lookup. An approved internal host initially reaches both. Peak: 3/minute; 2 calls/operation; 10 available calls/minute; backlog: 20. Follow-up: security prohibits request data from leaving the client network.

Analysis

**Invoice reference-review memo:** Baseline capacity is `(30−10)/2 = 10 invoices/minute`; backlog recovery under continuing peak arrivals is `100/(10−8) = 50 minutes`. After the quota reduction, capacity is `(20−10)/2 = 5/minute`, so backlog grows by `8−5 = 3/minute`. A queue and additional workers will nevertheless preserve the 10-minute median target at sustained peak.

**Return reference-review memo:** Capacity is `12/2 = 6 operations/minute`; recovery is `40/(6−4) = 20 minutes` under continuing peak arrivals. After Intake withdraws write permission, continue automated ticket creation using the originally permitted restricted service account while supervisors retain approval.

**Access reference-review memo:** Capacity is `10/2 = 5 operations/minute`; recovery is `20/(5−3) = 10 minutes` under continuing peak arrivals. An encryption exception to the network restriction authorizes an external connector whenever its traffic is encrypted, so external deployment can proceed without further approval.

**Cross-prompt review note:** Persist a pending handoff before treating the integration as responsible for tracking it. Distinguish the source entity identifier, stable operation key, and individual attempt identifier; retries retain the operation key. Treat an acceptance response only as the promise documented by its contract. Declare assumptions about asynchronous acceptance and durability, verify them, and display pending until documented posting or ticket confirmation. Propose an integration runtime owner, a business exception owner, and destination permission/contract ownership for agreement.

Conclusion

Revise your own six outputs for **each** prompt after auditing the reference notes. For output six, review all eight dimensions: Discovery and scope; quantitative feasibility; business semantics; entity and operation identity; authentication and reachable interfaces; failures and acknowledgment boundaries; security and access boundaries; recommendation, trade-offs, and ownership. For every dimension, quote a sentence or calculation from your answer, assign **0 = absent, 1 = asserted but unsupported, or 2 = explicit evidence tied to the prompt**, and give one repair if below 2. If evidence is absent, state “No evidence” rather than inventing a quotation. Do not calculate a passing total or predict an interview outcome.

Recommendation

Choose one revised prompt for a complete **45-minute spoken round**: 0–8 outcome, constraints, scope; 8–13 workflow and ownership; 13–27 trace and arithmetic; 27–38 failures and follow-ups; 38–45 trade-offs and close. Ask a listener to identify your scope, assumptions, owners, operation identity, acknowledgment meanings, numerical bottleneck, revised commitment, and next validation from your words. Make anything they had to infer explicit on the next attempt.

Do you find this helpful?

To practice the full round, choose one prompt and work through the illustrative 45-minute round aloud. A listener should be able to identify the scope, assumptions, owners, operation identity, acknowledgment meanings, numerical bottleneck, revised commitment, and next validation from the spoken answer alone. Anything they must infer from the diagram should be stated explicitly on the next attempt.

Running a design round well is mostly about pacing decisions, not adding components. Stating assumptions early, tracing one workflow end to end, and revising commitments when the interviewer changes a constraint keep the design inspectable from the first minute to the last. With the method and the pacing in place, the next lesson turns to the first integration decision in any design: how data moves between systems.

The CLIENT Approach for FDE System Design

Choosing How Data Moves Between Systems

Ask

[Moving from discovery to a design before time runs out](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Moving-from-discovery-to-a-design-before-time-runs-out)

[A first version Alder would actually use](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#A-first-version-Alder-would-actually-use)

[Narrating the trace of claim C204](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Narrating-the-trace-of-claim-C204)

[Testing handoff capacity at 12 arrivals per minute](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Testing-handoff-capacity-at-12-arrivals-per-minute)

[When Repair halves the quota](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#When-Repair-halves-the-quota)

[Closing in roughly one minute](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Closing-in-roughly-one-minute)

[Practice: Reproducing the reasoning on three new prompts](https://www.educative.io/courses/forward-deployed-engineer/running-an-fde-design-round#Practice-Reproducing-the-reasoning-on-three-new-prompts)