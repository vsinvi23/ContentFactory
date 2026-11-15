# Selecting_Data_Movement_Methods_for_AI_Systems_Integration

Source: https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Choosing How Data Moves Between Systems

Explore how to choose between files, APIs, change feeds, webhooks, and change data capture when moving data between systems. Learn how snapshots, watermarks, and checkpoints keep data moving without gaps or duplicates. Understand what each interface can promise about freshness and how to recover when a step fails partway.

We'll cover the following...

- [Choosing the interface for Morrow’s inventory data](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Choosing-the-interface-for-Morrows-inventory-data)
- [What an accepted import I17 actually confirms](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#What-an-accepted-import-I17-actually-confirms)
- [Joining snapshot S800 to the change feed without a gap](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Joining-snapshot-S800-to-the-change-feed-without-a-gap)
- [Where checkpoint 803 should be saved](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Where-checkpoint-803-should-be-saved)
- [Why webhook H9 cannot replace the poller](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Why-webhook-H9-cannot-replace-the-poller)
- [Should forecasting share the inventory queue?](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Should-forecasting-share-the-inventory-queue)
- [Morrow’s file-only vs. CDC access](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Morrows-file-only-vs-CDC-access)
- [Practice: Defending Pine Print’s movement and recovery contract](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Practice-Defending-Pine-Prints-movement-and-recovery-contract)

Morrow Supply offers three inventory interfaces: a nightly CSV, a read API with snapshot pagination and an incremental change endpoint, and best-effort webhook hints. Inventory changes must become visible within five minutes during normal operation, and approved database replication access is unavailable. Choosing the movement path means deciding both how quickly changes arrive and who can recover them after a crash.

## Choosing the interface for Morrow’s inventory data[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Choosing-the-interface-for-Morrows-inventory-data)

Choose API backfill plus incremental polling; optionally use webhooks to discover changes sooner. Nightly-only transfer misses the freshness target, and direct database change data capture (CDC) requires access Morrow has not approved.

Compare patterns against actual source capabilities, freshness, temporal coupling, permissions, recovery requirements, and operating cost:

- **Files:** Scheduled bulk transfer, including snapshots and increments; delivery completion needs an explicit protocol.
- **Synchronous APIs:** Immediate queries or bounded commands. The caller depends on the remote response arriving within its deadline.
- **Polling:** Repeated reads through a supported incremental interface; recovery depends on the continuation contract.
- **Webhooks:** Provider-initiated notifications that reduce discovery delay; completeness depends on delivery and recovery provisions.
- **Asynchronous messaging:** Queues distribute work; retained streams support independent consumption and replay. Messaging decouples sender and receiver availability while adding durable publication, consumption, and recovery responsibilities.
- **CDC:** Database changes captured through approved source or replication access, with snapshot and log-recovery contracts.
- **Virtualized or federated reads:** Queries retrieve external data without maintaining a full local copy. Source availability, query latency, permissions, network access, and quotas remain on the read path.

These patterns combine: An API poller can capture changes locally and then publish work for consumers. Before adding a broker, ask who will operate it, what retention costs, and whether the existing durable store suffices.

For Morrow, a one-minute sweep plus assumed source publication below one minute and waiting and processing below two minutes gives normal data age below 1 + 1 + 2 = 4 minutes, subject to validated capacity. Outage recovery requires a separate budget.

## What an accepted import I17 actually confirms[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#What-an-accepted-import-I17-actually-confirms)

A synchronous stock lookup returns a usable value within its response contract. An initial import returns an operation to track over time.

For Morrow, define this contract:

1. Persist operation identity `import:warehouse:v1` and its status before returning accepted operation `I17`.
2. Expose a status lookup by I17: `pending`, `running`, `completed`, or `failed`, with terminal outcome details.
3. Correlate request, progress, and outcome through I17. Fetch executions have separate attempt identities; retries retain the operation identity.
4. Set request and fetch timeouts. A timeout leaves the outcome unknown; it does not prove cancellation. A retry using the same operation identity finds the existing import.

Under this contract, acceptance establishes durable tracking responsibility. Business completion requires the snapshot and subsequent changes to be applied through an agreed catch-up boundary. The display remains pending or running until then; receipt of the request cannot justify user-visible success.

## Joining snapshot S800 to the change feed without a gap[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Joining-snapshot-S800-to-the-change-feed-without-a-gap)

A snapshot represents source state at a defined boundary. A **cursor** is a continuation token whose guarantees come from the provider. Pagination alone creates neither a consistent snapshot nor a recoverable change history.

Morrow’s documented API provides:

- **Snapshot token** `S800`**:** 250 inventory records as of source change position 800.
- **Three snapshot pages:** 100, 100, and 50 records.
- An ordered API change feed retaining 24 hours of changes, including deletes.

Load the snapshot this way:

1. Persist the backfill phase and S800. Store page 1 in staging, then durably save its next-page cursor; repeat for pages 2 and 3.
2. Publish the complete staged snapshot at an explicit boundary. Hold newer changes until publication so later snapshot pages cannot overwrite newer inventory state.
3. Consume changes strictly after 800. Capture the current source head (for example, 845) and keep the import running until changes through 845 have been applied.
4. Mark I17 completed through 845 and continue ongoing synchronization.

This handoff works because the source ties S800 to position 800. An ordinary REST endpoint need not expose such a feed. Finish capture within retained history or invoke a supported resynchronization path.

A **timestamp watermark** records progress through a time-based query window. With timestamps alone, `updated_at > last_timestamp` skips records sharing the boundary timestamp. Use documented bounded windows, stable pagination where supported, tie handling, inclusive overlap, and record-version deduplication. Delayed visibility, concurrent updates, unstable pages, and deletes still need source guarantees; unbounded visibility delay requires reconciliation or a qualified completeness claim.

## Where checkpoint 803 should be saved[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Where-checkpoint-803-should-be-saved)

A capture checkpoint records how far the integration has durably taken responsibility for source changes. Consider the tempting implementation: Save position 803, acknowledge webhook H9, then store changes 801–803. A crash before storage leaves the next poll starting after 803 and the provider considering H9 delivered, so the view silently loses updates.

Predict the outcomes when durable inbox capture and checkpoint advancement instead share one local transaction.

Crash at the commit boundary

1.

After snapshot S800, Morrow’s durable capture checkpoint is 800. The poller fetches changes 801 to 803 and, in one local database transaction, inserts all three inbox entries (with payloads, pending state, and unique keys on source and change position) and updates the checkpoint to 803. No worker has applied the changes yet. Which recovery outcomes are correct for a crash immediately before commit and immediately after commit?

A.

Before: Checkpoint 803 survives without the inbox entries, so polling skips them. After: Checkpoint 803 and all three pending entries survive.

B.

Before: Checkpoint 800 remains, and all three changes are fetched again. After: Checkpoint 803 proves all three changes are applied to the read model.

C.

Before: Checkpoint 800 remains, but refetching requires new operation identities. After: Checkpoint 803 survives, but pending work must be recreated under new identities.

D.

Before: Checkpoint 800 remains, and all three changes are fetched again. After: Checkpoint 803 and all three pending inbox entries survive.

---

1 / 1

Start with durable checkpoint 800 and a fetched page containing 801, 802, and 803. An **inbox** is durable storage of received work awaiting application. The source need not join this transaction: replayable source reads let the integration make inbox storage and capture progress atomic locally.

1. Begin a transaction in the integration database.
2. Insert inbox entries keyed by `(source, change_position)` for 801, 802, and 803, including payloads and pending application state. Unique keys identify replayed changes.
3. Update the capture checkpoint from 800 to 803.
4. Commit the transaction.

The crash outcomes are inspectable:

- **Before commit:** Neither entries nor checkpoint changes survive. Checkpoint remains 800, so the next poll fetches all three again.
- **After commit:** Checkpoint is 803 and all three entries are durable. Workers can recover pending application from the inbox.

A recovery position is meaningful only relative to the durable responsibility boundary it represents. Checkpoint 803 establishes capture; the read model could still be applied only through 800.

If records and checkpoint cannot share a transaction, persist records first and checkpoint afterward. A crash between those writes causes replay, handled by duplicate-safe application. Advancing the checkpoint first creates a loss window.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271043.5900000000001%27%20height=%27316.79%27/%3e)![Transactionally checkpointing data snapshots and changes](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Transactionally checkpointing data snapshots and changes")

Transactionally checkpointing data snapshots and changes

The same principle connects S800’s page cursors to change capture and lost acknowledgments: Recovery may repeat already durable work. Repetition must preserve the intended operation rather than create a new business action.

## Why webhook H9 cannot replace the poller[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Why-webhook-H9-cannot-replace-the-poller)

For Morrow, H9 says item P42 in warehouse W1 changed; it contains a hint rather than the complete inventory record.

At ingress:

1. Verify the provider-supported signature using the documented request bytes; apply supported timestamp or event-ID replay controls.
2. Durably insert H9 into ingress storage, recognizing repeated event IDs.
3. Return the provider’s expected acknowledgment only after durable capture.
4. Fetch the supported source representation and process asynchronously. A duplicate H9 must not create another intended business operation; distinct hints for the same source version must also converge safely.

If ingress storage is unavailable, do not acknowledge with a promise of durable acceptance. Keep the periodic authoritative change sweep to recover missed hints, and use provider-supported lookup or replay where available.

Explore which failures remain recoverable under that contract.

H9: Fast Discovery, Durable Acceptance, Safe Recovery

↓ Entry

🔐Provider-supported verification⌀2

📥Durable ingress before acknowledgment⌀2

⚙️Asynchronous lookup and application⌀2

↓ Entry

🔄Periodic authoritative change sweep⌀2

🔑Duplicate-safe operation handling⌀1

📦Intended inventory effects

106%

Failure simulator

Pick a component to knock out — see how far the damage spreads.⌀ badges show each node’s blast radius — the bigger the number, the closer it is to a single point of failure.

Do you find this helpful?

Monitor authoritative capture lag, not just successful webhook acknowledgments. Morrow’s sweep must capture missed changes before the feed’s 24-hour retention expires; durable ingress cannot recover expired source history.

## Should forecasting share the inventory queue?[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Should-forecasting-share-the-inventory-queue)

A **work queue** assigns each task to one of several competing workers. Use it when one inventory-update task needs one worker.

If both the inventory read model and forecasting need every change, give each an independent durable subscription and checkpoint. Putting them in one competing-consumer group would divide changes between them. Durable subscriptions and retained stream positions recover only within documented persistence and retention limits.

Specify ordering scope as `(warehouse_id, item_id)`, such as W1/P42. Partition or route by that key, name the broker’s ordering contract, and prevent concurrent workers from applying later versions first. Different keys can progress concurrently.

A worker can commit a database update and crash before acknowledging consumption. Redelivery then repeats the same operation under a new attempt identity. Duplicate-safe database application, or a destination-supported operation key for external actions, must cover that boundary; broker delivery guarantees alone cannot promise duplicate-free business effects.

## Morrow’s file-only vs. CDC access[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Morrows-file-only-vs-CDC-access)

For files, an hourly snapshot still cannot meet five minutes. Change the interface or renegotiate freshness. Define the file contract explicitly:

- **Completion:** Require a producer-published manifest for `inventory-20261026T1000.csv` after upload. Include snapshot time, file identity, expected row count, and checksum. File appearance alone does not establish upload completion; an atomic rename is another option where supported.
- **Publication:** Distinguish full snapshots from increments, stage and verify the input, recognize repeat file identities, and publish at an explicit boundary.
- **Restart:** If a failed run already issued external writes, partial effects may remain. Restart from recorded row or operation boundaries.
- **Atomicity:** Batch atomicity belongs to a specific transaction. For example, Palantir Foundry documents a single transaction for a batch sync’s output dataset; that guarantee says nothing about arbitrary downstream API calls.og handoff: snapshot S at log position L

For CDC, require approved access and a source-defined snapshot-to-l, retaining changes from the correct boundary during backfill. Capture inserts, updates, and delete tombstones; save positions after durable capture. If an outage outlasts retention, detect the gap and resnapshot or use supported repair rather than silently resume at the newest offset.

## Practice: Defending Pine Print’s movement and recovery contract[#](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Practice-Defending-Pine-Prints-movement-and-recovery-contract)

Pine Print’s dispatch staff need job-status changes within ten minutes during normal operation. Its complete interface contract is:

- At most one minute from a change to its source timestamp, then at most two additional minutes of visibility delay.
- Five-minute polling, with a maximum expected extraction and application time of one minute at validated load.
- An `updated_since` API supporting bounded windows and stable snapshot pagination within each poll.
- Stable `job_id` and `record_version`; an inclusive five-minute overlap covers the documented visibility delay.
- No events or database access.
- A nightly full snapshot whose absent job IDs identify deletes.

Try drafting a movement contract before reviewing the proposed memo below for errors. Include the normal freshness calculation, watermark and deduplication rules, checkpoint meaning, deletion policy, and recovery after records commit but checkpoint persistence fails. Then assess a new demand: deletes must also appear within ten minutes.

Pine Print: Movement and Recovery Contract

Your task

You are responsible for Pine Print’s integration contract. Dispatch staff need job-status changes within ten minutes during normal operation. The source takes at most one minute to assign a change its timestamp, followed by at most two additional minutes of visibility delay. Polls run every five minutes; extraction and application take at most one minute at validated load. The updated\_since API supports bounded windows and stable snapshot pagination within each poll. Stable job\_id and record\_version values are available, and an inclusive five-minute overlap covers the documented visibility delay. There are no events or database access. A nightly full snapshot identifies deletes through absent job IDs. Your contract must justify the movement pattern and rejected alternatives, freshness arithmetic, window and page handling, deduplication, capture and application progress, and deletion reconciliation. Address two follow-ups: records are durable but checkpoint persistence fails; deletes must now also become visible within ten minutes.

Tap any claim to classify it, and click on References to verify authorities.

TOPine Print dispatch staffFROMIntegration teamDATEOctober 26, 2026SUBJECTJob-status movement, recovery, and deletion visibility

Background

Pine Print needs job-status changes visible within ten minutes during normal operation. Its supported movement interface is an updated\_since API with bounded windows and stable snapshot pagination. Stable job\_id and record\_version values support duplicate recognition. Events and database access are unavailable.

Issue

The contract must establish a normal-operation freshness budget, a recoverable capture boundary, separate application progress, and a deletion policy. It must also handle durable records with a missing checkpoint update and assess a new ten-minute deletion requirement.

Analysis

Use five-minute API polling for job-status changes. The normal freshness budget is **1 + 2 + 5 + 1 = 9 minutes**, supported by the nightly full-snapshot contract. Nightly-only status transfer misses the target; webhooks and direct database CDC are not supported alternatives.

For each poll, query inclusively from the previous completed upper watermark minus five minutes to a fixed current upper bound. Keep that window fixed across all snapshot pages and deduplicate by (job\_id, record\_version). Once the first page is durable, advancing the completed watermark to the window’s upper bound is safe because stable pagination protects the remaining pages.

The capture watermark records durable responsibility, not application completion. Track application progress separately. If records commit but checkpoint persistence fails, recover from the last durable completed watermark, repeat the inclusive overlapping window, and recognize repeated (job\_id, record\_version) pairs. Duplicate-safe application must prevent replay from repeating effects or allowing older state to overwrite newer state.

Pine Print’s updated\_since API contract includes delete tombstones. Polling those tombstones therefore extends the nine-minute status budget to deletions, so the new ten-minute deletion requirement can be accepted without an interface change.

Conclusion

Approve a movement contract only when its freshness, capture, application, recovery, and deletion claims each have supporting interface guarantees. A normal-operation freshness budget is not an outage-recovery deadline.

Recommendation

Prepare the final contract in your own words. Include verified complete nightly-snapshot reconciliation before treating absent job IDs as deleted; an incomplete snapshot must not trigger absence-based deletion. For each satisfied review criterion, attach a quoted sentence from your revised contract as evidence.

Do you find this helpful?

The conservative status budget is 1 + 2 + 5 + 1 = 9 minutes. Inclusive overlap from the prior completed upper watermark, deduplicated by job ID and record version, makes replay safe within the supplied guarantees. Advance that watermark only after every bounded-window page is durably captured, and track application completion separately.

If records commit but the watermark does not, resume from the older durable watermark and accept replay. Recognize the same job/version pairs without creating new intended operations. This repeats capture work rather than risking a skipped page.

Nightly absence-based reconciliation cannot establish ten-minute delete visibility. Seek tombstones, a delete feed, another supported interface, or an explicitly relaxed requirement. Once the movement contract is feasible, the next connection decision is which identities and credentials can exercise those interfaces without expanding authorization.

Running an FDE Design Round

Bridging Authentication Across Systems

Ask

[Choosing the interface for Morrow’s inventory data](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Choosing-the-interface-for-Morrows-inventory-data)

[What an accepted import I17 actually confirms](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#What-an-accepted-import-I17-actually-confirms)

[Joining snapshot S800 to the change feed without a gap](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Joining-snapshot-S800-to-the-change-feed-without-a-gap)

[Where checkpoint 803 should be saved](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Where-checkpoint-803-should-be-saved)

[Why webhook H9 cannot replace the poller](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Why-webhook-H9-cannot-replace-the-poller)

[Should forecasting share the inventory queue?](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Should-forecasting-share-the-inventory-queue)

[Morrow’s file-only vs. CDC access](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Morrows-file-only-vs-CDC-access)

[Practice: Defending Pine Print’s movement and recovery contract](https://www.educative.io/courses/forward-deployed-engineer/choosing-how-data-moves-between-systems#Practice-Defending-Pine-Prints-movement-and-recovery-contract)