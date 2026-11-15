# Designing_Health_Data_Systems_with_Compliance_and_Integrity

Source: https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# System Design: The Health Data Hub

Examine the architecture of the National Health Data Office's data hub, including source adapters, patient views, and reporting extracts. Distinguish what acknowledgements, durable ingestion, and data normalisation confirm at each stage of processing. Define release criteria and track completion evidence for each destination to verify that reports meet delivery requirements.

We'll cover the following...

- [What the hospital’s acknowledgment promises](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-the-hospitals-acknowledgment-promises)
- [The contracts the three adapters implement](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#The-contracts-the-three-adapters-implement)
- [Where the hub accepts durable responsibility](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#Where-the-hub-accepts-durable-responsibility)
- [What survives normalization of LAB-884](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-survives-normalization-of-LAB-884)
- [When a report may enter a patient view or extract](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#When-a-report-may-enter-a-patient-view-or-extract)
- [What proves that LAB-884 became available](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-proves-that-LAB-884-became-available)
- [Practice: Designing OP-91’s path independently](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#Practice-Designing-OP-91s-path-independently)

Trace report LAB-884 through six processing and delivery milestones:

- **10:00:** Report published by the source.
- **10:00:01:** Report durably stored in the hub's intake system.
- **10:00:02:** Hub sends the hospital an acknowledgement confirming durable receipt.
- **10:00:04:** Report normalised into the hub's internal data model.
- **10:00:06:** Receiving system confirms acceptance of the report.
- **10:00:08:** Report availability confirmed through the authorised consumer's workflow.

The hospital receives a successful intake acknowledgement six seconds before the report becomes available to the care team. The National Health Data Office's ingestion hub must define and track intake acknowledgements and downstream availability separately.

The hub must acknowledge durable receipt so the source can safely hand off delivery responsibility under the agreed contract. Monitoring must distinguish successful intake from confirmed downstream availability.

## What the hospital’s acknowledgment promises[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-the-hospitals-acknowledgment-promises)

An acknowledgement confirms that the receiver met the agreed acceptance conditions. Downstream availability requires separate verification.

In HL7 v2.5.1 original acknowledgement mode, transport success alone does not confirm application-level acceptance. The standard allows acknowledgement after a message enters an input queue with database-level integrity, provided the receiver accepts responsibility for subsequent processing. It does not specify the receiver's downstream workflow or architecture.

For this case, define the positive hospital acknowledgement as: "The hub accepted the message after completing the agreed validation checks and durably recorded it for recoverable processing."

Verify this acknowledgement contract against the applicable HL7 version, local message profile, acknowledgement mode, and receiver processing boundary. This acknowledgement does not confirm downstream delivery, consumer access, or clinical review.

Keep the scoped workflows separate:

- **Hospital care access:** Proposed target of five minutes from source publication to availability in the authorised receiving workflow.
- **Clinic care access:** Separate workflow with a proposed fifteen-minute target from source publication to authorised availability.
- **Daily reporting:** Proposed target to make the approved reporting extract available by 06:00.

These targets remain provisional until the client approves them and feasibility testing confirms they are achievable.

Defer the weekly community-screening source from same-day patient-linked care access. Faster ingestion cannot overcome its weekly publication schedule or the lack of an assigned owner for patient identity resolution.

## The contracts the three adapters implement[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#The-contracts-the-three-adapters-implement)

Validate these interface assumptions with the source owners. Do not proceed with onboarding until the required capabilities are confirmed.

1. **Hospital:** Uses HL7 v2.5.1 `ORU^R01` messages with a local laboratory message profile and original acknowledgement mode, both subject to confirmation. Confirm required message segments, identifier authorities, report status handling, transport protocol, validation rules, and the conditions for acknowledging messages accepted into the durable input queue.
2. **Clinic:** Assumes FHIR R4 (4.0.1), with local profiles for `DiagnosticReport` and `Observation` and patient references scoped to the source system. Verify supported read and change-detection interactions, including retrieval of referenced resources, and validate whether the ingestion process can meet the proposed fifteen-minute freshness target. Do not assume the server supports subscriptions, resource history, or specific search parameters without verifying its capabilities.
3. **Regional laboratory:** Assumes a CSV export for the previous reporting day, scheduled for delivery at 02:00 using the `regional-lab-csv-v1` contract. Confirm the file schema, identifier authorities, timezone, reporting period, file identification rules, checksum validation, delivery mechanism, and signal indicating that the complete file is available.

A protocol or data format alone does not define the required interface contract. If the clinic cannot provide an agreed method for identifying changes, a polling worker cannot reliably determine which records need to be retrieved.

## Where the hub accepts durable responsibility[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#Where-the-hub-accepts-durable-responsibility)

Consider a flawed implementation: The hospital adapter sends a positive acknowledgment while `MSG-884` exists only in memory. The process restarts before persistence; the source treats the acknowledgment as successful acceptance and stops ordinary retransmission. Meanwhile, a dashboard labels LAB-884 “delivered.”

Repair the acceptance boundary before adding more workers:

Repair MSG-884’s Acknowledgment

1.

MSG-884 was positively acknowledged while held only in memory. A restart erased it, and the hospital stopped ordinary retransmission. The agreed acknowledgment promises recoverable processing, not care team availability. Which is the earliest defensible positive application acknowledgment boundary?

> **Note:** For this repair, raw storage is separate from the database. The database can atomically commit an intake-ledger entry and pending work referencing verified raw content.

A.

After persisting the raw object, before registering intake and pending work.

B.

After verifying raw persistence, atomically committing intake-ledger and pending-work entries, and passing agreed acceptance checks.

C.

After placing MSG-884 in an in-memory processing queue.

D.

After network receipt confirms that all message bytes arrived.

---

1 / 2

The repair also gives operations an audit check: Follow the accepted intake entry to both its raw-content reference and its pending-work entry. A dashboard acceptance claim must be traceable to that committed obligation, not inferred from an acknowledgment log alone.

Use one intake pattern behind all three adapters:

1. Persist encrypted source content in restricted raw storage under approved controls.
2. Verify the stored content’s checksum.
3. Atomically commit an intake-ledger entry and a pending-work entry referencing that content.
4. Issue the transport-specific acceptance evidence only after this commit and required acceptance checks.

The raw-object write precedes the ledger transaction; no cross-store atomic transaction is assumed. An incomplete write cannot support durable acceptance, and an unreferenced object does not count as accepted work. The ledger transaction ensures that accepted intake always has recoverable pending work.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271151%27%20height=%27511%27/%3e)![Securing clinical data ingestion and delivery](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Securing clinical data ingestion and delivery")

Securing clinical data ingestion and delivery

Define the durable acceptance boundary for each source interface:

- **Hospital:** At 10:00:01, validate the raw message and atomically commit it with its processing work record to durable storage. At 10:00:02, send the agreed application acknowledgement confirming durable acceptance.
- **Clinic:** A successful HTTP response confirms the request succeeded, but the hub must also verify that the expected resource data was returned. Advance the capture checkpoint only after the required response data and associated processing records are durably committed.
- **CSV:** A completed upload confirms transport receipt, not file validation or acceptance. Create a hub acceptance record only after verifying file completeness, validating the manifest, and durably committing the file and its processing work record.

Each acceptance record must identify the accepted message, captured resource set, or file and include a reference for tracking its processing status. Track processing states separately, including `accepted`, `normalized`, `identity-held`, `delivery-pending`, and `available`, so monitoring does not report successful receipt as confirmed downstream availability.

## What survives normalization of LAB-884[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-survives-normalization-of-LAB-884)

Normalize into a **versioned report envelope**: A shared processing representation that preserves source meaning and interpretation provenance. It supports consistent auditing without claiming to create a national clinical record.

For LAB-884, the envelope retains:

- **Source identity:** `HOSP-A`, patient reference `HOSP-A/4172`, source report `LAB-884`, and original message identifier `MSG-884`.
- **Source state:** Status `final` and the source revision when supplied. If no separate revision exists, record its absence and the source-agreed version discriminator; never manufacture revision `1`.
- **Timing and provenance:** Publication at 10:00, ingestion at 10:00:01, raw-content hash and reference, parser `hospital-v1`, and mapping `lab-report-v3`.
- **Meaning:** Source codes, units, and reference relationships alongside approved mapped fields. Unsupported meanings remain unresolved; missing source evidence remains explicitly unknown.

For clinic report `CL-55`, preserve its link to `Observation/OBS-55` and its `Patient/4172` reference scoped to the clinic’s source base. In FHIR R4, `DiagnosticReport` supplies clinical or workflow context for observations and references `Observation` resources to form a complete report. Flattening unrelated values into a patient row loses that relationship.

For regional CSV rows, retain file identity and row location. This lets a reviewer recover both the original evidence and the interpretation applied to it.

A shared FHIR-shaped model does not establish semantic equivalence. Source release, local profiles, identifier authority, permitted uses, and approved patient associations still govern processing. Replacing both `HOSP-A/4172` and `CLINIC-B/4172` with `patient_id: 4172` destroys the scope required to prevent an unsupported association.

## When a report may enter a patient view or extract[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#When-a-report-may-enter-a-patient-view-or-extract)

Require two independent decisions: Patient association and permission for the intended use.

For this case, assume the approved identity authority associates `HOSP-A/4172` with hub patient reference `NHD-920`. Record the authority and association version. Normalization itself has no authority to merge patients.

Clinic patient `CLINIC-B/4172` has no approved cross-source association. Keep CL-55 source-attributed, hold it from the cross-source patient view, and assign an identity-review work item to Morgan, the named identity steward for this case. The equal local number supplies no association evidence.

Even a valid association does not grant access. Before exposure or delivery, check:

- Receiving organization and authorized purpose.
- Permitted fields and current access policy.
- Destination-specific workload permissions.

Apply permissions at intake and again at downstream access and delivery. The regional file may feed only its separately approved reporting workflow; reporting approval grants no care-team access.

Source preservation also grants neither general access nor indefinite retention. Raw content, normalized copies, reporting extracts, and audit records all remain subject to approved access, residency, and retention controls.

## What proves that LAB-884 became available[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-proves-that-LAB-884-became-available)

After normalisation and the required validation and authorisation checks, atomically commit the normalised state and its delivery intent. Delivery workers process the recorded intent using permissions scoped to the target destination.

Assign a stable operation ID to the delivery of a specific LAB-884 source version to the receiving care workflow. Assign a unique attempt ID to each delivery attempt while retaining the same operation ID across retries. Keep operation and attempt IDs separate from the source report ID, source revision or agreed version discriminator, and transport message ID (`MSG-884`).

Record the destination, source version, mapping version, authorisation decision reference, operation ID, attempt ID, attempt result, receiving-system receipt, and downstream availability evidence in the delivery ledger.

For each event in the trace, identify what it is expected to confirm, then inspect the supporting evidence.

LAB-884: predict the strongest justified state

SourcePublishedHub intakeAcceptedHospital handoffProcessingNormalizedGatesDelivery-pendingIdentity checkReceiving workflowReceiving acceptedCare accessAvailable

10:0010:00:0110:00:0210:00:04Intervening step — untimed10:00:0610:00:08

PublicationSource · 1 inside

Verified storage and intake commitHub intake · 1 inside

Positive application acknowledgmentHospital handoff · 1 inside

NormalizationProcessing · 1 inside

Identity, permission, and delivery intentGates · 3 inside

Receiving workflow acceptanceReceiving workflow · 1 inside

Verified authorized availabilityCare access · 1 inside

Do you find this helpful?

At 10:00:02, the hospital has evidence of durable acceptance while care availability remains pending. At 10:00:06, the receiving receipt establishes acceptance into that workflow. At 10:00:08, destination evidence tied to LAB-884’s source version and authorized consumer scope confirms accessibility: Eight seconds from publication, within the proposed five-minute target for this event.

Keep four evidence categories distinct:

- **Request acceptance:** The adapter received the submission or response.
- **Durable responsibility:** Verified recoverable content and committed intake/work records exist.
- **Business completion:** For care, authorized receiving-workflow availability is confirmed; for reporting, approved coverage and extract-release criteria are satisfied.
- **User-visible success:** The care interface exposes the available report, or the reporting interface exposes the released extract, to its authorized user.

A queue acknowledgment, downstream HTTP success, or report count alone cannot prove all four.

The other branches use the same architecture without sharing outcomes. CL-55 is durably captured after its successful read but remains identity-held. File `regional-2026-10-25.csv` arrives at 02:00 on October 26, is registered after agreed completeness checks, and contributes only to the approved reporting extract due at 06:00 in the agreed source timezone. Its completion evidence is an approved release against coverage criteria.

## Practice: Designing OP-91’s path independently[#](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#Practice-Designing-OP-91s-path-independently)

The interviewer introduces an outpatient laboratory that delivers hourly UTF-8-encoded CSV files over SFTP using the `outpatient-v1` interface contract. Each uploaded file includes a manifest specifying the file ID, reporting hour, row count, and checksum. The source confirms that the manifest signals file completion.

The hub receives `outpatients-1000.csv` at 10:00. The file contains report `OP-91`, with source-local patient ID `SITE-C/4172`, status `final`, publication timestamp 09:52, and source revision `1`.

The reporting owner approves the specified report fields for inclusion in the daily reporting extract. Making the report available to a receiving care team requires a confirmed patient association and receiving-organisation authorisation. No approved cross-source patient association exists for `SITE-C/4172`.

Design the workflow from source adapter to authorised consumer, and create a concise state and evidence ledger from scratch.

Design OP-91’s Path

The National Health Data Office’s ingestion hub must onboard hourly UTF-8 outpatient-v1 CSV over SFTP: outpatients-1000.csv arrived at 10:00 with OP-91, SITE-C/4172, final status, publication at 09:52, and revision 1. The source confirms a complete-file manifest containing file identity, reporting hour, row count, and checksum; the reporting owner authorizes the listed report fields for the daily extract, but no approved cross-source patient association exists and care requires receiving-organization authorization. Start with empty fields: write your architecture and compact state/evidence ledger using only these facts and the lesson’s controls, choose parser and mapping version names as design decisions, and consult the reference options only after your initial response.

You'll make 3 decisions that reshape the highlighted sections — and watch the document update in real time as you go.

OP-91 Architecture and Evidence Ledger

1. Adapter and Durable IntakeConfigurable

2. Normalized Meaning and ProvenanceConfigurable

3. Identity and Consumer GatesConfigurable

4. State and Evidence Ledger

5. Review and Revise

Do you find this helpful?

Apply OP-91's identity hold only to patient-linked clinical delivery, rather than marking the report as failed across all destinations. An identity-review backlog should not block reporting workflows that have independent authorisation. Track completion status and supporting evidence separately for each destination.

The Health Data Hub design relies on verifiable processing boundaries: source acknowledgements, durable hub acceptance, validated normalised data, and destination-specific delivery confirmation. In the next lesson, evaluate this design through interview-style questions on failure scenarios and architectural trade-offs.

Decomposing the Problem: The Health Data Hub

FDE Interview Questions: The Health Data Hub

Ask

[What the hospital’s acknowledgment promises](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-the-hospitals-acknowledgment-promises)

[The contracts the three adapters implement](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#The-contracts-the-three-adapters-implement)

[Where the hub accepts durable responsibility](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#Where-the-hub-accepts-durable-responsibility)

[What survives normalization of LAB-884](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-survives-normalization-of-LAB-884)

[When a report may enter a patient view or extract](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#When-a-report-may-enter-a-patient-view-or-extract)

[What proves that LAB-884 became available](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#What-proves-that-LAB-884-became-available)

[Practice: Designing OP-91’s path independently](https://www.educative.io/courses/forward-deployed-engineer/system-design-the-health-data-hub#Practice-Designing-OP-91s-path-independently)