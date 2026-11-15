# Designing_a_Deep_Research_Agent_for_Budgeted_AI_Workflows

Source: https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design a Deep Research Agent

Explore the design of a deep research agent that decomposes research questions, gathers and verifies evidence from multiple sources, and synthesizes a cited report within defined time and budget constraints. Understand system architecture, workload estimation, trust boundaries, and safety features critical for reliable and cost-effective agentic AI workflows.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Resource-estimation)
  - [Work and cost estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Work-and-cost-estimation)
  - [Execution capacity estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Execution-capacity-estimation)
  - [Fetch and parsing bandwidth](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Fetch-and-parsing-bandwidth)
- [System design of a deep research agent](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#System-design-of-a-deep-research-agent)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#High-level-design)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Achieving-functional-requirements)
    - [Requirement-to-mechanism mapping](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Requirement-to-mechanism-mapping)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#A-detailed-system-design)
  - [Component behavior](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Component-behavior)
  - [Prompt injection boundary](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Prompt-injection-boundary)
    - [What the boundary enforces](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#What-the-boundary-enforces)
    - [What the guard checks](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#What-the-guard-checks)
  - [Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Putting-everything-together)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Workflow-of-the-system)
  - [Operational sequence](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Operational-sequence)
  - [Invariants and branch control](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Invariants-and-branch-control)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Achieving-nonfunctional-requirements)
- [Evaluation](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Evaluation)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Conclusion)

A product team asks for a research assistant that can answer "How are EU AI regulations changing enterprise compliance requirements?" in under 90 seconds and under $0.40. One model call will not do it. The system has to break the question into subquestions, search the web, read conflicting sources, keep citations attached, and stop before time or money runs out.

That is the design target for a deep research agent. In plain terms, it is a workflow that thinks in stages instead of pretending one prompt can do planning, retrieval, synthesis, and verification at once. The request enters an orchestrated pipeline that allocates budget, plans search breadth, reads candidate documents, stores evidence, writes a cited report, and verifies support for each claim.

The requirements are explicit and operational. The output must be readable, every factual claim must map to a source URL, total runtime must stay bounded, and model and tool spending must stay within budget. We should also measure report quality offline against a fixed benchmark. This lesson focuses on architecture, control, and safety boundaries rather than UI polish or implementation detail. That framing sets up the next lesson, where the same orchestration patterns will be generalized into broader multistep agentic workflows.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#System-requirements)

Let's turn this target into concrete functional and nonfunctional requirements.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Functional-requirements)

- **Question decomposition**: The system should break a research question into subquestions, search queries, and a report outline.
- **Parallel research**: The system should search, fetch, and read web sources in parallel and turn them into evidence records.
- **Cited report**: The system should write a readable report in which every factual claim maps to a source URL.
- **Verification**: The system should check citation support and surface conflicts between sources before release.
- **Auditability**: The system should log plans, tool actions, evidence, and verification outcomes.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Nonfunctional-requirements)

- **Latency**: Each run should finish in under 90 seconds.
- **Cost**: Each run should stay under $0.40 in model and tool spend.
- **Safety**: Retrieved content should never alter instructions or trigger tools.
- **Reliability**: A failure in one branch should stay local, and runs should resume from checkpoints.
- **Quality**: Report quality should be measured offline against a fixed benchmark before each release.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Resource-estimation)

Let's estimate the work, execution capacity, and fetch bandwidth one research run needs, starting with work and cost.

### Work and cost estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Work-and-cost-estimation)

A deep research agent spends resources on planning, search calls, document fetches, chunk reads, summaries, writing, and verification. Without an estimate of these units, the design will look clean on a diagram and fail under budget in production.

Let's use a back-of-the-envelope calculation that quickly estimates scale and feasibility, starting with a representative request. The planner generates 5 search queries. Each query returns 3 documents worth reading, so 15 fetched documents total. Suppose that each document contributes 2 chunks on average after extraction, producing 30 chunk reads. The run also includes one writer pass, one verifier pass, and the 5 search calls.

A simple token estimate might look like this.

- **Planner:** It consumes 400 input tokens and emits 250 output tokens.
- **Readers:** They consume about 1,200 input tokens per chunk and emit 150 output tokens, leading to 36,000 input and 4,500 output tokens across 30 chunks.
- **Writer:** It consumes 6,000 input tokens and emits 1,200 output tokens.
- **Verifier:** It consumes 4,000 input tokens and emits 500 output tokens.

At $5 per million input tokens and $15 per million output tokens, total cost is roughly $0.33. Latency is dominated by web I/O, not planning. Search and fetch together take about 8.5 of the 15.9 seconds, while the planner takes under 1. If 15 fetches run with concurrency 5, three waves of I/O determine the critical path. Breadth fights depth here. Pushing from the top 3 to the top 8 documents per query can easily blow both runtime and cost. That estimate defines the first operating envelope, and the next step turns it into a compact budget table.

The table below breaks the estimate down by stage.

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| **Stage** | **Avg. calls** | **Input tokens** | **Output tokens** | **Latency** | **Cost** | **Cost share** |
| **Planner** | 1 | 0.4k | 0.25k | 0.8s | $0.006 | 2% |
| **Search** | 5 | – | – | 2.5s | API fees | – |
| **Fetch and parse** | 15 | – | – | 6.0s | Compute only | – |
| **Read and summarize** | 30 | 36k | 4.5k | 3.0s | $0.248 | 75% |
| **Writer** | 1 | 6k | 1.2k | 2.2s | $0.048 | 15% |
| **Verifier** | 1 | 4k | 0.5k | 1.4s | $0.028 | 8% |
| **Total** | **53** | **46.4k** | **6.45k** | **15.9s** | **$0.33** | **100%** |

Fetch and parse runs 15 documents at concurrency 5, which is three waves of about 2 seconds each. Reading starts as chunks arrive and runs in parallel, so only about 3 seconds of it sits on the critical path.

### Execution capacity estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Execution-capacity-estimation)

After sizing one request, map those stages onto execution capacity. The planner is light and bursty. Research workers are mostly waiting on external I/O. The writer and verifier are LLM-heavy and should use protected capacity because their outputs determine final quality.

The simplest production shape uses an orchestrator, a task queue, and a bounded worker pool. The orchestrator creates branch tasks from the plan, pushes search and read jobs into the queue, and tracks per-run counters for tokens, dollars, and wall-clock time. The bounded pool limits parallel fetches so one user cannot consume all outbound connections or external API quota.

> **Note:** Concurrency reduces user latency, but it increases instantaneous spend and can trigger provider rate limits if not capped.

Admission control sits in front of the queue. If many users arrive at once, the system can defer low-priority jobs, lower search fan-out, or reject requests that cannot finish within SLO. This is standard backpressure.

Failures are mostly asymmetric. A search provider may stall, a PDF may expand into hundreds of pages, or multiple queries may return the same article. The orchestrator needs cancellation and deduplication so one bad branch does not drag the whole run past budget.

The diagram below shows where budget checks happen during execution.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271501%27%20height=%27631%27/%3e)![Bounded research execution](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Bounded research execution")

Bounded research execution

### Fetch and parsing bandwidth[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Fetch-and-parsing-bandwidth)

External I/O often dominates before model inference begins. Each research run issues search requests, fetches HTML or PDFs, extracts text, chunks documents, and transfers selected passages into model contexts. A deep research agent behaves less like a chatbot and more like a crawler with strict stopping rules.

We estimate bandwidth at the level of fetched bytes and extracted text. Fifteen candidate documents might mean only a few megabytes over the network, but malformed PDFs, cookie walls, or script-heavy pages can multiply parsing overhead and delay the critical path. Controls need to sit before parsing and before chunking.

Let's use the following controls to keep ingestion predictable.

- **Top-k limits:** These cap the number of candidate results per query before fetch fan-out begins.
- **Domain policies:** These enforce allowlists, blocklists, or trust tiers that shape which sources are even fetched.
- **MIME filters:** These reject unsupported or expensive formats before extraction starts.
- **Document caps:** These stop oversized pages or PDFs from flooding the parser and token budget.
- **Deduplication:** This removes repeated URLs or content hashes.

> **Practical tip:** It helps to start with a small exploration budget, then deepen only on sources whose first chunks materially increase evidence quality.

Caching search results and extracted text reduces repeated spend for related questions, but freshness may require bypassing caches for current events. With I/O bounded, the design can now focus on how the agent itself is structured.

## System design of a deep research agent[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#System-design-of-a-deep-research-agent)

Let's start with the high-level design.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#High-level-design)

The system should separate thinking, reading, and writing instead of giving one model every responsibility. In plain English, one part decides what to investigate, several parts gather evidence in parallel, and one part turns vetted evidence into a report.

The architecture uses three roles plus shared control services.

- **Planner:** It converts the user question into subtopics, search queries, priorities, and a depth strategy under explicit runtime and cost limits.
- **Researchers:** They execute searches, fetch documents, chunk content, summarize passages, and score relevance and trustworthiness.
- **Writer:** It synthesizes structured evidence into a readable report where each factual claim carries citations.
- **Guard service:** It enforces the trust boundary between trusted system instructions and untrusted retrieved content.
- **Budget manager:** It meters tokens, dollars, branch count, and wall-clock time across the run.
- **Memory and observability layer:** It stores plans, tool actions, evidence records, latencies, and final citations for auditability.
- **Source metadata store:** It keeps URLs, timestamps, publisher data, trust scores, and provenance attached to evidence.

A useful analogy is a newsroom. Reporters gather notes, editors assign work, and the final article is written from verified material rather than from raw rumor. Here the same split is enforced by system boundaries. The modularity also allows different models per role, which opens cost and latency trade-offs without changing the control plane.

The diagram below shows the trust boundary between system instructions and retrieved content.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271461%27%20height=%27551%27/%3e)![Evidence-first agent flow](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Evidence-first agent flow")

Evidence-first agent flow

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Achieving-functional-requirements)

Now, let's walk the request through the system and test each requirement against a mechanism. Quality begins at source selection. Researchers score documents by topical relevance, recency, source trust, and overlap with already collected evidence. The writer does not generate from open-ended memory. It writes from evidence records, which reduces unsupported claims.

Citations are handled as data, not formatting. Every evidence record stores URL, snippet, extraction timestamp, and chunk provenance. The writer can only cite from that store, and the verifier checks that each factual sentence maps to one or more records.

#### Requirement-to-mechanism mapping[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Requirement-to-mechanism-mapping)

The mapping below shows how the architecture turns constraints into runtime behavior.

- **Report quality:** The system ranks sources, reads selectively, and synthesizes from summaries rather than from raw web pages.
- **Source-backed claims:** The writer attaches citations from stored metadata, and the verifier flags sentences with no supporting evidence.
- **Runtime budget:** The orchestrator uses bounded concurrency, staged reading, and early stopping when coverage is sufficient.
- **Cost budget:** The budget manager tracks tokens and tool usage, then simplifies the plan when remaining budget falls below thresholds.
- **Safety:** The guard service scans retrieved content for prompt injection patterns and keeps untrusted text away from tool execution paths.
- **User trust:** Logs preserve searches, fetched URLs, summaries, and verification outcomes for review.

> **Attention:** Citation formatting is not citation correctness. A URL beside a sentence means nothing unless the verifier confirms semantic support.

The same life cycle works for the open web and for enterprise corpora. Only retrieval policy changes. Once requirements are mapped, the next step is a component-by-component design.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#A-detailed-system-design)

The orchestrator owns the run state and invokes each component in a controlled order. It creates a run ID, initializes budgets, persists checkpoints, and decides whether branches should broaden, deepen, retry, or terminate.

### Component behavior[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Component-behavior)

Each component should emit structured outputs so downstream stages can enforce invariants instead of interpreting free text.

- **Planner service:** It performs budget-aware decomposition and emits subquestions, query strings, a target outline, and a branch budget for each subtopic.
- **Search tool layer:** It abstracts providers, applies freshness filters and domain policies, and returns normalized search results.
- **Fetcher and parser:** It retrieves HTML or PDFs, extracts text, enforces size caps, and records parse failures without crashing the run.
- **Reader or summarizer:** It consumes chunks and emits evidence records containing claims, snippets, confidence, and source metadata.
- **Guard service:** It scans content for injection attempts and ensures retrieved text is treated only as data.
- **Writer service:** It follows the planned outline and synthesizes a report from evidence records only.
- **Verifier service:** It checks citation coverage, unsupported claims, and contradictions across sources.
- **Metadata layer:** It stores plans, tool actions, evidence, token usage, and latency for auditability.

### Prompt injection boundary[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Prompt-injection-boundary)

Prompt injection is the central safety problem in web-grounded agents.

#### What the boundary enforces[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#What-the-boundary-enforces)

The planner and tool executor are privileged. Raw web text is not. Retrieved content should be wrapped as data, summarized by a low-privilege reader, and passed forward only as structured records. Least-privilege tool access prevents a malicious page from escalating into actions.

#### What the guard checks[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#What-the-guard-checks)

The guard uses deterministic patterns and a separate classifier to flag text that tries to alter instructions, exfiltrate secrets, or redirect tools. It can quarantine evidence, lower trust scores, or drop the source entirely.

> **Note:** The safest tool call is the one untrusted content never gets a chance to influence.

With the components defined, the full workflow can be narrated end to end.

### Putting everything together[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Putting-everything-together)

At runtime, the request enters the orchestrator, which allocates a global budget and asks the planner for subquestions, queries, and branch budgets. Research workers then run with bounded parallelism. They search, fetch, parse, and summarize while the guard screens untrusted content and the metadata store records provenance for every evidence item.

Loop control is explicit. A branch stops when budget is exhausted, when evidence coverage for its subtopic is sufficient, or when recent fetches add no high-value information. Redundant branches are canceled after deduplication or low relevance scores. The run uses durable execution. Good checkpoint boundaries include after planning, after each search batch, and after each summary write.

The diagram below shows these components at runtime, including the trust boundary around web content, the budget checks that stop branches, and the verification gate before release.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271541%27%20height=%27481%27/%3e)![Detailed design of a deep research agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of a deep research agent")

Detailed design of a deep research agent

The sequence below lists each stage and the invariants it must preserve.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Workflow-of-the-system)

We can think of the workflow as a supervised loop, not an unconstrained agent. The orchestrator advances the run in stages and checks invariants at each boundary.

### Operational sequence[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Operational-sequence)

The system progresses through a fixed sequence of actions.

1. **Plan:** The planner emits subquestions, queries, and branch budgets.
2. **Search:** Researchers expand each branch into candidate URLs.
3. **Fetch and parse:** Documents are retrieved and converted into chunks.
4. **Guarded read:** The guard screens chunks, and readers turn them into evidence records.
5. **Write:** The writer synthesizes the report from evidence records only.
6. **Verify:** The verifier checks citation support and contradictions.
7. **Release:** The report goes out with its citations, or the run returns a marked draft or an error.

Planning sets the budgets. Everything after it runs under those limits. Reading and writing see only guarded, structured evidence, and nothing is released as final until verification passes. If it can’t run or fails, the system returns a marked draft or an error.

### Invariants and branch control[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Invariants-and-branch-control)

Every evidence item must retain URL, timestamp, and provenance. Every report claim must trace to evidence. Branches consume local budgets as the run consumes a global budget. If a branch keeps spending without improving coverage, the orchestrator prunes it. If sources conflict, the verifier escalates the disagreement instead of blending them into one unsupported sentence.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Achieving-nonfunctional-requirements)

Scalability comes from worker pools, queue-based orchestration, and caching of fetched documents or extracted summaries. Reliability comes from retries with idempotent task IDs, checkpointed run state, and bounded fan-out so failures remain local. Availability comes from fallback search providers and degraded modes that summarize fewer sources when one dependency fails.

Security relies on least privilege, source policy enforcement, and audit logs that retain evidence lineage. Agentic systems add unusual failure modes. Prompt injection can redirect reasoning, tool misuse can trigger unauthorized actions, citation hallucination can fabricate support, and uncontrolled loops can consume unlimited budget.

Let's track metrics that connect quality to spend.

- **Tokens per run:** This shows whether decomposition or reading depth is drifting upward.
- **Citations per paragraph:** This reveals whether report density and support are changing together.
- **Unsupported-claim rate:** This catches regressions in grounding and verifier effectiveness.
- **Latency percentiles:** These expose I/O stalls, queue buildup, and provider degradation.

> **Practical tip:** It helps to monitor branch cancellation rate too. A rising rate often means the planner is overexpanding low-value work.

These runtime metrics pair with the offline evaluation below.

## Evaluation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Evaluation)

Runtime metrics show whether the system is running well. They don’t show whether the reports are good, so the design also needs offline evaluation.

Let's build a fixed benchmark of 50 to 100 research questions covering different types: broad overviews, fast-moving topics, and questions where sources conflict. For each question, store reference notes: key facts a good report must include and a few trusted sources. The agent runs on the full set before every release that changes the planner, prompts, models, or budgets.

Each report is scored on four dimensions.

|  |  |  |
| --- | --- | --- |
| **Dimension** | **What it checks** | **Scored by** |
| Coverage | Does the report include the key facts and subtopics from the reference notes? | LLM judge against the notes |
| Citation accuracy | Does each cited source support its sentence? | Verifier plus judge on a sample |
| Conflict handling | Are disagreements between sources surfaced, not blended? | LLM judge |
| Budget compliance | Did the run finish within 90 seconds and $0.40? | Run logs |

An LLM judge is cheap and scalable, but it has its own biases, such as favoring longer reports. We calibrate it by having people score a sample of about 20 reports and checking that the judge agrees with them. Results are tracked by question type, so a gain on broad questions can’t hide a drop on conflicting-source questions.

Offline scores gate releases. Online metrics (unsupported-claim rate, tokens per run, latency percentiles) catch what the benchmark misses. Failing production questions are added to the benchmark over time.

Knowledge Check

Q1. A research run exceeds its 90-second budget. Search and fetch take most of the time, and many fetched pages are mirrored copies of the same article. Which change fits best?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Conclusion)

A deep research agent is a budgeted distributed workflow, not a clever single prompt. The strongest designs separate planning, guarded evidence collection, synthesis, and verification, then enforce budgets and termination at every stage.

In interviews, the differentiators are usually estimation discipline, the trust boundary around web content, and a credible evaluation plan. Once you can design this flagship agent, the next step is straightforward: generalize the same control patterns into broader multistep agentic workflows.

DALL·E

Design a Multi-Step Agentic Workflow

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Resource-estimation)

[Work and cost estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Work-and-cost-estimation)

[Execution capacity estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Execution-capacity-estimation)

[Fetch and parsing bandwidth](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Fetch-and-parsing-bandwidth)

[System design of a deep research agent](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#System-design-of-a-deep-research-agent)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#High-level-design)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Achieving-functional-requirements)

[Requirement-to-mechanism mapping](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Requirement-to-mechanism-mapping)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#A-detailed-system-design)

[Component behavior](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Component-behavior)

[Prompt injection boundary](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Prompt-injection-boundary)

[What the boundary enforces](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#What-the-boundary-enforces)

[What the guard checks](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#What-the-guard-checks)

[Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Putting-everything-together)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Workflow-of-the-system)

[Operational sequence](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Operational-sequence)

[Invariants and branch control](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Invariants-and-branch-control)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Achieving-nonfunctional-requirements)

[Evaluation](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Evaluation)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-deep-research-agent#Conclusion)