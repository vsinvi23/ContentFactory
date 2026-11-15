# Understanding_Data_Contracts_and_Schema_Changes_in_AI_Systems

Source: https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Data Contracts, Validation, and Schema Changes

Explore how data contracts catch bad or changed data before it reaches a client's systems. Learn how to validate records at the boundary, quarantine rejected revisions, and handle schema versions that change meaning without changing shape. Understand how versioned interpretations keep replay predictable and what evidence makes a mapping change safe.

We'll cover the following...

- [Does duration: 120 mean 2 hours or 120 hours?](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Does-duration-120-mean-2-hours-or-120-hours)
- [The worker, entry, and fields being mapped](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#The-worker-entry-and-fields-being-mapped)
- [What makes an E41 update acceptable](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#What-makes-an-E41-update-acceptable)
- [Where rejected revision 7 goes](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Where-rejected-revision-7-goes)
- [What changes when Time v2 arrives](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#What-changes-when-Time-v2-arrives)
- [Which interpretation replay should use](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Which-interpretation-replay-should-use)
- [Evidence that makes a mapping change safe](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Evidence-that-makes-a-mapping-change-safe)
- [Practice: Deriving Fen Water’s contract from its own facts](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Practice-Deriving-Fen-Waters-contract-from-its-own-facts)

Two records both say `duration: 120`; do they represent the same amount of work? For Bracken Services, answering requires the source version, units, and business meaning before any payroll write. A **data contract** makes those interpretations explicit so validation, mapping, and approved replay produce defensible results.

## Does `duration: 120` mean 2 hours or 120 hours?[#](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Does-duration-120-mean-2-hours-or-120-hours)

Bracken’s Time source v1 and payroll staging use these field meanings:

Ace Editor

1

2

3

{"system":"Time","schema\_version":"v1","duration":120,"status":"APPROVED"}

{"system":"Payroll staging","duration":120,"status":"PAID"}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The Time record describes 120 minutes eligible for export. The payroll record describes 120 hours with payment completed. Copying matching names would multiply worked time by 60 and falsely assert payment.

A safe mapping preserves business meaning through an explicit, versioned interpretation. Bracken’s integration stages approved time; it does not execute payments.

## The worker, entry, and fields being mapped[#](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#The-worker-entry-and-fields-being-mapped)

A **mapping contract** specifies source and destination meanings, field-level authority, units, enumerations, reference mappings, and conflict policy. Bracken’s contract includes:

- **Worker crosswalk:** `(B1, Time, W17)` maps to `(B1, Payroll, P804)`.
- **Entry identity:** `(B1, Time, E41)` identifies the time entry.
- **Project crosswalk:** Source project `P9` maps to payroll project `J22`.
- **Time authority:** Worked duration, project, approval, and entry revision.
- **Payroll authority:** Payment status and payment references, which are read-only to this integration.

Scope identifiers by tenant and source system. Email and display names are descriptive and mutable; they cannot establish identity. An unresolved crosswalk or ownership conflict becomes an exception rather than a guessed match or overwrite.

As established earlier in this chapter, keep entity, operation, and attempt identities distinct; retries retain the operation identity.

Bracken chooses canonical contract `c1` with tenant, entry identity, worker identity, source revision, `duration_hours`, project reference, cost center, and eligibility. A **canonical representation** is an explicitly chosen integration model: It reduces translation complexity while retaining distinctions the workflow needs. Preserve raw source data and provenance alongside it.

Time `APPROVED` maps to eligibility `READY`. Payroll’s `PAID` remains under Payroll’s control.

## What makes an E41 update acceptable[#](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#What-makes-an-E41-update-acceptable)

Bracken sends partial updates. **Structural validation** checks shape, required fields, and types. Require `tenant`, `entry_id`, `employee_id`, `revision`, `schema_version`, and event kind; an approved upsert also needs numeric duration and a project reference.

**Semantic validation** checks business meaning: supported approval status, declared units, positive duration, approved worker and project crosswalks, allowed transitions, and revision ordering. A structurally valid number can still be unsafe to apply.

Document these update rules separately:

- Missing `cost_center` leaves its existing value unchanged.
- Explicit `cost_center: null` clears it because this destination permits clearing.
- `VOID` invalidates eligibility and requests Payroll’s supported void transition; it never physically deletes payroll history.

For approved upserts, validate the effective record after combining the partial update with known state. If required business values cannot be established, quarantine the update. A full snapshot would need a different omission policy.

A malformed identifier fails its format rule. A well-formed but unknown worker or project fails reference resolution. Neither justifies matching a display name, guessing a project, coercing negative duration, or dropping an unsupported status.

Classify the contract failures and update meanings before following E41.

Apply Bracken’s update contract

Bracken case

Well-formed but unknown project PX

Approved upsert with numeric duration -120

Partial update with cost\_center absent

Partial update with cost\_center: null

Missing revision

VOID event

Contract result

Supported eligibility invalidation without deleting history

Clear cost center under the destination contract

Preserve existing cost center

Semantic range rejection

Structural rejection for missing required metadata

Semantic reference exception requiring authoritative resolution

Match each case to its contract result, then submit. Use the feedback to revise incorrect pairs.

Do you find this helpful?

Use the rejection category to route remediation: Send unresolved references to the data steward, not to an adapter rule that invents a match. Keep the record blocked while that decision is pending.

## Where rejected revision 7 goes[#](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Where-rejected-revision-7-goes)

E41 revision 7 declares source schema v1, employee W17, status `APPROVED`, duration `120`, and project `PX`. Structural validation succeeds; semantic validation fails because PX has no approved project crosswalk.

Quarantine it before destination submission with rejection code `UNKNOWN_PROJECT`. Preserve the raw payload, operation identity, source revision, source schema, mapping version, reference-data version, and timestamps.

Assign responsibility explicitly:

1. Bracken’s time-data steward diagnoses PX and repairs the authoritative Time record to project P9, producing revision 8. Revision 8 still declares v1.
2. The approved project crosswalk supplies P9 to J22.
3. The integration operator verifies that no destination effect exists and approves controlled replay under the established operation-key and fingerprint rules.
4. The operator verifies the resulting destination hours, references, eligibility, and unchanged payment fields.

Keep rejected revision 7 intact. Link revision 8, the repair decision, and approval to it. Editing the quarantined payload would destroy the evidence explaining why it failed.

## What changes when Time v2 arrives[#](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#What-changes-when-Time-v2-arrives)

While E41 remains pending, Time introduces v2, which expresses duration in hours and supports fractional values. Select the mapping based on the source version declared in the payload:

- **v1:** Apply `time-v1-to-c1@1` to convert 120 minutes into 2 hours (`120 / 60 = 2`).
- **v2:** Apply `time-v2-to-c1@1` to retain the source value of 2 hours without unit conversion.

Both mappings produce canonical contract `c1`. Preserve the v1 mapping for historical data. Hold or quarantine payloads with unsupported source versions.

Evaluate compatibility across the actual data producers, consumers, validators, and storage systems. Adding an optional `note` field may work with an adapter that tolerates unknown fields but fail validation or ingestion when downstream schemas reject additional fields. Define an explicit mapping for the new `APPROVED_PENDING_REVIEW` status. Do not treat it as `APPROVED` without confirming that both statuses have equivalent business meaning.

Detect schema and semantic drift by validating declared versions, monitoring field structures and types, flagging unknown enum values and references, and running semantic checks against contract test fixtures. Structural validation cannot detect a unit change when the field's numeric type remains unchanged.

## Which interpretation replay should use[#](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Which-interpretation-replay-should-use)

First declare the replay purpose. Then select authoritative input and its interpretation:

1. **Historical reconstruction:** Select preserved revision 7, v1 mapper `time-v1-to-c1@1`, and the recorded reference context. Duration becomes two hours, but PX remains unresolved. The expected result is the original exception, with no external write.
2. **Business repair:** Select approved authoritative revision 8, still v1, with the approved reference version containing P9 to J22. The same v1 mapper produces two hours and a resolved project.
3. **Current-state guard:** Before applying revision 8, inspect current E41 state and enforce a conditional revision check at application. If revision 9 has already voided E41, block revision 8 even though its mapping is correct.

The expected revision-8 canonical output is:

Ace Editor

1

2

{"tenant":"B1","entry\_id":"E41","worker\_id":"P804","source\_revision":8,"duration\_hours":2,"project\_ref":"J22","eligibility":"READY"}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

This update leaves cost center unchanged when absent and never writes payroll payment status.

Record an interpretation-provenance tuple containing:

- Source and entity identifiers, source revision, and event and ingestion times.
- Source schema or API version, mapping version, reference-data version, and canonical version.
- Resulting destination reference or exception.

For repair, retain both original and selected replay tuples, plus purpose, approval, current-state evidence, and verified destination result.

Replay still follows the established controls:

- Use a new attempt identity. Reuse the operation identity only under verified no-effect and provider fingerprint rules.
- A corrected payload with a bound conflicting key requires the established authorized replacement process.
- Enforce ordering, rate limits, and downstream-effect verification. Local history cannot extend provider deduplication or lookup guarantees.

The tempting shortcut creates three distinct failures:

- Sending preserved v1 `120` through the latest v2 mapper produces 120 hours instead of two. Version dispatch prevents wrong historical interpretation.
- Substituting a default project assigns those hours to the wrong project. Authoritative repair and provenance prevent unauthorized semantic coercion.
- Replaying after revision 9 restores eligibility after a void. A current-revision guard prevents stale application.

Another retry addresses none of these errors.

## Evidence that makes a mapping change safe[#](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Evidence-that-makes-a-mapping-change-safe)

Define contract test fixtures and their expected results before evaluating changes:

- **Duration conversion:** v1 value `120` minutes and v2 value `2` hours must both map to `2` hours in the canonical contract.
- **Cost centre updates:** An omitted field preserves the existing value; an explicit `null` clears it.
- **Unknown project:** Quarantine the record and report an unresolved project-reference error.
- **`VOID`** **status:** Apply the supported invalidation transition without deleting the record.
- **Unsupported schema version:** Block processing until a compatible mapping is available.
- **Out-of-order revisions:** Reject revision 8 when revision 9 is already current, preventing stale data from overwriting newer state.
- **Time approval:** Map Time status `APPROVED` to `READY` eligibility without writing or changing the `PAID` state.

Run these fixtures against each proposed change and compare actual results with the expected outcomes.

Assess three change proposals

1.

A proposed optional note field passes an adapter that tolerates unknown fields, followed by strict append storage. What evidence would justify calling the change compatible?

A.

The adapter’s successful acceptance establishes compatibility for the pipeline.

B.

End-to-end tests, including strict append storage, must establish compatibility.

C.

No further evidence is needed, because an optional field is compatible with every consumer.

---

1 / 3

Treat mapping corrections that affect previously processed records as data migrations. Run the updated mapper against a representative sample of historical records in dry-run mode, without writing to external systems. Compare canonical outputs and exception counts, investigate unexpected changes, and obtain approval for intended differences. Identify affected records and migrate persisted representations where necessary. Verify destination hours, worker and project associations, eligibility states, and that the migration has not introduced duplicate effects.

Connector storage semantics also affect migration and recovery. Palantir's Data Connection documentation discusses schema mismatches during incremental `APPEND` transactions and connector-specific recovery procedures, including pausing syncs, using versioned datasets, and reverting transactions with support assistance where applicable. These procedures depend on the connector and do not guarantee in-place schema evolution.

Before approving the migration, verify the client's API version, custom schemas, deprecation notices, compatibility requirements, and connector recovery capabilities against current provider documentation. Validate the proposed changes in a representative environment. Confirm applicable deprecation deadlines and migration procedures for the client's deployed product version and configuration.

## Practice: Deriving Fen Water’s contract from its own facts[#](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Practice-Deriving-Fen-Waters-contract-from-its-own-facts)

Challenge the supplied working memo, then independently write a compact mapping contract, record classifications, replay trace, and exactly four concrete input–expected-outcome tests. Fen Water has different units, null semantics, and retraction behavior; derive its rules from the supplied facts rather than copying Bracken’s contract.

Fen Water: Mapping Contract and Replay Review

Your task

You are Fen Water’s integration reviewer, responsible for reviewing a working memo on a compact mapping contract, record classifications, a replay trace, and four concrete input–expected-outcome tests. Tenant F1 has one approved meter crosswalk: (F1, source, M12) → (F1, Billing, A90). Mutable address cannot establish identity. Source owns readings and reading revisions; Billing owns invoice and payment status. Payloads are partial updates: missing optional quality\_note preserves the note; explicit null is forbidden. Source v1 reading\_value means cumulative liters; v2 means cumulative cubic meters; canonical units are cumulative cubic meters. VALID means eligible for billing review, not INVOICED. RETRACT invalidates a reading through a supported transition and never deletes invoices.

R6 revision 3 declares v1, reading\_value 2500, meter M99, and status VALID. M99 lacks a crosswalk, so revision 3 was quarantined before any destination submission. The meter-data steward corrects the authoritative source to revision 4 with meter M12; revision 4 remains v1. The integration operator approves replay. The provider confirms no effect and no bound operation key for R6. Separately, consider a follow-up in which revision 5 has already retracted R6.

Your contract must distinguish scoped entity, operation, and attempt identities; field ownership; structural and semantic checks; missing, null, and retraction rules; and supplied facts versus policies needing confirmation. Your trace must name diagnosis, repair, replay, and verification owners; preserve rejected revision 3; select versioned interpretation for revision 4; record provenance, approval, payload fingerprint, current-state protection, ordering, quota controls, and destination verification; and decide the revision-5 case. Include exactly four concrete tests, including v2 reading\_value 2.5 and meaningful contract boundaries. Identify which actual provider versions, customizations, compatibility, deprecation, storage, key/fingerprint, and connector migration/recovery guarantees still need verification. The working memo below is evidence to challenge, not a contract to copy.

Tap any claim to classify it, and click on References to verify authorities.

TOFen Water integration operatorFROMIntegration review teamDATEOctober 26, 2026SUBJECTR6 mapping contract and controlled repair

Background

R6 revision 3 was quarantined before destination submission because meter M99 had no approved crosswalk. The meter-data steward corrected the authoritative source to revision 4 with M12, retaining source schema v1. The integration operator approved replay; the provider confirmed no effect and no bound operation key.

Issue

The contract must determine which reading, interpretation, and destination reference are authorized, without taking ownership of invoices or payments. It must also distinguish the initial revision-4 repair from the separate case where revision 5 has already retracted R6.

Analysis

The Fen Water field and update facts authorize clearing quality\_note when a partial update explicitly supplies null. Omission instead preserves the existing note.

Once v2 is available, it supersedes the v1 interpretation for all replay. Revision 4 should therefore pass reading\_value 2500 unchanged into cumulative cubic meters through the latest mapper.

A mandatory Fen Water replay standard requires a new business operation identity whenever the source revision changes, even when the provider confirms no effect and no bound key. The new attempt identity alone is insufficient.

Use scoped reading identity (F1, source, R6) and the approved scoped M12-to-A90 crosswalk, never address matching. Classify an unresolved crosswalk as a semantic reference failure, malformed structure as a structural failure, omitted quality\_note as preservation, forbidden null as rejection, and RETRACT as a supported invalidation transition. VALID maps only to billing-review eligibility. Invoice and payment status remain Billing-owned.

Conclusion

Business repair selects authoritative revision 4 with an explicitly versioned v1 mapper, a recorded canonical version, and the approved reference version containing M12 → A90. Before application, inspect current state and enforce a conditional revision guard. If revision 5 has already retracted R6, block stale revision 4; do not restore eligibility or physically delete invoices.

Recommendation

Assign diagnosis and authoritative repair to the meter-data steward, and controlled replay and destination verification to the integration operator. Preserve the original rejection and link repair and approval. Record source/entity/revision identifiers, event and ingestion times, source schema/API version, mapper/reference/canonical versions, operation and attempt identities, payload fingerprint, destination reference or exception, current-state evidence, and verified result. Enforce ordering and quotas. Establish fixtures and confirm provider compatibility and recovery behavior before production use.

Do you find this helpful?

A useful extension is to write one fixture for a real integration in which field names and types stay unchanged but meaning changes. The contract should expose the difference before any destination write.

A data contract earns its value when it catches the changes that look harmless: a renamed unit, a reused field, a version that means something new. Validating at the boundary, quarantining what fails, and versioning interpretations keep bad data out of the client’s systems and make replay predictable. With the data itself under control, the next lesson turns to the environment it runs in: security, compliance, and deployment.

Handling Failures, Rate Limits, and Silent Errors

Designing for Client Security and Deployment Environments

Ask

[Does duration: 120 mean 2 hours or 120 hours?](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Does-duration-120-mean-2-hours-or-120-hours)

[The worker, entry, and fields being mapped](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#The-worker-entry-and-fields-being-mapped)

[What makes an E41 update acceptable](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#What-makes-an-E41-update-acceptable)

[Where rejected revision 7 goes](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Where-rejected-revision-7-goes)

[What changes when Time v2 arrives](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#What-changes-when-Time-v2-arrives)

[Which interpretation replay should use](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Which-interpretation-replay-should-use)

[Evidence that makes a mapping change safe](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Evidence-that-makes-a-mapping-change-safe)

[Practice: Deriving Fen Water’s contract from its own facts](https://www.educative.io/courses/forward-deployed-engineer/data-contracts-validation-and-schema-changes#Practice-Deriving-Fen-Waters-contract-from-its-own-facts)