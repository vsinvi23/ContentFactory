# Case_Facts_and_Context_Placement_for_Reliable_Claude_Sessions

Source: https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Master Claude Certified Architect Foundations Exam (CCAR-F)](https://www.educative.io/courses/claude-certified-architect-foundations)

# Case Facts and Context Placement

Explore how to manage context effectively in Claude AI systems by anchoring essential facts, choosing proper context layers, and identifying content that can be trimmed or externalized. Understand why context drift occurs and learn strategies to maintain reliable, verbatim facts across extended conversations and complex workflows.

We'll cover the following...

- [Why context drift happens](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Why-context-drift-happens)
- [The case facts block](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#The-case-facts-block)
- [Context placement by information category](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Context-placement-by-information-category)
- [Verbatim instructions adjacent to facts](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Verbatim-instructions-adjacent-to-facts)
- [Identifying verbose outputs for trimming](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Identifying-verbose-outputs-for-trimming)
- [Exercise: Place the context correctly](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Exercise-Place-the-context-correctly)
- [What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Whats-next)

Context management begins with a simple question: What must Claude get right every single time, and where does that information sit in the context window? In a short session, the answer almost does not matter; Claude will read everything. In a long-running investigation, a document extraction pipeline, or a multi-step support case, context drifts. Stable facts get paraphrased, approximated, or buried under later outputs. The values Claude uses in step 12 may differ subtly from the values established in step two, not because Claude misread them, but because they were positioned where they could be crowded out.

This lesson covers how to anchor facts that must stay verbatim, how to choose where different categories of information belong in the context structure, and how to identify verbose outputs that can be trimmed or externalized without losing the signal that matters. By the end of this lesson, we will be able to:

- Explain why context drift happens and why position in the context window affects fact retention.
- Define a case facts block and identify what belongs in it.
- Choose the correct context layer for different categories of information.
- Identify which outputs can be summarized or externalized and which must remain verbatim.

## Why context drift happens[#](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Why-context-drift-happens)

Claude reads the entire context window before generating a response. Attention is not uniform across the window. Information near the beginning and end of the context tends to be weighted more consistently than information buried in the middle. In a long session, earlier facts migrate toward the middle as the conversation grows: new user messages, tool outputs, and assistant responses push prior content further from both ends.

The problem compounds when facts appear only once, early in the conversation, without explicit anchoring. If a client’s policy number is mentioned in the opening user message and never repeated, Claude may accurately use it in the first three tool calls and then, 10 turns later, confuse it with a number that appeared in a tool response. The error is subtle: the extraction is structurally correct, the format matches, and the discrepancy is only visible when compared against the original case intake.

Three patterns accelerate context drift:

- **Single occurrence:** A fact appears once in the conversation and is not reinforced. As context grows, it competes with similar-looking values.
- **Middle burial:** The fact lands in the middle of a long context window, where attention is weakest, pushed there by accumulating tool outputs and assistant turns.
- **Paraphrase propagation:** Claude summarizes a fact slightly differently across turns. Each paraphrase is approximately correct but introduces small variations. Later tool calls use the paraphrased version rather than the original.

## The case facts block[#](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#The-case-facts-block)

A case facts block is a structured block of verbatim values that must survive intact across all turns of a task. It belongs at the top of the system prompt or at the start of the first user message, before any narrative context, instructions, or tool outputs.

A case facts block for a support investigation:

Ace Editor

1

2

3

4

5

6

7

=== CASE FACTS (do not rephrase or approximate) ===

Customer ID: ACC-77231

Policy number: POL-2024-0091-B

Incident date: 2024-11-14

Claim amount: $14,750.00

Assigned agent: Rivera, M.

=== END CASE FACTS ===

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A case facts block that uses delimiter lines to visually separate the stable values from narrative context. The instruction “do not rephrase or approximate” appears inside the block so it stays adjacent to the facts it governs, even if surrounding text is trimmed.

The block does three things:

1. Positions the facts at the top of the context, where attention is strongest.
2. Uses visual delimiters to signal that this content is structurally different from narrative text.
3. Includes an instruction so that the rule stays with the facts rather than floating separately in the system prompt.

The content of a case facts block is always flat key-value pairs: strings, dates, IDs, amounts, and names. Not summaries. Not interpretations. Not “the customer has a long-standing relationship with the company.” The block holds values that will be referenced directly in tool calls, written into output fields, or compared against documents. If a value could be a tool call argument, it belongs in the block. If it is background color, it does not.

## Context placement by information category[#](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Context-placement-by-information-category)

Different types of information belong in different parts of the context structure. Misplacement does not always cause visible failures immediately; it degrades reliability over time as the session grows. The following placement guidelines apply to both agent loops and extraction pipelines:

|  |  |  |
| --- | --- | --- |
| **Information Type** | **Where it Belongs** | **Why** |
| Stable facts (IDs, dates, amounts, names) | System prompt or top of first user message | Must survive intact across all turns; benefits from top-of-context positioning |
| Task instructions and constraints | System prompt | Persistent across all turns; applies to every response |
| Input documents being processed | User message | Changes per-request; does not belong in system prompt |
| Tool outputs and intermediate results | Message history (as tool results) | Ephemeral; may be summarized or externalized as context grows |
| Prior investigation findings | Scratchpad or summary | Grows over time; needs active management (covered in the next lesson) |
| User requests and clarifications | User message | Per-turn input |

A common misplacement puts task instructions in the user message rather than the system prompt. Instructions in the user message must be re-included in every subsequent turn and can be accidentally omitted. Instructions in the system prompt are always present.

The inverse mistake embeds per-document facts in the system prompt. If the system prompt says “the invoice total is $14,750.00,” that value will be wrong the moment the pipeline processes a different invoice. Per-document facts belong in the user message, not the system prompt.

## Verbatim instructions adjacent to facts[#](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Verbatim-instructions-adjacent-to-facts)

When a value must be reproduced exactly in outputs, a policy reference, a legal citation, or a product SKU, the system prompt should include an explicit verbatim instruction placed directly adjacent to the value:

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

You are a claims processing assistant.

=== POLICY CONSTRAINTS (apply to every output) ===

Coverage exclusion ref: EXCL-48B

Policy version: 2024-Q3

Jurisdiction: DE-NV-dual

These references must appear verbatim in any coverage determination output.

=== END POLICY CONSTRAINTS ===

Your task is to review the provided claim documents and produce a coverage determination.

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

A system prompt that places policy references in a delimited block. The verbatim instruction is inside the block, adjacent to the values — not separated by paragraphs of other text.

Adjacency matters. A verbatim instruction at the top of the system prompt, separated from the relevant values by hundreds of tokens, does not reliably bind to those values. A verbatim instruction placed immediately after the values it governs is unambiguous: this specific text must appear exactly as written.

Without the verbatim instruction, Claude treats the reference as approximate guidance and normalizes freely. `EXCL-48B` becomes `Exclusion 48B` in one turn and `Exclusion clause EXCL48B` in another. Both are semantically close, but neither is the authoritative identifier. Downstream systems that parse for the exact string will fail silently.

## Identifying verbose outputs for trimming[#](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Identifying-verbose-outputs-for-trimming)

Not everything in the context needs to remain verbatim. Long tool outputs, verbose intermediate results, and extended reasoning accumulate and compete with the facts that must stay intact. Identifying what can be trimmed is as important as identifying what cannot. A framework for deciding what to trim:

|  |  |  |
| --- | --- | --- |
| **Output type** | **Can it be trimmed or summarized?** | **Notes** |
| Raw document text (after extraction) | Yes | Keep the extracted fields; trim the source document once extraction is complete |
| Tool call stdout (long shell output) | Yes | Keep exit code, error message if any, and key lines; trim repetitive output |
| Reasoning traces | Yes | Intermediate chain-of-thought can be summarized after a decision is made |
| Extracted values used downstream | No | Must stay verbatim; these are the inputs to downstream tool calls |
| Error messages from failed tool calls | Conditional | Keep error type and message; trim stack traces |
| Prior assistant responses | Summarize, not verbatim | The fact that an earlier step completed is useful; the full response usually is not |

The governing rule is to trim anything that was a means to an end, not the end itself. The raw document was a means of extraction. The extraction is the end. The shell output was a means of detecting an error. The error type and message are the end.

Externalization is a related strategy: instead of trimming in context, the output is written to a file or memory store and replaced with a short reference in the context. The full content remains available if needed but no longer consumes context window space. Externalization is appropriate for large intermediate documents, reference tables, and accumulated findings from earlier turns.

## Exercise: Place the context correctly[#](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Exercise-Place-the-context-correctly)

Each scenario describes a context design choice. Identify the correct placement or the appropriate action.

Technical Quiz

1.

A multi-turn support agent processes insurance claims. Each session involves a fixed policy number provided at session start, a set of task instructions, and a series of documents the agent reviews one at a time. Where should the policy number be placed?

A.

In the user message, repeated before each document the agent reviews

B.

In a case facts block in the system prompt, with a verbatim instruction

C.

In the first tool call result, so it is grounded in retrieved data from the start

D.

In the `CLAUDE.md` file, so it applies to all sessions globally

---

1 / 4

## What’s next?[#](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Whats-next)

In the next lesson, we cover long-session health: how to use scratchpads and summaries to keep progress visible without overloading the context, when to delegate work to a sub-session, and the signals that indicate a session is approaching the point where continued work degrades reliability.

Validation and Metrics Assessment Quiz

Long Session Health

Ask

[Why context drift happens](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Why-context-drift-happens)

[The case facts block](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#The-case-facts-block)

[Context placement by information category](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Context-placement-by-information-category)

[Verbatim instructions adjacent to facts](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Verbatim-instructions-adjacent-to-facts)

[Identifying verbose outputs for trimming](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Identifying-verbose-outputs-for-trimming)

[Exercise: Place the context correctly](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Exercise-Place-the-context-correctly)

[What’s next?](https://www.educative.io/courses/claude-certified-architect-foundations/case-facts-and-context-placement#Whats-next)