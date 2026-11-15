# Design_Strategies_and_Challenges_in_Agentic_AI_Systems

Source: https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# Key Challenges and Design Strategies in Agentic AI Systems

Understand the major challenges in designing agentic AI systems including high latency, output reliability, memory consistency, integration complexity, and security concerns. Learn practical strategies such as model selection, caching, human oversight, fault tolerance, and modular architectures to build resilient, scalable, and trustworthy AI agents for real-world production environments.

We'll cover the following...

- [High inference latency](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#High-inference-latency)
- [Output uncertainty and hallucination](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Output-uncertainty-and-hallucination)
- [Memory management and consistency](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Memory-management-and-consistency)
- [Scalability](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Scalability)
- [Integration complexity](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Integration-complexity)
- [Security and privacy vulnerabilities](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Security-and-privacy-vulnerabilities)
- [Lack of standardized evaluation metrics](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Lack-of-standardized-evaluation-metrics)
- [Human-in-the-loop overhead](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Human-in-the-loop-overhead)
- [Fault tolerance and failure recovery](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Fault-tolerance-and-failure-recovery)
- [Summary: Building resilient agentic systems](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Summary-Building-resilient-agentic-systems)

We’ve now explored the foundational elements of AI agents: their core components, architectural loops, orchestration patterns, and the crucial role of guardrails and human oversight. As we move from theory to practical system design, it’s vital to recognize that building robust, production-ready agentic AI systems involves navigating a set of inherent challenges. These are not merely technical hurdles, but fundamental considerations that will shape our architectural decisions and directly impact our system’s reliability, cost, performance, and user experience.

This lesson consolidates these key challenges and, more importantly, provides practical design strategies for mitigating them. Understanding these potential pitfalls upfront allows us to proactively build resilience, trustworthiness, and efficiency into our agentic systems.

## High inference latency[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#High-inference-latency)

Large language models (LLMs), especially the more capable ones, are computationally intensive. This can lead to significant delays in an agent’s response time, often referred to as high inference latency. This challenge is critical in real-time applications like customer support, financial trading, or interactive tools, where even small delays can degrade user experience or lead to missed opportunities. Complex agentic workflows involving multiple LLM calls, tool invocations, or multi-agent interactions further exacerbate this.

Slow responses frustrate users and can make the agent feel unintelligent or unresponsive. High latency also translates directly to higher operational costs, as more powerful or numerous computing resources are needed to compensate. This presents a direct trade-off between response speed and computational expense.

The following are some of the design strategies that can help reduce this issue:

![A large, complex model can lead to slow responses (left), while strategies like judicious model selection and parallelization can lead to significantly faster outcomes (right)](006_Design_Strategies_and_Challenges_in_Agentic_AI_Systems_images/img_cc39db5fb944.svg "A large, complex model can lead to slow responses (left), while strategies like judicious model selection and parallelization can lead to significantly faster outcomes (right)")

A large, complex model can lead to slow responses (left), while strategies like judicious model selection and parallelization can lead to significantly faster outcomes (right)

- **Judicious model selection:** Do not always default to the largest or most capable LLM. For tasks that are straightforward (e.g., simple classification, basic summarization, intent recognition), consider using smaller, faster, and more cost-effective models. Reserve larger LLMs for complex reasoning, planning, or creative generation. For example, if our agent primarily extracts entities from text (structured data) but occasionally needs to generate creative marketing copy, consider a smaller, specialized model for extraction, and a larger one only when the creative task is invoked. This pattern, often called **routing**, ensures that you use the right model for the job, optimizing for both cost and speed. This avoids unnecessary latency and cost.
- **Model optimization:** Employ techniques like quantization, pruning, and knowledge distillation to reduce the model’s size and computational requirements without significant loss of accuracy. These methods make models lighter and faster for deployment.
- **Caching mechanisms:** Implement caching for frequently requested or deterministic outputs. If the agent repeatedly asks for the same static information, or if a tool call consistently returns the same result for identical inputs, cache the response to avoid re-running the LLM or tool calls. This can include caching common LLM responses, tool outputs for idempotent operations, or frequently accessed data from external knowledge bases.
- **Parallelization of operations:** Whenever possible, design your agent’s workflow to perform multiple LLM calls or tool invocations concurrently rather than sequentially. For example, if an agent needs to check multiple data sources for information before making a decision, trigger all necessary API calls in parallel.
- **Asynchronous processing:** For tasks that don’t require immediate user response (e.g., back-end data processing, report generation), design the agent to operate asynchronously. This allows the system to continue processing other requests without waiting for long-running tasks to complete.
- **Hardware acceleration and deployment strategy:** Leverage specialized hardware (GPUs, TPUs) and optimize deployment for low-latency inference. Consider edge computing if responsiveness to localized inputs is paramount.

## Output uncertainty and hallucination[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Output-uncertainty-and-hallucination)

LLMs can generate plausible-sounding but factually incorrect, biased, or nonsensical information, known as a “hallucination.” This inherent uncertainty is a significant concern, especially in high-stakes applications like medical diagnosis, legal analysis, or financial advice, where incorrect outputs can have severe consequences.

Unreliable outputs erode user trust, can lead to dangerous actions, and demand robust validation. However, aggressive validation (e.g., very strict guardrails) can lead to over-blocking or increased latency.

The following are some of the design strategies that can help reduce this issue:

![Grounding an agent in a verifiable knowledge base can combat hallucination. An initial, incoherent output is transformed into a clear, factual response after using retrieval-augmented generation (RAG)](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Grounding an agent in a verifiable knowledge base can combat hallucination. An initial, incoherent output is transformed into a clear, factual response after using retrieval-augmented generation (RAG)")

Grounding an agent in a verifiable knowledge base can combat hallucination. An initial, incoherent output is transformed into a clear, factual response after using retrieval-augmented generation (RAG)

- **Retrieval-augmented generation (RAG):** Use RAG to ground LLM responses in verifiable external knowledge bases. By retrieving relevant documents and facts *before* generating a response, the LLM is guided by accurate information, significantly reducing hallucination.
- **Output validation guardrails:** Implement strong rules-based output validation to check generated content against predefined criteria for accuracy, safety, and format. This can include factual consistency checks, regex for forbidden terms, or adherence to specific JSON schemas.
- **Ensembling and voting:** For critical decisions, query multiple LLM instances or different models and use a voting mechanism to select the most consistent or highest-confidence output.
- **Confidence scoring:** Design agents to provide a confidence score for their responses or recommendations. If confidence is below a certain threshold, it can trigger a human review or a clarifying question to the user.
- **Clear instructions and prompt engineering:** Ensure instructions are precise, define the expected output format, and explicitly state constraints (e.g., “Do not make up facts; if you don’t know, state ‘I don’t know.’”)

## Memory management and consistency[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Memory-management-and-consistency)

Maintaining coherent, up-to-date, and accurate context across multi-turn interactions or long periods is complex. Issues can arise with memory consistency, handling outdated information, preventing data corruption, and managing shared state in multi-agent systems.

Without effective memory, agents lose context, become repetitive, and cannot adapt over time, making them feel unintelligent or frustrating to use. Designing sophisticated memory systems involves trade-offs between storage cost, retrieval latency, and the complexity of managing consistency across distributed components.

The following are some of the design strategies to use memory effectively:

![An agent accessing distinct memory systems: short-term for immediate context (like a notepad), long-term for stored experiences (like a file cabinet), and external for vast knowledge bases (like a cloud database). This structure allows the agent to recall recent conversations while also retrieving deep, external knowledge when needed](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "An agent accessing distinct memory systems: short-term for immediate context (like a notepad), long-term for stored experiences (like a file cabinet), and external for vast knowledge bases (like a cloud database). This structure allows the agent to recall recent conversations while also retrieving deep, external knowledge when needed")

An agent accessing distinct memory systems: short-term for immediate context (like a notepad), long-term for stored experiences (like a file cabinet), and external for vast knowledge bases (like a cloud database). This structure allows the agent to recall recent conversations while also retrieving deep, external knowledge when needed

- **Structured memory systems:** Implement clear distinctions between short-term, long-term, and external memory. Use vector databases for long-term and external knowledge to enable efficient semantic retrieval. For example, store user preferences in a structured long-term memory (e.g., a database profile), dialogue history in short-term memory, and product documentation in an external vector database.
- **Explicit memory access policies:** Define which agents or modules can read, write, or update specific parts of memory. This prevents unauthorized access or accidental corruption, particularly in multi-agent systems.
- **Selective memory retention:** Implement policies for what information is stored and for how long. Not all dialogue turns or retrieved facts need to be permanently memorized. Filter sensitive or irrelevant information before storage.
- **Versioning and auditing memory:** For critical data in long-term memory, consider versioning to track changes. Implement logging and audit trails to monitor memory updates and ensure consistency.

## Scalability[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Scalability)

As user loads increase, task complexities grow, or the number of interacting agents expands, agentic systems must be able to scale efficiently without degradation in performance or an exponential rise in cost.

A system that works well for one user, but fails for a thousand is not production-ready. Scalability ensures the system remains performant and cost-effective as demand grows. However, achieving high scalability often involves increased architectural complexity and infrastructure costs.

The following are some of the design strategies to build agentic systems that can work at scale:

![By breaking down a large task into smaller “building blocks,” a system becomes easier to manage, adapt, and grow](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "By breaking down a large task into smaller “building blocks,” a system becomes easier to manage, adapt, and grow")

By breaking down a large task into smaller “building blocks,” a system becomes easier to manage, adapt, and grow

- **Modular architecture:** Design agents with a modular approach, breaking down complex systems into smaller, independent components (models, tools, instructions). This allows for independent development, deployment, and scaling of each module.
- **Multi-agent orchestration:** Utilize multi-agent patterns like Manager-Worker or decentralized handoff to distribute workload. Specialized agents can handle specific tasks in parallel, improving overall throughput.
- **Efficient resource allocation:** Implement dynamic resource allocation, and load balancing across LLM endpoints and tool services. Use auto scaling mechanisms to provision resources based on demand.
- **Optimized tool calls:** Ensure tools are highly optimized and efficient. Minimize redundant API calls and leverage batching where possible. External services (e.g., search APIs) should be high-performance.

## Integration complexity[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Integration-complexity)

Real-world agentic systems rarely operate in isolation. They often need to interact with a multitude of diverse external tools, APIs, legacy systems, and data sources, each with its own data formats, authentication methods, and error handling. Seamless and reliable integration can be a significant engineering hurdle.

Poor integration leads to brittle systems, frequent errors, and difficult debugging. The trade-off here is balancing rapid prototyping with building robust, maintainable connections that can handle diverse external systems.

The following are some of the design strategies to handle challenges associated with integration complexity:

![An API abstraction layer can simplify integration. It acts as a clean, single interface between the agent, and a complex web of external tools and legacy systems](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "An API abstraction layer can simplify integration. It acts as a clean, single interface between the agent, and a complex web of external tools and legacy systems")

An API abstraction layer can simplify integration. It acts as a clean, single interface between the agent, and a complex web of external tools and legacy systems

- **Standardized tool definitions:** Define tools with clear, standardized interfaces (e.g., JSON schemas for inputs/outputs) to simplify how the LLM interacts with them, and how different agents can invoke them.
- **API abstraction layers:** Create abstraction layers for external APIs. This separates the agent’s logic from the specifics of third-party APIs, making it easier to swap out or update services without modifying the core agent.
- **Robust error handling:** Implement comprehensive `try...catch` blocks and retry logic for all tool invocations and external calls. Design fallback mechanisms when tools fail, or return unexpected data.
- **Clear communication protocols:** In multi-agent systems, establish explicit communication protocols and message formats between agents to ensure smooth handoffs and data exchange.

## Security and privacy vulnerabilities[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Security-and-privacy-vulnerabilities)

Agent systems, particularly those powered by LLMs, introduce new attack vectors. These include prompt injection (manipulating prompts to bypass safety), jailbreaking (coaxing the LLM into generating harmful content), and unintentional data leakage (exposing sensitive user data).

Security breaches and privacy violations can lead to severe reputational damage, legal liabilities, and loss of user trust. Implementing comprehensive security measures, however, can introduce performance overhead and increase system complexity.

The following are some of the design strategies to build secure agentic systems:

![A multi-layered defense strategy against security vulnerabilities: A potential threat is stopped by sequential guardrails, including input filtering, PII redaction, and output moderation](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "A multi-layered defense strategy against security vulnerabilities: A potential threat is stopped by sequential guardrails, including input filtering, PII redaction, and output moderation")

A multi-layered defense strategy against security vulnerabilities: A potential threat is stopped by sequential guardrails, including input filtering, PII redaction, and output moderation

- **Multi-layered guardrails:** Implement a robust set of guardrails at various points in the agent’s workflow:

  - **Input filtering:** To detect and block malicious prompts (e.g., jailbreaks, prompt injections).
  - **PII redaction:** To automatically identify and mask sensitive personal information.
  - **Tool use safeguards:** To restrict unauthorized or risky actions by tools (e.g., allowlisting, argument validation, rate limits).
  - **Output moderation:** To filter harmful or inappropriate generated content.
- **Authentication and authorization:** Implement strong access controls to ensure only authorized users or systems can interact with the agent, or its tools.
- **Secure deployment practices:** Adhere to standard cybersecurity best practices for deployment environments, including network security, encryption, and regular security audits.
- **Differential privacy (advanced):** For highly sensitive applications, explore differential privacy techniques during model training or inference to protect individual data points from being inferred from agent outputs.

## Lack of standardized evaluation metrics[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Lack-of-standardized-evaluation-metrics)

Comprehensively evaluating agent systems is difficult because they are dynamic, goal-oriented, and interactive. Traditional metrics for static models often fall short. It’s hard to compare different systems or consistently measure progress when there’s no universal benchmark for qualities like adaptiveness, coherence, or goal-seeking behavior over time.

Without clear metrics, it’s difficult to know if our system is actually improving, where its weaknesses lie, or how it compares to alternatives. Developing custom evaluation frameworks requires significant effort and resources, presenting a trade-off between evaluation rigor and development speed.

The following design strategies can help us make better evaluations of our agentic systems:

![The challenge of evaluating dynamic agents: Using traditional, rigid metrics is like trying to measure a complex, shifting shape with a simple ruler. A more diverse set of evaluation tools is required](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The challenge of evaluating dynamic agents: Using traditional, rigid metrics is like trying to measure a complex, shifting shape with a simple ruler. A more diverse set of evaluation tools is required")

The challenge of evaluating dynamic agents: Using traditional, rigid metrics is like trying to measure a complex, shifting shape with a simple ruler. A more diverse set of evaluation tools is required

- **Define clear task-oriented metrics:** Go beyond linguistic fluency. Define success based on goal achievement (e.g., task completion rate, problem-solving accuracy) and interaction quality (e.g., efficiency in turns, user satisfaction). The MACRS case study (which we will learn as we proceed) provides excellent examples: Success Rate, Hit Ratio@K, Average Number of Turns.
- **Utilize simulation environments:** Develop or use simulated user environments to enable controlled, and reproducible testing of agent performance across various scenarios. This helps in surfacing edge cases, and iterating on design choices.
- **Human-centric evaluation:** Incorporate qualitative feedback through user satisfaction surveys, A/B testing with real users, and expert human review sessions to capture aspects that automated metrics might miss.
- **Observability and logging:** Implement robust logging and monitoring to capture detailed interaction traces, tool usage, and internal reasoning steps. This data is invaluable for retrospective analysis and identifying areas for improvement.

## Human-in-the-loop overhead[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Human-in-the-loop-overhead)

While human oversight is crucial for safety and reliability, especially in high-stakes scenarios, it introduces its own set of operational challenges. These include potential latency in approvals, significant operational costs, scalability issues (humans can’t keep up with hundreds of agents), and human fatigue from repetitive reviews.

Inefficient human-in-the-loop processes can bottleneck the system, increase costs, and lead to human errors due to burnout.

The following design strategies can help reduce this overhead:

![By strategically filtering tasks and escalating only complex issues to a human reviewer with an efficient interface, the system reduces bottlenecks. The feedback from these reviews then enables continuous learning for the agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "By strategically filtering tasks and escalating only complex issues to a human reviewer with an efficient interface, the system reduces bottlenecks. The feedback from these reviews then enables continuous learning for the agent")

By strategically filtering tasks and escalating only complex issues to a human reviewer with an efficient interface, the system reduces bottlenecks. The feedback from these reviews then enables continuous learning for the agent

- **Strategic placement of human touchpoints:** Design human intervention points only for high-stakes actions, ambiguous situations, or when model confidence is low. Avoid over-escalation for routine tasks. For example, a financial agent might require human approval for transfers over a certain amount, but automates smaller, low-risk transactions.
- **Efficient intervention interfaces:** Design intuitive dashboards or interfaces that provide human reviewers with all the necessary context to make quick and informed decisions (e.g., agent’s reasoning, relevant data, proposed action).
- **Automated summaries for reviewers:** If a human needs to review a complex interaction, have the agent itself generate a concise summary of the situation, its proposed plan, and the reasons for escalation.
- **Continuous learning to reduce human intervention:** Use data from human interventions as feedback to improve the agent’s models and instructions (e.g., via reflection mechanisms, as we will learn later in the MACRS case study ), gradually reducing the need for human involvement over time for similar scenarios.

## Fault tolerance and failure recovery[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Fault-tolerance-and-failure-recovery)

In multi-agent systems, or even complex single-agent workflows, components (like an agent, a tool, or an external API) can fail mid-execution. Without robust fault tolerance and recovery mechanisms, such failures can lead to stalled processes, inconsistent states, or complete system crashes. This is particularly complex when multiple agents are involved, as one agent’s failure can cascade through the system.

Production systems must be resilient. Unhandled failures result in unreliable agents, require manual intervention, and erode user trust, especially in high-stakes environments.

The following are some of the design strategies that can be implemented to handle such issues:

![When an error occurs in a process, a resilient system can use different recovery methods, such as retrying the action, rolling back to a safe checkpoint, handing off to a human, or continuing with reduced functionality](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "When an error occurs in a process, a resilient system can use different recovery methods, such as retrying the action, rolling back to a safe checkpoint, handing off to a human, or continuing with reduced functionality")

When an error occurs in a process, a resilient system can use different recovery methods, such as retrying the action, rolling back to a safe checkpoint, handing off to a human, or continuing with reduced functionality

- **Graceful degradation:** Design agents to continue operating, possibly with reduced functionality, even if a non-critical component or tool fails. For example, a customer support agent might temporarily disable a specific product lookup tool if its API is down, but still handle general FAQs.
- **Retry mechanisms:** Implement automatic retry logic for transient errors in tool calls or inter-agent communication, with exponential backoff.
- **Checkpointing and state management:** Periodically save the agent’s internal state and the overall workflow’s progress. This allows the system to resume from the last known good state after a failure, rather than restarting from scratch.
- **Failure handoffs (to human or another agent):** Define clear escalation paths. If an agent cannot recover from a failure after retries, it should hand off the task to a human supervisor (as discussed in human-in-the-loop) or a designated ‘recovery agent.’
- **Error boundaries and isolation:** Design a modular architecture where failures in one component are contained, and don’t propagate to the entire system. Use separate processes or microservices for critical agent components.

## Summary: Building resilient agentic systems[#](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Summary-Building-resilient-agentic-systems)

Designing agentic AI systems is an iterative process of balancing powerful capabilities with real-world constraints and risks. Proactively addressing these key challenges through thoughtful architectural choices, robust component design, strategic orchestration, and layered safety mechanisms, can help build AI systems. These system are not only intelligent, but also reliable, trustworthy, and truly impactful in production environments. This comprehensive understanding forms the bedrock for our journey as an agentic system designer.

**Production readiness checklist for agentic AI systems:** Before deploying your agentic AI system to a production environment, consider the following checklist to ensure its robustness, reliability, and trustworthiness:

- **Performance and latency:**

  - Are response times within acceptable limits for critical user journeys?
  - Has the system been tested under peak load conditions?
  - Are the cost implications of LLM inference and tool usage understood and managed?
- **Reliability and accuracy:**

  - Are hallucination rates minimized, especially for high-stakes outputs?
  - Are key decisions validated (e.g., via RAG, output guardrails, ensembling)?
  - Are error handling and retry mechanisms in place for tool failures?
  - Can the system gracefully degrade if a non-critical component fails?
- **Memory management:**

  - Is memory consistency maintained across turns and agents?
  - Are policies for sensitive data retention/expiration implemented?
  - Is the memory system scalable for long-term use?
- **Security and privacy:**

  - Are all inputs/outputs filtered for safety, PII, and malicious content?
  - Are tool access policies strictly enforced?
  - Are authentication and authorization mechanisms robust?
- **Human oversight and intervention:**

  - Are clear human-in-the-loop (HITL) points defined for high-risk actions?
  - Are intervention interfaces intuitive, and do they provide sufficient context for human reviewers?
  - Are audit trails and logging comprehensive for accountability and post-mortem analysis?
- **Observability and monitoring:**

  - Are continuous monitoring and alerting systems in place for key performance and safety metrics?
  - Can the system’s internal reasoning and tool usage be easily traced and debugged?
- **Scalability and maintainability:**

  - Is the architecture modular and extensible for future updates and scaling?
  - Are deployment strategies optimized for efficiency and resilience?
  - Is the documentation clear for ongoing maintenance and development?

Building Trustworthy Agents: Guardrails and Human Oversight

Introduction to MACRS and the Design Challenge

Ask

[High inference latency](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#High-inference-latency)

[Output uncertainty and hallucination](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Output-uncertainty-and-hallucination)

[Memory management and consistency](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Memory-management-and-consistency)

[Scalability](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Scalability)

[Integration complexity](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Integration-complexity)

[Security and privacy vulnerabilities](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Security-and-privacy-vulnerabilities)

[Lack of standardized evaluation metrics](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Lack-of-standardized-evaluation-metrics)

[Human-in-the-loop overhead](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Human-in-the-loop-overhead)

[Fault tolerance and failure recovery](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Fault-tolerance-and-failure-recovery)

[Summary: Building resilient agentic systems](https://www.educative.io/courses/agentic-ai-systems/key-challenges-and-design-strategies-in-agentic-ai-systems#Summary-Building-resilient-agentic-systems)