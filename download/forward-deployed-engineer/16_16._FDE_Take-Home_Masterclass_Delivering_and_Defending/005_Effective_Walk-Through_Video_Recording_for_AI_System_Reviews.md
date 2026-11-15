# Effective_Walk-Through_Video_Recording_for_AI_System_Reviews

Source: https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Recording the Walk-Through Video

Plan a walk-through that supports each spoken claim with clearly visible on-screen evidence. Demonstrate an actual application run, show a relevant failure and how the application handles it, and explain a significant implementation decision within five minutes. Avoid exposing credentials, personal data, or other sensitive information so reviewers can verify the functionality and limitations demonstrated in the recording.

We'll cover the following...

- [Showing verifiable evidence](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Showing-verifiable-evidence)
- [Planning the 3:30 recording](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Planning-the-330-recording)
- [Narrating the successful run?](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Narrating-the-successful-run)
- [Showing the failure case](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Showing-the-failure-case)
- [Readable, audible, and safe](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Readable-audible-and-safe)
- [Handling failures and edits](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Handling-failures-and-edits)
- [Auditing the final recording](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Auditing-the-final-recording)

A 45-second recording shows three source files while the narrator claims the tool handles ticket priorities and errors. The recording ends without executing the tool. The viewer can inspect the source code but cannot verify priority classification or error handling.

Support each significant claim with readable on-screen evidence and explain what the demonstrated behavior means for the user. When a demo video is required, prioritize an end-to-end workflow demonstration over a detailed walk-through of every source file.

A coordinator needs a list of urgent ticket IDs and a separate list of tickets with unresolved priority classifications. The local queue reviewer identifies urgent tickets and flags those requiring priority clarification. It does not assign tickets or mark them as resolved.

## Showing verifiable evidence[#](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Showing-verifiable-evidence)

Ensure the recording provides verifiable evidence of the required behavior. Show readable input data, execute the tool, inspect the resulting classifications, demonstrate input rejection, and explain why tickets with unresolved priorities remain visible.

Review the following hypothetical 3-minute, 30-second recording:

- **0:00–1:20:** Scroll through the repository without executing the application.
- **1:20–2:30:** Show function descriptions at a zoom level that makes the text unreadable.
- **2:30–3:00:** Display a previously captured output screenshot while claiming that the live system works.
- **3:00–3:30:** Show a missing-column error but incorrectly describe it as a successful result with no urgent tickets.

Technical Quiz

1.

**(Select all that apply.)** Which claims does the above recording scenario verify, which remain unsupported, and what additional footage is needed to demonstrate the required behavior? Multi-select

A.

Keep the screenshot and explain that its successful output proves the live system is reliable.

B.

Replace the old screenshot with results clearly produced by the command shown, and only claim what that run shows.

C.

Show the missing priority column, the failed run and its exit status. Explain that the input was rejected, not classified as having no urgent tickets.

D.

Replace the repository scrolling with readable sample input and footage of the command actually running.

E.

Keep the current footage but add smooth transitions so the viewer can follow along without seeing a command run.

F.

Make the text bigger, and replace the unreadable function tour with workflow evidence and narration that matches what’s on screen.

---

1 / 1

A missing required column prevents the application from processing the input. Reporting this failure as an empty urgent queue could cause the coordinator to miss tickets requiring attention.

Review the assignment requirements before planning the recording. Check whether a recording is required, along with its duration, format, submission instructions, access restrictions, and AI-assistance permissions. Publicly available examples do not establish requirements for a specific employer.

For this exercise, plan a 3-minute, 30-second walkthrough unless the assignment specifies a different duration. This is an instructional target, not an employer requirement.

## Planning the 3:30 recording[#](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Planning-the-330-recording)

Use a claim–screen–narration plan: For each spoken claim, identify the exact visible evidence that supports it. Arrange those observations in workflow order rather than repository order.

Use the following recording plan. Screen directions specify footage to capture, not behavior already verified.

**1. 0:00–0:20: Establish the task**

- **Screen:** Show the terminal and a brief task description. Close unrelated windows.
- **Narration:** “The coordinator needs urgent ticket IDs and a clarification list. This is a local CSV review using synthetic data; it makes no ticket changes.”
- **Evidence boundary:** Establishes the intended workflow and local execution context without claiming customer adoption or measured impact.

**2. 0:20–0:45: Show the input and rule**

- **Screen:** Display all four rows of `queue_sample.csv`, including the header.
- **Narration:** “Tickets marked urgent are classified for escalation, while those marked normal require no escalation. Flag unrecognized or blank priorities for review. Compare priority values without regard to letter case or surrounding whitespace.”
- **Evidence boundary:** The input file establishes the test values. The execution must demonstrate how each value is classified.

**3. 0:45–1:35: Execute and inspect**

- **Screen:** Execute `python queue_review.py queue_sample.csv`. Keep the command, input filename, ticket IDs, and classification counts visible.
- **Narration:** After verifying the results, explain: “For these four synthetic records, Q401 and Q403 are urgent. Q402 needs no escalation. Q404 needs clarification because its priority is blank. These classifications are recommendations. The tool does not assign or modify tickets.”
- **Evidence boundary:** Verifies the demonstrated behavior for the four supplied records, not other inputs or production conditions.

**4. 1:35–2:10: Reject invalid input**

- **Screen:** Display the invalid CSV, execute the command, and show the resulting error message and exit code.
- **Narration:** “This file has no priority column. Validation rejects the file with exit code `2` and produces no classifications for the failed run. The coordinator must correct the input before reviewing it.”
- **Evidence boundary:** Verifies missing-column validation only, not comprehensive error handling.

**5. 2:10–2:55: Explain the consequential decision**

- **Screen:** Return to the valid input and its verified Q404 review result. Keep the source and result clearly associated.
- **Narration:** “Q404 is a valid identified record with an unclear priority. Excluding it would reduce the number of reported records but conceal an unresolved priority. Retaining Q404 in the review list keeps the unresolved ticket visible and requires the coordinator to clarify its priority manually.”
- **Evidence boundary:** Demonstrates the classification decision and required follow-up but does not measure clarification effort in a live queue.

**6. 2:55–3:30: Close with verification and boundaries**

- **Screen:** Display a concise setup and verification note with the commands demonstrated.
- **Narration:** “These runs verify the supplied synthetic CSV cases. The tool does not use an API or model, persist changes, or assign tickets. The setup and verification instructions document how to reproduce these checks.”
- **Evidence boundary:** No live integration, production reliability, customer adoption, or measured business impact has been demonstrated.

If the assignment requires a shorter recording, cut optional code explanations and repetition before removing evidence of required behavior.

## Narrating the successful run?[#](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Narrating-the-successful-run)

Create a new folder named `queue-walkthrough` and save the four supplied files there. Use an available Python 3 interpreter: Check `python --version` on Windows, or `python3 --version` on macOS and Linux. The supporting program uses only the standard library; no package installation is needed. If your interpreter command is `python3` or `py`, use that consistently in place of `python`.

The supplied input is:

- **Q401:** `urgent`
- **Q402:** `normal`
- **Q403:** `urgent`
- **Q404:** Blank priority

Before running it, predict the three groups. Then execute the supplied program and compare every ID and count with your prediction.

Files

queue\_review.py

queue\_sample.csv

queue\_missing\_priority.csv

queue\_trial.csv

python310

```
import csv

import sys

def review(path):

groups = {'urgent': [], 'no escalation': [], 'review': []}

seen = set()

with open(path, encoding='utf-8-sig', newline='') as source:

reader = csv.DictReader(source, strict=True)

headers = reader.fieldnames or []

missing = [name for name in ('ticket_id', 'priority') if name not in headers]

if missing:

raise ValueError('missing required column(s): ' + ', '.join(missing))

if len(headers) != len(set(headers)):

raise ValueError('duplicate column names')

for number, row in enumerate(reader, start=1):

if None in row or any(value is None for value in row.values()):

raise ValueError(f'record {number}: values do not match header')

ticket_id = row['ticket_id'].strip()

if not ticket_id:

raise ValueError(f'record {number}: ticket_id must be nonblank')

if ticket_id in seen:

raise ValueError(f'record {number}: duplicate ticket_id {ticket_id}')

seen.add(ticket_id)

priority = row['priority'].strip().lower()

group = 'urgent' if priority == 'urgent' else 'no escalation' if priority == 'normal' else 'review'

groups[group].append(ticket_id)

return groups

def main():

if len(sys.argv) > 2:

print('Error: usage: python queue_review.py [INPUT.csv]', file=sys.stderr)

return 2

try:

groups = review(sys.argv[1] if len(sys.argv) == 2 else 'queue_sample.csv')

except (OSError, UnicodeError, csv.Error, ValueError) as error:

print(f'Error: {error}', file=sys.stderr)

return 2

for name, ids in groups.items():

print(f"{name} ({len(ids)}): {', '.join(ids) if ids else '(none)'}")

return 0

if __name__ == '__main__':

sys.exit(main())
```

⋯

Predict the three groups first, then run both sample files and check each exit status

The supporting code separates validation from printing. That ordering prevents an invalid later record from leaving an apparently successful partial result.

For `queue_review.py`:

- **Lines 1–2:** Import the standard-library CSV reader and system utilities; no third-party packages are needed.
- **Lines 5–7:** Define the review function, initialize all three output groups, and create a set for tracking identifiers. Initializing every group keeps empty groups visible too.
- **Lines 8–10:** Open the input with CSV-compatible newline handling and optional UTF-8 byte-order-mark support. Create a strict dictionary reader and obtain the headers.
- **Lines 11–13:** Check for both required columns and raise a specific error if either is missing. Missing structure must not become an empty classification result.
- **Lines 14–15:** Reject duplicate column names, avoiding ambiguous field interpretation.
- **Lines 16–18:** Number the records and reject rows whose values do not match the header shape. Record numbers help locate the problem.
- **Lines 19–24:** Strip identifier whitespace, reject blank or repeated identifiers, and track each accepted identifier. This keeps the recommendations tied to distinct records.
- **Lines 25–27:** Normalize priority whitespace and case, choose a group, and append the identifier. Unrecognized and blank priorities remain visible in review; appending preserves input order.
- **Line 28:** Return the accumulated groups only after the complete input has passed validation.
- **Lines 31–34:** Define the command-line entry function and require exactly one input path. Incorrect usage prints an error to standard error and returns status 2.
- **Lines 35–39:** Call the reviewer and catch file, decoding, CSV, and validation errors. Each produces a clear standard-error message and returns status 2.
- **Lines 40–42:** Print each group’s name, count, and identifiers, using `(none)` for an empty group. Return status 0 after successful printing.
- **Lines 45–46:** Run the entry function when this file is executed directly and pass its return value to the shell as the exit status.

The accompanying CSV files supply the recording cases:

- **Lines 1–5:** In `queue_sample.csv`, the required header and four records provide two urgent priorities, one normal priority, and one blank priority.
- **Lines 1–2:** In `queue_missing_priority.csv`, the header contains only `ticket_id`, followed by Q401. This isolates the missing-column failure.
- **Lines 1–6:** In `queue_trial.csv`, the required header and five fresh records provide the independent recording input, including uppercase `URGENT`, `later`, and a blank priority.

The expected successful transcript is:

Ace Editor

1

2

3

urgent (2): Q401, Q403

no escalation (1): Q402

review (1): Q404

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Results

Until you execute and inspect the command, this is an expected result. During recording, say “The output shows…” only after checking the visible result. Point to identifiers instead of relying on “It works.” Keep the input and output close enough in the sequence that the viewer can trace Q404 from blank priority to review.

## Showing the failure case[#](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Showing-the-failure-case)

Show `queue_missing_priority.csv`: Its only header is `ticket_id`, followed by Q401. Run:

Ace Editor

1

python queue\_review.py queue\_missing\_priority.csv

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The expected error is `Error: missing required column(s): priority`, with exit status `2` and no successful classifications for this invocation.

Immediately display the status, before another command overwrites it:

- **macOS/Linux shells:** `echo $?`
- **Windows PowerShell:** `echo $LASTEXITCODE`
- **Windows Command Prompt:** `echo %ERRORLEVEL%`

Keep this error separate from the earlier successful output. A clean terminal or a visible invocation boundary prevents an older result from looking like output from the failed command.

Now explain the distinction using the screen:

> “The missing column invalidates the file. Q404 has the required columns and a valid identifier, but its priority needs clarification. The review group keeps that unresolved work visible.”

This explains the decision through its consequence. A function-by-function tour would consume time without improving that evidence.

## Readable, audible, and safe[#](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Readable-audible-and-safe)

Before the full take, record and replay a ten-second sample containing your smallest text and spoken narration. Select only the necessary window, enable the intended microphone, enlarge terminal and editor text, and save the sample using your recorder’s normal export process.

Check the saved file at an ordinary playback size:

- Can you read the longest command and every relevant ID without enlarging the player?
- Are columns clipped or hidden by controls?
- Is narration intelligible, without missing audio or distortion?
- Does the cursor obscure the value being discussed?

Pause long enough for results to be read. A readable desktop and an active microphone indicator do not establish that the exported video is usable. No particular recorder, camera, paid editor, or hosting service is required.

Prevent sensitive information from entering the capture: Use synthetic data, disable notifications, close unrelated tabs, and avoid credential-bearing commands, logs, configuration files, and environment files. If a real credential is exposed, stop distribution, follow the applicable revocation or rotation process, and replace the recording. Cropping alone does not invalidate a credential.

## Handling failures and edits[#](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Handling-failures-and-edits)

If the successful demonstration produces an unexpected error, stop and diagnose outside the recording. Rerun the checks and make a fresh take as needed. Do not narrate the expected result over the error or silently substitute an older screenshot.

When the assignment permits edits, simple cuts can remove dead time. Disclose compressed waits when relevant; an accelerated wait cannot support a measured latency claim or imply uninterrupted successful execution. Label prerecorded footage, fixture-backed behavior, and live integrations accurately where they appear. A fixture-backed service demonstration must state its live limitation.

Unreadability, missing audio, and exposed secrets are reasons to repair or replace the artifact. Recording polish cannot compensate for missing or misleading execution evidence.

## Auditing the final recording[#](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Auditing-the-final-recording)

Make a fresh three-to-four-minute recording using `queue_trial.csv` and the missing-column sample. The trial contains Q501/normal, Q502/URGENT, Q503/later, Q504/blank, and Q505/urgent.

Expected valid results are urgent Q502/Q505, no escalation Q501, and review Q503/Q504: Counts **2/1/2**. The malformed file should produce the validation error, exit `2`, and no classifications for that invocation. Capture actual execution and inspect those outcomes.

Replay the complete exported recording. Review the draft audit guidance below for misleading claims, then prepare your own timestamped audit in a separate empty note. The guidance is not evidence about your footage.

Queue Walkthrough — Recording Audit

Your task

You are the queue reviewer's author, preparing an independent three-to-four-minute walkthrough for an authorized reviewer. The reviewer needs actual execution evidence, not a script. Retain the exported recording or submit it through the authorized assignment route, and replay it completely before writing your audit. The draft audit guidance below also needs review; its claims are not evidence about your footage.

Tap any claim to classify it, and click on References to verify authorities.

TOAuthorized assignment reviewerFROMQueue reviewer authorDATEOctober 19, 2026SUBJECTIndependent trial recording and timestamped replay audit

Background

Make a fresh three-to-four-minute recording using `queue_trial.csv` and `queue_missing_priority.csv`. Capture actual execution, export the take, and replay the entire exported file. Retain the actual recording or submit it through the authorized assignment route; a script alone is insufficient. This widget cannot upload or inspect footage.

Issue

Create your audit in a separate empty note, leaving observations blank until checked. Use these fields: **Recording status:**  ***(recorded / not yet recorded); **Retained file or authorized submission reference:***** ; **Export duration:** ***; **Project version and documented commands:***** . For each evidence entry, record an actual playback timestamp, what you observed, and **pass / repair needed / unverified**. If temporarily unable to record, use **not yet recorded**, explain the blocker, and leave recording capability unverified; plans and predictions are not observed evidence.

Analysis

Draft guidance: The lesson's `queue_sample.csv` successful transcript is the authority for checking the trial recording: urgent Q401/Q403, no escalation Q402, and review Q404. Those identifiers can be copied into the trial audit.

Draft guidance: An automatic recording-certification rule guarantees that a completed audit note proves intelligible audio, readable text, and recipient access, even without replaying or opening the exported recording.

Draft guidance: If the missing-column invocation produces exit 2, the coordinator can conclude there are no urgent tickets. Together with the successful trial, this proves reliable live queue operation.

Conclusion

Add these blank evidence entries to your note, each with **timestamp / observation / status**: **Customer task:** ***; **Readable trial input and header:***** ; **Trial invocation and checked IDs/counts:** ***; **Missing-column input, invocation, clear error, immediate exit status, and absence of classifications for that invocation:***** ; **Decision to keep Q503/Q504 visible and the manual-clarification consequence:** ***; **Local synthetic-data limitation:***** . State that recommendations neither assign nor resolve tickets and demonstrate no API, model, persistence, adoption, or measured business impact.

Recommendation

Finish with blank audit checks, each marked **pass / repair needed / unverified** and supported by replay observations or a repair action: **Complete exported-file replay and duration:** ***; **Commands, columns, IDs, and counts readable at ordinary playback size:***** ; **Narration intelligible throughout:** ***; **Recording matches submitted project version and documented commands:***** ; **Synthetic/local-only labeling accurate:** ***; **No sensitive material exposed:***** ; **Authorized submission route and recipient-equivalent access check when sharing:** *\_*. Record the access test used or why it was not feasible; do not infer access from a link's existence or make the recording public. Repair or rerecord failed text, audio, provenance, interpretation, or privacy checks, then replay the replacement and update the note. If a credential was exposed, stop distribution and follow applicable revocation or rotation procedures before replacing the recording.

Do you find this helpful?

Before sharing, confirm that the recording matches the submitted project version and documented commands. Check its duration and playback, then open the submitted file or link through an authorized recipient-equivalent access path where feasible. Preserve assessment privacy; do not make it public merely to simplify access.

If recording is temporarily unavailable, complete the plan and predictions, but leave recording capability marked unverified. The finished artifact is the actual take plus a successful replay audit, not the script alone.

Documenting Trade-Offs and Limitations

Presenting and Defending Your Decisions

Ask

[Showing verifiable evidence](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Showing-verifiable-evidence)

[Planning the 3:30 recording](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Planning-the-330-recording)

[Narrating the successful run?](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Narrating-the-successful-run)

[Showing the failure case](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Showing-the-failure-case)

[Readable, audible, and safe](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Readable-audible-and-safe)

[Handling failures and edits](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Handling-failures-and-edits)

[Auditing the final recording](https://www.educative.io/courses/forward-deployed-engineer/recording-the-walk-through-video#Auditing-the-final-recording)