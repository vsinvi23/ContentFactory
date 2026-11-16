# Session_Strategies_and_Context_Management_for_Agentic_Systems

Source: https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Session Strategy and Context Primer

Explore how to handle context degradation in long-running AI agent sessions by applying four key strategies: resuming, forking, summarizing, and starting fresh. Learn to preserve critical information with the scratchpad pattern and avoid stale data risks. This lesson equips you to manage session lifecycles effectively for reliable agentic system performance.

We'll cover the following...

- [What goes wrong in long sessions](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#What-goes-wrong-in-long-sessions)
- [The four-session strategies](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#The-four-session-strategies)
  - [Resume: Continue where you left off](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Resume-Continue-where-you-left-off)
  - [Fork: Explore without polluting the main session](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Fork-Explore-without-polluting-the-main-session)
  - [Summarize: Compress history to reclaim context space](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Summarize-Compress-history-to-reclaim-context-space)
  - [Clean session: Start fresh when context is a liability](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Clean-session-Start-fresh-when-context-is-a-liability)
- [The scratchpad pattern](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#The-scratchpad-pattern)
- [Stale context: The hidden risk in resumed sessions](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Stale-context-The-hidden-risk-in-resumed-sessions)
- [Exercise: Choose the session strategy](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Exercise-Choose-the-session-strategy)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Whats-next)

The loops we have built so far work on single, self-contained tasks. Production agents often run longer: a debugging investigation that takes 30 turns, a code review that spans multiple files, or a research task that accumulates dozens of tool results. In those sessions, context becomes a resource that must be managed, not just a byproduct of running the loop.

In this lesson, we cover what goes wrong in long sessions, the four session strategies that address different phases of the problem, and the scratchpad pattern that keeps critical information safe across context compression. By the end of this lesson, we will understand:

- The symptoms that indicate context degradation in a running agent
- When to resume a session vs. fork it vs. start fresh
- How `/compact` reduces context size without losing progress
- How a scratchpad file preserves facts that context compression would otherwise discard

## What goes wrong in long sessions[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#What-goes-wrong-in-long-sessions)

Every API call sends the full messages array. As a session runs, that array grows: each tool call adds an assistant turn and a user turn, and each response adds more text. Eventually, the array becomes large enough that early content is compressed or dropped by the model. Context degradation does not announce itself with an error. It shows up as a change in behavior. The four most common indicators are:

- The agent forgets instructions stated early in the session, such as a formatting rule or a constraint from the original task
- Responses become more generic and less specific to the task at hand
- Tool selection accuracy drops, and the agent picks the wrong tool for the situation
- The agent repeats work it has already completed because it no longer has the earlier results in context

These indicators are not bugs in the application code. They are the natural consequence of a context window that is approaching its limit. The messages array is the agent’s entire working memory. When that memory is full, older content yields to newer content.

## The four-session strategies[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#The-four-session-strategies)

There is no single correct response to context degradation. The right strategy depends on where the session is in its life cycle and what the agent is trying to accomplish.

### Resume: Continue where you left off[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Resume-Continue-where-you-left-off)

Resuming a session restores the full conversation history from a previous run. The agent has access to everything that happened before: all tool results, all intermediate findings, and all prior decisions. This is the right choice when a task was interrupted before completion and needs to pick up exactly where it stopped.

In Claude Code, the `--resume` flag handles this:

Ace Editor

1

2

3

4

5

# Resume the most recent session

claude --resume

# Resume a specific named session

claude --resume --session-name "audit-q2-2026"

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The --resume flag restores a previous session with its full context. Named sessions keep multi-session workflows organized when several long-running tasks are in progress simultaneously.

- **Line 2:** `claude --resume` with no arguments resumes the most recently active session.
- **Line 5:** Named sessions (`--session-name`) allow multiple concurrent long-running tasks to be tracked separately. Using a descriptive name makes it clear which task the session belongs to when you resume days later.

The risk with resuming is stale context: data retrieved early in the session may no longer reflect the current state. A database query result from 24 hours ago is still in the messages array, but the database may have changed. To mitigate this, refetch critical data at the start of a resumed session rather than trusting cached results.

### Fork: Explore without polluting the main session[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Fork-Explore-without-polluting-the-main-session)

Forking creates a branch of the current session. The branch starts with the same conversation history as the main session but diverges from that point forward. Changes in the branch do not affect the main session. This is the right choice when the next step involves exploration that might be a dead end: trying an approach that may not work or investigating a hypothesis that may prove wrong.

Ace Editor

1

2

# Fork the current session to explore an alternative

claude fork\_session --reason "Testing schema migration approach B"

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

fork\_session creates a branched copy of the current session. The branch receives a copy of the full conversation history at the point of the fork. The main session continues independently.

- **Line 2:** `fork_session` takes an optional `--reason` argument that labels the branch. The label appears in the session list and makes it easier to identify what each branch represents.

The fork pattern keeps the main session clean. If the exploration in the branch leads nowhere, discard the branch and continue the main session. If it succeeds, bring only the relevant findings back to the main session, not the full exploration transcript.

This is also the correct pattern for independent review tasks. A code review should not run in the same session as the code generation that preceded it: the reviewer retains the generator’s reasoning, which creates confirmation bias. Forking ensures the reviewer starts with the code but not with the rationale.

### Summarize: Compress history to reclaim context space[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Summarize-Compress-history-to-reclaim-context-space)

When the session is mid-task and the context window is approaching its limit, `/compact` compresses the conversation history into a denser summary. The session continues with reduced context overhead, allowing the task to proceed further before the limit is hit again.

In Claude Code:

Ace Editor

1

2

# Compress conversation history mid-session

/compact

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

/compact compresses the current session’s conversation history. The session continues from the compressed state. Recent turns are preserved in more detail; older turns are summarized.

The important limitation of `/compact` is that compression is lossy. Specific tool result values, exact error messages, and precise intermediate findings from early turns may not survive at full fidelity. This is where the scratchpad pattern becomes essential: facts that must survive compression need to be written to an external file before compression runs.

After `/compact`, the agent should reread its scratchpad file to restore the facts that compression may have condensed. This is a standard two-step pattern:

Ace Editor

1

2

3

Before /compact: write current findings to progress.md

Run /compact

After /compact: read progress.md to restore facts into context

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

### Clean session: Start fresh when context is a liability[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Clean-session-Start-fresh-when-context-is-a-liability)

A clean session discards the conversation history entirely and starts from a blank state. This is the right choice when:

- The current session has accumulated so much stale or irrelevant context that the agent is actively confused by it.
- The task has genuinely changed scope, and the prior history is no longer relevant.
- Context quality is so degraded that the cost of continuing exceeds the cost of re-explaining the task.

A clean session is often misread as giving up. It is not. It is a deliberate architectural choice to trade context-based progress for clarity. The key preparation step is to externalize everything worth preserving before starting fresh.

The decision tree below shows when each strategy applies, using the four questions that distinguish them.

![](data:image/svg+xml,%3csvg%20xmlns=%27http://www.w3.org/2000/svg%27%20version=%271.1%27%20width=%27950%27%20height=%27501%27/%3e)![Session strategy decision flow: Choose the right strategy based on your session's needs](data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7 "Session strategy decision flow: Choose the right strategy based on your session's needs")

Session strategy decision flow: Choose the right strategy based on your session's needs

## The scratchpad pattern[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#The-scratchpad-pattern)

Scratchpad files bridge session strategies. They are plain text or Markdown files that the agent writes during a run, and they contain structured summaries of findings that are too important to lose to context compression, a session restart, or subagent delegation.

A scratchpad file is not a log of the full transcript. It is a curated record of the facts that subsequent steps depend on. Here is an example from the memory leak investigation:

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

# Investigation progress — memory-service

\*\*Last updated:\*\* turn 14

## Confirmed findings

- Heap dump shows 340MB growth in `ConnectionPool` objects over 6 hours

- Growth pattern started at 2026-06-08 14:30 UTC

## Deployment correlation

- Deploy #d-4421 merged at 2026-06-08 14:25 UTC (5 min before onset)

- Deploy #d-4421 includes changes to `db/pool.py` and `config/limits.yaml`

## Next step

- Search code changes in deploy #d-4421 for connection lifecycle handling

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A scratchpad file written by an agent mid-investigation. It contains confirmed facts, a causal hypothesis, and the next step — structured to restore full context after a /compact or a session boundary.

- **Lines 2–3:** The header records when the file was last updated. “Turn 14” tells the agent how far into the session this snapshot was taken, which helps assess whether the facts are current.
- **Lines 5–7:** Confirmed findings are specific and quantified. “340MB growth in `ConnectionPool` objects over six hours” is more useful than “there is a memory leak” because it pins the facts precisely enough for the next step to act on them.
- **Lines 9–11:** The deployment correlation is recorded alongside the reasoning. Storing the causal hypothesis, not just the raw facts, means the agent can continue reasoning from where it left off rather than re-deriving the connection.
- **Lines 13–14:** The explicit next step eliminates ambiguity after a resume or a `/compact`. The agent does not need to re-read the full history to know what to do next.

The code below shows how the agent writes and reads this file using a simple tool:

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

import os

def write\_scratchpad(content: str, filename: str = "progress.md") -> str:

with open(filename, "w") as f:

f.write(content)

return f"Scratchpad written to {filename}."

def read\_scratchpad(filename: str = "progress.md") -> str:

if not os.path.exists(filename):

return "No scratchpad file found."

with open(filename, "r") as f:

return f.read()

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Two simple tool functions that give the agent persistent storage outside the context window. Content written here survives /compact, session restarts, and subagent boundaries.

- **Lines 3–6:** `write_scratchpad` takes a Markdown string and writes it to a file. The agent calls this tool when it wants to externalize findings: before a `/compact`, before delegating to a subagent, or before ending a session.
- **Lines 8–11:** `read_scratchpad` reads the file back. The agent calls this at the start of a resumed session, after a `/compact`, or at the start of a new related session to restore the facts it wrote earlier.

These functions are included in the agent’s tool list alongside the domain tools. The agent uses them like any other tool by calling them through the loop when it decides the time is right.

## Stale context: The hidden risk in resumed sessions[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Stale-context-The-hidden-risk-in-resumed-sessions)

Context is stale when the facts in the messages array no longer reflect the current state of the world. A tool result from 12 hours ago may describe a database row that has since been updated. An error message from turn three may describe a service that has since been restarted.

Stale context is dangerous because it is invisible. Claude reads old tool results with the same confidence it reads current ones. There is no timestamp on a message turn and no flag that says “this data is from yesterday.” The agent may act on stale facts without realizing they have changed.

Mitigation starts by identifying which data types are time-sensitive and re-fetching them at the start of any resumed session rather than trusting cached values. Data that changes infrequently, such as system configurations, schema definitions, and static reference data, can safely be used from earlier turns. Data that changes frequently, such as balances, statuses, inventory levels, and error states, should be refreshed before any session that depends on it.

## Exercise: Choose the session strategy[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Exercise-Choose-the-session-strategy)

Read each scenario and choose the correct strategy from the four options.

Technical Quiz

1.

An agent is 20 turns into a debugging investigation. It has confirmed three relevant findings and identified the next step. The context window is at 70% capacity. The team needs to pause and continue tomorrow morning. What is the most appropriate session strategy?

A.

Start a clean session tomorrow; 20 turns is too many to carry forward reliably.

B.

Fork the session before pausing, in case the next step leads to a dead end.

C.

Run `/compact` now before pausing so the session starts tomorrow with a smaller footprint.

D.

Write findings to a scratchpad file, then resume the session tomorrow with `--resume`.

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Whats-next)

In the next lesson, we’ll consolidate this chapter with an assessment quiz that tests architecture decisions (fixed workflow vs. adaptive vs. multi-agent), guardrail placement (prompt vs. code), and session life cycle choices through scenario-based questions.

Guardrails Outside the Prompt

Agentic Architecture Assessment Quiz

Ask

[What goes wrong in long sessions](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#What-goes-wrong-in-long-sessions)

[The four-session strategies](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#The-four-session-strategies)

[Resume: Continue where you left off](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Resume-Continue-where-you-left-off)

[Fork: Explore without polluting the main session](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Fork-Explore-without-polluting-the-main-session)

[Summarize: Compress history to reclaim context space](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Summarize-Compress-history-to-reclaim-context-space)

[Clean session: Start fresh when context is a liability](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Clean-session-Start-fresh-when-context-is-a-liability)

[The scratchpad pattern](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#The-scratchpad-pattern)

[Stale context: The hidden risk in resumed sessions](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Stale-context-The-hidden-risk-in-resumed-sessions)

[Exercise: Choose the session strategy](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Exercise-Choose-the-session-strategy)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/session-strategy-and-context-primer#Whats-next)