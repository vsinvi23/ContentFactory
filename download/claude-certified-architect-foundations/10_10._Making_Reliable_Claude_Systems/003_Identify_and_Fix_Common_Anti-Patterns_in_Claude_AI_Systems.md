# Identify_and_Fix_Common_Anti-Patterns_in_Claude_AI_Systems

Source: https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Anti-Pattern Reference

Explore how to identify key anti-patterns in Claude AI architecture by their production symptoms, understand the root causes of predictable failures, and learn the correct fixes to apply. This lesson helps you audit system designs effectively and prepare for certification by reviewing common issues in agent loops, tools, prompts, context management, and evaluation metrics.

We'll cover the following...

- [Agent loop anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Agent-loop-anti-patterns)
  - [Natural language loop termination](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Natural-language-loop-termination)
  - [Missing tool result in the next turn](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Missing-tool-result-in-the-next-turn)
  - [Loop without a retry budget](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Loop-without-a-retry-budget)
- [Tool and integration anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Tool-and-integration-anti-patterns)
  - [Opaque tool failures](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Opaque-tool-failures)
  - [Over-broad tool descriptions](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Over-broad-tool-descriptions)
  - [Prompt-only tool access control](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Prompt-only-tool-access-control)
- [Prompt and output anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Prompt-and-output-anti-patterns)
  - [Vague criteria that cannot be evaluated](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Vague-criteria-that-cannot-be-evaluated)
  - [Generic retry feedback](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Generic-retry-feedback)
  - [Schema without semantic validation](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Schema-without-semantic-validation)
- [Context management anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Context-management-anti-patterns)
  - [Fact drift through single occurrence](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Fact-drift-through-single-occurrence)
  - [Provenance loss at synthesis](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Provenance-loss-at-synthesis)
  - [Over-escalation from retry failures](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Over-escalation-from-retry-failures)
- [Evaluation and metrics anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Evaluation-and-metrics-anti-patterns)
  - [Single aggregate accuracy score](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Single-aggregate-accuracy-score)
  - [Treating all partial failures as retryable](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Treating-all-partial-failures-as-retryable)
- [Exercise: Name the anti-pattern](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Exercise-Name-the-anti-pattern)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Whats-next)

Anti-patterns are design choices that seem reasonable in isolation but produce predictable failures at scale or under realistic conditions. Each one in this reference was introduced in an earlier chapter and appears here consolidated, with its symptom, cause, and fix side by side. This lesson is both a study reference for the certification exam and a checklist for architectural review. When designing or auditing a Claude-powered system, walking through these entries can surface problems before they reach production. By the end of this lesson, we will be able to:

- Identify each anti-pattern by its production symptom rather than its design description.
- Explain the specific cause behind each failure, not just that something went wrong.
- Name the correct fix for each one and the chapter where the corrective pattern was introduced.
- Apply the anti-pattern checklist to a new system design in review.

## Agent loop anti-patterns[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Agent-loop-anti-patterns)

These anti-patterns affect the core agent loop: how turns are managed, how stop conditions are handled, and how the loop terminates.

### Natural language loop termination[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Natural-language-loop-termination)

Loop logic that relies on Claude's words to decide when the task is done treats text output as a reliable protocol signal, which it is not.

- **Symptom:** The agent loop runs forever, exits too early, or exits on a false signal: a response that sounds like completion but is not.
- **Cause:** The loop termination condition reads Claude's output text and looks for phrases like “I have completed the task” or “the work is done.” Natural language is not a reliable termination signal. Claude may produce these phrases mid-task as a conversational acknowledgment, and a task that genuinely completes may not use those exact words.
- **Fix:** Terminate the loop on `stop_reason == "end_turn"` from the API response, not on text content. For tool-using agents, check that no `tool_use` blocks are present before treating `end_turn` as genuine task completion. If the task requires an explicit completion signal, give Claude a dedicated `task_complete` tool to call. A structured tool call is unambiguous in a way that text is not.

### Missing tool result in the next turn[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Missing-tool-result-in-the-next-turn)

Omitting the tool result from the conversation after a tool call breaks the turn sequence Claude depends on to track what has already happened.

- **Symptom:** The agent produces a `tool_use` block but then repeats the same tool call on the next turn, or appears confused about whether the tool ran.
- **Cause:** The application did not append the `tool_result` block to the conversation before sending the next API call. Claude sent a tool call; the application ran the tool but passed only a new user message as the next turn. Claude has no record of the tool result and must infer the outcome from the absence of information, which produces inconsistent behavior.
- **Fix:** After any response that contains `tool_use` blocks, append a `tool_result` block for each tool call, with the correct `tool_use_id`, before the next user message. The conversation must include `[user, assistant (tool_use), user (tool_result), ...]` in the correct order. Never skip the tool result turn.

### Loop without a retry budget[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Loop-without-a-retry-budget)

A retry loop with no maximum attempt count runs indefinitely when a failure is systematic rather than transient, consuming tokens and time without any path to resolution.

- **Symptom:** The agent gets stuck in a retry loop indefinitely. The pipeline consumes tokens and time without converging, and the failure only surfaces when someone checks manually.
- **Cause:** The retry logic has no maximum attempt count. The same validation error or tool failure appears on every attempt, and the loop has no exit condition other than success.
- **Fix:** Set `max_retries` as an explicit parameter for every retry loop. On the final attempt, return `None` or a failure result rather than retrying. Log the repeated error pattern for investigation. A loop that cannot terminate on failure is a reliability hazard, regardless of how unlikely the failure is.

## Tool and integration anti-patterns[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Tool-and-integration-anti-patterns)

These anti-patterns affect how tools are designed, how their errors surface, and how Claude selects between them.

### Opaque tool failures[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Opaque-tool-failures)

Tool failures that return a plain string instead of a structured error type give the agent no information about what went wrong, only the fact that something did.

- **Symptom:** The agent receives a tool error, escalates, blindly retries, or produces an incorrect fallback because it cannot determine what kind of error occurred.
- **Cause:** Tool error responses return a generic string: `"error"`, `"failed"`, or the raw exception message from the underlying service. The agent has no structured information about whether the failure is retryable, requires different credentials, indicates an empty result, or reflects an invalid input.
- **Fix:** Return structured error objects from every tool: `{"error_type": "permission_denied", "message": "...", "retryable": false}`. A controlled vocabulary of error types (`permission_denied`, `not_found`, `timeout`, `invalid_input`, `service_unavailable`) allows the agent to route each failure to the correct recovery action without guessing.

### Over-broad tool descriptions[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Over-broad-tool-descriptions)

A description that says what a tool does but not when to avoid it leaves Claude to infer scope from context, which fails on edge cases and out-of-domain queries.

- **Symptom:** Claude calls the wrong tool for a given task, calls a tool when it should not, or fails to call a tool when it should. Tool selection errors produce results that are structurally valid but semantically wrong.
- **Cause:** The tool description says what the tool does, but not when to use it and when not to. Without the “do not use when” clause, Claude applies the tool to edge cases it was not designed for, cases where a different tool, a different approach, or no tool call is the correct action.
- **Fix:** Every tool description should include: (1) the primary purpose; (2) required parameter types and constraints; (3) example input values; and (4) explicit “do not use when” guidance. The last item prevents the most common selection errors and is the most frequently omitted.

### Prompt-only tool access control[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Prompt-only-tool-access-control)

Access rules that exist only in the system prompt rely on Claude treating instructions as hard constraints, which they are not. Prompt instructions are advisory; application code is the actual enforcement layer.

- **Symptom:** Claude calls a tool it should not have access to in the current session context, or the access control rule is bypassed by rephrasing the request.
- **Cause:** The access rule exists only as a prompt instruction: “do not call the delete tool unless the user has explicitly requested deletion.” Prompt instructions are advisory. Claude follows them as guidance, but they are not enforced by the application. A rephrased request or an adversarial input can produce a tool call the instruction was meant to prevent.
- **Fix:** Enforce access control programmatically in the `dispatch_tool` function or equivalent gate: check the session's authorization context before the tool function executes, and return a structured `permission_denied` error if the check fails. The prompt instruction can remain as guidance, but the programmatic check is the actual enforcement mechanism.

## Prompt and output anti-patterns[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Prompt-and-output-anti-patterns)

These anti-patterns affect how instructions are written, how outputs are specified, and how review flows are structured.

### Vague criteria that cannot be evaluated[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Vague-criteria-that-cannot-be-evaluated)

Criteria that use degree-of-certainty language rather than observable properties produce different results every time the same borderline case is evaluated, by Claude and by human reviewers alike.

- **Symptom:** Two reviewers applying the same prompt produce different classifications for identical inputs. The pipeline is inconsistent, and the inconsistency cannot be diagnosed because there is no measurable definition of “correct.”
- **Cause:** The prompt uses qualitative guidance: “classify as high priority if it seems urgent” or “flag if the content is inappropriate.” These descriptions are not criteria. They are labels for the outcome without specifying the observable properties that determine it.
- **Fix:** Replace qualitative guidance with observable, measurable criteria: “classify as `high_priority` if the reported issue prevents the user from completing their primary workflow AND the user has not been able to work around it.” The criterion can be applied independently by two reviewers and produce the same result. Testable criteria also enable automated evaluation against labeled examples.

### Generic retry feedback[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Generic-retry-feedback)

Feedback that describes the outcome of a failure rather than the specific field, value, and rule gives Claude no new information between attempts, so each retry reproduces the same result as the first.

- **Symptom:** The retry loop runs the maximum number of attempts, but the same semantic errors appear on every attempt. The second and third outputs are no more correct than the first.
- **Cause:** The retry feedback message is generic: “the extraction was incorrect; please try again.” Claude receives no new information between attempts and has no basis for a different output. The retry loop fires correctly, but the feedback does not enable correction.
- **Fix:** The retry feedback must name: (1) the specific field that failed; (2) the value that was extracted; (3) the rule that value violated; and (4) a directive that sends Claude back to the source document: “invoice\_total is −245.00, but invoice totals cannot be negative. Re-read the document and extract the correct positive total.” Feedback that a human reviewer could act on is feedback Claude can act on.

### Schema without semantic validation[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Schema-without-semantic-validation)

Validation that stops at schema structure cannot detect errors that are well formed but domain invalid, values that satisfy the type system while violating the rules that make them meaningful.

- **Symptom:** The output passes JSON schema validation and reaches downstream processing but produces incorrect results. Negative totals are accepted, dates are inverted, and enum values are present but wrong for the input context.
- **Cause:** Validation stops at the schema check. Schema validation confirms shape: keys present, types correct, and required fields non-empty. It cannot check that a number is non-negative, that two date fields are temporally consistent, or that a classification matches the content it was derived from.
- **Fix:** Implement a semantic validator that runs after schema validation and encodes domain rules: `invoice_total >= 0`, `issue_date <= due_date`, `currency in {"USD", "EUR", "GBP", "CAD", "AUD"}`. Return all errors as a list rather than raising on the first, so Claude can correct all failing fields in a single retry.

## Context management anti-patterns[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Context-management-anti-patterns)

These anti-patterns affect how facts are preserved, how long sessions are managed, and how provenance is tracked.

### Fact drift through single occurrence[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Fact-drift-through-single-occurrence)

A stable fact stated once in the conversation without structural anchoring migrates toward the middle of the context window as the session grows, where small paraphrase variations accumulate undetected across turns.

- **Symptom:** A value that was correct in early outputs is subtly wrong in later outputs. A policy number has a dropped digit, or a date has a transposed month. The error appears gradually and is not caught until an audit.
- **Cause:** The stable fact was placed once in the conversation, in a user message, in a tool result, or in the middle of a long system prompt, without a case facts block or a verbatim instruction. As the session grows, the fact migrates toward the middle of the context window, where attention is weakest, and small paraphrase variations accumulate across turns.
- **Fix:** Place stable facts in a delimited case facts block at the top of the system prompt, with a verbatim instruction inside the block. Summarization should regenerate the block from the original values, not from the summarized text, so the anchor is refreshed at each compression point.

### Provenance loss at synthesis[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Provenance-loss-at-synthesis)

When a coordinator merges specialist findings into a narrative, each claim loses the metadata, source, confidence, agent role, and timestamp that would allow a downstream reviewer to trace it to its origin.

- **Symptom:** A coordinator agent produces a synthesis report. A downstream reviewer asks which specialist agent produced a specific claim and cannot find out. The claim exists in the report, but its origin is gone.
- **Cause:** The coordinator merged findings into a narrative without preserving the provenance fields from the underlying findings. The synthesis step replaced `{field, value, source, confidence, agent_role, timestamp}` objects with flowing prose. The prose carries no attribution.
- **Fix:** Pass findings to the coordinator in structured form with provenance blocks attached. Include a synthesis instruction that requires citing field, agent role, and confidence for each conclusion. If two findings conflict, the synthesis must report both with their provenance rather than silently resolving the conflict in the narrative.

### Over-escalation from retry failures[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Over-escalation-from-retry-failures)

When the escalation tool fires on errors that the retry loop should handle, the review queue fills with routine failures, diluting the attention reviewers give to the genuine decisions that require human judgment.

- **Symptom:** The escalation queue is full of packets for JSON parse errors, validation failures, and single-tool timeouts. Reviewers stop reading carefully. When a genuine escalation arrives (conflicting evidence, a policy gap, or an irreversible action), it is processed with the same superficial attention as the routine failures.
- **Cause:** The escalation tool's description is too broad (“use this when something goes wrong”), or the retry loop escalates on exhaustion regardless of the failure type. Retryable errors that resolve in two attempts end up in the escalation queue when the retry budget is exceeded, even if the failure indicates a prompt problem rather than a decision that requires human judgment.
- **Fix:** The escalation tool description must include explicit exclusions: “do not use this tool for JSON parse errors, semantic validation failures, or single-tool timeouts. These are handled by the retry loop.” Escalation should fire on the four defined conditions: high-impact irreversible actions, policy gaps, conflicting evidence, and confidence below threshold.

## Evaluation and metrics anti-patterns[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Evaluation-and-metrics-anti-patterns)

These anti-patterns affect how pipeline quality is measured and how improvement decisions are made.

### Single aggregate accuracy score[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Single-aggregate-accuracy-score)

An accuracy score averaged across all documents, fields, and confidence levels is dominated by the most common easy cases, making severe failures in rare categories invisible until a manual audit surfaces them.

- **Symptom:** The pipeline reports 91% accuracy, and the team concludes it is production-ready. A later audit reveals 52% accuracy on a specific field and 43% accuracy on a specific document type, failures that were invisible in the aggregate.
- **Cause:** The aggregate accuracy is the volume-weighted average across all documents, all fields, and all confidence levels. It is dominated by the most common, easiest cases. Hard documents and rare fields are statistical noise in a large enough data set.
- **Fix:** Stratify accuracy by document type, by field, and by confidence level. Report each stratum separately. A pipeline that is 91% accurate in aggregate but 52% accurate on `tax_id` has a `tax_id` problem, not a healthy pipeline. Workflow-stage metrics (first-pass rate, retry rate, second-pass rate, and escalation rate) provide a diagnostic picture that aggregate accuracy cannot.

### Treating all partial failures as retryable[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Treating-all-partial-failures-as-retryable)

Applying the same retry response to every non-success result treats four distinct failure types as one, three of which will not improve with additional attempts against the same inputs.

- **Symptom:** The retry loop hits its maximum attempt count on every run for a specific document type. The escalation queue fills with access failures and empty-result cases that should have been routed differently on the first attempt.
- **Cause:** The coordinator routes all non-success results to the retry loop without inspecting the failure type. Access failures, empty results, stale data, and partial completions all receive the same treatment: more attempts with the same inputs.
- **Fix:** Classify partial failures explicitly at the point of production (`PartialResult.failure_type`) and route each type to a different recovery action. Access failures escalate. Empty results are accepted as data gaps. Stale data triggers a refresh or escalates. Only partial completions retry, and only for the incomplete steps.

## Exercise: Name the anti-pattern[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Exercise-Name-the-anti-pattern)

Each scenario describes a production symptom. Identify the anti-pattern responsible and name the fix.

Technical Quiz

1.

A pipeline processes 3,000 invoices per day with an aggregate accuracy of 93%. A finance team audit finds that `tax_id` is correct only 49% of the time and that invoices from a specific regional supplier format are correct only 38% of the time. The engineering team was unaware of either problem before the audit. What anti-pattern caused this, and what metric strategy would have surfaced it earlier?

A.

Generic retry feedback; adding field-specific error messages would have surfaced the tax\_id problem

B.

Vague criteria; rewriting the extraction prompt with measurable criteria would have improved accuracy

C.

Schema without semantic validation; adding a tax\_id format validator would have caught the extraction errors

D.

Single aggregate accuracy score; stratify accuracy by field and document type instead

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Whats-next)

In the next lesson, we apply every pattern from the course to a single integrated scenario. We will work through a full system design brief, produce an architecture sketch, and evaluate it against the reliability checklist that consolidates the standards from all 10 chapters.

Partial Failures and Recovery

End-to-End System Design and Reliability Audit

Ask

[Agent loop anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Agent-loop-anti-patterns)

[Natural language loop termination](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Natural-language-loop-termination)

[Missing tool result in the next turn](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Missing-tool-result-in-the-next-turn)

[Loop without a retry budget](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Loop-without-a-retry-budget)

[Tool and integration anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Tool-and-integration-anti-patterns)

[Opaque tool failures](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Opaque-tool-failures)

[Over-broad tool descriptions](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Over-broad-tool-descriptions)

[Prompt-only tool access control](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Prompt-only-tool-access-control)

[Prompt and output anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Prompt-and-output-anti-patterns)

[Vague criteria that cannot be evaluated](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Vague-criteria-that-cannot-be-evaluated)

[Generic retry feedback](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Generic-retry-feedback)

[Schema without semantic validation](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Schema-without-semantic-validation)

[Context management anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Context-management-anti-patterns)

[Fact drift through single occurrence](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Fact-drift-through-single-occurrence)

[Provenance loss at synthesis](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Provenance-loss-at-synthesis)

[Over-escalation from retry failures](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Over-escalation-from-retry-failures)

[Evaluation and metrics anti-patterns](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Evaluation-and-metrics-anti-patterns)

[Single aggregate accuracy score](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Single-aggregate-accuracy-score)

[Treating all partial failures as retryable](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Treating-all-partial-failures-as-retryable)

[Exercise: Name the anti-pattern](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Exercise-Name-the-anti-pattern)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/anti-pattern-reference#Whats-next)