# Task-Specific_Quality_Metrics_for_Reliable_AI_Workflows

Source: https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Task-Specific Quality Metrics

Explore how to measure and interpret task-specific quality metrics in AI systems beyond aggregate accuracy. Learn to break down accuracy by document type and field, assess confidence calibration, and track retry and escalation rates. This lesson helps you identify realistic failure patterns and make targeted improvements to production AI pipelines.

We'll cover the following...

- [Why aggregate scores are insufficient](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Why-aggregate-scores-are-insufficient)
- [Stratifying by document type](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Stratifying-by-document-type)
- [Stratifying by field](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Stratifying-by-field)
- [Confidence calibration](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Confidence-calibration)
- [Workflow stage metrics](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Workflow-stage-metrics)
- [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Complete-code)
- [Connecting metrics to improvement decisions](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Connecting-metrics-to-improvement-decisions)
- [Exercise: Read the metrics](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Exercise-Read-the-metrics)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Whats-next)

An aggregate accuracy score answers the question “How often is the output correct overall?” It does not answer the questions that matter for a production system: which document types are failing, which fields are unreliable, whether high-confidence outputs are actually trustworthy, and at what stage of the pipeline failures are occurring. A system that is 92% accurate overall may be 65% accurate on handwritten invoices, 40% accurate on the `tax_id` field, and return inflated confidence scores that downstream systems trust incorrectly. This lesson covers how to stratify evaluation to make those failures visible. By the end of this lesson, we will be able to:

- Explain why aggregate accuracy scores mask the failure patterns that matter in production
- Stratify extraction accuracy by document type and by field
- Measure confidence calibration and identify when Claude’s stated confidence does not match actual accuracy
- Track workflow stage metrics: retry rate, second-pass success rate, and escalation rate

## Why aggregate scores are insufficient[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Why-aggregate-scores-are-insufficient)

An aggregate accuracy score averages across all documents, all fields, and all confidence levels. This average is dominated by the most common cases, which are usually the easiest ones. Hard documents and rare fields become statistical noise. Consider a pipeline that extracts five fields from three document types:

|  |  |  |
| --- | --- | --- |
| **Document Type** | **Share of Volume** | **Accuracy** |
| Standard digital invoices | 80% | 97% |
| Scanned paper invoices | 15% | 71% |
| Handwritten receipts | 5% | 44% |

The aggregate accuracy is `(0.80 × 0.97) + (0.15 × 0.71) + (0.05 × 0.44) = 0.776 + 0.107 + 0.022 = 90.5%`. A 90.5% headline number sounds good. The 44% accuracy on handwritten receipts is invisible inside it.

Stratifying by document type reveals that handwritten receipts need a different extraction approach: more examples in the system prompt, a different model, or human review by default. The aggregate number gives no signal about where to invest improvement effort.

## Stratifying by document type[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Stratifying-by-document-type)

Tracking accuracy per document type requires attaching a document type label to each extraction result and computing accuracy separately for each label. The label can come from a classifier that runs before extraction, from metadata in the document source, or from a post hoc human review pass.

A metrics collector that accumulates per-document-type results:

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

from dataclasses import dataclass, field

from collections import defaultdict

@dataclass

class FieldResult:

correct: int = 0

total: int = 0

@property

def accuracy(self) -> float:

return self.correct / self.total if self.total > 0 else 0.0

@dataclass

class MetricsCollector:

by\_doc\_type: dict = field(default\_factory=lambda: defaultdict(FieldResult))

by\_field: dict = field(default\_factory=lambda: defaultdict(FieldResult))

def record(

collector: MetricsCollector,

doc\_type: str,

field\_name: str,

extracted: str,

ground\_truth: str

) -> None:

is\_correct = extracted.strip().lower() == ground\_truth.strip().lower()

collector.by\_doc\_type[doc\_type].total += 1

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A metrics collector that accumulates results by document type and by field simultaneously. Each call to record increments the counters for the relevant document type and field. Accuracy is computed lazily from the accumulated counts.

- **Lines 4–9:** `FieldResult` holds raw counts rather than a running average. Storing counts allows the final accuracy to be computed once over the full data set rather than averaging averages, which would weight each document equally regardless of how many fields it contributed.
- **Lines 11–13:** `MetricsCollector` maintains two separate `defaultdict` structures, one keyed by document type and one keyed by field name. Both map to `FieldResult` instances that are created automatically on first access via `defaultdict`.
- **Lines 21–22:** Normalizing both strings to lowercase before comparison handles capitalization differences between extraction output and ground truth labels. For numeric fields, a tolerance-based comparison is more appropriate than exact string matching.
- **Lines 24–28:** Each call to `record` increments exactly two counters: the document-type counter and the field counter. This means the same extraction event contributes to both stratifications without double-counting documents.

## Stratifying by field[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Stratifying-by-field)

Field-level accuracy reveals which specific values in the output schema are causing failures. A pipeline may extract `invoice_date` correctly 98% of the time but `line_items` correctly only 60% of the time. Without field-level metrics, both failures are averaged together, and neither is visible.

Reading field-level results from the collector:

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

def print\_field\_report(collector: MetricsCollector) -> None:

print("Field-level accuracy:")

rows = sorted(

collector.by\_field.items(),

key=lambda kv: kv[1].accuracy

)

for field\_name, result in rows:

bar = "#" \* int(result.accuracy \* 20)

pct = f"{result.accuracy \* 100:.1f}%"

print(f" {field\_name:<20} {pct:>6} [{bar:<20}] n={result.total}")

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A report that sorts fields by accuracy ascending so the worst-performing fields appear first. The bar chart gives a quick visual signal without requiring a plotting library.

- **Lines 3–5:** Sorting by `accuracy` ascending puts the lowest-accuracy fields at the top of the report. In a long field list, this ensures the failure cases are visible without scrolling.
- **Lines 6–9:** The bar chart scales `accuracy` to a 20-character width. A field at 50% accuracy shows 10 `#` characters; one at 100% shows 20. The `n=` suffix shows the sample size, which distinguishes a low-accuracy field with 1,000 observations (a real problem) from one with three observations (too little data to conclude anything).

## Confidence calibration[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Confidence-calibration)

Claude’s output often includes a `confidence` field with values like `"high"`, `"medium"`, or `"low"`. Confidence calibration measures whether those labels are predictive: when Claude says `"high"`, does it actually achieve high accuracy? When it says `"low"`, does accuracy drop?

A well-calibrated system produces a monotonic relationship: `accuracy(high) > accuracy(medium) > accuracy(low)`. A poorly calibrated system produces one or more of:

- `accuracy(high)` is not meaningfully higher than `accuracy(medium)`, and the high/medium distinction carries no signal
- `accuracy(low)` is still high, and Claude underestimates its own reliability
- `accuracy(high)` is low, and Claude overestimates its own reliability, which is the dangerous case

Tracking calibration requires recording the confidence level alongside correctness:

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

@dataclass

class ConfidenceBucket:

correct: int = 0

total: int = 0

@property

def accuracy(self) -> float:

return self.correct / self.total if self.total > 0 else 0.0

@dataclass

class CalibrationTracker:

buckets: dict = field(

default\_factory=lambda: defaultdict(ConfidenceBucket)

)

def record\_confidence(

tracker: CalibrationTracker,

confidence: str,

is\_correct: bool

) -> None:

tracker.buckets[confidence].total += 1

tracker.buckets[confidence].correct += int(is\_correct)

def calibration\_report(tracker: CalibrationTracker) -> None:

print("Confidence calibration:")

for level in ["high", "medium", "low"]:

b = tracker.buckets.get(level)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A calibration tracker that groups results by stated confidence level. The report prints accuracy and sample size for each level. A well-calibrated system shows decreasing accuracy from high to medium to low.

- **Lines 1–13:** `CalibrationTracker` mirrors the structure of `MetricsCollector` but keys by confidence level rather than document type or field name. Keeping it separate allows calibration to be tracked independently of field-level accuracy.
- **Lines 15–21:** `record_confidence` takes the string confidence label from the extracted output and a boolean correctness flag derived from comparison with ground truth. The confidence label is used directly as the bucket key, so any value Claude produces (`"high"`, `"medium"`, `"low"`, or anything unexpected) creates its own bucket.
- **Lines 23–29:** Iterating over `["high", "medium", "low"]` in that order prints the report in the natural monotonic direction. A well-calibrated system shows the `high` accuracy bar tallest. If `medium` accuracy is higher than `high`, the confidence signal is miscalibrated, and downstream systems should not trust `"high"` outputs more than `"medium"` ones.

## Workflow stage metrics[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Workflow-stage-metrics)

Field accuracy and confidence calibration measure output quality. Workflow stage metrics measure pipeline health: how often does extraction succeed on the first attempt, how often does a retry fix a failure, and how often does the pipeline give up and escalate? The four key workflow stage metrics are:

|  |  |  |
| --- | --- | --- |
| **Metric** | **Formula** | **What It Reveals** |
| First-pass success rate | Successful extractions / total documents | Whether the base prompt and schema produce valid output most of the time |
| Retry rate | Documents that required at least one retry / total documents | How often the validator catches an error and sends feedback |
| Second-pass success rate | Successful retries / total retried documents | Whether retry feedback is specific enough to fix the problem |
| Escalation rate | Documents that failed all retries / total documents | How many documents need human review |

A healthy pipeline has a high first-pass rate, a low retry rate, a high second-pass rate, and a near-zero escalation rate. Anomalies in any one metric point to a specific part of the pipeline to investigate. Track these metrics in the retry loop:

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

@dataclass

class PipelineMetrics:

total: int = 0

first\_pass\_ok: int = 0

retried: int = 0

retry\_ok: int = 0

escalated: int = 0

@property

def first\_pass\_rate(self) -> float: return self.first\_pass\_ok / self.total if self.total else 0.0

@property

def retry\_rate(self) -> float: return self.retried / self.total if self.total else 0.0

@property

def second\_pass\_rate(self) -> float: return self.retry\_ok / self.retried if self.retried else 0.0

@property

def escalation\_rate(self) -> float: return self.escalated / self.total if self.total else 0.0

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A PipelineMetrics dataclass that tracks counts at each stage. The four rate properties are computed from the raw counts on demand, so only counts need to be incremented during processing.

- **Lines 2–6:** Five integer counters cover the full pipeline life cycle. `total` is the denominator for first-pass and escalation rates. `retried` is the denominator for the second-pass rate; it measures retry effectiveness independently of how often retries were needed.
- **Lines 8–15:** Each rate is a property rather than a stored value, which ensures that the rates are always computed from the current counts and never go stale. The `if self.total else 0.0` guards prevent `ZeroDivisionError` when metrics are read before any documents have been processed.

## Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Complete-code)

We drive all three metric collectors in this lesson with 200 simulated documents across three document types and four fields. No API key is required; `random.seed(42)` makes the simulation fully reproducible. The output shows how aggregate accuracy masks per-type and per-field failures, how miscalibrated confidence appears in the calibration table, and what anomalous pipeline-stage ratios indicate.

Python

```
import random

from dataclasses import dataclass, field

from collections import defaultdict

@dataclass

class FieldResult:

correct: int = 0

total:   int = 0

@property

def accuracy(self) -> float:

return self.correct / self.total if self.total > 0 else 0.0

@dataclass

class MetricsCollector:

by_doc_type: dict = field(default_factory=lambda: defaultdict(FieldResult))

by_field:    dict = field(default_factory=lambda: defaultdict(FieldResult))

def record(collector, doc_type, field_name, extracted, ground_truth):

is_correct = extracted.strip().lower() == ground_truth.strip().lower()

collector.by_doc_type[doc_type].total   += 1

collector.by_doc_type[doc_type].correct += int(is_correct)

collector.by_field[field_name].total   += 1

collector.by_field[field_name].correct += int(is_correct)

def print_doc_type_report(collector):

print("Document-type accuracy (sorted worst first):")

for doc_type, result in sorted(collector.by_doc_type.items(), key=lambda kv: kv[1].accuracy):

bar = "#" * int(result.accuracy * 20)

print(f"  {doc_type:<25} {result.accuracy*100:>5.1f}%  [{bar:<20}]  n={result.total}")

def print_field_report(collector):

print("Field-level accuracy (sorted worst first):")

for field_name, result in sorted(collector.by_field.items(), key=lambda kv: kv[1].accuracy):

bar = "#" * int(result.accuracy * 20)

print(f"  {field_name:<20} {result.accuracy*100:>5.1f}%  [{bar:<20}]  n={result.total}")

@dataclass

class ConfidenceBucket:

correct: int = 0

total:   int = 0

@property

def accuracy(self) -> float:

return self.correct / self.total if self.total > 0 else 0.0

@dataclass

class CalibrationTracker:

buckets: dict = field(default_factory=lambda: defaultdict(ConfidenceBucket))

def record_confidence(tracker, confidence, is_correct):

tracker.buckets[confidence].total   += 1

tracker.buckets[confidence].correct += int(is_correct)

def calibration_report(tracker):

print("Confidence calibration (well-calibrated: high > medium > low):")

for level in ["high", "medium", "low"]:

b = tracker.buckets.get(level)

if b and b.total > 0:

bar = "#" * int(b.accuracy * 20)

print(f"  {level:<8}  acc={b.accuracy*100:.1f}%  n={b.total}  [{bar:<20}]")

@dataclass

class PipelineMetrics:

total:         int = 0

first_pass_ok: int = 0

retried:       int = 0

retry_ok:      int = 0

escalated:     int = 0

@property

def first_pass_rate(self)  -> float: return self.first_pass_ok / self.total if self.total else 0.0

@property

def retry_rate(self)       -> float: return self.retried / self.total if self.total else 0.0

@property

def second_pass_rate(self) -> float: return self.retry_ok / self.retried if self.retried else 0.0

@property

def escalation_rate(self)  -> float: return self.escalated / self.total if self.total else 0.0

def print_pipeline_report(m):

print("Pipeline stage metrics:")

print(f"  total documents  : {m.total}")

print(f"  first-pass rate  : {m.first_pass_rate*100:.1f}%  ({m.first_pass_ok}/{m.total})")

print(f"  retry rate       : {m.retry_rate*100:.1f}%  ({m.retried}/{m.total})")

print(f"  second-pass rate : {m.second_pass_rate*100:.1f}%  ({m.retry_ok}/{m.retried or 0})")

print(f"  escalation rate  : {m.escalation_rate*100:.1f}%  ({m.escalated}/{m.total})")

if __name__ == "__main__":

random.seed(42)

ACCURACY_PROFILE = {

("digital_invoice",    "vendor_name"):  0.97,

("digital_invoice",    "invoice_date"): 0.98,

("digital_invoice",    "line_items"):   0.91,

("digital_invoice",    "total_amount"): 0.99,

("scanned_invoice",    "vendor_name"):  0.78,

("scanned_invoice",    "invoice_date"): 0.80,

("scanned_invoice",    "line_items"):   0.62,

("scanned_invoice",    "total_amount"): 0.75,

("handwritten_receipt","vendor_name"):  0.55,

("handwritten_receipt","invoice_date"): 0.48,

("handwritten_receipt","line_items"):   0.30,

("handwritten_receipt","total_amount"): 0.52,

}

VOLUMES    = {"digital_invoice": 160, "scanned_invoice": 30, "handwritten_receipt": 10}

FIELDS     = ["vendor_name", "invoice_date", "line_items", "total_amount"]

RETRY_RATE = {"digital_invoice": 0.85, "scanned_invoice": 0.70, "handwritten_receipt": 0.35}

collector   = MetricsCollector()

calibration = CalibrationTracker()

pipeline    = PipelineMetrics()

for doc_type, count in VOLUMES.items():

for _ in range(count):

pipeline.total += 1

doc_passed_first = True

for f in FIELDS:

acc        = ACCURACY_PROFILE[(doc_type, f)]

is_correct = random.random() < acc

record(collector, doc_type, f, "correct_value" if is_correct else "wrong_value", "correct_value")

confidence = {"digital_invoice": "high", "scanned_invoice": "medium",

"handwritten_receipt": "low"}[doc_type]

if doc_type == "scanned_invoice" and random.random() < 0.30:

confidence = "high"

record_confidence(calibration, confidence, is_correct)

if not is_correct:

doc_passed_first = False

if doc_passed_first:

pipeline.first_pass_ok += 1

else:

pipeline.retried += 1

if random.random() < RETRY_RATE[doc_type]:

pipeline.retry_ok += 1

else:

pipeline.escalated += 1

print("=== Document-type accuracy ===\n")

print_doc_type_report(collector)

print("\n=== Field-level accuracy ===\n")

print_field_report(collector)

print("\n=== Confidence calibration ===\n")

calibration_report(calibration)

print("\n=== Pipeline stage metrics ===\n")

print_pipeline_report(pipeline)

total_correct = sum(r.correct for r in collector.by_doc_type.values())

total_items   = sum(r.total   for r in collector.by_doc_type.values())

print(f"\nKey insight: aggregate accuracy = {total_correct/total_items*100:.1f}%")

hw = collector.by_doc_type["handwritten_receipt"]

print(f"  handwritten_receipt accuracy = {hw.accuracy*100:.1f}% — hidden inside the aggregate.")
```

⋯

All three metric collectors in one file. The 30% miscalibration rate on scanned invoices is intentional; it demonstrates what a broken confidence signal looks like in the calibration table.

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

=== Document-type accuracy ===

Document-type accuracy (sorted worst first):

handwritten\_receipt 44.5% [######## ] n=40

scanned\_invoice 73.6% [############## ] n=120

digital\_invoice 96.5% [################### ] n=640

=== Field-level accuracy ===

Field-level accuracy (sorted worst first):

line\_items 74.5% [############## ] n=200

invoice\_date 82.0% [################ ] n=200

vendor\_name 84.5% [################ ] n=200

total\_amount 86.5% [################# ] n=200

=== Confidence calibration ===

Confidence calibration (well-calibrated: high > medium > low):

high acc=90.1% n=199 [################## ]

medium acc=72.8% n=84 [############## ]

low acc=46.2% n=40 [######### ]

=== Pipeline stage metrics ===

Pipeline stage metrics:

total documents : 200

first-pass rate : 77.5% (155/200)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The aggregate accuracy is 90.5%, a number that looks healthy. The document-type breakdown reveals handwritten receipts at 44.5%, which requires a separate extraction approach that is invisible in the aggregate. The calibration table shows `high` accuracy (90.1%) greater than `medium` (72.8%) greater than `low` (46.2%), a well-calibrated signal despite the intentional miscalibration. The 22.5% retry rate with 71.1% second-pass success matches the “high retry, high second-pass” pattern from the lesson: the validator is catching real errors, and retry feedback is working, so the improvement investment should target first-pass failures, not the retry mechanism.

## Connecting metrics to improvement decisions[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Connecting-metrics-to-improvement-decisions)

Metrics are only useful if they drive decisions. Each anomaly pattern points to a specific intervention:

- **High retry rate with high second-pass rate:** The validator is catching real errors, and the feedback is working. The underlying issue is in the system prompt or examples. Improve the extraction prompt to reduce first-pass failures.
- **High retry rate with low second-pass rate:** The feedback is not specific enough, or the failure is systematic and cannot be fixed by rephrasing. Review the error messages the validator is generating, and check whether the same errors repeat across retried documents.
- **High escalation rate on one document type:** That document type is structurally different from what the prompt was designed for. Add document-type-specific examples or route that type through a separate extraction pipeline.
- **Miscalibrated confidence (high confidence but low accuracy):** The extraction prompt or examples are producing overconfident outputs. Add negative examples that show “low” confidence for ambiguous cases, or add a post-extraction calibration step that adjusts confidence based on which fields are missing or inconsistent.

## Exercise: Read the metrics[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Exercise-Read-the-metrics)

Each question presents a metrics snapshot from a running pipeline. Use the rules from this lesson to identify the problem and the appropriate response.

Technical Quiz

1.

A pipeline reports: first-pass rate 94%, retry rate 6%, second-pass rate 82%, escalation rate 1.1%. Which statement best describes the pipeline’s health?

A.

The pipeline is failing at the validation step; the retry rate is too high

B.

The escalation rate of 1.1% indicates a critical problem requiring immediate intervention

C.

The second-pass rate of 82% is too low; the feedback messages need to be rewritten

D.

Healthy: most pass first time, retries fix most failures, and escalation is low

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Whats-next)

In the next lesson, we close this chapter with an assessment quiz covering validators, retry feedback, batch vs. synchronous processing, and quality metrics across scenario-based questions.

Batch vs. Synchronous Processing

Validation and Metrics Assessment Quiz

Ask

[Why aggregate scores are insufficient](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Why-aggregate-scores-are-insufficient)

[Stratifying by document type](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Stratifying-by-document-type)

[Stratifying by field](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Stratifying-by-field)

[Confidence calibration](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Confidence-calibration)

[Workflow stage metrics](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Workflow-stage-metrics)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Complete-code)

[Connecting metrics to improvement decisions](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Connecting-metrics-to-improvement-decisions)

[Exercise: Read the metrics](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Exercise-Read-the-metrics)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/task-specific-quality-metrics#Whats-next)