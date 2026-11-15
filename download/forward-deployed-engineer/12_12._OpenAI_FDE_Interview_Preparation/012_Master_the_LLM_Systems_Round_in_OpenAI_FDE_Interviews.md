# Master_the_LLM_Systems_Round_in_OpenAI_FDE_Interviews

Source: https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# The LLM Systems Round

Explore the LLM systems round to understand how Forward Deployed Engineer interviews at OpenAI probe problem-solving and decision-making. Learn to trace requests through authentication, eligibility checks, retrieval, drafting, and validation. Discover best practices for access control, testing, and handling scenarios like stale records or conflicting sources to confidently design and defend AI system components.

We'll cover the following...

- [What do interviewers probe?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#What-do-interviewers-probe)
- [How do we trace one request?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-do-we-trace-one-request)
- [What does R-18 actually say?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#What-does-R-18-actually-say)
- [How deep should an answer go?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-deep-should-an-answer-go)
- [How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-does-this-sound-in-an-interview)
- [Practice questions](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Practice-questions)
  - [Retrieval:](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Retrieval)
    - [1. Why run the access check before retrieval instead of filtering the model’s answer?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#1-Why-run-the-access-check-before-retrieval-instead-of-filtering-the-models-answer)
    - [2. How do you enforce per-user permissions in retrieval without calling the source system on every request?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#2-How-do-you-enforce-per-user-permissions-in-retrieval-without-calling-the-source-system-on-every-request)
    - [3. Retrieved sources contradict each other. What should the system do?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#3-Retrieved-sources-contradict-each-other-What-should-the-system-do)
  - [Evals:](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Evals)
    - [4. Your eval reports 90% overall. What do you ask next?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#4-Your-eval-reports-90-overall-What-do-you-ask-next)
    - [5. When is a model grader acceptable?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#5-When-is-a-model-grader-acceptable)
  - [Agents and orchestration:](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Agents-and-orchestration)
    - [6. Why did you use one agent instead of several?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#6-Why-did-you-use-one-agent-instead-of-several)
    - [7. An agent’s tool call times out. What do you do with the result if it arrives later?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#7-An-agents-tool-call-times-out-What-do-you-do-with-the-result-if-it-arrives-later)
  - [Latency and cost:](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Latency-and-cost)
    - [8. The model call is fast but users say the system feels slow. Where do you look?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#8-The-model-call-is-fast-but-users-say-the-system-feels-slow-Where-do-you-look)
    - [9. How do you estimate the monthly cost of a feature?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#9-How-do-you-estimate-the-monthly-cost-of-a-feature)
- [Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Try-it-yourself)
- [What’s next?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Whats-next)

Twenty minutes into the technical session, the interviewer slid a report across: an offline retrieval test of the candidate’s Northstar design, called R-18. It covered 40 cases.

- 27 of 30 eligible cases produced supported drafts.
- All 6 stale cases were withheld.
- 1 of 4 attempted unauthorized reads put a protected passage into the model’s input.

“So, are we ready for a pilot?”

The candidate said yes, with an output filter added to catch unauthorized passages in the final answer. The interviewer asked one more question: “Where was the passage when your filter ran?” It was already in the model’s input. The filter could hide it from the screen. It couldn’t take it back.

Candidates [report](https://www.theforwarddeployed.io/interviews/openai) a technical session on LLM systems as part of the FDE loop, often starting from their take-home and going deeper. Its signature move is following one decision down to the mechanism behind it. This lesson covers what interviewers probe, how to trace a request through its boundaries, and a bank of practice questions in the same style.

## What do interviewers probe?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#What-do-interviewers-probe)

OpenAI’s [interview guide](https://openai.com/interview-guide/) says interviews aim to understand how candidates approach problems, make decisions, and communicate reasoning. In an LLM systems conversation, that usually means six areas, each tied to a decision we made.

|  |  |
| --- | --- |
| **Area** | **The Question Behind It** |
| Agents | Why a fixed workflow, one agent, or several? What does each extra agent cost? |
| Retrieval | Where does the access check run relative to ranking and the model call? |
| Evals | What are the denominators, and which results were observed versus predicted? |
| Latency | Which interval is being measured, and for which requests? |
| Cost | What does a task cost under stated assumptions, and what’s left out? |
| Failure handling | What happens when a check fails, a call times out, or evidence is missing? |

Keep the customer → problem → build → proof → handoff account intact, and put the decision and its strongest evidence first. That gives the interviewer a clear position to push on.

## How do we trace one request?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-do-we-trace-one-request)

A common technical follow-up is: "Walk me through what happens when a request arrives." A strong answer explains each processing stage in order and identifies the controls enforced at each boundary.

1. **Authenticate:** The application verifies the operator's identity using trusted credentials, never model-generated claims.
2. **Check eligibility:** Application code verifies the operator's access permissions and each record's applicability and freshness before protected content is passed to ranking or generation. If access is denied, a record is stale, or eligibility cannot be confirmed, return a generic "unavailable" response without exposing protected content.
3. **Retrieve:** Rank only eligible passages. If no eligible evidence supports the request, route it to manual review.
4. **Draft:** Generate a response from eligible evidence using a model call constrained by the configured token and execution budgets.
5. **Validate and route:** Application-level checks reject invalid classifications, incomplete outputs, and claims that fail the configured evidence checks. The operator reviews accepted drafts and retains authority over the final decision.

Compare the intended processing sequence with the path request R-18 actually followed.

This order puts an enforceable boundary in front of the model. A model instruction, a schema-valid answer, or a relevant citation can’t grant access. A citation helps an operator check a claim after access is allowed. It can’t make an unauthorized read acceptable.

## What does R-18 actually say?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#What-does-R-18-actually-say)

Before reading the breakdown, make the call the candidate got wrong, then sort the results into their denominators.

The three results in R-18 answer three different questions, so they can’t be averaged.

|  |  |  |
| --- | --- | --- |
| **Result** | **What It Measures** | **What It Doesn’t Measure** |
| 27 of 30 supported drafts | Task quality on eligible cases | Anything about access |
| 6 of 6 stale cases withheld | The freshness check on this set | The earlier 12-record result, which still needs its own rerun |
| 1 of 4 unauthorized passages reached the model | The access boundary, which failed | How often it would fail in production |

The trace shows where it failed. The retrieval adapter sent the protected passage toward the model before the entitlement check ran. That handoff is the first broken boundary. An output filter would act after the model already had the passage, and adding a second agent to review passages would just give the passage another recipient.

Address the access-control failure in the following order.

1. **Quarantine:** Disable the faulty adapter's access to protected data and restrict further testing to synthetic or approved test inputs.
2. **Reproduce:** Retrieve the original test case and execution trace, then identify where unauthorized content crossed the access boundary.
3. **Repair:** Enforce entitlement checks before protected content reaches retrieval or model-facing processing, alongside freshness and applicability checks. If access is denied or eligibility cannot be verified, return "unavailable" without exposing protected content.
4. **Verify:** Rerun the original case and an independent holdout set. Inspect the model inputs and access logs to confirm that unauthorized content never reached the model, rather than checking only the final response.

The three unsupported drafts from eligible requests represent a separate task-quality failure. Repairing the access boundary does not establish that these drafts are correct. Investigate them separately and retain all eligible cases in the task-quality denominator during regression testing.

If inspection can’t show what reached the model, the evidence is incomplete and the path stays off. The same rule applies when an access check fails or returns something ambiguous: the model is never asked whether a record is safe to read.

## How deep should an answer go?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-deep-should-an-answer-go)

Listen to how deep the question goes. An opening answer gives the decision, one piece of evidence, and its limit. A follow-up traces one mechanism, then says how we’d test it and what happens when it fails. Reciting every component when the question is about one boundary wastes the interviewer’s time and hides the answer.

Here is the same question answered at two depths. Asked “how do you handle stale records?”, an opening answer is one sentence of decision and one of evidence: “Freshness is checked before retrieval, alongside entitlement, and a stale record returns unavailable. In R-18, all six stale cases were withheld, though the earlier 12-record check still needs its rerun.” If the interviewer follows up with “how does the check know a record is stale?”, the answer goes one level down: “Each record carries a source version and an effective date. The check compares them with the current authoritative version for that ticket, and anything older, or anything whose version can’t be resolved, is treated as stale. I’d test it with superseded records, records with missing versions, and a record updated between retrieval and drafting.” The second answer is longer because the question asked for more, not because the candidate had more to say.

Interviewers also change a constraint to see how the design holds: a new user group, a tighter latency target, a new compliance rule. The strong move is to name which components change, which stay the same, and what we’d re-verify. “If operators in a second region join, the entitlement data changes and the eval set needs cases from that region. Retrieval, drafting, and the review screen stay as they are.” A tighter latency target works the same way: measure the eligibility check and the draft call separately first, and treat a smaller model or more caching as a trade-off to test against the eval set, never as a default.

Practice on four changes. For each one, pick what you would revisit first.

## How does this sound in an interview?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-does-this-sound-in-an-interview)

**Interviewer:** “Show me exactly where the access check runs.”

**Weak answer:** “The system prompt tells the model to only use authorized documents, and we filter the final answer for anything sensitive.”

**Strong answer:** “Before retrieval. The application authenticates the operator, then checks entitlement for each record, along with applicability and freshness, before any text reaches ranking or the model. Anything that fails or can’t be checked returns ‘unavailable’ with no content. In R-18, one adapter path sent a passage to the model before that check ran, so I quarantined that adapter, moved the check in front of it, and reran the case plus a holdout, inspecting the actual model inputs.”

## Practice questions[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Practice-questions)

Try answering each question before reading the answer. The questions are grouped the way interviewers tend to move through a system.

### Retrieval:[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Retrieval)

#### 1. Why run the access check before retrieval instead of filtering the model’s answer?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#1-Why-run-the-access-check-before-retrieval-instead-of-filtering-the-models-answer)

Answer: Once protected text is in the model’s input, it has been disclosed to the model, and any later filter can only hide it from the screen. Checking entitlement before ranking, together with applicability and freshness, means the model only ever sees eligible passages. It also keeps retrieval honest: ranking over ineligible passages can crowd out the eligible ones the answer needs.

#### 2. How do you enforce per-user permissions in retrieval without calling the source system on every request?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#2-How-do-you-enforce-per-user-permissions-in-retrieval-without-calling-the-source-system-on-every-request)

Answer: Store each document’s access control list as metadata on its chunks, with a permission version, and filter the search by it at query time. Resolving the user’s current groups from the identity provider isn’t enough on its own. If a document’s ACL changes while the user’s groups stay the same, the index still says the old thing. So agree a freshness contract with the source owner, such as revocations reaching the index within five minutes, and push revocations to the index and any answer cache as events, not only on a nightly schedule. When the system can’t show its permission data is within that bound, it fails closed: it withholds the affected passages or checks the source system before disclosing them. Monitoring the sync still matters, but an alert only reports a stale permission. It doesn’t stop the disclosure.

#### 3. Retrieved sources contradict each other. What should the system do?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#3-Retrieved-sources-contradict-each-other-What-should-the-system-do)

Answer: Surface both sources with their dates or versions instead of silently choosing one, and prefer the current authoritative version where a rule defines one. The ingestion pipeline can mark superseded versions so they rank lower or drop out. Where the conflict is genuine, the instructions tell the model to say the sources disagree and cite both.

### Evals:[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Evals)

#### 4. Your eval reports 90% overall. What do you ask next?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#4-Your-eval-reports-90-overall-What-do-you-ask-next)

Answer: What the denominator is, and how the result splits by slice. Capability and safety cases need separate thresholds, incomplete cases must stay in the denominator, and each case should be paired with the baseline to catch regressions. A 90% that includes one unauthorized read is a failing result.

#### 5. When is a model grader acceptable?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#5-When-is-a-model-grader-acceptable)

Answer: Only for meaning that code can’t decide, such as whether a draft describes an ambiguous note faithfully. It gets a narrow rubric, receives the draft as data, is calibrated against expert labels, and marks a case incomplete instead of passing when it fails or isn’t calibrated. Tool use, authorization, and side effects always go to code graders.

### Agents and orchestration:[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Agents-and-orchestration)

#### 6. Why did you use one agent instead of several?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#6-Why-did-you-use-one-agent-instead-of-several)

Answer: Because the task didn’t need more. Each extra agent adds a model call, a place for context to leak, and a new failure mode. A second agent earns its place only when a measured comparison against a single-agent baseline shows a quality gain that pays for those costs. Splitting for modularity alone usually doesn’t.

#### 7. An agent’s tool call times out. What do you do with the result if it arrives later?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#7-An-agents-tool-call-times-out-What-do-you-do-with-the-result-if-it-arrives-later)

Answer: Keep it tied to the call and turn that issued it, and accept it only if that turn is still current. If the user has moved on or the request changed, suppress the late result and re-ask or re-read. For a write, a timeout means the outcome is unknown, so reconcile against the ledger before any retry.

### Latency and cost:[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Latency-and-cost)

#### 8. The model call is fast but users say the system feels slow. Where do you look?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#8-The-model-call-is-fast-but-users-say-the-system-feels-slow-Where-do-you-look)

Answer: At the interval users actually experience: from their action to the first useful output. That includes retrieval and permission checks, orchestration calls and retries, and rendering. Measure each segment separately and look at slow percentiles, since a median hides the requests users complain about.

#### 9. How do you estimate the monthly cost of a feature?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#9-How-do-you-estimate-the-monthly-cost-of-a-feature)

Answer: Price every model call one task makes, including orchestration calls, expected retries, and tool charges, using real usage for cached and uncached input. Multiply by volume per task type, then stress-test the cache hit rate and traffic. State what’s excluded, such as infrastructure and review time, and replace assumed prices with current ones before calling it a budget.

## Try it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Try-it-yourself)

Pick one system you’ve designed and write the five-step request trace for it. For each step, write the check it enforces and what happens when that check can’t complete. Any step where the answer is “the model handles it” is the first follow-up an interviewer will ask.

AI Powered

Saved

8 attempts left

Reset

Statement

Four questions an interviewer could ask after this lesson. Answer each one as you would out loud: lead with your claim, then your evidence. The interviewer scores each answer against the lesson, gives feedback, and then asks the next question.

Let's start. The candidate proposed an output filter to catch unauthorized passages in R-18. Why doesn't that fix the failure?

You have 8 attempts to answer.

## What’s next?[#](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Whats-next)

The next three lessons put these stages to work on detailed case studies, each built to test a different stage. The first is a take-home assignment and presentation for a telecom support team exploring AI agents to handle customer messages. The challenge is to respond to a sponsor whose expectations go beyond what the available evidence supports.

The Case Study and Presentation

Case Study: Support Agents for Meridian Telecom

Ask

[What do interviewers probe?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#What-do-interviewers-probe)

[How do we trace one request?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-do-we-trace-one-request)

[What does R-18 actually say?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#What-does-R-18-actually-say)

[How deep should an answer go?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-deep-should-an-answer-go)

[How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#How-does-this-sound-in-an-interview)

[Practice questions](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Practice-questions)

[Retrieval:](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Retrieval)

[1. Why run the access check before retrieval instead of filtering the model’s answer?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#1-Why-run-the-access-check-before-retrieval-instead-of-filtering-the-models-answer)

[2. How do you enforce per-user permissions in retrieval without calling the source system on every request?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#2-How-do-you-enforce-per-user-permissions-in-retrieval-without-calling-the-source-system-on-every-request)

[3. Retrieved sources contradict each other. What should the system do?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#3-Retrieved-sources-contradict-each-other-What-should-the-system-do)

[Evals:](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Evals)

[4. Your eval reports 90% overall. What do you ask next?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#4-Your-eval-reports-90-overall-What-do-you-ask-next)

[5. When is a model grader acceptable?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#5-When-is-a-model-grader-acceptable)

[Agents and orchestration:](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Agents-and-orchestration)

[6. Why did you use one agent instead of several?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#6-Why-did-you-use-one-agent-instead-of-several)

[7. An agent’s tool call times out. What do you do with the result if it arrives later?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#7-An-agents-tool-call-times-out-What-do-you-do-with-the-result-if-it-arrives-later)

[Latency and cost:](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Latency-and-cost)

[8. The model call is fast but users say the system feels slow. Where do you look?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#8-The-model-call-is-fast-but-users-say-the-system-feels-slow-Where-do-you-look)

[9. How do you estimate the monthly cost of a feature?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#9-How-do-you-estimate-the-monthly-cost-of-a-feature)

[Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Try-it-yourself)

[What’s next?](https://www.educative.io/courses/forward-deployed-engineer/the-llm-systems-round#Whats-next)