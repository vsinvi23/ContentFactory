# Agent_System_Design_for_Google_FDE_Interview_Preparation

Source: https://www.educative.io/courses/forward-deployed-engineer/agent-system-design

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Agent System Design

Explore a complete, worked system design for a telecom customer service agent, from data and tools to security, evaluation, and cost. Learn to handle common interviewer follow-up questions and distinguish strong answers from weak ones.

We'll cover the following...

- [Scope and success](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Scope-and-success)
- [Data and tools](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Data-and-tools)
- [Agent pattern](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Agent-pattern)
- [Architecture](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Architecture)
- [Permissions and guardrails](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Permissions-and-guardrails)
- [Evaluation and observability](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Evaluation-and-observability)
- [Deployment, scale, and cost](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Deployment-scale-and-cost)
- [Interviewer follow-ups](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Interviewer-follow-ups)

With the scope agreed, the Veltra engagement moves from what to build to how to build it. The first release covers billing explanations and outage status in chat and the mobile app, ticket creation and handoff to human agents, and agent assist for human billing agents, for one country and one language. The design has to work with an on-premises billing API, a five-minute outage feed, EU data residency requirements, and a CISO who will not approve automated financial actions.

This lesson presents a worked design for that release, structured the way a strong candidate would present it in a 60-minute system design round. It then covers follow-up questions an interviewer is likely to ask, with examples of weak and strong answers to each.

## Scope and success[#](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Scope-and-success)

A strong design opens by restating the scope and success criteria in a few sentences, so the interviewer and candidate agree on the target before any components appear.

The system resolves billing and outage questions for authenticated customers in chat and the mobile app, creates tickets when needed, and hands off to a human agent with a summary when it cannot help. Success means a higher share of billing chats resolved without a human, lower handling time on assisted contacts, customer satisfaction at or above the current baseline, and accuracy at or above an agreed threshold on a golden set of real billing and outage conversations.

## Data and tools[#](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Data-and-tools)

The agent needs three kinds of information and two kinds of action.

|  |  |  |
| --- | --- | --- |
| **Need** | **Source** | **Access method** |
| Customer’s bills, charges, and balance | On-premises billing system | Custom MCP server calling IT’s read-only middleware API |
| Outage status for the customer’s area | Network operations outage feed | Custom MCP server querying the feed by the postcode on the customer’s account |
| Billing policies and explanations | 400 current billing knowledge articles | Managed enterprise search over a curated data store |
| Create a ticket or callback request | CRM | MCP server exposing narrow ticket creation tools |
| Hand off to a human agent | Contact center platform | Handoff tool that passes a structured conversation summary |

Two design choices matter here. First, the retrieval data store contains only the 400 maintained billing articles, plus a small set of outage FAQs written for the pilot. The outdated articles are excluded rather than indexed and hoped for. Second, the outage tool looks up the postcode from the authenticated customer’s account rather than accepting a postcode from the conversation. This keeps the lookup tied to the customer’s identity and prevents the agent from being used to probe other areas.

## Agent pattern[#](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Agent-pattern)

The design uses a single ADK agent with five narrow tools. All tools share the same security boundary, are owned by the same delivery team, and serve one customer-facing workflow. None of the signals that justify multiple agents, such as separate ownership, separate permissions, or a tool set too large for one agent, is present. A single agent is faster, cheaper, and much easier to evaluate.

Agent assist for human billing agents is handled separately, through Google’s prebuilt contact center capabilities, provided Veltra’s contact center platform is compatible. It serves a different user, the human agent, inside a different tool, so keeping it separate from the customer-facing agent is a natural boundary rather than an added complexity.

## Architecture[#](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Architecture)

A customer signs in through the app or web chat, and the request passes through Apigee to the agent running on Agent Runtime in an EU region. Agent Runtime was chosen because Veltra’s IT team has limited experience operating containers at scale, and it provides managed sessions, memory, and integration with evaluation and observability. The custom MCP servers run on Cloud Run because they need private connectivity to on-premises systems, and Veltra’s IT team already deploys a small number of Cloud Run services.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%271156.725%27%20height=%27563.21427966%27/%3e)![Agen Observalibility](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Agen Observalibility")

Agen Observalibility

## Permissions and guardrails[#](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Permissions-and-guardrails)

The customer’s access token flows from the identity provider through the agent to each MCP server, so every billing lookup and ticket is scoped to the signed-in customer. The model never generates or sees the token.

A policy layer, implemented as an ADK callback, checks every tool call against the agreed risk tiers. Read actions and ticket creation run automatically and are logged. Service credits cannot be issued by the agent at all. When a customer asks for one, the agent creates a ticket that a human agent reviews. Model Armor screens inputs and outputs for prompt injection and sensitive data, VPC Service Controls keep data inside the approved perimeter, and logs pass through Sensitive Data Protection to mask personal information before storage.

## Evaluation and observability[#](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Evaluation-and-observability)

The golden set contains around 300 real billing and outage chats from the pilot country, labeled by senior contact center agents with the correct outcome, the expected tool calls, and whether handoff was appropriate. It includes common questions, difficult disputes, out-of-scope requests, and prompt injection attempts. A regression gate runs the golden set before every release and blocks deployment if task success, groundedness, or tool accuracy fall below the thresholds agreed with the sponsor.

In production, every conversation is traced end to end. Dashboards track resolution rate, handoff rate, latency, cost per conversation, and customer feedback. A weekly sample of conversations is scored by the same graders used in the golden set, and every confirmed failure is added to the golden set.

## Deployment, scale, and cost[#](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Deployment-scale-and-cost)

Outage spikes are the main scaling concern. Outage status is cached for each postcode for the five-minute refresh interval of the feed, so thousands of customers in the same area do not each trigger a separate lookup. The app also shows an outage banner when the feed reports an incident, which answers many questions before a conversation starts. Agent Runtime and Cloud Run scale automatically, and maximum instance limits protect the billing middleware from overload.

A rough cost estimate helps the sponsor plan. Chat and app handle about 40 percent of 1.2 million monthly contacts, and billing and outage contacts make up just over half of those, which gives roughly 250,000 eligible conversations per month across all three countries, or around 80,000 in the pilot country. At about six turns per conversation, with most turns on a Flash model, the model cost is in the range of one to two cents per conversation at typical Flash pricing, or roughly one to two thousand dollars per month for the pilot. The final figure must be confirmed with current pricing and measured pilot traffic, but even a rough number shows that model cost is small compared to contact center labor.

## Interviewer follow-ups[#](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Interviewer-follow-ups)

After the main design, interviewers probe specific decisions. The table below shows typical follow-ups with weak and strong answers.

|  |  |  |
| --- | --- | --- |
| **Question** | **Weak Answer** | **Strong Answer** |
| Why not a multi-agent design? | “Multi-agent systems are more scalable, so we could add one later.” | “All five tools share one security boundary and one owning team, and the tool set is small. A single agent is cheaper, faster, and easier to evaluate. If plan changes arrive with separate IT ownership and write permissions, that would be a reason to add a separate agent.” |
| Traffic triples during an outage. What happens? | “The system autoscales.” | “Outage status is cached per postcode for the feed’s five-minute refresh window, and the app banner deflects many questions before chat starts. The runtime scales automatically, and instance limits protect the billing middleware, which is the slowest dependency.” |
| A customer asks the agent to waive a late fee. What happens? | “The agent checks the policy and waives it if eligible.” | “Credits are high-risk and not automated in the pilot. The agent explains the fee, checks eligibility against the policy articles, and creates a ticket with a summary. A human agent approves or declines it. The policy layer blocks any direct credit call regardless of what the model decides.” |
| How do you know billing explanations are correct? | “Gemini is very accurate, and we would test it.” | “A golden set of 300 real conversations, labeled by senior agents, runs before every release. We measure groundedness against the billing articles and tool accuracy separately, so we can tell whether a failure comes from retrieval, the billing data, or the model’s reasoning.” |
| Leadership wants voice next quarter. What changes? | “We add speech-to-text and text-to-speech to the same agent.” | “Voice adds strict latency requirements and telephony integration. We would evaluate prebuilt voice capabilities first, measure end-to-end latency on the billing API, and expand only after the chat pilot meets its targets. The tools, policy layer, and golden set carry over.” |

The strong answers share a pattern. Each one ties the decision to a specific constraint from discovery, names the mechanism that enforces it, and acknowledges what would change the decision.

When an interviewer challenges a design choice, avoid defending it automatically. Restating the constraint that drove the choice, and explaining what would need to change for a different choice to make sense, shows the flexible judgment the role requires.

The Veltra design shows how the topics in this course combine into one coherent system. A single ADK agent on Agent Runtime uses narrow MCP tools, curated retrieval, and Gemini models chosen by task. Identity flows from the customer’s session to every tool, a policy layer enforces risk tiers in code, and evaluation and tracing are built in from the first release. Every choice traces back to a finding from discovery, and that traceability is what makes the design defensible to both Veltra’s stakeholders and a Google interviewer.

Case Discovery and Scoping

Case Debrief and Interview Follow-ups

Ask

[Scope and success](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Scope-and-success)

[Data and tools](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Data-and-tools)

[Agent pattern](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Agent-pattern)

[Architecture](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Architecture)

[Permissions and guardrails](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Permissions-and-guardrails)

[Evaluation and observability](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Evaluation-and-observability)

[Deployment, scale, and cost](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Deployment-scale-and-cost)

[Interviewer follow-ups](https://www.educative.io/courses/forward-deployed-engineer/agent-system-design#Interviewer-follow-ups)