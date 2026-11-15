# Managing_Deployment,_Voice,_Model_Selection_and_Cost_for_AI_Agents

Source: https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Deployment Surfaces, Voice, Model Choice, and Cost

Understand deployment options for AI agents, including infrastructure and data handling. Explore voice interaction architectures and how they impact system design. Learn model selection criteria balancing quality, speed, and cost. Calculate comprehensive operational expenses accounting for retries, caching, and workloads to prepare AI systems for real-world deployment and interview discussions.

We'll cover the following...

- [Where should the agent live?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Where-should-the-agent-live)
- [What does a customer need to hear about data?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#What-does-a-customer-need-to-hear-about-data)
- [When does voice change the design?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#When-does-voice-change-the-design)
- [How do we choose a model?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-we-choose-a-model)
  - [What does reasoning effort trade?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#What-does-reasoning-effort-trade)
- [How do caching, Batch, and Flex change the bill?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-caching-Batch-and-Flex-change-the-bill)
- [How do we cost the whole task?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-we-cost-the-whole-task)
- [How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-does-this-sound-in-an-interview)
- [Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Try-it-yourself)
- [What’s next?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Whats-next)

Northstar's finance lead approved a monthly budget of $126 for the operator assistant. The FDE based the estimate on one model call per task, assuming 6,000 cached input tokens and 500 output tokens for each of 18,000 monthly tasks.

Two weeks into the pilot, projected monthly costs exceeded $400, even though the assistant was functioning as designed. The estimate excluded additional model calls for orchestration, retry costs, and applicable tool charges. It also assumed a 100% prompt-cache hit rate.

The model with the lowest cost per call does not necessarily produce the lowest end-to-end deployment cost. This lesson examines the operational decisions that follow a working prototype: where to deploy the agent, how to manage data retention, whether to support voice interactions, which model to use, and how to estimate total operating costs.

These decisions are also relevant to FDE interviews because they require candidates to connect technical choices with operational constraints, customer requirements, and measurable costs.

## Where should the agent live?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Where-should-the-agent-live)

OpenAI offers three broad homes for an agent, and each moves the interface, the stored data, and the on-call duty to a different owner.

|  |  |  |
| --- | --- | --- |
| **Home** | **What It Is** | **Who Runs the Loop and Gets Paged** |
| Inside ChatGPT | The customer connects its systems to ChatGPT, for example through an MCP server, and teams can package repeatable work as shared Workspace Agents | Largely OpenAI’s product, governed by the customer’s workspace settings |
| ChatKit in the customer’s product | OpenAI’s embeddable chat interface, connected to a backend the customer runs | The customer, for the backend and everything behind it |
| The customer’s own service | The customer’s application calls an Agents SDK service it operates | The customer, end to end |

Northstar already has an operator console, so the strongest default is an Agents SDK service behind it, with ChatKit as an option if Northstar wants a ready-made chat interface. [ChatKit](https://developers.openai.com/api/docs/guides/chatkit)’s recommended setup is the advanced integration, where the customer runs a ChatKit server and connects it to any agent backend. The older hosted path built on Agent Builder is being retired, with shutdown scheduled for November 30, 2026 on OpenAI’s [deprecations page](https://developers.openai.com/api/docs/deprecations), and customers on it need a migration plan: inventory the workflow’s instructions, its tools and its approval points, rebuild it in code, and replay the old test cases against the new version before cutting over.

Running our own service means operating it. Northstar’s console log from the first week showed 24 draft submissions, six client timeouts each followed by a retry, and three duplicate drafts on operators’ screens. The tempting fix treats each timeout as a failure and resubmits with a new request ID. But a timeout only means the client stopped waiting. The server may still be working, or may have finished.

The service needs a stable request ID bound to the operator and the request content. A retry with the same ID returns the existing status. Changed content under the same ID is rejected. Until the service reconciles it, a timed-out request’s outcome is unknown, never failed. And the binding has to survive a restart, which means durable storage, not a dictionary in memory.

## What does a customer need to hear about data?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#What-does-a-customer-need-to-hear-about-data)

Enterprise customers ask where their data goes before they ask almost anything else. The answer has to be given per product and per endpoint, because every hop keeps its own copies.

- **Training:** Data sent to the API is not used to train OpenAI’s models unless the customer opts in.
- **Abuse monitoring:** By default, abuse-monitoring logs are kept for up to 30 days.
- **Zero data retention (ZDR):** Once OpenAI approves it for a customer, ZDR is configured at the organization or project level and keeps customer content out of those logs. Not every endpoint is eligible, so check OpenAI’s [current list](https://developers.openai.com/api/docs/guides/your-data) for each endpoint the design uses. At the time of writing it lists Responses as eligible with limitations, and Conversations, Files, and vector stores as not eligible.
- **Application copies:** Sessions, request registries, logs and traces all keep data, and so do error reports. Each needs a named owner who can read and delete it.
- **Product and third-party copies:** ChatGPT, ChatKit, connected destinations, and MCP servers each hold data under their own controls.

As the Responses API lesson noted, `store=False` stops a response from being saved for later retrieval. On its own, it doesn’t establish zero retention, data residency, or control over traces and connector copies. Any data requirement without a confirmed answer is a launch blocker.

## When does voice change the design?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#When-does-voice-change-the-design)

Northstar's operators want to ask about ticket dispatch windows using voice. Two common architectures support this:

- **Speech-to-speech:** A [Realtime](https://developers.openai.com/api/docs/guides/realtime-conversations) model processes audio input and generates spoken responses directly, without a separate transcription and synthesis pipeline. This can reduce latency and support more natural turn-taking. Input transcription is optional and runs separately from the audio model. Its output is an approximate representation of the speech, not an exact record of how the model interpreted the audio.
- **Chained pipeline:** Convert speech to text, process the text with a model, and synthesize the response as audio. Each stage can be inspected and replaced independently, but additional processing can increase latency. An incorrectly transcribed ticket number can also affect downstream reasoning.

Use speech-to-speech when low latency and natural interaction are priorities. A chained pipeline may be more suitable when the workflow requires explicit text checkpoints or when an existing text agent needs a voice interface. For browser-based Realtime sessions, WebRTC is a recommended connection method. The customer's backend can issue a short-lived client secret, allowing the browser to connect without exposing the server's long-lived API key.

In a text interface, submitting a message marks the end of the user's input. In a voice interface, the system must determine when the speaker has finished. Voice activity detection (VAD) can automate that decision. Server VAD detects the end of a speech turn after a configured period of silence. A shorter silence threshold can reduce response latency but may end a turn during a natural pause. Semantic VAD uses speech context to estimate whether the speaker has finished. Its `eagerness` setting controls how quickly the system concludes a turn, balancing responsiveness against premature interruptions.

In Northstar's first 20-turn rehearsal, the assistant began responding before the operator finished speaking in five turns. In two of those cases, a ticket lookup was already in progress when the operator corrected the request: "What's the dispatch window for NS-318... actually, wrong ticket."

Canceling the spoken response does not automatically cancel an in-flight ticket lookup. The lookup may still return correct information about NS-318, but presenting that result would answer a request the operator has withdrawn. The application must associate each tool call with its originating turn and discard results from requests that have been canceled or superseded.

The program below plays one session with two corrections, first with a tempting guard that treats every interruption as “the second turn,” then with the real one. It needs no API key.

Python 3.14.0

```
class FixedTurnGuard:

"""The tempting version: an interruption always means "the second turn"."""

def __init__(self):

self.turn = 1

self.calls = {}

def start_call(self, call_id):

self.calls[call_id] = self.turn

def interrupt(self):

self.turn = 2

def accept_result(self, call_id, result):

return result if self.calls.pop(call_id, None) == self.turn else None

class TurnGuard:

def __init__(self):

self.turn = 1

self.calls = {}                    # call_id -> the turn that issued it

def start_call(self, call_id):

self.calls[call_id] = self.turn

def interrupt(self):

self.turn += 1                     # every interruption opens a new turn

def accept_result(self, call_id, result):

if self.calls.pop(call_id, None) != self.turn:

return None                    # stale: suppress it and ask which ticket was meant

return result

def voice_session(guard):

"""An operator corrects the ticket twice while lookups are still in flight."""

guard.start_call("call_1")             # "What's the dispatch window for NS-318..."

guard.interrupt()                      # "...actually, wrong ticket. NS-381?"

guard.start_call("call_2")

guard.interrupt()                      # "No, sorry: NS-138."

guard.start_call("call_3")

late_results = [                       # lookups finish in whatever order the network allows

("call_2", "NS-381: window 09:00-11:00"),

("call_1", "NS-318: window 13:00-15:00"),

("call_3", "NS-138: window 16:00-18:00"),

]

for call_id, result in late_results:

shown = guard.accept_result(call_id, result)

print(f"  {call_id} -> {shown if shown else 'suppressed'}")

for guard in (FixedTurnGuard(), TurnGuard()):

print(type(guard).__name__)

voice_session(guard)
```

⋯

Drop tool results from a superseded turn

- **Lines 1–15:** `FixedTurnGuard` sets the turn to 2 on any interruption.
- **Lines 18–32:** `TurnGuard` counts every interruption and accepts a result only if its call was issued in the current turn.
- **Lines 35–49:** `voice_session` issues three lookups with two corrections between them, then delivers the results out of order.

Below is the output from one run.

Ace Editor

1

2

3

4

5

6

7

8

FixedTurnGuard

call\_2 -> NS-381: window 09:00-11:00

call\_1 -> suppressed

call\_3 -> NS-138: window 16:00-18:00

TurnGuard

call\_2 -> suppressed

call\_1 -> suppressed

call\_3 -> NS-138: window 16:00-18:00

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Output from one run

The fixed guard let NS-381’s result through. Its call came from the middle turn, and after two interruptions the fixed guard still thinks it’s the second turn. `TurnGuard` increments on every interruption, so only NS-138, the ticket the operator finally asked about, gets through. When a stale result is suppressed, the agent asks which ticket the operator meant and authorizes a fresh read. On interruption, the client also stops playback, cancels the stale response, and truncates the unplayed audio from the conversation so the model’s history matches what the operator actually heard.

Step through a session with two interruptions under both implementations and watch which late results reach the operator.

Latency is measured from the operator’s actual end of speech to the first audio they hear. A target budget for Northstar might be 350 ms to detect the end of the turn, 150 ms for network and dispatch, 500 ms to the first generated audio, and 100 ms of playback buffering, for 1,100 ms in total. That is a target to measure against, not a result.

## How do we choose a model?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-we-choose-a-model)

OpenAI’s lineup spans larger models for complex work, balanced models, and small fast models for high-volume tasks such as classification and routing. The tiers differ in quality, speed, price, context window, and which features and reasoning settings they support, and the lineup changes often. The starting tier comes from the task’s difficulty. The decision comes from the customer’s own evaluation.

Northstar compares two configurations on 40 real operator drafts. A draft passes when it follows the authorized source, cites the source and its version, and makes no unsupported claims. The bar is at least 38 of 40, with no critical unsupported claims.

|  |  |  |
| --- | --- | --- |
| **Configuration** | **Correct** | **Median Latency** |
| Fast candidate | 36 of 40 | 1.2 seconds |
| Stronger reasoning candidate | 39 of 40, no critical unsupported claims | 3.5 seconds |

Move the quality bar and the latency target to see which configuration qualifies, and when neither does.

The stronger candidate clears the bar, so it is the provisional choice. The fast one misses it, and its speed doesn’t change that. Before rollout, the FDE still investigates the one failure, agrees an acceptable latency with operators, and grows the eval set. A median says nothing about the slowest requests, and 40 cases are too few to prove production reliability. The voice path needs its own comparison on representative audio, because text results don’t carry over to speech.

### What does reasoning effort trade?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#What-does-reasoning-effort-trade)

Reasoning models accept a reasoning effort setting, such as `reasoning={“effort”: “low”}`. Supported values vary by model, typically from low through high, and some models also offer minimal or no reasoning. Lower effort answers faster and uses fewer tokens.

Reasoning tokens are billed as output and count against `max_output_tokens`. A tight output limit can end a response as `incomplete`, sometimes before any visible text appears. So tune effort as an experiment: run each setting on the same cases with the same output limit, and record correct drafts and incomplete responses, plus latency and token use. Changing the limit at the same time makes it impossible to tell which change helped.

## How do caching, Batch, and Flex change the bill?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-caching-Batch-and-Flex-change-the-bill)

Prompt caching reuses work on a matching prompt prefix. It applies automatically to prompts of at least 1,024 tokens, and cached input is billed at a discount. Put stable instructions and tool definitions first and case data last, keep tools in the same order, and read `usage.input_tokens_details.cached_tokens` to see actual hits. The cache is not a state store or an access boundary.

The program below sends two different notes behind the same long instructions and prices each call at this lesson’s working rates. Add your OpenAI API key in the widget before you run it.

Please provide values for the following:

OPENAI\_API\_KEY

Import Values from JSON

Python 3.14.0

```
from openai import OpenAI

client = OpenAI(api_key="{{OPENAI_API_KEY}}")

MODEL = "gpt-6.1-terra"

RATES = {"input": 2.00, "cached_input": 0.50, "output": 8.00}   # the lesson's working rates, USD per 1M tokens

MONTHLY_TASKS = 18_000

# Stable instructions go first, so every request shares the same long prefix.

REGIONS = ["North", "South", "East", "West", "Central", "Coastal"]

RULES = [f"Rule {i}: In the {REGIONS[i % 6]} region, a {kind} visit is dispatched within {2 + i % 5} "

f"business hours, and the operator confirms parts stock with depot {100 + i} before promising a time."

for i, kind in enumerate(["pump", "compressor", "boiler", "chiller", "generator"] * 12)]

INSTRUCTIONS = ("You draft short replies for Northstar operators. Follow the dispatch rules exactly.\n"

+ "\n".join(RULES))

NOTES = [  # case data goes last, after the shared prefix

"Draft a one-sentence reply: a pump in the North region stopped this morning.",

"Draft a one-sentence reply: a chiller in the Coastal region is making noise.",

]

def task_cost(usage):

cached = usage.input_tokens_details.cached_tokens

return ((usage.input_tokens - cached) * RATES["input"] + cached * RATES["cached_input"]

+ usage.output_tokens * RATES["output"]) / 1_000_000

for note in NOTES:

response = client.responses.create(model=MODEL, instructions=INSTRUCTIONS, input=note,

reasoning={"effort": "low"}, store=False)

usage = response.usage

print(f"input {usage.input_tokens:,} (cached {usage.input_tokens_details.cached_tokens:,}), "

f"output {usage.output_tokens:,}, cost ${task_cost(usage):.5f}")

cost = task_cost(usage)

uncached = (usage.input_tokens * RATES["input"] + usage.output_tokens * RATES["output"]) / 1_000_000

print(f"\nThis call at {MONTHLY_TASKS:,} tasks a month: ${cost * MONTHLY_TASKS:,.2f}")

print(f"The same call with no cache hits:      ${uncached * MONTHLY_TASKS:,.2f}")
```

⋯

Measure cache hits and price each call

- **Lines 5–6:** The rates are this lesson’s working assumptions, not current prices.
- **Lines 9–14:** About 2,000 tokens of dispatch rules form the stable prefix.
- **Lines 16–19:** The case data, two different notes, goes last.
- **Lines 22–25:** `task_cost` prices uncached input, cached input, and output separately.
- **Lines 28–33:** Each call reports its input tokens, how many were cached, and its output tokens.
- **Lines 35–38:** The monthly figures price only this one call, with and without cache hits.

Below is the output from one run. Cache hits aren’t guaranteed, so your second call may show fewer cached tokens.

Ace Editor

1

2

3

4

5

input 2,154 (cached 0), output 69, cost $0.00486

input 2,155 (cached 2,130), output 33, cost $0.00138

This call at 18,000 tasks a month: $24.82

The same call with no cache hits: $82.33

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Output from one run

The second call reused 2,130 cached tokens and cost less than a third of the first. Both monthly figures still price one call, not the whole task, which is the mistake the last section of this lesson fixes.

Processing mode is a separate decision:

|  |  |  |
| --- | --- | --- |
| **Mode** | **Fits** | **Trade-Off** |
| Standard | A draft an operator is waiting for | Full price, interactive latency |
| Batch | A nightly set of independent cases | About half the price, results within a 24-hour window; match outputs to inputs by `custom_id` |
| Flex | A single delay-tolerant job on a supported model | Lower price via `service_tier="flex"`, slower responses, occasional resource-unavailable errors to retry |

Neither Batch nor Flex fits a waiting operator or a live voice turn. For a nightly batch, reconcile every case ID. If the hardest cases are the ones that don’t finish, scoring only the completed ones flatters the result.

## How do we cost the whole task?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-we-cost-the-whole-task)

Back to the budget. The $126 estimate made two mistakes: it assumed a full cache hit, and it priced only the primary call. A task-level estimate prices every call. The rates below are working assumptions for the exercise, per million tokens: $2 for uncached input, $0.50 for cached input, and $8 for output.

|  |  |  |
| --- | --- | --- |
| **Component** | **Calculation** | **Cost Per Task** |
| Primary call | 4,000 uncached input ($0.008) + 2,000 cached ($0.001) + 500 output ($0.004) | $0.013 |
| Orchestration call | 2,000 uncached input ($0.004) + 250 output ($0.002) | $0.006 |
| Expected retries | 0.1 retries per task × $0.013 | $0.0013 |
| Tool charges | Per task | $0.002 |
| Total |  | $0.0223 |

At 18,000 tasks, that’s $401.40 a month, $275.40 more than the first budget. Two stress tests show how sensitive it is. With no cache hits, the primary call costs $0.016, the total is $0.0256 per task, and the month comes to $460.80. At 22,500 tasks with the original cache split, the month is $501.75.

Rebuild the estimate yourself. Start from the first estimate, add each missing piece, then stress the cache and the traffic.

These figures still leave out infrastructure, staff review time, and voice. Before they become a budget, the FDE swaps in current prices for the exact model and processing tier, plus the tools, and hands the operating team everything needed to redo the math: the configuration, the eval results, actual usage including cached tokens, the retry policy, and the price source.

## How does this sound in an interview?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-does-this-sound-in-an-interview)

**Interviewer:** “The fast configuration is three times faster at the median. Why choose the slower one?”

**Weak answer:** “The bigger model is always safer, and we can put requests in Batch to save money.”

**Strong answer:** “On Northstar’s 40-case set, the stronger configuration met the bar at 39 correct with no critical unsupported claims. The fast one got 36 and missed it. I’d investigate the remaining failure and agree a latency target with operators before rollout. Batch fits the nightly comparisons, not a draft someone is waiting for. And I’d price the whole task, including retries and tool charges, not just the first call.”

**Interviewer:** “What happens to the budget if the cache stops hitting?”

**Strong answer:** “With expected retries, it goes from $0.0223 to $0.0256 per task, or $460.80 a month at 18,000 tasks. I’d replace the assumed rates and cache split with real usage before calling it a budget.”

## Try it yourself[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Try-it-yourself)

Choose an LLM feature you've built or used. Identify every model call triggered by a single user action, including orchestration calls and retries, along with any billable tool usage. Calculate the total cost, then recalculate it without assuming any input tokens are cached.

AI Powered

Saved

8 attempts left

Reset

Statement

Four questions an interviewer could ask after this lesson. Answer each one as you would out loud: lead with your claim, then your evidence. The interviewer scores each answer against the lesson, gives feedback, and then asks the next question.

Let's start. A client times out and retries with a new request ID. Why does that produce duplicate drafts, and what's the fix?

You have 8 attempts to answer.

## What’s next?[#](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Whats-next)

Northstar's agent meets its latency and cost targets and runs in the intended deployment environment. The next challenge is demonstrating that it works reliably. How do you verify its behavior and identify failures?

In the next lesson, you'll build a programmatic evaluation set, implement guardrails and prompt-injection defenses, and use execution traces to investigate failures in an agent pipeline.

The Agents SDK, MCP, and Multi-Agent Patterns

Evals, Guardrails, and Debugging with Traces

Ask

[Where should the agent live?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Where-should-the-agent-live)

[What does a customer need to hear about data?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#What-does-a-customer-need-to-hear-about-data)

[When does voice change the design?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#When-does-voice-change-the-design)

[How do we choose a model?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-we-choose-a-model)

[What does reasoning effort trade?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#What-does-reasoning-effort-trade)

[How do caching, Batch, and Flex change the bill?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-caching-Batch-and-Flex-change-the-bill)

[How do we cost the whole task?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-do-we-cost-the-whole-task)

[How does this sound in an interview?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#How-does-this-sound-in-an-interview)

[Try it yourself](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Try-it-yourself)

[What’s next?](https://www.educative.io/courses/forward-deployed-engineer/deployment-surfaces-voice-model-choice-and-cost#Whats-next)