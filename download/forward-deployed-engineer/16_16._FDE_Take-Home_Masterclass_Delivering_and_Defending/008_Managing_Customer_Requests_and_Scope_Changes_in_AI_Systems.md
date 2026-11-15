# Managing_Customer_Requests_and_Scope_Changes_in_AI_Systems

Source: https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Customer Role-Play and Scope Changes

Clarify an urgent, loosely defined customer request to identify the underlying task and its success criteria. Present scope options with clear trade-offs, avoid committing to accuracy targets without supporting evaluation evidence, and document the agreed scope, constraints, and next steps in a written handoff. Keep the customer's primary objective central to scope decisions.

We'll cover the following...

- [Uncovering the real need](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Uncovering-the-real-need)
- [Handling unsupported accuracy targets](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Handling-unsupported-accuracy-targets)
- [Presenting scope options](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Presenting-scope-options)
- [Confirming who approves changes](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Confirming-who-approves-changes)
- [Writing the handback](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Writing-the-handback)
- [Practice: the equipment request](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Practice-the-equipment-request)

You are nearing the end of a support-review take-home assignment. The read-only CSV report runs successfully and retains every exported request. You have **120 minutes of active work remaining**, allocated as follows:

- **45 minutes:** Build an optional chart.
- **15 minutes:** Refine the visual presentation.
- **40 minutes:** Run verification checks.
- **20 minutes:** Complete the handoff.

Before you finish, the support supervisor sends a new request:

> “Urgent delivery complaints are being missed. Before tomorrow, add automatic routing at 99% accuracy.”

First, identify the customer task that must succeed tomorrow, the consequences of failure, and which parts of the existing implementation can change. Evaluate routing libraries only after clarifying the requirements and agreeing on scope.

Translate the customer's request into an agreed, feasible scope with measurable acceptance criteria. Avoid committing to outcomes that the available evidence cannot substantiate.

Public interview scenarios illustrate requirements discovery, late scope changes, and written handoffs. Their suggested timings and evaluation criteria are illustrative, not requirements shared by all employers.

## Uncovering the real need[#](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Uncovering-the-real-need)

Start by acknowledging the consequence. Then ask questions whose answers change the delivery decision.

> **Engineer:** “It sounds like the main risk is missing an urgent complaint. What happens if one is missed? How does your team currently review complaints?”

> **Supervisor:** “A delivery issue might not receive follow-up until the next day. I manually review about 40 exported requests before 16:00. I cannot miss requests already marked urgent.”

> **Engineer:** “For tomorrow, do you need every request marked urgent identified for review, or must the tool also assign teams automatically? What data can I access for this exercise? Are you authorized to approve changes to the remaining scope?”

> **Supervisor:** “Identifying urgent requests for review is the priority tomorrow. There is no authorized live helpdesk access for this exercise. I can provide a CSV export and approve replacing optional presentation work, but I cannot authorize live integration.”

> **Engineer:** “Then the immediate goal is to identify requests marked urgent without removing other requests from the report. Is automatic assignment required, or was it one possible way to improve the review?”

This exchange establishes six decision inputs:

- **Affected workflow:** The supervisor manually reviews exported requests.
- **Failure consequence:** A delivery complaint may wait until the next day.
- **Deadline:** Review must happen before 16:00 tomorrow.
- **Available access:** An authorized export, without live help desk access.
- **Decision authority:** The supervisor can remove optional presentation work.
- **Observable success:** Explicitly urgent requests are available for review, with every request still visible.

The feature request has now become a bounded workflow proposal. The supervisor still needs to approve its exact behavior and trade-off.

## Handling unsupported accuracy targets[#](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Handling-unsupported-accuracy-targets)

> **Supervisor:** “Fine, but I still want 99% accuracy.”

Before responding, decide what that number would need to describe:

Responding to the 99% Request

Q1. The supervisor says, “Fine, but I still want 99% accuracy.” No routing evaluation is supplied, and missed urgent complaints are the concern. Which response best supports a defensible commitment?

Do you find this helpful?

Before committing to an accuracy target, define the task, evaluation population, metric denominator, error costs, and supporting evidence. High team-assignment accuracy does not establish how many urgent requests were missed, particularly when routine requests dominate the dataset.

> **Engineer:** “What does the 99% target measure: urgent-request detection, team assignment, or automated replies? Which errors are unacceptable?”
>
> **Supervisor:** “Missing urgent requests is the concern.”
>
> **Engineer:** “Without routing evaluation results, I cannot substantiate a 99% routing-accuracy commitment. For this delivery, I propose a deterministic check: Every supplied record with the exact priority value `urgent` must appear in the urgent-review list. All requests remain available for manual review, including those with unknown priorities. This check does not establish whether the source data correctly identifies every genuinely urgent request. Before committing to automated routing, I would define a separate evaluation using representative cases and agreed measures for missed urgent requests and incorrect classifications.”

The engineer addresses the customer's concern, distinguishes verified behavior from uncertainty, and proposes a narrower, testable acceptance criterion. Ensure each acceptance criterion measures the behavior being promised.

## Presenting scope options[#](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Presenting-scope-options)

For this exercise, implementing the urgent-review list and its acceptance checks is estimated to take 60 minutes. Reserve another 40 minutes to run verification checks against the complete report and 20 minutes for the handoff.

Present three scope options with their time requirements and tradeoffs:

- **Option A:** Retain the current plan. Optional chart (45 minutes) + visual refinements (15 minutes) + verification (40 minutes) + handoff (20 minutes) = **120 minutes**. The urgent-review list is not added.
- **Option B:** Prioritize urgent review. Urgent-review list and acceptance checks (60 minutes) + verification (40 minutes) + handoff (20 minutes) = **120 minutes**. Defer the optional chart and visual refinements.
- **Option C:** Deliver the urgent-review list, chart, and visual refinements. Urgent-review list and acceptance checks (60 minutes) + chart (45 minutes) + visual refinements (15 minutes) + verification (40 minutes) + handoff (20 minutes) = **180 minutes**. This exceeds the remaining allowance by 60 minutes and is feasible only if an authorized extension is granted.

None of these options includes automated routing or live help desk integration. Additional time does not provide integration authorization or evidence of routing accuracy.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27819.45%27%20height=%27288.90000000000003%27/%3e)![Option B keeps verification and handoff within 120 minutes. The full scope would need 180](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Option B keeps verification and handoff within 120 minutes. The full scope would need 180")

Option B keeps verification and handoff within 120 minutes. The full scope would need 180

> **Engineer:** “I recommend Option B because it addresses your urgent-review requirement within the remaining 120 minutes. We would defer the chart and visual refinements. We would still follow access restrictions, validate the input, complete verification, and report the results accurately.”

> **Supervisor:** “Can you keep the chart too? Leadership expects something visual.”

> **Engineer:** “Keeping the urgent-review list and chart, even without visual refinements, would require 165 minutes, including verification and handoff. That exceeds the remaining allowance by 45 minutes. Within the current allowance, we can retain the original chart plan or prioritize the urgent-review list and defer the presentation work. Which outcome should take priority?”

The engineer presents feasible alternatives and asks the supervisor to prioritize the outcome.

Compare this with an unsupported commitment:

> “Absolutely, we can add automatic routing, achieve 99% accuracy, and keep the chart by tomorrow.”

That promise has no defined accuracy denominator or evaluation, no authorized live access, no budgeted routing implementation, no displaced work, and no customer confirmation of the tradeoff. Spending the 40-minute verification reserve would leave the delivery less checked while resolving none of those uncertainties.

A rigid “That is out of scope” also leaves the customer without a decision. The useful alternative is: “We can prioritize the urgent-review lane within the same time if we move out the chart and polish; is that the tradeoff you want?”

## Confirming who approves changes[#](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Confirming-who-approves-changes)

> **Engineer:** “Missed urgent complaints sound like the immediate risk. What happens when one is missed, and how does your team review them today?”
>
> **Supervisor:** “A delivery problem can go without follow-up until the next day. I manually review about 40 exported requests before 16:00. I cannot miss requests already marked urgent.”
>
> **Engineer:** “For tomorrow, is success finding every explicitly urgent request for your review, or must the system assign teams automatically? What data access is authorized, and can you approve changes to the remaining work?”
>
> **Supervisor:** “The review is what matters tomorrow. There is no authorized live helpdesk access for this exercise. I can supply an export and approve replacing optional presentation work, but I cannot grant integration access.”
>
> **Engineer:** “Then the immediate task is to make explicitly urgent requests easy to review while keeping every request visible. Is automation essential tomorrow, or is it your suggested way to achieve that?”
>
> **Supervisor:** “A review view would help if I can trust its inclusion rules.”

A proposed scope cut does not silently cancel an explicit obligation. Here, the supervisor confirms both that the removed work is optional and that they authorize its removal. If the chart were required by the assessment, the engineer would need confirmation from whoever can revise that requirement; otherwise the obligation remains and the conflict must be reported.

## Writing the handback[#](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Writing-the-handback)

A **handback** is a concise written record of the delivery agreement, its dependencies, and the next checkpoint. Write it while the decisions are fresh so both sides can detect a misunderstanding.

> **Support review delivery:**
>
> - **Outcome:** Help the supervisor review urgent requests before 16:00 tomorrow, with every request still visible.
> - **Deliverable (Option B, approved):** A read-only full report plus an urgent lane for priority exactly `urgent`. Blank or unrecognized priorities are flagged for manual review. No automatic routing, messages or live integration.
> - **Removed (approved):** Optional chart and visual polish.
> - **Time:** 13:30–15:30 tomorrow. 60 min implementation, 40 min verification, 20 min handoff.
> - **Dependency:** The supervisor provides the CSV export at 13:30. If it’s missing, report it immediately and replan.
> - **Acceptance check:** R11 (`urgent`), R12 (`normal`) and R13 (blank) all stay in the full report. Only R11 goes in the urgent lane. R13 is flagged for review.
> - **Limits:** These are synthetic examples, not executed results. They don’t prove real urgency detection or routing accuracy.
> - **Checkpoints:** Status update at 14:30. Final handoff by 15:30.
> - **Proposed (not agreed):** Scope an automation evaluation separately.

The written record matches the spoken agreement. Its status words matter: Approval confirms the delivery change, while the automation evaluation remains proposed.

Now test whether the agreement survives a dependency failure.

13:30: The authorized export is unavailable

↓ Entry

📋Confirmed Option B

↓ Entry

📁Supervisor-owned export

🛠️Report implementation

↓ Entry

🧪Synthetic acceptance checks

🔍Connected-report verification

📤15:30 checked handback

106%

Failure simulator

Pick a component to knock out — see how far the damage spreads.⌀ badges show each node’s blast radius — the bigger the number, the closer it is to a single point of failure.

Do you find this helpful?

A missing export changes feasibility immediately. A synthetic file may support development, but substituting it silently would change what the customer receives and what the evidence means.

## Practice: the equipment request[#](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Practice-the-equipment-request)

Use a separate fictional rehearsal. A facilities coordinator manually assigns equipment requests. The current delivery is a read-only report retaining all requests.

There are 90 active-work minutes remaining:

- **Optional category chart:** 45 minutes
- **Formatting polish:** 15 minutes
- **Verification:** 20 minutes
- **Handoff:** 10 minutes

A safety-priority review view would require 60 implementation minutes, including adding its checks. The coordinator says: “Keep the chart, add automatic assignment, and guarantee no safety request is missed.”

Use the stakeholder response card supplied with the rehearsal; it provides facts, not approval of your recommendation. Audit the analysis paragraphs as draft claims, not established facts. Prepare a short spoken discovery-and-negotiation response, then record its transcript and a concise proposed handback in the empty sections.

Equipment Request — Proposed Scope Review

Your task

You are the engineer negotiating a read-only equipment-request report with the facilities coordinator. The coordinator asks: “Keep the chart, add automatic assignment, and guarantee no safety request is missed.” Prepare a short response aloud, then record its transcript and a concise proposed handback. Use the stakeholder card below; it supplies facts, not approval. The analysis paragraphs are draft claims to audit before using them in your response.

Tap any claim to classify it, and click on References to verify authorities.

TOFacilities coordinatorFROMDelivery engineerDATEFictional rehearsalSUBJECTProposed safety-review scope within 90 active-work minutes

Background

**Stakeholder response card:** The immediate goal is reviewing requests explicitly marked `safety` before 15:00. The coordinator can authorize removal of the optional category chart and formatting polish. Tracker write access is unavailable. No assignment or safety-detection evaluation exists. The coordinator can provide an authorized CSV export at the start. The consequence of a missed safety request has not been supplied. This card does **not** approve a scope change.

Issue

**Spoken response transcript:**

**Proposed handback:**

Analysis

The earlier support-review Option B establishes the equipment plan: 60 minutes for implementation, 40 for verification, and 20 for handoff. We can therefore offer that plan within this scenario’s 90-minute boundary.

The stakeholder card contains the coordinator’s approval to remove the chart and polish, so the handback can begin “Confirmed” without another question.

If E21/`safety` enters the safety view and E23/blank receives a manual-review flag, these examples prove that no real safety request will be missed and justify automatic assignment.

The proposed read-only report retains every exported record. Only records whose priority is exactly `safety` enter the safety view; blank or unrecognized priorities remain visible and receive a manual priority-review flag. Expected behavior: E21/`safety`, E22/`routine`, and E23/blank all remain in the full report; E21 alone enters the safety view; E23 is flagged.

Conclusion

The feasible proposal replaces the optional chart and polish with the safety-review view while protecting verification and handoff. Delivery remains conditional on an authorized export at the start and explicit stakeholder confirmation. The consequence of a missed safety request remains an open discovery question.

Recommendation

Seek confirmation of the outcome, proposed deliverable and checks, displaced optional work, 90-minute boundary, and a start and delivery time that allow review before 15:00. Name the coordinator as export owner, state the evidence limits and no tracker write-back, and propose a next checkpoint after the 60-minute implementation period. If the export is unavailable at the start, report the blocker and replan rather than silently substituting synthetic data.

Do you find this helpful?

Before sending the written handoff, verify whether its status is Proposed or Confirmed. Use Confirmed only when an authorized stakeholder has approved the scope. Otherwise, label it Proposed.

Handling Live Extension Exercises

Common Take-Home Mistakes

Ask

[Uncovering the real need](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Uncovering-the-real-need)

[Handling unsupported accuracy targets](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Handling-unsupported-accuracy-targets)

[Presenting scope options](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Presenting-scope-options)

[Confirming who approves changes](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Confirming-who-approves-changes)

[Writing the handback](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Writing-the-handback)

[Practice: the equipment request](https://www.educative.io/courses/forward-deployed-engineer/customer-role-play-and-scope-changes#Practice-the-equipment-request)