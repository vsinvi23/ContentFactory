# Designing_a_Claude_Deployment_for_an_EU_Telecom_Enterprise

Source: https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Final Panel Solution Design Walk-Through

Explore how to lead a final panel solution design for deploying Claude in a regulated environment. Understand how to scope problems, identify trade-offs, address security and compliance, and defend design choices for an enterprise telecom customer with strict EU data residency requirements.

We'll cover the following...

- [Taking control of the opening minutes](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Taking-control-of-the-opening-minutes)
- [Building the design layer by layer](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Building-the-design-layer-by-layer)
- [Choosing the deployment path for EU data](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Choosing-the-deployment-path-for-EU-data)
- [Defending the design under pushback](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Defending-the-design-under-pushback)
- [Closing with a design summary](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Closing-with-a-design-summary)
- [Leading the room from start to finish](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Leading-the-room-from-start-to-finish)

The solution design in Anthropic’s final panel asks a candidate to architect a Claude deployment for an enterprise customer. The prompt is short on purpose. The candidate is expected to lead by scoping the problem, naming trade-offs, and raising failure modes before the interviewer asks. Waiting for the interviewer to narrow the problem reads as a weakness at this level.

The panel also probes the parts of a deployment that sales demos skip. Those parts include security, compliance, where the data goes, and how anyone will know the system works. The walk-through below works through one regulated prompt from the first minute to the closing summary.

> A European telecom wants a Claude support agent that answers billing questions and makes simple account changes for its customers. Customer data must stay in the EU. How would you design it?

## Taking control of the opening minutes[#](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Taking-control-of-the-opening-minutes)

The first minutes decide whether the rest of the session builds on facts or guesses. We lead with the questions that change the architecture, and we ask them in a batch so the interviewer sees a plan.

- **Channels:** Chat in the app, a web widget, or voice. Voice adds speech handling and tighter latency limits.
- **Volume:** Conversations per day and the peak hour. This drives cost and capacity.
- **Account changes:** Which changes the agent may make, such as switching a plan or adding a data bundle, and which are reversible.
- **Identity:** How a customer proves who they are before the agent reads or changes anything.
- **The meaning of “in the EU”:** Whether the requirement covers inference, stored conversations, logs, or all three, and whether the UK and Switzerland count.
- **Success:** What the telecom measures today, such as resolution without a human, handling time, or complaints.

When the interviewer leaves a question open, we state an assumption and keep moving. A line such as “I’ll assume chat only, about 40,000 conversations a day, and reversible changes only” shows which assumptions carry weight. We then write a one-line scope where the interviewer can see it.

Ace Editor

1

2

3

Scope: A chat agent for logged-in customers that answers billing questions and makes

reversible plan changes, with inference, conversations, and logs kept in the EU.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The scope gives every later decision something to point back to, starting with the design itself.

## Building the design layer by layer[#](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Building-the-design-layer-by-layer)

A strong design comes together one layer at a time, with a reason for each choice. The table below lists the layers for this prompt and the decision at each one:

|  |  |
| --- | --- |
| **Layer** | **Decision** |
| Channel | The app’s existing chat, so customers are already logged in when the conversation starts |
| Agent | One Claude agent with a short system prompt that states the support policy |
| Read tools | `get_bill`, `get_plan`, and `explain_charge`, scoped to the logged-in customer |
| Write tools | `change_plan` and `add_bundle`, each one confirmed by the customer before it runs |
| Data access | The telecom’s existing billing APIs, called from the telecom’s own EU services |
| Evals | Answer accuracy on real billing questions, correct changes, and escalation precision |
| Monitoring | Resolution rate, handoffs to people, cost per conversation, and every write in an audit log |
| Escalation | A handoff to a human agent with a summary, for disputes, complaints, and anything unclear |

The account ID is the design’s most important detail. Code takes it from the customer’s login session and passes it to every tool, so Claude never chooses which account to read or change. A prompt injection or a confused answer still cannot reach another customer’s account.

The eval layer deserves the most time out loud. A panel wants to hear how we would prove the agent helps, so we name the metrics, the test set built from real past conversations, and the threshold that has to hold before launch.

The dashed border in that picture is the hardest part of the prompt, and it depends on how Claude is reached.

## Choosing the deployment path for EU data[#](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Choosing-the-deployment-path-for-EU-data)

Where Claude runs is a deployment decision with real constraints, and stating them precisely is one of the strongest signals in this prompt. Anthropic’s first-party Claude API offers two inference locations through the `inference_geo` setting, `"global"` and `"us"`. Data stored at rest in a workspace currently stays in the US. The first-party API therefore cannot meet a requirement to keep this customer’s data in the EU.

Two cloud platforms can. Each one is operated by the cloud provider inside its own infrastructure.

- **Amazon Bedrock:** Claude runs on AWS infrastructure with regional endpoints. An EU inference profile routes requests across AWS’s European regions.
- **Google Cloud (Google-managed):** Claude runs on Google’s infrastructure, and an EU multi-region endpoint routes requests within the EU.

Both options cost 10 percent more than each platform’s global endpoint. One detail is worth raising before the interviewer does. AWS’s EU geography includes London and Zurich, which sit outside the EU. If the telecom’s requirement means the EU in the strict sense, we pin a single EU region that serves the chosen model in-region, and we confirm that region on the model’s page before committing.

The platform choice also changes the rest of the design because the cloud platforms do not offer every first-party feature.

> **Features to check on Amazon Bedrock:**
>
> Claude in Amazon Bedrock supports the Messages API, prompt caching, tool use, citations, and structured outputs. It does not support the Message Batches API, the MCP connector, Agent Skills, the Files API, or Claude Managed Agents. Google Cloud keeps its own feature list, which a design checks the same way.

For this design, the gaps are manageable. The agent loop and its tools run in the telecom’s own EU services, calling Claude through the Messages API. Prompt caching remains available for the long system prompt. The design simply cannot lean on batch pricing or a hosted agent runtime, and a candidate who says so before the interviewer asks shows real deployment experience.

With the data path settled, the interviewer turns to pushback.

## Defending the design under pushback[#](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Defending-the-design-under-pushback)

Three kinds of pushback come up in almost every solution design. Each one deserves a short, specific answer tied back to the design.

The first is cost. The interviewer says the agent is too expensive at the telecom’s volume.

Let’s put a number on it. A conversation with 20,000 input tokens and 1,000 output tokens on Claude Sonnet 5.5 costs about 5.5 cents before caching, at list price plus the 10 percent regional premium. Most of those input tokens are the system prompt and tool definitions, which repeat on every turn, so caching cuts the input cost sharply. Simple balance questions can go to Claude Haiku 5.5, which costs a fraction of that. The comparison that matters is cost per resolved conversation against the cost of a human agent handling the same question.

The second is safety. The interviewer asks what happens if the agent changes the wrong account.

The agent can’t choose the account. Code takes the account ID from the customer’s login and passes it to every tool. Every change is reversible, the customer confirms it in the chat before it runs, and each write goes to an audit log. If a change is still wrong, support can undo it from the log.

The third is scope. The interviewer asks whether the agent can also issue refunds.

Refunds can come later, once the first version has earned trust. In version one, the agent recognizes a refund request and hands it to a human agent with a summary, so the customer never repeats themselves. When the eval data shows the agent explains charges correctly, we can add small refunds under a fixed limit, with a human approving anything above it.

Each answer accepts the concern, points to a specific part of the design, and offers a path forward. That pattern carries the panel into its final minutes.

## Closing with a design summary[#](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Closing-with-a-design-summary)

The last few minutes are for a summary the interviewer can repeat to the hiring committee. We state it in seven short lines.

Ace Editor

1

2

3

4

5

6

7

8

Scope: Chat agent for logged-in customers. Billing answers and reversible plan changes.

Design: One Claude agent, read tools and confirmed write tools, account ID set by code.

Data path: Claude on Amazon Bedrock in a pinned EU region, conversations and logs in EU services.

Evals: Answer accuracy, correct changes, escalation precision, all on real past conversations.

Rollout: Read-only answers first, then plan changes for a small share of customers.

Costs: About 5.5 cents per conversation before caching, measured against human handling cost.

Risks: Model availability per EU region, and features unavailable on Bedrock.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Ending with open risks matters. A design that names its own weak points tells the panel that we would raise them with the customer too.

## Leading the room from start to finish[#](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Leading-the-room-from-start-to-finish)

A final panel design is a test of ownership as much as architecture. We scope before drawing, write the decisions down where the interviewer can see them, and keep the riskiest details, such as who chooses the account and where the data runs, under the control of code and configuration. A precise answer about EU data shows the panel that we know the platform’s limits as well as its strengths. A candidate who leads the session this way shows the judgment a customer would trust with its own deployment.

Multi-Level Coding Round Practice

Security Alert Triage Case Study and Scoping

Ask

[Taking control of the opening minutes](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Taking-control-of-the-opening-minutes)

[Building the design layer by layer](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Building-the-design-layer-by-layer)

[Choosing the deployment path for EU data](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Choosing-the-deployment-path-for-EU-data)

[Defending the design under pushback](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Defending-the-design-under-pushback)

[Closing with a design summary](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Closing-with-a-design-summary)

[Leading the room from start to finish](https://www.educative.io/courses/forward-deployed-engineer/the-final-panel-solution-design-walk-through#Leading-the-room-from-start-to-finish)