# Designing_an_AI_Code_Assistant_for_Real-Time_Developer_Support

Source: https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Grokking the Generative AI System Design Interview](https://www.educative.io/courses/generative-ai-system-design)

# Design an AI Code Assistant

Design an AI code assistant that streams context-aware completions from regional GPU clusters in under 300 ms, with caching, graceful degradation, and an async feedback loop.

We'll cover the following...

- [What is a code assistant?](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#What-is-a-code-assistant)
- [System requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#System-requirements)
  - [Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Functional-requirements)
  - [Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Nonfunctional-requirements)
- [Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Resource-estimation)
  - [Estimating the number of servers](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Estimating-the-number-of-servers)
  - [Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Storage-estimation)
  - [Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Bandwidth-estimation)
- [System design of an AI code assistant](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#System-design-of-an-AI-code-assistant)
  - [Building blocks](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Building-blocks)
  - [High-level design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#High-level-design)
  - [API design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#API-design)
  - [Storage schema](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Storage-schema)
  - [Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Achieving-functional-requirements)
- [A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#A-detailed-system-design)
  - [Inference path](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Inference-path)
  - [Telemetry path](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Telemetry-path)
  - [Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Putting-everything-together)
- [Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Workflow-of-the-system)
- [Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Achieving-nonfunctional-requirements)
- [Evaluation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Evaluation)
- [Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Conclusion)

Developers spend a significant portion of their time on repetitive tasks such as writing boilerplate code, navigating documentation, and fixing minor syntax errors. These tasks are frequent but low-cognitive-value, which makes them ideal candidates for automation. **AI-powered code assistants** attempt to reduce this friction by embedding large language model (LLM) inference directly into the developer’s IDE and generating suggestions in real time as code is written.

Industry reports and developer surveys indicate that AI-assisted coding improves perceived productivity, while controlled studies report mixed results in actual task-completion time.

This tension frames a real design constraint. This lesson focuses on understanding the problem space, defining requirements, and estimating resources to prepare for the full system architecture in the next lesson.

## What is a code assistant?[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#What-is-a-code-assistant)

A **code assistant**, often called Copilot, is an AI-powered tool embedded in a developer’s IDE (Integrated Development Environment) that provides real-time code suggestions, completions, and generation based on natural language prompts and surrounding code context.

The core capabilities of a modern code assistant span several categories:

- **Inline code completion:** The system predicts and suggests the next few tokens or lines as the developer types.
- **Multi-line function generation:** Given a function signature or partial implementation, the system generates a complete function body.
- **Natural language to code translation:** A developer writes a comment like `// sort array in descending order`, and the system produces the corresponding code.
- **Code editing and refactoring:** The system can modify existing code blocks, for example, rewriting a loop for efficiency or converting synchronous code into asynchronous patterns.
- **Code explanation and documentation:** The system can describe what a selected code block does in plain English.
- **Context-aware suggestions:** Completions are informed by the current file, open tabs, imported modules, project structure, and other signals that are assembled into a structured context window before being sent to the LLM.

![An example of an AI code assistant](images/img_b1ff5447d85b.svg "An example of an AI code assistant")

An example of an AI code assistant

Unlike traditional autocomplete systems that rely on symbol tables and static analysis, Copilot uses deep learning models trained on vast code corpora to predict semantically meaningful code blocks. To provide context-aware suggestions, the system uses a *context extractor* within the IDE to truncate and rank relevant snippets (for example, using Jaccard similarity or BM25) before sending them to the LLM. Sending entire files would exceed context windows and increase latency.

Because this system must support millions of concurrent developers, it becomes a distributed systems problem that requires low-latency inference, high availability, and effective context management. Given this workflow, the next step is to define the system’s functional and nonfunctional requirements.

## System requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#System-requirements)

Clearly scoping requirements (functional and nonfunctional) is one of the most critical steps in any system design interview. These will inform both the resource estimation later in this lesson and the architectural choices explored in the next lesson.

### Functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Functional-requirements)

The functional requirements define what the code assistant must do from the user’s perspective.

- **Real-time code completion:** The system should generate and return code suggestions within a strict latency budget of under 300 ms as the developer types, ensuring that suggestions arrive before the developer’s attention moves on.
- **Context-aware suggestions:** The system must accept and process contextual signals, including current file content, cursor position, open files, project structure, and programming language, to produce relevant completions rather than generic ones.
- **Multi-language support:** The system should support popular programming languages such as Python, JavaScript, TypeScript, Java, Go, and C++, requiring the underlying model to handle diverse syntax and semantics.
- **Natural language to code:** The system should translate developer comments or prompts written in natural language into functional code snippets, requiring an instruction-tuned LLM.
- **Code explanation and documentation:** The system should explain selected code blocks in natural language, helping developers understand unfamiliar codebases.
- **Streaming responses:** For longer generations, the system should support streaming tokens back to the IDE incrementally using mechanisms such as server-sent events (SSE), WebSockets, or streaming APIs.
- **User feedback loop:** The system should capture accept/reject signals from developers to build a telemetry pipeline for model fine-tuning over time.

The following table summarizes these requirements alongside their design implications.

|  |  |  |  |
| --- | --- | --- | --- |
| **Requirement** | **Description** | **Example** | **Design Implication** |
| Real-time code completion | Generate suggestions under 300ms | The developer types a function signature and gets the body | Requires low-latency inference and caching |
| Context-aware suggestions | Process file and project context | Uses imports and variable names to tailor output | Needs a context preprocessing pipeline |
| Multi-language support | Handle 10+ programming languages | Python, JS, Go, Java | The model must be trained on multilingual corpora |
| Natural language to code | Convert comments to code | "// sort array in descending order" generates sorting logic | Requires instruction-tuned LLM |
| Streaming responses | Incremental token delivery | Long function generation streams line by line | Needs server-sent events or WebSocket support |
| User feedback loop | Capture accept/reject signals | The developer dismisses a suggestion | Telemetry pipeline for model fine-tuning |

These functional requirements tell us what the system does. Equally important is defining how well it must perform under real-world conditions.

### Nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Nonfunctional-requirements)

Nonfunctional requirements define the quality attributes that determine whether the system is viable at production scale.

- **Low latency:** Developers typically type 40–80 words per minute, which means that suggestions must appear within a few hundred milliseconds (time to first token, or TTFT) to remain relevant before the user continues typing.
- **High availability:** The system should target 99.9%+ uptime because developers rely on it continuously during active coding sessions. Downtime directly disrupts productivity.
- **Scalability:** The system must scale horizontally to handle millions of concurrent developers across global regions, with traffic patterns that spike during business hours in different time zones.
- **Fault tolerance:** Failures in the inference layer should degrade gracefully by returning no suggestion rather than crashing the IDE plugin or displaying error messages.
- **Security and privacy:** Code context sent to the backend may contain proprietary source code. Data must be encrypted in transit using TLS and at rest, with options for enterprise customers to restrict data retention entirely.

  - **Safety and compliance:** Generated code should pass security and license checks to avoid introducing vulnerabilities or incompatible code into repositories.
- **Suggestion relevance:** Generated code should be syntactically valid and contextually relevant to minimize developer correction effort.
- **Cost efficiency:** LLM inference is GPU-intensive, so the system must optimize compute costs through techniques like model quantization, response caching, and batched inference.

> **Note:** AWS research identifies a review and QA bottleneck in which AI-generated code increases output volume faster than teams can review and validate it. This quality-assurance concern is a real nonfunctional consideration that affects how the system’s success is measured beyond raw throughput.

![Functional and non-functional requirements of an LLM-powered code assistant](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Functional and non-functional requirements of an LLM-powered code assistant")

Functional and non-functional requirements of an LLM-powered code assistant

The following quiz tests your understanding of how these nonfunctional requirements translate into system behavior.

Lesson Quiz

1.

A code assistant must return inline suggestions within a strict latency budget. If the inference service experiences a transient failure, what is the most appropriate system behavior?

A.

Return an error message in the IDE editor.

B.

Retry the request up to 3 times with exponential backoff before timing out.

C.

Degrade by showing no suggestion and logging the failure for monitoring.

D.

Queue the request and deliver the suggestion when the service recovers.

---

1 / 1

With requirements defined, we can now estimate the resources needed to operate this system at scale.

## Resource estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Resource-estimation)

Resource estimation translates requirements into concrete infrastructure numbers. This is where system design moves from abstract to actionable.

The estimation begins with these assumptions:

- Five million active developers
- 50 requests per developer per active hour
- Four active coding hours per day
- Users are distributed across five major global regions

Total daily requests come to:5M×50×4=1,000,000,000≈1 Billion requests per day.5M×50×4=1,000,000,000 ≈ 1\ Billion\ requests\ per\ day.5M×50×4=1,000,000,000≈1 Billion requests per day.

### Estimating the number of servers[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Estimating-the-number-of-servers)

We estimate servers for peak traffic, and we assume that all users are active and making requests, which results in five million requests per second. We’ll use the following formula to calculate the number of servers:

Servers needed at peak load=Number of requests/secondRPS of the server\text{ Servers needed at peak load} = \frac{\text{Number of requests/second}}{\text{RPS of the server}} Servers needed at peak load=RPS of the serverNumber of requests/second​

Using 64,000 as the estimated RPS a server can handle from the [back-of-the-envelope calculation](https://www.educative.io/courses/grokking-the-system-design-interview/put-back-of-the-envelope-numbers-in-perspective) section, we’ll calculate the required number of servers as follows:

Servers needed at peak load=5 million64,000≈79 servers\text{Servers\ needed\ at\ peak\ load} = \frac{5\ million}{64,000} \approx \text{79 servers}Servers needed at peak load=64,0005 million​≈79 servers

#### Servers Required

|  |  |  |
| --- | --- | --- |
| Daily Active Users (DAUs) | 5 | million |
| RPS of a server | 64000 | RPS |
| Total servers required | f79 | servers |

The above estimate is for application servers. Because the LLM’s suggestions rely heavily on GPU servers for fast inference, it’s crucial to factor them in. If a single GPU server handles approximately 200 inference requests per second, then at peak, the system needs roughly 5 million200≈25 K\frac{5\ million}{200} \approx 25\ K2005 million​≈25 K GPU servers, distributed across regions with redundancy.

![The number of estimated servers](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The number of estimated servers")

The number of estimated servers

> **Note:** Caching frequently requested completions and applying model quantization can reduce the GPU server count by 30–40%, which translates directly into significant cost savings at this scale. For a quick, accurate estimate of GPU requirements, check out the [back-of-the-envelope calculations](https://www.educative.io/courses/generative-ai-system-design/estimating-training-compute-and-cost).

### Storage estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Storage-estimation)

If each request-response pair generates about4 KB4\ KB4 KB of telemetry, then at one billion requests per day, the system produces roughly4 TB4\ TB4 TB of telemetry data per day.

1,000,000,000×4 KB=4,000,000,000 KB≈4 TB/day1{,}000{,}000{,}000 \times 4 \text{ KB} = 4{,}000{,}000{,}000 \text{ KB} \approx 4\ TB/day1,000,000,000×4 KB=4,000,000,000 KB≈4 TB/day

Below is a calculator to help us estimate the required resources.

#### Storage required for text-based requests on ChatGPT

|  |  |  |
| --- | --- | --- |
| Daily Active Users | 5 | million |
| Average Daily Requests per User | 200 | requests/user |
| Total Daily Requests | f1000 | million |
| Request size | 4 | KB |
| Total Storage per day | f4 | TB |

### Bandwidth estimation[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Bandwidth-estimation)

Assuming a 3 KB request size and a 1 KB response size, based on the assumptions made in the storage estimation section, we can estimate the incoming and outgoing bandwidth requirements as follows:

Incoming bandwidth is calculated as follows:

Incoming bandwidth =Total requests×Single request size=5 M/s×3 KB=15 GBps\begin{align\*}
\text{Incoming bandwidth } &= \text{Total requests} \times \text{Single request size} \\
&= 5 \text{ M/s} \times 3 \text{ KB} \\
&= 15 \text{ GBps}
\end{align\*}Incoming bandwidth ​=Total requests×Single request size=5 M/s×3 KB=15 GBps​

Outgoing bandwidth is calculated as follows:

Outgoing bandwidth =Total requests×Single request size=5 M/s×1 KB=5 GBps\begin{align\*}
\text{Outgoing bandwidth } &= \text{Total requests} \times \text{Single request size} \\
&= 5 \text{ M/s} \times 1 \text{ KB} \\
&= 5 \text{ GBps}
\end{align\*}Outgoing bandwidth ​=Total requests×Single request size=5 M/s×1 KB=5 GBps​

#### Incoming and Outgoing Bandwidth Requirement

|  |  |  |
| --- | --- | --- |
| Daily Active Users (DAUs) | 5 | million |
| Average daily requests per user per second | 1 | requests/user |
| Total daily requests | f5 | million |
| Request size | 3 | KB |
| Response size | 1 | KB |
| Incoming bandwidth | f15 | GBps |
| Outgoing bandwidth | f5 | GBps |

![Total bandwidth required for an AI code assistant](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Total bandwidth required for an AI code assistant")

Total bandwidth required for an AI code assistant

These estimates establish the infrastructure baseline. The next step is identifying the distributed system building blocks that will form the architecture.

## System design of an AI code assistant[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#System-design-of-an-AI-code-assistant)

Let's start with the building blocks this design relies on, then move to the high-level design.

### Building blocks[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Building-blocks)

Designing a code assistant at this scale requires composing several well-known distributed system components. The building blocks that will form the architecture in the next lesson include the following:

- **Load balancers** distribute inference requests across GPU server clusters and handle regional traffic routing.
- **Blob storage** reliably stores and versions model weights and training artifacts.
- **Key-value stores** such as Redis cache frequent completions and session context, reducing redundant inference calls.
- **Vector databases** or embedding stores retrieve semantically relevant code snippets from the repository to enrich the model context.
- **CDNs and edge nodes** minimize latency by serving cached responses closer to developers in each region.
- **Pub-sub systems or message queues** handle asynchronous telemetry ingestion for accept/reject signals and usage logs without blocking the inference path.
- **Monitoring services** track inference latency, error rates, GPU utilization, and model quality metrics such as suggestion acceptance rate.

![Building blocks required to design a system for an LLM-powered code assistant](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Building blocks required to design a system for an LLM-powered code assistant")

Building blocks required to design a system for an LLM-powered code assistant

> **Note:** None of these components is unique to AI systems. The challenge lies in how these components are composed to meet strict latency, availability, and cost constraints for real-time LLM inference workloads.

These building blocks will be assembled into a complete system architecture in the next lesson. Before moving on, let's test our ability to apply the concepts from this lesson to a realistic design scenario.

AI Powered

Saved

12 attempts left

Reset

AI Code Assistant Design Challenge

Hi, I'm Ed! Let's work through this design challenge together. You are a system design engineer at a company planning to launch an AI code assistant for 2 million internal developers across 3 global regions. The company's primary concerns are keeping inline suggestion latency under 200ms, ensuring code privacy since developers work on proprietary codebases, and managing GPU infrastructure costs. Identify which functional and non-functional requirements from this lesson are most critical given these constraints and explain why?

You have 12 attempts to answer.

Next, we translate these requirements and estimates into a concrete system architecture.

We will walk through the high-level architecture, define the API contracts between the IDE plugin and backend services, lay out the storage schema for caching and telemetry, and then dive into the detailed component interactions for both the inference and telemetry paths. We then validate the full system architecture against the previously defined requirements to ensure that they are all covered.

### High-level design[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#High-level-design)

The high-level workflow is as follows: A developer enters code or a comment. The IDE plugin captures the context, including the cursor position, open files, and language metadata. The IDE plugin sends a request through an API gateway that handles authentication, rate limiting, and routing before forwarding it to the orchestration service. The backend orchestration service preprocesses context, applies safety filters, and routes the request to an LLM inference cluster. The model generates candidate completions, and the results return to the IDE with minimal latency.

The following diagram illustrates this end-to-end request flow, from the developer’s keystroke to the rendered suggestion.

![Code assistant request lifecycle showing the complete round-trip from the IDE to the inference service](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Code assistant request lifecycle showing the complete round-trip from the IDE to the inference service")

Code assistant request lifecycle showing the complete round-trip from the IDE to the inference service

Regional deployment is essential. Load balancers distribute traffic across GPU clusters deployed in multiple geographic regions, keeping requests close to developers and meeting both latency and availability targets. The cache layer can reduce GPU load for repeated prompt hashes from identical or highly similar contexts. Even modest cache hit rates (for example, 10–20%) can significantly reduce GPU inference load at scale.

> **Note:** The cache hit rate directly impacts cost efficiency. Even a five percent improvement in cache hits can eliminate thousands of GPU-hours per month at scale.

With the high-level architecture established, we can now define the precise contracts that the IDE plugin uses to communicate with these backend services.

### API design[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#API-design)

The API layer acts as the contract between the IDE plugin and backend services, mapping developer actions to system operations. The following APIs define the system’s external interface:

- `getCompletion` is a POST endpoint that returns a stream of suggested tokens along with a `completion_id`, delivered via server-sent events (SSE). This streaming approach helps ensure that the first token arrives within the 300 ms budget, even though full generation may take longer.

Ace Editor

1

getCompletion(session\_id, file\_content, cursor\_position, language, open\_files)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `session_id` | Unique identifier for the developer session |
| `file_content` | Current file content is being edited |
| `cursor_position` | Current cursor location in the file |
| `language` | Programming language of the file |
| `open_files` | Additional open files used for context |

- `submitFeedback` is a POST endpoint that uses a fire-and-forget pattern from the client’s perspective and routes messages through the pub-sub system so the IDE is not blocked waiting for a write acknowledgment.

Ace Editor

1

submitFeedback(completion\_id, action, session\_id)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `completion_id` | Unique identifier for the generated suggestion |
| `action` | Developer action (accepted, rejected, modified) |
| `session_id` | Session identifier for correlating feedback |

- `explainCode` is a POST endpoint that accepts a code block, language, and `session_id`, returning a streamed natural-language explanation of the selected code. It uses the same inference infrastructure to generate explanations for selected code blocks.

Ace Editor

1

explainCode(code\_block, language, session\_id)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

|  |  |
| --- | --- |
| **Parameter** | **Description** |
| `code_block` | Selected code snippet to explain |
| `language` | Programming language of the code |
| `session_id` | Session identifier |

- `getStatus` is a GET endpoint that returns a synchronous health check, allowing the IDE plugin to verify backend availability before sending inference requests.

Ace Editor

1

getStatus()

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

> **Practical tip:** Adding a client-side debounce of 150–200 ms before calling `getCompletion` prevents excessive requests on every keystroke and reduces backend load.

The table below summarizes these APIs and their key characteristics.

## API Endpoints Overview

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **API Endpoint** | **Method** | **Key Parameters** | **Response Type** | **Purpose** | **Notes** |
| `getCompletion` | POST | `context`, `cursor_position`, `language`, `file_content`, `open_files`, `session_id` | Streaming (SSE) | Generate code suggestions | Sub-300ms time-to-first-token target |
| `submitFeedback` | POST | `completion_id`, `action`, `session_id` | Async fire-and-forget | Capture user acceptance signals | Routed through pub-sub to avoid blocking the IDE |
| `explainCode` | POST | `code_block`, `language`, `session_id` | Streaming (SSE) | Explain the selected code in natural language | Uses the same inference cluster with an instruction-tuned prompt |
| `getStatus` | GET | None | Sync | Health check for backend availability | Called before inference requests to enable client-side fallback |

Now that the API contracts are defined, we need to design the storage layer that supports caching, telemetry ingestion, and model management.

### Storage schema[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Storage-schema)

The storage layer is shaped directly by the APIs and the two data flows described above. Four distinct schemas serve different parts of the system.

- **Completion cache (Redis)** stores a hashed representation of the assembled prompt as the key, mapped to the generated completion text, a TTL for automatic expiration, and metadata such as language and model version. The TTL ensures that stale suggestions are evicted as code context evolves. Consistent hashing distributes entries across Redis nodes to avoid hotspots.
- **Telemetry events (columnar store** (such as ClickHouse, BigQuery, or Snowflake)**)** capture each feedback signal with fields for `completion_id`, `session_id`, `timestamp`, action (accepted, rejected, or modified), language, and latency metrics. This store ingests approximately 4 TB per day based on previous estimates and must support efficient batch reads for model fine-tuning pipelines.
- **Model registry (blob storage)** tracks each model artifact with `model_version`, `upload_timestamp`, quantization level, `file_path`, and `deployment_status`. This registry enables safe rollouts and rollbacks of model versions.
- **Session context (ephemeral store)** holds minimal session metadata used for request correlation and rate limiting.

> **Note:** Setting TTLs too low can significantly reduce the cache hit rate, while setting them too high can result in outdated suggestions being served. Benchmark against real usage patterns to determine the optimal balance.

The following quiz tests your understanding of the storage and API design decisions covered so far.

Lesson Quiz

1.

Why does the submitFeedback API use an asynchronous fire-and-forget pattern delivery through a pub-sub system rather than synchronous writes?

A.

To reduce storage costs

B.

To avoid blocking the developer's IDE experience and the inference path

C.

Because feedback data is not important

D.

To encrypt the data in transit

---

1 / 2

### Achieving functional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Achieving-functional-requirements)

To ensure that the proposed architecture satisfies the system goals defined earlier, we map each requirement to the architectural components responsible for implementing it. This verification step confirms that every functional capability and operational constraint is explicitly supported by the design.

|  |  |  |
| --- | --- | --- |
| **Functional Requirement** | **Architectural Component** | **How the Architecture Satisfies It** |
| Real-time code completion | GPU inference cluster + streaming API | The inference service generates suggestions and streams tokens to the IDE, ensuring the first token arrives within the sub-300 ms latency target. |
| Context-aware suggestions | Context aggregation service | The orchestration layer assembles prompts using signals such as the current file, cursor position, open tabs, and language metadata before sending them to the model. |
| Multi-language support | Polyglot LLM (or specialized model set) | The inference cluster hosts models trained on diverse programming languages, enabling suggestions across ecosystems like Python, JavaScript, Java, Go, and C++. |
| Natural language to code | Instruction-tuned prompting in inference service | Developer comments are translated into executable code using prompts optimized for instruction-following behavior. |
| Code explanation and documentation | explainCode  API + inference cluster | Selected code blocks are sent to the model with explanation prompts, returning natural-language descriptions to the IDE. |
| Streaming responses | SSE streaming pipeline | Tokens are streamed incrementally using Server-Sent Events, so developers see suggestions immediately while generation continues. |
| User feedback loop | Pub-sub telemetry pipeline | Feedback signals from the IDE are asynchronously published to a message queue and later aggregated for quality monitoring and model improvement. |

With the functional requirements mapped, we can now examine how these components interact in detail during both the inference and telemetry workflows.

## A detailed system design[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#A-detailed-system-design)

The system’s behavior is best understood by tracing two parallel paths: the inference path, which generates suggestions, and the telemetry path, which captures feedback for continuous improvement.

### Inference path[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Inference-path)

When a developer types in the IDE, the plugin sends a request through the API gateway, which handles authentication, rate limiting, and routing. The request is then passed to the context aggregation service, where relevant signals, such as the current file, cursor position, open tabs, and language metadata, are assembled into a prompt. This prompt is truncated to fit within the model’s context window.

To improve relevance, the system may enrich this prompt using a **retrieval layer**, which queries a vector database of repository embeddings and adds semantically related code snippets. This is especially useful for large codebases, where important context may not be present in the currently open files.

Before invoking the model, the orchestration layer performs a cache lookup using a hash of the assembled prompt:

- On a **cache hit**, the stored completion is streamed back immediately.
- On a **cache miss**, the request is forwarded to the inference cluster.

The request then reaches the GPU inference cluster, where a model serving framework such as vLLM performs batched inference. By grouping multiple requests into a single GPU execution and leveraging KV cache optimization, the system improves throughput while keeping latency low.

As soon as generation begins, tokens are streamed back to the IDE using SSE. This reduces time to first token (TTFT), even if full response generation takes longer. Once generation completes, the response is cached for reuse.

The following illustration highlights the real-time flow of the inference layer:

![ Real-time flow from IDE through context processing, caching, and GPU inference to deliver streamed code suggestions](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 " Real-time flow from IDE through context processing, caching, and GPU inference to deliver streamed code suggestions")

Real-time flow from IDE through context processing, caching, and GPU inference to deliver streamed code suggestions

### Telemetry path[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Telemetry-path)

While the inference path is latency-critical, the telemetry path is designed to be fully asynchronous, ensuring that it never impacts the developer experience. When a developer interacts with a suggestion, the IDE sends feedback signals such as accepted, rejected, or modified. These events are published to a message queue (e.g., Kafka), which decouples ingestion from downstream processing. A telemetry consumer service then processes these events and writes them to a columnar data store optimized for large-scale analytical queries.

Over time, aggregation jobs compute key metrics, including:

- Acceptance rates per model version
- Latency distributions
- Performance across languages or repositories

These aggregated signals feed into fine-tuning pipelines, evaluation systems, and monitoring dashboards. Together, these components form a continuous feedback loop that improves model quality and relevance over time without impacting real-time inference performance.

One industry-observed risk is a review and QA bottleneck, where AI-generated code volume outpaces a team’s review capacity and stalls overall delivery speed. The monitoring service must therefore track not just throughput and latency, but also suggestion acceptance rates and downstream code quality metrics to detect this pattern early.

### Putting everything together[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Putting-everything-together)

The following diagram illustrates this complete architecture with all major components and their interactions:

![End-to-end system combining inference, telemetry, and ML pipelines for scalable code generation and continuous improvement](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "End-to-end system combining inference, telemetry, and ML pipelines for scalable code generation and continuous improvement")

End-to-end system combining inference, telemetry, and ML pipelines for scalable code generation and continuous improvement

Supporting this system at scale requires careful infrastructure design. The GPU inference layer uses techniques such as model quantization (e.g., INT8) to reduce memory usage and improve throughput where supported. Auto-scaling policies dynamically adjust GPU capacity based on regional traffic patterns.

From a reliability perspective, the system follows a graceful degradation model:

- If inference fails or exceeds latency thresholds, the system returns no suggestion instead of an error.
- Cached responses provide a partial fallback for frequently seen requests.

This ensures that even under failure conditions, the IDE remains responsive, and the developer workflow is not disrupted. Next, let's follow a single request through this design step by step.

## Workflow of the system[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Workflow-of-the-system)

Let's trace one completion request end to end, followed by the feedback it generates.

As the developer types, the IDE plugin sends a request through the API gateway, which authenticates the caller, applies rate limits, and routes the request. The context aggregation service assembles the current file, cursor position, open tabs, and language metadata into a prompt, optionally enriches it with related snippets from the repository's vector index, and truncates it to fit the context window.

The orchestration layer then checks the prompt cache. On a hit, the stored completion streams back immediately. On a miss, the GPU inference cluster generates the suggestion with batched decoding, and tokens stream back to the IDE over SSE as soon as generation starts. If inference fails or misses the latency threshold, the IDE simply shows no suggestion.

After the developer accepts, rejects, or edits the suggestion, the IDE publishes a feedback event to the message queue. The telemetry consumer writes it to the columnar store, where aggregation jobs compute acceptance rates and latency distributions that feed dashboards, evaluation, and fine-tuning.

## Achieving nonfunctional requirements[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Achieving-nonfunctional-requirements)

With the workflow traced, let's check how the architecture satisfies its strict operational constraints. The following table shows how the System Design addresses each nonfunctional requirement.

|  |  |  |
| --- | --- | --- |
| **Nonfunctional Requirement** | **Architectural Component** | **How the Architecture Satisfies It** |
| Low latency | Regional deployment + Redis cache + batched inference | Requests are routed to the nearest region, cached completions bypass GPU inference, and batching improves GPU throughput. |
| High availability | Multi-region deployment + load balancers | Traffic can be routed across regions, ensuring service continuity during regional disruptions. |
| Scalability | Horizontally scalable GPU clusters + auto-scaling policies | GPU nodes are added or removed dynamically based on traffic patterns across time zones. |
| Fault tolerance | Graceful degradation + cache fallback | If inference fails, the system returns an empty suggestion while maintaining IDE responsiveness. |
| Security and privacy | API gateway authentication + TLS + data retention controls | Requests are authenticated, encrypted in transit, and subject to enterprise data governance policies. |
| Cost efficiency | Model quantization + prompt caching + auto-scaling | Quantized models reduce GPU memory usage, caching avoids redundant inference, and capacity scales with demand. |

## Evaluation[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Evaluation)

While infrastructure metrics ensure that the system operates reliably, the architecture also tracks developer-centric quality signals to evaluate real-world effectiveness. Monitoring services collect metrics such as:

- Suggestion acceptance rate
- Edit distance between the suggested code and the final code
- Time-to-first-token latency
- Model performance by language or repository type

Tracking these signals helps detect issues such as the review and QA bottleneck, where AI-generated code volume grows faster than teams can review it.

Research into the perception gap suggests that developers often believe AI assistance makes them faster, yet empirical data sometimes shows no measurable improvement. This reinforces why the monitoring service must track actual developer productivity metrics, such as acceptance rates, edit distances on accepted suggestions, and deployment frequency, rather than relying solely on raw suggestion throughput.

To test your ability to apply these design principles under pressure, consider the following scenario.

AI Powered

Saved

10 attempts left

Reset

AI Code Assistant Performance Crisis

Hi, I'm Ed! Let's work through this design challenge together. First question: A company is deploying an internal code assistant for 50,000 developers across three regions. During peak hours, the GPU inference cluster in one region becomes overloaded, cache hit rates drop to 15%, and p99 latency spikes to 800ms. Identify at least three architectural changes or optimizations that could address this situation, explain the trade-offs of each change, and describe how the monitoring service should be configured to detect and respond to this scenario before it impacts developers

You have 10 attempts to answer.

## Conclusion[#](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Conclusion)

In this chapter, we explored how AI-powered code assistants evolve from a developer productivity problem into a large-scale, latency-sensitive distributed system. We began by defining the problem space, key capabilities, and strict requirements, particularly the need for real-time, context-aware suggestions under tight latency constraints. We then translated those requirements into a concrete architecture, showing how components like API gateways, context aggregation services, GPU inference clusters, caching layers, and telemetry pipelines work together to meet these demands at scale.

Designing such systems goes beyond enabling code generation and requires balancing competing constraints, including low latency, high availability, cost-efficient GPU utilization, and continuous improvement via feedback loops. The success of a code assistant depends not only on system performance but also on the quality and usefulness of its suggestions within the developer workflow.

Design a Document Q&A Assistant

Design an LLM-Powered Search Engine

Ask

[What is a code assistant?](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#What-is-a-code-assistant)

[System requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#System-requirements)

[Functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Functional-requirements)

[Nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Nonfunctional-requirements)

[Resource estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Resource-estimation)

[Estimating the number of servers](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Estimating-the-number-of-servers)

[Storage estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Storage-estimation)

[Bandwidth estimation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Bandwidth-estimation)

[System design of an AI code assistant](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#System-design-of-an-AI-code-assistant)

[Building blocks](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Building-blocks)

[High-level design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#High-level-design)

[API design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#API-design)

[Storage schema](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Storage-schema)

[Achieving functional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Achieving-functional-requirements)

[A detailed system design](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#A-detailed-system-design)

[Inference path](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Inference-path)

[Telemetry path](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Telemetry-path)

[Putting everything together](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Putting-everything-together)

[Workflow of the system](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Workflow-of-the-system)

[Achieving nonfunctional requirements](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Achieving-nonfunctional-requirements)

[Evaluation](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Evaluation)

[Conclusion](https://www.educative.io/courses/generative-ai-system-design/design-an-ai-code-assistant#Conclusion)