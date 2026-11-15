# Building_a_User_Interface_for_Stock_Review_with_Streamlit

Source: https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Building a Demonstrable Interface

Explore how to build a thin interface that collects inputs, calls working logic, and shows results tied to the current run. Understand how to handle empty, invalid, and replaced inputs without showing stale results, and how to plan a timed demo route, preparing you to show your work truthfully in under five minutes.

We'll cover the following...

- [Designing the opening screen](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Designing-the-opening-screen)
- [Choosing the minimal controls](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Choosing-the-minimal-controls)
- [Building the Streamlit app](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Building-the-Streamlit-app)
- [Handling edge-case uploads](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Handling-edge-case-uploads)
- [Planning a timed demo](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Planning-a-timed-demo)
- [Handling live-service failures](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Handling-live-service-failures)
- [Practice: The stock trial](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Practice-The-stock-trial)

## Designing the opening screen[#](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Designing-the-opening-screen)

Review stock levels and identify reorder recommendations. The application does not place orders. Display this scope statement before the coordinator interacts with the application.

A stock coordinator uses a local browser application to upload a CSV file, review reorder recommendations, and investigate invalid records. The coordinator places orders outside the application.

The opening screen must display the following input requirements and workflow constraints:

- **Required CSV columns:** `sku`, `on_hand`, and `reorder_point`.
- **Validation:** Both `on_hand` and `reorder_point` must contain nonnegative integers. The `sku` field must not be blank.
- **Review output:** The review generates reorder recommendations and identifies invalid rows that require correction.
- **Execution:** All calculations run locally. The application does not submit purchase orders.

A **thin interface** accepts user inputs, invokes the existing business logic, and displays results without duplicating decision logic. Every displayed result must correspond to the input and execution that generated it.

Use Streamlit for this example to support the required browser-based file upload and result display. A command-line interface (CLI) would be sufficient if the brief required only command-line interaction. Other lightweight options, such as Gradio, may also meet the requirements. The assignment does not mandate a specific framework.

## Choosing the minimal controls[#](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Choosing-the-minimal-controls)

One CSV uploader and an explicit “Review stock” button are enough. Before visual polish, provide the inputs, execution action, useful outputs, supporting evidence, and actionable empty and error states.

After processing, show:

- The current filename and execution mode: `Local input , local calculation`.
- Counts accounting for every input row: Reorder, no reorder, or review.
- Recommendations containing SKU, `on_hand`, `reorder_point`, proposed quantity, and source row.
- Review items containing the available SKU, source row, rejected value or missing field, and correction guidance.

An explicit no-reorder message handles a successful run with no recommendations. Charts, login, hosting, editable grids, and automated purchasing have no required job here. The coordinator can correct verified values in the local CSV and rerun.

## Building the Streamlit app[#](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Building-the-Streamlit-app)

Keep this example in its own folder; it does not change earlier examples or a shared README. The prerequisites are Python 3.11 or later and the Streamlit dependency installed below.

Create and activate a virtual environment on macOS or Linux:

Ace Editor

1

2

python3 -m venv .venv

source .venv/bin/activate

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

On Windows PowerShell:

Ace Editor

1

2

py -m venv .venv

.venv\Scripts\Activate.ps1

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

If PowerShell blocks activation, use `.venv\Scripts\python.exe` in place of `python` in the following commands; activation is optional.

Save this complete file as `stock_review_app.py`:

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

15

16

17

18

19

20

21

22

23

24

25

26

27

import csv

import io

import streamlit as st

COLUMNS = ("sku", "on\_hand", "reorder\_point")

def review\_stock(data):

try:

text = data.decode("utf-8-sig")

except UnicodeDecodeError as exc:

raise ValueError("Unreadable bytes; save the CSV as UTF-8.") from exc

try:

reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)

headers = reader.fieldnames or []

missing = [name for name in COLUMNS if name not in headers]

if missing:

raise ValueError("Missing required columns: " + ", ".join(missing))

if len(headers) != len(set(headers)):

raise ValueError("Duplicate column names; use unique headers.")

report = {"total": 0, "reorder": [], "no\_reorder": 0, "review": []}

for row in reader:

source\_row = reader.line\_num

report["total"] += 1

sku = (row.get("sku") or "").strip()

errors = []

if None in row:

errors.append("Extra fields beyond the header")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Lines 1–5:** Import the CSV reader, in-memory text stream, and interface library; declare the input contract once.
- **Lines 7–19:** Decode UTF-8 and validate the headers. A missing required column prevents a successful run.
- **Lines 20–38:** Read records and validate values explicitly. Decimal digits represent nonnegative integers; blanks, negative values, and fractions produce review reasons.
- **Lines 39–49:** Assign each record exactly one disposition. Only a valid row strictly below its reorder point receives a recommendation for the difference.
- **Lines 50–51:** Convert CSV parser errors into a concise recovery message. No partially accumulated report is returned.
- **Lines 53–67:** Build the opening screen and require an explicit review action. Merely selecting a file produces no current result.
- **Lines 68–76:** Call the calculation once, stop rendering on failure, and label successful results with their filename and counts.
- **Lines 77–91:** Render zero-row success, recommendations, and review items separately, then expose the application entry point.

The source reference uses the CSV reader’s physical line number at the end of each record. In the supplied files, every record occupies one line: The header is row 1, and the first stock record is row 2. These references belong to that file, not to a durable inventory identity.

Install Streamlit and launch from the folder containing the file:

Ace Editor

1

2

3

python -m pip install streamlit

python -m streamlit run stock\_review\_app.py

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Open the local browser address printed by the launch command. Keep that command available for the reviewer; the app needs no credentials, service connection, or retained local report.

Create `stock_sample.csv` using this synthetic sample input:

Ace Editor

1

2

3

4

5

sku,on\_hand,reorder\_point

K10,2,5

K11,8,5

K12,,4

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** Supplies the required headers.
- **Lines 2–4:** Cover a recommendation, a valid no-reorder record, and an invalid record.

Predict the dispositions before running the file.

Technical Quiz

1.

Before you run `review_stock` on `stock_sample.csv`, what result should you expect?

A.

K12’s missing `on_hand` makes the whole file fail. Show a failure message instead of any results or summary.

B.

K10: order placed for 3 (row 2).

K11: no reorder (row 3). K12: review; `on_hand` missing (row 4).

Summary: 1 reorder + 1 no reorder + 1 review = 3.

C.

K10: recommend 3 (row 2). K11: no reorder (row 3).

K12: review, on\_hand missing (row 4).

Summary: 1 reorder + 1 no reorder + 1 review = 3. No orders placed

D.

K10: recommend 3 (row 2). K11: no reorder (row 3).

K12: treat blank on\_hand as 0 and recommend 4 (row 4).

Summary: 2 reorder + 1 no reorder + 0 review = 3. No orders placed

---

1 / 1

Treating a blank quantity as zero would turn missing evidence into an actionable recommendation. Keeping that row visible for review lets the coordinator correct it without losing recommendations from valid rows. The disposition counts also provide a completeness check: every input record must be accounted for, even when it cannot support a recommendation.

## Handling edge-case uploads[#](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Handling-edge-case-uploads)

Create three more files:

`stock_no_reorder.csv`:

Ace Editor

1

2

sku,on\_hand,reorder\_point

K11,8,5

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

`stock_empty.csv` contains only:

Ace Editor

1

sku,on\_hand,reorder\_point

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

`stock_bad_schema.csv`:

Ace Editor

1

2

sku,on\_hand

K10,2

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

These inputs produce different expected states:

- **Header only:** Successful review, zero input rows, and `No stock rows supplied.`
- **K11 only:** Successful review, one no-reorder record, no review items, and `No reorder recommendations from valid rows.`
- **Missing column:** `Review failed for stock_bad_schema.csv: Missing required columns: reorder_point`, followed by a correction or replacement action.
- **Unreadable bytes or malformed CSV:** A failed review with the filename, encoding or parsing cause, and recovery guidance.

A blank recommendation area cannot communicate these distinctions.

Consider this faulty screen after a successful sample run followed by the bad-schema file:

> **Selected input:** `stock_bad_schema.csv`  
> **Missing required columns:** `reorder_point`  
> **Reorder recommendations:** K10, quantity 3

The quantity 3 is real evidence from an earlier execution, but the new filename makes it look current. Adding a red error banner does not repair that false association.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27651%27%20height=%27201%27/%3e)![Replacing the upload clears the earlier result, and a failed review shows no recommendation table for the current input](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Replacing the upload clears the earlier result, and a failed review shows no recommendation table for the current input")

Replacing the upload clears the earlier result, and a failed review shows no recommendation table for the current input

The supplied implementation avoids that state by keeping `report` local to the current button-triggered execution. Streamlit reruns the script when the upload changes; the button is no longer active, so execution returns at the “No current result” message. There is no report in session state or a cache to reappear beneath a new filename.

Stock review: predict each change before revealing feedback

↓ Entry

🚦A — Current-run state

📄A — Replace the sample

↓ Entry

🛑B — Stop on failure

⚠️B — Review bad schema

↓ Entry

🧮C — Calculation owns decisions

📊C — Review equality

106%

Failure simulator

Pick a component to knock out — see how far the damage spreads.⌀ badges show each node’s blast radius — the bigger the number, the closer it is to a single point of failure.

Do you find this helpful?

On failure, the early return prevents all successful-output rendering. Even a parse error encountered after some readable records returns no partial successful report. If you later add downloads, generate and label them from the same successful report and input; retaining an old download under a new filename recreates the same problem.

## Planning a timed demo[#](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Planning-a-timed-demo)

Begin with the customer task, execute the workflow, inspect its result and evidence, and demonstrate a meaningful boundary or failure. This follows the outcome-focused walkthrough and deliberate-failure habit described in the supplied guidance.

Launch the application before the rehearsal. Time only the user interactions:

1. **0:00–0:25:** Explain the coordinator’s task and clarify that the application does not place orders.
2. **0:25–1:15:** Upload `stock_sample.csv` and click **Review stock**.
3. **1:15–2:15:** Verify `K10`’s recommended reorder quantity against its source values. Then inspect `K12`’s missing-value reason and required correction.
4. **2:15–3:05:** Upload and review `stock_no_reorder.csv` to demonstrate a valid result with no reorder recommendations. Then upload `stock_bad_schema.csv` and show the schema-validation error without displaying stale results.
5. **3:05–3:50:** Reload and review `stock_sample.csv`. Explain that the coordinator must place any recommended orders outside the application and investigate `K12` separately.
6. **3:50–4:20:** Identify the synthetic test data, confirm that calculations ran locally, and distinguish demonstrated functionality from untested behavior.

This is an inspection route, not a video-production script. The course target is less than five minutes; the assignment’s duration and deliverable requirements take precedence. If file switching consumes the route, improve the interaction or rehearse it again rather than timing only your introduction.

## Handling live-service failures[#](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Handling-live-service-failures)

This worked app has no live dependency beyond its local runtime. For an assignment that requires a service, preflight the connection and prepare a fallback only if the assessment permits it.

If the request fails during the demonstration, show the actual failure and bound the outage attempt so it does not consume the remaining time. Before using synthetic responses, display:

> Fixture mode, synthetic service responses; live request failed.

Identify which behavior the fixture illustrates, such as rendering a recommendation from a known response. Fixture success supplies no evidence that the failed live integration worked, and cannot satisfy a required live-integration criterion.

A prerecorded fallback needs a different label: State that it is prerecorded and identify the earlier run’s mode and provenance. Never describe a screenshot or earlier recording as current execution.

## Practice: The stock trial[#](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Practice-The-stock-trial)

Create your own `stock_trial.csv`:

Ace Editor

1

2

3

4

5

6

sku,on\_hand,reorder\_point

K20,0,6

K21,4,4

K22,-1,3

K23,7,2

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

- **Line 1:** Declares the same input contract.
- **Lines 2–3:** Test a reorder and equality at the threshold.
- **Lines 4–5:** Test an invalid negative quantity and a valid above-threshold quantity.

Start in the empty `observation_record.md`. Record predictions before execution, then collect browser observations and evidence from an actual timed demonstration. Open `self_check.md` only after your attempt.

Files

observation\_record.md

task.md

stock\_trial.csv

stock\_empty.csv

stock\_bad\_schema.csv

self\_check.md

markdown

⋯

Non-runnable response workspace. Write in the empty observation\_record.md; run Streamlit locally, outside this widget. Open self\_check.md only after your attempt. This widget does not execute or verify the browser app.

The workspace contains instructions and input files, not a second implementation:

In the `task.md` file:

- **Lines 3–5:** Define the local execution boundary and evidence labels. These prevent predictions from being recorded as observed behavior.
- **Lines 7–8:** Require predictions before execution, followed by the launch command and browser evidence. Source values and row references make recommendations inspectable.
- **Lines 9–10:** Require separate zero-row, replacement, and failed-run checks. Inspecting before and after the button press tests both execution boundaries.
- **Line 11:** Requests a concrete repair and repeated check only when inspection supports a change. It also permits an evidence-backed conclusion that no repair is needed.
- **Line 12:** Requires verification before editing K22, then a prediction and rerun. This separates a source correction from merely changing data to obtain a desired result.
- **Line 13:** Defines the actual timed demonstration and its evidence. An estimate cannot establish that the interaction fits the time limit.
- **Lines 15–19:** Separate the hypothetical outage response from local execution and defer the self-check until after the attempt.

In the `stock_trial.csv` file:

- **Lines 1–3:** Reuse the familiar CSV contract and supply below-threshold and equality cases. Together, they test the strict comparison boundary.
- **Lines 4–5:** Supply an invalid negative quantity and an above-threshold case. Change **line 4** only after completing the verification step in `task.md`, **line 12**; predict the new disposition before rerunning.

In the `stock_empty.csv` file:

- **Line 1:** Supplies valid headers without stock records, allowing you to distinguish empty success from processing failure.

In the `stock_bad_schema.csv` file:

- **Lines 1–2:** Supply an incomplete header and a matching record. This tests required-column validation rather than row-level quantity validation.

In the `self_check.md` file:

- **Lines 3–7:** Distinguish expected checks from execution evidence and provide the original trial’s expected dispositions and provenance requirements.
- **Lines 8–10:** Specify the empty-success and stale-result checks, plus the evidence needed for any interface repair.
- **Lines 11–13:** Provide corrected-run expectations, measured-demo criteria, and the customer-action boundary. Compare these with your record only after attempting the work.
- **Lines 15–19:** Provide the fallback label and limits on the live-integration claim. Keep that hypothetical answer separate from observations of this local app.

Keep “planned route” separate from “completed timed run.” If inspection exposes an interface problem, make one evidence-driven improvement and repeat the relevant check. For your own submission, identify the exact input, execution mode, and next customer action a reviewer should be able to verify without your narration.

Designing Around the End User's Workflow

Writing the README

Ask

[Designing the opening screen](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Designing-the-opening-screen)

[Choosing the minimal controls](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Choosing-the-minimal-controls)

[Building the Streamlit app](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Building-the-Streamlit-app)

[Handling edge-case uploads](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Handling-edge-case-uploads)

[Planning a timed demo](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Planning-a-timed-demo)

[Handling live-service failures](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Handling-live-service-failures)

[Practice: The stock trial](https://www.educative.io/courses/forward-deployed-engineer/building-a-demonstrable-interface#Practice-The-stock-trial)