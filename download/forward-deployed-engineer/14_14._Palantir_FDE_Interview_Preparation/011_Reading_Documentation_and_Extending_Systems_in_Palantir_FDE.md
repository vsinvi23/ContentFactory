# Reading_Documentation_and_Extending_Systems_in_Palantir_FDE

Source: https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The Learning Round: Reading Docs and Extending Systems

Understand unfamiliar libraries by tracing calls, reviewing relevant documentation, and testing interpretations through small experiments. Identify documented guarantees, ambiguous rules, and potential uncertainties before making changes. Preserve existing behavior by evaluating dependencies, accounting for concurrent updates, and applying appropriate synchronization. Work through practical exercises to reinforce documentation analysis, validate assumptions, and handle uncertain system behavior safely.

We'll cover the following...

- [What a guarantee does and doesn’t say](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#What-a-guarantee-does-and-doesnt-say)
- [A learning loop for unfamiliar systems](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#A-learning-loop-for-unfamiliar-systems)
- [What the interview evidence supports](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#What-the-interview-evidence-supports)
- [Probing an ambiguous rule](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Probing-an-ambiguous-rule)
- [Extending the batch library](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Extending-the-batch-library)
  - [The tempting extension](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#The-tempting-extension)
  - [The simpler extension](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#The-simpler-extension)
  - [Practice: extend it yourself](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Practice-extend-it-yourself)
  - [Explain it in 60 seconds](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Explain-it-in-60-seconds)
  - [Reported learning-round questions](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Reported-learning-round-questions)

An unfamiliar library says: “Successful results are returned in input order; execution and completion order are unspecified.”

That sentence lets you predict the returned list, but not much else. Working from documentation means finding exactly where a guarantee stops, then making a small change you can defend even when tasks finish in an unexpected order.

## What a guarantee does and doesn’t say[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#What-a-guarantee-does-and-doesnt-say)

You submit J1, J2, and J3 to the library above, and all succeed. Using only that sentence, decide which prediction is warranted.

Commit an order prediction

1.

The practice-library documentation says: “Successful results are returned in input order; execution and completion order are unspecified.”

You submit J1, J2 and J3, and all succeed. Using only this excerpt, which prediction is warranted?

A.

The tasks begin executing in J1, J2, J3 order.

B.

The returned results appear in J1, J2, J3 order.

C.

Any external calls made by the tasks occur in J1, J2, J3 order.

D.

The tasks finish in J1, J2, J3 order.

---

1 / 1

A **contract** is a documented promise about inputs, outputs, or behavior. “Results are returned in input order” fixes where each result appears in the list. It says nothing about which task starts first, which external call happens first, or which task finishes first.

## A learning loop for unfamiliar systems[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#A-learning-loop-for-unfamiliar-systems)

1. Restate the change requested and the behavior that must stay the same.
2. Trace one existing call through the entry point.
3. Read only the signatures, examples, concurrency notes, and failure rules on that path.
4. Write down the contracts the change relies on.
5. Test the riskiest unresolved interpretation with a small experiment.
6. Make the smallest extension, then verify new and preserved behavior.

Keep working notes in three columns:

|  |  |  |
| --- | --- | --- |
| **Documented Contract** | **Unresolved Question** | **Smallest Useful Probe** |
| Results return in input order | Is the service safe for concurrent reads? | Ask, or find the service’s contract |
| Waits for all tasks before returning | Does a failed batch roll anything back? | Docs say no rollback, so assume none |
| Execution order unspecified | None for this change | Force an unusual completion order in a test |

A successful concurrent run can’t establish thread safety. Don’t read every page up front. Read enough to choose the next safe action, then go back to the docs when a specific question comes up.

## What the interview evidence supports[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#What-the-interview-evidence-supports)

Public candidate reports describe tasks where a candidate gets a database schema and documentation and implements functions during the interview, and others mention learning SQL or unfamiliar systems on the spot. These are single reports through a secondary guide, not guaranteed questions. I found no sourced report of a multithreaded-library task, so the batch library below is an invented practice example, not Palantir software.

Your recruiter’s instructions set the real format, language, and permitted resources. A reported experience doesn’t override them.

## Probing an ambiguous rule[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Probing-an-ambiguous-rule)

Suppose the docs for an unfamiliar query language say: “`KEEP value > 5` retains rows where the predicate is true. Comparing a missing value gives *unknown*, and unknown rows are dropped.” You must find each device’s latest reading, then keep only devices whose latest value exceeds 5.

Two readings of the pipeline compete:

- **Latest first, then filter:** Device C’s latest reading has a missing value, so C is dropped.
- **Filter first, then latest:** The missing row is removed early, so an older C reading of 8 wrongly survives.

A good probe is a device whose latest value is missing and whose older value is above 5. A device with one clean reading couldn’t tell the two apart. The docs’ rule about unknown values, not familiarity with SQL, decides the answer: C is excluded. Familiar PostgreSQL behavior is no evidence about a new language.

## Extending the batch library[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Extending-the-batch-library)

**Task:** The existing `enrich` function returns enriched records in input order. Add totals by region without changing that list.

**Contract for this exercise:**

- `parallel_map(fn, items, workers=3)` runs `fn` once per input in worker threads, with no automatic retries.
- Execution and completion order are unspecified, and results come back in input order.
- It waits for every task before returning, or raises `BatchError` if any worker fails. It has no rollback.
- Clarified: the service supports concurrent reads, each input contributes once, and a failed batch must not return a partial summary.

### The tempting extension[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#The-tempting-extension)

Have each worker add its amount to a shared `totals` dictionary. The update is three steps, read, add, write, and a legal interleaving loses one:

1. J1 reads `north = 0`. J3 reads `north = 0`.
2. J1 stores 7. J3 stores 11.

The result is 11, not 7 + 11 = 18. Python’s GIL isn’t a documented guarantee for that sequence. A lock around only the final assignment keeps the stale reads. To make shared updates safe, the lock must cover the whole read-add-write.

### The simpler extension[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#The-simpler-extension)

Workers return immutable records, and the caller builds the totals *after* `parallel_map` returns. The library’s documented “waits for every task” boundary is the synchronization, and no shared mutable state exists to race on.

C++

```
import threading

from concurrent.futures import ThreadPoolExecutor, wait

from dataclasses import dataclass

class BatchError(Exception):

pass

def parallel_map(fn, items, workers=3):

"""Results come back in input order; completion order is unspecified."""

with ThreadPoolExecutor(max_workers=workers) as pool:

futures = [pool.submit(fn, item) for item in items]

wait(futures)

results, errors = [], []

for future in futures:

try:

results.append(future.result())

except Exception as error:

errors.append(error)

if errors:

raise BatchError(f"{len(errors)} worker(s) failed")

return results

@dataclass(frozen=True)

class Job:

job_id: str

region: str

@dataclass(frozen=True)

class Enriched:

job_id: str

region: str

amount: int

def enrich(jobs, read_amount):

def worker(job):

return Enriched(job.job_id, job.region, read_amount(job.job_id))

return parallel_map(worker, jobs, workers=3)

def enrich_with_totals(jobs, read_amount):

records = enrich(jobs, read_amount)

totals = {}

for record in records:

totals[record.region] = totals.get(record.region, 0) + record.amount

return records, totals

AMOUNTS = {"J1": 7, "J2": 5, "J3": 11, "J4": 3}

JOBS = [Job("J1", "north"), Job("J2", "south"), Job("J3", "north"), Job("J4", "south")]

finished = []

lock = threading.Lock()

j3_done = threading.Event()

def read_amount(job_id):

if job_id == "J1":

j3_done.wait(timeout=5)  # J1 cannot finish before J3

with lock:

finished.append(job_id)

if job_id == "J3":

j3_done.set()

return AMOUNTS[job_id]

def check(name, got, expected):

ok = got == expected

print("PASS" if ok else "FAIL", "-", name)

if not ok:

print("  got:", got)

print("  expected:", expected)

records, totals = enrich_with_totals(JOBS, read_amount)

check("records in input order", [r.job_id for r in records], ["J1", "J2", "J3", "J4"])

check("totals", totals, {"north": 18, "south": 8})

check("J3 finished before J1", finished.index("J3") < finished.index("J1"), True)

check("empty batch", enrich_with_totals([], read_amount), ([], {}))

def failing_read(job_id):

if job_id == "J2":

raise RuntimeError("service down")

return AMOUNTS[job_id]

try:

enrich_with_totals(JOBS, failing_read)

print("FAIL - failed batch returned a summary")

except BatchError as error:

print("PASS - failed batch raised:", error)
```

⋯

Library, extension and checks with forced completion order.

- **Lines 10–23:** This is the library. It waits for all futures, then reads them in submission order, which is why results come back in input order. It raises only after every task has finished.
- **Lines 39–42:** This is the original `enrich`, unchanged.
- **Lines 45–50:** This is the extension. `totals` is created and updated only on the caller’s thread, after `parallel_map` has returned. No worker touches it.
- **Lines 61–68:** J1 waits until J3 has finished, so J3 finishes before J1 even though J1 comes first in the input.
- **Lines 79–82:** The records stay in input order, the totals are correct, and the forced out-of-order completion really happened.
- **Lines 86–96:** If any worker fails, the whole batch raises. Catching the error and returning partial totals would label an incomplete batch as successful.

All five lines should print PASS. One run doesn’t prove correctness for every thread schedule. The ownership argument does the heavy lifting: the totals dictionary has a single owner.

**What this change does not claim:** read-only calls that already completed stay completed after a failure, which is acceptable here. A service that *writes* would need its own failure and recovery contract. Don’t claim retries, deduplication, or rollback that the docs don’t give you. Repeated jobs submitted as separate inputs contribute separately: submitting J1 twice gives `north = 14`.

### Practice: extend it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Practice-extend-it-yourself)

**Task:** Add a `summarize` function that returns `{region: (count, total)}`. Every record counts once, and the update happens on the caller’s thread, not inside workers.

Predict first: jobs `K1/east (4)`, `K2/east (6)` and `K3/west (2)` should give `east (2, 10)` and `west (1, 2)`. Submitting K1 twice should give `east (2, 8)`.

C++

```
from concurrent.futures import ThreadPoolExecutor, wait

def parallel_map(fn, items, workers=3):

with ThreadPoolExecutor(max_workers=workers) as pool:

futures = [pool.submit(fn, item) for item in items]

wait(futures)

return [f.result() for f in futures]  # input order; raises if any worker failed

AMOUNTS = {"K1": 4, "K2": 6, "K3": 2}

def read_amount(job_id):

return AMOUNTS[job_id]

def enrich(jobs):

# jobs are (job_id, region); returns (job_id, region, amount) in input order

return parallel_map(lambda job: (job[0], job[1], read_amount(job[0])), jobs)

def summarize(jobs):

records = enrich(jobs)

summary = {}

# TODO 1: loop over records here, on the caller's thread

# TODO 2: for each region keep (count, total); every record counts once

return summary
```

⋯

Add per-region counts on the caller thread.

### Explain it in 60 seconds[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Explain-it-in-60-seconds)

Be ready to name:

- **One documented rule:** Results return in input order, and the call waits for all tasks.
- **One uncertainty a probe resolved:** The completion order was forced, not assumed.
- **One thing your tests don’t prove:** Thread safety of the service beyond what was clarified, and behavior for services that write.

Add the location of the single owner: the totals dictionary lives on the caller thread, and the library’s return is the “all workers done” boundary.

### Reported learning-round questions[#](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Reported-learning-round-questions)

These prompt families appear in public candidate reports. Wording varies, and none is guaranteed.

1.

You’re given a schema and documentation. Implement a function.

Show Answer

1 / 5

When an unfamiliar system produces a wrong result instead of a missing feature, the job changes: isolate which contract or implementation step failed without rewriting everything. That is the re-engineering round, which comes next.

From Ideation to Execution: Users, Data Models, and APIs

The Re-Engineering Round: Debugging and Verifying Fixes

Ask

[What a guarantee does and doesn’t say](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#What-a-guarantee-does-and-doesnt-say)

[A learning loop for unfamiliar systems](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#A-learning-loop-for-unfamiliar-systems)

[What the interview evidence supports](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#What-the-interview-evidence-supports)

[Probing an ambiguous rule](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Probing-an-ambiguous-rule)

[Extending the batch library](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Extending-the-batch-library)

[The tempting extension](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#The-tempting-extension)

[The simpler extension](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#The-simpler-extension)

[Practice: extend it yourself](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Practice-extend-it-yourself)

[Explain it in 60 seconds](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Explain-it-in-60-seconds)

[Reported learning-round questions](https://www.educative.io/courses/forward-deployed-engineer/the-learning-round-reading-docs-and-extending-systems#Reported-learning-round-questions)