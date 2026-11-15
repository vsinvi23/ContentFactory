# Writing_Effective_READMEs_for_AI_System_Delivery_and_Verification

Source: https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Writing the README

Explore how to lead a README with the customer outcome and the shortest verification route. Understand how to label expected, reported, and personally observed results, and how to document failure behavior and boundaries, preparing you to write handoffs a reviewer can follow and check.

We'll cover the following...

- [Structuring the README](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Structuring-the-README)
- [Gathering delivery facts first](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Gathering-delivery-facts-first)
- [A worked README example](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#A-worked-README-example)
  - [Invoice review, worked README](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Invoice-review-worked-README)
    - [Purpose and approach](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Purpose-and-approach)
    - [Quick verification and prerequisites](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Quick-verification-and-prerequisites)
    - [Sample input and expected output](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Sample-input-and-expected-output)
    - [Tests](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Tests)
    - [Failure check and existing reports](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Failure-check-and-existing-reports)
    - [Assumptions, scope, and repository map](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Assumptions-scope-and-repository-map)
  - [End of worked README](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#End-of-worked-README)
- [Auditing the README commands](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Auditing-the-README-commands)
- [Choosing the right context](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Choosing-the-right-context)
- [Repairing overstated claims](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Repairing-overstated-claims)
- [Practice: the ticket-ageing README](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Practice-the-ticket-ageing-README)

These are the two questions a fictional invoice-review handoff must answer.

“Which invoices need follow-up?”

“How can I reproduce that answer?”

An accounts-receivable coordinator needs a locally generated list of overdue, unpaid invoices for manual follow-up. Stakeholders need to understand the user's task, expected output, and workflow limitations. Engineers also need input requirements, execution commands, filtering rules, and verification steps.

A README should explain the customer's task and provide a reproducible workflow that reviewers can verify independently. Setup instructions alone do not explain the project's purpose, while a project description without execution and verification steps does not establish reproducibility.

## Structuring the README[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Structuring-the-README)

Put the customer outcome and shortest verification route before implementation detail. A practical course structure covers:

- Customer problem and intended value.
- Approach and decision rules.
- Prerequisites, setup, and usage.
- Expected outputs and failure behavior.
- Tests and their coverage limits.
- Assumptions and operational boundaries.

Adapt that structure to the assignment’s requested artifacts. It is not a mandatory employer template.

Public take-home guidance recommends working code, sensible structure, edge-case handling, and concise explanations of assumptions and choices. It does not establish a universal scoring weight for README quality.

## Gathering delivery facts first[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Gathering-delivery-facts-first)

Start with delivery facts rather than adjectives. For this writing exercise, the fictional delivery packet stipulates:

- **Runtime:** Python 3.11 or later, standard library only.
- **Files:** `invoice_review.py`, `samples/invoices.csv`, `samples/invoices_bad.csv`, and `test_invoice_review.py`.
- **Execution:** Commands run from the repository root. The program creates the output directory.
- **Rule:** Select unpaid invoices whose `due_date` is strictly before the supplied `--as-of` date, preserving source order.
- **Writing:** Validate the entire input before writing; replace the report on a successful run.

The packet also supplies expected outputs, a failure contract, and a report of eight passing tests. These are fictional exercise inputs: this lesson supplies no runnable implementation and has not executed these commands. The README below is a writing specimen, not an instruction to run nonexistent files.

Keep three evidence labels distinct:

- **Expected:** A result derived from the stated rules and input.
- **Packet-reported:** An observation asserted by the fictional delivery packet.
- **Personally observed:** Something the learner actually executes and inspects.

The matching activity also includes Unsupported for claims the available evidence does not establish. Classify each claim or hypothetical scenario before using it in a handoff.

What supports each claim?

Claim or scenario

The tool saves hours and is production-ready.

From the sample and rules, only I101 and I104 qualify as of 2026-04-15.

The fictional delivery packet says eight tests passed.

Suppose you run a real implementation and inspect its report: it contains only I101 and I104.

Evidence label

Packet-reported

Unsupported

Expected

Personally observed

Match each claim to its evidence label. The learner-run scenario is hypothetical: this lesson supplies no runnable files, and no personal run is assumed.

Do you find this helpful?

An expected result helps a reviewer detect disagreement. It becomes execution evidence only when someone runs the command and inspects what happened. Similarly, a successful local fixture would not demonstrate live-service reliability.

## A worked README example[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#A-worked-README-example)

Review the sample README below. It connects the customer's task to a named sample file, a specified run date, and a report that reviewers can verify.

### Invoice review, worked README[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Invoice-review-worked-README)

#### Purpose and approach[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Purpose-and-approach)

This local tool helps an accounts-receivable coordinator find overdue unpaid invoices for manual follow-up. It validates a CSV, selects unpaid invoices due strictly before an explicit review date, and writes a two-column follow-up list in source order.

It neither contacts customers nor synchronizes a billing system. No measured time savings or adoption evidence is available.

#### Quick verification and prerequisites[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Quick-verification-and-prerequisites)

Use Python 3.11 or later. No third-party dependencies are required. The fictional packet does not specify credential or configuration requirements. The examples use local CSV mode; there is no live-service mode.

Open a terminal in the repository root, the directory containing `invoice_review.py`. Check that `python --version` reports Python 3.11 or later, then run:

Ace Editor

1

2

python invoice\_review.py --input samples/invoices.csv --as-of 2026-04-15 --output out/overdue.csv

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The program creates `out/` if needed. Input and output paths are relative to the repository root.

If your Python installation uses `python3` on macOS or Linux, substitute `python3` in every command. On Windows, `py -3.11` is an alternative when that interpreter is installed; use the same interpreter for the report and tests.

#### Sample input and expected output[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Sample-input-and-expected-output)

The named input, `samples/invoices.csv`, contains:

Ace Editor

1

2

3

4

5

6

7

invoice\_id,due\_date,paid

I101,2026-04-10,false

I102,2026-04-15,false

I103,2026-04-01,true

I104,2026-04-14,false

I105,2026-04-18,false

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** Names the required fields.
- **Lines 2 and 5:** I101 and I104 are unpaid and due before April 15, so they qualify.
- **Line 3:** I102 is due on April 15; strict comparison excludes it.
- **Line 4:** I103 is paid, so its earlier due date does not qualify it.
- **Line 6:** I105 is due after the review date, so it is excluded.

For this input, date, and local CSV mode, expected stdout is:

Ace Editor

1

Wrote 2 overdue invoices to out/overdue.csv

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Expected contents of `out/overdue.csv` are:

Ace Editor

1

2

3

invoice\_id,due\_date

I101,2026-04-10

I104,2026-04-14

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The two qualifying records retain their source order. These are expected results from the supplied contract, not a claim of personal execution.

#### Tests[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Tests)

From the repository root, run:

Ace Editor

1

python -m unittest discover -s . -p 'test\_invoice\_review.py'

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The fictional delivery packet reports eight passing tests covering:

- Strict date comparison and paid exclusion.
- Source-order preservation and header-only input.
- Malformed dates, missing columns, and duplicate IDs.
- Report replacement on a successful run.

These checks cover supplied cases; they do not establish production readiness or customer adoption. The sample output makes the workflow inspectable, while the tests check particular behaviors and boundaries.

#### Failure check and existing reports[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Failure-check-and-existing-reports)

The supplied `samples/invoices_bad.csv` contains an invalid date on physical line 3. Run:

Ace Editor

1

python invoice\_review.py --input samples/invoices\_bad.csv --as-of 2026-04-15 --output out/overdue.csv

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The expected exit status is `2`, with stderr:

Ace Editor

1

Invalid due\_date at line 3

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The program validates the entire file before writing, so this failure does not replace an existing report. An older `out/overdue.csv` may remain on disk: it is not a result for the failed input. Correct the input and rerun successfully before treating a report as current.

#### Assumptions, scope, and repository map[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Assumptions-scope-and-repository-map)

Dates are ISO calendar dates; `paid` is exactly `true` or `false`; invoice IDs must be unique. Supplying `--as-of` explicitly makes the example independent of the machine’s current date.

Scope is local CSV review and manual follow-up. Billing integration is omitted, and no integration is simulated.

- `invoice_review.py`: CLI entry point, validation, selection, and report writing.
- `samples/invoices.csv`: Valid sample used above.
- `samples/invoices_bad.csv`: Invalid-date failure sample.
- `test_invoice_review.py`: Focused behavioral checks.

### End of worked README[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#End-of-worked-README)

That evidence chain makes the customer claim independently checkable.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27825.93%27%20height=%27328.23%27/%3e)![Expected results from the fictional contract, not observed execution: successful validation replaces the report, while validation failure can leave an earlier report on disk](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Expected results from the fictional contract, not observed execution: successful validation replaces the report, while validation failure can leave an earlier report on disk")

Expected results from the fictional contract, not observed execution: successful validation replaces the report, while validation failure can leave an earlier report on disk

The file’s existence alone cannot establish success. After the invalid-date run, the same path may still contain the earlier two-row report. Exit status, error output, and report provenance determine whether it belongs to the current request.

## Auditing the README commands[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Auditing-the-README-commands)

As in the Code Quality, Testing, and Reproducibility lesson, document the clean-clone route precisely: working directory, input and output paths, and any relevant configuration.

For a real submission, audit the README this way:

1. Start from a clean clone with only the documented prerequisites.
2. Copy the commands exactly, using the documented interpreter alternative if necessary.
3. Inspect stdout and the report contents against the named sample and mode.
4. Run the failure check and confirm that any retained report is understood as older output.
5. Run the tests and record what actually passed or failed.

Record personal observations separately from expected results and someone else’s reported run. If you change a command during the audit, repair the README and repeat the copied route.

## Choosing the right context[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Choosing-the-right-context)

Retain explanations that affect how reviewers interpret the results. Treating dates as ISO-formatted calendar dates is a documented assumption about how input values are interpreted. Document the absence of billing synchronization as a scope exclusion. A stub simulates a dependency's behavior, such as returning a predefined billing API response. Document assumptions, scope exclusions, and simulated behavior separately. Distinguish intentionally excluded features from implemented code paths that simulate unavailable functionality.

Include a concise repository map showing where to find the implementation, test fixtures, and verification artifacts. Alternative architectures and extensive future-work lists add little value when reviewing this two-row report. Document the workflow's limitations and excluded capabilities without adding unrelated implementation details.

## Repairing overstated claims[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Repairing-overstated-claims)

Consider this flawed README:

> Automates collections and saves hours. Install Python. Run `python invoice_review.py`. All tests pass. Production-ready.

Its invocation omits the input, date, and output arguments. It also changes manual follow-up into automated collections, asserts unmeasured savings, and turns a bounded test report into a readiness claim.

Repair the actual sentences and execution route.

Repair the invoice handoff

Your task

You are reviewing an invoice README before it reaches an accounts-receivable coordinator and an engineer. Replace the flawed five-sentence draft with a concise handoff paragraph, commands, and expected result grounded in the fictional delivery contract. This is a writing exercise: no runnable implementation is supplied, and no execution should be claimed.

Tap any claim to classify it, and click on References to verify authorities.

TOInvoice handoff reviewerFROMREADME authorDATEOctober 19, 2026SUBJECTLocal invoice review: purpose, reproduction, and evidence

Background

An accounts-receivable coordinator needs a local list of overdue unpaid invoices for manual follow-up. An engineer needs enough information to reproduce and inspect that list.

Issue

The draft's five sentences appear below. Review their wording and the accompanying evidence claims against the delivery contract.

Analysis

> “Automates collections and saves hours.”

This describes the tool's customer value.

> “Install Python. Run `python invoice_review.py`.”

These instructions reproduce the delivery contract's sample invocation.

> “All tests pass. Production-ready.”

The fictional delivery packet certifies production readiness through its test report.

Conclusion

The replacement must make the expected successful result inspectable and explain how a failed run affects an existing report.

Recommendation

Write a concise replacement paragraph plus commands and expected result. Include the manual-review purpose, prerequisites, working directory, valid invocation, expected IDs, qualified test evidence, and invalid-date/stale-output boundary. Change only the replacement text; do not execute commands or report execution.

Do you find this helpful?

A targeted repair connects the customer’s manual task to the exact sample command and expected two-row report. “The fictional packet reports eight passing tests” preserves the available evidence; “all tests pass” leaves both the speaker and the scope unclear.

## Practice: the ticket-ageing README[#](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Practice-the-ticket-ageing-README)

Use this independent fictional delivery packet. No runnable implementation is supplied; your deliverable is a compact README.

- **Customer task:** A support coordinator needs a local list of older open tickets for manual follow-up.
- **Prerequisites:** Python 3.11+, no third-party dependencies, repository-root execution.
- **Files:** `ticket_ageing.py`, `samples/tickets.csv`, and `test_ticket_ageing.py`.
- **Command:** `python ticket_ageing.py --input samples/tickets.csv --as-of 2026-05-10 --output out/follow_up.csv`.
- **Behavior:** Creates the output directory, validates all rows, and writes `ticket_id,opened_date` for open tickets opened strictly before `2026-05-03`, preserving source order.

The sample is:

Ace Editor

1

2

3

4

5

6

ticket\_id,opened\_date,status

T201,2026-05-01,open

T202,2026-05-03,open

T203,2026-04-20,closed

T204,2026-05-02,open

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** Supplies the required columns.
- **Lines 2 and 5:** T201 and T204 qualify because they are open and precede the cutoff.
- **Line 3:** T202 is exactly on the cutoff and is excluded.
- **Line 4:** T203 is closed and is excluded.

Expected output is:

Ace Editor

1

2

3

4

ticket\_id,opened\_date

T201,2026-05-01

T204,2026-05-02

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Expected stdout is `Wrote 2 tickets to out/follow_up.csv`.

Tests run with `python -m unittest discover -s . -p ‘test_ticket_ageing.py’`. The packet reports six passing tests: Strict cutoff, closed exclusion, source order, empty input, malformed dates, and missing columns.

A missing required column exits with status `2`, names the column on stderr, and does not replace an existing output. Assumptions are ISO calendar dates, unique ticket IDs, and status exactly `open` or `closed`. The tool supports manual follow-up only, has no live helpdesk connection, and has no measured customer-impact evidence.

Write your compact README from the packet. Then use the handoff audit below to review a supplied draft containing deliberate errors. Trace one workflow claim, one command, one expected result, and one boundary back to the packet.

Ticket-ageing README — Handoff Audit

Your task

You are preparing a compact README for a reviewer and a support coordinator who needs older open tickets for manual follow-up. The fictional ticket-ageing packet is the sole evidence source. The handoff must explain an executable route without implying personal execution: no runnable implementation is supplied. Its audit must trace one workflow claim, one command, one expected result, and one boundary to the packet.

Tap any claim to classify it, and click on References to verify authorities.

TOHandoff reviewerFROMREADME authorDATEOctober 19, 2026SUBJECTLocal ticket-ageing workflow and verification boundaries

Background

## Purpose and approach

Help a support coordinator identify older open tickets for manual follow-up. Validate all rows, select open tickets opened strictly before `2026-05-03` for the supplied `--as-of 2026-05-10` example, and preserve source order. This is a local CSV workflow, not a live helpdesk connection; no measured customer-impact evidence is available.

Issue

## Prerequisites and route

Use Python 3.11+ with no third-party dependencies. Run from the repository root, containing `ticket_ageing.py`:

1

python ticket\_ageing.py --input samples/tickets.csv --as-of 2026-05-10 --output out/follow\_up.csv

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The program creates the output directory. Repository map: `ticket_ageing.py` is the program; `samples/tickets.csv` is the supplied sample; `test_ticket_ageing.py` contains the tests.

Analysis

## Expected report

The packet's sample and cutoff rule support the following expected contents of `out/follow_up.csv`:

1

2

3

4

5

ticket\_id,opened\_date

T201,2026-05-01

T202,2026-05-03

T203,2026-04-20

T204,2026-05-02

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

## Failure behavior

A missing required column exits with status `2` and does not replace an existing report. The packet specifies the exact stderr template `ERROR: required column {column} is missing`. An older report may remain on disk and must not be treated as output for the failed input; correct the input and rerun successfully before treating it as current.

## Tests and verification

Run `python -m unittest discover -s . -p 'test_ticket_ageing.py'` from the repository root. The packet reports six passing tests covering strict cutoff, closed exclusion, source order, empty input, malformed dates, and missing columns. I personally ran these tests and inspected the generated CSV, confirming production readiness and reduced support workload.

Conclusion

## Expected stdout and assumptions

Expected stdout for the supplied command is `Wrote 2 tickets to out/follow_up.csv`. This is an expected result, not an observed run. Assume ISO calendar dates, unique ticket IDs, and status exactly `open` or `closed`. No implementation is supplied here, so this writing exercise does not execute or verify files.

Recommendation

## Four-item trace audit

1. **Workflow claim:** Local identification of older open tickets for manual follow-up → packet customer task and behavior.
2. **Command:** The root-relative invocation above → packet command and prerequisites.
3. **Expected result:** Only `T201,2026-05-01` and `T204,2026-05-02`, under `ticket_id,opened_date` → packet sample, strict cutoff, and closed exclusion.
4. **Boundary:** No live helpdesk connection or measured impact evidence → packet scope.

Revise the README wherever its claims disagree with these traces, retaining the stale-output warning and distinguishing expected results from packet-reported tests.

Do you find this helpful?

A draft can copy the command correctly yet misrepresent its result. Audit the connections too: sample membership must follow the selection rule, and retained output must not imply a successful current run.

Once that handoff is verifiable, the next question is which delivery decisions deserve an explanation,and which improvements the evidence actually justifies.

Building a Demonstrable Interface

Documenting Trade-Offs and Limitations

Ask

[Structuring the README](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Structuring-the-README)

[Gathering delivery facts first](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Gathering-delivery-facts-first)

[A worked README example](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#A-worked-README-example)

[Invoice review, worked README](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Invoice-review-worked-README)

[Purpose and approach](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Purpose-and-approach)

[Quick verification and prerequisites](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Quick-verification-and-prerequisites)

[Sample input and expected output](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Sample-input-and-expected-output)

[Tests](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Tests)

[Failure check and existing reports](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Failure-check-and-existing-reports)

[Assumptions, scope, and repository map](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Assumptions-scope-and-repository-map)

[End of worked README](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#End-of-worked-README)

[Auditing the README commands](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Auditing-the-README-commands)

[Choosing the right context](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Choosing-the-right-context)

[Repairing overstated claims](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Repairing-overstated-claims)

[Practice: the ticket-ageing README](https://www.educative.io/courses/forward-deployed-engineer/writing-the-readme#Practice-the-ticket-ageing-README)