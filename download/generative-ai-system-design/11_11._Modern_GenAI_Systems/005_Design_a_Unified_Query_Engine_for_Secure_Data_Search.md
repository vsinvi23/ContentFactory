# Design_a_Unified_Query_Engine_for_Secure_Data_Search

Source: https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design a Unified Query Engine Across Data Sources

Design a unified query engine that runs a single query across emails, chats, documents, and calendars and returns ranked results or cited answers. Use connectors for ingestion, hybrid retrieval, and permission checks so only authorized, fresh information is returned within latency limits at scale.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Resource-estimation)
  - [Storage and index estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Storage-and-index-estimation)
  - [Query-serving capacity estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Query-serving-capacity-estimation)
  - [Ingestion bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Ingestion-bandwidth-estimation)
- [System design of unified query engine](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#System-design-of-unified-query-engine)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#High-level-design)
    - [Source connectivity and ingestion](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Source-connectivity-and-ingestion)
    - [Unified retrieval and permission enforcement](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Unified-retrieval-and-permission-enforcement)
    - [Answer generation with citations](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Answer-generation-with-citations)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Achieving-functional-requirements)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#A-detailed-system-design)
  - [Connector and ingestion internals](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Connector-and-ingestion-internals)
    - [Full sync path](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Full-sync-path)
    - [Incremental sync path](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Incremental-sync-path)
  - [Retrieval, permissions, and answering](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Retrieval-permissions-and-answering)
    - [Retrieval execution](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Retrieval-execution)
    - [Permission verification and answering](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Permission-verification-and-answering)
  - [Query understanding and hybrid retrieval](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Query-understanding-and-hybrid-retrieval)
  - [Enterprise index and permission layer](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Enterprise-index-and-permission-layer)
  - [Answer generation and guardrails](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Answer-generation-and-guardrails)
  - [Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Putting-everything-together)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Workflow-of-the-system)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Achieving-nonfunctional-requirements)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Conclusion)

A product manager asks, "What changed for the Phoenix launch after Tuesday's review?" The evidence lives everywhere. The decision note sits in a document, the final approval came through email, the scheduling change lives in calendar invites, and the objection thread happened in chat. The system must answer in a few hundred milliseconds, show citations, and never reveal a private message or restricted attachment.

That request defines the unified query engine. It is an enterprise retrieval system that executes one user query across heterogeneous sources while preserving source-native permissions and freshness expectations.

We can treat this lesson as retrieval infrastructure for later agentic systems. The next lesson on deep research agents will assume this backbone already exists because multi-step agents fail quickly when retrieval, governance, and citations are weak.

The design tension is straightforward. You want broad coverage, low latency, fresh data, and exact access control, but each of those goals pushes the architecture in a different direction.

We will walk through requirements, storage and serving estimates, architecture choices, connector design, permission enforcement, query execution, answer generation, and evaluation. From there, the retrieval backbone becomes concrete enough to support more advanced reasoning systems.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#System-requirements)

Before sizing anything, fix what the engine must do and how well it must do it. The rest of the lesson is checked against these requirements.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Functional-requirements)

- **Unified search:** The system should search email, chat, documents, and calendar with one query.
- **Permission enforcement:** The system should show users only what they can access in the source system.
- **Grounded answers:** The system should return ranked results or a synthesized answer with citations.
- **Safe abstention:** The system should abstain or ask a follow-up when evidence is weak.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Nonfunctional-requirements)

- **Latency:** a few hundred milliseconds at p95, with per-source deadlines.
- **Freshness:** under 1 minute for email and chat, under 5 minutes for documents and calendar. Permission revocations apply faster than new content appears.
- **Scale:** 50K users, about 1.375B items, and 150 peak queries per second.
- **Availability:** a slow or failed source returns partial, labeled results.
- **Security:** encrypted, region-aware data and audit logs of the evidence behind each answer.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Resource-estimation)

Let's estimate the storage, query-serving capacity, and ingestion bandwidth this system needs, starting with storage and the index.

### Storage and index estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Storage-and-index-estimation)

Let's start with a representative enterprise of 50,000 users. We use rough per-user counts such as 5,000 emails, 20,000 chat messages, 2,000 documents, and 500 calendar events. That gives about 250 million emails, 1 billion chat messages, 100 million documents, and 25 million calendar items, or roughly 1.375 billion searchable objects.

The byte distribution is uneven. Documents dominate storage because extracted text from slides, PDFs, and attachments is much larger than a single email or message. Email and chat dominate update frequency, which drives ingestion throughput, checkpoint churn, and shard refresh behavior.

Let's assume average searchable text sizes of 2 KB for email, 0.5 KB for chat, 50 KB for documents, and 1 KB for calendar. The index also stores metadata, ACL payloads, tokenized inverted indexes, and replicas. Index size usually lands at 1 to 5 times raw searchable text, especially when storing snippets, term positions, and optional vectors.

A good estimate separates four budgets rather than one giant number.

- **Corpus storage:** This stores normalized text, metadata, ACL references, and optional snippets for retrieval.
- **Hot shards:** This keeps active index partitions sized for low-latency querying and frequent refreshes.
- **Replicas:** This duplicates searchable state for availability and read scaling.
- **Connector state:** This stores checkpoints, webhooks, change tokens, and retry queues.

Freshness targets are set early. Email and chat often target under one minute, while documents and calendar can tolerate up to five minutes. Those assumptions directly shape centralized vs. federated indexing, shard topology, and whether highly sensitive sources store full text, snippets, or metadata only. The next step is to turn these assumptions into a compact estimation table.

Indexed size per source = items × (text + ACL metadata + embedding) × 2 for index overhead × 3 for replicas. Peak shard operations come from 150 peak user queries per second × 20 shards = 3,000 per second, split across sources.

This table turns the back-of-the-envelope assumptions into directional numbers you can defend in an interview.

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Source** | **Users** | **Items per user** | **Total items** | **Avg text** | **ACL / item** | **Embedding / item** | **Freshness SLA** | **Peak shard ops/s** | **Indexed size (×2 index, ×3 replicas)** |
| Email | 50K | 5,000 | 250M | 2 KB | 0.5 KB | 1 KB | <1 min | 900 | ~5.3 TB |
| Chat | 50K | 20,000 | 1.0B | 0.5 KB | 0.2 KB | 0.3 KB | <1 min | 1,200 | ~6.0 TB |
| Documents | 50K | 2,000 | 100M | 50 KB | 1 KB | 5 KB | <5 min | 700 | ~33.6 TB |
| Calendar | 50K | 500 | 25M | 1 KB | 0.3 KB | 0.5 KB | <5 min | 200 | ~0.3 TB |
| **Total** | 50K | – | **1.375B** | – | – | – | – | **3,000** | **~45 TB** |

The last column splits the 3,000 shard operations per second across sources. The split is an assumption based on how often each source is queried, with chat and email dominating. Federated calls to nonindexed sources add to this load and are not counted here.

### Query-serving capacity estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Query-serving-capacity-estimation)

A single user query rarely becomes a single backend lookup. It usually expands into shard fan-out, optional federated calls, reranking, permission verification, and sometimes answer synthesis.

Let's assume 150 peak user queries per second. If the central index fans each query across 20 shards, that already implies 3,000 shard-level retrieval operations per second. With four federated wrappers for nonindexed sources, the same external query may produce several more source API calls. Query amplification is normal here.

The serving path includes several independent capacity pools.

- **Query mediator:** This parses the request, expands filters, routes to central and federated backends, and enforces deadlines.
- **Search nodes:** These execute lexical or hybrid retrieval and return candidate sets from indexed sources.
- **Permission service:** This resolves user groups and verifies top results against current ACL state.
- **Reranker and answer layer:** These consume candidate sets, rerank, and optionally synthesize a citation-backed response.

Late ACL verification inflates backend work because top KKK candidates may require exact checks before the final top NNN can be returned. Federated systems are also dominated by the slowest source, so p99 matters more than p50.

> **Note:** Retrieval is decoupled from answer generation so ranked results can still return when the model tier is degraded.

Stateless mediators usually autoscale horizontally, while ingestion workers and search clusters scale separately. With capacity framed, the request path becomes easier to visualize.

The diagram below shows the indexed and federated paths side by side.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27893.52%27%20height=%27360.71999999999997%27/%3e)![Unified query architecture](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Unified query architecture")

Unified query architecture

### Ingestion bandwidth estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Ingestion-bandwidth-estimation)

Bandwidth here is mostly an ingestion problem, not a user query problem. Connectors continuously pull or receive updates from email, chat, documents, and calendar systems. Query traffic is smaller in bytes, though burstier in latency sensitivity.

Polling-based ingestion creates periodic spikes and wasted calls when nothing changed. Webhooks or event streams reduce needless traffic for high-churn sources like chat and email, but they shift complexity into replay, ordering, and backpressure handling. A watermark keeps the pipeline efficient.

Internal bandwidth often exceeds user-facing egress. Attachment extraction, OCR, virus scanning, and parser fan-out can multiply bytes as binaries turn into text and metadata. Cross-region replication adds another layer, especially under residency constraints.

Connectors use compression, batching, and queue-based backpressure. Also budget for query-time federation spikes, where remote SaaS APIs may be rate-limited or return variable payload sizes.

## System design of unified query engine[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#System-design-of-unified-query-engine)

Let's start with the high-level design.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#High-level-design)

A simple way to think about the system is that it has three jobs. First, it connects to source systems and keeps searchable views fresh. Second, it retrieves across those views while enforcing access control. Third, it synthesizes an answer only from verified evidence.

The architecture is easiest to discuss in three subsystems.

#### Source connectivity and ingestion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Source-connectivity-and-ingestion)

Connectors authenticate with least privilege, fetch full and incremental changes, normalize source-specific records, and push them into downstream parsing and indexing stages.

#### Unified retrieval and permission enforcement[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Unified-retrieval-and-permission-enforcement)

The query path accepts a user request, resolves identity context, retrieves candidates from centralized indexes and federated sources, merges them, reranks them, and then runs exact permission checks before returning evidence.

#### Answer generation with citations[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Answer-generation-with-citations)

The answer layer receives only permission-verified results. It packs snippets into context, attaches citations, and abstains when evidence is weak or inconsistent.

Across all subsystems, a canonical schema keeps ranking and filtering coherent. Typical fields include `source_app`, `item_type`, `author` or sender, participants, title or subject, timestamp, folder or channel, visibility, content snippet, and ACL references.

The major architectural decision is whether each source is centralized, federated, or hybrid. In practice, hybrid is the default. Stable or high-value sources are indexed centrally, while dynamic or highly sensitive sources may stay live behind federated wrappers. The next section shows how those choices satisfy concrete requirements.

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Achieving-functional-requirements)

Let's map each requirement to a mechanism in the request life cycle. Supported sources enter through dedicated connectors, each of which extracts text, metadata, and source ACLs, then maps them into the canonical schema. Source diversity is handled at ingestion time so query serving remains uniform.

Freshness is met by combining full syncs with incremental syncs. Connectors rely on watermarks, change logs, webhooks, or event streams depending on what each source exposes. Email and chat usually take the fastest path. Documents and calendar can often tolerate slightly slower propagation.

Latency is managed by centralized indexing for the common path, asynchronous fan-out for federated calls, and strict source-specific deadlines. The mediator does not wait forever for a slow backend.

Cross-source relevance is achieved through metadata normalization, content deduplication, and source-aware ranking features.

- **Freshness:** Recent chat and email often receive a boost for operational queries.
- **Authority:** Official documents or organizer-authored meeting notes often outrank side discussions.
- **Behavior:** Historical clicks or saves can refine ranking over time.

Answer generation takes the final verified set and produces a concise response with citations back to source items. Evaluation then measures retrieval quality, permission correctness, freshness compliance, and faithfulness of the generated answer. That functional map sets up the deeper internal design.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#A-detailed-system-design)

Now, let's move one layer deeper and follow the data through the system. The mechanics matter more than the labels.

### Connector and ingestion internals[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Connector-and-ingestion-internals)

Each connector holds credentials with least privilege, tracks checkpoints, and emits idempotent change records so retries do not duplicate indexed items.

#### Full sync path[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Full-sync-path)

The connector enumerates the source corpus, extracts text and metadata, captures ACL information, computes content fingerprints, and sends normalized records into indexing.

#### Incremental sync path[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Incremental-sync-path)

The connector resumes from a watermark, consumes source change logs or webhook events, and updates only changed, deleted, or permission-revoked items.

Deletion and revocation handling must be explicit. A removed permission should invalidate searchable access faster than a newly created item appears. We can think of ACL revocation like pulling a book from a library shelf before reprinting the catalog entry.

### Retrieval, permissions, and answering[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Retrieval-permissions-and-answering)

The query frontend performs understanding, source routing, retrieval, reranking, permission verification, and optional answer synthesis.

#### Retrieval execution[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Retrieval-execution)

The mediator parses the query, applies metadata filters, retrieves central candidates, sends parallel requests to federated wrappers, then merges and deduplicates the result pool.

#### Permission verification and answering[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Permission-verification-and-answering)

The system first uses indexed ACL hints for fast prefiltering. It then performs exact late binding on top results. After verification, the answer layer packs context, adds citations, and abstains if evidence is weak.

> **Attention:** Stale ACLs are a correctness bug, not a ranking bug.

Failure modes include stale permissions, duplicate content, slow SaaS APIs, and partial source outages. Graceful degradation means returning partial results with visible source labels, while continuing background retries and telemetry collection. That retrieval frontend becomes even more effective when query understanding is designed explicitly.

The diagram below shows the ingestion path, where freshness problems usually appear before they reach query time.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27906.83%27%20height=%27498.73%27/%3e)![The ingestion path for a query engine](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The ingestion path for a query engine")

The ingestion path for a query engine

### Query understanding and hybrid retrieval[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Query-understanding-and-hybrid-retrieval)

At the front of retrieval, the system first asks a simple question. What kind of search is this, and which retrieval method should answer it?

Query parsing extracts entities, dates, participants, and source hints. Intent detection may distinguish "find the document" from "summarize what changed after the meeting." The parser also applies metadata filters such as source, author, channel, or date range.

When wording differs across sources, embeddings can help. An embedding lets the engine connect a meeting summary document with a chat discussion that used different language. Lexical retrieval still matters for exact names, codes, and quoted phrases.

Most enterprises use hybrid retrieval. Lexical search acts like a precise filing cabinet, while vector retrieval acts more like a librarian who recognizes topics despite different wording.

### Enterprise index and permission layer[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Enterprise-index-and-permission-layer)

The persistent enterprise knowledge layer is not the source of truth. It is a derived retrieval substrate that must stay synchronized with source systems and identity state.

Its main stores usually include the central search index, the user and group directory, ACL expansion caches, audit logs, freshness dashboards, and optional click or feedback signals for ranking improvements. The source systems remain authoritative for raw content and final permissions.

Some state needs stricter latency than the index itself. Group membership changes and permission revocations often belong in a separate low-latency permission service rather than living only inside copied metadata. That separation keeps serving fast without letting stale ACL snapshots leak content.

Retention and compliance policies also sit here. Snippets, cached attachments, and replicated text may require encryption, regional pinning, or stricter deletion workflows than ordinary ranking metadata. Once this index and permission layer is in place, the answer synthesis layer can consume verified evidence safely.

### Answer generation and guardrails[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Answer-generation-and-guardrails)

The language model sits after retrieval, not in front of it. It receives only evidence that has already passed permission verification and source selection.

Prompt construction tags each snippet with source, title, timestamp, and a stable citation handle. The model then synthesizes an answer grounded in those snippets and returns citations to emails, calendar events, documents, or chat messages. If evidence is weak, conflicting, or too sparse, the system abstains or asks a clarifying follow-up rather than improvising.

Guardrails operate on both inputs and outputs.

- **Redaction:** Sensitive previews can be shortened or masked before being shown to the model.
- **Grounding rules:** The model is required to cite supporting evidence for factual claims.
- **Audit logging:** The system records which evidence was exposed to the model and which citations were returned.

> **Practical tip:** Storing evidence IDs alongside prompts lets later audits reconstruct exactly what the model saw.

This pattern directly supports future deep research agents, which will reason longer but still depend on the same retrieval and citation substrate.

### Putting everything together[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Putting-everything-together)

Let's put the whole request path together in interview order. The user sends a query through the API gateway, authentication resolves identity, and the query mediator fetches user and group context from the directory and permission layer. It then decides which sources should use the central index and which should remain federated.

Candidate retrieval happens in parallel. Central shards return prefiltered results, federated wrappers query remote systems under deadlines, and the mediator merges both streams. A fingerprinting step removes duplicates, then reranking applies relevance, freshness, authority, and item-type features.

Top candidates undergo exact permission verification before answer generation sees them. The answer layer either returns ranked results directly or synthesizes a concise citation-backed response. Audit logs capture query metadata, source timing, permission-check outcomes, and evidence IDs.

The following illustration brings the connectors, the central index and federated wrappers, the permission layer, and the answer layer together into one detailed design.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27895.23%27%20height=%27662.13%27/%3e)![Detailed design of a unified query engine across data sources](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of a unified query engine across data sources")

Detailed design of a unified query engine across data sources

Instrumentation points should track ingestion lag, source timeouts, ACL mismatches, and answer quality metrics. With the request assembled end to end, the runtime workflow becomes easy to narrate.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Workflow-of-the-system)

In an interview, it helps to present the runtime flow as a numbered sequence so the control path stays clear.

1. **Authenticate user:** The gateway validates the session and fetches group memberships.
2. **Parse query:** The mediator detects filters, entities, and likely source targets.
3. **Retrieve centrally:** Indexed sources return candidates using metadata prefilters.
4. **Federate in parallel:** Live wrappers query remote systems with strict deadlines.
5. **Merge and deduplicate:** Results are normalized into one candidate pool.
6. **Rerank candidates:** Relevance, freshness, authority, and type-aware signals reorder the pool.
7. **Verify permissions:** Top results undergo authoritative late-binding checks.
8. **Generate answer:** The system returns citations or falls back to ranked results if answer synthesis is disabled.
9. **Log metadata:** Audit and observability systems record timings, sources, and permission outcomes.

Failures split into two policies. Missing data degrades the answer: if a source is slow or down, or the model tier is degraded, the system returns partial, clearly labeled results or ranked results without synthesis. Missing verification blocks the answer: if identity, group membership, or exact permission checks can’t run, the system returns no results for that query.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Achieving-nonfunctional-requirements)

Nonfunctional requirements are where the architecture choice becomes visible. Performance comes from centralized indexing on the common path, shard sizing for hot sources, source-specific timeouts, and caching of identity expansions. Query mediators stay stateless so they can scale horizontally, while ingestion workers and search clusters scale independently based on source churn and corpus growth.

Availability requires retries, circuit breakers, and partial-result behavior when a federated source is slow or unavailable. Availability never overrides access control. A permission outage causes a visible error and a retry, not unverified results. The permission service runs across zones, group expansions stay in a short-TTL cache, and that TTL stays shorter than the revocation target.

|  |  |  |
| --- | --- | --- |
| **Component** | **On failure** | **Behavior** |
| Slow or down federated source | Degrade | Partial results with source labels, background retry |
| Central shard timeout | Degrade | Results from remaining shards, flagged as partial |
| Reranker | Degrade | Fall back to first-stage ranking |
| Model tier (answer generation) | Degrade | Ranked, verified results with citations, no synthesis |
| Permission service or identity and group lookup | Fail closed | Return no results and an error, retry |
| Exact late-binding ACL check on a candidate | Fail closed | Drop that candidate, never show it unverified |
| Audit logging | Buffer and retry | If it can’t buffer, skip answer synthesis |

Reliability comes from idempotent ingestion, replayable event streams, checkpoint recovery, and deletion propagation that survives worker restarts.

Security work is distributed through the system rather than isolated in one layer.

- **Connector security:** Credentials use least privilege and rotate cleanly.
- **Data protection:** Copied snippets and indexes are encrypted and region-aware.
- **Auditability:** Query logs and evidence trails support forensic review.
- **Permission correctness:** Prefiltering accelerates retrieval, while late binding preserves exact access control.

> **Note:** Federated search buys freshness and source-native ACLs, but latency is bounded by the worst backend.

Centralized indexing buys lower latency and better ranking, but it inherits larger freshness and security burdens. Hybrid is the practical compromise for most enterprises. That trade-off framing is exactly what interviewers usually want to hear before they ask for failure modes and metrics.

The assessment below tests whether you can choose between centralized, federated, and hybrid retrieval under latency, freshness, and permission constraints.

Knowledge Check

Q1. An enterprise wants to search email, chat, documents, and calendar. Chat and email need sub-minute freshness. A legal archive is highly sensitive and must keep its own source-native permissions. Which architecture fits best?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Conclusion)

A unified query engine is a retrieval, permissions, and systems integration problem before it becomes an LLM problem. Strong designs estimate scale first, choose a hybrid architecture deliberately, keep connectors incremental, enforce prefilter plus late-binding ACL checks, and generate answers only from verified evidence.

That foundation is what makes trustworthy enterprise QA possible. In the next lesson, we will build on this substrate to design a deep research agent that can plan multistep investigations without crossing permission boundaries or inventing unsupported findings.

Design an LLM-Powered Search Engine

Design a Real-Time Voice Assistant

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Resource-estimation)

[Storage and index estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Storage-and-index-estimation)

[Query-serving capacity estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Query-serving-capacity-estimation)

[Ingestion bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Ingestion-bandwidth-estimation)

[System design of unified query engine](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#System-design-of-unified-query-engine)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#High-level-design)

[Source connectivity and ingestion](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Source-connectivity-and-ingestion)

[Unified retrieval and permission enforcement](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Unified-retrieval-and-permission-enforcement)

[Answer generation with citations](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Answer-generation-with-citations)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Achieving-functional-requirements)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#A-detailed-system-design)

[Connector and ingestion internals](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Connector-and-ingestion-internals)

[Full sync path](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Full-sync-path)

[Incremental sync path](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Incremental-sync-path)

[Retrieval, permissions, and answering](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Retrieval-permissions-and-answering)

[Retrieval execution](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Retrieval-execution)

[Permission verification and answering](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Permission-verification-and-answering)

[Query understanding and hybrid retrieval](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Query-understanding-and-hybrid-retrieval)

[Enterprise index and permission layer](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Enterprise-index-and-permission-layer)

[Answer generation and guardrails](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Answer-generation-and-guardrails)

[Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Putting-everything-together)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Workflow-of-the-system)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Achieving-nonfunctional-requirements)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-unified-query-engine-across-data-sources#Conclusion)