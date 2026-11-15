# Design_Cost_Efficiency_for_Generative_AI_at_One_Million_Queries_Daily

Source: https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design for Cost at 1M Queries a Day

Design a GenAI serving system that answers 1 million queries a day for under $0.02 each without sacrificing latency or quality. It routes traffic through exact and semantic caches and a cheap-versus-frontier model cascade, caps retrieval and output tokens, and keeps spend in check with per-route monitoring and degradation policies.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Nonfunctional-requirements)
- [Baseline cost estimate](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Baseline-cost-estimate)
- [Cost levers in the architecture](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Cost-levers-in-the-architecture)
  - [Priority order for interviews](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Priority-order-for-interviews)
    - [Route first](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Route-first)
    - [Reuse second](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Reuse-second)
    - [Trim third and cap fourth](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Trim-third-and-cap-fourth)
- [Applying caching and model tiering](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Applying-caching-and-model-tiering)
- [Retrieval budgets and request limits](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Retrieval-budgets-and-request-limits)
  - [Retrieval-side controls](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Retrieval-side-controls)
  - [Generation-side controls](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Generation-side-controls)
- [Operating the system within budget](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Operating-the-system-within-budget)
- [Interview answer blueprint](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Interview-answer-blueprint)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Conclusion)

One million GenAI queries per day turn small inefficiencies into budget incidents. Adding 200 extra prompt tokens, letting output length drift, or routing every question to the strongest model moves the monthly bill before anyone notices any quality gain. In this setting, cost is not a finance afterthought. It is a design constraint that sits next to latency and answer quality.

This lesson treats the interview problem as a production design exercise for a conversational RAG assistant under a hard unit-cost ceiling. We assume three concrete targets: cost at or below $0.02 per query, P95 time to first token (TTFT) at or below 500 ms, with streaming, and retrieval and answer quality that stay within an acceptable range, such as recall@5 near 0.90 and no visible answer collapse on hard questions.

Interviewers ask this because strong candidates must reason quantitatively across pricing, tokens, traffic mix, caching, and serving architecture. Drawing boxes is not enough. You need to show how the request path changes cost.

> **Note:** The strongest answer usually starts with a naive estimate, then reduces blended cost through routing and reuse instead of hand-waving about "optimizing prompts."

We will build the expensive baseline first, identify the dominant multipliers, then redesign the path with caching, model tiering, retrieval budgets, output limits, and batch processing. That structure also sets up the next lesson on delivering this clearly in a 45-minute interview.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#System-requirements)

Let's pin down what the assistant must do and the budgets it must meet before estimating cost.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Functional-requirements)

- **Conversational answers**: The system should answer questions with retrieval-augmented generation and stream responses.
- **Reuse**: The system should serve repeated and near-duplicate questions from exact and semantic caches.
- **Model routing**: The system should route each cache miss to a cheap or frontier model based on predicted difficulty, with escalation on low confidence.
- **Request budgets**: The system should cap retrieval depth, output length, agent steps, and per-user usage.
- **Offline processing**: The system should run re-embedding, summarization, and evaluation as batch jobs outside the serving path.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Nonfunctional-requirements)

- **Cost**: The system should stay at or below $0.02 per query, about $20,000 per day at 1 million queries.
- **Latency**: P95 time to first token should stay at or below 500 ms with streaming.
- **Quality**: Retrieval recall@5 should stay near 0.90, with no visible answer collapse on hard questions.
- **Availability**: Cache or vector-store failures should degrade gracefully instead of failing requests.
- **Observability**: Cost, tokens, and quality should be measurable per route.

## Baseline cost estimate[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Baseline-cost-estimate)

Let's start with the simplest possible online path. Every request performs full retrieval, every prompt carries the same large system instruction block, the prompt builder injects many context chunks, there is no cache, and every query goes to a frontier model. This is the design many candidates implicitly describe unless they force themselves to quantify it.

Let's use a back-of-the-envelope token budget. Suppose that the system prompt is 500 tokens, the user query is 50 tokens, retrieval returns 10 chunks at 300 tokens each, and the model produces 250 output tokens. Input tokens become 500+50+3000=3550500 + 50 + 3000 = 3550500+50+3000=3550. Output tokens are 250.

Now, let's attach representative pricing. Suppose that a frontier model costs $5 per million input tokens and $15 per million output tokens. Then the per-request generation cost is

C=3550106×5+250106×15=0.01775+0.00375=0.0215C = \frac{3550}{10^6} \times 5 + \frac{250}{10^6} \times 15 = 0.01775 + 0.00375 = 0.0215C=1063550​×5+106250​×15=0.01775+0.00375=0.0215

At 1,000,000 queries per day, daily generation spend is about $21,500. That already misses the $20,000 target, and this estimate still ignores embeddings, reranking, moderation, vector lookups, retries, and observability pipelines.

The baseline calculation exposes the real multipliers.

- **Model tier:** More expensive models magnify every token.
- **Input token volume:** Large prompts and wide retrieval quickly dominate spend.
- **Output token volume:** Verbose answers raise both cost and latency.
- **Traffic volume:** Small per-query overruns compound at scale.

> **Attention:** Clean spreadsheets undercount real systems. Retries, timeout fallbacks, and retrieval fan-out usually push actual spend above the nominal estimate.

The point of the baseline is not precision. The point is to identify where the architecture must change next.

First, let's see where the money goes in the naive flow.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271241%27%20height=%27422%27/%3e)![Naive costly request path](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Naive costly request path")

Naive costly request path

## Cost levers in the architecture[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Cost-levers-in-the-architecture)

Cost control works best when treated as request-path design, not as a set of isolated tricks. The system should decide early whether a request deserves expensive reasoning, whether an earlier answer can be reused, and how much evidence and generation budget the request is allowed to consume.

A simple way to think about it is that every request spends from three wallets. One wallet pays for the model, one pays for tokens, and one pays for repeated work. The optimized design shrinks all three.

The main levers fit into the architecture in a predictable order.

- **Model tiering:** A cascade changes the model wallet first.
- **Caching layers:** Exact-response caches, semantic caches, and prompt-prefix caches remove repeated work before generation begins.
- **Retrieval budgets:** Caps on top-K, chunk size, and reranking depth constrain how much evidence enters the prompt.
- **Request limits:** Output-token caps, agent-step limits, tool-call budgets, and per-user quotas keep a single request from expanding without bound.
- **Batch processing:** Offline summarization, embedding refreshes, and evaluations move noninteractive work out of the latency-sensitive serving path.

### Priority order for interviews[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Priority-order-for-interviews)

In an interview, it helps to present the levers in the order that usually changes unit economics fastest.

#### Route first[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Route-first)

Routing changes the largest multiplier immediately because it alters which price sheet applies to most traffic.

#### Reuse second[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Reuse-second)

Caching then removes entire inference calls or discounts large prompt prefixes that remain stable across requests.

#### Trim third and cap fourth[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Trim-third-and-cap-fourth)

Retrieval budgets and output limits reduce token volume after routing and cache policy are already in place.

> **Practical tip:** It helps to state explicitly what percentage of traffic takes each path. Weighted averages make the design credible.

Each lever introduces failure modes such as stale cache entries, misrouted hard questions, and silent quality drops from overtrimmed context. So the next step is a concrete serving flow.

The hint below explains why prompt prefixes need to stay stable.

## Applying caching and model tiering[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Applying-caching-and-model-tiering)

The optimized online path begins before retrieval. The gateway first checks an exact-match cache for repeated FAQs and policy questions. If that misses, it checks a semantic cache. It uses a high similarity threshold so the system prefers a miss over a wrong cached answer.

Requests that still miss move to a lightweight complexity gate. This can be a small classifier, a rules engine, or a cheap model that predicts whether the query is easy, ambiguous, or policy sensitive. The serving layer then chooses a route.

- **Cache hit path:** The system returns a stored answer quickly and spends almost nothing on generation.
- **Easy miss path:** The system retrieves fewer chunks, uses a cheaper model, and applies tighter output limits.
- **Hard path:** The system keeps larger context budgets and calls the frontier model.

Let's assume a blended 30 percent cache-hit rate, 56 percent easy misses, and 14 percent hard misses after escalation. A 30 percent hit rate is realistic for first-turn and standalone questions such as FAQs, but follow-up turns depend on earlier messages and hit far less often, so the rate should be measured per turn type. Even this reuse sharply changes blended economics.

Distributed-systems details matter here. Cache entries should be versioned by corpus snapshot so a documentation update invalidates only affected answers. Cache-store outages should fail open into generation, not fail the request. Routing should include a low-confidence escalation path instead of forcing one-shot classification.

> **Note:** A good router is conservative. Misclassifying an easy query as hard wastes money, but misclassifying a hard query as easy damages quality and usually triggers expensive retries later.

The following illustration shows the detailed design of this routed serving path, including the two caches, the complexity gate, the per-route retrieval and output budgets, and the offline batch plane.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271421%27%20height=%27858%27/%3e)![Detailed design of a cost-optimized serving path](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of a cost-optimized serving path")

Detailed design of a cost-optimized serving path

The weighted paths are easier to compare as numbers. Let's assume the cheap model costs $0.50 per million input tokens and $1.50 per million output tokens, while the frontier model keeps its $5 and $15 prices. Easy misses use about 1.5K input and 150 output tokens, and hard queries use about 4K input and 400 output tokens.

The per-path costs include the machinery that picks the route. Every query that misses the exact cache pays for a semantic-cache embedding lookup, about $0.0001, and every miss pays for the complexity gate, about $0.0002, plus retrieval and reranking, about $0.001. Leaving these out would understate blended cost by about 20 percent, and each miss also spends tens of milliseconds of the TTFT budget on them.

Latency is measured as time to first token. Streaming lets the answer start within the budget, but a full 400-token hard-path answer still takes several seconds to finish.

The estimator below lets us vary traffic shares, token counts, and prices.

Blended Cost Estimator

Vary traffic shares, token counts, and prices to see blended cost per query and daily spend for the routed design.

Queries per DayN

queries

Cache-Hit Sharesc​

%

Easy-Miss Sharese​

%

Easy Input TokensIe​

tokens

Easy Output TokensOe​

tokens

Hard Input TokensIh​

tokens

Hard Output TokensOh​

tokens

Frontier Input PricePfi​

$/1M

Frontier Output PricePfo​

$/1M

Cheap Input PricePci​

$/1M

Cheap Output PricePco​

$/1M

Semantic Lookup CostCl​

$

Complexity Gate CostCg​

$

Retrieval and Rerank CostCr​

$

Hard-Query Sharesh​

14%

Easy-Miss CostCe​

0.0023$

Hard-Query CostCh​

0.0273$

Blended Cost per QueryC

0.0051$

Daily SpendD

5,100$

Naive Cost per QueryCn​

0.0215$

Savings vs Naivex

4.2×

Blended cost is **$0.0051** per query, or about **$5,100** per day. That is **4.2x** cheaper than the **$0.0215** naive flow, and the hard path drives most of the spend.

Do you find this helpful?

Routing and caching decide which model handles each request, but the token volume inside each path still drives cost. Next, let's see how retrieval budgets and request limits keep that volume in check.

## Retrieval budgets and request limits[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Retrieval-budgets-and-request-limits)

After routing decides the model path, the next control point is token intake. Retrieval should not dump everything into the prompt. The retrieval service should request enough evidence to answer the question, then stop. In practice, routine support traffic often works with 3 to 5 chunks instead of 10, especially if reranking pushes the best evidence upward.

A useful mental model is a library desk. Pulling ten folders every time costs time and attention. Pulling the top three well-indexed folders usually works, and only difficult cases require a deeper search.

### Retrieval-side controls[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Retrieval-side-controls)

The online path can reduce input tokens through several mechanisms.

- **Top-K limits:** Easy routes can cap retrieval at 3 to 5 chunks, while hard routes keep larger budgets.
- **Chunk deduplication:** Near-duplicate passages should be removed before prompt assembly.
- **Context trimming:** Low-value metadata, boilerplate headers, and repeated navigation text should not consume model context.
- **Reranking:** A reranker increases evidence quality per token.

### Generation-side controls[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Generation-side-controls)

The system should also constrain how much text it asks the model to generate.

- **Output caps**: Easy routes can default to 100 to 150 tokens, while hard routes get larger caps only when needed.
- **Structured stopping**: Templates, JSON schemas, and explicit stop conditions reduce rambling completions and improve predictability.

Agentic systems need the same discipline. Tool calls, planning steps, and recursive retries all need caps. An unbounded agent loop is both a latency amplifier and a hidden budget leak.

> **Attention:** Token trimming can create silent regressions. Retrieval recall and answer accuracy need to be measured per route, not only as global averages.

With online requests bounded, the next step is keeping those bounds intact in production.

## Operating the system within budget[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Operating-the-system-within-budget)

Design-time controls are not enough. Production traffic drifts. New documents enlarge retrieved chunks, policy prompts grow, output length creeps upward, and outages push traffic onto more expensive fallback paths. The operating model must catch those shifts early.

Let's track unit economics per route, not only global totals.

- **Generation spend:** This covers cost per query and total tokens by model tier.
- **Retrieval spend:** This covers vector queries, reranker calls, and fan-out depth.
- **Reuse effectiveness:** This covers exact-cache hit rate, semantic-cache hit rate, and prompt-cache discount utilization.
- **Quality by path:** This compares answer accuracy, escalation rate, and retrieval recall between easy and hard routes.

Dashboards should include token percentiles, not just means. A small long tail of huge prompts can dominate the bill. Alerts fire when P95 retrieval fan-out or output length moves above policy.

Offline work stays separate from the serving plane. Reembedding corpora, nightly summarization, and evaluation runs should execute in batch systems with independent quotas. For some workloads, small self-hosted models with batching can beat managed APIs, but only after operational overhead is included.

> **Practical tip:** Budget guardrails work best as control loops that estimate, route, cap, measure, and recalibrate every week.

Failure handling also affects spend. Vector-store outages can force answer-only fallbacks. Cache invalidation bugs can serve stale guidance. Timeout storms can escalate too many requests to the expensive model at once. The system needs rate limits and degradation policies so incidents do not become billing spikes.

The following illustration shows how per-route metrics, alerts, and degradation policies form a budget control loop around the serving path.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271806.8000000000002%27%20height=%27764%27/%3e)![Operating within budget](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Operating within budget")

Operating within budget

The hint below lists the hidden cost components a complete estimate includes.

## Interview answer blueprint[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Interview-answer-blueprint)

In the interview, a strong answer stays tight and quantitative. It restates the requirements, computes the naive per-query cost, and shows why that cost fails. It then identifies the dominant multipliers, usually model tier, input context size, output length, and repeated work.

Next, it introduces optimizations in priority order: routing traffic across model tiers, checking caches before generation, trimming retrieval budgets, capping outputs and agent steps, and moving offline jobs into batch systems. For each path, it states the traffic share and estimated unit cost so the interviewer can see the weighted average rather than a list of tactics.

Finally, it closes the loop with trade-offs and operations, explaining how the system detects stale cache entries, misrouted hard queries, and fallback storms, and connecting every cost decision back to latency and quality guardrails. That framing is exactly what the next lesson uses when turning system design thinking into a strong 45-minute interview answer.

Let's test our understanding with the questions below.

Knowledge Check

Q1. In the routed design, about 14 percent of queries take the hard path, yet it drives most of the spend. Why?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Conclusion)

Cost at GenAI scale is an architectural outcome, not a cleanup step after deployment. The repeatable pattern is simple: estimate the naive path, then lower blended cost through routing, caching, retrieval budgets, and bounded generation while preserving latency and answer quality.

Strong interview answers make those moves with numbers, traffic shares, and failure handling.

Design a Document Extraction and Decision Pipeline

ElevenLabs

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Nonfunctional-requirements)

[Baseline cost estimate](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Baseline-cost-estimate)

[Cost levers in the architecture](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Cost-levers-in-the-architecture)

[Priority order for interviews](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Priority-order-for-interviews)

[Route first](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Route-first)

[Reuse second](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Reuse-second)

[Trim third and cap fourth](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Trim-third-and-cap-fourth)

[Applying caching and model tiering](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Applying-caching-and-model-tiering)

[Retrieval budgets and request limits](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Retrieval-budgets-and-request-limits)

[Retrieval-side controls](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Retrieval-side-controls)

[Generation-side controls](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Generation-side-controls)

[Operating the system within budget](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Operating-the-system-within-budget)

[Interview answer blueprint](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Interview-answer-blueprint)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-for-cost-at-1m-queries-a-day#Conclusion)