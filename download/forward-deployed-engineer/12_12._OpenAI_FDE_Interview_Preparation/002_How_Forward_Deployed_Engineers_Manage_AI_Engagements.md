# How_Forward_Deployed_Engineers_Manage_AI_Engagements

Source: https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Inside the FDE Team: How an Engagement Runs

The engagement process for OpenAI FDEs involves navigating complex interactions with various teams while managing customer expectations. Effective communication is crucial; messages must clearly outline problems, consequences, evidence, requests, and follow-through to avoid ambiguity. FDEs must identify decision-makers and ensure that each phase of engagement is backed by specific evidence. Observational visits to customers can yield valuable insights that enhance collaboration and decision-making. Ultimately, successful FDEs demonstrate ownership of outcomes by articulating clear responsibilities and tracking progress meticulously.

We'll cover the following...

- [Who does an OpenAI FDE work with?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Who-does-an-OpenAI-FDE-work-with)
- [Why did the broadcast message fail?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Why-did-the-broadcast-message-fail)
- [How does one engagement run?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#How-does-one-engagement-run)
- [What did Cedar’s trial actually find?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-did-Cedars-trial-actually-find)
  - [Writing one escalation that works](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Writing-one-escalation-that-works)
- [What makes field feedback worth sending?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-makes-field-feedback-worth-sending)
- [What does embedding with the customer look like?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-does-embedding-with-the-customer-look-like)
- [How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#How-does-this-sound-in-an-interview)
- [Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Try-it-yourself)
- [What’s next?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Whats-next)

Cedar’s two-week trial concluded on Friday. The following Monday morning, the FDE shared this update in the engagement channel:

“Product, Research, Security, GRC, GTM: Cedar is blocked on several issues from the trial. Please fix before the HR desk rollout next week. I’ve told the sponsor we’re on track.”

By Thursday, nothing had moved. Everyone had read the message. Nobody had agreed to do anything, because the message never said what anyone was being asked to do.

An OpenAI FDE owns the outcome of an engagement, but almost none of the people who can unblock it report to them. Customer engineers control the customer’s systems. Domain specialists decide what a correct answer looks like. Several OpenAI teams own pieces the FDE needs. Interviewers probe this directly, often with some version of: how do you move a blocked deployment through people you don’t manage?

## Who does an OpenAI FDE work with?[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Who-does-an-OpenAI-FDE-work-with)

[OpenAI’s posting](https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/) says FDEs work closely with Product, Research, Partnerships, GRC, Security, and GTM teams. It does not publish reporting lines or say that every team joins every engagement, so the useful skill is knowing what to bring to each one.

|  |  |
| --- | --- |
| **Team** | **What an FDE Typically Brings Them** |
| Research | A model behavior that reproduces outside the customer’s integration |
| Product | A recurring workflow need that might point to an OpenAI product surface |
| Security | A security concern that needs assessment before a connection is used |
| GRC (governance, risk, and compliance) | Assurance questions from the customer, and who can accept the answer |
| Partnerships | Coordination on the customer relationship beyond the engineering team |
| GTM (go-to-market) | How to describe scope and readiness so commercial expectations match what was proven |

Customer teams retain responsibility for their systems, data, and business decisions throughout the engagement. At Cedar, the IT team manages the ticketing system, the knowledge team maintains the FAQ, and service desk leads define the criteria for acceptable responses. Without clear ownership boundaries, an FDE may escalate issues to OpenAI that require decisions or changes from the customer's teams.

The teams listed in this table are examples of possible owners, not confirmed assignments. At the start of an engagement, confirm who has decision-making authority, who implements changes, and who handles operational issues.

## Why did the broadcast message fail?[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Why-did-the-broadcast-message-fail)

Before reading the diagnosis, review the Monday message and identify every phrase that fails to specify a clear action for the reader.

The Monday message conveyed urgency but assigned no clear actions. It mentioned five teams without identifying a specific problem, providing supporting evidence, or requesting a decision or action. It also described delivery as "on track" without confirmation from the teams responsible for the outstanding work.

An actionable escalation includes five elements:

1. **Problem:** State the specific issue observed.
2. **Consequence:** Explain how the issue affects delivery or the customer's workflow.
3. **Evidence:** Include the observations, logs, or test results that support the issue.
4. **Request:** Specify the decision, action, or assistance required.
5. **Follow-through:** Identify who will track progress and confirm resolution.

Record one additional detail separately: whether the recipient has accepted responsibility for the requested action. Adding a deadline to a request does not make it an agreed commitment. Until the responsible owner accepts the action, keep it marked as unassigned or awaiting acceptance in the delivery plan, and report that status accurately to the sponsor.

## How does one engagement run?[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#How-does-one-engagement-run)

The posting describes the work as scoping, sequencing delivery, removing blockers early, and trading off scope, speed, and quality to protect delivery. In practice, an engagement moves through phases, and each phase ends with a specific piece of evidence.

|  |  |  |
| --- | --- | --- |
| **Phase** | **What Happens** | **What Ends It** |
| Discovery and scoping | Learn the real workflow, agree what is in and out of scope | A written scope the customer accepts |
| Build on approved data | Build against data the customer approved for the purpose | A working system and a versioned eval set |
| Trial | Real users, narrow scope, fallback in place | Measured results against the agreed targets |
| Readiness | Fix what the trial found, verify live connections and owners | Evidence for each launch condition |
| Rollout and handoff | Widen in steps, transfer operation | The customer’s team running it without the FDE |

Delays often arise during transitions between delivery phases: a delayed system integration, an untested review process, or an owner who has not accepted responsibility. Three milestones are particularly important to distinguish.

A working integration means the connected workflow is available for testing, not that testing is complete. Verified readiness means the agreed launch criteria have been met. Accepted rollout means an authorized customer decision-maker has approved deployment. Each milestone requires separate evidence.

Review each delivery phase, then select only the readiness milestones supported by Cedar's recorded evidence.

## What did Cedar’s trial actually find?[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-did-Cedars-trial-actually-find)

Four staff handled 40 requests over two weeks. The headline was 34 of 40 drafts accepted, or 85%. That number hides where the problems are, so we split it by request type.

|  |  |  |
| --- | --- | --- |
| **Request Type** | **Drafts Accepted** | **What Went Wrong?** |
| Routine FAQ questions | 28 of 28 | Nothing |
| Policies changed in the last two weeks | 4 of 8 | The tool’s FAQ copy was older than Cedar’s live FAQ |
| Reimbursement limits | 2 of 4 | Two drafts stated the wrong limit even with the correct FAQ entry supplied |

The overall acceptance rate is `(28 + 4 + 2) ÷ 40 = 85%`, while the reimbursement category has an acceptance rate of just `2 ÷ 4 = 50%`. Reporting only the overall 85% acceptance rate would hide the weaker results for reimbursement questions, where incorrect amounts could have financial consequences.

The trial revealed two additional findings. Median handling time was 4.8 minutes, above the 4.5-minute target but below the 6-minute baseline. Staff reported spending additional time checking reimbursement amounts. Before the HR desk rollout, Cedar's security lead also raised a data-handling question: Does OpenAI retain employee names included in support tickets?

Each finding requires a specific next action and an appropriate owner. Escalating every issue broadly to OpenAI would repeat the Monday message's mistake of leaving responsibilities unclear.

Review the four findings and select the most appropriate owner for each next action. Then read the explanation for each choice.

### Writing one escalation that works[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Writing-one-escalation-that-works)

Here’s finding 2 rewritten in the five-part form, after a controlled replay:

**Problem:** Drafts state the wrong reimbursement limit on two request types.  
  
**Consequence:** Staff re-check every amount, which keeps handling time above target, and the HR rollout depends on amount accuracy.  
  
**Evidence:** With the correct FAQ entry supplied directly, the integration bypassed, and instructions and model settings held fixed, both cases produce the wrong limit in 5 of 5 runs. Sanitized inputs and outputs attached.  
  
**Request:** Can Research investigate whether this is a known behavior, and suggest any configuration we should test?  
  
**Follow-through:** I’ll track this and supply more cases if needed. Local containment ships this week regardless.

The controlled replay is what makes this report useful. Because the problem reproduces without Cedar’s integration, someone at OpenAI can investigate it without access to Cedar’s systems. It supports an investigation. It does not prove anything about the model’s internals.

The local containment matters as much as the report. Research may take weeks. In the meantime, the FDE proposes a deterministic check to Cedar: any draft that states an amount must match the figure in the cited FAQ entry, or the request goes to the manual process. Passing that check confirms the amount matches its source. It does not prove the rest of the draft is right.

## What makes field feedback worth sending?[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-makes-field-feedback-worth-sending)

The posting asks FDEs to share field feedback that helps Research and Product understand where the models succeed and where they fall short. Feedback earns attention when someone else can rerun it.

A report someone can act on contains:

- The workflow consequence, in one sentence.
- The observed set, with counts: 2 of 4 reimbursement cases, reproducing 5 of 5 times.
- The controlled replay conditions.
- A sanitized representative input with its expected and actual output.
- The exact model identifier, settings, and instruction version, copied from the run record and never from memory.
- Steps to reproduce, and the specific request.

Sanitizing needs one more check. After replacing employee names and amounts with approved stand-ins, rerun the cases and confirm they still fail. A sanitized case that no longer reproduces the problem is not evidence.

The posting also asks FDEs to codify working patterns into tools, playbooks, or building blocks. Cedar’s amount check is a candidate: an eval pattern for “amounts in drafts must match their cited source” applies to any customer drafting from policy documents. The pattern travels; Cedar’s data stays with Cedar.

Product can also hear recurring needs, such as staff wanting drafts inside their ticketing tool. That goes in clearly labeled as a customer request. It creates no roadmap commitment, and the FDE should never tell the customer that it does.

## What does embedding with the customer look like?[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-does-embedding-with-the-customer-look-like)

The posting lists travel of up to 50%. Time on site pays off when it produces evidence or decisions that a video call would miss. For Cedar’s next visit, a useful agenda looks like this:

- Watch staff use the tool without coaching them, and time where the minutes go.
- Sit with the knowledge team to agree how FAQ updates reach the tool, and who owns that step.
- Agree with Cedar’s IT team which systems the HR desk version may read, and who authorizes the connection.
- Get names for the operating owner, the incident owner, and the person who approves the HR rollout.

None of these items is “demo the new version.” A visit spent presenting produces applause. A visit spent observing and deciding produces the inputs the next phase needs.

## How does this sound in an interview?[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#How-does-this-sound-in-an-interview)

**Interviewer:** “Your deployment is blocked on three teams you don’t manage. What do you do?”

**Weak answer:** “I’d escalate to all the relevant teams with a clear deadline and keep the sponsor updated that we’re on track.”

**Strong answer:** “I’d split the blockers by owner first. At Cedar, the stale FAQ was the customer’s knowledge team, the wrong reimbursement limits went to Research only after a controlled replay showed they reproduce without our integration, and the data-retention question went to Security and GRC for an authoritative answer. Each request named the problem, the consequence, the evidence, and what I needed, and I tracked acceptance separately. While Research looked at the model behavior, we shipped a local check that routes any mismatched amount to the manual process.”

**Interviewer:** “The sponsor asks if you’re on track. What do you say?”

**Strong answer:** “I’d say which items are closed, which have an accepted owner and a date, and which are still waiting for acceptance. ‘On track’ is only true for the first two groups.”

The strong answer is specific about ownership. It never claims another team’s commitment before that team made it.

## Try it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Try-it-yourself)

Recall an escalation you sent in the past year that received no response. Rewrite it using the five-part structure: problem, consequence, evidence, request, and follow-through. Then identify the person who needed to accept responsibility for the requested action.

AI Powered

Saved

8 attempts left

Reset

Statement

Four questions an interviewer could ask after this lesson. Answer each one as you would out loud: lead with your claim, then your evidence. The interviewer scores each answer against the lesson, gives feedback, and then asks the next question.

Let's start. Why does a message addressed to several teams with a deadline often fail to unblock a deployment?

You have 8 attempts to answer.

## What’s next?[#](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Whats-next)

With the reimbursement check in place, Cedar's sponsor wants to expand the assistant to the HR desk and proposes an additional capability. The sponsor wants the assistant to analyze employee messages, identify individuals who may be experiencing burnout, and send their managers a weekly list of names.

The next lesson examines how OpenAI's AI principles and deployment safeguards inform decisions about which customer requests to implement, modify, or decline.

What an OpenAI FDE Owns

OpenAI’s Mission, Charter, and Deployment Philosophy

Ask

[Who does an OpenAI FDE work with?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Who-does-an-OpenAI-FDE-work-with)

[Why did the broadcast message fail?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Why-did-the-broadcast-message-fail)

[How does one engagement run?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#How-does-one-engagement-run)

[What did Cedar’s trial actually find?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-did-Cedars-trial-actually-find)

[Writing one escalation that works](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Writing-one-escalation-that-works)

[What makes field feedback worth sending?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-makes-field-feedback-worth-sending)

[What does embedding with the customer look like?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#What-does-embedding-with-the-customer-look-like)

[How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#How-does-this-sound-in-an-interview)

[Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Try-it-yourself)

[What’s next?](https://www.educative.io/courses/forward-deployed-engineer/inside-the-fde-team-how-an-engagement-runs#Whats-next)