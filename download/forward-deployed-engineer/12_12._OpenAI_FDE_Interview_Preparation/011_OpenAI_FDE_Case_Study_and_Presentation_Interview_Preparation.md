# OpenAI_FDE_Case_Study_and_Presentation_Interview_Preparation

Source: https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Case Study and Presentation

Explore how to prepare and present a strong case study for OpenAI FDE interviews. Learn to identify customer needs, scope a first release with clear limitations, package your work effectively, and confidently defend your design decisions in live presentations.

We'll cover the following...

- [What does the case stage test?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-does-the-case-stage-test)
- [How do we read the brief?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-read-the-brief)
- [How do we scope the first release?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-scope-the-first-release)
- [What goes in the submission?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-goes-in-the-submission)
  - [What do the stale records change?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-do-the-stale-records-change)
- [How do we present a recommendation that survives questions?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-present-a-recommendation-that-survives-questions)
- [How do we handle pushback?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-handle-pushback)
- [How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-does-this-sound-in-an-interview)
- [Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#Try-it-yourself)
- [What’s next?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#Whats-next)

The candidate’s first slide read: “Recommendation: pilot with Northstar operators next month.” Below it, in large type: “10 of 12 evidence checks passed.”

The interviewer had read the appendix. “What happened in the other two?”

The other two were stale service records, older versions that should have been withheld, and the system had let them through to the drafting step. A draft built on stale evidence could tell an operator a technician was coming when the visit had been canceled. The candidate knew this. It was in their notes. It just wasn’t on the slide, and the recommendation on the slide didn’t account for it.

A coding task comes with a contract. A deployment case comes with a customer, and nobody says what to build. OpenAI’s [interview guide](https://openai.com/interview-guide/) lists take-home projects among possible assessment formats, and FDE candidates [report](https://www.theforwarddeployed.io/interviews/openai) a take-home case that they then walk through and defend live. The work is choosing a workflow, a first release, and the proof that release needs, then presenting it so the hardest question is already answered.

## What does the case stage test?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-does-the-case-stage-test)

[OpenAI’s FDE posting](https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/) covers the path from discovery and scoping to production rollout, and asks FDEs to sequence work and make trade-offs that protect delivery. A take-home case is a small window onto those same decisions. A strong submission is narrow and complete, and honest about its limits. A broad submission that hides its gaps tends to fall apart at the first follow-up.

Our actual assessment instructions decide the artifact, the format and the tools, along with the time we have. If anything is unclear, we ask the recruiter before starting.

## How do we read the brief?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-read-the-brief)

Before deciding what to build, identify five things in the assignment brief.

1. **Customer request:** What workflow needs to improve, and who will use the solution?
2. **Required deliverables:** What must you submit, such as code, documentation, or a demonstration recording?
3. **Permitted tools and assistance:** Which development tools, AI assistants, and external resources are allowed?
4. **Presentation requirements:** Who will review the work, how should it be presented, and what time limits apply?
5. **Unresolved requirements:** Which unanswered questions could materially affect the architecture, scope, or implementation?

Consider the following practice assignment. Northstar Equipment Services wants to reduce the time required to handle incoming service requests and needs a reproducible demonstration of the proposed solution. Currently, operators review each request, retrieve service records they are authorized to access, assess urgency, draft a response, and decide whether to escalate or close the request. Northstar requires operators to retain responsibility for the final escalation or closure decision.

Prioritize clarifying questions whose answers would affect the proposed design, implementation, or delivery plan.

|  |  |
| --- | --- |
| **Question** | **Why It Changes the Design** |
| Which operators may read which records? | Without an answer, the demo runs on test records only |
| What does it cost if an urgent request is treated as routine? | Tells us which mistakes need their own release gate |
| What must an operator see before accepting a draft? | Shapes the output and the review screen |
| What can the reviewer run, and which dependencies are allowed? | Shapes setup and reproducibility |
| Who defines labels, reviews outputs, and supports a pilot? | Decides whether a pilot is possible at all |

Every unanswered question becomes a written assumption. “Customer engineering will own identity configuration” is a proposal until customer engineering agrees.

## How do we scope the first release?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-scope-the-first-release)

The first release is an operator-reviewed, read-only triage draft. It reads a record the operator may see, suggests an urgency label from a fixed set, drafts a response, and routes anything uncertain to manual review. Operators keep the decision, and the system has no way to write tickets or message customers.

The tempting alternative closes tickets or sends messages on its own. That version needs authorization rules for actions, approval controls, a way to observe what it actually did, and an operating process, and the brief settles none of them. A polished interface can’t stand in for those decisions.

The cut list belongs in the presentation, not hidden. “I didn’t build automatic closing, because it needs action controls and an owner the brief doesn’t give us” is a scoping decision. Leaving it unsaid makes it look like an oversight.

## What goes in the submission?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-goes-in-the-submission)

Package the work as a runnable slice plus a short README that lets a reviewer reproduce and inspect it. Call it the artifact manifest.

- Setup and inputs: requirements, test records, the test identity, configuration.
- Command: the exact command and where to run it.
- Expected behavior: entitled inputs get a triage draft, and denied access, invalid labels, failed classification, and stale evidence all route to manual review.
- Actual results: the command we ran, the output we saw, and any failures.
- Limits: the test identity is not real authentication, and nothing writes tickets or sends messages.

Expected behavior and actual results stay in separate sections. A prediction written as a result is the fastest way to lose a reviewer’s trust.

If the brief asks for a recorded walkthrough, treat it as a customer demo with a technical audience. Show the scope decisions explicitly, run the failure cases on camera, and say what you would do next with more time.

### What do the stale records change?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-do-the-stale-records-change)

The practice brief includes one more piece of evidence: a 12-record stale-evidence check. Ten records took the intended review route. Two stale records were wrongly admitted to drafting.

That result decides the recommendation. A stale record can ground a draft in information that should have been withheld, so the honest recommendation is an offline demonstration only, with the defect shown openly and no pilot proposed yet. The fix is to check eligibility and freshness before any record reaches classification or drafting, then rerun the original 12 cases plus a separate holdout set.

Northstar’s pilot gates, proposed during discovery, make “not yet” concrete.

|  |  |  |
| --- | --- | --- |
| **Gate** | **Threshold** | **Status** |
| Triage quality | At least 22 of 24 labels match agreed references, and all 6 out-of-service cases are flagged urgent | Not yet run |
| Side effects | Zero ticket writes and zero customer messages in the evaluated workflow | Not yet verified |
| Stale evidence | Every stale record routed to manual review | Failing: 2 of 12 wrongly admitted |
| Pilot time | Median end-to-end handling time of at most 6 minutes in a representative pilot | Requires a pilot |

Work through the gates in order and watch the recommendation change.

## How do we present a recommendation that survives questions?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-present-a-recommendation-that-survives-questions)

Start with your recommendation, support it with evidence, and explain its limitations. Identify the limitations yourself rather than waiting for the interviewer to uncover them.

1. **Recommendation:** State what you propose, the strongest supporting evidence, and the main limitation in two sentences.
2. **Customer and problem:** Identify the users, the affected workflow, and the current operational cost or impact.
3. **Design:** Describe the proposed release, its capabilities and limitations, and what has been excluded from scope.
4. **Evidence:** Present each measured result with its sample size or denominator, and distinguish observed outcomes from projections.
5. **Risks and open questions:** Explain potential failure modes, pause or rollback conditions, and who has authority to make those decisions.
6. **Handoff and next decision:** Identify who will operate the system and what approval or decision is needed from the customer.

Draft your own opening recommendation before reviewing Northstar's example.

For Northstar, the opening sounds like this: “I recommend an offline demonstration of a read-only, operator-reviewed triage draft. It routes 10 of 12 stale-evidence cases correctly, but 2 stale records reached drafting, so I’m not proposing a pilot until the freshness check is fixed and re-verified.”

Here is the candidate’s original slide, with the evidence on file above it. Flag every line an interviewer could take apart.

## How do we handle pushback?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-handle-pushback)

The live portion often includes someone playing a skeptical stakeholder. Four challenges come up in some form, and each has a pattern for the answer.

- “Can we skip the review step to save time?” Acknowledge the cost of review, then name what would have to be true first: tested action controls, an owner, and evidence on representative cases. Offer to measure review time so the decision is based on data.
- “A competitor did this in two weeks.” Ask what they shipped and what it was allowed to do. Then restate what our gates require and how quickly we can meet them.
- “Can’t a better prompt fix the stale-record problem?” Explain where the defect lives: in the eligibility check before the model. A prompt change might hide the symptom on the test set and leave the stale record flowing to the model.
- “What would you do with another week?” Name the next gate in order, not a feature list: fix freshness, rerun with a holdout, then run the triage quality gate.

When a question reveals something we hadn’t considered, the strong move is to say so and adjust the recommendation on the spot. Defending an earlier answer against new evidence reads as poor judgment.

## How does this sound in an interview?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-does-this-sound-in-an-interview)

**Interviewer:** “Ten of twelve passed. Why aren’t you recommending a pilot?”

**Weak answer:** “83% is a good start, and we can monitor the pilot closely and fix issues as they come up.”

**Strong answer:** “The two failures are stale records that reached drafting, and a draft built on stale evidence can tell an operator something that’s no longer true. That’s a different class of failure from a wrong urgency label. The fix belongs in the eligibility check before the model, so I’d repair it, rerun the 12 cases plus a holdout set, and then run the triage quality gate. I’d propose a pilot once those pass and operations has agreed to run it.”

**Interviewer:** “The sponsor needs something to show leadership next week.”

**Strong answer:** “The offline demonstration is that something. It shows the drafts on test records, the manual-review routing working, and a clear list of what’s left before a pilot. That’s more useful to leadership than a pilot date we’d have to walk back.”

## Try it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#Try-it-yourself)

Take a project you know and write the first slide of a recommendation for it: one recommendation, the strongest evidence with its denominator, the most important limit, and the decision you need. If the limit doesn’t fit on the slide, the recommendation is probably too broad.

AI Powered

Saved

8 attempts left

Reset

Statement

Four questions an interviewer could ask after this lesson. Answer each one as you would out loud: lead with your claim, then your evidence. The interviewer scores each answer against the lesson, gives feedback, and then asks the next question.

Let's start. What five things should you pull out of a case brief before building anything?

You have 8 attempts to answer.

## What’s next?[#](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#Whats-next)

After the presentation comes the follow-up that goes deeper: “Show me exactly where the access check runs.” The next lesson prepares for the technical round on LLM systems, where an interviewer follows one decision down to the mechanism behind it.

The Coding Round

The LLM Systems Round

Ask

[What does the case stage test?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-does-the-case-stage-test)

[How do we read the brief?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-read-the-brief)

[How do we scope the first release?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-scope-the-first-release)

[What goes in the submission?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-goes-in-the-submission)

[What do the stale records change?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#What-do-the-stale-records-change)

[How do we present a recommendation that survives questions?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-present-a-recommendation-that-survives-questions)

[How do we handle pushback?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-do-we-handle-pushback)

[How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#How-does-this-sound-in-an-interview)

[Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#Try-it-yourself)

[What’s next?](https://www.educative.io/courses/forward-deployed-engineer/the-case-study-and-presentation#Whats-next)