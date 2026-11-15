# Designing_a_GenAI_Gateway_for_Unified_Access_and_Scalability

Source: https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design a GenAI Gateway

Design a GenAI gateway that unifies provider integrations behind one internal API and enforces identity, policy, routing, caching, and metering on every request. Keep it low-latency and highly available at millions of daily requests, so it acts as the central control point for safety, reliability, and cost visibility.

We'll cover the following...

- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Resource-estimation)
- [System design of a GenAI gateway](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#System-design-of-a-GenAI-gateway)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#High-level-design)
    - [Data plane components](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Data-plane-components)
    - [Control plane and state](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Control-plane-and-state)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Achieving-functional-requirements)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#A-detailed-system-design)
  - [Admission and policy path](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Admission-and-policy-path)
    - [Identity and access checks](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Identity-and-access-checks)
    - [Token-aware throttling](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Token-aware-throttling)
  - [Transformation and execution path](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Transformation-and-execution-path)
  - [Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Putting-everything-together)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Workflow-of-the-system)
  - [Normal request path](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Normal-request-path)
  - [Failure and completion path](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Failure-and-completion-path)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Achieving-nonfunctional-requirements)
- [Trade-offs and interview discussion](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Trade-offs-and-interview-discussion)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Conclusion)

Eight product teams ship copilots in parallel. Within a quarter, the company has five sets of provider credentials, four retry implementations, three incompatible safety filters, and no reliable answer to a simple finance question about who spent the last $200,000 on LLM calls.

A GenAI gateway fixes that by turning scattered provider integrations into one internal platform surface. Clients send requests to a canonical API, and the gateway enforces identity, policy, routing, caching, fallback, and metering before any provider call leaves the company boundary.

In an interview, this is an AI platform design problem rather than a model problem. The discussion centers on how the request is controlled, how failures are contained, and how governance remains enforceable while throughput scales to millions of requests per day.

The scope here stays deliberately narrow. We will design unified access, security checks, token-aware limits, reliability mechanisms, and cost visibility around LLM traffic.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#System-requirements)

Let's start with the following functional and nonfunctional requirements.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Functional-requirements)

The functional requirements should cover the entire request path.

- **Unified API:** The gateway should expose one provider-agnostic interface for prompting, embeddings, and streaming responses.
- **Access control:** The system should authenticate callers, authorize allowed models, and enforce provider approval rules.
- **Traffic control:** The platform should enforce quotas, rate limiting, and longer-running spend budgets.
- **Execution controls:** The gateway should route requests, apply fallback, cache repeat traffic, log usage, and attribute cost by team.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Nonfunctional-requirements)

The nonfunctional side then drives implementation choices.

- **Low overhead:** The gateway should add under 20 ms of p99 latency, which rules out slow synchronous checks on the hot path.
- **High availability:** The fleet should survive instance, region, and provider failures.
- **Extensibility:** New providers and routing policies should plug in without client rewrites.
- **Compliance:** The system should produce audit trails and constrain regulated data paths.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Resource-estimation)

Start with rough numbers before drawing boxes. A gateway design becomes much clearer once you quantify teams, providers, request volume, and token flow. In GenAI systems, requests are shaped not only by count but also by tokens, streaming duration, and provider-specific limits.

Assume an enterprise with 40 internal teams, 4 providers, and 8 million requests per day. If 35 percent of traffic streams output tokens and an average request carries 1,200 input tokens plus 500 output tokens, daily token volume exceeds 13 billion tokens. Spread over a day, 8 million requests is only about 93 requests per second on average, or roughly 460 at a 5 times peak, which is a small load for Redis. Streaming sets the connection load: with 35 percent of requests streaming for about 12 seconds each, the gateway holds roughly 400 concurrent streams on average and about 2,000 at peak.

Gateway Capacity Estimator

Change the workload to see how request rate, token volume, and open streams move.

Requests per dayR

requests

Peak-to-average ratiop

x

Average input tokensI

tokens

Average output tokensO

tokens

Streaming shares

%

Average stream durationd

s

Average QPSQ

92.59req/s

Peak QPSQp​

462.95req/s

Tokens per dayT

13.6billion

Average concurrent streamsC

388.88streams

Peak concurrent streamsCp​

1,944.4streams

The gateway handles **92.59 QPS** on average and **462.95 QPS** at peak, moves **13.6 billion tokens** per day, and holds about **1,944.4 concurrent streams** at peak.

Do you find this helpful?

## System design of a GenAI gateway[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#System-design-of-a-GenAI-gateway)

Let's start with the high-level design of a GenAI gateway.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#High-level-design)

The simplest mental model is this. The data plane handles live requests. The control plane tells the data plane which rules to apply.

At the edge, internal product services call an API gateway or edge proxy that terminates TLS, validates coarse-grained client access, and forwards traffic to a load balancer. Behind it sits a stateless GenAI gateway fleet. Each instance runs request middleware for auth, policy checks, prompt scanning, quota enforcement, routing, caching, streaming proxying, and usage emission.

> **Note:** Keep the gateway stateless on the hot path. Shared state belongs in external stores so replicas scale horizontally and fail independently.

#### Data plane components[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Data-plane-components)

Inside the data plane, the request moves through several cross-cutting modules.

- **Policy enforcement:** The gateway maps credentials to a team identity and validates permitted models, regions, and data-handling constraints.
- **Safety middleware:** Input checks run before provider selection: PII detection and redaction. Output checks run after the response: moderation and policy filters.
- **Execution services:** The router selects a primary model, the cache checks for a hit, and provider adapters translate canonical requests into provider-specific APIs.
- **Reliability controls:** Retries, circuit breakers, and fallback chains keep isolated provider failures from breaking clients.
- **Telemetry path:** The gateway emits logs, metrics, and usage events asynchronously so the synchronous path stays lean.

#### Control plane and state[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Control-plane-and-state)

The control plane stores all slow-changing configuration. Think of it like an air traffic control tower issuing rules while the planes keep moving independently.

- **Registry and policy stores:** The control plane maintains provider registry data, model capability tags, pricing metadata, quotas, approved-provider lists, residency constraints, and routing policies.
- **Shared infrastructure stores:** Redis stores hot counters and exact-match cache entries. A queue or log stream stores usage events for later aggregation. An analytics warehouse supports dashboards for spend, latency, and provider health.

The diagram below separates the data plane from the control plane.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271411.0800000000002%27%20height=%27390.72%27/%3e)![Gateway architecture overview](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Gateway architecture overview")

Gateway architecture overview

With the system boundary in place, we can now inspect how each requirement is enforced.

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Achieving-functional-requirements)

A good gateway answer ties each requirement to a mechanism in the request path rather than listing features abstractly.

Unified access begins with a canonical internal API. The request shape normalizes prompt fields, streaming flags, tool parameters, and response metadata so clients do not care whether the downstream call lands on OpenAI, Anthropic, a self-hosted model, or an internal inference stack. Provider adapters absorb those differences.

Authentication answers who is calling, while authorization answers what they may use. Teams usually authenticate with service accounts, signed internal tokens, or team-scoped API keys. The gateway then applies model-level RBAC, approved-provider rules, and region restrictions before any request is admitted.

> **Practical tip:** In interviews, separate authentication, authorization, quotas, and budgets explicitly. Candidates often merge them and lose precision.

Security and governance work as middleware. Prompt scanners detect sensitive strings, PII, and policy violations. Sensitive traffic can be masked, blocked, or routed only to private providers.

Reliability comes from health-aware routing, retries with backoff, and circuit breakers. Fallback should target only providers in the same capability class.

Performance uses exact caching first, optional semantic caching second, and streaming passthrough to preserve time to first token. The gateway also keeps prompt prefixes stable, with system prompts first, so provider-side prefix caching can cut input cost. Cost control comes from token accounting and usage tags attached to every request.

The next section details each component.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#A-detailed-system-design)

Now move from boxes to mechanics. Each gateway instance should execute the same deterministic pipeline, with shared stores handling mutable state.

### Admission and policy path[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Admission-and-policy-path)

The first stage decides whether the request may run at all.

#### Identity and access checks[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Identity-and-access-checks)

Credentials map to a team, environment, and application. The policy layer then evaluates allowed models, approved providers, data residency rules, and whether the caller can access premium capabilities such as long-context or multimodal endpoints.

#### Token-aware throttling[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Token-aware-throttling)

LLM traffic needs both RPM and TPM controls. Before execution, the gateway estimates input tokens and reserves an expected output allowance, often by using a token bucket in Redis. If a request asks for 1,500 estimated input tokens and 700 expected output tokens, the gateway reserves 2,200 tokens against the team's current minute bucket. After completion, it reconciles that estimate against actual usage. This approach is production-friendly even though estimation is imperfect.

> **Attention:** Streaming makes TPM harder because the final output size is unknown at admission time. Reserve first, reconcile later, and cap worst-case output.

### Transformation and execution path[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Transformation-and-execution-path)

Once admitted, the request enters the safety and provider selection stages.

- **PII and guardrails:** The middleware detects emails, identifiers, and regulated entities, masks them where policy allows, and routes sensitive traffic only to approved private endpoints.
- **Router:** The router uses capability tags, latency SLOs, price, geography, and provider health to choose a primary model and an ordered fallback set.
- **Provider adapters:** Adapters translate the canonical request into each provider API and normalize responses, token counts, and error semantics.
- **Caching:** Exact-match caching keys on tenant, user permission scope, prompt, parameters, and retrieved context, and fits deterministic or low-temperature requests best. Semantic cache may sit behind stricter policies.
- **Telemetry:** The gateway publishes usage records asynchronously to a queue, which keeps warehouse writes and cost aggregation off the hot path.

### Putting everything together[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Putting-everything-together)

The following illustration brings the admission path, the execution path, the provider layer, and the control plane together into one detailed design of the GenAI gateway.

Follow a request from left to right. After the edge proxy and load balancer, the admission path authenticates the team, checks policy, and reserves tokens in Redis, returning a 429 when the budget is exhausted. The execution path then masks sensitive content, routes to a primary model with ordered fallbacks, and checks the exact cache. On a miss, a provider adapter calls the model, with retries and fallback allowed only before the first token. The streaming proxy relays chunks through output filters, and on completion, actual usage reconciles the reservation and flows asynchronously to the analytics warehouse.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271971%27%20height=%27645%27/%3e)![Detailed design of a GenAI gateway](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Detailed design of a GenAI gateway")

Detailed design of a GenAI gateway

Every gateway instance runs the same pipeline, so any instance can serve any request. Redis holds the token buckets, counters, and exact-match cache that all instances share. The control plane pushes registry, policy, routing, and budget updates to every instance, and usage records leave the hot path through an asynchronous queue.

The next section follows one request through these components.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Workflow-of-the-system)

A single request should follow a predictable path, even when the provider does not.

### Normal request path[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Normal-request-path)

A product team sends a prompt to the canonical API. The gateway authenticates the caller, loads policy, estimates token demand, and checks both request-per-minute and token-per-minute budgets. If admission succeeds, the prompt passes through PII detection and policy checks.

The router then consults the model registry, capability metadata, routing rules, and current provider health. Before any external call, the cache checks for an exact hit. If no entry exists, the selected provider adapter sends the transformed request. For streaming traffic, the gateway proxies chunks back immediately rather than buffering the full result, while token usage accumulates in parallel.

### Failure and completion path[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Failure-and-completion-path)

If the provider returns a timeout, 5xx, or 429, bounded retries apply only when the request is safe to repeat. Circuit breakers prevent every gateway replica from hammering the same unhealthy dependency. If the primary provider remains unavailable, the router advances to the next eligible provider in the fallback chain. For streaming requests, failover is allowed only before the first token reaches the client. After that, the gateway returns a retryable error instead of splicing in a second provider's output.

> **Note:** Fallback should preserve policy class. A request approved only for private processing must not fail over to a public endpoint.

When the response finishes, actual token counts replace estimates, cost is computed, and usage records are written asynchronously to logs and analytics systems.

The diagram below shows the latency and governance checkpoints along the request path.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271641%27%20height=%271151%27/%3e)![Request workflow sequence](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Request workflow sequence")

Request workflow sequence

The next section checks this request path against the nonfunctional requirements.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Achieving-nonfunctional-requirements)

Nonfunctional requirements are met by reducing synchronous work and isolating mutable state. The gateway should add only a small p99 overhead, so authentication metadata, policy caches, and Redis counters must be low-latency, while analytics writes remain asynchronous.

Scalability comes from stateless replicas behind load balancers. Shared counters, caches, and configuration stores let any replica process any request. Availability improves with multiregion deployment, diversified providers, and health-based failover policies that avoid concentrating all traffic on one backup target. With regional Redis, a team could exceed its quota by spreading traffic across regions, so counters either sync across regions or the system accepts a small, bounded overrun.

Reliability depends on retries with backoff, circuit breakers, and graceful degradation. If a premium model fails, the gateway may route to a cheaper model with lower quality instead of returning a hard failure, assuming policy allows it. Idempotency keys help for nonstreaming operations where replay risk exists.

Security requires encrypted transport, isolated secrets, least-privilege service access, and audit logs that omit raw sensitive content. Common failure modes include inaccurate token estimation, semantic cache contamination across tenants, and gradual provider lock-in through proprietary features.

The diagram below shows how a token reservation is made at admission and reconciled after the response.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271421%27%20height=%27431%27/%3e)![Token reservation and reconciliation](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Token reservation and reconciliation")

Token reservation and reconciliation

The next section covers the trade-offs an interviewer will probe.

## Trade-offs and interview discussion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Trade-offs-and-interview-discussion)

Interviewers usually want to hear where the design bends, not just where it works.

Exact caching is safest for deterministic or low-temperature requests, where identical inputs produce reusable outputs. Semantic caching can save much more money, but it introduces correctness risk, especially when prompts depend on hidden tenant context or time-sensitive data.

Aggressive fallback improves availability but can reduce behavioral consistency. Two providers with similar capability tags may still differ in formatting, reasoning style, tool use, or refusal behavior. That is acceptable for some chat workloads and unacceptable for others.

> **Attention:** A centralized gateway simplifies governance but also creates a critical-path dependency. Treat it like core infrastructure, not middleware that can be casually overloaded.

Rich observability adds hot-path overhead unless telemetry is buffered and shipped asynchronously. Hard budgets protect finance but can block important workloads unexpectedly, while soft budgets preserve productivity but allow spend overruns.

A strong answer estimates scale, separates the control plane from the data plane, explains routing and guardrails, and names failure modes such as retry storms, cache misscoping, and PII leakage.

Test your understanding of the gateway trade-offs with the questions below.

Knowledge Check

Q1. A streaming response fails after 200 tokens have already reached the client. What should the gateway do?

Do you find this helpful?

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Conclusion)

A GenAI gateway is an operational control point, not just an API wrapper. It centralizes authentication, token-aware admission, safety checks, routing, fallback, caching, and usage attribution behind one canonical interface.

The design process followed the usual interview arc: define requirements, estimate scale, draw the high-level architecture, drill into core components, walk through the request life cycle, and close with nonfunctional trade-offs.

Design a Compliance-Constrained Generation System

Design a GPU Training Job Scheduler

Ask

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Resource-estimation)

[System design of a GenAI gateway](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#System-design-of-a-GenAI-gateway)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#High-level-design)

[Data plane components](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Data-plane-components)

[Control plane and state](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Control-plane-and-state)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Achieving-functional-requirements)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#A-detailed-system-design)

[Admission and policy path](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Admission-and-policy-path)

[Identity and access checks](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Identity-and-access-checks)

[Token-aware throttling](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Token-aware-throttling)

[Transformation and execution path](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Transformation-and-execution-path)

[Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Putting-everything-together)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Workflow-of-the-system)

[Normal request path](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Normal-request-path)

[Failure and completion path](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Failure-and-completion-path)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Achieving-nonfunctional-requirements)

[Trade-offs and interview discussion](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Trade-offs-and-interview-discussion)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-a-genai-gateway#Conclusion)