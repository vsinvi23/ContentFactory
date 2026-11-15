# Scoping_and_Interpreting_FDE_Assignments_for_Effective_Solutions

Source: https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Reading the Brief

Identify the users, existing workflow, pain points, and constraints described or implied in an assignment brief. Distinguish explicit requirements from inferred needs and proposed implementation approaches, then translate validated requirements into testable acceptance criteria to ensure the implementation addresses the customer's requirements.

We'll cover the following...

- [Understanding the customer’s task](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Understanding-the-customers-task)
- [Which words create obligations?](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Which-words-create-obligations)
- [Writing testable acceptance criteria](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Writing-testable-acceptance-criteria)
- [Missing data and failures](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Missing-data-and-failures)
- [Brief versus preferred design](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Brief-versus-preferred-design)
- [Practice: the equipment brief](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Practice-the-equipment-brief)

A dispatch lead receives a chart showing order counts. The chart appears complete but does not identify which orders require follow-up. A list of orders requiring follow-up, with unresolved records clearly identified, would help the dispatch lead prioritize the morning’s follow-up tasks.

Identify the customer's task, document explicit requirements, and define measurable acceptance criteria before selecting an implementation approach. A feature list alone does not demonstrate that the solution provides the information needed to make the decision.

## Understanding the customer’s task[#](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Understanding-the-customers-task)

Consider this fictional brief:

> - Every morning, the dispatch lead reviews the daily order CSV, compares promised dates with the current date, and manually checks dispatch statuses to identify orders requiring follow-up. This manual process leads to missed follow-ups and repeated order checks.
> - Build a local tool that accepts an order CSV file and a run date as inputs. List all orders with a promised date earlier than the run date and a dispatch status other than `dispatched`. Include orders with missing promised dates in the output and flag them as unresolved.
> - Run the tool locally without transmitting CSV data to external services. Consider a dashboard as an optional interface.

Read it first for five things:

- **User:** The dispatch lead.
- **Current process:** Compare the daily CSV with today’s date, then manually check dispatch status.
- **Pain:** Missed follow-ups and repeated checking.
- **Constraint:** Operate locally without transmitting the CSV to external services.
- **Observable desired outcome:** Identify orders needing follow-up while seeing which records lack enough information to classify.

A **customer outcome** describes a task or decision improved. Here, the outcome is: “The dispatch lead can use the daily CSV and a supplied date to identify orders to chase and distinguish unresolved records.” This gives direction without inventing a time-saving target or committing to a dashboard, model, or framework.

## Which words create obligations?[#](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Which-words-create-obligations)

An **explicit obligation** is directly requested. An **inferred need** is reasoned from the workflow but is not automatically an agreed requirement. Preserve the wording or reasoning behind each interpretation so a reviewer can inspect the distinction.

A **constraint** limits acceptable delivery or behavior. An **implementation suggestion** proposes a means. An **optional improvement** adds capability beyond the requested obligations.

Apply those labels to the exact clauses:

- **Explicit input obligation:** “Build a local tool that accepts the CSV and a supplied run date.” The run date must be an input; silently using only the machine’s current date would miss that instruction.
- **Explicit classification obligation:** “List orders whose promised date is before the run date and whose status is not dispatched.” Both conditions must hold.
- **Explicit unresolved-record obligation:** “Keep records with missing promised dates visible as unresolved.” Those records must remain inspectable.
- **Constraint:** “Run locally; do not send the CSV to external services.” A constraint still carries a binding obligation; its label describes its role.
- **Implementation suggestion:** “A dashboard could be useful.” “Could” leaves the interface open. “Must provide a dashboard” would create an obligation.
- **Workflow-derived inferred need:** Keep order identifiers beside results, because the lead must locate the orders to chase. The brief does not explicitly request identifier visibility.
- **Candidate-proposed optional improvement:** Automatically email suppliers. This adds an action the brief never requests.

Customer empathy helps uncover the identifier need. It does not turn every plausible improvement into a customer requirement. Automatic emails could consume effort while leaving the requested classification unfinished.

## Writing testable acceptance criteria[#](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Writing-testable-acceptance-criteria)

An acceptance criterion defines the observable conditions that a requirement must meet to be considered complete. Specify the input conditions, expected behavior, and verifiable results. Use the format “Given this input, expect this result” to define testable behavior.

Use 2026-10-19 as the run date and the six-row test fixture below. Treat all dates as calendar dates without timezone conversion. Treat a blank promised date as a missing value.

|  |  |  |
| --- | --- | --- |
| **Order ID** | **Promised Date** | **Status** |
| S101 | 2026-10-17 | pending |
| S102 | 2026-10-18 | dispatched |
| S103 | 2026-10-19 | pending |
| S104 | blank | pending |
| S105 | 2026-10-18 | pending |
| S106 | 2026-10-20 | pending |

Before reading the worked result, apply both parts of the classification rule to the fixture.

Technical Quiz

1.

With a run date of 2026-10-19, which order below requires follow-up because its promised date has passed and its status is not dispatched?

**Note:** Orders with blank promised dates remain visible as unresolved but do not qualify for follow-up.

A.

S104: promised date blank

B.

S103: promised date 2026-10-19, status pending

C.

S101: promised date 2026-10-17, status pending

D.

S106: promised date 2026-10-20, status pending

---

1 / 1

Turn the classification decision into a check a reviewer can repeat:

- **Criterion:** Given the supplied CSV and run date 2026-10-19, the follow-up result contains exactly S101 and S105. S102, S103, and S106 receive no follow-up classification.
- **Source:** The date boundary and status condition come directly from the classification clause.
- **Workflow-derived proposal:** “Show each result’s order identifier.” The need to locate an order supports this criterion; the brief does not explicitly request it.
- **Evidence:** An inspectable output or exact-membership check can establish membership without requiring a particular screen or framework.

This separates required behavior from a proposed way to make it inspectable. These are expected checks for a hypothetical submission, not claims that software has been built or executed.

## Missing data and failures[#](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Missing-data-and-failures)

S104 has no promised date, so its overdue status cannot be determined. Classifying S104 as on time would rely on missing data, while excluding it would violate the requirement to retain unresolved records.

**Acceptance criterion:** Given S104 with a missing promised date, display it as unresolved and exclude it from the follow-up list. Displaying order identifiers allows the reviewer to locate S104 and verify its classification.

The expected results should account for all six records in the test fixture:

- Two follow-up candidates: S101 and S105.
- One unresolved record: S104.
- Three other classified records: S102, S103, and S106.

Distinguish missing values in a readable CSV from failures that prevent the CSV from being read. For an unreadable CSV, define the following failure criterion: “If the selected CSV cannot be read, display an error message identifying the file and do not generate a success report.” Mark this criterion as derived because the brief does not specify how to handle unreadable files.

**Failure criteria** define the expected system behavior when a workflow fails or cannot complete as intended. “Handle errors gracefully” does not specify the failure condition or expected response, making the requirement difficult to verify.

## Brief versus preferred design[#](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Brief-versus-preferred-design)

Consider this candidate interpretation:

> Success means a dashboard loads, shows two overdue orders, and uses an LLM to summarize them. Ignore rows without dates.

A screenshot showing a count of two does not verify that the correct orders were selected. For example, the result could include S101 and dispatched order S102 while omitting pending order S105. Excluding S104 violates the requirement to retain orders with missing promised dates as unresolved. The interpretation also incorrectly treats the dashboard and LLM as required components, although the brief does not mandate either.

Revise the interpretation by verifying each claim against the original brief and expected results in the test fixture.

Audit the Dispatch Interpretation

AI Analysis Report

Tag each sentence that hides a statistical bias, then submit your audit.

0 / 3 flagged

Audit this candidate interpretation: “Success means a dashboard loads, shows two overdue orders, and uses an LLM to summarize them. Ignore rows without dates.” Mark the problematic claims below, then write a short repair.

We select dashboard loading and an LLM summary as the evidence of success, rather than checking the requested order classifications.

The latest claimed screenshot shows count 2 with follow-up identifiers S101 and S102; because it is the newest evidence, we accept it as confirmation without comparing its membership with the fixture.

S104 is omitted because its promised date is blank; judging only rows with dates makes the result look complete.

The brief requires a local tool accepting the CSV and a supplied run date, follow-up classification only when the promised date is before that date and status is not dispatched, visible unresolved records for missing dates, and no CSV transmission to external services.

For run date 2026-10-19, the fixture is S101: 2026-10-17, pending; S102: an earlier date, dispatched; S103: 2026-10-19, pending; S104: missing promised date; S105: 2026-10-18, pending; S106: 2026-10-20, pending. In your repair, state exact follow-up membership, the equality boundary, unresolved handling, and whether identifier visibility is explicit or inferred.

Do you find this helpful?

The repair replaces a count-only check with exact membership, preserves the equality boundary at S103, and restores visible unresolved S104. It removes the invented LLM requirement and leaves the dashboard as a suggested interface.

A local table could satisfy the requested behavior. If the wording changed to “must provide a dashboard,” that same table alone would no longer satisfy the interface obligation. Wording determines which design choices remain open.

Use this audit chain for each criterion: Customer task, supporting clause or reasoning, expected behavior, inspectable evidence.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27802%27%20height=%27381%27/%3e)![Trace each customer task to its supporting wording or reasoning, acceptance criterion, and expected evidence, keeping inferred proposals distinct from explicit obligations](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Trace each customer task to its supporting wording or reasoning, acceptance criterion, and expected evidence, keeping inferred proposals distinct from explicit obligations")

Trace each customer task to its supporting wording or reasoning, acceptance criterion, and expected evidence, keeping inferred proposals distinct from explicit obligations

Distinguish requirements stated in the brief from proposed requirements derived through engineering judgment. If an acceptance criterion depends on a business rule not defined in the brief, such as whether orders with a new status of `cancelled` should be excluded from follow-up, document the ambiguity instead of introducing an unsupported rule.

Tests using the supplied fixture verify behavior for the specified cases. They do not demonstrate customer adoption, time savings, or production reliability, so limit conclusions to the behavior verified by the tests.

## Practice: the equipment brief[#](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Practice-the-equipment-brief)

Use a fresh fictional brief:

> Each Monday, the maintenance coordinator checks an equipment CSV and copies items into a follow-up sheet. Rechecking dates takes repeated effort. Build a local report showing equipment with next\_inspection\_date on or before a supplied review date. Show missing inspection dates separately as unknown. Keep the CSV on the local machine. A CLI would be acceptable.

Use review date 2026-11-02 and these records:

- **E201:** `next_inspection_date` = `2026-11-01`
- **E202:** `next_inspection_date` = `2026-11-02`
- **E203:** `next_inspection_date` = `2026-11-03`
- **E204:** `next_inspection_date` is blank

Review the proposed interpretation below and identify its errors. Then write a corrected, compact requirements interpretation covering the requested outcome, workflow, classifications, and acceptance criteria. Use this brief’s wording to determine the boundary; do not borrow the dispatch rule.

Equipment Report: Requirements Interpretation

Your task

You are interpreting a maintenance coordinator’s equipment-report brief before implementation. The interpretation should connect the coordinator’s weekly task to binding obligations and observable checks, without inventing business results.

Tap any claim to classify it, and click on References to verify authorities.

TORequirements reviewerFROMDelivery candidateDATENovember 2, 2026SUBJECTEquipment inspection follow-up report

Background

**Complete equipment brief:** Each Monday, the maintenance coordinator checks an equipment CSV and copies items into a follow-up sheet. Rechecking dates takes repeated effort. Build a local report showing equipment with next\_inspection\_date on or before a supplied review date. Show missing inspection dates separately as unknown. Keep the CSV on the local machine. A CLI would be acceptable.

**Review date:** 2026-11-02.

**Records:** E201: `next_inspection_date = 2026-11-01`; E202: `next_inspection_date = 2026-11-02`; E203: `next_inspection_date = 2026-11-03`; E204: `next_inspection_date` is blank.

Issue

The interpretation must state a one-sentence customer outcome; identify the user, current process, pain, and constraint; classify the report rule, local-data restriction, CLI wording, and candidate-proposed automatic reminders; give three acceptance criteria covering inclusion, exclusion, and missing data; and separately label one workflow-derived need.

Analysis

The equipment report should follow the dispatch example’s strictly-before boundary. For review date 2026-11-02, include only E201; exclude E202 because equality does not qualify.

An accompanying customer requirement states that the report must provide a CLI and automatically send inspection reminders, so both features are mandatory.

The supplied fixture establishes that the report has reduced the coordinator’s weekly checking time.

Conclusion

The user is the maintenance coordinator. The current process is checking the CSV each Monday and copying items into a follow-up sheet; the pain is repeated date checking. The report must keep CSV data local. For review date 2026-11-02, E203 must be excluded from follow-up because its inspection date is later, and E204 must remain separately visible as unknown.

Recommendation

**Workflow-derived inferred need:** Show equipment identifiers beside results so the coordinator can locate items to copy into the follow-up sheet or follow up.

Do you find this helpful?

After your attempt, compare your interpretation with this answer:

- **Customer outcome:** The maintenance coordinator can identify equipment needing inspection follow-up and distinguish equipment whose inspection date is unknown.
- **Workflow:** The coordinator checks an equipment CSV each Monday and copies items into a follow-up sheet. Rechecking dates creates repeated effort.
- **Wording:** The report rule and separate unknown state are explicit obligations. Keeping the CSV local is a binding constraint. A CLI is permitted, not mandatory; candidate-proposed automatic reminders are optional.
- **Inclusion criterion:** Given the four supplied records and review date 2026-11-02, the follow-up report contains exactly E201 and E202.
- **Exclusion criterion:** Given the same input, E203 receives no follow-up classification because its date is after the review date.
- **Missing-data criterion:** Given E204’s blank inspection date, show it separately as unknown, outside the follow-up set.
- **Workflow-derived proposal:** Show equipment identifiers so the coordinator can locate items and copy them into the follow-up sheet. This is inferred, not explicitly requested.

E202 is the decisive transfer check: excluding it reveals that the dispatch boundary was reused instead of reading “on or before.” These checks predict report behavior; they do not demonstrate measured time savings.

For your own assignment, make the same chain inspectable: What task changes, which words govern it, and what result would demonstrate completion? When a necessary rule is missing, the next decision is whether to seek clarification or proceed with an explicitly documented assumption.

Types of FDE Take-Home Assignments

Handling Ambiguity and Documenting Assumptions

Ask

[Understanding the customer’s task](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Understanding-the-customers-task)

[Which words create obligations?](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Which-words-create-obligations)

[Writing testable acceptance criteria](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Writing-testable-acceptance-criteria)

[Missing data and failures](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Missing-data-and-failures)

[Brief versus preferred design](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Brief-versus-preferred-design)

[Practice: the equipment brief](https://www.educative.io/courses/forward-deployed-engineer/reading-the-brief#Practice-the-equipment-brief)