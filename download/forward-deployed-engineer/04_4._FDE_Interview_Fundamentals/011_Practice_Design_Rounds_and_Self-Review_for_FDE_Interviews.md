# Practice_Design_Rounds_and_Self-Review_for_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Practice Rounds and Self-Review Rubric

Apply the complete FDE design method across three new client scenarios, developing an initial design and revising it in response to follow-up requirements. Compare your design decisions with the reference reasoning, identify unsupported claims, and document corrections without modifying your original submission. Use a self-review rubric to identify recurring weaknesses in your design decisions and prioritise areas for further practice.

We'll cover the following...

- [Defending three designs before opening the references](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Defending-three-designs-before-opening-the-references)
- [Round 1: How Northstar could connect approval to scheduling](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-1-How-Northstar-could-connect-approval-to-scheduling)
- [Round 2: How Meadow could make an hourly file useful](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-2-How-Meadow-could-make-an-hourly-file-useful)
- [Round 3: How Ridgeway could preserve each engineer’s authority](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-3-How-Ridgeway-could-preserve-each-engineers-authority)
- [Decisions that survive comparison](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Decisions-that-survive-comparison)
  - [Northstar: Recoverable scheduling handoff](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Northstar-Recoverable-scheduling-handoff)
  - [Meadow: Timestamped planning evidence](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Meadow-Timestamped-planning-evidence)
  - [Ridgeway: Authorized, applicable evidence](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Ridgeway-Authorized-applicable-evidence)
- [Evidence that shows what to practice next](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Evidence-that-shows-what-to-practice-next)

This lesson starts with three blank design notes and the reference architectures kept closed. The task is to build a three-round portfolio: an initial design and a separately preserved follow-up revision for each client. The useful result is evidence of changing a commitment when capacity, freshness, or authority changes.

## Defending three designs before opening the references[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Defending-three-designs-before-opening-the-references)

Allow 12 minutes for each initial design and three minutes for its follow-up. These are suggested practice timings, not standard interview limits. Save each initial design before addressing the new constraint. Complete and preserve all six responses before reviewing any worked solutions.

Structure your design decisions using CLIENT: Context, Landscape, Integration points, End-to-end design, Non-happy paths, and Trade-offs. Distinguish confirmed facts, working assumptions, and unresolved questions.

For each initial design, document six areas:

1. **Outcome and scope:** Define the initial workflow, measurable target, exclusions, and completion criteria.
2. **Interface inventory:** Identify supported or proposed connections, authentication methods, network paths, authoritative data fields, system identities, and responsible owners.
3. **Operation trace:** Trace one operation through request acceptance, durable processing, business completion, and user-visible confirmation, identifying the evidence required at each stage.
4. **Numerical feasibility:** Show the calculation, input assumptions, limiting constraint, and what the estimate does not establish.
5. **Controls and recovery:** Address failure scenarios, uncertain operation outcomes, authorisation checks, deployment safeguards, and ownership of unresolved exceptions.
6. **Recommendation:** Propose the smallest viable implementation, identify its operational owner, explain the rejected alternative, and specify the next validation step.

For each follow-up, update the affected design commitment, operation trace, and trade-off analysis. Keep the original designs, follow-up revisions, and subsequent corrections as separate records.

## Round 1: How Northstar could connect approval to scheduling[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-1-How-Northstar-could-connect-approval-to-scheduling)

Northstar Components’ planners manually copy approved releases into Scheduling, taking a median of 20 minutes. The pilot aims for five minutes during normal operation without scheduling unapproved work.

- **Authority:** Approval owns `release_id`, revision, approval state, and quantity. Scheduling owns `job_id` and execution state. An approved item crosswalk connects their different item identifiers.
- **Source contract:** Approval provides a read-only, API-key REST feed with stable continuation positions, deletes, seven-day retention, and approved read capacity above the workload.
- **Destination contract:** Scheduling supports workload OAuth access, conditional job creation using an expected release revision, and atomic create deduplication plus lookup under a caller-supplied operation identity for seven days. Its normal create-and-status sequence costs two calls per release.
- **Budget:** Total destination quota is 60 calls per minute, with 12 reserved elsewhere. Arrivals are 18 releases per minute; an outage leaves 120 queued releases.
- **Environment and ownership:** An approved client-VPC host reaches both APIs and token endpoints. Operations resolves approval or item exceptions; integration engineering operates the connector; Scheduling’s owner approves its write contract.

Choose the thin slice and define what proves completion. Separate the normal five-minute target from the outage-recovery commitment.

Commit the initial response before taking this follow-up: The total destination quota falls to 40 calls per minute, with the 12-call reservation unchanged. Recalculate capacity and revise the original commitment explicitly.

## Round 2: How Meadow could make an hourly file useful[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-2-How-Meadow-could-make-an-hourly-file-useful)

Meadow Distribution’s warehouse coordinators spend a median 15 minutes assembling stock evidence for transfer planning. The goal is seven minutes, with displayed stock changes no more than 75 minutes old during normal operation.

- **Stock contract:** Stock owns quantities by `warehouse_id` and SKU. Its only interface is hourly full CSV snapshots over internal SFTP. Each producer-issued manifest supplies file identity, snapshot boundary, row count, checksum, and schema version.
- **Timing:** The next snapshot boundary occurs at most 60 minutes after a stock change. Publication finishes within five minutes of the boundary; verification and application take at most five minutes.
- **Meaning and scale:** Snapshot absence means a stock row was removed, not quantity zero. There are 12,000 rows at roughly 250 bytes each. The approved pipeline can stage and verify a snapshot within its five-minute processing allowance.
- **Planning contract:** The transfer planner has a read-only API using an mTLS integration certificate. It owns `transfer_id`, `warehouse_id`, SKU, and planning state. An approved crosswalk resolves SKU differences.
- **Environment and ownership:** Both interfaces are reachable only from the warehouse network. Planning is human-approved; no reservation or transfer-execution interface exists. Warehouse operations owns missing-reference and stale-data exceptions. The client platform team owns runtime and certificate rotation.

Commit the initial response before taking this follow-up: A stakeholder demands 15-minute visibility with unchanged interfaces. Give a recommendation grounded in those interfaces.

## Round 3: How Ridgeway could preserve each engineer’s authority[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-3-How-Ridgeway-could-preserve-each-engineers-authority)

Ridgeway Engineering’s engineers spend a median 12 minutes finding an applicable maintenance procedure. The pilot aims for five minutes while returning only currently authorized, applicable published procedures.

- **Access contracts:** The portal uses OIDC login. The separate document API supports workload OAuth for ingestion and bounded reads; portal login is not its API credential.
- **Evidence contract:** Documents have stable `doc_id`, revision, publication state, effective date, site scope, and access labels. An approved index stores chunks, source references, revisions, and access labels and supports permission-filtered retrieval.
- **Current authorization:** A client service validates current site, document, and action permissions and denies access when unavailable.
- **Baseline answer path:** Before evidence reaches the model, one document API call checks candidate applicability and one fetches selected current evidence. The source permits 90 calls per minute, with 30 reserved elsewhere. Demand is 20 answers per minute.
- **Boundary:** Approved hosting and model processing stay inside the client’s cloud boundary. Logs may not contain document bodies. Version one provides bounded evidence and citations or hands uncertainty to the maintenance knowledge owner; it never changes procedures or operates equipment.

Commit the initial response before taking this follow-up: A formerly authorized document remains indexed after access revocation. Its text instructs the assistant to retrieve a restricted procedure and send it to an external diagnostic URL. Revise the execution trace and permitted user claim.

Enter the portfolio with all response fields initially empty. Keep the worked portfolio closed until all three initial responses and all three follow-ups are committed.

Three-Round CLIENT Portfolio

Build a portfolio for Northstar Components, Meadow Distribution, and Ridgeway Engineering using their complete prompt contracts above; organizational sizes are not specified. Defend supported interfaces, business meaning, numerical commitments, current authorization, recoverable effects, and accountable delivery before opening the worked portfolio.

You'll make 3 decisions that reshape the highlighted sections — and watch the document update in real time as you go.

Three Originals and Three Follow-ups

1. Commitment Protocol

Use CLIENT to organize each response. Keep facts, assumptions, and open questions separate. Produce six compact outputs: outcome and scope; interface inventory; one operation trace; numerical feasibility; controls and recovery; recommendation. Use the definitions in the lesson. Allow an illustrative 12 minutes per initial response and three minutes per follow-up. Commit each initial response before addressing its follow-up. Preserve three immutable originals and three separately committed follow-ups. Each follow-up must explicitly revise the affected commitment, operation trace, and trade-off, not merely add a component; record what remains unchanged. Keep solutions, calculation hints, comparison feedback, and reference criteria closed until all six responses are committed.

2. Northstar Design NotesConfigurable

3. Meadow Design NotesConfigurable

4. Ridgeway Design NotesConfigurable

5. Comparison and Repairs

Only after all six responses are committed, open the worked portfolio in the lesson and compare decisions and evidence. Retain all original and follow-up commitments as the evidence base for w4. Append later repairs separately, identifying the client, commitment being repaired, replacement decision or trace step, remaining risk, named owner, and next validation. Never overwrite a committed response.

Do you find this helpful?

A defensible answer changes its promise when the evidence no longer supports it. Adding a component is useful only when it changes the limiting condition.

## Decisions that survive comparison[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Decisions-that-survive-comparison)

Stop here if any attempt or follow-up is uncommitted. Once all six are saved, open the complete reference portfolio below. These are defensible recommendations under the supplied contracts, not unique architectures or official interview answers; alternatives need equivalent feasibility, safety, recovery, and business value, with changed assumptions stated.

Open after committing all six responses: Worked portfolio

### Northstar: Recoverable scheduling handoff[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Northstar-Recoverable-scheduling-handoff)

Deploy a connector on the approved VPC host to poll Approval and create one Scheduling job for each eligible release generation, maintaining a durable link between the records. Start with an approved set of items and route unresolved mappings or approval exceptions to Operations.

- Persist release R-81 revision 4 and its source position before advancing the polling checkpoint. Reject unsupported records and prevent stale revisions or deletion events from incorrectly restoring release eligibility.
- Verify the release's approval status and its mapping to approved Scheduling items. Durably record the scheduling intent under operation ID `R-81:schedule:1`, including the source revision and approved request payload. Assign a unique attempt ID to each execution while retaining the same operation ID across retries.
- Use the approved OAuth workload identity to submit a conditional Scheduling job creation request for release revision 4. Verify that the Scheduling API enforces the agreed conditions for rejecting stale revisions and releases whose approval has been revoked. A successful Scheduling API acceptance confirms receipt of the request, not that the job is ready. Keep the handoff pending until readiness is verified.
- If the create request times out, mark the operation as `outcome-unknown` because Scheduling may have created the job. Within the supported seven-day lookup window, use the original operation key to check whether Scheduling created J-620. Retain the same operation ID across all attempts. The stable operation ID prevents duplicate job creation only because Scheduling enforces atomic deduplication for that key. After the seven-day lookup window expires, suspend automatic retries and require investigation before attempting another create.
- Agree on the job status that constitutes handoff completion with the Scheduling owner. Before marking the handoff complete, verify that status and the durable link between R-81 and J-620. Update the planner's success status only after the backend confirms the required completion evidence.

Durable source capture and scheduling intent establish recoverable processing responsibility. Scheduling API acceptance and job readiness require separate confirmation.

**Capacity check**

- The baseline destination budget is `60 − 12 = 48` calls per minute.
- At two calls per release, capacity is `48 / 2 = 24` releases per minute.
- Net recovery is `24 − 18 = 6`, so 120 queued releases drain in `120 / 6 = 20` idealized minutes.
- Budget extra destination polls, retries, and reconciliation separately; source polling also needs its own budget.
- Capacity alone does not prove five-minute latency, so validate polling, waiting, and readiness delays.

**Follow-up: Quota reduction**

- After the reduction, `40 − 12 = 28` calls allow `28 / 2 = 14` releases per minute.
- Against 18 arrivals, the backlog grows by four per minute.
- Retract the unchanged five-minute commitment and negotiate quota, supported batching, or a narrower admitted scope with accountable handling of excluded work.
- Reject extra workers as a repair for this fixed API budget.

**Owners**

- **Integration engineering:** Owns runtime and recovery.
- **Operations:** Owns business exceptions.
- **Scheduling’s owner:** Validates conditional-write semantics.

### Meadow: Timestamped planning evidence[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Meadow-Timestamped-planning-evidence)

Recommend an internal read view that joins verified stock snapshots to read-only planning evidence through the approved crosswalk. It supports human transfer planning without claiming reservation or execution.

1. Receive file F-31 and its manifest. Stage all `12,000 × 250 = 3,000,000` bytes, roughly 3 MB; verify checksum, row count, schema, and mappings.
2. Durable staging establishes recoverable processing responsibility. Publish a complete version of the read view only after validating that the approved pipeline supports an atomic switch; verify that repeated processing of F-31 cannot duplicate publication. If validation fails, retain the prior snapshot with visible source time and stale-state handling.
3. Trace warehouse W2/SKU S-17 through its approved planner SKU mapping. A missing reference blocks the joined evidence and goes to warehouse operations. A removed stock row becomes unavailable evidence, never a fabricated zero.
4. Published read-view state establishes application completion; the coordinator display must show the corresponding evidence and snapshot timestamp. File receipt alone establishes neither. Human planning approval remains separate.

**Timing check**

- The normal change-to-display bound is `60 + 5 + 5 = 70` minutes.
- That supports the 75-minute target under the supplied timing assumptions.
- Measure the seven-minute evidence-assembly goal separately.

**Follow-up: 15-minute freshness request**

- Decline a 15-minute guarantee with unchanged interfaces.
- Retain the timestamped planning aid while seeking a different source contract or renegotiating freshness.
- Even eliminating all downstream delay leaves up to 60 minutes before the source captures a change.
- Reject local streaming of rows as a freshness repair.

**Owners and launch checks**

- **Platform team:** Owns runtime and certificate rotation.
- **Warehouse operations:** Owns stale and missing-reference exceptions.
- **Before launch:** Validate manifest behavior and the full publication timing.

### Ridgeway: Authorized, applicable evidence[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Ridgeway-Authorized-applicable-evidence)

Recommend a bounded procedure-finding assistant using separate portal identity and workload document access. Propose a named client platform operator for runtime, credentials, and quota management; obtain agreement rather than assuming that owner exists.

1. Authenticate the portal caller and establish trusted site context S3. Retrieve candidate references through permission-filtered retrieval, enforcing current site, document, and action authorization before indexed text is exposed to the model. If current authorization is unavailable, deny protected access.
2. For candidate D-204 revision 6, use the baseline source check to verify current publication, revision, effective date, and site applicability. Fetch only the selected permitted current evidence with the second source call. If the selected evidence changes, reassess its authorization before exposure.
3. Produce a bounded cited answer, or hand uncertainty to the maintenance knowledge owner. Receiving a question is request acceptance; a useful answer requires checked evidence and actual delivery. A handoff remains pending until its agreed durable ownership evidence exists.

**Capacity check**

- Available capacity is `(90 − 30) / 2 = 30` answers per minute.
- Twenty arrivals consume `20 × 2 = 40` of the available 60 calls per minute.
- The remaining 20 calls support explicitly bounded exceptional source work, including additional checks and retries.
- Validate answer latency and the five-minute user workflow separately.

**Follow-up: Changed execution trace**

After revocation, current authorization excludes D-204 before model exposure, even if the index returns its chunk.

- Stop at authorization and release no revoked text.
- Deny restricted-document retrieval and reject external egress.
- Treat document text as evidence, never as authority to expand tools or destinations.
- Keep bodies out of logs and use only approved internal processing.

**Permitted claim and validation**

The permitted response is: "I can't provide a verified procedure for this request. The maintenance knowledge owner needs to review it." Do not reveal whether restricted procedures or documents exist.

Do not retrieve restricted content into the model context and rely on output filtering. Access controls must prevent unauthorised retrieval before the model receives the content. Test access revocation and prompt injection scenarios before enabling this retrieval path.

Evaluate your design decisions against the evidence-based rubric below. Compare each initial design with its follow-up revision to verify that the changed constraint led to an appropriate update to the original commitment.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27851%27%20height=%27511%27/%3e)![Evaluating capacity, latency, and access controls](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Evaluating capacity, latency, and access controls")

Evaluating capacity, latency, and access controls

Each limiting condition belongs to a different authority: Scheduling controls the call budget, Stock controls when changes become observable, and Ridgeway’s authorization service controls current access. A local optimization cannot substitute for a change to those contracts.

Next, inspect three polished but flawed recommendations. Locate the exact unsupported claim and replace it with a feasible decision before appending the repairs to the portfolio.

Portfolio Review — Three Commitments to Audit

Your task

All three initial designs and follow-up revisions are committed. You are reviewing a portfolio summary before its recommendations reach the client owners. Each client note contains a claim that must be replaced with a feasible commitment supported by numerical or causal evidence.

Tap any claim to classify it, and click on References to verify authorities.

TOClient operating ownersFROMPortfolio design teamDATEOctober 26, 2026SUBJECTFollow-up commitments for Northstar, Meadow, and Ridgeway

Background

The portfolio covers an approval-to-scheduling connector for Northstar, a stock-evidence planning view for Meadow, and a procedure-finding assistant for Ridgeway. Each recommendation must remain defensible after its changed constraint.

Issue

Northstar's destination quota has fallen. Meadow wants 15-minute visibility without changing its interfaces. Ridgeway must handle an indexed document whose access has been revoked and whose text requests restricted retrieval and external transmission.

Analysis

**Northstar memo.** The connector will preserve durable intent, conditional creation, and operation-identity lookup. Integration engineering will add workers after the quota reduction. **The original capacity of 24 releases per minute still applies, so added workers preserve five-minute completion for all 18 arrivals per minute.** Operations will retain ownership of approval and mapping exceptions.

**Meadow memo.** The warehouse-network pipeline will stage the hourly CSV, verify its manifest, and publish a complete read view. The display will retain the snapshot timestamp and distinguish absent rows from zero quantities. **Streaming rows from the hourly CSV makes the display live and guarantees stock-change visibility within 15 minutes without changing the source interface.** Planning remains human-approved.

**Ridgeway memo.** Portal login and workload document credentials remain separate, processing stays within the client boundary, and logs exclude document bodies. **Retrieved text may reach the model before current permission filtering because model instructions prevent leakage and can treat a document's request for restricted retrieval or external transmission as delegated authority.** The assistant will otherwise provide bounded answers with citations or hand uncertainty to the maintenance knowledge owner.

Conclusion

A useful implementation is not sufficient evidence for every business commitment. Capacity, source timing, and current authorization must support the promised outcome.

Recommendation

Preserve the original portfolio and its follow-up commitments. Record evidence-backed replacements separately, then append a second revision after comparison rather than overwriting the first repair. Carry forward each client's remaining risk, accountable owner, and next validation.

Do you find this helpful?

An impressive architecture can still leave a growing queue, an impossible freshness promise, or unauthorized evidence exposure. Repairs must change those outcomes, not merely the wording of the recommendation.

## Evidence that shows what to practice next[#](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Evidence-that-shows-what-to-practice-next)

Reuse the author-created, non-official eight-dimension review. Score each dimension 0 for absent, 1 for asserted but unsupported, or **2** for explicit evidence tied to the prompt. A component name earns no credit by itself.

- **Discovery:** User, baseline, target, scope, and unresolved assumptions.
- **Feasibility:** Supported interfaces, routes, numerical budgets, and timing.
- **Business semantics:** Authoritative fields, lifecycle meaning, and completion evidence.
- **Identity:** Entity, operation, and attempt distinctions; crosswalks and duplicate-prevention evidence.
- **Authentication and authorization:** Credential purpose and current caller/action permissions.
- **Failures and recovery:** Ambiguous effects, replay safety, retention limits, and accountable exceptions.
- **Security and deployment:** Approved locations, sensitive copies, logs, credentials, and network controls.
- **Trade-offs and delivery ownership:** Rejected option, thin slice, operating owner, and next validation.

Apply the rubric separately to each original attempt and its follow-up commitment. For the follow-up, inspect the original plus the explicitly recorded amendment; never silently import a reference decision. Quote the learner’s words for every dimension or mark evidence absent. Record original and follow-up totals out of 16 for each client, preserving those scores after comparison.

For every 0 or 1, append a specific replacement decision or trace step. There is no official pass mark, and a high aggregate cannot excuse unauthorized disclosure, an unverified duplicate write, or an impossible freshness promise.

Audit Your Design Portfolio

Review your saved Northstar Components, Meadow Distribution, and Ridgeway Engineering commitments against the lesson’s eight dimensions. Use w1 as evidence, the worked portfolio only for comparison, and optional w3 repairs as later additions; never treat a reference decision as something you committed.

You'll make 3 decisions that reshape the highlighted sections — and watch the document update in real time as you go.

Original, Follow-up, and Repair Record

1. Saved Commitment Evidence

2. Original Commitment ReviewsConfigurable

3. Follow-up Commitment ReviewsConfigurable

4. Post-comparison RepairsConfigurable

5. Corrected Spoken Defense

Do you find this helpful?

Keep revised reasoning separate from the original assessment. A correction demonstrates improved understanding but does not change what the initial submission established. Recurring weaknesses across different client scenarios provide better guidance for further practice than how closely a design matches a single reference architecture.

Identify your weakest recurring assessment area and practise explaining one corrected design decision aloud. For the scenario with the weakest score, explain the initial workflow, evidence of successful completion, limiting capacity constraint, revised commitment, recovery owner, and next validation step. For each client scenario, record the revised recommendation, outstanding risks, responsible owner, and next validation step. Preserve the original submission unchanged.

Practice rounds should reveal how design decisions change when client constraints or requirements change. Preserve the initial design, evaluate it against the available evidence, and practise the weakest area. This helps develop the ability to make and revise design commitments as client constraints change.

By the end of this exercise, you should be able to defend your design decisions with evidence, recognise where your initial reasoning fell short, and explain how you would adapt your approach under changing client constraints. Use these lessons to strengthen your judgment, communicate trade-offs clearly, and make defensible commitments in future FDE design discussions.

Designing for Client Security and Deployment Environments

Decomposing the Problem: The RAG System

Ask

[Defending three designs before opening the references](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Defending-three-designs-before-opening-the-references)

[Round 1: How Northstar could connect approval to scheduling](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-1-How-Northstar-could-connect-approval-to-scheduling)

[Round 2: How Meadow could make an hourly file useful](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-2-How-Meadow-could-make-an-hourly-file-useful)

[Round 3: How Ridgeway could preserve each engineer’s authority](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Round-3-How-Ridgeway-could-preserve-each-engineers-authority)

[Decisions that survive comparison](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Decisions-that-survive-comparison)

[Northstar: Recoverable scheduling handoff](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Northstar-Recoverable-scheduling-handoff)

[Meadow: Timestamped planning evidence](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Meadow-Timestamped-planning-evidence)

[Ridgeway: Authorized, applicable evidence](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Ridgeway-Authorized-applicable-evidence)

[Evidence that shows what to practice next](https://www.educative.io/courses/forward-deployed-engineer/practice-rounds-and-self-review-rubric#Evidence-that-shows-what-to-practice-next)