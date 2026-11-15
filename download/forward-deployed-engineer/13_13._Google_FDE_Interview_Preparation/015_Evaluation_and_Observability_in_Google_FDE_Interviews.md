# Evaluation_and_Observability_in_Google_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Evaluation and Observability

Explore how to measure agent quality across task success, groundedness, tool use, safety, latency, and cost. Learn to build golden sets, enforce regression gates before release, trace agent behavior in production, and turn every failure into a lasting test case.

We'll cover the following...

- [What to measure](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#What-to-measure)
- [Golden sets](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Golden-sets)
- [Regression gates](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Regression-gates)
- [Tracing and observability](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Tracing-and-observability)
- [A simple debugging loop](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#A-simple-debugging-loop)
- [Common evaluation mistakes](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Common-evaluation-mistakes)

A traditional software system can be tested with fixed inputs and expected outputs, and once a test passes, it keeps passing until someone changes the code. Agents do not behave this way. The same question can produce different answers, a small prompt change can improve one type of request while breaking another, and a model version update can shift behavior across the entire system. Most failures are also silent. An agent that retrieves the wrong policy and answers confidently does not crash or raise an error. It simply gives a wrong answer that looks right.

For these reasons, evaluation and observability are what turn an agent demonstration into a production system a customer can trust. FDE interviewers for Google’s GenAI track pay particular attention to this area, and a design that treats evaluation as a final step is one of the most frequently flagged gaps in system design rounds. This lesson covers golden sets, regression gates, tracing, and a simple loop for debugging agent failures.

## What to measure[#](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#What-to-measure)

An agent’s quality has several dimensions, and a single accuracy score hides important differences between them. A useful evaluation plan measures each dimension that matters for the use case.

|  |  |  |
| --- | --- | --- |
| **Dimension** | **Question it answers** | **Example measure** |
| Task success | Did the agent solve the user’s problem? | Percentage of cases with a correct final outcome |
| Groundedness | Is the answer supported by the retrieved sources? | Share of claims backed by a cited passage |
| Retrieval quality | Did retrieval return the right information? | Whether the correct document appears in the top results |
| Tool use | Did the agent call the right tools with the right arguments? | Tool selection and argument accuracy |
| Safety and policy | Did the agent stay within allowed behavior? | Rate of refusals on out-of-scope or harmful requests |
| Latency and cost | Is the agent fast and affordable enough? | Response time percentiles and cost per request |

Measuring these separately makes failures easier to locate. If task success drops but retrieval quality stays high, the problem is likely in reasoning or tool use, not in the data pipeline.

## Golden sets[#](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Golden-sets)

A golden set is a curated collection of test cases, each with an input and a definition of the correct outcome. It is the foundation of agent evaluation, because it provides a fixed, repeatable standard against which every change can be measured.

A strong golden set has four properties. It is built from **real requests**, drawn from support logs, user interviews, or pilot traffic, rather than invented by the engineering team. It provides **balanced coverage**, including common requests, difficult edge cases, out-of-scope questions, and adversarial inputs such as prompt injection attempts. It is **verified by domain experts** from the customer’s side, since only they can confirm the correct answer to a billing or policy question. It is also **versioned and growing**, with new cases added whenever a production failure is discovered.

For a first release, 50 to 200 well-chosen cases are usually enough to detect meaningful changes in quality. Size matters less than coverage of the situations the agent will actually face.

Each case can be scored in several ways, depending on what the correct outcome looks like.

|  |  |  |
| --- | --- | --- |
| **Evaluation Methon** | **Best For** | **Limitations** |
| Exact or programmatic checks | Tool names, structured fields, numeric values | Cannot judge open-ended text |
| Model-based grading | Open-ended answers judged against a rubric | Must be calibrated against human judgments |
| Human review | High-stakes or ambiguous cases | Slow and expensive at scale |

Most production evaluation combines all three. Programmatic checks cover what can be checked precisely, a model-based grader scores open-ended answers against a written rubric, and humans periodically review a sample to confirm the grader still agrees with expert judgment. Gemini Enterprise Agent Platform’s Agent Evaluation service supports these approaches, including evaluation of tool-use trajectories as well as final answers.

## Regression gates[#](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Regression-gates)

A golden set becomes most valuable when it runs automatically before every release. A regression gate runs the agent against the golden set, compares the scores to agreed thresholds, and blocks the release if any score falls below its threshold. This prevents a well-intended prompt change or model upgrade from quietly reducing quality in production.

The following script shows a simple regression gate. It uses a stand-in agent so it can run directly, without an API key.

Python 3.14.0

```
GOLDEN_SET = [

{"question": "Where is order 1042?", "expected_tool": "get_order_status", "must_include": "shipped"},

{"question": "Refund my $500 order", "expected_tool": "request_refund", "must_include": "approval"},

{"question": "What is your CEO's home address?", "expected_tool": None, "must_include": "can't help"},

]

THRESHOLDS = {"tool_accuracy": 0.95, "answer_accuracy": 0.90}

def evaluate(agent, golden_set):

tool_hits, answer_hits = 0, 0

for case in golden_set:

result = agent(case["question"])

tool_hits += result["tool"] == case["expected_tool"]

answer_hits += case["must_include"].lower() in result["answer"].lower()

n = len(golden_set)

return {"tool_accuracy": tool_hits / n, "answer_accuracy": answer_hits / n}

def regression_gate(scores):

failures = [m for m, t in THRESHOLDS.items() if scores[m] < t]

if failures:

raise SystemExit(f"Release blocked. Below threshold: {failures}")

print("Release approved:", scores)

def sample_agent(question):  # Stand-in for the real agent

if "order" in question and "Refund" not in question:

return {"tool": "get_order_status", "answer": "Order 1042 has shipped."}

if "Refund" in question:

return {"tool": "request_refund", "answer": "Your refund is pending approval."}

return {"tool": None, "answer": "Sorry, I can't help with that request."}

regression_gate(evaluate(sample_agent, GOLDEN_SET))
```

⋯

- **Lines 1–5:** Each golden case defines the question, the tool the agent should call, and a phrase the answer must contain. Line 4 is an out-of-scope request, where the correct behavior is to call no tool and decline.
- **Line 7:** Thresholds are agreed with the customer in advance, so the release decision follows a rule rather than a judgment made under deadline pressure.
- **Lines 9–16:** `evaluate` runs every case through the agent and scores tool selection and answer content separately.
- **Line 13:** Tool accuracy compares the tool the agent called with the expected tool, which catches errors that a correct-sounding answer could hide.
- **Line 14:** Answer accuracy uses a simple programmatic check. In production, open-ended answers would usually be scored by a calibrated model-based grader.
- **Lines 18–22:** `regression_gate` compares each score with its threshold and stops the release if any metric falls short.
- **Lines 24–29:** `sample_agent` stands in for the real agent so the script runs on its own. Changing one of its answers shows the gate blocking a release.
- **Line 31:** In a CI/CD pipeline, this line runs on every proposed change before deployment.

When proposing a regression gate in an interview, mention who sets the thresholds. Agreeing on them with the customer’s business owner turns “is the agent good enough?” from an open debate into a shared, measurable standard.

## Tracing and observability[#](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Tracing-and-observability)

Evaluation measures quality before release. Observability shows what the agent is actually doing in production. The most important tool here is tracing: recording each step of a request as a structured sequence, including the user input, each model call, retrieval results, tool calls and their arguments, approvals, and the final response, along with the latency and token usage of each step.

Traces make agent behavior inspectable. When a user reports a wrong answer, a trace shows whether retrieval returned the wrong document, the model chose the wrong tool, or a tool returned unexpected data. ADK supports OpenTelemetry tracing, and Gemini Enterprise Agent Platform’s Agent Observability, together with Cloud Trace and Cloud Logging, provides a place to store and analyze these traces.

Production monitoring builds on traces with ongoing signals: user feedback such as thumbs up or down, escalation rates to human agents, latency and cost trends, and a regular sample of conversations scored by the same graders used in the golden set. Because traces may contain personal or sensitive data, logging should apply masking and retention rules agreed with the customer’s security and compliance teams.

## A simple debugging loop[#](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#A-simple-debugging-loop)

When a production failure is reported, a consistent loop turns it into a lasting improvement rather than a one-time fix.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27712%27%20height=%27482%27/%3e)![debugging loop](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "debugging loop")

debugging loop

The most important step is adding the failing case to the golden set before fixing it. This confirms that the failure can be reproduced, shows when the fix works, and ensures the same failure cannot return unnoticed in a future release. Over time, the golden set becomes a record of every lesson the system has learned in production.

Localizing the failure also prevents wasted effort. Teams often respond to a wrong answer by rewriting the prompt, when the trace would have shown that the correct document was never retrieved. Fixing the right component, whether it is the data, retrieval, tool definition, prompt, or model choice, leads to faster and more durable improvements.

## Common evaluation mistakes[#](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Common-evaluation-mistakes)

Several mistakes recur in agent projects. The first is evaluating with a handful of manual spot checks instead of a repeatable golden set. The second is building the golden set from engineer-written questions that do not reflect real user requests. The third is measuring only final answers, which hides retrieval and tool-use failures. The fourth is relying on a model-based grader without checking that it agrees with human experts. The last is shipping prompt or model changes without rerunning the evaluation, which allows quality to drift silently over time.

Evaluation and observability give both the FDE team and the customer an objective view of how the agent performs. Golden sets define what correct behavior means, regression gates protect that standard on every release, tracing shows exactly what the agent did in production, and a consistent debugging loop turns each failure into a permanent test. Designs that build these practices in from the start are the ones that earn a customer’s confidence, and they are what Google’s interviewers look for when they ask how a candidate would know the system is working.

Identity and AI Security

The Telecom Case Brief

Ask

[What to measure](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#What-to-measure)

[Golden sets](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Golden-sets)

[Regression gates](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Regression-gates)

[Tracing and observability](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Tracing-and-observability)

[A simple debugging loop](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#A-simple-debugging-loop)

[Common evaluation mistakes](https://www.educative.io/courses/forward-deployed-engineer/evaluation-and-observability#Common-evaluation-mistakes)