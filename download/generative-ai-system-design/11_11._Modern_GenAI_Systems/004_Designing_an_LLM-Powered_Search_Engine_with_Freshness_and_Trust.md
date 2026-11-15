# Designing_an_LLM-Powered_Search_Engine_with_Freshness_and_Trust

Source: https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design an LLM-Powered Search Engine

Design an LLM-powered search engine that rewrites queries, retrieves and ranks web evidence, and generates grounded answers with citations. Balance live search with cached content to keep responses fresh, fast, reliable, and cost-efficient at high query volumes.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Resource-estimation)
- [System design of an LLM-powered search engine](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#System-design-of-an-LLM-powered-search-engine)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#High-level-design)
  - [Choosing the retrieval path](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Choosing-the-retrieval-path)
    - [Common failure modes](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Common-failure-modes)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Achieving-functional-requirements)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#A-detailed-system-design)
  - [Query rewriting and retrieval flow](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Query-rewriting-and-retrieval-flow)
    - [Rewriting the query](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Rewriting-the-query)
    - [Retrieving and filtering evidence](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Retrieving-and-filtering-evidence)
  - [Grounded answers with citations](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Grounded-answers-with-citations)
    - [Verifying support after generation](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Verifying-support-after-generation)
  - [Caching and quality evaluation](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Caching-and-quality-evaluation)
    - [Measuring whether the system is working](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Measuring-whether-the-system-is-working)
  - [Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Putting-everything-together)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Workflow-of-the-system)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Achieving-nonfunctional-requirements)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Conclusion)

A user asks, "What changed in the new EU AI policy this morning?" and now the system has four seconds to search the web, read enough evidence, write a useful answer, and show citations that support each claim. That request sounds like chat, but the engineering problem looks more like search under tight freshness, latency, and trust constraints.

This lesson designs an LLM-powered search engine that answers open-web questions with grounded, cited responses. The request enters a pipeline that understands the query, rewrites it when needed, retrieves candidate pages, ranks trustworthy evidence, synthesizes an answer, and evaluates whether the answer remained supported by sources.

From a system design angle, the requirements are clear. The answer must be fresh for fast-moving topics, fast enough for interactive use, cheap enough to serve at scale, and trustworthy enough that users can inspect the evidence path. We keep the scope to web retrieval only, not enterprise documents or multisource federation. That narrower scope lets us build a strong single-source architecture first, which sets up the next lesson on unified retrieval across many backends.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#System-requirements)

Let's turn these goals into concrete functional and nonfunctional requirements.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Functional-requirements)

- **Query understanding**: The system should resolve conversational references and rewrite or decompose questions into retrieval-friendly subqueries.
- **Fresh retrieval**: The system should retrieve open-web evidence, using live search for time-sensitive queries and cached or indexed content for evergreen ones.
- **Evidence ranking**: The system should deduplicate candidates and rank them by relevance, recency, and source trust.
- **Grounded answers**: The system should answer from the selected evidence with sentence-level citations.
- **Verification**: The system should verify each claim against its cited passage and downgrade or remove unsupported claims.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Nonfunctional-requirements)

- **Latency**: The p95 answer should complete within about 4 seconds, with streaming.
- **Freshness**: Answers to time-sensitive questions should reflect current sources.
- **Cost**: Fan-out, page fetches, and model calls should stay within a per-query budget at 100K queries per day.
- **Trust**: Users should be able to inspect the evidence behind every factual claim.
- **Reliability**: Provider or fetch failures should degrade to partial, cached, or indexed evidence rather than failing the request.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Resource-estimation)

Let's start with a back-of-the-envelope estimate before choosing components. For an answer engine, fan-out matters more than raw user QPS because one user query often expands into several retrieval operations.

Let's assume 100K user queries per day. If the rewriter produces three subqueries on average, the system executes 300K searches per day. If each search returns 10 candidate pages and the fetcher reads snippets or trimmed content from all of them, the system touches roughly 3M page candidates daily. If each fetched page contributes 1K useful tokens after trimming, retrieval processing reaches about 3B tokens per day before the reader model writes a response.

Latency and cost split across stages. Search API calls add network delay and per-call charges. Page fetches add tail latency and parsing cost. Answer synthesis adds reader-model inference cost, but retrieval often dominates spend because fan-out multiplies every upstream request.

A practical budget model often treats indexing infrastructure and observability as semi-fixed costs, while search calls, page fetches, reranking, and generation are variable costs. Lowering top K, using cheaper rewriters, aggressive caching, or adding a hybrid internal index all change the spend curve. The table below turns these assumptions into concrete design pressure.

The table below summarizes these assumptions and their design implications.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Metric** | **Assumption** | **Daily Volume** | **Monthly Volume** | **Design Implication** |
| **User queries** | 100K queries/day | 100K | 3.0M | Baseline demand for the system |
| **Rewritten sub-queries** | 3 per user query | 300K | 9.0M | Fan-out improves recall but triples search-side workload |
| **Pages fetched** | 10 pages per sub-query | 3.0M | 90.0M | Network, parsing, and storage load scale quickly with fan-out |
| **Tokens per page after trimming** | 1K tokens/page | 3.0B tokens | 90.0B tokens | Token processing becomes a major cost and latency driver |
| **Reranking load** | 30 candidates per user query | 3.0M candidates | 90.0M candidates | Reranking quality helps precision but adds model inference overhead |
| **Answer tokens** | 500 tokens per final answer | 50.0M tokens | 1.5B tokens | Generation cost is material but usually smaller than retrieval processing |
| **Approximate monthly cost bands** | Depends on search, fetch, rerank, and LLM rates | — | Medium to very high | Cost rises nonlinearly as fan-out multiplies API usage, page volume, and token load |

The 4-second budget is spread across the serial stages of the request path. Subqueries and page fetches run in parallel, so each of those stages costs its slowest call, not their sum.

Latency Budget Estimator

Adjust each stage's p95 latency to see whether the answer engine fits its 4-second budget.

Latency BudgetB

s

Query RewriteLrw​

s

Search Calls (slowest subquery)Ls​

s

Page Fetch (slowest page)Lf​

s

Rerank and DedupeLrr​

s

Time to First TokenLft​

s

Full GenerationLg​

s

Verification Tail (last sentence)Lv​

s

Retrieval Complete AtTret​

2s

First Token Visible AtTft​

2.4s

Total LatencyT

3.9s

Remaining BudgetR

0.1s

Retrieval finishes at **2 s**, the first token appears at **2.4 s**, and the full answer completes in **3.9 s**. That leaves **0.1 s** of the **4 s** budget.

Do you find this helpful?

The user sees the first token at about 2.4 seconds, since retrieval must finish before generation starts. This is why retrieval, not the model, usually decides whether the budget holds.

That estimate gives us a budget envelope, so the next step is choosing the retrieval architecture that can meet it.

## System design of an LLM-powered search engine[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#System-design-of-an-LLM-powered-search-engine)

Let's start with the high-level design.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#High-level-design)

The request enters an API gateway, which authenticates, rate-limits, and forwards it to query understanding. From there, the retrieval fabric issues live searches, looks up any internal web index, fetches page content, and sends candidates to ranking and trust filters. The top evidence set reaches the answer synthesizer, and the output then passes through citation verification and monitoring.

Three architecture options usually appear in interviews. A live search API gives strong freshness and low operational burden, but it creates dependency risk, provider throttling exposure, and variable latency, and ranking is controlled by the provider. An in-house crawler plus index gives control over ranking, deduplication, and cost at scale, but freshness lags and operations become much heavier. A hybrid system uses internal indexed snapshots for broad, cheap recall and selectively performs live fetches when recency matters.

### Choosing the retrieval path[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Choosing-the-retrieval-path)

A simple rule works well. Evergreen queries can often hit cache or internal index first, while time-sensitive queries force live retrieval. The classifier looks for intents such as breaking news, prices, release notes, regulations, or scores, then adjusts TTLs and retrieval policy.

#### Common failure modes[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Common-failure-modes)

Failures are rarely total. A provider may throttle only some subqueries, a crawler may lag one domain, robots rules may block fetching, or page parsing may fail on dynamic content. The system should keep partial evidence, downgrade confidence, and still return a bounded response rather than timing out completely.

> **Note:** Freshness policy is partly product policy. A sports answer may expire in minutes, while historical facts can remain cached for days.

The diagram below shows the critical path from request to cited answer.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271261%27%20height=%27541%27/%3e)![Critical retrieval path](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Critical retrieval path")

Critical retrieval path

Freshness policy determines when the system retrieves live content, so it is worth examining closely.

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Achieving-functional-requirements)

Each functional requirement maps to a component in this architecture.

- **Query understanding**: The query-understanding service resolves references, rewrites the query, and caps decomposition.
- **Fresh retrieval**: The freshness classifier routes time-sensitive queries to live search and evergreen ones to caches or the internal index.
- **Evidence ranking**: Hybrid lexical and embedding scoring, deduplication, and trust-aware reranking select a compact evidence set.
- **Grounded answers**: The reader model answers only from that evidence and attaches sentence-level citations.
- **Verification**: The verifier checks each streamed sentence against its cited passage.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#A-detailed-system-design)

With the architecture set, we can now inspect how the system rewrites queries and controls retrieval fan-out.

### Query rewriting and retrieval flow[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Query-rewriting-and-retrieval-flow)

Users rarely ask retrieval-friendly questions. They ask follow-ups like "what about the new one?" or bundle several hops into one prompt. The system first normalizes that request into something search can execute.

#### Rewriting the query[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Rewriting-the-query)

The request goes to a lightweight query-understanding service that resolves conversational references, expands synonyms, and decides whether decomposition is needed. For example, "How did Nvidia react after the export rule changed?" may be rewritten into a standalone question, plus a few narrower searches around the policy update, stock reaction, and the official company statement.

- **When to use LLM rewriting:** An LLM rewriter is useful for pronoun resolution, decomposition, and semantic expansion, but it adds a serial model call before retrieval starts. For high-volume traffic, many teams reserve LLM rewriting for ambiguous or conversational prompts and use cheaper rule-based templates for keyword queries.
- **Capping fan-out:** Every additional subquery increases recall and also multiplies latency, page fetches, and reranking work. Good systems cap fan-out using heuristics such as user tier, query class, or confidence from first-pass results.

#### Retrieving and filtering evidence[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Retrieving-and-filtering-evidence)

Where the system controls retrieval, it should combine lexical matching and semantic recall. This applies to the internal index in a hybrid design and to the passages the system fetches. Exact terms like policy IDs or error codes are caught by BM25, while embeddings cover paraphrases. A live search API is different. The provider decides first-stage ranking, so the system can only shape results through query wording, filters, and subquery choice, then rerank what comes back.

After fetching, the system chunks pages into passages and scores them with both lexical and embedding signals. This is where hybrid ranking applies to live-search results.

The system fetches snippets first when possible, then promotes only promising URLs to full-page fetch. It deduplicates mirrored pages, syndicated articles, and repeated snippets using canonical URL signals plus content similarity. Ranking then mixes relevance, recency, domain authority, author signals, and cross-source consistency. We can think of it like investigative reporting. The goal is not to interview everyone, but to gather the smallest set of witnesses that supports the story.

> **Attention:** Query rewriting can drift from the original intent. Guardrails should preserve named entities, dates, and required constraints from the user prompt.

Once the evidence set is small and trustworthy, the system can generate an answer that stays tied to those passages.

### Grounded answers with citations[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Grounded-answers-with-citations)

Generation starts only after retrieval has produced a compact evidence set. The reader model receives selected passages, source metadata, and instructions to answer strictly from provided evidence. That phrase matters. This stage should behave more like open-book summarization than open-ended generation.

The answer should attach citations at the claim or sentence level, not only as a source list at the end. A user should be able to inspect a statement, click its marker, and land on a passage that supports it. Too few citations weaken trust. Too many make the answer unreadable. In practice, the system aims for dense support on factual claims and lighter citation on connective prose.

#### Verifying support after generation[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Verifying-support-after-generation)

Verification cannot wait for the full answer if the answer streams. Instead, the system verifies each sentence as it completes, in parallel with generation. Each sentence streams with its citation marked as pending. The verifier checks the claim against the cited passage and confirms the marker, usually within a few hundred milliseconds. If a claim is weakly supported or unsupported, the interface downgrades it with hedged wording, replaces it with a source snippet, or removes it.

Practical ranking rarely uses semantic similarity alone. The final evidence selector usually combines authority, recency, relevance, and corroboration across independent sources. Domain reputation helps, but it is not enough when duplicate content or scraped summaries flood the web.

> **Practical tip:** It helps to verify each sentence after it is generated, not just before. The model can turn a supported passage into an unsupported claim while summarizing.

The diagram below shows how each claim is checked against its cited passage.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27889.96%27%20height=%27411.16%27/%3e)![Hybrid answer engine flow](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Hybrid answer engine flow")

Hybrid answer engine flow

Source quality can fail in subtle ways, so trust signals need careful treatment.

After generation and verification work, production readiness depends on whether the service can stay fast, measurable, and affordable over time.

### Caching and quality evaluation[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Caching-and-quality-evaluation)

Caching works at several layers, and each layer has its own TTL. Query rewrites can be cached for repeated prompts. Search results can be cached briefly to avoid repeated provider calls. Page snapshots can be cached with URL-based invalidation or scheduled refresh. Final answers can be cached for evergreen topics, but they are risky for volatile domains because users may receive a polished but stale answer.

#### Measuring whether the system is working[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Measuring-whether-the-system-is-working)

The system should log end-to-end latency, retrieval success rate, freshness lag of cited sources, citation accuracy, groundedness, answer helpfulness, and dollars per 1,000 queries. Offline evaluation sets test replayed queries against judged evidence and expected answers. Online experiments compare fan-out depth, reranker variants, or freshness policies under real traffic.

Reliability features belong here too. External search calls need retries with budget caps, circuit breakers when providers degrade, and graceful fallback to cached or indexed results when live search is unavailable. Observability should trace a request across rewrite, retrieval, rerank, generation, and verification so operators can quickly locate the expensive or unstable stage.

> **Note:** The safest cache for time-sensitive queries is usually the page snapshot or search-result cache with a short TTL, not the final generated answer cache.

With these controls in place, the full request path can be summarized.

### Putting everything together[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Putting-everything-together)

A production answer engine receives a user query, rewrites it into one or more retrieval-friendly forms, and sends those requests through a hybrid retrieval layer that combines search APIs, optional indexed snapshots, and selective live page fetches. The system deduplicates candidates, reranks them using relevance plus trust signals, synthesizes an answer from a compact evidence set, inserts inline citations, and verifies each sentence as it streams.

The following illustration brings the query understanding, hybrid retrieval, ranking, generation, verification, and caching layers together into one detailed design.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27907.74%27%20height=%27427.14000000000004%27/%3e)![Detailed design of an LLM-powered search engine](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of an LLM-powered search engine")

Detailed design of an LLM-powered search engine

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Workflow-of-the-system)

Let's follow one query through the system.

The API gateway authenticates the request, applies rate limits, and forwards it to query understanding. A lightweight service resolves conversational references and decides whether to decompose the question, and a freshness classifier marks it as evergreen or time sensitive.

Evergreen queries check the caches and the internal index first, while time-sensitive queries go to live search. Subqueries run in parallel under a fan-out cap, and the fetcher pulls snippets first, promoting only promising URLs to full-page fetch.

Fetched pages are chunked, scored with lexical and embedding signals, deduplicated, and reranked by relevance, recency, authority, and corroboration. The top passages form a compact evidence set for the reader model.

The reader model answers strictly from that evidence and streams sentences with pending citation markers, while the verifier checks each sentence against its cited passage and confirms, hedges, or removes it. If a provider slows down or fails, circuit breakers shift retrieval to cached or indexed results, and the answer reports reduced confidence instead of timing out.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Achieving-nonfunctional-requirements)

That workflow addresses the four headline requirements directly. Freshness comes from policy-driven live retrieval, citations come from passage-level grounding, latency comes from capped fan-out and parallel fetches, and cost comes from trimming context, caching aggressively, and limiting expensive model calls. When external dependencies fail, the system degrades toward cached or indexed evidence instead of failing hard.

The next step is to test whether you can make those trade-offs under a concrete latency budget.

Knowledge Check

Q1. Your answer engine has a 4-second p95 budget. Stage latencies are rewrite 0.3s, search 0.5s, page fetch 1.4s, rerank 0.4s, generation 1.6s, and verification tail 0.3s, which totals 4.5s. Which change best fits the budget without hurting trust?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Conclusion)

An LLM-powered search engine is not just an LLM with web access. It is a retrieval system that must control freshness, grounding, trust, latency, and cost on every request.

For interviews, it helps to keep the sequence clear: estimate first, rewrite carefully, retrieve with freshness awareness, rank and deduplicate aggressively, generate with inline citations, verify support, and cache selectively. Strong answers also surface failure modes such as provider throttling, stale indexes, duplicate sources, and unsupported claims.

Design an AI Code Assistant

Design a Unified Query Engine Across Data Sources

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Resource-estimation)

[System design of an LLM-powered search engine](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#System-design-of-an-LLM-powered-search-engine)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#High-level-design)

[Choosing the retrieval path](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Choosing-the-retrieval-path)

[Common failure modes](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Common-failure-modes)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Achieving-functional-requirements)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#A-detailed-system-design)

[Query rewriting and retrieval flow](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Query-rewriting-and-retrieval-flow)

[Rewriting the query](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Rewriting-the-query)

[Retrieving and filtering evidence](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Retrieving-and-filtering-evidence)

[Grounded answers with citations](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Grounded-answers-with-citations)

[Verifying support after generation](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Verifying-support-after-generation)

[Caching and quality evaluation](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Caching-and-quality-evaluation)

[Measuring whether the system is working](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Measuring-whether-the-system-is-working)

[Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Putting-everything-together)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Workflow-of-the-system)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Achieving-nonfunctional-requirements)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-an-llm-powered-search-engine#Conclusion)