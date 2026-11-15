# Case_Study_on_Automating_Support_Agents_for_Meridian_Telecom

Source: https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Case Study: Support Agents for Meridian Telecom

Explore how to approach a real-world AI system design case study for Meridian Telecom's support agents. Learn to analyze assignment briefs, prioritize workflows, propose piloted automation under realistic constraints, and prepare clear presentations. Understand the importance of discovery, defining metrics, handling pilot tests, and revising plans based on feedback and changing requirements.

We'll cover the following...

- [How do we read the brief?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-read-the-brief)
- [Which questions change the plan?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Which-questions-change-the-plan)
- [Which workflow goes first?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Which-workflow-goes-first)
- [How do we define success with Meridian?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-define-success-with-Meridian)
- [What does the design look like?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-does-the-design-look-like)
- [What did the replay show?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-did-the-replay-show)
- [How do we present it?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-present-it)
- [How do we handle pushback and a changed requirement?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-handle-pushback-and-a-changed-requirement)
- [What did this case stress?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-did-this-case-stress)
- [Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Try-it-yourself)
- [What’s next?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Whats-next)

This case study focuses on the take-home assignment and presentation stages. Approach it as a real assessment: review the brief, make your own decisions before checking the example responses, and rehearse your presentation aloud at the end.

On Monday, you receive the following assignment brief:

Meridian Telecom receives 12,000 support contacts a month: 7,200 by phone and 4,800 by chat. A person handles every contact today, and the median handling time across both channels is eight minutes. Representatives look up the account in the account console, read the relevant policy in the knowledge base, handle or route the request, and record a disposition in the ticket system. Contacts fall into four categories: billing questions, service interruptions, plan changes, and account access. Meridian’s support leader wants an agent system that automates 70% of contacts and reduces handling time. Propose a first release and present it.

The 70% target is the first thing most candidates build around. It is also the first thing that falls apart under questioning.

## How do we read the brief?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-read-the-brief)

Before designing anything, we sort every line of the brief into three buckets.

Sort the lines yourself first, then check your answers against the table.

Here’s the sorted brief to check your answers against:

|  |  |
| --- | --- |
| **Bucket** | **Meridian’s Brief** |
| Facts | 12,000 contacts a month, the 7,200/4,800 channel split, the eight-minute median, the five-step workflow, three systems |
| Asks | 70% automation, shorter handling time |
| Gaps | Category volumes, outcome quality, what a service may read or change, identity verification, who would run the system |

A plan that treats an assumption as a verified fact is difficult to defend when questioned. The eight-minute median measures handling time across all contacts. It does not establish whether those contacts were resolved or how an AI agent would perform.

The target to "automate 70%" could refer to three different outcomes.

- **Deflected:** The customer completes the interaction without reaching a human agent. This may reduce human-handled contacts, but it does not establish that the customer's issue was resolved.
- **Answered:** The system provides a response. That response may be incomplete or incorrect, and the customer may still need further assistance.
- **Resolved:** The customer's issue meets agreed resolution criteria, including any required follow-up period. Meridian has not yet defined those criteria.

Each metric requires a clearly defined denominator, eligibility criteria, and baseline. Until Meridian defines the target metric and agrees on eligible contact types, the 70% goal should guide discovery rather than serve as a launch acceptance criterion.

The brief also includes a review of 30 closed contacts. Eight contacts were marked as resolved. In three of those eight cases, the same customer contacted support again within seven days.

These follow-up contacts show that a resolved status alone is insufficient to confirm that the original issue remained resolved. The review does not establish why those customers returned, whether their new contacts concerned the same issue, or how frequently this occurs across Meridian's 12,000 contacts.

The proposal might claim: "The resolved status proves we can automate 70% of contacts and eliminate repeat contacts." Meridian has not yet evaluated an AI agent, so the available data cannot establish its expected automation or resolution rate. A defensible proposal should report the observed findings and recommend further discovery before defining measurable targets.

## Which questions change the plan?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Which-questions-change-the-plan)

Good discovery questions are the ones whose answers would change the recommendation.

|  |  |
| --- | --- |
| **Question** | **Why It Matters** |
| What identity verification must happen before a system reads an account? | Without an accepted method, all account-specific automation is blocked |
| Who approves the official answer when policy guidance conflicts? | Without approved guidance, even general answers may be wrong |
| Which integrations exist, and what may a service read or change? | A console representatives use doesn’t mean a service may use it |
| Who reviews drafts, takes escalations, and covers failures? | Available staff is a good sign, but staffing needs a commitment |
| Which mistakes hurt customers most? | A wrong general answer, another customer’s bill, and an unauthorized plan change need different boundaries |

Discovery then produces a deliberately varied sample of 60 contacts. Because Meridian chose them to show how workflows differ, the counts don’t estimate the full population.

- 28 account-specific billing contacts, such as “why is my bill higher this month?”
- 20 general billing-guidance contacts, answerable from policy alone.
- 12 plan-change contacts.

Four of the 20 general-guidance contacts depended on policy guidance that reviewers couldn’t reconcile. Automated identity verification and live integration access are unconfirmed. Representatives could review drafts, but Meridian hasn’t committed staffing or a fallback.

## Which workflow goes first?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Which-workflow-goes-first)

Each candidate has a different blocker:

|  |  |  |  |
| --- | --- | --- | --- |
| **Workflow** | **Value** | **Blocker** | **Decision** |
| Account-specific billing | High | Needs verified identity and authorized account access, neither of which exists | Defer |
| Plan changes | High | Adds a consequential action on top of identity and access | Defer |
| General billing guidance | Moderate | Needs approved guidance and a human route for the 4 conflicting cases | First release |

The recommendation is chat drafts for general billing questions, reviewed by a representative before anything reaches the customer. It holds only if Meridian accepts the scope, supplies approved guidance, and commits staff to run it.

Weight the criteria however you like and watch what changes, and what doesn’t.

A weighted scoring matrix might rank account billing first on value. No score turns a missing permission into a permission. Identity verification and account access are prerequisites, not points to trade away.

## How do we define success with Meridian?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-define-success-with-Meridian)

Success is agreed before anything runs. The proposal is a pilot of 40 eligible chat contacts alongside a separately observed manual comparison of 40 contacts from the same workflow and channel. The eight-minute baseline covers every contact type in both channels, so it can’t be the comparison.

|  |  |
| --- | --- |
| **Measure** | **How It’s Counted** |
| Eligibility | Contacts screened, judged eligible, and excluded with reasons, with all screened contacts as the denominator |
| Draft quality | Each draft labeled supported, unsupported, or unclassifiable against approved guidance; the target is zero unsupported answers sent |
| Escalation | Missed escalations over contacts that required one; unneeded escalations counted separately |
| Handling time | Both medians with their usable counts and the timing definition, monitored, not promised |
| Repeat contacts | Same-issue contacts within seven days, with unknowns counted as unknown, never as “no repeat” |

The trap this table avoids is the containment-only report. Picture a report that says “10 of 10 answered.” Two of those customers came back about the same issue within a week, and one request that met the escalation rule never reached a person. Counting all ten as successes hides both problems. That is why the 70% containment target can’t gate the first release: containment can rise while customers get poor answers, come back, or never reach a person.

## What does the design look like?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-does-the-design-look-like)

The design keeps the model inside a narrow boundary.

1. The application receives the representative’s request and screens it before any agent runs. A request is eligible only if it is a general question, an approved policy version covers it, and that guidance doesn’t conflict. If the application can’t confirm all three, the request goes to a person.
2. For an eligible request, a drafting agent calls one read-only tool that retrieves an approved, versioned policy excerpt, and returns a draft that cites it.
3. The representative reviews the draft, corrects it if needed, and sends it through the existing workflow.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27781%27%20height=%27190%27/%3e)![The application screens first; only eligible requests reach the agent](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "The application screens first; only eligible requests reach the agent")

The application screens first; only eligible requests reach the agent

A fixed screen-then-draft workflow with no separate triage agent is a credible design here. A triage agent that hands off to a specialist is the alternative, and it should earn its extra model call in a measured comparison.

A human escalation is a work item sent to a named recipient, who acknowledges it. It carries a short summary, the reason, and the relevant policy references, and leaves out anything the recipient doesn’t need. The application records the acknowledgment, because a sent message or an agent handoff doesn’t prove anyone received the work.

When a customer asks “why is my bill higher this month?”, the application screens it as account-specific and routes it to the representative. A specialist agent could produce a plausible answer, but only with account facts the pilot isn’t allowed to read, and a handoff between agents verifies nobody’s identity.

Plan changes are deferred. When they come, they will need the full action path from the Agents SDK lesson: an exact proposal, explicit approval of that proposal, a recheck of identity, permission, and account state at execution time, a single execution with an idempotency key, and reconciliation before any retry.

Voice comes in a later phase, starting with a chained pipeline so the transcript shows exactly what the system heard and the chat boundary carries over unchanged.

## What did the replay show?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-did-the-replay-show)

Before customer-facing rollout, run local replay tests that compare routing decisions against predefined expected outcomes.

- **Text routing:** Of 12 test cases, four general questions should produce drafts. Three account-specific, two plan-change, and three conflicting-guidance cases require human escalation. One conflicting-guidance case incorrectly produced a draft, so 11 of 12 routes matched the expected outcomes.
- **Voice state:** Of eight execution traces, two retained a pending confirmation after the user interrupted. Six of eight traces matched the expected behavior.

The chat pilot requires zero missed mandatory escalations. Because one case was incorrectly routed to drafting, the pilot does not meet its acceptance criterion.

An evaluator checking only the final response might have missed the failure because the draft appeared acceptable. Although a representative reviewed the draft, that review did not satisfy the required escalation workflow. The case required escalation to a designated owner authorized to resolve the conflicting guidance. Instead, the representative received a draft without any indication that the underlying instructions contradicted each other.

A plausible draft based on conflicting guidance may pass a routine review if the conflict is not made visible.

Review the four proposed next steps and decide whether each should proceed, be held pending further evidence, or be blocked.

## How do we present it?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-present-it)

Lead with the decision, then walk the five parts, then the ask.

“My recommendation is no chat pilot yet. I’d first fix the conflicting-guidance route and re-verify it, and get approved guidance, a staffed fallback, and named owners.  
  
Meridian handles 12,000 contacts a month and wants 70% automation. The eight-minute median covers everything, and nobody has defined what ‘automated’ means, so I started with discovery.  
  
The first release is chat drafts for general billing questions, reviewed by a representative. The application screens for eligibility and approved guidance, a drafting agent cites a versioned policy excerpt, and anything account-specific, ambiguous, or conflicting goes to a person who has to acknowledge it. No account access, no writes, no unreviewed replies, no voice.  
  
The text replay matched 11 of 12 routes, but the miss was a conflicting-guidance case that should have gone to the escalation route. The voice replay matched 6 of 8. Neither is a production result, and the 40-versus-40 comparison hasn’t run.  
  
I’m proposing that support operations own review and fallback, a policy owner maintain approved guidance, and customer engineering own access and telemetry. None of them has agreed yet. What I need from Meridian is a decision on those owners and a definition of ‘resolved’ we can measure.”

## How do we handle pushback and a changed requirement?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-handle-pushback-and-a-changed-requirement)

**Interviewer:** “Eleven of twelve is a strong result. Why not launch the pilot and monitor the exception?”

**Weak answer:** “It’s over 90%, so we can launch and fix missed routes as they come up.”

**Strong answer:** “The gate is zero missed human routes, because that case skipped the escalation route that settles conflicting guidance and reached ordinary review looking like a normal draft. I’d fix the screen and rerun those cases plus a held-out set. The pilot measures the workflow once the fallback and owners exist. It doesn’t create them.”

Then the interviewer changes the requirement.

**Interviewer:** “Meridian now wants weekend voice support next month, with representatives still reviewing guidance. In an escalation rehearsal, 11 of 14 work items were acknowledged and 3 weren’t. What do you recommend?”

Three work items reached nobody, which is a new blocker on top of the interruption failures. A strong revision walks the five parts again: weekend phone demand is real, since 7,200 contacts a month come by phone; the voice design uses speech-to-text, the same reviewed drafting, then speech output; the unacknowledged items need investigating and the route needs fixing and retesting; and voice needs real audio tests that state replays can’t replace. The deliverable next month becomes an offline voice demo, not a live launch.

The interviewer may ask for a cost estimate under stated assumptions: 3,000 eligible tasks a month, a $0.018 primary call, $0.006 for orchestration, 0.1 fully billed primary retries per task, $0.002 in tools, and no caching. Per task, that is 0.018 + 0.006 + 0.0018 + 0.002 = $0.0278, or $83.40 a month. The strong answer then names what’s missing: transcription and speech charges, representative review time, and infrastructure, which may well cost more than the model calls.

## What did this case stress?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-did-this-case-stress)

The take-home and presentation stage rewards three habits that this case exercised.

- Reading the brief into facts, asks, and gaps before designing.
- Leading with a decision that already accounts for its weakest evidence.
- Revising the whole plan when a requirement changes, instead of bolting the change on.

## Try it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Try-it-yourself)

Rewrite the two-minute recommendation for the weekend-voice requirement in five sentences: the decision, the design, the evidence with its denominators, the open blockers, and the ask. Then check it against three boundaries.

- It doesn’t promise a live voice launch next month.
- It names the 3 unacknowledged escalations and the 2 of 8 voice-state failures as separate blockers, each with its own retest.
- Its cost line gives $83.40 a month for model calls only, and names transcription, speech output, review time, and infrastructure as excluded.

If your draft blends the voice results into the 11 of 12 text result, start again.

AI Powered

Saved

8 attempts left

Reset

Statement

Four questions an interviewer could ask after this lesson. Answer each one as you would out loud: lead with your claim, then your evidence. The interviewer scores each answer against the lesson, gives feedback, and then asks the next question.

Let's start. Why can't Meridian's 70% automation target be the first release's success gate?

You have 8 attempts to answer.

## What’s next?[#](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Whats-next)

Meridian tested the presentation. The next case tests the technical round. The next lesson follows a wealth management firm whose advisors want a research assistant, and whose evaluation results disagree with what the sponsor believes about it.

The LLM Systems Round

Case Study: A Research Assistant for Aster Wealth

Ask

[How do we read the brief?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-read-the-brief)

[Which questions change the plan?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Which-questions-change-the-plan)

[Which workflow goes first?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Which-workflow-goes-first)

[How do we define success with Meridian?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-define-success-with-Meridian)

[What does the design look like?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-does-the-design-look-like)

[What did the replay show?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-did-the-replay-show)

[How do we present it?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-present-it)

[How do we handle pushback and a changed requirement?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#How-do-we-handle-pushback-and-a-changed-requirement)

[What did this case stress?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#What-did-this-case-stress)

[Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Try-it-yourself)

[What’s next?](https://www.educative.io/courses/forward-deployed-engineer/case-study-support-agents-for-meridian-telecom#Whats-next)