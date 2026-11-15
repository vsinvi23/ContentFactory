# Master_Case_Discovery_and_Scoping_for_Google_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Case Discovery and Scoping

Explore how discovery findings turn a broad customer mandate into a focused, approvable first release. Learn to prioritize use cases by value and feasibility, apply risk tiers to agent actions, and run a build-versus-buy check before committing to a design.

We'll cover the following...

- [What discovery revealed](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#What-discovery-revealed)
- [Prioritizing use cases](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#Prioritizing-use-cases)
- [Applying risk tiers to Veltra’s actions](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#Applying-risk-tiers-to-Veltras-actions)
- [The build-versus-buy check](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#The-build-versus-buy-check)
- [The scoped first release](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#The-scoped-first-release)

The Veltra Telecom brief asked for an AI agent that handles customer service end to end and cuts contact center costs by 30 percent within six months. Taken literally, this request describes a project that would touch every channel, every contact type, and every backend system at once. It would also depend on an outdated knowledge base, an on-premises billing platform, and approvals from several teams. A project scoped this way is very unlikely to reach production on schedule.

Discovery and scoping turn a broad mandate into a first release that is valuable, buildable, and approvable. In Google’s FDE interviews, this step often separates strong candidates from weaker ones. Interviewers want to see a candidate gather the facts that matter, prioritize use cases deliberately, decide which actions are safe to automate, and check whether an existing product already solves part of the problem before proposing to build it. This lesson walks through each of these steps for Veltra.

## What discovery revealed[#](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#What-discovery-revealed)

The FDE team held a series of discovery sessions with Veltra’s stakeholders, using the questions identified from the brief. The sessions included the sponsor, IT, network operations, the CISO’s team, and a group of contact center agents. The key findings are summarized below.

|  |  |
| --- | --- |
| **Area** | **Finding** |
| Contact mix | Billing 32%, network and outages 20%, device issues 15%, plan changes 14%, roaming 9%, other 10% |
| Channels | Phone 60%, chat 30%, mobile app 10% |
| Billing system | A read-only API, provided through IT’s middleware, returns balances, invoices, and charges. Any write operation requires a formal IT change request. |
| Network status | Network operations publishes an internal outage feed, updated every five minutes, that can be queried by postcode |
| Knowledge base | About 40% of articles have not been updated in two years. The 400 billing articles are maintained by the billing team and are mostly current. |
| Cost target | The 30% figure is a leadership aspiration for the full program. The sponsor would treat a measurable reduction in billing handling time as pilot success. |
| Previous chatbot | It failed because it used rigid menus and could not pass context to human agents, so customers had to repeat themselves |
| Languages | Three languages across the three countries |
| Security | The CISO requires EU data residency, no automated financial actions in the pilot, and a full audit trail |

These findings change the picture considerably. Billing is the largest contact type, and its data is both accessible and reasonably current. Network outages drive the worst wait times, and outage data is already available through an API. Device troubleshooting, by contrast, depends heavily on the outdated part of the knowledge base, and plan changes require write access that IT has not yet approved.

## Prioritizing use cases[#](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#Prioritizing-use-cases)

With discovery complete, the next step is to compare candidate use cases on business value and feasibility. Value reflects contact volume, cost, and customer pain. Feasibility reflects data readiness, integration effort, and approval risk.

Billing explanations and outage status, both in chat and app, score high on value and feasibility. Billing is the largest contact type with a ready API and current articles, and outages drive the worst wait times with a feed that already exists. Agent assist for human billing agents scores medium on value but high on feasibility, since it helps the 60 percent of phone contacts without automating voice. Device troubleshooting is held back by outdated articles. Automated plan changes and a full voice agent are valuable but blocked, the first by write-access approval and the second by latency, telephony integration, and broad scope

The top-right quadrant shows where the first release should focus. Use cases with high value but low feasibility are not abandoned. They move to later phases, each with a clear dependency that must be resolved first, such as IT approval for write access or cleanup of the device articles.

## Applying risk tiers to Veltra’s actions[#](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#Applying-risk-tiers-to-Veltras-actions)

The next step is to decide which actions the agent may take and under what controls. Risk tiers make this decision explicit and give the CISO’s team a concrete artifact to review.

|  |  |  |
| --- | --- | --- |
| **Agent Action** | **Risk Level** | **Pilot Policy** |
| Explain a bill, charge, or balance | Read | Automatic, scoped to the authenticated customer |
| Report outage status for the customer’s area | Read | Automatic |
| Create a callback request or support ticket | Reversible write | Automatic, logged |
| Hand off to a human agent with a conversation summary | Reversible write | Automatic, logged |
| Apply a service credit | High risk | Not automated in the pilot. The agent prepares a request, and a human agent approves it. |
| Change a service plan | High risk | Out of scope for the first release |
| Cancel a service or transfer a number | High risk | Never automated |

This table addresses several concerns at once. It meets the CISO’s requirement that no financial actions run automatically. It fixes the previous chatbot’s biggest failure by making handoff with context a core capability. It also gives the sponsor a clear path for later phases, since plan changes can move into scope once IT approves write access and the pilot has built trust.

## The build-versus-buy check[#](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#The-build-versus-buy-check)

Before designing a custom system, an FDE checks whether an existing product already solves part of the problem. Building what could be bought adds delivery time, cost, and long-term maintenance for the customer. Buying what should be built can leave the customer with a tool that does not fit their systems or workflows.

Google Cloud offers Gemini Enterprise for CX, previously known as Customer Engagement Suite with Google AI, which provides prebuilt contact center capabilities such as conversational agents for customer self-service and agent assist for human agents. For Veltra, the check compares these capabilities against a custom agent built with ADK on Gemini Enterprise Agent Platform.

|  |  |  |
| --- | --- | --- |
| **Criterion** | **Customer Engangement Suit** | **Custom Agent** |
| Time to value | Faster for standard contact center patterns | Slower, since more is built from scratch |
| Integration with the on-premises billing API | Possible through connectors or tools | Full control through a custom MCP server |
| Fit with Veltra’s existing contact center platform | Depends on compatibility, which must be confirmed | Integrated through APIs |
| Agent assist for phone agents | Available as a core capability | Would need to be built |
| Custom billing explanation logic | Configurable within the product’s limits | Fully customizable |
| Ongoing ownership | Shared with the product | Owned by Veltra’s team |

The check points toward a hybrid approach. Prebuilt agent assist is a strong candidate for helping human agents on the phone channel, provided it is compatible with Veltra’s contact center platform. A custom ADK agent is a strong candidate for billing explanations and outage status, because these depend on Veltra’s specific billing API, outage feed, and explanation rules. The final decision depends on one open question: whether Veltra’s existing contact center platform integrates with Google’s prebuilt capabilities. The FDE team records this as a dependency rather than assuming the answer.

In interviews, a build-versus-buy check that ends with “it depends on one specific fact, and here is how we would confirm it” is stronger than a confident answer that ignores the customer’s existing systems.

## The scoped first release[#](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#The-scoped-first-release)

The outcome of discovery and scoping is a short scope statement that every stakeholder can review and approve.

- **Goal:** Reduce handling time and wait times for billing and outage contacts
- **Channels:** Chat and mobile app, plus agent assist for human billing agents
- **Market:** One country and one language, expanding after the pilot
- **In scope:** Billing explanations, outage status, ticket creation, and handoff with summary
- **Out of scope:** Voice self-service, plan changes, automated credits, device troubleshooting
- **Success metrics:** Share of billing chats resolved without a human, handling time on assisted contacts, CSAT at or above baseline, and accuracy on an agreed golden set
- **Dependencies:** Billing API and outage feed access, contact center platform compatibility, CISO approval
- **Timeline:** Pilot plan in four weeks, limited production release within three months

This scope does not promise the full 30 percent reduction in the first release. Instead, it targets the contact types that drive the most volume and the worst waits, using data and systems that are ready now. A successful pilot creates evidence and trust, which makes approval for later phases, such as voice and plan changes, far more likely.

Discovery and scoping turn Veltra’s broad mandate into a focused first release that can reach production. The FDE team used discovery to replace assumptions with facts, compared use cases on both value and feasibility, applied risk tiers to every action the agent could take, and checked existing products before deciding what to build. The result is a scope that the sponsor, the CISO, IT, and the contact center can all support, and it provides a clear foundation for designing the system itself.

The Telecom Case Brief

Agent System Design

Ask

[What discovery revealed](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#What-discovery-revealed)

[Prioritizing use cases](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#Prioritizing-use-cases)

[Applying risk tiers to Veltra’s actions](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#Applying-risk-tiers-to-Veltras-actions)

[The build-versus-buy check](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#The-build-versus-buy-check)

[The scoped first release](https://www.educative.io/courses/forward-deployed-engineer/case-discovery-and-scoping#The-scoped-first-release)