# Maintaining_Claude_AI_Reliability_in_Long_Sessions

Source: https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Long Session Health

Explore how to maintain reliability in long Claude AI sessions by detecting context degradation early. Learn to implement scratchpads that preserve state, use conversation summarization to compress history, and delegate to sub-sessions to manage context windows effectively. Understand the signals of session health decline and apply practical strategies to keep AI conversations precise and stable over time.

We'll cover the following...

- [Signals that a session is degrading](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Signals-that-a-session-is-degrading)
- [The scratchpad pattern](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#The-scratchpad-pattern)
- [Conversation summarization](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Conversation-summarization)
- [Detecting context pressure from the API response](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Detecting-context-pressure-from-the-API-response)
- [Delegation to a sub-session](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Delegation-to-a-sub-session)
  - [Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Complete-code)
- [When to summarize vs. when to delegate](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#When-to-summarize-vs-when-to-delegate)
- [Exercise: Diagnose and respond](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Exercise-Diagnose-and-respond)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Whats-next)

A session that starts reliably can degrade as it grows. Context window pressure is the most common cause: the window fills with earlier tool outputs, assistant responses, and intermediate reasoning until there is little headroom left for the work that remains. A second, subtler cause is fact drift; the session has grown so long that facts from early turns are now in the middle of the window, where they compete with later content for attention. The session still functions, but it makes mistakes it would not have made in the first 10 turns. This lesson covers how to detect these patterns before they cause failures and how to use scratchpads, summaries, and sub-session delegation to keep long work on track. By the end of this lesson, we will be able to:

- Identify the signals that indicate a session is approaching a reliability boundary.
- Implement a scratchpad pattern that keeps the running state visible without growing without bound.
- Apply conversation summarization to compress completed work and preserve context headroom.
- Decide when to delegate remaining work to a sub-session rather than continuing in the current one.

## Signals that a session is degrading[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Signals-that-a-session-is-degrading)

A session does not fail suddenly. It degrades gradually, and the degradation is visible before failures become costly. Key signals to watch:

- **Context length approaching the model's window:** The most concrete signal. When input tokens (context + current message) approach the model's context limit, there is less space for the response and less attention available for early-context facts. Each additional turn makes this worse.
- **Repeated extraction of the same value differently:** A policy number that appeared as `POL-2024-0091-B` in turn three appears as `POL-2024-91B` in turn 19. The session is still producing plausible outputs but no longer reproducing earlier facts verbatim.
- **Stale reasoning used for current decisions:** Claude refers to a conclusion reached in an earlier turn that has since been updated or corrected, applying the outdated conclusion to a current step. This happens when the correction is buried in the middle of the context and the earlier statement is closer to the beginning.
- **Tool calls that duplicate earlier work:** Claude calls a tool to retrieve data that it already retrieved earlier in the session. This is a symptom of the earlier tool result being trimmed or pushed far enough from the current turn that Claude did not notice it was already available.
- **Increasingly verbose or hedged responses:** As context pressure builds, responses become less precise. This is a softer signal, but it is a real one: a response that was sharp and direct in turn five becomes qualified and uncertain in turn 40 for the same type of question.

## The scratchpad pattern[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#The-scratchpad-pattern)

A scratchpad is a running state document that Claude maintains across turns. It records what has been decided, what has been found, what remains to be done, and any values that must be kept verbatim. The scratchpad replaces the need to re-read the full conversation history to recover state. The scratchpad lives in one of two places:

1. As a user message or tool result appended to the conversation at the start of each turn, containing the current state.
2. As a file written and read by a dedicated write/read tool call at the start of each turn.

Both approaches work. The key property is that the scratchpad is updated after each meaningful action, kept short (under one page), and structured so the most important facts appear first. A scratchpad structure for a claim investigation session:

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

=== SESSION SCRATCHPAD (updated after each action) ===

## Anchored facts

Case ID: CLM-2024-4471

Policy ref: POL-2024-0091-B

Claimant: Torres, Alejandra

## Progress

Step 1 (done): Retrieved policy terms — coverage confirmed for incident type

Step 2 (done): Requested adjuster notes — received, attached

Step 3 (active): Reviewing adjuster notes for documented exclusion flags

Step 4 (pending): Determine if Exclusion EXCL-48B applies

## Current finding

Adjuster noted three items of possible concern. None yet confirmed as exclusions.

## Open questions

- Were repair costs pre-approved by the insurer?

=== END SCRATCHPAD ===

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A scratchpad that separates anchored facts, completed steps, the current active step, and open questions. The anchored facts section mirrors the case facts block from the previous lesson and reinforces it even as the full conversation grows.

The scratchpad is not the same as a verbose reasoning trace. It captures decisions and verified values, not the process of arriving at them. A scratchpad entry that says “Step one (done): Retrieved policy terms, coverage confirmed for incident type” is enough. A scratchpad entry that re-explains the full reasoning is just another source of context bloat.

## Conversation summarization[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Conversation-summarization)

Summarization compresses completed turns into a compact representation that preserves the decisions made without preserving the full text that led to them. It is applied retroactively: the last N turns are replaced with a summary, freeing context space for the work that remains.

The summary must preserve:

- All values that will be referenced in future tool calls or outputs (IDs, dates, amounts, decisions).
- All constraints that are still active (rules that apply to remaining steps).
- All findings that have not yet been acted on.
- Any open questions that a later turn must answer.

The summary does not need to preserve:

- The exact wording of intermediate tool outputs.
- Reasoning traces that led to closed decisions.
- Raw document text that has been fully processed.
- Hedging language from earlier responses that was resolved later.

A summarization instruction to include in the system prompt for long-running sessions:

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

When the conversation exceeds 30 turns or 60,000 input tokens, produce a structured

summary of completed steps before continuing. The summary must include:

- All case facts verbatim (do not abbreviate IDs, amounts, or dates)

- A numbered list of completed steps with their outcomes

- All active constraints that still apply

- All unresolved findings and open questions

After the summary, continue with the current step as if the summary were the complete

prior context.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A summarization instruction that specifies exactly what the summary must and must not include. The “verbatim” qualifier on case facts prevents the summary from being the point where IDs get paraphrased.

Summarization can be triggered automatically by the application by detecting context length in the API response's `usage` field, or manually by a human operator who monitors session health. Automatic triggering is more reliable in production systems.

## Detecting context pressure from the API response[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Detecting-context-pressure-from-the-API-response)

The API response includes a `usage` object that reports the number of tokens in the current context. Monitoring this field allows the application to trigger summarization or delegation before the window is exhausted:

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

import anthropic

client = anthropic.Anthropic()

SUMMARIZE\_AT = 60\_000 # trigger summarization

DELEGATE\_AT = 90\_000 # trigger sub-session delegation

MAX\_CONTEXT = 200\_000 # claude-opus-4-8 context window

def run\_turn(messages: list, system: str) -> tuple[str, int]:

response = client.messages.create(

model="claude-opus-4-8",

max\_tokens=4096,

system=system,

messages=messages

)

input\_tokens = response.usage.input\_tokens

text = response.content[0].text

return text, input\_tokens

def session\_loop(task: str, system: str) -> None:

messages = [{"role": "user", "content": task}]

while True:

reply, used = run\_turn(messages, system)

messages.append({"role": "assistant", "content": reply})

if used >= DELEGATE\_AT:

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A session loop that checks response.usage.input\_tokens after each turn and triggers either summarization or delegation when thresholds are crossed. The loop checks the delegation threshold first, so a session that crosses both in a single turn delegates rather than summarizing.

- **Lines 11–12:** `SUMMARIZE_AT` and `DELEGATE_AT` define two escalation thresholds. Summarization recovers some context headroom while keeping the session alive. Delegation is the stronger action: the current session ends, and a sub-session takes over.
- **Lines 21–22:** `response.usage.input_tokens` is checked after each turn, not before. The check uses the actual input tokens the API reported, which is more reliable than estimating token count from character length.
- **Lines 30–32:** The delegation threshold is checked before the summarization threshold. A session that has already been summarized multiple times and is still growing toward the limit should be delegated, not summarized again.

## Delegation to a sub-session[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Delegation-to-a-sub-session)

Delegation creates a fresh session with a compact handoff packet derived from the current session's scratchpad. The sub-session inherits the state that matters: verified facts, completed steps, active constraints, and open questions, without inheriting the full conversation history that caused the context pressure. A handoff packet structure:

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

def build\_handoff\_packet(

case\_facts: dict,

completed\_steps: list[str],

active\_constraints: list[str],

open\_questions: list[str],

current\_step: str

) -> str:

facts\_block = "\n".join(

f"{k}: {v}" for k, v in case\_facts.items()

)

steps\_block = "\n".join(

f" {i+1}. {s}" for i, s in enumerate(completed\_steps)

)

constraints\_block = "\n".join(f" - {c}" for c in active\_constraints)

questions\_block = "\n".join(f" - {q}" for q in open\_questions)

return (

"=== HANDOFF PACKET ===\n"

f"CASE FACTS (verbatim):\n{facts\_block}\n\n"

f"COMPLETED STEPS:\n{steps\_block}\n\n"

f"ACTIVE CONSTRAINTS:\n{constraints\_block}\n\n"

f"OPEN QUESTIONS:\n{questions\_block}\n\n"

f"CURRENT STEP: {current\_step}\n"

"=== END HANDOFF PACKET ==="

)

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A function that assembles a structured handoff packet from the scratchpad components. The packet is the first user message in the sub-session. It carries forward only the state the sub-session needs, not the full conversation.

- **Lines 8–10:** Case facts are formatted as flat key-value pairs, the same format as the case facts block from Lesson 9.1. The label “verbatim” is preserved explicitly, so the sub-session's system prompt receives the same signal the original session had.
- **Lines 11–12:** Each section of the packet is a separately labeled block. Labeling makes it easy for the sub-session to locate specific information without rereading the full packet.

### Complete code[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Complete-code)

We bring the token thresholds, `session_loop`, `summarize_session`, and `build_handoff_packet` from this lesson into one runnable file. The non-interactive part, the handoff packet builder, always runs and prints a fully formatted packet. We include the interactive session loop in the file, but comment it out so the script completes immediately without waiting for keyboard input.

Please provide values for the following:

ANTHROPIC\_API\_KEY

Import Values from JSON

Python 3.14.0

```
import anthropic

anthropic_api_key = "{{ANTHROPIC_API_KEY}}"

client = anthropic.Anthropic(api_key=anthropic_api_key)

SUMMARIZE_AT = 2_00   # trigger summarization at this many input tokens

DELEGATE_AT  = 3_00   # trigger sub-session delegation at this many input tokens

SYSTEM = """You are a claim investigation assistant working through a multi-step insurance claim review.

After each step, update the scratchpad provided in the user message.

When the conversation exceeds 30 turns or 2,00 input tokens, produce a structured

summary of completed steps before continuing. The summary must include:

- All case facts verbatim (do not abbreviate IDs, amounts, or dates)

- A numbered list of completed steps with their outcomes

- All active constraints that still apply

- All unresolved findings and open questions

After the summary, continue with the current step as if the summary were the complete

prior context."""

INITIAL_SCRATCHPAD = """=== SESSION SCRATCHPAD (updated after each action) ===

## Anchored facts

Case ID:    CLM-2024-4471

Policy ref: POL-2024-0091-B

Claimant:   Torres, Alejandra

## Progress

Step 1 (pending): Retrieve policy terms

## Current finding

None yet.

## Open questions

- Does coverage apply to the reported incident type?

=== END SCRATCHPAD ==="""

def run_turn(messages: list, system: str) -> tuple[str, int]:

response = client.messages.create(

model="claude-opus-4-8",

max_tokens=4096,

system=system,

messages=messages

)

input_tokens = response.usage.input_tokens

text = response.content[0].text

return text, input_tokens

def summarize_session(messages: list, system: str) -> list:

compress_request = (

"The session is approaching its context limit. "

"Produce a structured summary of everything completed so far, "

"preserving all case facts verbatim, all decisions, all active constraints, "

"and all open questions. Then continue from where we left off."

)

messages_with_request = messages + [{"role": "user", "content": compress_request}]

summary_text, _ = run_turn(messages_with_request, system)

return [{"role": "user", "content": summary_text}]

def build_handoff_packet(

case_facts:         dict,

completed_steps:    list,

active_constraints: list,

open_questions:     list,

current_step:       str

) -> str:

facts_block       = "\n".join(f"{k}: {v}" for k, v in case_facts.items())

steps_block       = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(completed_steps))

constraints_block = "\n".join(f"  - {c}" for c in active_constraints)

questions_block   = "\n".join(f"  - {q}" for q in open_questions)

return (

"=== HANDOFF PACKET ===\n"

f"CASE FACTS (verbatim):\n{facts_block}\n\n"

f"COMPLETED STEPS:\n{steps_block}\n\n"

f"ACTIVE CONSTRAINTS:\n{constraints_block}\n\n"

f"OPEN QUESTIONS:\n{questions_block}\n\n"

f"CURRENT STEP: {current_step}\n"

"=== END HANDOFF PACKET ==="

)

def delegate_to_sub_session(last_reply: str, messages: list) -> None:

print("\n[DELEGATION] Remaining work handed off to a fresh sub-session.")

print("  The sub-session would receive a handoff packet containing:")

print("  - All anchored case facts (verbatim)")

print("  - Completed steps and their outcomes")

print("  - Active constraints")

print("  - Open questions")

print("  - The current step to resume from")

def session_loop(task: str, system: str) -> None:

messages = [{"role": "user", "content": task}]

while True:

reply, used = run_turn(messages, system)

messages.append({"role": "assistant", "content": reply})

print(f"  [turn complete] input_tokens={used}")

print(f"  Reply excerpt: {reply[:120]}...\n")

if used >= DELEGATE_AT:

print(f"[{used} tokens] Threshold reached — delegating remaining work to sub-session.")

delegate_to_sub_session(reply, messages)

break

if used >= SUMMARIZE_AT:

print(f"[{used} tokens] Threshold reached — summarizing completed work.")

messages = summarize_session(messages, system)

next_input = input("Next instruction (or 'done'): ").strip()

if next_input.lower() == "done":

print("Session complete.")

break

messages.append({"role": "user", "content": next_input})

if __name__ == "__main__":

print("=== Long Session Health Demo ===\n")

print(f"  SUMMARIZE_AT = {SUMMARIZE_AT:,} tokens")

print(f"  DELEGATE_AT  = {DELEGATE_AT:,} tokens\n")

print("=== Handoff Packet Example ===")

packet = build_handoff_packet(

case_facts={

"Case ID":    "CLM-2024-4471",

"Policy ref": "POL-2024-0091-B",

"Claimant":   "Torres, Alejandra"

},

completed_steps=[

"Retrieved policy terms — coverage confirmed for incident type",

"Requested adjuster notes — received and attached"

],

active_constraints=[

"Exclusion EXCL-48B must be checked before approving payout",

"Pre-approval required for repair costs over $5,000"

],

open_questions=[

"Were repair costs pre-approved by the insurer?"

],

current_step="Step 3: Review adjuster notes for documented exclusion flags"

)

print(packet)

print("\n\nTo run the interactive session loop, uncomment the line below:")

print("# session_loop(INITIAL_SCRATCHPAD, SYSTEM)")
```

⋯

Token thresholds, session loop, summarizer, and handoff packet builder

Running the file with the session loop commented out prints only the threshold constants and the formatted handoff packet.

The expected output is deterministic; no API call is required.

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

=== Long Session Health Demo ===

SUMMARIZE\_AT = 2,00 tokens

DELEGATE\_AT = 3,00 tokens

=== Handoff Packet Example ===

=== HANDOFF PACKET ===

CASE FACTS (verbatim):

Case ID: CLM-2024-4471

Policy ref: POL-2024-0091-B

Claimant: Torres, Alejandra

COMPLETED STEPS:

1. Retrieved policy terms — coverage confirmed for incident type

2. Requested adjuster notes — received and attached

ACTIVE CONSTRAINTS:

- Exclusion EXCL-48B must be checked before approving payout

- Pre-approval required for repair costs over $5,000

OPEN QUESTIONS:

- Were repair costs pre-approved by the insurer?

CURRENT STEP: Step 3: Review adjuster notes for documented exclusion flags

=== END HANDOFF PACKET ===

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Output

To see the summarization threshold in action, uncomment `session_loop(INITIAL_SCRATCHPAD, SYSTEM)` at **line 150**. It requires `ANTHROPIC_API_KEY`. Drive the session through enough turns that `input_tokens` crosses 2,000. The script will print a `[SUMMARIZE_AT reached]` line and replace the full message history with a single compressed summary before continuing.

## When to summarize vs. when to delegate[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#When-to-summarize-vs-when-to-delegate)

Both summarization and delegation address context pressure, but they have different costs and appropriate use cases.

|  |  |  |
| --- | --- | --- |
| **Factor** | **Summarize** | **Delegate** |
| Context pressure | Approaching the summarization threshold | Approaching context limit even after prior summaries |
| Session continuity | Preserve the current session and continue | End the current session; sub-session takes over |
| State transfer fidelity | High: the summary is generated from the full history | High only if the scratchpad is up to date before delegation |
| Cost | Lower: one extra turn to generate the summary | Higher: sub-session starts from scratch and may re-ask clarifying questions |
| Appropriate for | Tasks with many remaining steps and a growing but still manageable context | Tasks where the context has become so large that continued work degrades reliability |

The practical rule: summarize early (at 30–40% of the context window), and summarize before starting major new phases of the work. Delegate when the session has been summarized multiple times and is still growing, or when the work naturally divides into phases in which the earlier phase's full transcript is not needed to continue.

## Exercise: Diagnose and respond[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Exercise-Diagnose-and-respond)

Each scenario describes a session state. Identify the correct action.

Technical Quiz

1.

A multi-turn extraction session has run for 28 turns. The API’s `usage.input_tokens` is 67,000. The last three turns show that a client ID cited in the output differs slightly from the one in the case facts block set at turn 1: turn 26 has `ACC-77231`, turn 27 has `ACC-7723I` (capital I instead of digit 1), and turn 28 has `ACC-7723`. Which action is most appropriate?

A.

Increase `max_tokens` to give Claude more room to reproduce the ID correctly

B.

Delete the case facts block and re-enter it at the current position in the conversation

C.

Run a summarization that regenerates the case facts verbatim from the turn-1 block

D.

Start a completely fresh session and re-run all 28 turns from the beginning

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Whats-next)

In the next lesson, we cover information provenance: how to annotate findings with source, confidence, timestamp, and agent role, and how to resolve conflicts between two plausible outputs that arrived through different paths.

Case Facts and Context Placement

Information Provenance

Ask

[Signals that a session is degrading](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Signals-that-a-session-is-degrading)

[The scratchpad pattern](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#The-scratchpad-pattern)

[Conversation summarization](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Conversation-summarization)

[Detecting context pressure from the API response](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Detecting-context-pressure-from-the-API-response)

[Delegation to a sub-session](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Delegation-to-a-sub-session)

[Complete code](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Complete-code)

[When to summarize vs. when to delegate](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#When-to-summarize-vs-when-to-delegate)

[Exercise: Diagnose and respond](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Exercise-Diagnose-and-respond)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/long-session-health#Whats-next)