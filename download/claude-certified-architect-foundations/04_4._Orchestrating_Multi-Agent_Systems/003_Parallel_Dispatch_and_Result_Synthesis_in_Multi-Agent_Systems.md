# Parallel_Dispatch_and_Result_Synthesis_in_Multi-Agent_Systems

Source: https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Parallel Work and Result Synthesis

Explore how to dispatch multiple AI specialists concurrently and accurately synthesize their varied results into a coherent output. Understand the critical distinction between access failures and empty results, validate the completeness of specialist responses, and build a coordinator synthesis step for multi-agent systems. This lesson equips you to manage parallel workflows while ensuring reliable, comprehensive reporting.

We'll cover the following...

- [Dispatching specialists in parallel](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Dispatching-specialists-in-parallel)
- [The critical distinction: Access failure vs. empty result](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#The-critical-distinction-Access-failure-vs-empty-result)
- [Collecting and validating results](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Collecting-and-validating-results)
- [The synthesis step](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#The-synthesis-step)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Complete-code)
- [Exercise: Trace the synthesis](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Exercise-Trace-the-synthesis)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Whats-next)

In the previous lesson, we designed the coordinator-specialist split and the handoff packet. This lesson covers the runtime: dispatching specialists simultaneously, handling the full range of outcomes (success, partial result, access failure, empty result), and building the synthesis step that turns multiple structured results into a single coherent output. By the end of this lesson, we will be able to:

- Dispatch multiple specialists in parallel and collect all results before synthesis
- Distinguish access failures from empty results and handle each correctly
- Merge specialist results into a synthesis payload
- Build a coordinator synthesis step that is complete only when all expected fields are accounted for

## Dispatching specialists in parallel[#](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Dispatching-specialists-in-parallel)

When specialist subtasks are independent, the coordinator dispatches all of them before waiting for any results. This is the primary performance benefit of a multi-agent architecture: total wait time equals the slowest specialist, not the sum of all specialists. In Python, this pattern uses `concurrent.futures`:

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

from concurrent.futures import ThreadPoolExecutor, as\_completed

def run\_specialist(system: str, prompt: str) -> dict:

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=1024,

system=system,

messages=[{"role": "user", "content": prompt}]

)

for block in response.content:

if block.type == "text":

return json.loads(block.text)

return {"error": "no\_text\_block", "data\_gaps": ["specialist returned no content"]}

def dispatch\_all\_specialists(company: str, fiscal\_year: int) -> dict:

handoffs = {

"financial": build\_financial\_handoff(company, fiscal\_year),

"legal": build\_legal\_handoff(company),

"news": build\_news\_handoff(company, days=90),

}

results = {}

with ThreadPoolExecutor(max\_workers=3) as executor:

futures = {

executor.submit(

run\_specialist,

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Parallel specialist dispatch using a thread pool. All three specialists start simultaneously. Results and exceptions are both captured into the results dict — the coordinator sees every outcome, including failures.

- **Lines 3–13:** `run_specialist` runs one specialist. It calls the API with the specialist’s system prompt and handoff-packet prompt, parses the JSON result, and returns the dict. If the response contains no text block, which is unusual but possible, it returns a structured error dict with a `data_gaps` entry.
- **Lines 16–20:** `dispatch_all_specialists` builds all three handoff packets. Each is keyed by specialist name.
- **Lines 22–23:** The `ThreadPoolExecutor` with `max_workers=3` allows all three specialists to run concurrently. The three API calls are in flight at the same time.
- **Lines 24–29:** We submit one future per specialist. The `futures` dict maps each future to its specialist name, so we can identify which result belongs to which specialist as it completes.
- **Lines 30–38:** `as_completed(futures)` yields futures as they finish, so the fastest specialist’s result arrives first. For each completed future, we try to get its result. If the specialist function itself raised an exception (network error, JSON parse failure), we catch it and store a structured error dict rather than letting it propagate.
- **Lines 33–37:** The exception handler stores the same shape as a normal specialist result: a dict with `error`, `message`, and `data_gaps` keys. The coordinator can process all results uniformly without special-casing failures.

## The critical distinction: Access failure vs. empty result[#](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#The-critical-distinction-Access-failure-vs-empty-result)

The most common error in multi-agent result handling is returning an empty result when data retrieval failed. The coordinator reads `[]` or `{}` and concludes that the specialist found nothing, when in fact the specialist could not reach the data source at all. This distinction is one of the most tested concepts on the exam. Here is what each outcome looks like and what the coordinator should conclude from each:

|  |  |  |
| --- | --- | --- |
| **What Happened** | **Correct Return** | **Coordinator Conclusion** |
| Looked up records, found none | `{"results": [], "data_gaps": []}` | Source is accessible; no records exist for this company |
| API returned a 403 error | `{"error": "access_failure", "data_gaps": ["court records: 403 Forbidden"]}` | Could not check; existence of records is unknown |
| API timed out | `{"error": "timeout", "data_gaps": ["court records, connection timed out"]}` | Could not check; existence of records is unknown |
| Found three records | `{"results": [...], "data_gaps": []}` | Source is accessible; three records found |

The difference matters for the final report. “No court records found” is a clear finding that tells the client something positive about the company. “Could not check court records” is an unresolved gap that must be disclosed. Here is what a legal specialist’s structured access failure looks like:

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

# Access failure result — correct structure

legal\_access\_failure = {

"corporate\_registration": {

"status": "found",

"details": "Registered in Delaware, active since 2019"

},

"court\_records": {

"status": "access\_failure",

"reason": "API returned 403 Forbidden — subscription required",

"data\_gaps": ["court records — access failure, subscription required"]

},

"sanctions\_check": {

"status": "found",

"matches": []

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A legal specialist result with a partial access failure. corporate\_registration and sanctions\_check succeeded; court\_records failed with a 403. Each section’s status field lets the coordinator process results without guessing what happened.

- **Lines 3–6:** `corporate_registration` succeeded. `status: "found"` tells the coordinator it can include this data in the report.
- **Lines 7–11:** `court_records` failed. `status: "access_failure"` is explicit. `reason` provides enough context for the coordinator to include in the report or for an engineer to diagnose. `data_gaps` carries the entry that the coordinator will surface in the final output.
- **Lines 12–15:** `sanctions_check` succeeded with no matches. `matches: []` means “checked and found nothing,” a clean negative result, not a failure. This is the correct way to represent an empty search result: the `status` is `"found"`, and the `matches` list is empty.

## Collecting and validating results[#](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Collecting-and-validating-results)

After all specialists complete, the coordinator validates the result set before synthesis. Validation checks two things: that every expected specialist returned a result and that any failures are categorized correctly.

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

EXPECTED\_SPECIALISTS = {"financial", "legal", "news"}

def validate\_results(results: dict) -> tuple[dict, list[str]]:

gaps = []

validated = {}

for name in EXPECTED\_SPECIALISTS:

if name not in results:

gaps.append(f"{name} specialist: no result received")

validated[name] = None

continue

result = results[name]

if "error" in result:

gaps.append(

f"{name} specialist: {result.get('message', 'unknown error')}"

)

validated[name] = result

return validated, gaps

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A validation function that checks every expected specialist returned something. Missing specialists and specialist-level errors are both captured in gaps for inclusion in the final report.

- **Line 1:** `EXPECTED_SPECIALISTS` is declared at module level, which provides a single source of truth for which specialists should always report. If a new specialist is added, add it here.
- **Lines 7–11:** If a specialist key is missing entirely from `results`, perhaps because the future was never submitted due to a configuration error, the gap is recorded, and `validated[name]` is set to `None`. The synthesis step will encounter `None` for this specialist and handle it.
- **Lines 13–17:** If the result dict contains an `"error"` key, the specialist raised an exception or returned a failure. The gap is recorded from the `"message"` field. The result is still stored in `validated`; the synthesis step reads the `data_gaps` field from it.

## The synthesis step[#](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#The-synthesis-step)

Synthesis is the coordinator’s core job. It receives validated results from all specialists, merges their findings into a coherent structure, and ensures that every gap is surfaced rather than silently omitted.

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

def synthesize\_results(validated: dict, report\_gaps: list[str]) -> dict:

merged\_findings = {}

aggregated\_gaps = list(report\_gaps)

conflict\_flags = []

for name, result in validated.items():

if result is None:

aggregated\_gaps.append(f"{name}: no data received")

continue

# Collect confirmed findings

for key, value in result.items():

if key == "data\_gaps":

aggregated\_gaps.extend(value)

elif key in ("error", "message"):

pass # already captured in report\_gaps

else:

if key in merged\_findings:

conflict\_flags.append(

f"Conflicting values for '{key}': "

f"{merged\_findings[key]} vs {value} (from {name})"

)

else:

merged\_findings[key] = value

return {

"findings": merged\_findings,

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The synthesis function. It merges confirmed findings across all specialists, collects all data gaps, and flags conflicts for resolution. The is\_complete field tells the coordinator whether the report can be finalized.

- **Lines 2–4:** We initialize three accumulators. `merged_findings` collects confirmed data. `aggregated_gaps` starts with any gaps from the validation step. `conflict_flags` collects fields where two specialists returned different values.
- **Lines 6–8:** A `None` result means the specialist was expected but never returned anything. The gap is recorded.
- **Lines 11–13:** Each result's `data_gaps` list is extended into `aggregated_gaps`. The synthesis step does not discard gaps; it collects them all.
- **Lines 14–15:** We skip the `error` and `message` keys; those are metadata fields, not findings to merge.
- **Lines 16–21:** If a key already exists in `merged_findings`, we have a conflict: two specialists returned different values for the same field. The conflict is recorded with enough context (both values and which specialist provided each) for the provenance-based resolver from Lesson 4.2 to handle it.
- **Lines 23–28:** The final structure includes all four categories. `is_complete` is `True` only when there are no gaps and no conflicts, which indicates a clean synthesis. If `is_complete` is `False`, the coordinator knows the report needs a disclosed gaps section before it can be finalized.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Complete-code)

We wire together the parallel dispatch pattern, the access-failure vs. empty-result distinction, validation, and synthesis from this lesson into one executable file. The script dispatches three real specialist API calls simultaneously using a `ThreadPoolExecutor`, then passes all results through `validate_results` and `synthesize_results` to produce a complete report structure.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python

```
import json

import re

from concurrent.futures import ThreadPoolExecutor, as_completed

from dataclasses import dataclass, field

import anthropic

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = anthropic.Anthropic(api_key=anthropic_api_key)

def _parse_json(text: str) -> dict:

text = text.strip()

m = re.search(r'```(?:json)?\s*\n?([\s\S]+?)\n?\s*```', text)

if m:

text = m.group(1).strip()

start, end = text.find('{'), text.rfind('}') + 1

if start != -1 and end > start:

text = text[start:end]

return json.loads(text)

@dataclass

class HandoffPacket:

context: str

task:    str

def build_financial_handoff(company: str, fiscal_year: int) -> HandoffPacket:

return HandoffPacket(

context=f"Due diligence for {company}, FY{fiscal_year}",

task=(

f"Summarize the financial profile of {company} for FY{fiscal_year} based on "

"publicly available information. Return a JSON object with these keys: "

"revenue_estimate (string or null), growth_signal ('positive'/'neutral'/'negative'), "

"risk_flags (list of strings), data_gaps (list of strings), sources (list of strings). "

"Return only the JSON object."

),

)

def build_legal_handoff(company: str) -> HandoffPacket:

return HandoffPacket(

context=f"Legal compliance review for {company}",

task=(

f"Assess the regulatory and legal standing of {company} based on publicly available "

"information. Return a JSON object with these keys: "

"compliance_signal ('clean'/'caution'/'unknown'), notes (list of strings), "

"data_gaps (list of strings), sources (list of strings). "

"Do not invent specific case numbers. Return only the JSON object."

),

)

def build_news_handoff(company: str, days: int = 90) -> HandoffPacket:

return HandoffPacket(

context=f"News sentiment for {company}, last {days} days",

task=(

f"Summarize public news sentiment for {company} over the past {days} days. "

"Return a JSON object with these keys: "

"sentiment ('positive'/'neutral'/'negative'), highlights (list of up to 3 strings), "

"data_gaps (list of strings), sources (list of strings). "

"Return only the JSON object."

),

)

def packet_to_prompt(packet: HandoffPacket) -> str:

return f"Context: {packet.context}\n\nTask: {packet.task}"

SPECIALIST_SYSTEMS = {

"financial": "You are a financial due diligence specialist. Return structured JSON only.",

"legal":     "You are a legal compliance specialist. Return structured JSON only.",

"news":      "You are a news and sentiment analyst. Return structured JSON only.",

}

def run_specialist(system: str, prompt: str) -> dict:

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=1024,

system=system,

messages=[{"role": "user", "content": prompt}]

)

for block in response.content:

if block.type == "text":

return _parse_json(block.text)

return {"error": "no_text_block", "data_gaps": ["specialist returned no content"]}

def dispatch_all_specialists(company: str, fiscal_year: int) -> dict:

handoffs = {

"financial": build_financial_handoff(company, fiscal_year),

"legal":     build_legal_handoff(company),

"news":      build_news_handoff(company, days=90),

}

results = {}

with ThreadPoolExecutor(max_workers=3) as executor:

futures = {

executor.submit(

run_specialist,

SPECIALIST_SYSTEMS[name],

packet_to_prompt(packet)

): name

for name, packet in handoffs.items()

}

for future in as_completed(futures):

name = futures[future]

try:

results[name] = future.result()

except Exception as exc:

results[name] = {

"error":     "specialist_exception",

"message":   str(exc),

"data_gaps": [f"All {name} data unavailable, specialist raised an exception"]

}

return results

EXPECTED_SPECIALISTS = {"financial", "legal", "news"}

def validate_results(results: dict) -> tuple[dict, list[str]]:

gaps      = []

validated = {}

for name in EXPECTED_SPECIALISTS:

if name not in results:

gaps.append(f"{name} specialist: no result received")

validated[name] = None

continue

result = results[name]

if "error" in result:

gaps.append(f"{name} specialist: {result.get('message', 'unknown error')}")

validated[name] = result

return validated, gaps

def synthesize_results(validated: dict, report_gaps: list[str]) -> dict:

merged_findings = {}

aggregated_gaps = list(report_gaps)

conflict_flags  = []

for name, result in validated.items():

if result is None:

aggregated_gaps.append(f"{name}: no data received")

continue

for key, value in result.items():

if key == "data_gaps":

aggregated_gaps.extend(value)

elif key in ("error", "message"):

pass

else:

if key in merged_findings:

conflict_flags.append(

f"Conflicting values for '{key}': "

f"{merged_findings[key]!r} vs {value!r} (from {name})"

)

else:

merged_findings[key] = value

return {

"findings":    merged_findings,

"gaps":        aggregated_gaps,

"conflicts":   conflict_flags,

"is_complete": len(aggregated_gaps) == 0 and len(conflict_flags) == 0,

}

if __name__ == "__main__":

COMPANY     = "Stripe"

FISCAL_YEAR = 2025

print(f"=== Parallel specialist dispatch: {COMPANY} FY{FISCAL_YEAR} ===\n")

print("Dispatching all three specialists simultaneously...\n")

raw = dispatch_all_specialists(COMPANY, FISCAL_YEAR)

print("All specialists returned:\n")

for name, result in raw.items():

status = "error" if "error" in result else "ok"

keys   = [k for k in result if k not in ("data_gaps", "sources", "error", "message")]

print(f"  {name:<12} [{status}]  finding keys: {keys}")

print("\n=== Validation ===\n")

validated, gaps = validate_results(raw)

print(f"Validation gaps : {gaps or 'none'}")

print("\n=== Synthesis ===\n")

report = synthesize_results(validated, gaps)

print("Merged findings:")

for key, value in report["findings"].items():

display = str(value)

if len(display) > 80:

display = display[:80] + "..."

print(f"  {key:<22} : {display}")

print(f"\nAggregated gaps : {report['gaps'] or 'none'}")

print(f"Conflicts       : {report['conflicts'] or 'none'}")

print(f"is_complete     : {report['is_complete']}")
```

⋯

Parallel specialist dispatch with validation and synthesis. All three API calls are in flight simultaneously. validate\_results checks for missing specialists and errors; synthesize\_results merges confirmed findings and collects all data gaps into the final report structure.

Running the script produces output like this:

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

=== Parallel specialist dispatch: Stripe FY2025 ===

Dispatching all three specialists simultaneously...

All specialists returned:

financial [ok] finding keys: ['revenue\_estimate', 'growth\_signal', 'risk\_flags']

legal [ok] finding keys: ['compliance\_signal', 'notes']

news [ok] finding keys: ['sentiment', 'highlights']

=== Validation ===

Validation gaps : none

=== Synthesis ===

Merged findings:

revenue\_estimate : $95B+ (estimated, private company)

growth\_signal : positive

risk\_flags : ['regulatory scrutiny in EU', 'payment processing competition']

compliance\_signal : clean

notes : ['No major litigation on record', 'PCI DSS compliant']

sentiment : positive

highlights : ['Strong developer adoption growth', 'International expansion news']

Aggregated gaps : none

Conflicts : none

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

`is_complete` is `True` when both `aggregated_gaps` and `conflicts` are empty. If any specialist returned an access failure, its `data_gaps` entries would appear here, and `is_complete` would be `False`. The coordinator reads this flag to decide whether to generate a clean report or a report with a disclosed gaps section before finalizing.

## Exercise: Trace the synthesis[#](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Exercise-Trace-the-synthesis)

Read the specialist results and answer the questions below. The coordinator ran three specialists in parallel. Their results are:

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

financial\_result = {

"revenue\_2025": "$94M",

"growth\_rate": "18% YoY",

"risk\_flags": ["high customer concentration — top 3 clients = 61% of revenue"],

"data\_gaps": [],

"sources": ["SEC EDGAR (verified)"]

}

legal\_result = {

"sanctions\_match": False,

"court\_records": {

"status": "access\_failure",

"reason": "403 Forbidden — subscription required"

},

"data\_gaps": ["court records — access failure, subscription required"],

"sources": ["OFAC API (verified)", "court records API (failed)"]

}

news\_result = {

"revenue\_2025": "$96M",

"sentiment": "neutral",

"data\_gaps": [],

"sources": ["earnings call transcript (extracted)"]

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Technical Quiz

1.

The financial result and the news result both contain a `revenue_2025` field with different values: `$94M` (verified) and `$96M` (extracted). How should the synthesis step handle this?

A.

Average the two values and report `$95M`.

B.

Use the most recent value, the earnings call transcript may be more current than the SEC filing.

C.

Flag the conflict and trust the verified SEC figure: report `$94M`, noting the call cited `$96M`.

D.

Discard both values, conflicting revenue figures make the financial analysis unreliable.

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Whats-next)

In the next lesson, we consolidate this chapter in the assessment quiz, which tests coordinator/specialist design, context isolation, structured failure reporting, and result synthesis across scenario-based questions.

Context Handoff Design

Multi-Agent Orchestration Quiz

Ask

[Dispatching specialists in parallel](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Dispatching-specialists-in-parallel)

[The critical distinction: Access failure vs. empty result](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#The-critical-distinction-Access-failure-vs-empty-result)

[Collecting and validating results](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Collecting-and-validating-results)

[The synthesis step](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#The-synthesis-step)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Complete-code)

[Exercise: Trace the synthesis](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Exercise-Trace-the-synthesis)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/parallel-work-and-result-synthesis#Whats-next)