# Inference_Engine_Requirements_for_Efficient_GenAI_Model_Serving

Source: https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Requirements for an Inference Engine

Explore the essential requirements for designing an inference engine in generative AI systems. Learn how to handle latency and throughput SLOs, GPU memory constraints, stateful execution, and distributed parallelism to build scalable model serving architectures that meet operational and user experience goals.

We'll cover the following...

- [Why inference requirements matter](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Why-inference-requirements-matter)
- [What the serving tier must guarantee](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#What-the-serving-tier-must-guarantee)
  - [Reading the latency targets](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Reading-the-latency-targets)
  - [Matching SLOs to workload shape](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Matching-SLOs-to-workload-shape)
- [Why LLM serving is not web serving](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Why-LLM-serving-is-not-web-serving)
  - [How the KV cache consumes memory](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#How-the-KV-cache-consumes-memory)
  - [Architectural consequences](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Architectural-consequences)
- [Hardware and deployment choices](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Hardware-and-deployment-choices)
  - [Distributing models across GPUs](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Distributing-models-across-GPUs)
- [The inference engine components](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#The-inference-engine-components)
  - [Continuous batching](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Continuous-batching)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Conclusion)

In enterprise System Design, model serving is the operational bridge where assembled prompts turn into live output streams. Traditional web microservices scale horizontally by adding stateless containers that handle independent, millisecond requests. In contrast, LLM serving is stateful, hardware-constrained, and memory-bandwidth bound.

Deploying generative models in production requires managing prefill and decode, allocating GPU memory for the KV cache, and scheduling requests to improve hardware utilization. This lesson explores inference performance, continuous batching, latency SLOs, and distributed model parallelism, along with the trade-offs each introduces.

## Why inference requirements matter[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Why-inference-requirements-matter)

In an interview, requirements are the fastest way to turn a vague “design an LLM serving system” problem statement into an architecture discussion with measurable targets. In production, the same requirements govern admission control, hardware sizing, and pricing. The request path begins when a client submits a prompt and ends only after streamed tokens arrive with a cadence users can tolerate.

Two latency metrics dominate interactive systems. **TTFT** measures time to first token, which is the delay between request acceptance and the first visible output. **TPOT** measures time per output token, which is the steady-state speed of generation after streaming starts. A response with acceptable total runtime can still feel bad if TTFT is high or if token cadence stutters.

**Note:** Average latency hides the user experience. A chat product usually fails at the tail, not at the mean.

The serving tier must also satisfy broader constraints during that same life cycle.

- **Throughput:** The system must sustain enough aggregate token generation under peak load.
- **Availability:** The service must continue routing and streaming despite worker failures or overload.
- **Cost per token:** The architecture must keep serving economics within product limits.

These requirements now split naturally into what the system must do functionally and what it must guarantee operationally.

## What the serving tier must guarantee[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#What-the-serving-tier-must-guarantee)

The serving tier starts with user-visible behaviors, then layers operational SLOs underneath them. In practice, the request enters a router, is mapped to a model and policy, waits in a scheduler, executes on a worker, and streams tokens back while carrying request state. Each of those stages exists to preserve explicit guarantees.

The functional guarantees usually include the following capabilities.

- **Streaming generation:** The engine should emit tokens as soon as they are decoded instead of buffering the full answer, so the client can render progressive output over SSE or WebSockets.
- **Multiple-model support:** The router should direct requests among general-purpose, smaller, or task-specific models based on task type, tenant policy, latency tier, or budget.
- **Model versioning:** The platform should expose explicit model revisions so staged rollout, rollback, A/B experiments, and customer-specific variants can coexist safely.
- **Multitenancy and prioritization:** The system should enforce quotas, rate limits, and priority classes so one tenant or free tier does not starve premium traffic.

The nonfunctional requirements define the operational targets the serving tier must meet, including latency, throughput, availability, scalability, cost efficiency, and resource utilization.

### Reading the latency targets[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Reading-the-latency-targets)

A simple way to reason about interactive performance is to split latency into startup delay and token cadence.

- **TTFT in the request path:** TTFT includes queue wait, prompt tokenization, prompt processing, and the first decode step. It dominates how quickly the system feels responsive.
- **TPOT in the streaming path:** TPOT captures the interval between streamed tokens after generation begins. It dominates whether output appears smooth or jerky.

### Matching SLOs to workload shape[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Matching-SLOs-to-workload-shape)

The same engine can support very different products, but the metric emphasis changes by workload.

- **Chat workloads:** The design usually prioritizes low TTFT and stable TPOT because users react strongly to startup delay and uneven streaming.
- **Offline summarization:** The design usually prioritizes throughput and cost per token because the system can batch aggressively and interactive feel matters less.
- **Mixed-tenant platforms:** The design usually prioritizes percentile SLO isolation so premium traffic stays within target even when free-tier queues build up.

**Attention:** High throughput alone is not success if many requests miss latency SLOs. Systems need goodput, meaning useful throughput that still meets targets.

Larger batches often improve throughput but can worsen TTFT, which shows why these guarantees are hard. The root cause is that LLM serving is not equivalent to ordinary stateless request handling.

## Why LLM serving is not web serving[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Why-LLM-serving-is-not-web-serving)

Traditional web servers typically handle independent requests with relatively predictable resource requirements. LLM serving is different because each request can generate a variable number of tokens while occupying GPU memory throughout generation. The inference engine must manage both computation and the state maintained for active requests.

Each request moves through two execution phases:

- Prefill phase
- Decode phase

The lesson, *Latency, Throughput, and Cost*, explains these phases, along with TTFT, TPOT, and their performance trade-offs. Here, we focus on the serving mechanisms that manage inference workloads efficiently.

Three characteristics make LLM serving particularly challenging:

- **Dynamic memory usage:** The KV cache grows as tokens are processed and generated, increasing memory demand for longer sequences.
- **Variable request duration:** Requests produce different amounts of output, making fixed batching inefficient when some sequences finish earlier than others.
- **Hardware constraints:** Model weights, KV caches, and intermediate computations compete for limited GPU memory and compute capacity.

These constraints make request scheduling, KV-cache allocation, and GPU utilization central to inference engine design.

### How the KV cache consumes memory[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#How-the-KV-cache-consumes-memory)

During prefill, the model computes key and value tensors for the prompt tokens and stores them in the KV cache. During decode, it reuses these cached tensors instead of recomputing attention states for the entire preceding sequence at every step. The cache grows as new tokens are generated.

This reduces repeated computation, but introduces a memory trade-off. Each active request occupies GPU memory for its KV cache, and longer sequences consume more memory. As concurrency increases, these caches compete with model weights and other runtime allocations for limited GPU memory.

The cache size depends on the number of layers, attention heads, head dimensions, cached tokens, and numerical precision. For a fixed model configuration, cache memory grows approximately linearly with the number of cached tokens.

Production engines manage this pressure through techniques such as paged KV-cache allocation, cache eviction, and limits on active sequences. These controls help prevent memory exhaustion while preserving enough capacity to serve concurrent requests. Because the request remains attached to its cache, serving becomes stateful.

### Architectural consequences[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Architectural-consequences)

Those execution phases change routing, load balancing, and scheduling.

- **GPU-bound execution:** The hot path sits on accelerators, not on commodity CPU app servers, so autoscaling web containers does not remove the true bottleneck.
- **Sticky request state:** Once a request has built KV cache on a worker, moving it elsewhere is expensive, which weakens stateless load-balancing assumptions.
- **Highly variable request cost:** A long prompt or long answer can consume much more compute and memory than a short exchange, making queue times unpredictable.

One useful analogy is a restaurant kitchen. A stateless web server is like a cashier who can hand any order to any free clerk. An LLM worker is more like a chef who has already laid out ingredients for a specific dish. Switching stations mid-cook wastes setup and slows everyone.

The visual contrast below should make the statefulness difference immediate.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271221%27%20height=%27650.7%27/%3e)![Why model serving needs sticky GPU workers](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Why model serving needs sticky GPU workers")

Why model serving needs sticky GPU workers

Once state, memory, and variability enter the request path, hardware and deployment choices become part of the architecture rather than an implementation footnote.

## Hardware and deployment choices[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Hardware-and-deployment-choices)

The hardware discussion starts from a simple fact. The model worker must fit weights and active request state in memory, then read that state fast enough to sustain target token speed. That is why accelerator choice is usually driven by memory capacity and bandwidth before peak FLOPS.

A high-level comparison makes the trade-offs concrete.

- **CPUs:** They fit smaller models and low-throughput or offline workloads, but they usually miss interactive TTFT and TPOT targets for modern LLM products.
- **GPUs:** They are the common default because they combine strong parallel compute with high-bandwidth memory, which decode-heavy serving depends on.
- **TPUs and other accelerators:** They can provide strong efficiency in managed environments, but model support, toolchains, and deployment flexibility may be narrower.

**Practical tip:** For interactive chat, ask first whether the target hardware can hold weights plus expected KV cache at concurrency, then ask whether bandwidth can sustain TPOT.

Memory capacity determines whether the worker can host the model and active caches. Memory bandwidth influences token generation speed because decode repeatedly touches weights and cache for every output token. For long-context systems, cache growth can reduce concurrency even when the model itself fits.

A platform team usually chooses between buying inference as a service and operating the engine directly.

- **Hosted API path:** Hosted APIs reduce operational burden, speed initial launch, and shift hardware management to the provider. The trade-off is reduced control over scheduling policy, model versions, custom routing, and unit-cost tuning.
- **Self-hosted path:** Self-hosted serving provides control over versions, accelerator pools, routing logic, and tenant isolation. The trade-off is owning capacity planning, failover, upgrades, observability, and GPU utilization.

Whichever deployment path is chosen, the same guarantees still need concrete software components to enforce them.

### Distributing models across GPUs[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Distributing-models-across-GPUs)

Large models may exceed the memory capacity of a single GPU or require more compute to meet serving targets. Model parallelism distributes model execution across multiple GPUs so they can cooperate to process each request.

Two common approaches are:

- **Tensor parallelism:** Splits individual layer computations across GPUs.
- **Pipeline parallelism:** Places different groups of model layers on different GPUs.

We'll address parallelism and its types in detail in the lesson “Parallelism in GenAI Models”

Distributed execution allows larger models to run across multiple accelerators, but it introduces communication overhead, coordination requirements, and additional failure modes. The design must balance model capacity and throughput against interconnect bandwidth, latency, and infrastructure cost.

## The inference engine components[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#The-inference-engine-components)

An inference engine is easiest to read as a request pipeline. A client request enters with a prompt, target model, tenant identity, and streaming preference. The system then selects a pool, schedules work under latency and memory constraints, executes prefill and decode on model workers, and reuses or evicts cache based on locality and pressure.

The main components usually break down as follows.

- **Router:** The router acts as the entry point that selects model, version, tenant policy, and often the serving pool based on request metadata and capacity signals.
- **Scheduler:** The scheduler decides queueing, batching, admission, and priority under memory and latency constraints, which is where SLO enforcement often begins.
- **Tokenizer:** Converts input text into tokens before inference and converts generated tokens back into text.
- **Model workers:** The workers are accelerator-bound processes that run prefill and decode, maintain per-request state, and stream tokens back to the client.
- **Streaming layer:** Delivers generated output incrementally through protocols such as SSE or WebSockets.
- **Cache subsystem:** The cache manages reusable state, including per-request KV cache and sometimes shared prompt prefixes that eliminate repeated prefill work.
- **Worker health and failover:** Health checks detect failed workers, and the router redirects new requests to healthy workers. In-flight streams may terminate if their KV cache is lost, requiring a retry that restarts generation from the prompt.
- **Autoscaler:** Adds or removes serving capacity based on demand, queue depth, and resource utilization, while accounting for model loading time and GPU availability.

**Note:** A shared prefix cache differs from per-request KV cache, which continues growing during generation.

Requests with the same prefix are often routed with cache locality in mind. That choice reduces repeated prompt computation, but long-lived cache entries can also crowd out fresh requests if eviction is weak.

The following diagram narrows the focus from the whole serving stack to the engine internals where latency usually accumulates.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27871%27%20height=%27541%27/%3e)![Request flow through inference engine internals](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Request flow through inference engine internals")

Request flow through inference engine internals

### Continuous batching[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Continuous-batching)

A fixed batch waits for its requests to finish together, even when some requests complete much earlier than others. This can leave GPU capacity underused because LLM requests generate different numbers of tokens.

Continuous batching addresses this problem by allowing the scheduler to add new requests to an active batch as other requests finish. Instead of waiting for the entire batch to complete, the engine repeatedly adjusts which sequences participate in each generation step.

For example, if three requests generate 20, 80, and 150 tokens, the first request can leave the batch after 20 tokens. The scheduler can admit another request without waiting for the remaining two to finish.

Continuous batching improves GPU utilization and throughput under variable workloads. However, the scheduler must account for KV-cache memory, request priorities, and latency SLOs when admitting new sequences. Aggressive batching can improve throughput while increasing queueing delay or harming TPOT.

AI Powered

Saved

1 attempt left

Reset

LLM serving bottlenecks and performance optimization

A company’s AI chat assistant experiences slow responses and inconsistent token streaming despite adding more web servers. The bottleneck is traced to overloaded GPU workers. How should the team redesign its LLM serving system to improve latency, throughput, and cost efficiency?

This is your last attempt.

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Conclusion)

A strong interview answer defines the inference engine's guarantees first, then chooses an architecture that can enforce them under load. Identify the key metrics, account for stateful GPU execution, and connect hardware and software choices to user experience and cost. The next lesson explores how techniques such as quantization, caching, and speculative decoding optimize inference performance while balancing latency, throughput, and cost.

Context Assembly and Prompt Management

Inference Optimization in GenAI Systems

Ask

[Why inference requirements matter](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Why-inference-requirements-matter)

[What the serving tier must guarantee](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#What-the-serving-tier-must-guarantee)

[Reading the latency targets](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Reading-the-latency-targets)

[Matching SLOs to workload shape](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Matching-SLOs-to-workload-shape)

[Why LLM serving is not web serving](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Why-LLM-serving-is-not-web-serving)

[How the KV cache consumes memory](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#How-the-KV-cache-consumes-memory)

[Architectural consequences](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Architectural-consequences)

[Hardware and deployment choices](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Hardware-and-deployment-choices)

[Distributing models across GPUs](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Distributing-models-across-GPUs)

[The inference engine components](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#The-inference-engine-components)

[Continuous batching](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Continuous-batching)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/requirements-for-an-inference-engine#Conclusion)