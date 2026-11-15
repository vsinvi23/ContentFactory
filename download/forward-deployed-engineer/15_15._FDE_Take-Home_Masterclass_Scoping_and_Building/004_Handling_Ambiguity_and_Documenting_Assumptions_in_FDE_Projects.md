# Handling_Ambiguity_and_Documenting_Assumptions_in_FDE_Projects

Source: https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Handling Ambiguity and Documenting Assumptions

Explore how to rank unanswered questions by their effect on the customer’s decision, feasibility, and assessment compliance. Understand how to write focused clarification messages and defensible, revisable assumption entries, preparing you to keep moving without inventing certainty.

We'll cover the following...

- [Ranking unanswered questions](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Ranking-unanswered-questions)
- [Ask or decide yourself](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Ask-or-decide-yourself)
- [Writing the clarification message](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Writing-the-clarification-message)
- [Keeping an assumption log](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Keeping-an-assumption-log)
  - [A1: The provisional 30-day window](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#A1-The-provisional-30-day-window)
  - [A2: C12 remains visibly unresolved](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#A2-C12-remains-visibly-unresolved)
- [Defensible versus convenient assumptions](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Defensible-versus-convenient-assumptions)
- [Updating after an answer](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Updating-after-an-answer)
- [Practice: The invoice report](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Practice-The-invoice-report)

Before starting implementation, a candidate drafted several questions about a take-home assignment. Which questions should they ask?

> Draft message (unsent):
>
> 1. What does “due soon” mean?
> 2. How should I handle conflicting contract rows?
> 3. Where do the CRM credentials come from?
> 4. Is AI coding assistance allowed?
> 5. Which table color should I use?

Which questions deserve an interruption before implementation? First, inspect the request they came from:

> - The account team reviews contracts to decide which customers need renewal outreach.
> - Build a local report from the supplied contract CSV and a supplied review date. The report should show active contracts that are due for renewal soon. Add each contract’s account owner by looking it up through the live CRM API. Include a README that explains your assumptions.
> - Send any questions about the assessment through the recruiter.

Use review date 2026-11-01 and these records:

- C10/account A10/active/renewal date 2026-11-15
- C11/account A11/active/renewal date 2026-12-01
- C12/account A12/active/renewal date 2026-11-12
- C12/account A12/active/renewal date 2026-11-20
- C13/account A13/active/renewal date 2026-12-02

Treat all dates as calendar dates without time zone conversion. Do not use input order to determine record precedence. The brief does not specify credentials, duplicate-resolution rules, a renewal horizon, or AI-assistance permissions.

## Ranking unanswered questions[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Ranking-unanswered-questions)

Prioritize unclear requirements based on their impact on the customer’s decisions, implementation feasibility, and compliance with assessment instructions. A presentation choice that is easy to change generally requires less attention than an ambiguity that affects correctness or compliance.

Classify the five questions in the draft message before deciding which defaults to apply.

What does each question affect?

Unsent question

Is AI coding assistance allowed?

Where do CRM credentials come from?

What does “due soon” mean?

How should I handle conflicting contract rows?

Which table color should I use?

Primary consequence

Reversible presentation

Customer decision and report membership

Business meaning and record authority

Feasibility of required live work

Assessment compliance

Match each unsent question to its primary consequence. All pairs start unmatched. Use feedback to revise your matches; these categories do not rank the first four questions.

Do you find this helpful?

These categories can overlap. The unresolved authority of C12 also affects which records qualify for outreach within the 14-day window. Prioritize ambiguities based on the impact of incorrect assumptions, not the number of unresolved questions.

This leaves four high-impact questions, but each may require a different approach while awaiting clarification.

## Ask or decide yourself[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Ask-or-decide-yourself)

Compare plausible interpretations and the consequence of choosing incorrectly:

- **Renewal horizon:** A 14-day inclusive window ends on November 15; a 30-day inclusive window ends on December 1. C11 changes membership. Ask for the intended horizon; a disclosed, revisable default can support independent classification work meanwhile.
- **Conflicting dates:** Choosing the last C12 row selects November 20, but nothing establishes that row as newer or authoritative. Ask whether either record has authority. Preserve the conflict while waiting.
- **CRM access:** Working credentials would permit a live lookup; sample owner names would only simulate one. Ask how to obtain access. Silence supplies neither credentials nor permission to replace the required integration.
- **AI assistance:** Permission would allow assistance within its stated limits. Silence leaves permission unresolved. Ask before using assistance; continue independently.
- **Table color:** Choose a readable conventional style yourself. It is inexpensive to change and does not alter report membership.

Follow the assignment’s instructions on when, how, and where to submit questions. Publicly available assignment examples vary. Some encourage clarification questions, while others require candidates to make their own data-related decisions. These examples illustrate different approaches, not policies that apply to every employer. If the brief assigns data-related decisions to the candidate, make reasonable assumptions, document the rationale, and proceed without seeking unnecessary clarification.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27924.9449999999999%27%20height=%27242.18999999999997%27/%3e)![Each gap calls for a distinct interim response: silence confirms neither a provisional interpretation nor access or permission](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Each gap calls for a distinct interim response: silence confirms neither a provisional interpretation nor access or permission")

Each gap calls for a distinct interim response: silence confirms neither a provisional interpretation nor access or permission

An **assumption** interprets an unknown. An **acceptance criterion** specifies observable behavior. A **scope cut** omits capability. A **stub** simulates behavior. These labels describe different things: recording a fake CRM response under “assumptions” does not change what it demonstrates.

## Writing the clarification message[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Writing-the-clarification-message)

A useful clarification question names the gap, explains its consequence, and requests a concrete answer. Where a defensible default exists, state it so the recipient can confirm or correct it.

Send a compact message through the stated assessment contact:

Hi,

I have a few questions about the renewal report:

1. **“Due soon”:** Should this mean renewal dates from the review date up to and including 30 calendar days later? Unless you tell me otherwise, I’ll use that window for now and label it clearly in the report.
2. **C12’s conflicting dates:** Is either record the correct one? If there’s no rule for choosing, I’ll show C12 separately as unresolved instead of picking a date.
3. **CRM access:** The brief asks for a live CRM owner lookup, but no credentials or access instructions were included. How should I get access? If access isn’t possible, can I use sample data instead?
4. **AI tools:** Am I allowed to use AI coding tools for this assessment?

The first two questions propose inspectable interim behavior. The final two request access or permission. Neither says that failure to reply authorizes a fallback or assisted work.

## Keeping an assumption log[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Keeping-an-assumption-log)

An **assumption log** records an unresolved interpretation and the provisional decision used to proceed. Each entry needs an identifier, gap, default, rationale, consequence, verification example, status, and revision trigger.

For this report, write two separate entries.

### A1: The provisional 30-day window[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#A1-The-provisional-30-day-window)

- **Gap:** “Due soon” has no defined horizon or boundary.
- **Chosen default:** `review_date <= renewal_date <= review_date + 30 calendar days`. For November 1, the window ends on December 1, inclusive.
- **Rationale:** This is a bounded, explicit interpretation that is easy to revise. Thirty days is a chosen default here, not an industry standard.
- **Consequence:** C10 and C11 are included among confidently classified renewals. C13 is excluded. C12 is handled under A2.
- **Verification example:** C11 on December 1 is included at the upper boundary; C13 on December 2 is excluded one day beyond it. C10 on November 15 is included.
- **Status:** Provisional; clarification requested, no answer received.
- **Revisit when:** An authoritative answer defines the horizon or its boundaries; update the rule and affected checks.

### A2: C12 remains visibly unresolved[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#A2-C12-remains-visibly-unresolved)

- **Gap:** C12 has renewal dates November 12 and November 20, with no authority rule.
- **Chosen default:** Preserve both dates in a separate unresolved result. Exclude C12 from the confidently classified set.
- **Rationale:** Neither row has established authority; selecting one would invent certainty.
- **Consequence:** The account team sees the conflict and cannot treat C12 as a confirmed outreach classification.
- **Verification example:** Exactly one unresolved contract C12 remains visible with both supplied dates. Reordering the input must not select a winning date. Neither C12 row becomes a confidently classified renewal.
- **Status:** Provisional; clarification requested, no answer received.
- **Revisit when:** An authoritative resolution policy or corrected source record is supplied.

Under the assumed 30-day window, both dates associated with C12 fall within the range. The conflicting dates remain unresolved, so the report cannot identify a definitive renewal date. With a shorter window, the conflicting dates could also affect whether C12 qualifies for the report.

Track the following two unresolved dependencies separately from the assumption log:

- **B1: Live CRM access blocked.** Credentials and access instructions have been requested. Live owner enrichment remains incomplete and unverified. Label fixture results separately. They do not verify the required live CRM integration.
- **P1: AI-assistance permission unresolved.** Clarification has been requested. Do not use AI assistance unless permission is confirmed. Proceed only with independently completed work that requires neither blocked access nor unconfirmed assistance permissions.

These classifications describe expected results, not verified software behavior or completed owner enrichment. Without clarification, A1 and A2 remain provisional, B1 remains blocked, and P1 remains unresolved.

## Defensible versus convenient assumptions[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Defensible-versus-convenient-assumptions)

Consider this candidate note:

> No reply, so I assumed due soon means 30 days, used the last C12 row as the latest version, replaced CRM with sample owner names, and used an AI coding tool because I will disclose it.

Four different problems are compressed into one sentence:

- The 30-day rule lacks an explicit provisional status and exact boundaries, making an unconfirmed choice look settled.
- “Last row” invents an authority rule that the input explicitly lacks.
- Sample names simulate enrichment without satisfying or verifying the live lookup.
- Disclosure describes tool use; it does not supply missing permission.

Repair the handoff with A1 and A2, a visible C12 conflict, and explicit B1 and P1 statuses. If assistance was already used, stop and ask how to proceed, accurately reporting what happened; do not rewrite the history as independent work.

“Assume the data is clean” also fails: It supplies no reasoned interpretation, consequence, check, or revision trigger, and C12 directly contradicts it. A2 instead preserves the information needed to inspect the uncertainty.

Documentation makes a choice inspectable. It cannot override explicit constraints, grant permission, create credentials, or establish live-service success. Even the carefully documented A1 can be wrong; its defensibility depends on being disclosed and revisable, not customer-approved.

## Updating after an answer[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Updating-after-an-answer)

Suppose the reply says:

> Use a 14-day inclusive window; do not resolve conflicting contract dates automatically.

Predict the changes before updating the log.

Predict the effects of replacing A1

↓ Entry

📝A1 — provisional 30-day rule

📅Inclusive window

↓ Entry

📋A2 — preserve conflicting dates

↓ Entry

🔒B1 — CRM access

↓ Entry

❔P1 — assistance permission

↓ Entry

📄C10 / A10 — active

📄C11 / A11 — active

⚠️C12 / A12 — active

↓ Entry

📄C13 / A13 — active

72%

Failure simulator

Pick a component to knock out — see how far the damage spreads.⌀ badges show each node’s blast radius — the bigger the number, the closer it is to a single point of failure.

Do you find this helpful?

Record the actual answer and revise the affected criteria:

- **A1 becomes superseded:** Preserve its original 30-day decision as history. Add the confirmed rule, `review_date <= renewal_date <= review_date + 14 calendar days`, linked to the reply.
- **The upper boundary becomes November 15:** C10 remains included on that boundary. C11 moves out; C13 remains out.
- **A2 becomes confirmed:** The reply supports keeping C12 unresolved with both dates visible. November 12 falls inside the new window and November 20 outside it, so choosing either would now change the outreach decision.
- **B1 and P1 remain open:** The reply says nothing about CRM access or AI permission.

Update expected membership to exactly C10 among confidently classified renewals, with C12 separately unresolved. Confirmation changes the decision record and its checks; it is more than a new label on the README.

## Practice: The invoice report[#](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Practice-The-invoice-report)

Use this independent brief:

> Build a local CSV report for the finance reviewer showing large invoices issued on or before a supplied review date. Keep the data local. Include assumptions in your handoff. Send questions to the assessment contact.

Review date: 2026-11-10. All amounts are valid USD values; all dates are calendar dates.

- **I21:** 999 USD, issued 2026-11-09
- **I22:** 1000 USD, issued 2026-11-10
- **I23:** 1500 USD, issued 2026-11-11

The brief does not define the threshold for a “large” transaction or specify whether AI assistance is permitted. Review the candidate’s memo. Identify reasoning errors and explain how to correct them. Draft a separate clarification message and assumption log entry.

For this exercise, use USD 1,000 or more as the proposed threshold for a large transaction. This is an instructional assumption, not an established business rule.

Invoice Report — Clarification and Assumptions

Your task

You are preparing an independent assessment handoff for a local invoice report. Your response must prioritize the undefined amount threshold, explicit date boundary, unresolved AI permission, and cosmetic styling; include a concise message to the assessment contact; and document one complete provisional threshold entry. Membership decisions and assessment compliance both matter.

Tap any claim to classify it, and click on References to verify authorities.

TOAssessment contactFROMAssessment candidateDATENovember 10, 2026SUBJECTLocal invoice report: clarification priorities and provisional threshold

Background

The brief requires a local CSV report showing large invoices issued on or before review date **2026-11-10**. Keep the data local and include assumptions in the handoff. I21 is 999 USD, issued November 9; I22 is 1000 USD, issued November 10; I23 is 1500 USD, issued November 11.

Issue

The amount threshold affects membership, and AI permission affects assessment compliance. Both need clarification; either may be ranked first. The date boundary is already explicit, and readable styling can be chosen independently.

Analysis

The brief’s phrase “on or before” supports using `issue_date < 2026-11-10`, excluding invoices issued on the review date.

An established invoice-reporting industry rule defines a large invoice as at least 1000 USD, so this threshold can be recorded as authoritative rather than provisional.

If the contact does not reply, disclosing AI use in the handoff is sufficient permission to use an external AI service to process the invoice CSV.

Conclusion

To the assessment contact: What amount should count as a large invoice? Pending clarification, I propose at least 1000 USD, inclusive, as a provisional instructional default; the threshold changes report membership. Are AI coding tools permitted for this assessment? I will work independently without AI assistance pending permission and keep all invoice data local.

Recommendation

**A1 — Undefined large-invoice threshold.** Default: `amount_usd >= 1000`, retaining `issue_date <= 2026-11-10`. Rationale: a simple, checkable instructional choice, not an industry standard. Status: provisional and unconfirmed; clarification requested. Consequence: expected membership is exactly I22. Checks: I21 fails at 999 USD despite its November 9 date; I22 qualifies at exactly 1000 USD and exactly November 10; I23 meets the amount threshold but fails because November 11 is after the review date. Revision trigger: an authoritative threshold answer; update the amount rule and affected membership checks while preserving the explicit date boundary.

Do you find this helpful?

After reviewing the memo and writing your own response, compare with this model:

> The undefined threshold affects invoice membership, and assistance permission affects compliance; both need clarification. “On or before” already defines the date boundary. I will choose readable formatting independently.To the assessment contact: What amount should count as a large invoice? Pending clarification, I propose at least 1000 USD, inclusive, labeled provisional. This affects which invoices appear. Also, are AI coding tools permitted for this assessment? I will work independently until permission is established.

Document the assumption as follows:

- **Identifier and gap:** A1, undefined large-invoice threshold. The brief does not specify a minimum amount.
- **Default and rationale:** Use USD 1,000 or more as a testable instructional default until the threshold is confirmed.
- **Status:** Provisional; clarification requested.
- **Consequence:** Under the proposed threshold and explicit issue-date rule, the expected report contains only I22.
- **Check:** I21 is excluded because USD 999 is below the threshold. I22 qualifies because its amount is exactly USD 1,000 and its issue date matches the review date. I23 meets the amount threshold but is excluded because its November 11 issue date is after the November 10 review date.
- **Revision trigger:** When the threshold is confirmed, update the amount rule and expected results without changing the explicit issue-date boundary.

For your own brief, make every consequential gap inspectable: Its question, interim behavior, dependent check, and revision trigger. With those decisions visible, what is the smallest end-to-end workflow you can commit to delivering in the available time?

Reading the Brief

Scoping the MVP

Ask

[Ranking unanswered questions](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Ranking-unanswered-questions)

[Ask or decide yourself](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Ask-or-decide-yourself)

[Writing the clarification message](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Writing-the-clarification-message)

[Keeping an assumption log](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Keeping-an-assumption-log)

[A1: The provisional 30-day window](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#A1-The-provisional-30-day-window)

[A2: C12 remains visibly unresolved](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#A2-C12-remains-visibly-unresolved)

[Defensible versus convenient assumptions](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Defensible-versus-convenient-assumptions)

[Updating after an answer](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Updating-after-an-answer)

[Practice: The invoice report](https://www.educative.io/courses/forward-deployed-engineer/handling-ambiguity-and-documenting-assumptions#Practice-The-invoice-report)