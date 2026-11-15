# Introduction_to_Autonomous_AI_Agents_and_Their_Capabilities

Source: https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Agentic System Design](https://www.educative.io/courses/agentic-ai-systems)

# Introduction to AI Agents

Understand what defines an AI agent and how it differs from traditional AI models. Learn about the core components of AI agents, their evolution from rule-based systems to LLM-powered autonomous agents, and the types of agents including software, physical, and hybrid. Discover when building an agent is appropriate based on task complexity, decision-making needs, and data type to design effective and adaptive agentic systems.

We'll cover the following...

- [What is an AI agent?](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#What-is-an-AI-agent)
- [AI models vs. AI agents](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#AI-models-vs-AI-agents)
- [Three categories of AI agents](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Three-categories-of-AI-agents)
  - [Software-based agents (sandbox environment)](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Software-based-agents-sandbox-environment)
  - [Physical agents (embodied systems)](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Physical-agents-embodied-systems)
    - [Hybrid and adaptive agents (real-world integration)](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Hybrid-and-adaptive-agents-real-world-integration)
- [Evolution from rule-based systems to LLM-powered agents](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Evolution-from-rule-based-systems-to-LLM-powered-agents)
  - [Rule-based agents: Fixed logic, limited flexibility](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Rule-based-agents-Fixed-logic-limited-flexibility)
  - [Learning-based agents: Trial and feedback](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Learning-based-agents-Trial-and-feedback)
  - [LLM-powered agents: Generalization through language](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#LLM-powered-agents-Generalization-through-language)
- [When should you build an agent?](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#When-should-you-build-an-agent)
  - [The task requires contextual decision-making](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-task-requires-contextual-decision-making)
  - [The rules are too complex to maintain](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-rules-are-too-complex-to-maintain)
  - [The workflow relies on unstructured or natural language data](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-workflow-relies-on-unstructured-or-natural-language-data)
- [Summary](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Summary)

The landscape of AI is rapidly evolving, especially with the rise of large language models (LLMs). While early LLM applications focused on single-turn interactions or basic text generation, the field of AI agents, with its roots in earlier rule-based and learning-based systems, has seen a significant resurgence and transformation. A new category of intelligent systems, powered by LLMs, has emerged. These systems are not limited to processing information in isolation. They are designed to carry out complex, multi-step tasks on behalf of users, often without explicit instructions at every step.

In this course, we’ll move beyond individual agents to focus on **agentic system design**. This means understanding how individual agents are not just standalone entities, but are architected and integrated as part of larger, cohesive systems. Effective agentic system design involves making deliberate architectural choices and utilizing reusable patterns to create reliable, scalable, and adaptive AI solutions. Real-world agentic systems often involve multiple interacting agents, necessitating careful planning, communication, and arbitration as fundamental design aspects.

By the end of this lesson, you will be able to:

- Define what makes a system an AI agent.
- Distinguish between AI models and agents.
- Identify different types of agents and their roles.
- Understand the evolution from rule-based to LLM-powered agents.
- Evaluate when to use an agent instead of a simpler solution.

## What is an AI agent?[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#What-is-an-AI-agent)

In the world of artificial intelligence, the term **agent** refers to a system that can perceive its environment, make decisions, and act autonomously to achieve specific goals. This concept, often summarized as ‘perceive-reason-act,’ is a cornerstone of classical AI theory, notably popularized by Russell and Norvig. Unlike a passive model that requires a user to query it or interpret its outputs, an AI agent is an active entity. It can sense, think, and act on its own, often without continuous human oversight.

Let’s break this down more concretely. At its core, an AI agent has three fundamental capabilities:

![Breaking down how an AI agent works: It perceives the environment (input), reasons to make a decision (processing), and performs a task (output)](001_Introduction_to_Autonomous_AI_Agents_and_Their_Capabilities_images/img_23c3856a5afc.svg "Breaking down how an AI agent works: It perceives the environment (input), reasons to make a decision (processing), and performs a task (output)")

Breaking down how an AI agent works: It perceives the environment (input), reasons to make a decision (processing), and performs a task (output)

1. **Perception:** The agent must be able to sense its environment. This could mean reading text from a user, analyzing images or audio, or retrieving data from sensors or databases. The goal is to extract meaningful information from the raw input.
2. **Reasoning and planning:** Once the environment is perceived, the agent must make decisions. This involves understanding context, selecting actions, and planning steps toward a goal. LLMs like `gpt-6-astra`, `claude-fable-5-1`, and `gemini-3.8-flash` are often used here, providing powerful language-based reasoning abilities. Agents can be reactive, responding directly to immediate stimuli, or deliberative, engaging in multi-step planning and reasoning before acting.
3. **Action execution:** The agent must then act. This could mean sending a reply, calling an API, triggering a robot’s motion, or updating a database. The key is that the agent’s actions are grounded in its reasoning process and tailored to its goals.

This full pipeline, which includes sensing, interpreting, and acting, captures what makes an AI system *agentic* rather than reactive. The autonomy levels of agents can vary, from partial automation requiring human approval to full independence, depending on the task and safety requirements.

Here’s a simple real-world analogy:

> Imagine a personal AI assistant embedded in your smart home. It hears you say, “Remind me to call mom at 6 PM.” It parses your speech (perception), understands that this is a timed reminder (reasoning), and schedules an alarm for 6 PM (action).

Another analogy that mimics a more complex agentic system:

> Picture an AI travel concierge running on your phone. It sees your flight to Berlin has been cancelled (perception), and reasons that you must still reach Berlin tonight. It then checks alternate flights/trains, books the best combo, and messages your hotel about the late arrival (plan and multi-step action).

This full pipeline, which includes sensing, interpreting, and acting, captures what makes an AI system agentic rather than reactive.

Key characteristics of an AI agent are summarized in the following table:

## Key Characteristics of an AI Agent

|  |  |
| --- | --- |
| **Feature** | **Description** |
| **Autonomy** | Acts independently, initiating actions and making decisions without continuous human intervention. |
| **Goal-Oriented Behavior** | Consistently directs actions toward achieving predefined objectives, rather than merely reacting or producing isolated outputs. |
| **Perception and Feedback Loop** | Continuously observes its environment, processes inputs, and adjusts behavior based on the outcomes or new information. |
| **Continuity** | Maintains memory or context over time, allowing multi-turn reasoning. |
| **Flexibility** | Can revise plans and policies when objectives or context change, provided the agent’s perception, memory, and planning modules support it. |

This agent-centric view aligns with how intelligence is typically understood in biological systems. It is not just about recognizing patterns, but about using those insights to take meaningful action.

## AI models vs. AI agents[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#AI-models-vs-AI-agents)

A common point of confusion in AI system design is the distinction between an AI model and an AI agent. Although both are foundational elements in artificial intelligence, they serve very different roles.

![AI model vs. AI agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "AI model vs. AI agent")

AI model vs. AI agent

Let’s start with the simpler concept:

An **AI model** is a self-contained program trained to perform a specific function. More precisely, an AI model is often an artifact (e.g., a set of learned weights and biases) that is consumed by a program to perform a specific function. For example:

- A classification model predicts whether an email is spam or not.
- A text generation model completes a sentence or writes a poem.
- A speech recognition model converts audio into text.

These models do not have goals, initiative, or awareness of context beyond the current input. They wait for a prompt, compute an output, and stop. In this sense, models are powerful, but passive.

An **AI agent**, by contrast, is an active system. It uses one or more models as components within a larger decision-making process. An agent has autonomy, memory, goals, and the ability to take action based on what it observes.

An agent might:

- Use a language model to understand instructions.
- Call a search tool to gather information.
- Store conversation history in a vector database to reuse facts or preferences later.
- Monitor its success and adapt its behavior over time.

The key difference is this: the agent takes initiative and operates over time, often within a loop of perception, reasoning, and action.

## Comparison Between AI Model and AI Agent

|  |  |  |
| --- | --- | --- |
| **Feature** | **AI Model** | **AI Agent** |
| **Scope** | Narrow task | Broader system of behavior |
| **Role** | Computes outputs from inputs | Chooses actions in pursuit of goals |
| **Context Awareness** | Limited to the current inference window | Maintains and updates internal context |
| **Initiative** | Waits for input | Acts autonomously when triggered or scheduled |
| **Tool Use** | No | Yes, often includes multiple tools and models |
| **Example** | Sentiment classifier | Customer support assistant that answers, escalates, and logs tickets |

Here’s an analogy: If an AI model is like a calculator, then an AI agent is like a personal assistant. The calculator waits for a formula, and gives a result. The assistant listens to your needs, figures out what to do, takes initiative, asks clarifying questions, and performs actions on your behalf.

## Three categories of AI agents[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Three-categories-of-AI-agents)

AI agents can take many forms depending on how they interact with their environment. One way to organize this variety is by categorizing agents based on their mode of operation. Broadly, there are three main types:

### Software-based agents (sandbox environment)[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Software-based-agents-sandbox-environment)

These agents operate entirely in digital spaces. They interact with users, applications, or data through APIs, web interfaces, documents, or databases.

![Software-based AI agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Software-based AI agent")

Software-based AI agent

Examples include:

- A chatbot that provides customer service on a retail website.
- An email triage agent that categorizes and replies to messages.
- A trading bot that monitors financial news and executes trades.

Although these agents are not embodied in the physical world, they can still carry out meaningful actions, such as updating records, sending alerts, or triggering automated workflows.

**Key characteristics:**

- No physical sensors or hardware.
- Act through code, interfaces, and digital data.
- Often use tools like web search, file access, and language models.

### Physical agents (embodied systems)[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Physical-agents-embodied-systems)

Physical agents interact with the real-world using sensors and actuators. These systems perceive their surroundings through hardware, and perform actions by physically affecting the environment.

![Physical AI agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Physical AI agent")

Physical AI agent

Examples include:

- A domestic robot that cleans your home and responds to voice commands.
- An autonomous vehicle that navigates traffic and avoids obstacles.
- A robotic arm on a factory floor that assembles products.

These agents require a complex integration of perception (e.g., cameras, microphones, LiDAR), real-time reasoning, and precise control mechanisms.

**Key characteristics:**

- Sense the physical world using embedded sensors.
- Act using motors, arms, wheels, or other actuators.
- Must handle uncertainty, delay, and safety in real environments.

#### Hybrid and adaptive agents (real-world integration)[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Hybrid-and-adaptive-agents-real-world-integration)

Hybrid agents combine both digital and physical capabilities. These agents work across environments, and continuously adapt based on feedback. They are capable of learning from both structured data, and unstructured sensory input over time.

![Hybrid AI agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Hybrid AI agent")

Hybrid AI agent

Examples include:

- An AI-driven traffic system that analyzes live camera feeds and adjusts signal timing based on congestion.
- A healthcare assistant who monitors wearable devices, suggests treatment adjustments, and communicates with doctors.
- A warehouse robot that uses online databases to restock inventory and physically moves goods.

These agents often blend software logic with real-world embodiment and rely on learning mechanisms to refine their behavior over time.

**Key characteristics:**

- Operate across both digital and physical domains.
- Integrate multi-modal data (text, images, sensor readings).
- Adapt and improve through real-world feedback loops, potentially by periodically retraining its perception module with logged sensor data.

Each of these categories highlights a different level of complexity and environmental interaction. As we move from software-based to hybrid agents, the challenges grow, and so do the opportunities for creating deeply intelligent systems.

## Evolution from rule-based systems to LLM-powered agents[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Evolution-from-rule-based-systems-to-LLM-powered-agents)

The idea of autonomous agents is not new. In fact, early AI systems from decades ago could already make decisions and take actions. However, their capabilities were limited due to the narrow scope of their design. Most early agents were rule-based systems: if X happened, then do Y. This approach worked for clearly defined, repetitive tasks, but it quickly failed in dynamic or unpredictable environments.

![Evolution of AI agents](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Evolution of AI agents")

Evolution of AI agents

### Rule-based agents: Fixed logic, limited flexibility[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Rule-based-agents-Fixed-logic-limited-flexibility)

Rule-based or expert systems, such as MYCIN and XCON, were prominent in the 1970s to 1980s. In rule-based systems, human developers explicitly define all the rules.

![Rule-based agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Rule-based agent")

Rule-based agent

For example:

- If the user says “I forgot my password,” then show a password reset form.
- If the temperature exceeds 30°C, turn on the fan.

These systems are easy to understand and control. However, they do not generalize well. They cannot infer new rules from data or handle edge cases and ambiguity. Scaling such systems requires writing and maintaining thousands of individual rules by hand.

### Learning-based agents: Trial and feedback[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Learning-based-agents-Trial-and-feedback)

The next major leap came with machine learning. Learning-based agents, spanning supervised, unsupervised, and reinforcement learning paradigms, shifted rule authoring from explicit human definition to data-driven optimization. While supervised learning models, like CNNs and RNNs, enable advancements in perception for agents (e.g., speech recognition in virtual assistants), reinforcement learning (RL) introduces a powerful new paradigm. It allows agents to learn complex behaviors through trial and error, receiving rewards for good actions and penalties for bad ones. RL is often considered the most ‘agent-like’ subset due to its focus on sequential decision-making in dynamic environments.

AlphaGo’s breakthrough in 2016, for example, demonstrated its power. Given that, in RL, agents learn through experimentation, this approach enables agents to discover strategies that human designers might not think to program explicitly.

![Learning-based agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Learning-based agent")

Learning-based agent

For example:

- AlphaGo learned to defeat world-class Go players by playing millions of games against itself.
- Robot arms trained with RL can learn to pick up objects without needing precise location data.

While more flexible than rule-based systems, RL agents often require large-scale training, significant compute resources, and carefully structured environments. They are powerful, but not always practical for general-purpose applications.

### LLM-powered agents: Generalization through language[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#LLM-powered-agents-Generalization-through-language)

The most recent breakthrough in agent design has come from large language models (LLMs) such as GPT, Claude, and Gemini.

While reinforcement learning discovers optimal policies through iterative reward signals, large language models bring a new dimension: zero-shot generalization. They achieve this by internalizing vast amounts of world knowledge and reasoning capabilities directly within their parameters. This enables them to understand and respond to novel tasks without explicit retraining. These models are pretrained on massive datasets of human language. This, in turn, gives them the ability to reason, plan, and coordinate tasks using natural language instructions.

When LLMs are used within agent systems, they enable several powerful capabilities:

- **Tool use:** Selecting and operating the right tool for a given job/action to perform. The agent, through its reasoning, decides which tool to use and what parameters to pass to it.
- **Dynamic task planning:** Decomposing complex goals into manageable steps and deciding how to approach them.
- **Conversational memory:** Maintaining awareness across multiple turns of dialogue.
- **Generalization:** Handling novel tasks without needing retraining.

![LLM-powered agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "LLM-powered agent")

LLM-powered agent

For example, a modern LLM-powered agent can handle a request like:

> “Summarize this research paper and email the key points to my team.”

The agent can understand the instruction, extract and summarize the content, format the result, and trigger an API call to send the email. None of these behaviors need to be hardcoded in advance.

This level of flexibility marks a major shift. Agents are no longer just reactive systems built on rigid logic. They are evolving into adaptive, collaborative, and tool-using systems that can generalize their behavior across a wide range of problems.

It’s crucial to acknowledge that while LLM-powered agents are immensely powerful, they also come with inherent limitations. These can include issues with reliability (e.g., generating inaccurate outputs often called hallucinations), and interpretability (understanding why an agent made a particular decision). Moreover, there can also be potential for biases, and challenges related to high inference latency and security vulnerabilities. Understanding these limitations is as important as recognizing their capabilities when designing trustworthy agentic systems.

AI Powered

Saved

2 attempts left

Reset

Concept check

Consider the following scenarios. For each, decide whether a rule-based system or an LLM-powered AI agent would be the more appropriate solution, and why.

- **Scenario 1:** A system that automatically turns off the lights in an office building at 7 p.m. every weekday.
- **Scenario 2:** A system that responds to customer email inquiries, categorizes them, and escalates complex cases to a human, learning from past interactions.
- **Scenario 3:** A system that flags financial transactions over $10,000 for manual review.

You have 2 attempts to answer.

## When should you build an agent?[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#When-should-you-build-an-agent)

**Note:** In this course, our focus will be on LLM-powered agents. Whenever we refer to an “agent,” we specifically mean an agent powered by a large language model (LLM).

Not every problem needs an agent. Sometimes, a simple script or rule-based automation is enough. Agents introduce complexity, cost, and often uncertainty, so it’s important to be strategic about when to use them.

You should consider building an agent when your use case involves complex decision-making, dynamic context, or flexible task execution that traditional automation struggles to handle. Below are three key signals that suggest an agent may be the right choice:

![Deciding when to build an LLM-powered AI agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Deciding when to build an LLM-powered AI agent")

Deciding when to build an LLM-powered AI agent

### The task requires contextual decision-making[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-task-requires-contextual-decision-making)

Agents shine in situations where outcomes depend on nuanced judgment. If your workflow involves interpreting ambiguous input, balancing trade-offs, or adjusting behavior based on prior interactions, an agent can outperform static rules.

An example of this can be a refund approval process that depends on the customer’s past behavior, the tone of their message, and the reason for return. A rule-based system might miss important cues, while an agent can reason through the situation like a support representative would.

### The rules are too complex to maintain[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-rules-are-too-complex-to-maintain)

Some systems grow so large and fragmented that updating them becomes a liability. When your logic involves dozens of conditional branches, exception cases, and special handling for edge conditions, agents offer a more maintainable alternative.

An example of this can be a vendor security review process with evolving compliance requirements and unstructured documentation. Instead of encoding every possible case in logic, an agent can read and interpret the documents as part of the workflow.

### The workflow relies on unstructured or natural language data[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-workflow-relies-on-unstructured-or-natural-language-data)

Agents are uniquely equipped to parse and reason over unstructured data such as documents, emails, and conversations. If your pipeline needs to extract meaning from natural language, an agent may significantly reduce manual effort.

For example, consider an insurance claim intake process where customers describe events in their own words. An agent can extract relevant entities, ask follow-up questions, and route the case accordingly.

Before committing to building an agent, it’s crucial to validate that your use case clearly meets these criteria. If a deterministic solution can suffice, it may be a more appropriate approach.

## Summary[#](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Summary)

AI agents are autonomous systems that perceive, reason, and act to achieve goals. Unlike AI models, which are passive and task-specific, agents operate over time, maintain context, and take initiative.

We explored three types of agents: software-based, physical, and hybrid. We also examined how agent design has evolved from rule-based logic to LLM-powered flexibility.

Agents are most useful when tasks involve complex decisions, dynamic context, or unstructured data. Understanding when and why to build agents sets the stage for designing them effectively.

Agent Architecture: Core Agent Components

Ask

[What is an AI agent?](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#What-is-an-AI-agent)

[AI models vs. AI agents](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#AI-models-vs-AI-agents)

[Three categories of AI agents](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Three-categories-of-AI-agents)

[Software-based agents (sandbox environment)](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Software-based-agents-sandbox-environment)

[Physical agents (embodied systems)](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Physical-agents-embodied-systems)

[Hybrid and adaptive agents (real-world integration)](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Hybrid-and-adaptive-agents-real-world-integration)

[Evolution from rule-based systems to LLM-powered agents](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Evolution-from-rule-based-systems-to-LLM-powered-agents)

[Rule-based agents: Fixed logic, limited flexibility](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Rule-based-agents-Fixed-logic-limited-flexibility)

[Learning-based agents: Trial and feedback](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Learning-based-agents-Trial-and-feedback)

[LLM-powered agents: Generalization through language](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#LLM-powered-agents-Generalization-through-language)

[When should you build an agent?](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#When-should-you-build-an-agent)

[The task requires contextual decision-making](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-task-requires-contextual-decision-making)

[The rules are too complex to maintain](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-rules-are-too-complex-to-maintain)

[The workflow relies on unstructured or natural language data](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#The-workflow-relies-on-unstructured-or-natural-language-data)

[Summary](https://www.educative.io/courses/agentic-ai-systems/introduction-to-ai-agents#Summary)