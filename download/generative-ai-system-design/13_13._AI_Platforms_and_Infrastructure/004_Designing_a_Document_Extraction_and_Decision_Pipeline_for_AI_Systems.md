# Designing_a_Document_Extraction_and_Decision_Pipeline_for_AI_Systems

Source: https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design a Document Extraction and Decision Pipeline

Design a document extraction and decision pipeline that turns invoices, claims, and clinical notes into trustworthy decisions at 250K documents a day. It combines OCR, schema-based extraction with field-level provenance, deterministic validation, and confidence-based routing to automation or human review, all backed by an immutable audit trail.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Resource-estimation)
  - [Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Storage-estimation)
  - [Compute estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Compute-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Bandwidth-estimation)
- [System design of a document extraction and decision pipeline](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#System-design-of-a-document-extraction-and-decision-pipeline)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#High-level-design)
    - [Major subsystems](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Major-subsystems)
    - [Control points that matter](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Control-points-that-matter)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Achieving-functional-requirements)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#A-detailed-system-design)
  - [Understanding and extraction path](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Understanding-and-extraction-path)
  - [Validation, routing, and review](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Validation-routing-and-review)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Workflow-of-the-system)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Achieving-nonfunctional-requirements)
  - [Reliability and compliance](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Reliability-and-compliance)
  - [Observability](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Observability)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Conclusion)

Messy PDFs break automation long before model accuracy becomes the only issue. A payment system may receive clean digital invoices, skewed phone photos of receipts, scanned insurance claims, and clinical notes full of handwriting. It must then turn them into trustworthy decisions without losing track of where each field came from.

This lesson treats that problem as reusable platform infrastructure. The document extraction and decision pipeline acts like a multimodal backend service that accepts files, normalizes them, extracts structured data, validates it, and decides whether to automate or escalate. The same pattern works for invoices, claims, contracts, and clinical notes.

The hard part is not merely reading text. The hard part is sustaining throughput, preserving provenance, and routing risky cases to humans before a consequential action fires.

We will walk through estimation, ingestion, OCR and parsing, schema-based extraction, validation, confidence scoring, deterministic decisioning, review, and audit logging. That flow gives you one interview answer that adapts to many prompts.

> **Note:** In these systems, perfect extraction is not the target. Safe automation with bounded failure is the target.

That estimation-first mindset carries into the next lesson, where cost becomes the main constraint at much larger scale.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#System-requirements)

Let's scope our design problem with the following requirements.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Functional-requirements)

- **Document intake:** The system should accept PDFs, phone photos, and scans from API, mailbox, and SFTP sources.
- **Structured extraction:** The system should fill a schema, with provenance to the page, bounding box, and source snippet for every field.
- **Validation and routing:** The system should run deterministic checks, then route by confidence and field criticality to automation, review, or rejection.
- **Human review:** The review UI should show fields over the source document and log every correction.
- **Audit and replay:** The system should keep an immutable history of model, schema, and user actions for every decision.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Nonfunctional-requirements)

- **Throughput:** The system should handle 250K documents a day, about 2.9 per second on average and 8.7 at peak.
- **Quality:** The system should reach 75 percent straight-through processing with bounded error on critical fields.
- **Review SLA:** The team should size reviewers to the exception queue so backlog never outgrows the SLA.
- **Reliability:** The system should use durable queues, idempotent jobs, retries, and dead-letter queues.
- **Security and compliance:** The system should encrypt data, isolate tenants, enforce regional boundaries, and redact PII or PHI where needed.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Resource-estimation)

Let's estimate the storage, compute, and bandwidth this pipeline needs, starting with storage.

### Storage estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Storage-estimation)

Let's start with volume before boxes and arrows. Suppose that the platform handles 250K documents per day across invoices, claims, and notes, with an average of 3 pages per document. That yields 750K pages daily. If 60% are scanned, OCR capacity must be sized for 450K page images each day.

Pages and tokens drive different resources. OCR and image preprocessing scale with page count, while LLM-based validation or summarization scales with tokenized text. If each page produces roughly 800 OCR tokens, the pipeline sees about 600 million tokens per day after extraction.

Storage breaks into several layers.

- **Raw documents:** These stay in object storage for replay, compliance, and audit.
- **OCR text and** **bounding boxes****:** These store extracted text plus coordinates for later review and provenance.
- **Structured outputs:** These hold JSON records, line items, classifications, and routing outcomes.
- **Audit logs:** These capture model version, schema version, user actions, and downstream writes.
- **Review artifacts:** These include reviewer annotations, snapshots, and correction histories.

Sizes make this concrete. Raw files at about 2 MB each create about 500 GB a day, or about 180 TB a year before replication. OCR text and bounding boxes add about 40 GB a day, review artifacts about 30 GB, audit logs about 5 GB, and structured outputs about 1 GB. In total that is about 575 GB a day, or about 210 TB a year, and raw files make up roughly 87 percent of it.

Let's assume a peak multiplier of 3 during business-hour uploads. Average throughput becomes about 2.9 documents per second, but peak ingest approaches 8.7 documents per second. Reviewer capacity must be estimated separately. If straight-through processing reaches 75%, then 62.5K documents still need review daily. It is safer to overestimate that queue. A human review backlog hurts the SLA faster than a temporary compute spike.

Staffing follows from field-level review. If every field in those 62.5K documents were reviewed, at 20 fields and about 25 seconds each, that is about 8,700 reviewer-hours a day. Reviewers usually check only the flagged fields, so at about 4 flagged fields per document the load drops to about 1,700 hours a day, or roughly 290 reviewers at 6 productive hours each.

The estimator below lets us vary these assumptions.

Review Capacity Estimator

Vary volume, straight-through rate, and review effort to see how many reviewers the exception queue needs.

Documents per dayD

docs

Straight-through rateS

%

Fields per documentF

fields

Flagged fields per review documentG

fields

Review time per fieldT

seconds

Productive hours per reviewer per dayH

hours

Documents needing review per dayN

62,500docs

Reviewer-hours if every field is reviewedHall​

8,681hours

Reviewer-hours if only flagged fields are reviewedHflag​

1,736hours

Reviewers neededW

289reviewers

**62,500** documents need review each day. Reviewing every field would take **8,681** reviewer-hours, but reviewing only flagged fields takes **1,736** hours, or about **289** reviewers.

Do you find this helpful?

Next comes compute sizing, where worker pools often become the first bottleneck.

### Compute estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Compute-estimation)

Compute in this pipeline is split by job type rather than by a single model endpoint. OCR workers process images, classification workers detect document type and layout family, extraction workers run parsers or multimodal models, validation services execute deterministic checks, and the review backend serves the reviewer UI.

Extraction often dominates spend when the system uses layout-aware models or LLMs over long documents. In scan-heavy workloads, OCR can dominate instead. The design should support both patterns without rebuilding the platform.

A simple interview estimate keeps the math rough but directional. At 250K documents per day, average throughput is under 3 documents per second. With a 3x peak multiplier and an average of 3 pages per document, peak page processing can exceed 25 pages per second. Batch uploads from email drops or nightly SFTP feeds make bursts sharper, so queues absorb spikes and workers scale against backlog.

Tiered serving helps control cost.

- **Deterministic parsers:** These handle known templates and digital-born PDFs cheaply.
- **General extraction models:** These process unfamiliar layouts and mixed formatting.
- **Expensive multimodal calls:** These are reserved for hard pages, tables, handwriting, or failed earlier stages.

> **Practical tip:** The fastest capacity win usually comes from raising straight-through processing, not from shaving milliseconds off one model.

Workers should run idempotent jobs, enforce concurrency limits, and push oversized or poisoned documents into a dead-letter queue. With compute bounded, bandwidth is the next layer.

### Bandwidth estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Bandwidth-estimation)

Bandwidth is usually secondary to compute, but image-heavy flows can still matter. If each raw document averages 2 MB, then 250K daily uploads create roughly 500 GB of ingress before replication. Internal traffic grows when workers repeatedly fetch page images from object storage, write OCR outputs, and generate review snapshots.

Text outputs are small. Extracted JSON, confidence metadata, and audit records are tiny compared with scanned pages. The expensive movement happens inside the platform when preprocessing services, OCR workers, and extraction workers pass around page images or rendered tiles.

Compliance can multiply traffic. Cross-region archival, tenant-isolated storage, or separate PHI retention zones may replicate both raw files and review artifacts.

> **Attention:** Internal network costs can become noticeable when each page is rendered several times by different services.

With the resource model set, we can describe the architecture that fits those capacities.

## System design of a document extraction and decision pipeline[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#System-design-of-a-document-extraction-and-decision-pipeline)

Let's start with the high-level design.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#High-level-design)

The platform is easiest to reason about as five cooperating subsystems plus shared platform controls. A document arrives from an upload widget, mailbox connector, API, or SFTP feed. The ingestion service stores the raw file, records metadata, and places a durable job onto a queue so downstream work can proceed asynchronously.

#### Major subsystems[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Major-subsystems)

From there, the architecture divides responsibilities across clear services.

- **Ingestion and preprocessing:** This stage normalizes files, renders pages, detects native text, and prepares images for OCR.
- **Document understanding:** This stage classifies document type, language, and layout family so later services know which schema and parser strategy to use.
- **Schema extraction and validation:** This stage produces structured fields, line items, and provenance, then runs deterministic checks.
- **Decision and routing:** This stage applies confidence and criticality policies to choose automation, review, or rejection.
- **Human review plus audit:** This stage exposes a reviewer UI, captures corrections, and preserves immutable event history.

#### Control points that matter[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Control-points-that-matter)

Two controls determine whether the design is safe in production.

A straight-through processing metric tracks the percentage of documents that complete without human intervention. The router should not only inspect confidence. It should also inspect field criticality. A missing shipping address might tolerate review delay. A wrong total amount should block payment immediately.

Even when extraction uses generative models, consequential actions should be guarded by deterministic business rules. We can think of the model as a skilled clerk and the rules engine as the final checklist before releasing funds.

> **Note:** Generative extraction can suggest data, but approval, denial, and payment actions should still pass explicit rules.

The system also enforces tenant isolation, encryption, regional boundaries, and immutable audit logs. With the flow in place, we can decompose the services.

The architecture becomes clearer when the automation path and review loop are shown side by side.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271767.8000000000002%27%20height=%27514%27/%3e)![Pipeline with review loop](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Pipeline with review loop")

Pipeline with review loop

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Achieving-functional-requirements)

Each functional requirement maps to a component in this architecture.

- **Document intake**: The ingestion service accepts uploads, mailbox, API, and SFTP files, stores the raw file, and queues a durable job.
- **Structured extraction**: Document understanding selects the schema and parser, and extraction fills the schema with provenance for every field.
- **Validation and routing**: Deterministic validation and the confidence router send each record to automation, review, or rejection.
- **Human review**: The reviewer UI overlays extracted fields on the source document and logs every correction.
- **Audit and replay**: The audit log records model, schema, and user actions for every state change.

Now we zoom into the component mechanics and the evidence each stage must preserve.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#A-detailed-system-design)

The detailed design starts with ingestion because correctness problems begin there, not at the model. The ingestion service computes a content hash for deduplication, runs malware scanning, detects file type, and stores the raw artifact in object storage. PDFs then pass through text detection. Native PDFs skip OCR where possible, while scanned PDFs and images go through page splitting, deskewing, denoising, and OCR with bounding boxes.

### Understanding and extraction path[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Understanding-and-extraction-path)

After text becomes available, the system chooses how to read the document.

Classification predicts document type, language, and layout family. Layout family matters because a recurring vendor invoice can use a cheap template parser, while an unseen claim form may require a general model. A schema registry provides the extraction contract.

Extraction should target a schema rather than free-form text. Required fields, nested line items, numeric types, and date formats are specified up front. Each extracted field also carries provenance back to page number, bounding box, and source snippet.

### Validation, routing, and review[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Validation-routing-and-review)

Once the structured record exists, the platform checks whether it is safe to act on.

- **Validation rules:** These enforce arithmetic checks, date ordering, master-data lookups, duplicate detection, and format constraints.
- **Field confidence:** These combine OCR confidence, calibrated model confidence, and validation outcomes into field-level scores instead of one coarse document score. Raw LLM confidence is not trusted until it is calibrated against reviewer-labeled data, per field and layout family.
- **Deterministic decisions:** These apply stricter thresholds for critical fields such as total amount, diagnosis code, or renewal date.
- **Reviewer workflow:** This presents extracted fields overlaid on the source document and logs every correction with user, timestamp, model version, and schema version.

> **Practical tip:** Review UIs should optimize the correction path, not just document viewing. Every extra click reduces effective throughput.

The following illustration brings the ingestion, understanding, extraction, validation, routing, review, and audit components together into one detailed design.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%272000.04%27%20height=%27488.03999999999996%27/%3e)![Detailed design of a document extraction and decision pipeline](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of a document extraction and decision pipeline")

Detailed design of a document extraction and decision pipeline

Next, the runtime workflow shows how these services cooperate on each document.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Workflow-of-the-system)

The request life cycle is simple when described one step at a time. A document arrives through upload, mailbox ingestion, API submission, or file drop. The ingestion layer stores the raw file, computes a content hash, and drops an idempotent job into a durable queue.

Preprocessing then detects whether the file contains native text or scanned pages. Native text extraction runs first when possible. Otherwise, image cleanup and OCR generate text blocks plus coordinates. The document-understanding service classifies type, language, and layout family, then selects a schema and parser strategy.

Extraction fills the target schema and attaches provenance to every field. Validation services then run arithmetic checks, required-field checks, duplicate detection, and business lookups. The confidence router inspects both scores and criticality. High-confidence, valid records proceed down the straight-through path into ERP, claims, or case-management systems. Low-confidence or high-risk records are placed into the review queue.

Reviewer corrections flow back into labeled data sets, template updates, and threshold tuning. Retries handle transient OCR or model failures, dead-letter queues isolate poisoned files, and downstream writes remain idempotent. Every state change is copied into the audit trail before processing closes.

That flow needs nonfunctional support to stay fast, resilient, and auditable under sustained load.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Achieving-nonfunctional-requirements)

Nonfunctional behavior comes from the mechanics already described. Performance improves when OCR batches pages, high-volume templates are cached, and cheap parsers run before expensive multimodal extraction. Scalability comes from stateless workers behind queues that autoscale on page backlog rather than raw request count.

### Reliability and compliance[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Reliability-and-compliance)

Availability relies on multi-AZ queues, replayable jobs, idempotent writes, and circuit breakers around external OCR or LLM vendors. Security relies on encryption, role-based reviewer access, redaction where needed, and regional data boundaries for PII or PHI workloads. Idempotency is essential for safe reprocessing.

### Observability[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Observability)

Dashboards should track field-level accuracy, drift by vendor or layout family, straight-through processing rate, reviewer backlog, and queue age. We can think of this like a factory line with a rework bench. The useful metric is not only inspector accuracy, but also how many units clear the line without piling up at rework.

> **Attention:** A system can show excellent model accuracy and still fail operationally if reviewer backlog or queue age grows unchecked.

Those operating signals are exactly what an interviewer will probe, so the lesson ends with a reusable pattern and a short knowledge check.

Knowledge Check

Q1. Why should the router check field criticality as well as confidence?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Conclusion)

A strong interview answer follows one reusable pattern. It estimates document and review volume, ingests safely, extracts against a schema, validates deterministically, routes by confidence and criticality, and preserves provenance for every decision.

That architecture generalizes across invoices, claims, contracts, and clinical notes with only schema and policy changes.

Design an AI Content Moderation System

Design for Cost at 1M Queries a Day

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Resource-estimation)

[Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Storage-estimation)

[Compute estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Compute-estimation)

[Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Bandwidth-estimation)

[System design of a document extraction and decision pipeline](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#System-design-of-a-document-extraction-and-decision-pipeline)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#High-level-design)

[Major subsystems](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Major-subsystems)

[Control points that matter](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Control-points-that-matter)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Achieving-functional-requirements)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#A-detailed-system-design)

[Understanding and extraction path](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Understanding-and-extraction-path)

[Validation, routing, and review](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Validation-routing-and-review)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Workflow-of-the-system)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Achieving-nonfunctional-requirements)

[Reliability and compliance](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Reliability-and-compliance)

[Observability](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Observability)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-document-extraction-and-decision-pipeline#Conclusion)