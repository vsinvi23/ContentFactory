# Mastering_Context_Management_Techniques_and_Assessment_Quiz

Source: https://www.educative.io/courses/claude-certified-architect-foundations/context-management-assessment-quiz

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Context Management Assessment Quiz

Explore key context management techniques to keep Claude AI reliable during long sessions. Learn to anchor stable facts, organize information correctly, use scratchpads and summaries, and track provenance. This lesson includes a quiz with realistic scenarios to help you apply concepts for managing context effectively in AI workflows.

We'll cover the following...

- [Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/context-management-assessment-quiz#Chapter-summary)

This quiz covers the techniques from this chapter: anchoring stable facts so they survive context drift, placing different categories of information in the correct context layer, keeping long sessions productive through scratchpads and summarization, and annotating findings with provenance so conflicts can be resolved by tracing each claim to its origin. Each question presents a realistic engineering scenario. Select the single best answer, then check your reasoning against the explanation.

Technical Quiz

1.

A support agent session has run for 35 turns. The opening user message contained the client’s case ID as `CLM-2024-4471`. In turn 28, Claude’s output references `CLM-2024-4471`. In turn 32, the output uses `CLM-20244471`. In turn 35, it uses `CLM-2024-471`. What best explains this pattern?

A.

The model has a known bug that corrupts numeric identifiers after 30 turns

B.

The ID was not in a case facts block and drifted through paraphrase as the session grew

C.

Turn 28 was correct, so the later errors are random one-offs, not a structural problem

D.

The model should be replaced with a larger one that has a longer context window

---

1 / 13

## Chapter summary[#](https://www.educative.io/courses/claude-certified-architect-foundations/context-management-assessment-quiz#Chapter-summary)

Before you move to the next chapter, make sure you can explain these five ideas clearly:

1. Position stable facts at the top of the context, with verbatim instructions adjacent. A case facts block at the top of the system prompt, with a “do not rephrase or approximate” instruction inside the block, anchors IDs, dates, and amounts throughout long sessions. Facts that appear once in the middle of a growing conversation drift through paraphrase propagation.
2. Match the information category to the context layer. Stable per-session facts belong in the system prompt. Per-request documents belong in the user message. Tool outputs and intermediate results belong in the message history and are candidates for trimming. Instructions in the user message can be omitted by mistake; instructions in the system prompt cannot.
3. Scratchpads make progress visible; summaries compress completed work. A scratchpad with anchored facts, a step record, the current active step, and open questions gives Claude a structured view of session state without requiring it to re-read the full conversation. Summarization removes the full text of completed turns while preserving the decisions and values that matter for remaining work.
4. Delegate when repeated summarization stops recovering headroom. Summarization at 30–40% of the context window buys more turns. When a session returns to the same high-context level after multiple summaries, the accumulation rate exceeds what summarization can compress. Sub-session delegation, using the scratchpad as a handoff packet, transfers essential state to a fresh context.
5. Provenance makes conflicts resolvable. Every finding should carry a source, confidence, timestamp, and agent role at the point it is generated. These four fields enable three-tiebreaker conflict resolution (confidence → authority → recency) and allow reviewers to trace any claim to its origin. Provenance lost at a synthesis step cannot be recovered later.

Information Provenance

Escalation and Human Review

Ask

[Chapter summary](https://www.educative.io/courses/claude-certified-architect-foundations/context-management-assessment-quiz#Chapter-summary)