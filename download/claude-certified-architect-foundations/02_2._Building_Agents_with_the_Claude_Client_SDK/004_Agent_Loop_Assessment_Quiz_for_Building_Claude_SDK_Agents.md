# Agent_Loop_Assessment_Quiz_for_Building_Claude_SDK_Agents

Source: https://www.educative.io/courses/claude-certified-architect-foundations/agent-loop-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Agent Loop Assessment Quiz

Explore and assess your understanding of agent loops using a multiple-choice quiz. Learn to identify correct engineering steps and output interpretations related to tool calls, stop reasons, conversation ordering, and error handling to build reliable agents with the Claude Client SDK.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/agent-loop-assessment-quiz#Chapter-summary)

Each question describes an agent loop being built or a transcript being analyzed and asks you to choose the next engineering step or interpret what the output shows. Each question has four options and one correct answer, with detailed explanations provided after the full set of 14 questions. Work through the questions before reading the answers.

Technical Quiz

1.

A developer writes an agent loop with a single `if response.stop_reason == "end_turn": return text` branch. There is no branch for `"tool_use"`. The agent is given a task that requires a tool call. What happens?

A.

The tool is never dispatched; the loop either spins indefinitely or exits with a wrong result like `None`.

B.

Claude answers without calling the tool, since no tool branch is available.

C.

The loop raises a `KeyError` because `stop_reason` is not a valid attribute on the response object.

D.

The API blocks the request and returns a 400 error because the tool is defined, but the loop does not handle it.

---

1 / 14

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-foundations/agent-loop-assessment-quiz#Chapter-summary)

Before you move to the next chapter, make sure you can explain these five ideas clearly:

1. Every stop reason needs an explicit branch. A loop without a `"max_tokens"` branch will silently loop or return `None` on truncation. Unhandled stop reasons are silent failures, not safe defaults.
2. The assistant turn must be appended before the tool results. The conversation record is ordered. Tool results have no anchor without the preceding `tool_use` block. This is the most common loop bug and the first thing to check when a loop re-requests tools it has already called.
3. Multiple tool results belong in one `user` turn. When Claude makes two tool calls in one response, both results go into a single `user` message as a list of `tool_result` blocks, not as two separate messages.
4. The `messages=` count in the log is the fastest correctness check. After one complete tool cycle, the count should grow by exactly two (one assistant turn and one user turn). A count one lower than expected means the assistant turn is missing.
5. Error strings from tools are information for Claude, not exceptions for the loop. Return the error as the tool result content. Claude reads it, reasons about it, and produces an appropriate response. The loop should only raise an exception for conditions it cannot recover from, such as an unrecognized tool name or a truncated response.

The next chapter builds on this loop foundation to examine when an agent is the right architecture at all: fixed workflows, adaptive agents, and the programmatic guardrails that make agents safe to deploy.

Debugging the Agent Transcript

Fixed Workflows and Adaptive Agents

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/agent-loop-assessment-quiz#Chapter-summary)