# Data_Integration_Challenge_for_Forward_Deployed_Engineers

Source: https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Capstone: Data Integration Challenge

Complete a timed, independent assignment to reconcile inconsistent customer and work-order exports in a local review dashboard. Implement traceable reconciliation, retain unresolved records for review, and handle invalid inputs safely. Evaluate your submission against the rubric before reviewing the annotated reference solution.

We'll cover the following...

- [Deliverables and timing rules](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Deliverables-and-timing-rules)
  - [Full delivery brief](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Full-delivery-brief)
- [Input files and rules](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Input-files-and-rules)
  - [customer\_export.csv](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#customerexportcsv)
  - [work\_order\_export.csv](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#workorderexportcsv)
  - [Supplied reconciliation requirements](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Supplied-reconciliation-requirements)
- [Defining acceptance evidence](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Defining-acceptance-evidence)
  - [Assignment-specific scoring criteria](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Assignment-specific-scoring-criteria)
- [Planning the 240 minutes](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Planning-the-240-minutes)
- [Freezing and self-scoring](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Freezing-and-self-scoring)
- [The post-attempt reference](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#The-post-attempt-reference)
  - [Intended design and availability](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Intended-design-and-availability)
  - [Prerequisites and conditional execution](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Prerequisites-and-conditional-execution)
  - [Trace the customer records](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Trace-the-customer-records)
  - [Customer reconciliation](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Customer-reconciliation)
  - [Work-order reconciliation](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Work-order-reconciliation)
  - [Expected matched-open results](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Expected-matched-open-results)
  - [Checks that protect results](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Checks-that-protect-results)
  - [What would a naive join get wrong?](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#What-would-a-naive-join-get-wrong)
  - [Limits and acceptable alternatives](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Limits-and-acceptable-alternatives)
- [Defending your frozen result](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Defending-your-frozen-result)

In this capstone, you’ll build a complete take-home solution for a real-style customer request. Here’s the brief from the customer:

“I compare the customer export with the work-order export by hand. Give me a local, read-only dashboard where I can review matched open work by customer and investigate open work that can’t be safely matched.”

**Service operations coordinator**

## Deliverables and timing rules[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Deliverables-and-timing-rules)

**Start-of-attempt notice:** Opening the full brief and accompanying files starts the 240-minute active-work limit. Do not open them until you are ready to begin. Reading, implementation, testing, documentation, and recording all count toward this limit.

This fictional course assignment is separate from the other capstone and does not represent an employer's assessment. You may use standard documentation and software libraries. During the independent first attempt, do not use AI assistance for coding or writing, implementation help from others, or annotated model solutions.

Clarification is unavailable in this self-directed exercise. Document unresolved assumptions and questions without changing or overriding any explicit requirements.

### Full delivery brief[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Full-delivery-brief)

Build a repeatable ingestion-and-reconciliation pipeline and a runnable local dashboard for the coordinator. Deliver:

- Matched open work grouped by customer, with identifiable work-order details.
- Visible unresolved and invalid records, including reasons and source references.
- Complete input accounting, with customer exceptions, closed work, and suppressed duplicates still inspectable.
- Focused tests and an end-to-end smoke test.
- Documented prerequisites and a one-command execution route from a clean clone, without hidden local state or embedded credentials.
- A README covering usage, reconciliation choices, assumptions, limitations, and safe failure behavior.
- Actual time and assistance declarations, including unmet requirements.
- An accessible, playable recorded walkthrough shorter than five minutes.

Both inputs are synthetic local exports. No API, live service, write-back, cloud deployment, authentication system, or LLM is required. Choose familiar tools. Charts, hosting, fuzzy matching, and additional services are outside the required MVP.

Save the brief as `data_integration_brief.md` and the following files under their exact names. Keep this assignment independent of earlier examples.

## Input files and rules[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Input-files-and-rules)

### `customer_export.csv`[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#customerexportcsv)

Ace Editor

1

2

3

4

5

6

7

8

9

10

customer\_id,customer\_name

C01,North Clinic

" c01 "," North Clinic "

C02,East Clinic

C03,Hill Clinic

C03,Ridge Clinic

C04,

,West Clinic

C05,Lakes Clinic

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

customer\_export.csv

The input file contains eight customer records. The header is on physical **line 1**, followed by eight records on **lines 2–9**. Quotation marks delimit fields and are not part of the values.

### `work_order_export.csv`[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#workorderexportcsv)

Ace Editor

1

2

3

4

5

6

7

8

9

10

11

12

13

14

work\_order\_id,customer\_id,status

W101,C01,open

W102," c02 "," OPEN "

W103,C03,open

W104,C99,open

W105,,open

W106,C05,closed

W107,C01,open

W107," c01 "," open "

W108,C01,open

W108,C02,open

W109,C05,pending

W110,C04,open

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

work\_order\_export.csv

There are twelve work-order records, occupying physical **lines 2–13**.

### Supplied reconciliation requirements[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Supplied-reconciliation-requirements)

Use these customer requirements to determine expected behavior before implementing the solution.

- **Normalization:** Remove surrounding whitespace from identifiers, then convert them to uppercase. Trim surrounding whitespace from customer names without changing their spelling. Trim and lowercase status values. Only `open` and `closed` are valid statuses.
- **Customer validity:** Reject blank customer IDs or names as invalid. Deduplicate identical normalized customer records while retaining references to every source row. If a normalized customer ID has different names, retain the group as unresolved. Do not select an authoritative name. Only valid customer groups without conflicts can be used for matching.
- **Work-order validity:** Flag missing work-order IDs and unrecognized statuses as invalid data. Do not infer whether a work order is open or closed from an invalid status.
- **Work-order duplicates:** Deduplicate identical normalized work-order records into one logical order while accounting for every duplicate source row. If records under the same work-order ID differ, retain them as one unresolved group with all source references. Do not use input order to select an authoritative record. Do not discard an invalid group member and treat the remaining record as trusted.
- **Matching:** Count each distinct trusted work-order ID only once in matched-open totals. Keep eligible open work unresolved when its customer reference is blank, unknown, conflicted, or otherwise unusable. Exclude closed work from open-work totals while retaining it in the reconciliation accounting.
- **Failed review:** Reject unreadable files and missing required headers with a visible error. Do not report a successful empty result or present an earlier successful report as current.
- **Successful empty review:** Accept a valid work-order file containing only headers, report zero work orders, and retain customer-input quality findings.

## Defining acceptance evidence[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Defining-acceptance-evidence)

Write your own expected memberships and accounting before building. The reconciled sample answer is deliberately reserved for the post-attempt reference.

Your acceptance checks must establish that:

1. The matched-open view groups distinct trusted orders by usable customer, and every count leads to identifiable orders.
2. Unresolved and invalid records expose reasons and source references.
3. Every row in both files has a traceable disposition. Customer exceptions, closed orders, and suppressed work-order duplicates remain inspectable.
4. Identical reruns do not accumulate output. Changed inputs produce a current replacement result.
5. Missing headers and unreadable inputs visibly fail without displaying earlier success as current.
6. Header-only work input produces a successful empty review, retaining customer-quality reporting.
7. A reviewer can execute the documented route from a clean clone and inspect the required tests, README, declarations, and recording.

### Assignment-specific scoring criteria[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Assignment-specific-scoring-criteria)

Assess your submission using the course rubric introduced earlier in this chapter:

- **Customer workflow acceptance (30 points):** The coordinator can navigate from customer totals to individual work-order IDs, investigate exceptions, review exclusions, and distinguish an empty successful review from a failed one.
- **Domain correctness and evidence (25 points):** Normalization, customer matching eligibility, duplicate handling, conflict preservation, invalid-data handling, distinct-order counts, source provenance, and both input ledgers follow the supplied rules.
- **Reliability and reproducibility (20 points):** The application runs from a clean clone using documented setup instructions. Targeted tests and an end-to-end smoke test verify critical behavior. Verification evidence covers repeated runs, modified inputs, header-only files, and failure cases.
- **Communication (15 points):** The README provides accurate setup and execution commands. Assumptions and limitations are explicit. An accessible recording under five minutes demonstrates the customer workflow and a meaningful failure or limitation.
- **Ownership and integrity (10 points):** You can explain significant implementation decisions and identify their supporting evidence. Accurately document work time, assistance, unmet requirements, and verification limits. Preserve the original attempt.

Ratings are as follows:

**0:** Evidence absent or contradicted.

**1:** Major gaps.

**2:** Partial evidence with material gaps.

**3:** Core criteria evidenced with bounded shortcomings.

**4:** All listed category criteria evidenced.

Each category earns **weight × rating ÷ 4** points. Every rating needs an artifact reference and evidence limit. Record contract violations and unmet obligations separately from the numerical score. These weights and the time limit are course conventions, with no implied hiring threshold.

## Planning the 240 minutes[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Planning-the-240-minutes)

Plan the work around verifiable deliverables rather than a prescribed implementation. One suggested time allocation is:

1. **20 minutes:** Review the brief, inspect both exports, define acceptance criteria, and document scope and assumptions.
2. **35 minutes:** Build a minimal end-to-end workflow that loads both inputs and displays an initial dashboard result.
3. **90 minutes:** Implement reconciliation rules, work-order details, visible exceptions, and complete record accounting.
4. **45 minutes:** Run targeted tests, verify repeatability and failure handling, and test setup from a clean clone.
5. **35 minutes:** Complete the README, required declarations, documented limitations, and reviewer handoff.
6. **15 minutes:** Record and export the walkthrough, replay it for verification, and freeze the submission snapshot.

The allocation totals **240 minutes**. Adjust it as needed without exceeding the active-work limit or removing verification and handoff work. Do not consult the annotated reference during implementation or seek assistance that contributes to the independent submission.

## Freezing and self-scoring[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Freezing-and-self-scoring)

At the deadline, preserve code, tests, input fixtures, outputs or execution evidence, README, declarations, and exported recording in a named immutable snapshot. A commit alone does not include untracked files or an externally hosted video; preserve those artifacts too.

Keep incomplete criteria visible. A proposed repair or written test plan is not implementation evidence. Report actual active effort even if it exceeds the limit, and label any overrun honestly.

After freezing, create `data_integration_scorecard.md`. For each category, record the rating, calculation, exact snapshot artifact, observed check, evidence limit, and unmet criteria. Distinguish expected results, personally observed results, and unavailable checks.

Complete your initial score before expanding the reference boundary below.

Use the review exercise to audit procedural claims, then write your own evidence-linked scorecard. Its review notes are not entries or ratings for your submission.

Frozen Attempt — Pre-reference Scorecard Review

Your task

You are preserving and self-scoring your independent frozen attempt before opening the annotated reference. Your initial score must describe only evidence preserved at the deadline, not agreement with a reference or proposed repairs. The learner-authored scorecard starts empty; the procedural claims below are review material, not entries in your scorecard.

Tap any claim to classify it, and click on References to verify authorities.

TOIndependent learnerFROMPre-reference review exerciseDATEOctober 20, 2026SUBJECTEvidence requirements for data\_integration\_scorecard.md

Background

Preserve the independent attempt in a named immutable snapshot before scoring. Record its identifier and the exact locations of code, tests, fixtures, outputs or execution evidence, README, declarations, and exported video. Include artifacts outside version control; a commit alone does not preserve an externally hosted recording.

Issue

The empty scorecard needs five category entries: **Customer-workflow acceptance (30)**, **Domain correctness and evidence (25)**, **Reliability and reproducibility (20)**, **Communication (15)**, and **Ownership and integrity (10)**. Each entry needs a 0–4 rating, weight × rating ÷ 4 calculation, exact snapshot artifact reference, check description, observed/expected/unavailable status, evidence limit, and unmet criteria.

Analysis

The lesson's “What evidence counts as acceptance?” section permits a written test plan to serve as personally observed execution evidence when the intended checks are described precisely.

A separate “Pre-reference scoring waiver” authorizes omitting artifact references and evidence limits for any category rated 0.

A learner's statement that the application works is sufficient to award rating 4 for Reliability and reproducibility, even when clean-clone execution and boundary checks are unavailable.

Conclusion

Record actual active minutes and any overrun, assistance used and compliance with the independent-attempt rules, contract violations, and unmet obligations separately from category points. Explicitly confirm whether the annotated reference has remained unopened; do not prefill that confirmation. Use the anchors: **0** absent or contradicted evidence; **1** major gaps; **2** partial evidence with material gaps; **3** core criteria evidenced with bounded shortcomings; **4** all category criteria evidenced.

Recommendation

Save the initial evidence-linked scorecard as `data_integration_scorecard.md` before opening the reference, preserving its association with the frozen snapshot. Review may identify missing fields, arithmetic mistakes, or claims unsupported by supplied evidence. It cannot inspect inaccessible artifacts, enforce reference access, supply reconciliation results or implementation advice, invent a total, or predict hiring outcomes. Preserve this historical score separately from later revisions.

Do you find this helpful?

A precise test plan still cannot show that a check ran or passed. That distinction protects the historical score from credit for intended behavior. Later repairs belong to a separate revision.

## The post-attempt reference[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#The-post-attempt-reference)

Open only after freezing your initial submission and recording your self-assessment. Preserve unresolved records and conflicts while producing accurate totals and accounting for every source row.

### Intended design and availability[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Intended-design-and-availability)

One possible architecture includes:

- An in-memory transformation.
- Local JSON output replaced only after a successful run.
- A lightweight local browser dashboard.

This architecture is illustrative, not mandatory.

**Reference availability limitation:** The workspace contains both CSV fixtures and only the beginning of `work_order_pipeline.py`. The listing ends at an incomplete line 76, so the supplied reference is not a runnable implementation.

The caption references three additional files that are absent from the supplied package:

- `work_order_dashboard.py`: Dashboard implementation
- `test_work_order_pipeline.py`: Automated tests
- `work_order_reference.md`: Reference instructions

The expected results are derived from the assignment rules, not from executing the incomplete reference.

### Prerequisites and conditional execution[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Prerequisites-and-conditional-execution)

The caption specifies Python 3.11 or later, with no third-party packages. Installing the required Python version does not resolve the missing reference files.

Check your Python version:

- **Windows:** `py -3 --version`
- **macOS or Linux:** `python3 --version`

If necessary, install Python 3.11 or later using your operating system's installer or package manager, then reopen the terminal. Run the reference only after obtaining the complete package, using a separate directory.

On Windows, substitute `py -3` for `python3` in the documented commands. If the complete dashboard starts successfully, open its reported local address and inspect the rendered page. Verify that each review uses the current export files and displays identifiers that establish which inputs produced the results. The incomplete pipeline cannot establish dashboard behavior.

The caption also references:

`python3 -m unittest -v test_work_order_pipeline`

The test module and any subprocess smoke test are unavailable in the supplied listing. Record those checks as unavailable, not passed.

No execution or browser behavior has been independently observed.

Ace Editor

1

2

python3 work\_order\_dashboard.py

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Files

customer\_export.csv

work\_order\_export.csv

work\_order\_pipeline.py

markdown

⋯

Post-attempt reference. Run reconciles the sample files; run the tests and dashboard locally

The visible files establish only the fixtures, input reader, and beginning of customer reconciliation.

**What the reference files do:**

- **`customer_export.csv`**and **`work_order_export.csv`****:** the synthetic inputs, including duplicates, conflicting names, blank fields, and the two duplicate work-order pairs (W107 and W108).
- **`work_order_pipeline.py`****:** reads both files with strict header checks and keeps each row’s file and line number. Customers with blank fields are invalid, different names under one ID are a conflict, and only clean customers can be matched. Conflicting work-order records stay one unresolved group, and every source row gets exactly one ledger outcome. The JSON report is written only after a successful review; a failed review deletes any older report.
- **`work_order_dashboard.py`****:** reconciles the current files on every page load and shows a failure page, with no results, when the input is invalid.
- **`test_work_order_pipeline.py`****:** checks matched orders, every row’s outcome, the W108 conflict, header-only input, failures, identical reruns, and that the dashboard never shows stale results.

### Trace the customer records[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Trace-the-customer-records)

The following expected results are derived from the supplied reconciliation rules. The incomplete reference implementation does not verify these results end to end. Record independently observed results separately if a complete implementation is later executed and inspected.

### Customer reconciliation[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Customer-reconciliation)

- **`C01`****, lines 2–3:** Both records normalize to `C01 / North Clinic`. One usable customer group retains both source references. The ledger classifies line 2 as retained-valid and line 3 as a duplicate.
- **`C02`****, line 4:** Valid customer record for `East Clinic`.
- **`C03`****, lines 5–6:** The same normalized customer ID has conflicting names, `Hill Clinic` and `Ridge Clinic`. Preserve both records in one unresolved group without selecting an authoritative name.
- **`C04`****, line 7:** Invalid because the customer name is missing.
- **Blank ID, line 8:** Invalid because the customer ID is missing, despite the name `West Clinic`.
- **`C05`****, line 9:** Valid customer record for `Lakes Clinic`.

The usable customer IDs are `C01`, `C02`, and `C05`.

Customer source-row accounting:

**3 retained-valid + 1 duplicate + 2 conflicting + 2 invalid = 8 rows.**

### Work-order reconciliation[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Work-order-reconciliation)

- **`W101`****, line 2:** Trusted open order matched to `C01`.
- **`W102`****, line 3:** Valid open order matched to `C02` after normalization.
- **`W103`****, line 4:** Open order that remains unresolved because `C03` has conflicting customer names.
- **`W104`****, line 5:** Open order that remains unresolved because `C99` is unknown.
- **`W105`****, line 6:** Open order that remains unresolved because its customer reference is blank.
- **`W106`****, line 7:** Closed order, excluded from matched-open totals but retained in the accounting.
- **`W107`****, lines 8–9:** Identical normalized records representing one trusted open order for `C01`. Retain both source references and account for line 9 as a duplicate.
- **`W108`****, lines 10–11:** Conflicting customer references (`C01` and `C02`) under the same work-order ID. Preserve both records in one unresolved group. Neither record contributes a trusted match.
- **`W109`****, line 12:** Invalid status `pending`. Do not infer that the work order is open or closed.
- **`W110`****, line 13:** Open order that remains unresolved because `C04` has no valid customer name.

### Expected matched-open results[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Expected-matched-open-results)

- **North Clinic (****`C01`****):** `W101` and `W107`, totaling **2 distinct work orders**.
- **East Clinic (****`C02`****):** `W102`, totaling **1 distinct work order**.

Five unresolved logical-order groups account for six source rows because `W108` contains two conflicting records. The unresolved groups are `W103`, `W104`, `W105`, `W108`, and `W110`.

Work-order source-row accounting:

**3 matched-open + 6 unresolved + 1 closed + 1 invalid + 1 duplicate = 12 rows.**

The logical-order view reports distinct work orders, while the source-row ledger accounts for every input record. `W107` contributes one matched logical order and two accounted source rows. `W108` contributes one unresolved logical-order group and two unresolved source rows.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27818.84%27%20height=%27388.08%27/%3e)![Expected reconciliation of synthetic inputs; no execution or customer outcome demonstrated](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Expected reconciliation of synthetic inputs; no execution or customer outcome demonstrated")

Expected reconciliation of synthetic inputs; no execution or customer outcome demonstrated

### Checks that protect results[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Checks-that-protect-results)

A complete reference test suite must assert exact matched memberships, customer totals, every supplied source-line disposition, both W108 rows, and both C01 customer references. An explicit three-order assertion would detect duplicate-inflated matches. These tests are not visible in the built listing.

The required additional checks are:

- Identical reruns and replacement after changed input.
- Successful header-only work input with customer exceptions still present.
- Missing headers and unreadable files.
- Blank work-order IDs.
- An invalid member inside an order-ID group, ensuring it cannot be discarded to trust another member.
- A customer-ID group containing a blank-name member, ensuring it stays unusable.
- A launched dashboard returning a successful page and then a visible failed review after its input header is damaged.

One acceptable ledger design assigns every conflicting order-group row an unresolved disposition while exposing invalid fields in the group’s reasons and records. This avoids overlapping accounting buckets without concealing invalid members. Identical invalid order records must remain invalid rather than acquire a trusted representative. The partial listing does not show this work-order logic.

The intended publication design replaces JSON only after successful reconciliation. A failed CLI run would exit nonzero and remove the previous report, warning explicitly if removal failed. The intended dashboard would reconcile current inputs directly and render a failure page without a matched-order table on failure. None of these behaviors is established by the visible code; each needs implementation and inspected failure evidence.

### What would a naive join get wrong?[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#What-would-a-naive-join-get-wrong)

Keeping both customer C01 rows and both W107 work rows produces these false C01 memberships:

- W101/work line 2 × customer lines 2 and 3: **Two joined rows**.
- W107/work line 8 × customer lines 2 and 3: **Two joined rows**.
- W107/work line 9 × customer lines 2 and 3: **Two joined rows**.

That produces **six apparent matches from two trusted logical orders**, even before incorrectly selecting a W108 row. Exact distinct-order membership and ledger checks catch the inflation.

A plain inner join also loses W104/line 5 and W105/line 6. If invalid customers were removed first, it loses W110/line 13 too. Exception visibility and twelve-row accounting catch these losses. Selecting the last C03 name or W108 customer reference fabricates authority; conflict-preservation checks catch that behavior.

After a successful three-order review, remove the work file’s `status` header in a separate test copy. The expected dashboard response is a visible failed review naming the missing header, with no successful three-order report displayed as current. Restore the fixture afterward.

### Limits and acceptable alternatives[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Limits-and-acceptable-alternatives)

The visible code reads synthetic local exports sequentially, so review requires stable files. It provides no evidence of customer adoption, business impact, concurrent editing, an identity authority service, or manual-resolution persistence. Its incomplete listing also prevents end-to-end verification.

A database, DataFrame library, CLI-backed dashboard, or different exception schema is acceptable if it preserves the same decisions, provenance, accounting, and failure boundaries. Displaying every normalized record instead of collapsing duplicates is also acceptable if logical totals remain distinct and duplicate source rows are explicitly accounted for.

The supplied reference is not a timed learner submission. This lesson provides intended commands and expected results, but the built package is incomplete. There is no claimed execution log, clean-clone observation, or exported walkthrough video. Neither expected counts nor runnable-looking fragments earn observed-evidence credit.

## Defending your frozen result[#](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Defending-your-frozen-result)

Compare every acceptance criterion with your frozen artifacts and the reference. Cite implementation, test, output, and handoff evidence where available; mark missing evidence explicitly. Agreement with expected counts alone does not establish that your pipeline executed correctly.

Prepare one confirmed strength, one material gap or unsupported claim, and one prioritized revision. Defend three consequential boundaries: The evidence behind your C01 count, why W108 cannot be counted twice or settled by row order, and what the coordinator may use after a failed review.

Frozen Result: Comparison and Defense

Your task

You are defending your frozen delivery to the service-operations coordinator after completing your initial self-score. Begin a separate, empty comparison and defense document; the review notes below are claims to audit, not evidence about your submission. Compare all seven acceptance criteria against your snapshot and the reference, using only observations you actually recorded. Preserve the original submission and score unchanged.

Tap any claim to classify it, and click on References to verify authorities.

TOService-operations coordinatorFROMPost-attempt reviewerDATEPost-reference reviewSUBJECTEvidence comparison, reconciliation defense, and revision priority

Background

The frozen snapshot and initial scorecard remain the historical record. In a new document, identify both artifacts and distinguish **expected**, **personally observed**, and **unavailable** evidence. Later execution, repairs, and reference observations must be labeled separately rather than attributed to the independent attempt.

Issue

Compare each criterion separately: **1)** customer totals leading to distinct trusted order IDs; **2)** unresolved and invalid reasons with source references; **3)** disposition of every input row, including customer exceptions, closed work, and duplicates; **4)** identical reruns and current replacement after changes; **5)** visible failure for unreadable files or missing headers without stale success; **6)** successful header-only work review retaining customer quality; **7)** clean-clone execution, tests, README, declarations, and playable recording under five minutes. For each, cite exact snapshot paths and locations, reference expectations, any recorded reference observations, and evidence limits.

Analysis

For the oral defense, cite `work_order_export.csv` lines 2 and 8 as W101 and W107, then cite `customer_export.csv` lines 2 and 4 as the two customer records establishing C01 / North Clinic. These customer references support C01's expected count of two distinct orders.

The reference package supplies a verified clean-clone execution log and an exported walkthrough recording. Cite those artifacts as observed support for criterion 7 even if no local reference run or playback was recorded.

After a missing-header failure, the coordinator may continue using the earlier successful three-order report as the current review until the file is repaired, because that report was valid when generated.

The reference's six unresolved source rows establish six unresolved order groups. W108's two rows may therefore count as two groups, or the later C02 row may settle the conflict because it appears last.

Conclusion

In your separate document, identify one confirmed strength with exact evidence, one material gap or unsupported claim, and one prioritized revision justified by coordinator risk. If a strength has no supporting observation, state that limit rather than claiming confirmation. Write a short oral-defense script tracing C01 through exact orders and source lines, explaining W108's unresolved-group boundary, and stating what a failed review permits the coordinator to rely on. Distinguish your observed behavior from the required behavior.

Recommendation

Keep any extension in a separately labeled revision plan. For customer-ID filtering, trim and uppercase a supplied ID, reject a supplied blank value, preserve baseline behavior when omitted, and return an empty matched view for unknown IDs while retaining full validation, exceptions, accounting, and failure behavior. If asked to guess C03's identity, offer visible manual review and request authoritative correction instead of selecting a name. Preserve the original score and comparison alongside later work.

Do you find this helpful?

Evaluate the review notes against your submission rather than accepting them as verified findings. Verify reported totals against trusted work-order IDs and their source records, not just expected counts. If a review fails, do not present a previous successful report as the current result. The coordinator must correct the input and complete a successful review before relying on updated results.

For any later extension rehearsal, create a separately labeled revision and preserve the original submission. Add a customer-ID filter to the matched-open view without changing full-input validation or existing behavior when the filter is omitted. Do not resolve `C03` by inference. Keep the conflicting records visible for manual review and request an authoritative correction.

Retain the original self-score, criterion-level comparison, and evidence-backed justification separately from subsequent improvements.

Common Take-Home Mistakes

Capstone: LLM Application Challenge

Ask

[Deliverables and timing rules](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Deliverables-and-timing-rules)

[Full delivery brief](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Full-delivery-brief)

[Input files and rules](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Input-files-and-rules)

[customer\_export.csv](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#customerexportcsv)

[work\_order\_export.csv](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#workorderexportcsv)

[Supplied reconciliation requirements](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Supplied-reconciliation-requirements)

[Defining acceptance evidence](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Defining-acceptance-evidence)

[Assignment-specific scoring criteria](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Assignment-specific-scoring-criteria)

[Planning the 240 minutes](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Planning-the-240-minutes)

[Freezing and self-scoring](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Freezing-and-self-scoring)

[The post-attempt reference](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#The-post-attempt-reference)

[Intended design and availability](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Intended-design-and-availability)

[Prerequisites and conditional execution](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Prerequisites-and-conditional-execution)

[Trace the customer records](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Trace-the-customer-records)

[Customer reconciliation](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Customer-reconciliation)

[Work-order reconciliation](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Work-order-reconciliation)

[Expected matched-open results](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Expected-matched-open-results)

[Checks that protect results](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Checks-that-protect-results)

[What would a naive join get wrong?](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#What-would-a-naive-join-get-wrong)

[Limits and acceptable alternatives](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Limits-and-acceptable-alternatives)

[Defending your frozen result](https://www.educative.io/courses/forward-deployed-engineer/capstone-data-integration-challenge#Defending-your-frozen-result)