# Designing_AI_Systems_Around_End_User_Workflow_and_Task_Handling

Source: https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Designing Around the End User's Workflow

Design a workflow that helps facilities coordinators review, track, and manage maintenance requests. Define triggers, user inputs, result interpretation, and follow-up actions or blockers. Include identifiers and relevant request details, allow users to review and correct information locally, and keep unresolved requests visible. Support manual assignments without updating external systems, and clearly indicate ownership and completion status during handoff.

We'll cover the following...

- [Why summary counts fall short](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Why-summary-counts-fall-short)
- [Mapping the first-week workflow](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Mapping-the-first-week-workflow)
- [Showing each request’s outcome](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Showing-each-requests-outcome)
- [Correcting and rerunning R202](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Correcting-and-rerunning-R202)
- [Handling edge-case files](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Handling-edge-case-files)
- [Walking through the design](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Walking-through-the-design)
- [Practice: Support ticket triage](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Practice-Support-ticket-triage)

## Why summary counts fall short[#](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Why-summary-counts-fall-short)

Try completing a maintenance handoff from this output:

> Plumbing: 1  
> Electrical: 0  
> All requests processed.

Suppose a facilities coordinator reviews an exported request CSV each morning, then manually assigns eligible requests in an existing tracker. The routing calculation behind those counts is correct. Which tracker record should they open next?

Technical Quiz

1.

The morning CSV run reports: “Plumbing: 1; Electrical: 0; All requests processed.” The routing calculation is correct. What can the coordinator safely conclude?

A.

The run reports one plumbing routing result, but doesn’t say which request it is.

B.

The summary gives enough information to find the plumbing request in the tracker.

C.

One plumbing assignment has been completed in the tracker.

D.

All requests were processed, so no unresolved records need checking

---

1 / 1

The message “All requests processed” does not distinguish between completed processing, resolved blockers, and completed tracker assignments. The summary confirms only that processing has completed. Without request identifiers and visibility into the two unresolved review items, the coordinator cannot identify the remaining investigation and assignment tasks.

Each reported item should include an identifier, the required next action, and instructions for handling blockers. Provide separate assignment and review lists to support the handoff. Adding another chart would not address the missing task-level information.

## Mapping the first-week workflow[#](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Mapping-the-first-week-workflow)

A **first-week workflow** describes the user’s trigger, inputs, interpretation of results, next action, correction path, and handling of likely exceptions. It is a bounded design exercise: Choose the situations worth supporting immediately rather than attempting to predict every production situation.

Assume the routing backend already works. This fictional brief requires assignment recommendations and visible unresolved records, prohibits writes to the tracker, and permits correcting a local CSV copy. Start with those boundaries and the coordinator’s existing tools:

1. Obtain the morning request export and keep a local working copy.
2. Supply that copy to the routing process.
3. Inspect the current run’s assignment recommendations and unresolved review items.
4. Locate each recommended request in the tracker by request ID and manually assign it.
5. Investigate unresolved items using their identifiers and reasons.
6. Correct verified information in the local input copy, rerun, and inspect the replacement results before continuing the handoff.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27822.53%27%20height=%27233.23%27/%3e)![Request response life cycle](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Request response life cycle")

Request response life cycle

Displaying routing reasons and source-row references is a workflow-derived proposal: These details reduce the work of interpreting and correcting results. They are not additional explicit requirements discovered in the brief.

As in chapter 2, keep assumptions, scope cuts, and simulated behavior distinct; the proposed source reference is a workflow-derived aid, not an explicit requirement. Automatic tracker assignment is prohibited here, rather than merely deferred as an optional feature.

## Showing each request’s outcome[#](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Showing-each-requests-outcome)

The input columns are `request_id`, `status`, `category`, and `room`. Apply these supplied rules:

- Only requests with status `open` are eligible for routing.
- Category `plumbing` routes to the plumbing team; `electrical` routes to the electrical team.
- Every eligible request requires a nonblank room.
- Missing rooms and unsupported categories remain unresolved.
- Requests with status `completed` are excluded.

The source file contains the following four records, listed in their original order:

- `R201,open,plumbing,B2`
- `R202,open,electrical,` (the room field is empty).
- `R203,open,lift,A1`
- `R204,completed,electrical,C3`

Use request IDs to identify and track requests consistently across systems. For source references, count the header as row 1. The four records therefore occupy rows 2–5. A row number identifies a record's position in the current file but is not a stable identifier if the file is reordered or modified.

|  |  |  |  |
| --- | --- | --- | --- |
| **Request ID** | **Input** | **Result** | **Reason** |
| R201 | open, plumbing, B2 | Recommendation | Plumbing team. Open request, supported category, room B2 present. |
| R202 | open, electrical, blank room | Unresolved | Required room is missing. |
| R203 | open, lift, A1 | Unresolved | “Lift” isn’t a supported category |
| R204 | completed, electrical, C3 | Excluded | Status is completed. |

Interpret each disposition as a required next action, not just a routing classification. `R202` requires verification of its missing room information under the existing routing rule. `R203` requires clarification of the `lift` category or an approved category mapping. Both records remain unresolved, but each requires a different follow-up action. `R204` is intentionally excluded because its status is `completed`, not because processing was incomplete.

Verify source-record reconciliation: 4 inputs = 1 recommended assignment + 2 unresolved records + 1 intentional exclusion. Reporting all four dispositions allows the coordinator to identify pending follow-up work and distinguish it from records excluded by the rules.

## Correcting and rerunning R202[#](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Correcting-and-rerunning-R202)

The coordinator learns from the requester that R202’s room is C4. Trace the recovery roadmap below. Identify where the source correction becomes durable and where the coordinator( not the submission) completes the assignment.

Recover R202 and complete the manual handoff

Inspect R202Verify roomCorrect local CSVRerun routingInspect recommendationManually assign R202

Recover R202 and complete the manual handoff: stage 1 of 6, Inspect R202.

Overview

Build R202's recovery chain. Result: 2 recommendations + 1 unresolved + 1 excluded = 4. R203 stays unresolved: no authorized mapping or verified category correction.

Build R202's recovery chain. Result: 2 recommendations + 1 unresolved + 1 excluded = 4. R203 stays unresolved: no authorized mapping or verified category correction.

Inspect R202 at source row 3: room missing. Use the request ID as stable identity; the row locates this input.

Contact the requester and verify that R202's room is C4 before changing the source.

Set R202's room to C4; keep its ID. Reject editing only the displayed result: regeneration loses that correction.

Run the routing process against the corrected local CSV copy before inspecting replacement results.

Check R202: room C4, electrical team. It is open, its category is supported, and its room is now present.

Locate R202 in the existing tracker; assign to electrical. Reject automatic tracker writes: they are prohibited.

Do you find this helpful?

The chain crosses two distinct boundaries:

- **Verification:** It authorizes changing the source. A rerun alone cannot establish that C4 is correct.
- **Assignment:** The corrected recommendation enables a manual tracker action; it does not prove that action happened.

Keeping these boundaries explicit prevents a successful rerun from being mistaken for a completed assignment.

After rerunning, the current result accounts for all four inputs:

- **2 recommendations:** R201 and R202
- **1 unresolved record:** R203
- **1 excluded record:** R204

Thus, 2 + 1 + 1 = 4. R202 retains its request ID, connecting the corrected result to the same tracker record.

Editing only the displayed output loses the correction when results are regenerated. Source correction and rerun provide complete recovery without an inline editor, database, or write-back integration.

R203 needs a different recovery path. It requires an authorized category mapping or a verified correction before proceeding. Guessing that `lift` means `electrical` silently changes a business rule.

Keep R203 identifiable and unresolved, with the next step “Seek category clarification or an authorized mapping.”

The submission stops at preparing recommendations. The coordinator’s subsequent tracker action,not producing the recommendation, completes the assignment.

## Handling edge-case files[#](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Handling-edge-case-files)

Define these first-week cases as user-visible behavior before choosing interface controls:

- **Ordinary assignment:** R201 shows its ID, room, recommended team, and reason so the coordinator can locate and assign it.
- **Missing room:** R202 remains visible with its missing field and verification step, allowing correction and rerun.
- **Unsupported category:** R203 remains visible with `lift` and a clarification step; no team is invented.
- **Valid file containing only completed records:** The run succeeds with zero recommendations and zero unresolved records. All inputs are accounted for as excluded, so this review requires no assignment or investigation.
- **Unreadable file:** The review did not complete. Identify the failed input and ask the coordinator to obtain or select a readable copy. No current successful result should be claimed.

An empty assignment list alone cannot tell the user which situation occurred. If unresolved records exist, investigation remains necessary. If the input failed, even an older successful report must not appear to be the result of this attempt.

These are behavioral requirements: They describe what the coordinator can understand and do. None requires selecting widgets or implementing error-handling machinery here.

## Walking through the design[#](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Walking-through-the-design)

Walk through the four records as the coordinator, answering concrete questions:

- Which tracker record do I locate? R201 initially; R202 also becomes actionable after correction.
- Which team is recommended, and why? Plumbing for R201; electrical for corrected R202, under the supplied eligibility and category rules.
- What is stopping R202 initially? Its required room is blank.
- Where do I correct it? In the local CSV copy, after verification.
- What changes after rerunning? R202 moves from review to a recommendation; R203 remains unresolved.
- Has the submission assigned anything in the tracker? No. It prepares the manual handoff and never writes to the tracker.

A paper walk-through checks whether the design supports these specified actions; check an implemented path before claiming the application does. As in chapter 2, walkthrough evidence does not establish adoption, measured time savings, or production readiness.

## Practice: Support ticket triage[#](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Practice-Support-ticket-triage)

Apply the method to an independent support-triage task. A support coordinator reviews a local CSV, prepares a routing list, and manually transfers tickets to existing team queues. The submission must not write to those queues. Local input correction and rerun are permitted.

Only status `new` is eligible. Topic `billing` routes to the billing team, and `login` routes to the account-access team. Every eligible ticket requires a nonblank `customer_ref`. Unsupported topics and missing customer references remain unresolved; closed tickets are excluded.

The input file contains the columns `ticket_id`, `status`, `topic`, and `customer_ref`, with the following four records:

- `Q51,new,billing,C8`
- `Q52,new,login,` (the `customer_ref` field is empty).
- `Q53,new,delivery,C9`
- `Q54,closed,billing,C10`

First, draft a specification describing the workflow in no more than six steps. For each ticket, specify its disposition, reason, and required next action. After verifying that `Q52` belongs to customer `C12`, update the local source file, rerun the workflow, and document the resulting dispositions.

Describe how the workflow handles a valid file containing only closed tickets and a file that cannot be read. State explicitly whether any tickets have actually been transferred between queues. Do not include code, UI mockups, or videos.

Then review the memo below, checking its proposed interpretations against the supplied rules. Attempt your specification before consulting the review explanations.

Support-triage workflow specification

Your task

You are specifying the support coordinator’s first-week workflow for reviewing a local ticket CSV and preparing manual queue transfers. Account for every ticket, preserve stable ticket identifiers, and provide a correction-and-rerun path without writing to existing queues.

Tap any claim to classify it, and click on References to verify authorities.

TOSupport coordinatorFROMWorkflow reviewerDATEOctober 19, 2026SUBJECTQ51–Q54 routing, recovery, and manual handoff

Background

Specify a workflow of six steps or fewer for the supplied records: `Q51,new,billing,C8`; `Q52,new,login,`; `Q53,new,delivery,C9`; `Q54,closed,billing,C10`. No code or mockup is required.

Issue

Include a before-correction table or structured list giving each ticket’s result, reason, and next action. Explain verification of Q52’s customer reference as C12, local source correction, rerun, and exact replacement dispositions. Also explain a valid all-closed file, an unreadable file, and whether any queue transfers have actually occurred.

Analysis

Proposed interpretation: The lesson’s rule that `login` routes to the account-access team makes Q52 actionable immediately, even with its blank `customer_ref`.

Proposed interpretation: A “nearest supported topic” rule authorizes routing Q53’s `delivery` topic to billing.

Proposed interpretation: Once a routing list has been produced, the tickets have been transferred. An empty list also establishes a successful review, even when the current input was unreadable.

Conclusion

The recovery path must preserve Q52’s identifier and correct the local input rather than only changing displayed results.

Recommendation

Use the comparison to revise your written specification. Ensure every ticket has an identifiable next action and distinguish recommendations from completed manual transfers. Treat this as self-review of a specification, not proof that an application works.

Do you find this helpful?

For each result category in your assignment, complete the following statement: “The user identifies \_\_\_\_\_, understands \_\_\_\_\_, and takes \_\_\_\_\_\_ as the next action.”

Identify the most likely blocker, describe how to correct the source data, and specify how to rerun the workflow. Use these answers to determine what information and actions the minimal interface must provide.

Code Quality, Testing, and Reproducibility

Building a Demonstrable Interface

Ask

[Why summary counts fall short](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Why-summary-counts-fall-short)

[Mapping the first-week workflow](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Mapping-the-first-week-workflow)

[Showing each request’s outcome](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Showing-each-requests-outcome)

[Correcting and rerunning R202](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Correcting-and-rerunning-R202)

[Handling edge-case files](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Handling-edge-case-files)

[Walking through the design](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Walking-through-the-design)

[Practice: Support ticket triage](https://www.educative.io/courses/forward-deployed-engineer/designing-around-the-end-users-workflow#Practice-Support-ticket-triage)