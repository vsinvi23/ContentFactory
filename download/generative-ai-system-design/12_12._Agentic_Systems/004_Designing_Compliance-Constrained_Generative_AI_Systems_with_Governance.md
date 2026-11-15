# Designing_Compliance-Constrained_Generative_AI_Systems_with_Governance

Source: https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design a Compliance-Constrained Generation System

Explore how to design generative AI systems constrained by compliance requirements, emphasizing evidence-backed outputs, policy enforcement, and human oversight. Understand system components for traceability, audit logs, and handling high-risk outputs, ensuring safe and auditable generation for regulated domains like legal and healthcare.

We'll cover the following...

- [Designing for evidence first](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Designing-for-evidence-first)
- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Resource-estimation)
  - [Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Storage-estimation)
  - [Compute estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Compute-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Bandwidth-estimation)
- [System design of compliant generation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#System-design-of-compliant-generation)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#High-level-design)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Achieving-functional-requirements)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#A-detailed-system-design)
  - [Evidence retrieval and policy enforcement](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Evidence-retrieval-and-policy-enforcement)
    - [Query handling and approved-source retrieval](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Query-handling-and-approved-source-retrieval)
  - [Operational memory and constrained generation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Operational-memory-and-constrained-generation)
    - [Operational memory, not evidence](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Operational-memory-not-evidence)
    - [Constrained generation and verification](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Constrained-generation-and-verification)
  - [Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Putting-everything-together)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Workflow-of-the-system)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Achieving-nonfunctional-requirements)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Conclusion)

A legal or medical assistant becomes dangerous the moment it states something that cannot be traced to approved evidence. In an interview, that shifts the problem away from building a clever RAG bot and toward building a governed generation pipeline in which unsupported text is mechanically hard to produce.

## Designing for evidence first[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Designing-for-evidence-first)

A compliance-constrained system starts with a simple rule. The model is not the source of truth. The approved corpus is.

That changes the request life cycle. The user does not ask a model for an answer directly. The request first enters policy checks, then retrieval restricted to approved documents, then a generation stage that must stay within those retrieved facts, and then a verification stage that can still reject parts of the draft before release.

> **Note:** Agentic behavior still exists here, but the agent is fenced in by policy, evidence, and review checkpoints.

In practice, this design targets assistants for legal drafting, clinical summarization, benefits explanation, or regulated finance communication. These are not ordinary chat products. The system must reconstruct why a sentence was shown, which source version supported it, which model and prompt were used, and whether a human signed off.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#System-requirements)

Requirements are stricter than normal RAG, so fix them before sizing anything.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Functional-requirements)

- **Traceability:** Every claim must point to stable source identifiers, versions, and spans.
- **Source control:** Retrieval must exclude unapproved material before ranking or synthesis occurs.
- **Auditability:** Inputs, intermediate artifacts, and release decisions must remain reconstructable later.
- **Compliance:** Policies must enforce disclaimers, jurisdiction limits, and refusal behavior for unsupported requests.
- **Human oversight:** High-risk outputs require reviewer sign-off before release.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Nonfunctional-requirements)

- **Latency:** Answers without human review return in seconds, and reviewed answers return a pending status instead of blocking.
- **Scalability:** Serve about 20,000 sessions per day, with peaks around 5 times the average.
- **Availability:** Fail toward safe behavior by refusing or holding an answer instead of releasing unverified text.
- **Reliability:** Keep audit logs append-only and tamper-evident, with idempotent review actions.
- **Security and privacy:** Enforce role-based access, encryption, tenant isolation, and minimal prompt exposure of sensitive records.
- **Cost:** Bound verifier calls per answer, since verification can cost more than generation.

A useful mental model is a pharmaceutical label, not a chatbot. Every line needs backing, and every revision needs records.

The design path in interviews should follow a predictable order. We estimate scale first, then restrict retrieval to the approved corpus. After that, the system generates structured claims, binds citations, verifies support, escalates risky cases to humans, and stores an append-only trail for audits. That estimation-first view sets up the sizing discussion next.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Resource-estimation)

Let's size the system from one workload: 50,000 approved documents, 20,000 sessions per day with 3 queries each, 10 percent of sessions high-risk, 18 audit events per session, and a 5 times peak. Every number below derives from these assumptions.

### Storage estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Storage-estimation)

Let's start with the corpus, then add what every session leaves behind. The corpus is small, about 44 GB for the workload below, but the audit trail grows every day and dominates over a seven-year retention window.

Let's assume 50,000 approved documents with an average of 4,000 tokens each. If chunking uses 400-token windows with overlap, each document yields roughly 12 chunks, producing about 600,000 chunks. Each chunk record stores text, normalized metadata, access tags, validity windows, and a stable span identifier, which comes to about 2.5 KB, or 1.5 GB in total. Embeddings at 1,024 float32 values take 4 KB each, about 2.4 GB. Each retained version also keeps an immutable source file of about 200 KB, so 4 versions of 50,000 documents add about 40 GB. The corpus totals roughly 44 GB.

A chunk lineage is required so citations survive reindexing. You also need immutable snapshots of each source version. If policies require seven-year retention and quarterly updates, version multiplication is real system data, not archival trivia.

Per-session storage also grows quickly. Each interaction can persist the user prompt, normalized query, retrieved chunk IDs, evidence package, generated claim objects, verification results, review notes, and append-only audit events. Signed policy snapshots and prompt registry references add more rows. We also assume 20,000 sessions per day with 18 audit events each. At about 1 KB per event that is 360 MB per day, and the evidence package for each session (claims, retrieved chunk IDs, verification results) adds about 1 GB per day. Over seven years the audit trail reaches roughly 3.6 TB, far larger than the corpus.

> **Attention:** Candidates often count embeddings and forget reviewer artifacts, policy snapshots, and span-level citation bindings.

A realistic footprint includes 600,000 active chunks, 4 retained versions per document, and about 11 million audit events per month. The system stores more metadata than ordinary RAG because provenance must outlive product changes and disputes. With the storage shape clear, the next step is throughput sizing.

### Compute estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Compute-estimation)

Inference capacity must be sized per stage, not per request. One user query can trigger retrieval fan-out, synthesis, claim extraction, support verification, and possibly review queueing.

Let's assume two request classes. Low-risk informational questions may return three claims and skip human review. High-risk recommendation flows may produce about eight claims, each requiring stricter support checks and possibly reviewer approval. In that mix, generation QPS alone is misleading because the verifier tier often dominates both latency and compute. With 20,000 sessions per day and 3 queries each, that is 60,000 queries per day, about 0.7 QPS on average and 3.5 at peak. Counting 6 verifier calls for a low-risk answer and 16 for a high-risk one, the average is 7 per query, so the verifier tier sees about 5 calls per second on average and about 24 at peak, roughly 7 times the generation request rate.

An entailment model may run once per claim or once per claim-source pair. If each high-risk answer has eight claims and each claim checks against the top two spans, verification fans out to sixteen model calls. That can exceed the cost of one synthesis pass.

We size the system as separate pools.

- **Retrieval workers:** These handle metadata filtering, vector search, and evidence packaging.
- **Generation servers:** These produce structured drafts with citation placeholders.
- **Verification workers:** These run lexical checks, entailment scoring, and policy rule validation.
- **Review processors:** These manage asynchronous queues, SLA timers, and reviewer actions.

Deterministic template blocks reduce both cost and variance for disclaimers, statutory notices, and escalation instructions. During policy updates or document refreshes, expect bursts from reindexing and replay evaluation, not just live traffic.

Separating the compute tiers shows which services exchange the largest internal payloads.

### Bandwidth estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Bandwidth-estimation)

User-facing traffic is usually the smallest bandwidth category. Internal service-to-service transfers carry the heavy payloads.

Each request sends a prompt inward and returns a short answer outward, but retrieval services may send dozens of chunk payloads plus provenance metadata to the generation layer. Verification may then receive claim objects, candidate source spans, and policy context. In enterprise deployments, reviewer screenshots, annotations, or document previews add even more bytes.

A simple estimate uses four streams. Ingress includes user prompts and session metadata. East-west traffic includes evidence packages, citation spans, and verifier requests. Egress includes the released answer and citations. Audit traffic includes append-only events and out-of-band references to larger artifacts.

> **Practical tip:** Pass chunk IDs and fetch text lazily where possible. Repeating full chunk text across services inflates bandwidth and increases leakage surface.

Multiregion compliance adds another constraint. Data residency can require regional isolation for prompts, documents, and logs, so cross-region replication may be limited to model metadata or policy digests. The estimator below lets us change the workload and see which resource dominates before drawing the architecture.

Compliance System Capacity Estimator

Adjust the workload to see which resource dominates: corpus storage, audit growth, or verifier load.

Approved DocumentsD

docs

Chunks per DocumentC

chunks

Sessions per DayS

sessions

Queries per SessionQ

queries

High-Risk Share of SessionsH

%

Audit Events per SessionE

events

Peak MultiplierM

×

Retention PeriodY

years

Total ChunksN

600,000chunks

Corpus StorageGcorpus​

43.9GB

Audit Growth per DayGday​

1.4GB/day

Audit Storage over RetentionTaudit​

3.577TB

Average QPSQPSavg​

0.6944req/s

Peak QPSQPSpeak​

3.4722req/s

Verifier Calls per QueryV

7calls

Peak Verifier CallsVpeak​

24.3056calls/s

Human Reviews per DayR

2,000reviews

The corpus needs about **43.9 GB**, but the audit trail reaches **3.577 TB** over the retention window. Peak load is **3.4722 QPS** for generation and **24.3056 calls/s** for verification, with **2,000 reviews** per day.

Do you find this helpful?

## System design of compliant generation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#System-design-of-compliant-generation)

Let's start with the high-level design.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#High-level-design)

The system is built around evidence flow and decision checkpoints. A request enters through an API layer that authenticates the caller, applies authorization, and loads the active policy set for that user and jurisdiction. Only then does the request move into retrieval.

The retrieval subsystem searches a curated corpus that contains approved, versioned documents only. Metadata filters execute before ranking so disallowed material never becomes a candidate. Retrieved chunks are packaged with stable source IDs, version IDs, and source spans.

The generation subsystem does not emit free-form prose first. It drafts structured claims tied to evidence references. A citation assembler then resolves each claim to exact source spans. A verifier checks lexical overlap, semantic support, and policy constraints. Unsupported claims are removed or escalated.

High-risk outputs enter a human review workflow. Reviewers inspect the claims, source spans, and policy context, then approve, edit, or reject. The final response includes review status and citations where required.

Side systems are core components, not background utilities.

- **Policy store:** This serves versioned rules for jurisdiction, disclaimers, and prohibited actions.
- **Model registry:** This binds outputs to model, prompt, and decoding settings.
- **Source repository:** This preserves immutable source versions and document lineage.
- **Audit log store:** This keeps append-only records for reconstruction and dispute handling.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271394.85%27%20height=%27502.34999999999997%27/%3e)![Event-gated architecture](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Event-gated architecture")

Event-gated architecture

That high-level map is useful only if it can be tied back to the required system guarantees, which is the next step.

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Achieving-functional-requirements)

Let's walk each functional requirement above through the request path. Each one maps to a concrete mechanism.

- **Traceability:** The response object stores document ID, version ID, chunk or section ID, span offsets, and retrieval timestamp for every released claim.
- **Source control:** Retrieval is limited to approved evidence, and unsupported statements are blocked during verification before user release.
- **Auditability:** Immutable logs record inputs, retrieval results, prompts, model version, policy version, verifier outputs, and review decisions.
- **Regulatory compliance:** Deterministic templates inject required disclaimers, refusal text, and jurisdiction-specific language.
- **Human oversight:** High-risk outputs require sign-off before release, with reviewer identity and timestamps persisted.

When sources disagree, the system should not average them into a neat paragraph. It should either present a consensus-only summary or route the case for review. In other words, disagreement becomes a workflow event.

A stable identifier is what makes claim reconstruction possible months later. Privacy controls sit alongside this path. Sensitive patient or matter data is minimized in prompts, encrypted at rest, and gated by role-based access.

> **Note:** Out-of-scope handling is part of functionality. "Insufficient evidence in approved corpus" is often the correct system output.

The next section breaks the pipeline into its internal subsystems.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#A-detailed-system-design)

Let's describe the system as three cooperating internal areas. That keeps the interview answer structured and lets you attach failure modes to each boundary.

The first area handles evidence access and policy enforcement. The second performs constrained generation and verification. The third governs release through review, logging, and evaluation. No subsystem exists for convenience alone. Each one enforces an invariant on the path to release.

### Evidence retrieval and policy enforcement[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Evidence-retrieval-and-policy-enforcement)

This area decides what information is even eligible to influence the answer.

#### Query handling and approved-source retrieval[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Query-handling-and-approved-source-retrieval)

It helps to keep this layer simple in the explanation. It prepares the request for safe retrieval, not for final answering.

The service normalizes the query, strips or redacts sensitive fields when policy requires, and runs a policy classifier that extracts scope, jurisdiction, and intent. It then computes embeddings for semantic search and combines them with metadata constraints. We can think of the vector index like a library card catalog that you can search semantically, except the catalog also enforces access control and version windows.

The vector store keeps chunk embeddings together with stable document IDs, version IDs, authority scores, validity windows, and access tags. A semantic cache may store retrieval hints such as prior top chunk IDs for repeated low-risk queries, but it should not cache final answers because freshness and provenance can drift.

Before ranking, rule-based filters reject unsupported intents and remove prohibited retrieval scopes. Negative tests should prove that deprecated or unauthorized sources cannot be surfaced at all.

That retrieval boundary leads naturally to the second memory-related boundary, which supports workflow without becoming evidence itself.

### Operational memory and constrained generation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Operational-memory-and-constrained-generation)

The next area stores context and executes the draft-and-verify loop.

#### Operational memory, not evidence[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Operational-memory-not-evidence)

In regulated systems, long-term memory is operational, not evidentiary. It stores reviewer decisions, user entitlements, case metadata, and workflow state, but it must not silently become factual support for future claims.

Useful stores include session state, authorization records, review history, document lineage, and retention metadata. Sensitive records need encryption, retention windows, redaction-aware retrieval, and tenancy isolation. Conversational history can guide workflow, but it cannot justify new medical or legal claims. The approved corpus remains the only evidence memory.

Review feedback can still improve the system. It can retrain risk routing, ranking features, and deterministic templates without changing the invariant that every generated claim maps to approved source material.

#### Constrained generation and verification[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Constrained-generation-and-verification)

The model host receives the sanitized query and retrieved evidence package. It outputs structured claims, not a final polished paragraph first. Each claim includes evidence IDs or citation placeholders. Regulated sections such as contraindication language, notices, or escalation instructions are generated from deterministic templates to reduce variance.

A citation assembler resolves placeholders into exact source spans. Then the verifier runs layered checks.

- **Lexical checks:** These confirm that the cited span contains the key entities, numbers, or terms.
- **Semantic verification:** This uses entailment-style scoring to test whether the evidence supports the claim.
- **Policy validation:** This checks for missing disclaimers, prohibited advice, and jurisdiction errors.

If support is weak, the system deletes the claim or routes it for review. Output moderation here is policy enforcement, not only generic safety filtering. Safe refusal is preferable to speculative completion.

> **Attention:** A beautifully phrased answer with one uncited sentence is a failed output in this architecture.

With the internals laid out, the full production flow becomes straightforward to narrate.

### Putting everything together[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Putting-everything-together)

Let's walk through the live request path in order.

The API gateway authenticates the caller and loads user entitlements. A policy service classifies risk, extracts jurisdiction, and blocks unsupported intents. Retrieval then searches only the approved corpus under strict metadata constraints. The generation service drafts structured claims from the returned evidence package. Citation binding resolves each claim to source spans, and the verifier rejects unsupported text.

High-risk or low-confidence outputs are pushed into a reviewer queue. Subject-matter reviewers can approve, edit, or reject, and every action is idempotent so retries do not duplicate decisions. Once released, the final answer, intermediate artifacts, and decision metadata are written into an append-only audit store.

Supporting infrastructure completes the design.

- **Internal gateway:** This routes traffic to retrieval, generation, verification, and review services, each with its own load balancer across replicas.
- **Job queues:** These absorb asynchronous review and replay-evaluation workloads.
- **Version stores:** These pin model, prompt, policy, and source versions for reconstruction.
- **Observability services:** These track stage latency, verifier failure rates, and reviewer backlog.

The diagram below traces this path through the three internal areas: evidence retrieval and policy enforcement, constrained generation and verification, and release governance with an append-only audit store.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271921%27%20height=%27531%27/%3e)![Detailed design of a compliance-constrained generation system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of a compliance-constrained generation system")

Detailed design of a compliance-constrained generation system

The workflow can now be written explicitly as an operational sequence, including exception branches.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Workflow-of-the-system)

The production workflow is easiest to explain as a checkpointed pipeline.

The request is received, authenticated, and tagged with policy context. A policy gate checks authorization, jurisdiction, and whether the intent is allowed. The retrieval layer applies corpus filters, logs the retrieval event, and packages evidence with stable IDs and spans. The generation service drafts structured claims. The citation binder attaches source mappings. The verifier runs support and policy checks. If confidence is low or policy requires oversight, the response enters human review. After approval or safe refusal, the system releases the output and writes all artifacts to the audit store.

Asynchronous branches matter too. Reviewer escalation runs on queues with SLA monitoring. Historical sessions may be replayed after policy changes or corpus updates to identify regressions. If no sufficient evidence is found, the system returns an approved insufficiency response, logs the miss, and may notify corpus curators.

Failure handling should always bias toward safer user-visible behavior. Stale document versions trigger regeneration or refusal. Verifier timeouts hold or downgrade the answer. Reviewer SLA breaches can return a pending status instead of releasing unreviewed content. That operational flow leads directly into nonfunctional trade-offs.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Achieving-nonfunctional-requirements)

Performance comes from separating stages with different latency profiles. Retrieval can use cached embeddings and optimized indexes, while answer caching remains limited because source versions drift. Scalability comes from decoupling retrieval, generation, verification, and review queues because they scale with different drivers.

Availability depends on deployment rules. Multiregion replicas may be used where regulation permits, but regional isolation often takes priority for corpus and audit data. Reliability requires append-only, tamper-evident logs and replayable workflows with idempotent review actions. Security requires RBAC, encryption, strict tenant isolation, and minimal prompt exposure of sensitive records.

A tamper-evident log is especially useful during audits. Compliance robustness also requires every response to bind to policy version, model version, corpus version, and reviewer status. In high-risk systems, cross-region consistency for those versions is often worth more than shaving off a few hundred milliseconds.

Let's test our understanding of these trade-offs with the questions below.

Knowledge Check

Q1. A deprecated policy document outranks the approved ones in retrieval, and the model cites it. Where should the system have blocked it?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Conclusion)

A compliance-constrained generation system is a governed pipeline, not a general chatbot with citations sprinkled on top. The request path starts with estimation, then restricts retrieval, drafts structured claims, verifies support, routes risky cases to humans, and records every decision in an auditable trail.

In interviews, the strongest answer shows where unsupported text gets blocked, not just how the model is prompted. That framing carries directly into the next lesson, where output control remains central but the medium shifts from text to image generation.

Design an Agentic Customer Support System

Design a GenAI Gateway

Ask

[Designing for evidence first](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Designing-for-evidence-first)

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Resource-estimation)

[Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Storage-estimation)

[Compute estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Compute-estimation)

[Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Bandwidth-estimation)

[System design of compliant generation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#System-design-of-compliant-generation)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#High-level-design)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Achieving-functional-requirements)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#A-detailed-system-design)

[Evidence retrieval and policy enforcement](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Evidence-retrieval-and-policy-enforcement)

[Query handling and approved-source retrieval](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Query-handling-and-approved-source-retrieval)

[Operational memory and constrained generation](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Operational-memory-and-constrained-generation)

[Operational memory, not evidence](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Operational-memory-not-evidence)

[Constrained generation and verification](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Constrained-generation-and-verification)

[Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Putting-everything-together)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Workflow-of-the-system)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Achieving-nonfunctional-requirements)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-compliance-constrained-generation-system#Conclusion)