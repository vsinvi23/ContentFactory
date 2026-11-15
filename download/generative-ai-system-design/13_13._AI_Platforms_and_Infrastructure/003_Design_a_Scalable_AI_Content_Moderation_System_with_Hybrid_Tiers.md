# Design_a_Scalable_AI_Content_Moderation_System_with_Hybrid_Tiers

Source: https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design an AI Content Moderation System

Design an AI content moderation system that screens 500 million daily submissions under tight latency and cost budgets. It uses a cascade of rules, lightweight classifiers, LLM adjudication, and human review, with category-specific thresholds, appeals, and versioned policies.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Resource-estimation)
- [System design of an AI content moderation system](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#System-design-of-an-AI-content-moderation-system)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#High-level-design)
    - [The four-tier moderation path](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#The-four-tier-moderation-path)
    - [Routing signals](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Routing-signals)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Achieving-functional-requirements)
    - [Requirement-to-mechanism mapping](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Requirement-to-mechanism-mapping)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#A-detailed-system-design)
  - [Core services in the request path](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Core-services-in-the-request-path)
  - [Storage and reliability mechanics](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Storage-and-reliability-mechanics)
    - [Data stores](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Data-stores)
    - [Failure handling](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Failure-handling)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Workflow-of-the-system)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Achieving-nonfunctional-requirements)
- [Evaluation and policy updates](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Evaluation-and-policy-updates)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Conclusion)

Hundreds of millions of posts, messages, images, and videos can arrive each day, and the platform still has to stop harmful content before users see it. Sending every submission to a large language model or a human reviewer breaks both latency and cost budgets, so the system must make most decisions cheaply and reserve expensive judgment for the minority of ambiguous cases.

This lesson builds a hybrid moderation system that combines rules, lightweight classifiers, LLM adjudication, and human review in one production pipeline. In an interview, that means framing trust and safety as a system with measurable targets rather than as a vague policy problem.

The scope starts with category-specific precision and recall, pre-publish and post-publish latency budgets, and submission volume. A moderation system also makes asymmetric decisions. Missing a credible terror threat is not the same as overblocking satire, and the acceptable trade-off changes by category.

We can think of the design like an airport security line. Most bags pass quick screening, a few go through deeper scans, and only the uncertain ones reach manual inspection.

By the end, you should be able to explain how uncertain machine decisions are routed through structured review and policy layers, a pattern that carries directly into the next lesson on extraction and decision pipelines.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#System-requirements)

Let's start by defining the product behavior before drawing boxes. The system receives text, images, short videos, audio transcripts, and links, then decides whether to allow, block, downrank, age-gate, or send the submission for review.

Let's use the following categories to anchor the design discussion.

- **Terrorism and violent threats:** These categories usually optimize for recall first because legal and safety exposure from false negatives is unacceptable.
- **Hate speech and harassment:** These categories often use balanced thresholds, with precision increasing on speech-sensitive surfaces.
- **Misinformation and self-harm:** These categories often require policy nuance, escalation, and review-heavy handling.
- **Spam, scams, and phishing:** These categories support aggressive automated blocking because repeated patterns make them easier to detect.

Terrorist content needs special handling outside the normal cascade. Known material is detected mainly through hash matching against industry-shared databases, and platforms often face legal duties to remove it within hours and to report credible threats to the authorities. The evidence is kept out of third-party LLMs and general reviewer queues. Matches go to a restricted evidence vault and a small specialist team, and the escalation and reporting workflow runs outside the standard pipeline.

For latency, we split the system into pre-publish and post-publish paths. Urgent blocking on uploads or public comments may need sub-200 ms p99, which only Tier 1 and Tier 2 decisions can meet. Items that need the LLM or human tier are held back for severe categories, or published with limited reach and reviewed afterward for lower-risk ones, while slower judgments on nuanced misinformation can tolerate seconds.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Functional-requirements)

- **Multimodal decisions:** The system should accept text, images, short videos, audio transcripts, and links, and return allow, block, downrank, age-gate, or review.
- **Per-category handling:** The system should apply different thresholds and actions by harm category and by surface.
- **Review and appeals:** The system should route uncertain or severe items to specialized queues, and replay the original evidence on appeal.
- **Policy updates:** Teams should be able to change rules, prompts, and thresholds without retraining every model.
- **Sensitive-evidence isolation:** The system should keep terrorist-content evidence out of third-party LLMs, the normal stores, and the general reviewer pool.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Nonfunctional-requirements)

- **Latency:** Tier 1 and Tier 2 decisions stay under 200 ms p99 on the pre-publish path.
- **Scale:** The system should handle 500 million submissions per day, about 5,800 QPS on average and 17,000 at peak.
- **Cost:** The system should send at most 5 percent of traffic to the LLM tier and 0.5 percent to human review.
- **Availability:** The system should degrade to review-based handling, never to a silent allow, when the LLM tier fails.
- **Auditability and compliance:** The system should keep an immutable decision log with model and policy versions, encrypted evidence, role-based reviewer access, and regional data boundaries.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Resource-estimation)

Now, let's estimate the scale. With 500 million submissions per day, suppose rules resolve 65 percent (known-bad blocks plus allows for known-safe hashes and trusted sources) and lightweight classifiers resolve another 30 percent. The remaining 5 percent reach the LLM tier, and about 10 percent of those, or 0.5 percent of all traffic, go on to human review. That still means 2.5 million human-reviewed items daily.

> **Note:** Reviewer volume is the hidden scaling constraint. A design that sends even 2 percent of traffic to humans becomes operationally fragile very quickly.

If one reviewer handles 400 items per day, capacity needs are about 2,500,000/400=6,2502{,}500{,}000 / 400 = 6{,}2502,500,000/400=6,250 reviewer-days each day, before coverage for languages, shifts, and quality checks. That estimate forces a moderation cascade rather than a single-model design.

The LLM tier is the other cost line. Five percent of 500 million is 25 million LLM calls per day, and at about 1,000 tokens each that is about 25 billion tokens per day, or roughly 290 calls per second on average and 870 at peak. The rule engine sees every submission, about 5,800 QPS on average and 17,000 at peak, while classifiers see the 35 percent that rules do not resolve, about 2,000 QPS on average and 6,000 at peak. Sending everything to an LLM would multiply the token bill by 20, so the cascade is forced by economics as well as by reviewer capacity.

The estimator below lets us vary traffic, tier shares, and token price.

Moderation Capacity Estimator

Vary traffic, tier shares, token price, and reviewer throughput to see LLM spend, reviewer headcount, and peak QPS for each tier.

Submissions per dayS

items

Resolved by rulesR

%

Resolved by classifiersC

%

Human review share of all trafficH

%

Tokens per LLM callT

tokens

Price per million tokensP

$

Peak-to-averageK

x

Items per reviewer per dayI

items

Share reaching the LLM tierL

5%

LLM calls per dayNllm​

25million

LLM tokens per dayTok

25billion

LLM spend per dayCost

12.5$K

Human-reviewed items per dayNh​

2.5million

Reviewers neededW

6,250reviewers

Rule engine peak QPSQ1​

17,361QPS

Classifier peak QPSQ2​

6,076QPS

LLM peak QPSQ3​

868QPS

At this mix, **25 million** LLM calls per day use **25 billion** tokens and cost about **$12.5K** per day. Human review adds **2.5 million** items, which needs about **6,250** reviewers. Peak load is **17,361** QPS at the rule engine, **6,076** at classifiers, and **868** at the LLM tier.

Do you find this helpful?

With the requirements and scale set, we can shape the cascade that meets them.

## System design of an AI content moderation system[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#System-design-of-an-AI-content-moderation-system)

Let's start with the high-level design of an AI content moderation system.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#High-level-design)

A good interview answer describes a cascade, not a monolithic model. The system makes cheap decisions first, then spends more compute only when uncertainty remains.

#### The four-tier moderation path[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#The-four-tier-moderation-path)

A simple way to think about it is a hospital triage desk. Obvious emergencies are fast-tracked, routine cases are handled quickly, and only unclear cases consume specialist time.

- **Tier 1 rule and hash engine:** This stage checks exact hashes, perceptual hash, URL blocklists, regexes, and hard policy rules. It returns deterministic blocks for known-bad content and allows only for known-safe hashes or trusted sources, in a few milliseconds. Everything else continues to Tier 2.
- **Tier 2 lightweight classifiers:** This stage runs small text, image, and spam models under tight latency budgets. It handles most traffic and emits category scores with calibrated confidence.
- **Tier 3 LLM adjudication:** This stage reads the evidence bundle and policy prompt for nuanced, multilingual, or adversarial cases. It behaves like a policy-aware judge rather than a universal first-pass filter.
- **Tier 4 human review:** This stage handles high-severity, low-confidence, or appealed content. Review queues are specialized by language, region, and urgency.

#### Routing signals[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Routing-signals)

Routing depends on more than score alone.

- **Confidence thresholds:** High-confidence outputs can auto-enforce, while uncertain outputs escalate.
- **Content type:** Images, transcripts, and text each use different detectors before decisions are merged.
- **User surface:** Direct messages, livestream chat, and public feeds can have different thresholds and SLAs.
- **Policy category:** Legally sensitive harms escalate faster and tolerate more false positives.
- **Account signals:** Account age, reputation, past violations, and posting rate shift thresholds, so a new account with repeated violations escalates sooner than a long-standing one.

> **Attention:** Candidates often say "use an LLM for moderation" without specifying what fraction of traffic it sees. In production, expensive tiers must process only a small minority.

To visualize that flow, we can place the tiers into one end-to-end architecture with separate fast and slow paths.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271752.1999999999998%27%20height=%27501%27/%3e)![Moderation cascade overview](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Moderation cascade overview")

Moderation cascade overview

Next, let's map the functional requirements to this cascade.

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Achieving-functional-requirements)

The architecture meets functional goals by assigning a different operating point to each harm category instead of relying on one global threshold. Terrorism and violent threats can trigger recall-first routing with immediate blocking or urgent escalation, while harassment and borderline hate speech can use tighter precision thresholds to reduce over-enforcement.

#### Requirement-to-mechanism mapping[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Requirement-to-mechanism-mapping)

The mechanics are straightforward when tied to the request path.

- **Low-latency prepublish moderation:** Tier 1 and Tier 2 absorb most traffic inside the strict latency budget.
- **Nuanced policy handling:** Tier 3 and human review handle ambiguity, multilingual content, and context-heavy judgments.
- **Severity-first processing:** Queue priority pushes imminent threats, terrorism, exploitative content, and legal escalations ahead of standard review.
- **Appeals as a product feature:** A dedicated appeals workflow stores replayable evidence, reviewer context, and reversal actions with its own SLA.
- **Fast policy updates:** Policy-as-data lets trust and safety teams update behavior without retraining every model.
- **Multimodal support:** Text, image, and audio-derived signals are merged before enforcement decisions are issued.

No single score captures system quality. Teams need category-level behavior per surface, because the same phrase can be harmless in a private message, abusive in public comments, or escalated when paired with repeated targeting.

The queueing view below shows how human review and appeals preserve that differentiated handling.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271201%27%20height=%27858%27/%3e)![Review queue operations](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Review queue operations")

Review queue operations

With the requirements mapped to the cascade, the next step is the backend decomposition that makes it reliable.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#A-detailed-system-design)

Now, let's switch from policy flow to service boundaries, showing how requests move through backend components and how decisions stay auditable.

### Core services in the request path[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Core-services-in-the-request-path)

Each service should own one clear responsibility and emit versioned outputs that downstream systems can replay later.

- **Ingestion and normalization:** The ingestion layer accepts text, image, video, and audio submissions, authenticates the caller, strips malformed payloads, normalizes metadata, and generates transcripts or sampled frames when needed.
- **Rule and hash engine:** This service checks exact hashes, perceptual hashes, banned domains, and deterministic policy rules for known illegal or previously removed content.
- **Classifier service:** This stateless service runs category-specific small models, applies versioned thresholds, and returns calibrated scores plus model identifiers.
- **LLM adjudication service:** This service receives only ambiguous cases, uses policy templates, requests structured JSON output, and isolates prompts from raw user instructions to reduce injection risk.
- **Decision engine:** This service merges rule hits, classifier scores, and LLM outputs into one enforcement action and attaches reason codes.
- **Event logging pipeline:** This asynchronous path writes idempotent moderation events, model versions, policy versions, evidence references, and reviewer outcomes.

The following illustration shows how these services connect to the data stores, review queues, and logging pipeline described in the following sections.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271402.17%27%20height=%27550.165%27/%3e)![Detailed design of an AI content moderation system](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of an AI content moderation system")

Detailed design of an AI content moderation system

### Storage and reliability mechanics[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Storage-and-reliability-mechanics)

The design also needs state.

#### Data stores[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Data-stores)

- **Submission store:** Raw content and normalized artifacts are stored with retention controls. Terrorist-content evidence is the exception: it is held in a separate restricted vault.
- **Feature store:** Derived embeddings, image fingerprints, and classifier features are cached for reuse.
- **Decision log:** Every enforcement result is appended to an immutable audit trail.
- **Reviewer label store:** Human decisions and override reasons feed retraining and appeals.
- **Analytics store:** Aggregate metrics support dashboards, drift detection, and policy rollout analysis.

#### Failure handling[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Failure-handling)

- **Queues and backpressure:** Tier transitions use partitioned queues so bursts do not overload downstream services.
- **Retries and dead letters:** Transient failures retry automatically, while malformed or repeatedly failing jobs move to a dead-letter queue for inspection.
- **Regional deployment:** Public traffic is served from multiple regions, while sensitive evidence stays within jurisdictional boundaries when required.

The following note deepens one design principle that comes up often in interviews.

With services and storage defined, you can walk an interviewer through one submission end to end.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Workflow-of-the-system)

A request starts at the API gateway, where authentication, rate limiting, and abuse checks run before the payload enters moderation. The ingestion service then normalizes the content, extracts links and metadata, and generates derived inputs such as OCR text or audio transcripts.

Next, Tier 1 checks exact hashes, perceptual hashes, regexes, and domain rules. Known illegal content can be blocked immediately, while content matching known-safe hashes or from trusted sources may bypass deeper analysis.

Unresolved items move to Tier 2, where lightweight models score categories under a tight latency budget. High-confidence outputs go to the decision engine for auto-enforcement. Low-confidence or policy-sensitive items are packaged with evidence and sent to Tier 3, where the LLM receives the current policy prompt and returns structured findings.

If uncertainty remains, or if the content involves severe harm, the system places the item into a specialized human review queue based on language, region, urgency, and policy type. After a decision, enforcement propagates to storage, search indexes, ranking systems, and user notifications.

Appeals replay the original evidence bundle, earlier reason codes, and exact model and policy versions so reviewers can reconstruct the decision path.

Next, let's check the design against the nonfunctional requirements.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Achieving-nonfunctional-requirements)

Scalability starts with stateless classifier and decision services that autoscale horizontally behind queues. Nonurgent content can be processed in batches, while urgent public submissions stay on the fast path. Partitioned queues keep hot categories or languages from starving the rest of the workload.

Availability comes from multiregion ingestion and failover. If the LLM adjudication service becomes unavailable, the system should degrade safely by routing ambiguous items to slower review-based handling instead of silently allowing them. That is a better failure mode for severe categories.

Reliability depends on replayable logs, idempotent actions, retries, and dead-letter queues. A removed post should not be deleted twice in inconsistent ways, and an appeal should be able to reconstruct the original decision exactly.

> **Note:** Graceful degradation is often the difference between a research pipeline and a production system.

Performance is controlled by giving each tier a budget and constraining LLM traffic to a small percentage. Security and compliance require encryption, role-based reviewer access, audit trails, and retention rules for sensitive evidence. Fairness and robustness require continuous checks for threshold drift, language bias, and adversarial evasion.

The next note captures several trade-offs that interviewers often probe directly.

The final layer is how the system is measured and updated after launch.

## Evaluation and policy updates[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Evaluation-and-policy-updates)

Launch does not end the design. The system logs outcomes per harm category, language, geography, modality, and user surface, then computes precision, recall, false-positive rate, false-negative rate, appeal overturn rate, harm exposure rate, queue latency, and time to policy rollout.

Online monitoring watches for drift, new evasion patterns, and threshold degradation. When policies change, trust and safety teams update rules, prompts, taxonomies, and thresholds under version control, then release through canaries with rollback support.

> **Attention:** Aggregate accuracy can rise while one critical category gets worse. Moderation quality has to be read slice by slice.

Reviewer labels and successful appeals flow back into training data sets and threshold recalibration, closing the loop between operations and model quality. Let's test those design choices with the questions below.

Knowledge Check

Q1. Why is terrorist-content evidence kept out of the normal moderation cascade?

Do you find this helpful?

That closes the design loop from requirements to operations to continuous policy evolution.

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Conclusion)

A scalable moderation system works by narrowing uncertainty in stages. Rules and hashes remove known cases, lightweight models absorb most volume, and LLMs plus humans handle the ambiguous edge cases that remain.

For interviews, it helps to keep returning to the same anchors: category-specific precision and recall, traffic estimation, reviewer capacity, appeals, and policy versioning. The next lesson reuses this same orchestration pattern, but applies it to document extraction and decision pipelines where uncertain machine outputs also need structured escalation.

Design a GPU Training Job Scheduler

Design a Document Extraction and Decision Pipeline

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Resource-estimation)

[System design of an AI content moderation system](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#System-design-of-an-AI-content-moderation-system)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#High-level-design)

[The four-tier moderation path](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#The-four-tier-moderation-path)

[Routing signals](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Routing-signals)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Achieving-functional-requirements)

[Requirement-to-mechanism mapping](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Requirement-to-mechanism-mapping)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#A-detailed-system-design)

[Core services in the request path](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Core-services-in-the-request-path)

[Storage and reliability mechanics](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Storage-and-reliability-mechanics)

[Data stores](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Data-stores)

[Failure handling](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Failure-handling)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Workflow-of-the-system)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Achieving-nonfunctional-requirements)

[Evaluation and policy updates](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Evaluation-and-policy-updates)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-content-moderation-system#Conclusion)