# Scoping_the_MVP_for_Forward_Deployed_Engineer_Assignments

Source: https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Scoping the MVP

Define the smallest end-to-end workflow that meets all explicit requirements within the available time. Plan backward from the handoff deadline, build a walking skeleton that validates the end-to-end workflow, and reduce optional scope when implementation takes longer than planned while preserving time for testing, documentation, and handoff.

We'll cover the following...

- [Defining the MVP](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Defining-the-MVP)
- [Building a walking skeleton](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Building-a-walking-skeleton)
- [Prioritizing and recording cuts](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Prioritizing-and-recording-cuts)
- [Planning backward from handoff](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Planning-backward-from-handoff)
- [Testing the riskiest dependency](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Testing-the-riskiest-dependency)
- [Recovering from an overrun](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Recovering-from-an-overrun)
- [Practice: The support report](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Practice-The-support-report)
  - [Model plan and recovery](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Model-plan-and-recovery)

Supplier API integration has exceeded its estimated time by 30 minutes. Completing the required report functionality will take an estimated 15 more minutes. You also allocated 30 minutes to building a chart. Should you keep the optional chart and reduce the time allocated to recording and final verification, or remove the chart from scope?

First, review the fictional assignment to identify the requirements that must be completed within the time limit:

> - Build a local reorder report for a stock coordinator using `inventory.csv` and the supplied live supplier API.
> - The report should list every item whose stock is strictly below its reorder point, along with its supplier contact. Missing contacts and unusable input must look clearly different from successful results.
> - Submit focused checks, a documented way to run the tool with one command, a README, and a recorded walkthrough of no more than three minutes.
> - You have a maximum of 240 minutes of active work. API credentials and documentation are provided. Hosting, login, and charts are not required.

## Defining the MVP[#](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Defining-the-MVP)

The **minimum viable product (MVP)** is the smallest usable workflow that satisfies the required acceptance criteria within the constraints. Calling a submission an MVP does not authorize removing explicit obligations.

Protect the connected customer workflow and the evidence needed to inspect and run it; spend optional scope when implementation overruns.

For this assignment, completion means CSV input through live enrichment to an inspectable reorder report, followed by the requested verification and handoff. Use these supplied records:

- **P10:** Stock 2, reorder point 5, supplier S1
- **P11:** Stock 5, reorder point 5, supplier S2
- **P12:** Stock 0, reorder point 3, supplier S3

The supplied API test account contains S1 with contact `purchasing@example.test` and no contact for S3. Its paginated responses must be traversed to establish the lookup results.

The expected completed report includes P10 with its contact and P12 with an explicit unresolved-contact status. P11 is excluded because `5 < 5` is false. An unreadable CSV produces a clear failure rather than a success report. These are planned expected results, not executed software or live-call results.

## Building a walking skeleton[#](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Building-a-walking-skeleton)

A local command is enough: Read the CSV, select qualifying rows, enrich their supplier IDs through the live API, and write a readable report. Nothing in the brief requires a browser interface.

A **walking skeleton** is a thin, executable path from input to visible output. It establishes that the parts connect while leaving required behavior to complete. Building that path early exposes connection problems before individual components consume the budget.

Use P10 for the first connected-path milestone: Read its CSV row, retrieve S1 through the live API, and display P10 with `purchasing@example.test`.

Choose the strongest walking-skeleton checkpoint, then identify what still needs completing before the submission meets the brief.

Connected, not complete

Q1. Which proposed checkpoint would provide the strongest evidence of a walking skeleton for this inventory report? These are hypothetical checkpoints, not claims of executed live calls. Select one.

Do you find this helpful?

Use these as two separate planning gates: “the parts connect” and “the required submission is complete.” Passing the first gate justifies further implementation, not a completion claim. Otherwise, early success on P10 can hide unfinished obligations until the delivery reserve is already gone.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27721%27%20height=%27371%27/%3e)![Complete planned workflow and evidence](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Complete planned workflow and evidence")

Complete planned workflow and evidence

## Prioritizing and recording cuts[#](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Prioritizing-and-recording-cuts)

Classify the work by priority before allocating time:

- **Must-have:** Work required to meet explicit requirements and deliver a functional end-to-end workflow. This includes record selection, live supplier-data enrichment, an inspectable report, visibility into incomplete results, targeted tests, reproducible execution, a README, and a recording.
- **Nice-to-have:** An optional improvement that is not required by the brief. The low-stock chart has an estimated implementation time of 30 minutes.
- **Stretch:** Work attempted only after all required functionality and delivery checks are complete. Interactive filtering belongs in this category.

Document omitted capabilities and simulated behavior separately.

Record the following scope exclusions and simulation status:

- **Cut C1:** Omit hosted deployment because the brief requires local execution.
- **Cut C2:** Omit multi-user authentication because the brief does not require shared access.
- **Cut C3:** Omit scheduled refresh because the report runs on demand.
- **Stub status:** Do not use simulated responses in the live report workflow. Deterministic supplier fixtures may be used for targeted tests, with results explicitly labeled as fixture-mode.

If a development path returns fake supplier responses, add a stub entry identifying that path and its simulated contacts. Fixture output cannot satisfy the required live enrichment. Neither assumptions nor stubs change the brief’s requirements.

## Planning backward from handoff[#](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Planning-backward-from-handoff)

Work backward from the handoff. Reserve **75 minutes**, calculated as `25 + 25 + 15 + 10`, for checks and fixes, README completion, recording, and clean-clone verification. Budgeting writing and handoff before implementation helps keep them inside the timebox.

The complete initial schedule is:

1. **Discovery and plan (15 minutes):** Confirm criteria and access instructions; draft README headings, expected results, and cut/stub notes. Exit with a written scope and budget.
2. **Walking skeleton (30 minutes):** Connect P10 from CSV through live S1 lookup to visible output. Exit with that inspectable result.
3. **Supplier API risk (45 minutes):** Establish retrieval of all needed supplier IDs across paginated responses. Exit with the expected S1 contact and visibly unresolved S3 result.
4. **Required report behavior (45 minutes):** Complete all-row selection, contact coverage, incomplete-result display, and meaningful input failure. Exit with the expected three-row classification and unreadable-input behavior available for checking.
5. **Optional chart (30 minutes):** Add only if required behavior is complete. Exit with a chart consistent with the report, or a recorded cut.
6. **Focused checks and fixes (25 minutes):** Check selection boundaries, contact handling, input failure, and report contents. Exit with recorded results and any remaining failures identified.
7. **README completion (25 minutes):** Finish prerequisites, execution, usage, modes demonstrated, limitations, cuts, and stubs. Exit with an inspectable handoff document.
8. **Recording (15 minutes):** Record and review a walkthrough of at most three minutes showing the workflow and important failure behavior. Exit with an accessible recording.
9. **Clean-clone and handoff check (10 minutes):** Follow the documented execution path and verify submission access and artifact presence. Exit with checked handoff evidence or accurately reported gaps.

The durations total `15 + 30 + 45 + 45 + 30 + 25 + 25 + 15 + 10 = 240` minutes. These allocations are instructional choices, not employer standards.

**One-command reproducibility** means execution from a clean clone after documented prerequisites, without hidden local state or embedded credentials. Reserve time to check this explicitly: A successful run in your existing development folder can conceal missing configuration or files.

## Testing the riskiest dependency[#](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Testing-the-riskiest-dependency)

The external dependency can invalidate the required workflow. After the narrow skeleton establishes connectivity, the risk block asks a more consequential question: Can the report obtain the contacts it actually needs and preserve missing-contact information?

A checkable risk checkpoint contains three parts:

- **Result:** Retrieve S1 and establish the unresolved S3 contact across the supplied paginated responses.
- **Evidence:** Inspect P10’s expected contact and P12’s unresolved status. A successful HTTP response alone is insufficient.
- **Decision:** If retrieval works, finish report behavior. If it fails, investigate within a bounded extension, consuming optional chart time first.

For this case, allow at most 30 additional minutes, ending at minute 120. If the required integration remains unavailable then, record the incomplete obligation and use the permitted clarification channel where useful. A labeled fixture can keep independent checks moving, but it supplies no evidence of live success.

## Recovering from an overrun[#](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Recovering-from-an-overrun)

Return to minute 150. A tempting recovery note says:

> Keep the chart. Move implementation later. Record and check the clean clone if time remains. Use cached sample contacts for the demo and describe it as live-integrated.

This displaces requested evidence with optional polish. The recording may be absent, hidden local configuration may remain undetected, and sample contacts cannot establish live enrichment.

Use the timeline’s original schedule to draft a revised budget separately. Include your chart decision and what you will do next at minute 150.

Repair the 240-minute plan after the API overrun

RequiredOptionalRequired delivery

0–15 · 15 minutes15–45 · 30 minutes45–90 · originally 45 minutes90–135 · 45 minutes135–165 · 30 minutes165–190 · 25 minutes190–215 · 25 minutes215–230 · 15 minutes230–240 · 10 minutes

Discovery and planRequired

Walking skeletonRequired

Supplier API riskRequired

Required report behaviorRequired

Optional chartOptional

Focused checks and fixesRequired delivery

README completionRequired delivery

RecordingRequired delivery

Clean-clone and handoff checkRequired delivery

Do you find this helpful?

The API block now costs `45 + 30 = 75` minutes. Removing the chart releases exactly 30 minutes, so the required implementation can move later without moving delivery:

1. **15 min:** Discovery and plan
2. **30 min:**  One-row walking skeleton
3. **75 min:** Supplier API risk and bounded extension
4. **45 min:** Required report behavior
5. **25 min:** Focused checks and fixes
6. **25 min:** README completion
7. **15 min:** Recording
8. **10 min:** Clean-clone and handoff verification

The revised total is `15 + 30 + 75 + 45 + 25 + 25 + 15 + 10 = 240`. At minute 150, finish the remaining 15 minutes of required implementation. Add cut C4: “Low-stock chart omitted to absorb the integration overrun and preserve required verification and artifacts.”

Replacing live contacts with fake contacts would remove a required behavior, so it is not an equivalent scope reduction. If another delay makes required work infeasible and no optional scope remains, report unmet criteria and modes demonstrated, use the permitted contact channel if useful, and stop at the stated limit. An honest incomplete submission remains different from a completed MVP.

## Practice: The support report[#](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Practice-The-support-report)

Use this independent practice brief:

> In 180 active-work minutes, build a local CSV report for a support lead. Select tickets whose status is `open` and whose `age_hours` is at least 48. Show unresolved invalid-age rows separately. Include focused checks, documented one-command execution, a README, and a recording of at most two minutes. No API, hosting, or login is required. A chart is optional.

Inputs are T1/open/48, T2/closed/80, and T3/open/unknown. Expected output is T1 in the follow-up set, T2 excluded, and T3 visibly unresolved.

Suggested estimates are discovery 10 minutes, walking skeleton 20, risky age validation 25, remaining required implementation 35, optional chart 20, checks 25, README 20, recording 15, and clean-clone/handoff verification 10. They total 180 minutes. Validation then takes **20 extra minutes**.

Assess the planning claims in the memo reviewer, then write your own prose delivery plan covering its requested checkpoints, records, and budgets. Attempt it before comparing with the model below. No code is required.

Support-Ticket Delivery Plan

Your task

You are planning a local CSV report for a support lead within 180 active-work minutes. Write an independent delivery memo, not code. Include the customer workflow and observable completion criteria; must-have, nice-to-have, and stretch categories; separate cut and stub records; a connected-path milestone; an age-validation checkpoint with evidence and an end-of-block decision; a complete initial budget; and a revised budget after validation takes 20 extra minutes. The planning claims below also need scrutiny before they inform your memo.

Tap any claim to classify it, and click on References to verify authorities.

TOSupport leadFROMDelivery plannerDATEOctober 19, 2026SUBJECTLocal support-ticket report within 180 minutes

Background

Build a local CSV report selecting tickets whose status is `open` and whose `age_hours` is at least 48. Show invalid-age rows separately as unresolved. Supply focused checks, documented one-command execution, a README, and a recording of at most two minutes. No API, hosting, or login is required; a chart is optional.

Issue

Use T1/open/48, T2/closed/80, and T3/open/unknown. Suggested effort estimates are discovery 10 minutes, walking skeleton 20, age validation 25, remaining required implementation 35, optional chart 20, checks 25, README 20, recording 15, and clean-clone/handoff verification 10. These total 180 minutes. Validation subsequently requires 20 extra minutes.

Analysis

Planning claim to assess: The support brief uses the inventory report's strict boundary rule, so T1 at exactly 48 hours should be excluded.

Planning claim to assess: A delivery exception in the support brief permits replacing the README and clean-clone check with a chart when validation overruns.

Planning claim to assess: If the program runs successfully once, age validation is proven complete; a demonstration with T3 silently replaced by a numeric age can be presented as evidence for the required workflow.

Conclusion

The memo must distinguish required behavior from optional improvements and stretch work. It must also keep omitted capabilities and reasons in a cut record, separate from a stub record identifying any simulated behavior and its limitations. An explicit “No stubs” entry is appropriate when nothing is simulated.

Recommendation

Write a plan with observable exits for each block. Establish an early connected path from T1's CSV row to visible follow-up output. Reserve time for focused checks, README completion, the recording, and clean-clone/handoff verification, including execution using the documented one-command path after documented prerequisites.

Do you find this helpful?

### Model plan and recovery[#](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Model-plan-and-recovery)

The initial schedule using those estimates is:

- **0–10:** Discovery and artifact notes.
- **10–30:** Connected path using T1, from CSV to visible follow-up report.
- **30–55:** Age-validation risk checkpoint.
- **55–90:** Remaining required implementation.
- **90–110:** Optional chart.
- **110–135:** Focused checks and fixes.
- **135–155:** README completion.
- **155–170:** Recording.
- **170–180:** Clean-clone and handoff verification.

Define a risk exit condition that verifies the required behavior: “Verify that T1 qualifies at the 48-hour boundary, T3 remains visible as unresolved without a calculated age, and processing produces an inspectable report.” This verifies the required behavior rather than simply confirming that 25 minutes were allocated to validation.

Remove the optional chart from the time budget. Document hosting and login as unnecessary scope, the chart as an optional feature removed to protect delivery, and the stub status as “No stubs” if no behavior is simulated. Required tests should verify that T2 is excluded and that invalid input produces an error rather than a successful report with no results.

Evaluate the plan against five criteria: end-to-end workflow completion, coverage of explicit requirements, budget feasibility, measurable risk-resolution outcomes, and separate documentation of scope cuts and simulated behavior. Alternative time allocations are acceptable if the estimates are justified and all required functionality and deliverables remain covered.

Define these verification checkpoints for your assignment before choosing the implementation tools. Which familiar, minimal technology stack will support the required workflow and make the implementation easy to review?

Handling Ambiguity and Documenting Assumptions

Choosing a Stack and Project Structure

Ask

[Defining the MVP](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Defining-the-MVP)

[Building a walking skeleton](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Building-a-walking-skeleton)

[Prioritizing and recording cuts](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Prioritizing-and-recording-cuts)

[Planning backward from handoff](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Planning-backward-from-handoff)

[Testing the riskiest dependency](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Testing-the-riskiest-dependency)

[Recovering from an overrun](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Recovering-from-an-overrun)

[Practice: The support report](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Practice-The-support-report)

[Model plan and recovery](https://www.educative.io/courses/forward-deployed-engineer/scoping-the-mvp#Model-plan-and-recovery)